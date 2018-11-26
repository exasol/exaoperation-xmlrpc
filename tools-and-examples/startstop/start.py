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
    
    #wait until all nodes are online
    print('Waiting until all nodes are online')
    allNodesOnline = False
    while not allNodesOnline:
	allNodesOnline = True
    	for nodeName in cluster.getNodeList():
            nodeState = XmlRpcCall('/' + nodeName).getNodeState()
            if nodeState['status'] != 'Running':
                allNodesOnline = False
                break
	print('.')
	sleep(5)
    print('All nodes are online now')

    #start EXAStorage
    if not storage.serviceIsOnline() and storage.startEXAStorage() != 'OK':
        stderr.write('Not able startup EXAStorage!\n')
        stderr.flush()
        exit(1)
        print('EXAStorage has been started successfully')
    elif storage.serviceIsOnline():
        print('EXAStorage already online; continuing startup process')

    #triggering database startup
    for databaseName in cluster.getDatabaseList():
        database = XmlRpcCall('/db_' + quote_plus(databaseName))
        if not database.runningDatabase():
            print('Starting database instance %s' % databaseName)
            database.startDatabase()
        else:
            print('Database instance %s already running' % databaseName)
    exit(0)


except Exception as e:
    if 'unauthorized' in str(e).lower():
        print 'no access to EXAoperation: username or password wrong'
    elif 'Unexpected Zope exception: NotFound: Object' in str(e):
        print 'database instance not found'
    else:
        print(str(e))
    exit(1)
