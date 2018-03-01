#!/usr/bin/env python

import sys, os, xmlrpclib
from xmlrpclib import Server as xmlrpc
from pprint import pprint as pp

server = xmlrpc(open(os.path.join(os.path.expanduser('~'), '.exaopurl')).read().strip())
dbver = server.getListValues('EXASolutionVersions')[-1]
ddisk = server.storage.getListValues('DataDisks')[0]
sdisk = server.storage.getListValues('StorageDisks')[0]
nodes = server.storage.getListValues('Nodes')
users = server.getAllUserLogins()

if not server.storage.serviceIsOnline():
    print "Starting storage:", server.storage.startEXAStorage()
else: print "Storage already online!"

volumes = server.getListValues('Volumes')
if len(volumes) == 0:
    ret = server.storage.addStorageVolume({'allowed_users': users,
                                           'hdd_type': sdisk,
                                           'masternodes': len(nodes),
                                           'nodes_list': nodes,
                                           'redundancy': 1,
                                           'size': 8,
                                           'volume_type': 'Data'})
    print "Create data volume:", ret
    ret = server.storage.addStorageVolume({'allowed_users': users,
                                           'hdd_type': sdisk,
                                           'masternodes': len(nodes),
                                           'nodes_list': nodes, 
                                           'redundancy': 1,
                                           'size': 8,
                                           'volume_type': 'Archive'})
    print "Create archive volume:", ret
    volumes = server.getListValues('Volumes')
else: print "Volumes already created:", volumes

if 'db1' not in server.getListValues('Databases'):
    ret = server.addDatabase({'clients_port_number': 8563,
                              'data_disk': 'd02_data',
                              'data_volume': volumes[0],
                              'database_name': 'db1',
                              'database_version': dbver,
                              'memory_usage': 4,
                              'nodes_list': nodes,
                              'nodes_number': len(nodes)})
    print "Add database:", ret
else: print "Database already exists"

if server.db_db1.getDatabaseState() == 'none':
    print 'Create database'
    server.db_db1.createDatabase()
else: print 'Database already created'
if server.db_db1.getDatabaseState() == 'setup':
    print 'Startup database'
    server.db_db1.startDatabase()
else: print 'Database already running'
    
print "Current database state:"
pp(server.db_db1.getDatabaseInfo())
