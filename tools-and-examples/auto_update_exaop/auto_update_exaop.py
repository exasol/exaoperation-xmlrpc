# -*- coding: utf-8 -*-
import xmlrpclib, ssl, time, os, sys
import base64
import argparse, commands
import requests
import logging

UPLOAD_TIMEOUT = 60 * 20
LS_TIMEOUT = 0

# 10 = DEBUG, 20 = INFO
LOGGING_LEVEL = 20

# destination path of packages to be uploaded
DEST_PATH = None

# add args
parser = argparse.ArgumentParser(description='Update EXASuite automatically')
#parser.add_argument('--dest', help="destination path to store downloaded package")
required_args = parser.add_argument_group('Required arguments')
required_args.add_argument('--timeout', help='Timeout for upgrading the management node in minutes')
required_args.add_argument('--protocol', help='Communication protocol, https or http')
required_args.add_argument('--user', help='Username to login to EXAoperation')
required_args.add_argument('--password', help='Password of the given username')
required_args.add_argument('--ip', help='IP address of license node')
required_args.add_argument('--node_ips', nargs='+', help='List of ip addresses of cluster nodes')
required_args.add_argument('--port', help='Port number of license node')
required_args.add_argument('--packages', nargs='+', help='List of package paths')
required_args.add_argument('--loglevel', nargs='?', const=20, default=20, help='Logging level, default value 20')
required_args.add_argument('--dest', nargs='?', const='/tmp/', default='/tmp/', help='The destination directory, where the update packages should be copied and uploaded. If the given directoy does not exist, it will be created. This directory will be removed after the update. Default destination /tmp/')


# init logger
FORMAT = '[%(asctime)s]  %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('EXAoperation update')
logger.setLevel(LOGGING_LEVEL)

# ssl function
def ssl_server_proxy(url):
    func_name = ssl_server_proxy.__name__
    if hasattr(ssl, 'SSLContext'):
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        sslcontext.verify_mode = ssl.CERT_NONE
        sslcontext.check_hostname = False
        return xmlrpclib.ServerProxy(url, context = sslcontext, allow_none = True)
    return xmlrpclib.ServerProxy(url, allow_none = True)

def prepare_update(cluster, cluster_path, storage):
    func_name = prepare_update.__name__

    # check db backups and shutdown all dbs
    dbs = cluster.getAllDatabases()
    if len(dbs) != 0:
        logger.info('%s: Shutting down following databases: %s', func_name, str(dbs))
    for db_name in dbs:
        logger.info('%s: Database name: $s', func_name, db_name)
        db = ssl_server_proxy(cluster_path + '/' + db_name)
        backup = db.getBackupSchedule()
        if len(backup) != 0:
            logger.error('%s: Backup/Restore should be none on %s', func_name, db_name)
            return 1
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
    for node_name in cluster.getNodeList():
        node = ssl_server_proxy(cluster_path + '/' + node_name)
        node.stopClusterServices()
        timeout = time.time() + LS_TIMEOUT
        while node.getNodeState()['status'] != 'Suspended':
            if time.time() > timeout:
                logger.error('%s: Timeout while suspending node %s', func_name, node_name)
                return 1
            else:
                time.sleep(10)
    logger.info('%s: Stopped cluster service on all nodes', func_name)
    return 0

def upload_package(cluster, pkg_dest_path):
    func_name = upload_package.__name__
    logger.info('%s: Uploading %s', func_name, pkg_dest_path)	
    # upload package
#    session = requests.session()
#    csrftoken = session.get(software_https_path).cookies['__csrftoken__']
#    response = session.post(software_https_path, data = {'__csrftoken__': csrftoken, 'update_submit_button': '1'}, files = {'software_upload_file': open(pkg_dest_path)})
#    if response.status_code != 200:
#        logger.error('%s: Response code of upload package is %s', func_name, str(response.status_code))
#        return 1
#    else:
#        logger.info('%s: Uploaded package', func_name)
#        return 0
    try:
        p = xmlrpclib.Binary(open(pkg_dest_path).read())
        cluster.uploadSoftware(p)
    except Exception as e:
        logger.exception('%s: %s', func_name, e)
        return 1
	logger.info('%s: Upload %s done', func_name, pkg_dest_path)
    return 0

        # try:
    #     cluster.uploadSoftware(pkg_dest_path)
    # except Exception, e:
    #     print("upload failed %s" % e)
    #     return 1

def reboot_and_restart(cluster, cluster_path, storage, current_installation_history, node_ips):
    func_name = upload_package.__name__
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
        logger.exception('%s: %s', func_name, e)

    timeout = LS_TIMEOUT * 2
    while True:
        if time.time() > timeout:
            logger.error('%s: Timeout while restarting license server, please check license server manually', func_name)
            break
        try:
            cluster.getInstallationHistory()
        except Exception:
            time.sleep(20)
        else:
            break

    # check installation history
    histories = cluster.getInstallationHistory()
    for his in histories:
        logger.info('%s: Installation histories: ', func_name, his)
    if len(histories) <= len(current_installation_history):
        logger.error('%s: Upgrade is not successful, installation histories has no change, please restart upload', func_name)
        return 1
    logger.info('%s: Installation histories are ok', func_name)


    # # reboot cluster nodes
    # for node_name in cluster.getNodeList():
    #     node = ssl_server_proxy(cluster_path + '/' + node_name)
    #     try:
    #         node.rebootNode()
    #         logger.info("%s: Rebooting node: %s", func_name, node_name)
    #     except Exception:
    #         sleep(10)
    #         continue

    # reboot cluster nodes via ssh
    for node in node_ips:
        sts, out = commands.getstatusoutput('ssh {0} -p 20 reboot'.format(node))
        if sts != 0:
            logger.exception('%s: Cannot reboot %s', func_name, node)
            sleep(10)
            continue

    time.sleep(20)
    
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

    timeout = time.time() + LS_TIMEOUT
    up_node_count = 0
    while True:
        if time.time() > timeout:
            logger.error('%s: Timeout while rebooting nodes', func_name)
            break
        for node_name in cluster.getNodeList():
            node = ssl_server_proxy(cluster_path + '/' + node_name)
            logger.info('%: Check node state of %s', func_name, node_name)
            try:
                if node.getNodeState() == 'Running':
                    logger.info('%s: Node %s is running', func_name, node_name)
                    up_node_count = up_node_count + 1
            except Exception as e:
                logger.info('%s: check node state: %s', func_name, e)
                continue
        if up_node_count == len(cluster.getNodeList()):
            logger.info('%s: All nodes are running', func_name)
            break
        else:
            logger.info('%s: Nodes are not yet all running, waiting...', func_name)
            up_node_count = 0
            time.sleep(60)
    logger.info('%s: Rebooted all nodes', func_name)

    # startup EXAStorage
    try:
        storage.startEXAStorage()
    except Exception:
        logger.exception('%s: Cannot start storage', func_name)

    timeout = time.time() + LS_TIMEOUT
    while storage.serviceIsOnline() is False:
        if time.time() > timeout:
            logger.error('%s: Timeout while starting storage service', func_name)
            break
        else:
            time.sleep(10)

    # start EXAoperation plugins
    if cluster.havePlugins() == True:
        plugins = cluster.getPlugins()
        for plugin in plugins:
            cluster.callPlugin(plugin)
    logger.info('%s Installation histories: ', func_name)
    for history in histories:
        logger.info('%s:    %s', func_name, history)

def clean_up(dest_path):
    func_name = clean_up.__name__
    #os.system('rm -Rf ' + dest_path)
    logger.info('%s: cleanup done', func_name)


def main():
    """main entry point"""

    func_name = main.__name__
    args = parser.parse_args()

    LS_TIMEOUT = args.timeout * 60
    LOGGING_LEVEL = args.loglevel
    DEST_PATH = args.dest
    cluster_path = '{0}://{1}:{2}@{3}:{4}/cluster1'.format(args.protocol, args.user, args.password, args.ip, args.port)
    #software_https_path = '{0}://{1}:{2}@{3}:{4}/cluster1/software.html'.format('http', args.user, args.password, args.ip, 1080)
    if args.protocol is None or args.user is None or args.password is None or args.ip is None or args.port is None:
        parser.print_help()
        exit(1)
    sts, out = commands.getstatusoutput('mkdir {0}'.format(DEST_PATH))
    if sts != 0:
        logger.error('%s: Cannot create %s: %s', func_name, DEST_PATH, out)

    # get cluster node ip
    node_ips = args.node_ips

    # create cluster and storage objects
    cluster = ssl_server_proxy(cluster_path)
    if cluster.listObjects() is None:
        logger.error('%s: Database Connection String error', func_name)
        exit(1)
    storage_path = cluster_path + '/storage'
    storage = ssl_server_proxy(storage_path)

    current_cos_version = str(cluster.getEXACOSVersion())
    current_installation_history = cluster.getInstallationHistory()

    # store the input package names
    pkg_names = []
    pkg_paths = args.packages

    exit(0)

    # prepare update
    ret = prepare_update(cluster, cluster_path, storage)
    if ret == 1:
        clean_up(DEST_PATH)
        exit(1)

    # sort package paths
    # example of links:
    # https://www.exasol.com/support/secure/attachment/55195/EXAClusterOS-6.0.4_LS-Update.pkg
    # https://www.exasol.com/support/secure/attachment/65453/EXASOL-6.0-CentOS-6-CumulativeUpdate-16.pkg
    # do upload, LS_UPDATE will be installed firstly
    for pkg in pkg_paths:
        if 'LS-Update' in pkg:
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
            pkg_dest_path = DEST_PATH + '/' + pkg_name
            # add pkg name to list of package names
            pkg_names.append(pkg_name)
            logger.info('%s: Download ended', func_name)
        else:
            logger.info('%s: Package location is file or local', func_name)
            pkg_name = pkg_path.split('/')[-1]
            logger.info('%s: Moving local pkg to /%s', func_name, DEST_PATH)
            sts, out = commands.getstatusoutput('cp {0} {1}'.format(pkg_path, DEST_PATH))
            if sts != 0:
                logger.error('%s: Cannot save package %s to %s: %s', func_name, pkg_path, DEST_PATH, out)
                continue
            logger.info('%s: Moving done', func_name)
            pkg_dest_path = DEST_PATH + pkg_name

        #run_ret = run_update(cluster, cluster_path, software_https_path, storage, pkg_dest_path, current_cos_version, current_installation_history)
        ret = upload_package(cluster, pkg_dest_path)
        
        if ret == 1:
            if pkg_path[0:4] == 'https' or pkg_path[0:3] == 'ftp':
                clean_up(DEST_PATH)
            continue

        if pkg_path[0:4] == 'https' or pkg_path[0:3] == 'ftp':
            clean_up(DEST_PATH)

    # startup after update
    ret = reboot_and_restart(cluster, cluster_path, storage, current_installation_history, node_ips)
    if ret == 1:
        clean_up(DEST_PATH)
        exit(1)

if __name__ == '__main__':
    main()
