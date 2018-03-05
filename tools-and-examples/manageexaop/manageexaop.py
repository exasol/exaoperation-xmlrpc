#!/usr/bin/python
import os.path, re, xmlrpclib, base64, ssl
from pprint import pprint
from sys import exit, argv, version_info, stdout
from getopt import getopt
from urllib import quote_plus
from pipes import quote
from subprocess import check_output, Popen, PIPE, STDOUT
from tempfile import NamedTemporaryFile
from datetime import datetime
from time import sleep

opts, args = None, None
try:
    opts, args = getopt(argv[1:],'hsodl:u:p:v:i:j:')
except:
    print "Unknown parameter(s): %s" % argv[1:]
    opts = []
    opts.append(['-h', None])


startupCluster = False
shutdownCluster = False
debugMode = False
licenseServerIp = None
userName = None
password = None
vpcId = None
instanceList = None
jhInstance = None

for opt in opts:
    parameter = opt[0]
    value = opt[1]
    if parameter == '-h':
        print """
    Options:
        -h                  shows this help
        -s                  start up cluster
        -o                  shutdown cluster
        -d                  trigger more output for debugging purposes
        -l <license server>
        -u <exaoperation user>
        -p <exaoperation pwd>
        -v <vpc id>
        -i <instances>
        -j <jump host instance>
"""
        exit(0)
    elif parameter == '-s':
        startupCluster = True

    elif parameter == '-o':
        shutdownCluster = True

    elif parameter == '-d':
         debugMode = True
    
    elif parameter == '-l':
        licenseServerIp = value

    elif parameter == '-u':
        userName = value

    elif parameter == '-p':
        password = value

    elif parameter == '-v':
        vpcId = value

    elif parameter == '-i':
        instanceList = value.split(',')

    elif parameter == '-j':
        jhInstance = value

if startupCluster and shutdownCluster:
    print "Cannot startup and shutdown the cluster at the same time."
    exit(2)

elif not (startupCluster or shutdownCluster):
    print "Please specify one of those options: -s or -o"
    exit(2)

elif shutdownCluster and not jhInstance:
    print "Please specify the AWS instance ID of the jump host"
    exit(2)

elif not (licenseServerIp and userName and password):
    print "Please specify an user, a password and the license server IP or domain name."
    exit(2)

elif not ((vpcId and not instanceList) or (not vpcId and instanceList)):
    print "Please specify either a vpc id or a comma seperated list of instance ids."
    exit(2)

if vpcId and not re.match('^vpc-[0-9a-fA-F]+$', vpcId):
    print "Not a valid vpc id."
    exit(2)
elif vpcId:
    proc = Popen(['ec2-describe-vpcs', vpcId], stdout=PIPE)
    if proc.wait():
        print "Not a valid vpc id."
        exit(2)
elif instanceList:
    for instance in instanceList:
        if not re.match('^i-[0-9a-fA-F]+$', instance):
            print "Not a valid instance id: " + instance
            exit(2)
    proc = Popen(['ec2-describe-instances'] + instanceList, stdout=PIPE)
    if proc.wait():
        print "One of the passed instance ids is not valid."
        exit(2)


def MyServerProxy(urlPath = ''):
    url = 'https://%s:%s@%s/cluster1%s' % (quote_plus(userName), quote_plus(password), licenseServerIp, urlPath)
    if debugMode:
        print('Connecting ServerProxy to:' + url)
    if version_info[0] > 2:
        from xmlrpc.client import ServerProxy
    else:
        from xmlrpclib import ServerProxy
    if hasattr(ssl, 'SSLContext'):
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        sslcontext.verify_mode = ssl.CERT_NONE
        sslcontext.check_hostname = False
        return ServerProxy(url, context=sslcontext)
    return ServerProxy(url)

# create a handle to the XML-RPC interface
cluster = MyServerProxy()
storage = MyServerProxy('/storage')

if startupCluster:
    # start AWS instances
    print "Starting AWS instances"
    if vpcId:
        proc = Popen(['ec2-describe-instances -F "vpc-id=' + vpcId + '" -F "instance-state-code=80" |grep stopped |cut -f 2 |ec2-start-instances -'], shell=True)
        if proc.wait():
            print "Failed to start one or more instances"
            exit(1)
    elif instanceList:
        proc = Popen(['ec2-start-instances'] + instanceList)
        if proc.wait():
            print "Failed to start one or more instances"
            exit(1)

    # wait for license server
    print "Waiting for license server"
    while True:
        try:
            if cluster.getNodeList():
                print "\nConnected to %s" % (licenseServerIp)
                break
            else:
                stdout.write('.')
                stdout.flush()
                sleep(10)
        except:
            stdout.write('.')
            stdout.flush()
            sleep(10)
            continue
    stdout.write('\n')

    # wait for DB nodes
    finished = False
    while not finished:
        finished = True
        for node in cluster.getNodeList():
            currentNode = MyServerProxy('/' + node)
            try:
                nodeState = currentNode.getNodeState()
                stdout.write('Node %s is in status %s, \t' % (node, nodeState['status']))
                if nodeState['status'] != 'Running':
                    finished = False
            except:
                stdout.write('Node %s is still booting, \t' % (node))
                finished = False
        stdout.write('\n')
        stdout.flush()
        if not finished:
            sleep(10)

    # start the Storage service
    state = cluster.getServiceState()
    for service, status in state:
        if service == 'Storaged' and status == 'OK':
            print "Storage is already running!"
        elif service == 'Storaged':
            storage.startEXAStorage()

    # print the runtime state of all services
    print(cluster.getServiceState())

    # start all databases
    for db in cluster.getDatabaseList():
        instance = MyServerProxy('/db_%s' % (db))
        state = instance.getDatabaseConnectionState()
        if state == 'No':
            instance.startDatabase()
            while True:
                if 'Yes' == instance.getDatabaseConnectionState():
                    print("database %s is accepting connections at %s\n" % (db, instance.getDatabaseConnectionString()))
                    break
                else:
                    print("database %s is currently starting\n" % (db))
                    sleep(5)
        else:
            print("database %s is already running\n" % (db))
        


elif shutdownCluster:
    # check that license server is EXAoperation master
    licenseServerId = 10
    exaoperationMaster = cluster.getCurrentLicenseServer()

    if exaoperationMaster != licenseServerId:
        print("node n%0.4i is the current EXAoperation master but it should be n%0.4i\n"  % (exaoperationMaster, licenseServerId))
        exit(1)


    # shutdown databases
    for db in cluster.getDatabaseList():
        instance = MyServerProxy('/db_%s' % (db))
        state = instance.getDatabaseState()

        if 'running' == state:
            operation = instance.getDatabaseOperation()
            if 'None' == operation:
                instance.stopDatabase()
                while True:
                    if 'setup' == instance.getDatabaseState():
                        print("database %s stopped\n" % (db))
                        break
                    else:
                        print("Database %s is currently shutting down" % (db))
                        sleep(5)
            else:
                print("Database %s is currently in operation %s" % (db, operation))
                exit(1)
        else:
            print("Database %s is currently in runtime state %n" % (db, state))
           

    # shutdown storage
    storage.stopEXAStorage()
    print(cluster.getServiceState())

    # shutdown all nodes 
    print "Shut down AWS instances"
    if vpcId:
        print('Instance ID of jump host is %s (will not be shut down)' % (jhInstance))

        proc = Popen(['ec2-describe-instances -F "vpc-id=' + vpcId + '" -F "instance-state-code=16" |grep running |grep -v ' + jhInstance + ' |cut -f 2 |ec2-stop-instances -'], shell=True)
        if proc.wait():
            print "Failed to start one or more instances"
            exit(1)
    elif instanceList:
        proc = Popen(['ec2-stop-instances'] + instanceList)
        if proc.wait():
            print "Failed to start one or more instances"
            exit(1)

