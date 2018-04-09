import ssl
from sys            import exit
from urllib         import quote_plus
from xmlrpclib      import ServerProxy

### fill out the variables with your own credentials ###
userName = 'admin'
password = 'admin'
hostName = '10.0.0.10'
databaseName = 'exa_db1'

def XmlRpcCall(urlPath = ''):
    url = 'https://%s:%s@%s/cluster1%s' % (quote_plus(userName), quote_plus(password), hostName, urlPath)
    if hasattr(ssl, 'SSLContext'):
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        sslcontext.verify_mode = ssl.CERT_NONE
        sslcontext.check_hostname = False
        return ServerProxy(url, context=sslcontext)
    else:
        return ServerProxy(url)

try:        
    cluster = XmlRpcCall('/')
    database = XmlRpcCall('/db_' + quote_plus(databaseName))
    
    ### place your code here ###
    cluster.getNodeList()
    database.getDatabaseInfo()


except Exception as e:
    if 'unauthorized' in str(e).lower():
        print 'no access to EXAoperation: username or password wrong'
    elif 'Unexpected Zope exception: NotFound: Object' in str(e):
        print 'database instance not found'
    else:
        print(str(e))
    exit(1)