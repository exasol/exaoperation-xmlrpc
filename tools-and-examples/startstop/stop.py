#!/usr/bin/python
import ssl
from ConfigParser   import SafeConfigParser
from sys            import exit, stdout, stderr
from urllib         import quote_plus
from xmlrpclib      import ServerProxy
from time           import sleep

userName = None
password = None
hostName = None

# load configuration file
try:
    config = SafeConfigParser()
    config.read('startstop.cfg')
    userName = config.get('startstop', 'username')
    password = config.get('startstop', 'password')
    hostName = config.get('startstop', 'hostname')
    licenseServerNode = config.get('startstop', 'licenseServerNode')
    exaOperationTimeout = int(config.get('startstop', 'exaOperationTimeOut'))

except NoOptionError as err:
    stderr.write('%s\n' % err)
    exit(1)

def XmlRpcCall(urlPath = ''):
    url = 'https://%s:%s@%s/cluster1%s' % (quote_plus(userName), quote_plus(password), hostName, urlPath)
    if hasattr(ssl, 'SSLContext'):
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        sslcontext.verify_mode = ssl.CERT_NONE
        sslcontext.check_hostname = False
        return ServerProxy(url, context=sslcontext)
    else:
        return ServerProxy(url)

try:        
    cluster = XmlRpcCall('/')
    storage = XmlRpcCall('/storage')
    
    #get EXAoperation host
    exaOpHost = 'n%0.4i' % cluster.getCurrentLicenseServer()

    #shutdown databases
    for databaseName in cluster.getDatabaseList():
        database = XmlRpcCall('/db_' + quote_plus(databaseName))
        if database.runningDatabase():
            print('Database %s is online yet; shutting down database now' % databaseName)
            database.shutdownDatabase()
            while database.runningDatabase():
                print('.')
                sleep(5)
            print('Database %s is offline; continuing shutdown procedure' % databaseName)
        else:
            print('Database %s is already offline; continuing shutdown procedure' % databaseName)
    database = None

    #shutting down EXAStorage
    if storage.serviceIsOnline():
        print('EXAStorage service is online yet; shutting down service')
        storage.stopEXAStorage()
        while storage.serviceIsOnline():
            print('.')
            sleep(5)
        print('EXAStorage service has been stopped')
    else:
        print('EXAStorage is not running; continuing shutdown procedure')

    #shutting down nodes
    clusterNodes = cluster.getNodeList()
    shutdownNodes = []
    for nodeName in clusterNodes:
        if nodeName != exaOpHost:
            node = XmlRpcCall('/' + nodeName)
            node.shutdownNode()
            shutdownNodes.append(nodeName)
            print('Shutting down node %s' % nodeName)

    allNodesOffline = False
    while not allNodesOffline:
        allNodesOffline = True
        for nodeName in shutdownNodes:
            nodeState = XmlRpcCall('/' + nodeName).getNodeState()
            if nodeState['status'] == 'Running':
                allNodesOffline = False
                break
        print('.')
        sleep(5)
    print('All database nodes shut down')



    if exaOpHost in clusterNodes:
        print('Shutting down EXAoperation host node %s' % exaOpHost)
        node = XmlRpcCall('/' + exaOpHost)
        node.shutdownNode()
        sleep(exaOperationTimeout) #wait till EXAoperation moved back to license server
        print('Shutting down license server')
        cluster.haltLicenseServer(licenseServerNode)

    else:
        print('Shutting down license server')
        sleep(10)
        cluster.haltLicenseServer(exaOpHost)

except Exception as e:
    if 'unauthorized' in str(e).lower():
        print 'no access to EXAoperation: username or password wrong'
    elif 'Unexpected Zope exception: NotFound: Object' in str(e):
        print 'database instance not found'
    else:
        print(str(e))
    exit(1)
