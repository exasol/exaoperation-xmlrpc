# -*- coding: utf-8 -*-
import xmlrpc.client, ssl, time, os, sys
import base64
import argparse
import subprocess
import requests
import logging
import getpass
import urllib3
from datetime import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder

UPLOAD_TIMEOUT = 60 * 20
LS_TIMEOUT = 0

# add args
parser = argparse.ArgumentParser(description='Update EXASuite automatically')
required_args = parser.add_argument_group('Required arguments')
required_args.add_argument('--timeout', default=15, help='Timeout for upgrading the management node in minutes - DEFAULT: 5minutes')
required_args.add_argument('--protocol', default='https', choices=['https', 'http'], help='Communication protocol, https or http - DEFAULT: https')
required_args.add_argument('--user', default='admin', help='Username to login to EXAoperation - DEFAULT: admin')
required_args.add_argument('--password', help='Password of the given username')
required_args.add_argument('--credentials', help='EXAOperation user credentials in base64 encoded value - Ex. encoded user:password')
required_args.add_argument('--ip', help='IP address of license node, private or public ones')
required_args.add_argument('--node_ips', nargs='+', help='List of ip addresses of cluster nodes, private or public ones')
required_args.add_argument('--port', default=443, help='Port number of license node - DEFAULT: 443')
required_args.add_argument('--packages', nargs='+', help='List of package paths')
optional_args = parser.add_argument_group('Optional arguments')
optional_args.add_argument('--loglevel', nargs='?', const=20, default=20, help='Logging level - DEFAULT: 20 - DEBUG')
optional_args.add_argument('--dest', nargs='?', const='/tmp/', default='/tmp/', help='The destination directory, where the update packages should be copied and uploaded. If the given directoy does not exist, it will be created. This directory will be removed after the update. - DEFAULT: /tmp/')


# init logger
def init_logger(LOGGING_LEVEL):
    LOG_FORMAT = '[%(asctime)s]  %(message)s'
    LOG_DATE = datetime.now().strftime("%Y%m%d_%H%M%S")
    LOG_NAME = 'update_script_logs_' + LOG_DATE + '.log'
    logging.basicConfig(filename=LOG_NAME, format=LOG_FORMAT, filemode='w', level=logging.INFO)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))

    file_handler = logging.FileHandler(LOG_NAME, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger = logging.getLogger(LOG_NAME)
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    logger.info('LOGS STARTED...')
    return logger

# ssl function
def ssl_server_proxy(url):
    func_name = ssl_server_proxy.__name__
    if hasattr(ssl, 'SSLContext'):
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        sslcontext.check_hostname = False
        sslcontext.verify_mode = ssl.CERT_NONE
        return xmlrpc.client.ServerProxy(url, allow_none=True, context=ssl._create_unverified_context())
    return xmlrpc.client.ServerProxy(url, allow_none=True)

def prepare_update(cluster, cluster_path, storage, LS_TIMEOUT, logger):
    func_name = prepare_update.__name__

    # delete obsolete versions
    obsolete_versions = cluster.getObsoleteEXASuiteVersions()
    if obsolete_versions is not None:
        logger.info('%s: List of obsolete versions: %s', func_name, str(obsolete_versions))
        for version in obsolete_versions:
            cluster.removeObsoleteEXASuite(version)
            logger.info('%s: Obsolete version deleted: %s', func_name, str(version))
    else:
        logger.info('%s: There are no obsolete versions to be deleted', func_name)

    # check db backups and shutdown all dbs
    dbs = cluster.getAllDatabases()
    if len(dbs) != 0:
        logger.info('%s: Shutting down following databases: %s', func_name, str(dbs))
    for db_name in dbs:
        logger.info('%s: Database name: %s', func_name, db_name)
        db = ssl_server_proxy(cluster_path + '/' + db_name)
        try:
            db.shutdownDatabase()
        except:
            logger.exception('%s: Cannot shutdown database %s', func_name, db_name)

        timeout = time.time() + LS_TIMEOUT
        while db.getDatabaseConnectionState() != 'No':
            if time.time() > timeout:
                logger.error('%s: Timeout while shutting down database %s', func_name, db_name)
                return 1
            else:
                time.sleep(20)
    logger.info('%s: Databases are offline now',func_name)

    # restart EXAop on license node
    if not str(cluster.getCurrentLicenseServer()) in cluster.getEXAoperationMaster():
        timeout = time.time() + LS_TIMEOUT
        new_exaop_node = min(cluster.getEXAoperationNodes())
        try:
            cluster.restartEXAoperation(new_exaop_node)
        except Exception:
            pass
        while True:
            if time.time() > timeout:
                logger.error('%s: Cannot restart EXAoperation on license node', func_name)
                exit(1)
            if cluster.getEXAoperationMaster() == new_exaop_node:
                break
            else:
                time.sleep(10)
    logger.info('%s: Restarted EXAoperation on license node', func_name)

    # shutdown EXAStorage
    try:
        storage.stopEXAStorage()
    except Exception:
        logger.exception('%s: Cannot stop storage', func_name)

    timeout = time.time() + LS_TIMEOUT
    while storage.serviceIsOnline():
        if time.time() > timeout:
            logger.error('%s: Timeout while waiting for storage to shutdown', func_name)
            return 1
        else:
            time.sleep(10)
    logger.info('%s: EXAStorage is offline now', func_name)

    #stop cluster service on all nodes
    if str(cluster.getEXAoperationMaster()) not in cluster.getNodeList():
        for node_name in cluster.getNodeList():
            node = ssl_server_proxy(cluster_path + '/' + node_name)
            if node.getNodeState()['status'] != 'Unknown':
                node.stopClusterServices()
                timeout = time.time() + LS_TIMEOUT
                while node.getNodeState()['status'] != 'Suspended':
                    if time.time() > timeout:
                        logger.error('%s: Timeout while suspending node %s', func_name, node_name)
                        return 1
                    else:
                        time.sleep(10)
            else:
                logger.info('%s: Stopping cluster service for node: %s is skipped, node state is: %s', func_name, node_name, node.getNodeState()['status'])
        logger.info('%s: Stopped cluster service on all running nodes', func_name)
    else:
        logger.info('%s: Single node used...', func_name)
    return 0

def upload_package(cluster, dest_path, pkg_names, protocol, management_node_ip, user, password, port, logger):
    func_name = upload_package.__name__
    for pckg in pkg_names:
        logger.info('%s: Uploading %s', func_name, pckg)	
        pckg_dest_path = dest_path + pckg
        url = '{}://{}:{}/'.format(protocol, management_node_ip, port)
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, headers=headers, verify=False)
        cookie ='; '.join([x.name + '=' + x.value for x in response.cookies])
        cookie_split = cookie.split(';')[0].split('=')[1]
        encoder = MultipartEncoder(fields={"software_upload_file": (pckg, open(pckg_dest_path, 'rb'), 'application/octet-stream'), 'update_submit_button': '', '__csrftoken__': cookie_split})
        headers['Cookie'] = cookie
        headers['Content-Type'] = encoder.content_type
        response = requests.post(url + 'cluster1/software.html', auth=(user, password), data = encoder, headers=headers, verify = False)
        logger.info('{}: Request status code for package upload: {} is: {}'.format(func_name, pckg, response.status_code))
        if response.status_code != 200:
            return 1
        return 0 

def reboot_and_restart(cluster, cluster_path, storage, current_installation_history, LS_TIMEOUT, LS_UPDATE_FOUND, logger):
    func_name = reboot_and_restart.__name__
    # reboot license server
    license_server_num = int(cluster.getCurrentLicenseServer())
    if license_server_num < 99:
        license_server = 'n00' + str(license_server_num)
    elif license_server_num > 99 and license_server_num <= 999:
        license_server = 'n0' + str(license_server_num)
    elif license_server_num > 999:
        license_server = 'n' + str(license_server_num)
    try:
        cluster.restartLicenseServer(license_server)
    except Exception as e:
        logger.info('Wait until cluster is restarting. It can take up to 10mins...')
        logger.exception('%s: %s', func_name, e)

    # it usually takes up to 6 minutes to start the license server
    node_unknown = []
    i = 1
    timeout = time.time() + (i * 10 * 60)
    while True:
        if time.time() > timeout:
            logger.info('%s: %s minutes have passed and license server is not yet available, please wait...', func_name, str(i * 10))
            i = i + 1
            timeout = time.time() + (i * 10 * 60)
        try:
            cluster.getInstallationHistory()
            logger.info('%s: Cluster has been restarted!', func_name)
        except Exception:
            time.sleep(20)
        else:
            break
        

    # check installation history
    histories = cluster.getInstallationHistory()
    for his in histories:
        logger.info('%s: Installation histories: %s', func_name, his)
    if len(histories) <= len(current_installation_history):
        logger.error('%s: Upgrade is not successful, installation histories has no change, please restart upload', func_name)
        return 1
    logger.info('%s: Installation histories are ok', func_name)

    # # reboot cluster nodes
    if str(cluster.getEXAoperationMaster()) not in cluster.getNodeList():
        for node_name in cluster.getNodeList():
            node = ssl_server_proxy(cluster_path + '/' + node_name)
            if node.getNodeState()['status'] != 'Unknown':
                try:
                    node.rebootNode()
                    logger.info("%s: Rebooting node: %s", func_name, node_name)
                except Exception:
                    logger.info('%s: Cannot reboot node: %s...', func_name, node_name)
                    time.sleep(10)
                    continue
            else:
                node_unknown.append(node_name)
                logger.info('%s: Rebooting node: %s skipped as node state is: %s', func_name, node_name, node.getNodeState()['status'])
    else:
        logger.info('%s: Single node used. No cluster nodes to reboot!', func_name)

    time.sleep(20)
    
    if str(cluster.getEXAoperationMaster()) not in cluster.getNodeList():
        timeout = time.time() + LS_TIMEOUT
        node_list = []
        while True:
            if time.time() > timeout:
                logger.error('%s: Timeout: Cannot get access to cluster', func_name)
                return 1
            try:
                node_list = cluster.getNodeList()
            except Exception:
                logger.info('%s: Cannot get access to cluster, waiting...', func_name)
                time.sleep(30)
            else:
                break

        up_node_count = 0
        for node_name in node_list:
            node = ssl_server_proxy(cluster_path + '/' + node_name)
            logger.info('%s: Check node state of %s', func_name, node_name)
            if node_name not in node_unknown:
                timeout = time.time() + (15 * 60)
                while True:
                    if time.time() > timeout:
                        logger.error('%s: Timeout while rebooting node: %s', func_name, node_name)
                        break
                    try:
                        if node.getNodeState()['status'] == 'Running':
                            logger.info('%s: Node %s is running', func_name, node_name)
                            up_node_count = up_node_count + 1
                            break
                    except Exception as e:
                        logger.info('%s: check node state: %s', func_name, e)
                        continue
            else:
                logger.info('%s: Node %s is in Unknown state', func_name, node_name)

        if len(node_list) == up_node_count:
            logger.info('%s: All nodes are running', func_name)

    # startup EXAStorage
    if str(cluster.getEXAoperationMaster()) not in cluster.getNodeList():
        try:
            logger.info('%s: Starting EXAStorage service...', func_name)
            storage.startEXAStorage()
        except Exception:
            logger.exception('%s: Cannot start storage', func_name)
    else:
        logger.info('%s: Single node used, storage service has been started at boot time...', func_name)

    timeout = time.time() + LS_TIMEOUT
    while storage.serviceIsOnline() is False:
        if time.time() > timeout:
            logger.error('%s: Timeout: Storage service could not started...', func_name)
            break
        else:
            logger.info('%s: Wait until storage service is online...')
            time.sleep(10)

    # start EXAoperation plugins
    if cluster.havePlugins() == True:
        logger.info('%s: Starting cluster plugins...', func_name)
        plugins = cluster.getPlugins()
        for plugin in plugins:
            logger.info('%s: Starting plugin: %s', func_name, str(plugin))
            cluster.callPlugin(plugin, license_server, 'START')
    logger.info('%s Installation histories: ', func_name)
    for history in histories:
        logger.info('%s:    %s', func_name, history)

    # start all dbs
    dbs = cluster.getAllDatabases()
    
    if len(dbs) != 0:
        logger.info('%s: Starting following databases: %s', func_name, str(dbs))
    for db_name in dbs:
        logger.info('%s: Database name: %s', func_name, db_name)
        db = ssl_server_proxy(cluster_path + '/' + db_name)
        if LS_UPDATE_FOUND:
            timeout = time.time() + LS_TIMEOUT
            update_version = {'database_version' : str(cluster.getEXACOSVersion()).split(' ')[0]}
            logger.info('%s: Database update has been tracked, editing database version from %s to %s', func_name, str(db.getProperties()['database_version']), str(cluster.getEXACOSVersion()).split(' ')[0])
            try:
                db.editDatabase(update_version)
            except:
                logger.exception('%s: Cannot edit database %s', func_name, db_name)
            while str(cluster.getEXACOSVersion()).split(' ')[0] != db.getProperties()['database_version']:
                if time.time() > timeout:
                    logger.info('%s: Timeout editing database!')
                    break
                else:
                    logger.info('%s: Please wait until database editing is finished...')
                    time.sleep(10)
        try:
            db.startDatabase()
        except:
            logger.exception('%s: Cannot start database %s', func_name, db_name)

        timeout = time.time() + LS_TIMEOUT
        while db.getDatabaseConnectionState() != 'Yes':
            if time.time() > timeout:
                logger.error('%s: Timeout while starting database %s', func_name, db_name)
                return 1
            else:
                time.sleep(20)
    logger.info('%s: Databases are up now',func_name)


def clean_up(dest_path, pkg_paths, logger):
    func_name = clean_up.__name__
    if dest_path[-1] != '/':
        dest_path = dest_path + '/'
    for pkg in pkg_paths:
        pkg_name = pkg.split('/')[-1]
        try:
            subprocess.run('rm {0}/{1}'.format(dest_path, pkg_name), shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.info('Something went wrong removing package from directory:{}. Return code: {}, output: {}'.format(dest_path, e.returncode, e.output))
    logger.info('%s: cleanup done', func_name)


def main():
    """main entry point"""

    func_name = main.__name__
    args = parser.parse_args()

    if args.credentials is not None:
        decoded_creds = base64.b64decode(args.credentials).decode("utf-8").split(':')
        user_pass = len(decoded_creds)
        if user_pass == 1:
            args.password = getpass.getpass('{} password: '.format(decoded_creds[0]))
        elif user_pass == 2:
            args.user = decoded_creds[0]
            args.password = decoded_creds[1]
        else:
            print('Please give base64 encoded username and password in correct form!')
            parser.print_help()
            sys.exit(1)
    else:
        if args.password is None:
            args.password = getpass.getpass('{} password: '.format(args.user))


    LS_UPDATE_FOUND = False
    LS_TIMEOUT = int(args.timeout) * 60
    LOGGING_LEVEL = args.loglevel
    DEST_PATH = args.dest

    logger = init_logger(LOGGING_LEVEL)
    cluster_path = '{0}://{1}:{2}@{3}:{4}/cluster1'.format(args.protocol, args.user, args.password, args.ip, args.port)

    try:
        subprocess.run('mkdir {0}'.format(DEST_PATH), shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.info('{}'.format(e))

    # create cluster and storage objects
    cluster = ssl_server_proxy(cluster_path)
    if cluster.listObjects() is None:
        logger.error('%s: Database Connection String error', func_name)
        sys.exit(1)
    
    storage_path = cluster_path + '/storage'
    storage = ssl_server_proxy(storage_path)

    current_installation_history = cluster.getInstallationHistory()

    # store the input package names
    pkg_names = []
    pkg_paths = args.packages
    
    # prepare update
    ret = prepare_update(cluster, cluster_path, storage, LS_TIMEOUT, logger)
    if ret == 1:
        clean_up(DEST_PATH, pkg_paths, logger)
        exit(1)

    # sort package paths
    # example of links:
    # https://x-up.s3.amazonaws.com/7.x/7.1.30/EXAClusterOS-7.1.30_LS-Update.pkg
    #
    # do upload, LS_UPDATE will be installed firstly
    for pkg in pkg_paths:
        if 'LS-Update' in pkg:
            LS_UPDATE_FOUND = True
            pkg_paths.remove(pkg)
            pkg_paths.insert(0, pkg)
    for pkg_path in pkg_paths:
        logger.info('%s: Package path: %s', func_name, pkg_path)
        # read package path from command line and upload to cluster
        # if it is a http path
        if pkg_path[0:4] == 'http' or pkg_path[0:3] == 'ftp':
            logger.info('%s: download started', func_name)
            pkg_name = pkg_path.split('/')[-1]
            os.system('wget ' + pkg_path + ' -P ' + DEST_PATH)
            # add pkg name to list of package names
            pkg_names.append(pkg_name)
            logger.info('%s: Download ended', func_name)
        else:
            logger.info('%s: Package location is file or local', func_name)
            pkg_name = pkg_path.split('/')[-1]
            logger.info('%s: Moving local pkg to %s', func_name, DEST_PATH)
            try:
                subprocess.run('cp {0} {1}'.format(pkg_path, DEST_PATH), shell=True, check=True)
            except subprocess.CalledProcessError as e:
                logger.info('Something went wrong coping package:{} to destination directory: {}. Return code: {}, output: {}'.format(pkg_path, DEST_PATH, e.returncode, e.output))
            logger.info('%s: Moving done', func_name)
            pkg_names.append(pkg_name)

        pwd = p if args.password is None else args.password
        ret = upload_package(cluster, DEST_PATH, pkg_names, args.protocol, args.ip, args.user, pwd, args.port, logger)
        if ret == 1:
            logger.info('%s: Upload failed!', func_name)
            return 1
        timeout = time.time() + LS_TIMEOUT
        if 'LS-Update' in pkg_path:
            logger.info('%s: Database update found, please wait until the update is ready...', func_name)
            while True:
                if "First part of update process succeeded" in cluster.getUploadPackageState():
                    break
                else:
                    if time.time() > timeout:
                        logger.info('%s: Timeout installing database update...', func_name)
                        return 1
            
            logger.info('%s: Database update has been installed!', func_name)

        if ret == 1:
            if pkg_path[0:4] == 'https' or pkg_path[0:3] == 'ftp':
                clean_up(DEST_PATH, pkg_paths, logger)
            continue

        if pkg_path[0:4] == 'https' or pkg_path[0:3] == 'ftp':
            clean_up(DEST_PATH, pkg_paths, logger)

    # startup after update
    ret = reboot_and_restart(cluster, cluster_path, storage, current_installation_history, LS_TIMEOUT, LS_UPDATE_FOUND, logger)
    if ret == 1:
        clean_up(DEST_PATH, pkg_paths, logger)
        sys.exit(1)

if __name__ == '__main__':
    main()