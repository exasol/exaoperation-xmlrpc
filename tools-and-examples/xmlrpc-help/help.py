#!/usr/bin/python
import ssl
from sys            import exit
from urllib         import quote_plus
from xmlrpclib      import ServerProxy

### fill out the variables with your own credentials ###
userName = 'admin'
password = 'admin'
hostName = '10.10.0.10'

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
    users = XmlRpcCall('/users')
    databaseList = cluster.getDatabaseList()
    if len(databaseList) == 0:
        print('No database available')
        exit(1)
    database = XmlRpcCall('/db_' + quote_plus(databaseList[0])) #we're just inspecting the methods so every DB is okay
    logserviceList = cluster.getAllLogServices()
    if len(logserviceList) == 0:
        print('No logservice available')
        exit(1)
    logservice = XmlRpcCall('/' + logserviceList[0]['name'])
    nodeList = cluster.getNodeList()
    if len(nodeList) == 0:
        print('No nodes available')
        exit(1)
    node =  XmlRpcCall('/' + nodeList[0])

    #get all method lists
    clusterMethodList = cluster.listMethods()
    storageMethodList = storage.listMethods()
    usersMethodList = users.listMethods()
    databaseMethodList = database.listMethods()
    logserviceMethodList = logservice.listMethods()
    nodeMethodList = node.listMethods()

    #create dictionaries
    clusterHelp = {}
    for method in clusterMethodList:
        clusterHelp[method] = cluster.methodHelp(method)

    storageHelp = {}
    for method in storageMethodList:
        storageHelp[method] = storage.methodHelp(method)

    usersHelp = {}
    for method in usersMethodList:
        usersHelp[method] = users.methodHelp(method)

    databaseHelp = {}
    for method in databaseMethodList:
        databaseHelp[method] = database.methodHelp(method)

    logserviceHelp = {}
    for method in logserviceMethodList:
        logserviceHelp[method] = logservice.methodHelp(method)

    nodeHelp = {}
    for method in nodeMethodList:
        nodeHelp[method] = node.methodHelp(method)

    #convert or print the collected data
    print('# Exasol XML-RPC help')
    
    #cluster
    print("## cluster = XmlRpcCall('/')")
    for key in clusterHelp.keys():
        print('### cluster.' + key + '()')
        print('```\n' + str(clusterHelp[key]) + '\n```\n\n')

    #storage
    print("## storage = XmlRpcCall('/storage')")
    for key in storageHelp.keys():
        print('### storage.' + key + '()')
        print('```\n' + str(storageHelp[key]) + '\n```\n\n')

    #users
    print("## users = XmlRpcCall('/users')")
    for key in usersHelp.keys():
        print('### users.' + key + '()')
        print('```\n' + str(usersHelp[key]) + '\n```\n\n')

    #database
    print("## database = XmlRpcCall('/db_" + quote_plus(databaseList[0]) + "')")
    for key in databaseHelp.keys():
        print('### database.' + key + '()')
        print('```\n' + str(databaseHelp[key]) + '\n```\n\n')

    #logservice
    print("## logservice = XmlRpcCall('/')")
    for key in logserviceHelp.keys():
        print('### logservice.' + key + '()')
        print('```\n' + str(logserviceHelp[key]) + '\n```\n\n')
    
    #node
    print("## node = XmlRpcCall(/'" + nodeList[0] + "')")
    for key in nodeHelp.keys():
        print('### node.' + key + '()')
        print('```\n' + str(nodeHelp[key]) + '\n```\n\n')

except Exception as e:
    if 'unauthorized' in str(e).lower():
        print 'no access to EXAoperation: username or password wrong'
    elif 'Unexpected Zope exception: NotFound: Object' in str(e):
        print 'database instance not found'
    else:
        print(str(e))
    exit(1)
