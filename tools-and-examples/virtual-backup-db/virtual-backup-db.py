#!/usr/bin/python
import ssl
from ConfigParser   import SafeConfigParser
from sys            import exit, stdout, stderr
from urllib         import quote_plus
from xmlrpclib      import ServerProxy
from time           import sleep, mktime
from datetime       import datetime

userName = None
password = None
hostName = None
databaseName = None
archiveVolume = None

# load configuration file
try:
    config = SafeConfigParser()
    config.read('virtual-backup-db.cfg')
    userName = config.get('virtualbackup', 'username')
    password = config.get('virtualbackup', 'password')
    hostName = config.get('virtualbackup', 'hostname')
    databaseName = config.get('virtualbackup', 'database')
    archiveVolume = config.get('virtualbackup', 'archive')
    foreignDatabaseName = config.get('virtualbackup', 'foreign_database')

except NoOptionError as err:
    stderr.write('%s\n' % err)
    exit(1)

def XmlRpcCall(urlPath = ''):
    url = 'https://%s:%s@%s/cluster1%s' % (quote_plus(userName), quote_plus(password), hostName, urlPath)
    if hasattr(ssl, 'SSLContext'):
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        sslcontext.verify_mode = ssl.CERT_NONE
        sslcontext.check_hostname = False
        return ServerProxy(url, context=sslcontext)
    return ServerProxy(url)

def convertVolumeId(volumeId):
    result = None
    if volumeId.lower().startswith('v'):
        result = int(volumeId.replace('v', ''))
    elif volumeId.lower().startswith('r'):
        result = int(volumeId.replace('r', '')) + 10000
    else:
        result = int(volumeId)
    return result

try:
    cluster = XmlRpcCall('/')
    database = XmlRpcCall('/db_' + quote_plus(databaseName))
    latestBackupIdentifier = None
    latestBackupExpiration = 0
    latestBackupExpireAlterable = None
    latestBackupItemVolumeId = None

    list = database.getBackups(True, True)
    if list and len(list) > 0:
        lastBackupId = 0
        for item in list:
            itemVolumeId = convertVolumeId(item['volume'])
            volumeId = convertVolumeId(archiveVolume)
            if  item['system'] == foreignDatabaseName \
                and item['usable'] and (itemVolumeId == volumeId) \
                and (item['bid'] >= lastBackupId):
                latestBackupIdentifier = item['id']
                lastBackupId = item['bid']
                latestBackupExpireAlterable = item['expire_alterable']
                latestBackupItemVolumeId = itemVolumeId
                if item['expire'] and item['expire'] != '':
                    latestBackupExpiration = int(mktime(datetime.strptime(item['expire'], '%Y-%m-%d %H:%M').timetuple()))

    if latestBackupIdentifier:
        print('BackupId of last backup in volume %s is %i (%s)' % (volumeId, lastBackupId, latestBackupIdentifier))
        if database.runningDatabase():
            print('Database is online yet; shutting down database now')
            database.shutdownDatabase();
            while database.runningDatabase():
                print('.')
                sleep(5)
            print('Database is offline; continuing restore procedure')
        else:
            print('Database is already offline; continuing restore procedure')

        print('Resetting expiration date of backup set')
        database.changeBackupExpiration(latestBackupItemVolumeId, latestBackupExpireAlterable.split(' ')[1], 0)

        print('Triggering restore process')
        database.restoreDatabase(latestBackupIdentifier, 'virtual access')
        print('Restore process successfully triggered.')

        print('Writing back expiration date of backup set')
        database.changeBackupExpiration(latestBackupItemVolumeId, latestBackupExpireAlterable.split(' ')[1], latestBackupExpiration)
        print('All done.')

        exit(0)
    else:
        print('No backup found!')
        exit(1)

except Exception as e:
    if 'unauthorized' in str(e).lower():
        print 'no access to EXAoperation: username or password wrong'
    elif 'Unexpected Zope exception: NotFound: Object' in str(e):
        print 'database instance not found'
    else:
        print(str(e))
    exit(1)
