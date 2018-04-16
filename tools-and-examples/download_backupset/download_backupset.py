#!/usr/bin/env python
import os.path, re, xmlrpclib, base64, ssl
from pprint import pprint
from sys import exit, argv 
from getopt import getopt
from urllib import quote_plus
from pipes import quote
from subprocess import Popen, PIPE, STDOUT
from tempfile import NamedTemporaryFile
from datetime import datetime
from time import sleep

opts, args = None, None
try:
    opts, args = getopt(argv[1:],'hodl:s:u:p:b:i:a:c:')
except:
    print "Unknown parameter(s): %s" % argv[1:]
    opts = []
    opts.append(['-h', None])

datePattern = re.compile('^\d{4}-\d{2}-\d{2}$')
connectionString = None
resolveDepencies = False
archiveVolume = None
licenseServer = None
sourceDatabase = None
backupPath = None
backupId = None
userName = None
password = None
overwriteBackups = False

for opt in opts:
    parameter = opt[0]
    value = opt[1]
    if parameter == '-h':
        print """
    Options:
    -h  shows this help
    -l  <license server>
    -u  <user name>
    -p  <password>
    -s  <source database name>
    -b  <backup path>
    -i  <backup id>             (optional, get backup set with id xxx instead of latest backup)
    -a  <archive volume>        (optional, helps to resolve id conflicts on different volumes)
    -c  <connection string>     (optional, neccessary for additional public networks)
    -d                          (optional, resolve backup depencies and download all files)
    -o                          (optional, overwrite existing backup sets)
"""
        exit(0)
    elif parameter == '-l':
        licenseServer = value.strip()

    elif parameter == '-s':
        sourceDatabase = value.strip()

    elif parameter == '-b':
        backupPath = value.strip()
        if not os.path.isdir(backupPath):
            print "Backup path does not exist!"
            exit(1)

    elif parameter == '-u':
        userName = value.strip()

    elif parameter == '-p':
        password = value.strip()

    elif parameter == '-i':
        backupId = int(value)

    elif parameter == '-a':
        archiveVolume = value.strip().lower()

    elif parameter == '-d':
        resolveDepencies = True

    elif parameter == '-o':
        overwriteBackups = True

    elif parameter == '-c':
        connectionString = value.strip()

if not (licenseServer and sourceDatabase and backupPath and userName and password):
    print "Please define a license server, the source database name, backup path and the auth credentials! (use -h for help)"
    exit(1)

def ServerProxy(urlPath):
    url = 'https://%s:%s@%s/%s' % (quote_plus(userName), quote_plus(password), licenseServer, urlPath)
    if hasattr(ssl, 'SSLContext'):
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        sslcontext.verify_mode = ssl.CERT_NONE
        sslcontext.check_hostname = False
        return xmlrpclib.ServerProxy(url, context=sslcontext)
    return xmlrpclib.ServerProxy(url)

s = ServerProxy('cluster1')
if sourceDatabase not in s.getDatabaseList():
    print "Source database does not exist on this cluster!"
    exit(1)

# tricky part: get connection string and iproc table for database and match them
db = ServerProxy('cluster1/db_' + quote_plus(sourceDatabase))
ipList = []
if not connectionString:
    connectionString = db.getDatabaseConnectionString()

for partition in connectionString.strip().split(','):
    match = re.match('^(\d+\.\d+\.\d+\.)(\d+)\.\.(\d+)', partition)
    if match:
        for ip in xrange(int(match.group(2)), int(match.group(3)) + 1):
            ipList.append(match.group(1) + str(ip))
    match = re.match('^(\d+\.\d+\.\d+\.\d+)(:\d+|$)', partition)
    if match:
        ipList.append(match.group(1))

# implying that the node ips are straight forward (but they don't have to be continuous)
ipList.sort()

databaseNodes = db.getDatabaseNodes()
databaseNodes = databaseNodes['active'] + databaseNodes['reserve']
nodeIpList = {}
i = 0
for node in sorted(databaseNodes):
    nodeIpList[node] = ipList[i]
    i += 1

iprocIpList = {}
i = 0
for node in databaseNodes:
    iprocIpList['node_' + str(i)] = nodeIpList[node]
    i += 1

# get backup informations
files = []
backupList = db.getBackupList()

# get latest backup id if no id parameter is given
a = backupId
if not backupId:
    a, b = 0, ''
    for item in backupList:
        if len(item) == 2 and item[0] > b:
            a, b = item[1], item[0]

if a > 0:
    backupId = a
else:
    print "No backup set found!"
    exit(1)

if not overwriteBackups and os.path.isdir(backupPath + os.sep + sourceDatabase + os.sep + 'id_%s' % backupId):
    print "Stopping: backup directory already exists (use -o to force overwrite)!"
    exit(0)

expirationDate = None
for backup in backupList:
    if backup[1] == backupId:
        backupInfo = db.getBackupInfo(backup[0])
        expirationDate = datetime.strptime(backupInfo['expire date'], '%Y-%m-%d %H:%M')
        if not archiveVolume:
            archiveVolume = backupInfo['volume'][0]

        if backupInfo['volume'][0] == archiveVolume:
            files += backupInfo['files']
            if resolveDepencies and len(backupInfo['dependencies']) > 0:
                for depency in backupInfo['dependencies']:
                    for depBackup in backupList:
                        if depBackup[1] == depency:
                            depBackupInfo = db.getBackupInfo(depBackup[0])
                            files += depBackupInfo['files']
files.sort()

#create local directories and start wget processes
wgetProcs = {}
wgetProcsItems = {}
pathNodePattern = re.compile('([^/]+\/id_\d+\/level_\d+\/)(node_\d+)\/([^/]+)')
i = 0
for item in files:
    match = pathNodePattern.search(item)
    if match:
        nodeIp = iprocIpList[match.group(2)]
        localPath = backupPath + os.sep + match.group(1) + os.sep + match.group(2)
        if not os.path.exists(localPath):
            os.makedirs(localPath)

        downloadPath = 'ftp://%s:%s@%s:2021/%s/%s' % (quote_plus(userName), quote_plus(password), nodeIp, archiveVolume, item)
        wgetProc = Popen(
            [
                'wget -O - --no-check-certificate --no-verbose %s |tee %s |md5sum' % (
                    quote(downloadPath),
                    quote(localPath + os.sep + match.group(3))
                )
            ],
            shell = True,
            stdout = PIPE
        )
        sleep(5)
        wgetProcs[i] = wgetProc
        wgetProcsItems[i] = item
        i += 1

#all upload processes are currently running so wait until all of them have been finished
runningProcs = True
while runningProcs:
    runningProcs = any(wgetProcs[process].poll() == None for process in wgetProcs.keys())

#if any of the processes returned an error code != 0 show a warning and exit with error code 1
if any(wgetProcs[process].poll() != 0 for process in wgetProcs.keys()):
    print "An error occoured!"
    exit(1)

#read metadata file(s) for md5 check
metadataPattern = re.compile('^(.*?)\/metadata_\d+$')
md5FilePattern = re.compile('^\s*([a-f0-9]{32,32})\s*(.*?)$', re.I)
md5FileList = {}
for fileName in files:
    match = metadataPattern.search(fileName)
    if match:
        with open(backupPath + os.sep + fileName) as f:
            for line in f:
                fileMatch = md5FilePattern.match(line)
                if fileMatch:
                    if fileMatch.group(2) not in md5FileList.keys():
                        md5FileList[fileMatch.group(2)] = fileMatch.group(1)

#compare target and source md5 sums
md5pattern = re.compile('^\s*([a-f0-9]{32,32})\s*', re.I|re.M)
allValid = True
for procKey in wgetProcs.keys():
    proc = wgetProcs[procKey]
    itemName = wgetProcsItems[procKey]
    lines = proc.stdout.read()
    match = md5pattern.match(lines)
    if match and itemName in md5FileList.keys():
        if md5FileList[itemName].lower() == match.group(1).lower():
            print 'OK:     ' + itemName
        else:
            print 'FAILED: ' + itemName
            allValid = False

node0Directories = []
if allValid:
    node0Pattern = re.compile('^([^/]+\/id_\d+\/level_\d+\/node_0\/)')
    for fileName in files:
        match = node0Pattern.search(fileName)
        if match and match.group(1) not in node0Directories:
            node0Directories.append(match.group(1))
            node0Path = backupPath + os.sep + match.group(1) 
            open(node0Path + 'expire_' + expirationDate.strftime('%Y%m%d%H%M'), 'a').close()
            open(node0Path + 'validated_' + datetime.now().strftime('%Y%m%d%H%M'), 'a').close()

    exit(0)
else:
    exit(2)
   
