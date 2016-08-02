# EXAoperation XMLRPC using examples with python

Here are sample usage of the EXAoperation XMLRPC API with python.

## Import

```python
>>> from xmlrpclib import Server as xmlrpc
```

## Create connection

For the connection type full URL to the exaoperation.

```python
>>> server = xmlrpc('http://admin:admin@10.10.1.1/cluster1')
```

## Methods and objects

To list the methods and objects, use the `listMethods` and `listObjects` functions.
```python
>>> server.listMethods()
['activateNodes', 'addBackupService', 'addBucketFS', 'addDatabase', ....]
>>> server.listObjects()
['bfsdefault', 'logservice1', 'n0011', 'n0012', 'n0013', 'n0014', 'storage', 'support']
```

EXAoperation XMLRPC has tab completion support for python, f.e. in IPython notebook:
```python
In [1]: server.add<TAB>
   server.addBackupService   server.addKeyStore        server.addPublicNetwork   server.addSrvMgmtGroup
   server.addBucketFS        server.addLogService      server.addRemoteVolume    server.addUser
   server.addDatabase        server.addNode            server.addRoute           server.addVLAN
   server.addJDBCDriver      server.addNodesFromXML    server.addScriptExtension
```

## Method description

To get the method description, please use the `methodHelp` function.
```python
>>> server.storage.methodHelp('startEXAStorage')
>>> print server.storage.methodHelp('startEXAStorage')
Start EXAStorage service.
    Tries to start EXAStorage. Raises UsageError in case of error.

Usage: storage.startEXAStorage(ignored_nodes)
Parameters:
  ignored_nodes - list of nodes, where EXAStorage will not be started, or an empty list.
```

## Start and configure storage

Start storage with `startEXAStorage` function.

```python
>>> server.storage.startEXAStorage()
'OK'
```

To create a volume, use the `addStorageVolume` function.
```python
>>> server.storage.addStorageVolume({'allowed_users': ['admin'],
                                     'hdd_type': 'd03_storage',
                                     'masternodes': 4,
                                     'nodes_list': ['n0011', 'n0012', 'n0013', 'n0014'],
                                     'redundancy': 1,
                                     'size': 8,
                                     'volume_type': 'Data'})
'v0000'
```

The `hdd_type` and `nodes_list` values can be discovered with `getListValues` function:
```python
>>> print server.storage.getListValues('StorageDisks')
['d03_storage']
>>> print server.storage.getListValues('Nodes')
['n0014', 'n0011', 'n0012', 'n0013']
```

The list of users is available with `getAllUserLogins` function:
```python
>>> server.getAllUserLogins()
['admin']
```

## Create, configure and start the database

Creation of the database is very similar to the creation of the storage volume:
```python
>>> server.addDatabase({'clients_port_number': 2568,
                        'data_disk': 'd02_data',
                        'database_name': 'db1',
                        'database_version': '6.0.dev5',
                        'memory_usage': 4,
                        'nodes_list': ['n0011', 'n0012', 'n0013', 'n0014'],
                        'nodes_number': 4})
'db_db1'
```

Then the database itself can be created and started:
```python
>>> server.db_db1.createDatabase()
>>> server.db_db1.startDatabase()
>>> server.db_db1.getDatabaseInfo()
{'connectible': 'No',
 'connection string': '10.50.1.11..14:2568',
 'info': '',
 'name': 'db1',
 'nodes': {'active': ['n0011', 'n0012', 'n0013', 'n0014'],
  'failed': [],
  'reserve': []},
 'operation': 'None',
 'persistent volume': 'v0000',
 'quota': 0,
 'state': 'setup',
 'temporary volume': 'None',
 'usage persistent': 0,
 'usage temporary': 0}
```

After some time the `connectible` is set to 'Yes' and the database can be used.