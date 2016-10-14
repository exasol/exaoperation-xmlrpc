# EXAoperation XMLRPC API

This project contains Python script examples how to automate the administration of EXASOL cluster using its XMLRPC API instead of EXAoperation's web interface. Additionally, you'll find a complete description for all API methods in file [EXAoperation_XMLRPC.md](EXAoperation_XMLRPC.md).

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

# Example tools

In this repository you will find following example tools:
* `startdatabase.py` - initialize and start a test database
* `logentries.py` - shows current log entries

# Brief reference of all functions

```
Every service support this functions:

object.getPath() - return absolute and relative pathes to current object
  Usage: object.getPath()

object.getListValues(list) - Return various list values depending on a type of object.
  Usage: object.getListValues(list)
  Parameters:
    list - name of a list. Possible values are: ['Users', 'TimeZones', 'Days', 'Databases', 'ExapScriptTypes', 'DataDisks', 'StorageDisks', 'StorageVolumeNodes', 'ScalingGovernor', 'VLAN', 'PublicNetwork', 'SrvMgmtGroup', 'KeyStore', 'BootInterface', 'DatabaseNetworkInterfaces', 'EXASolutionVersions', 'VMBootDevice', 'Nodes', 'NodesReserve', 'NodesRemoveReserve', 'NodesDeactivate', 'NodesReactivate', 'BackupManager', 'BackupSystems', 'Disks', 'Volumes', 'DiskTypes', 'RaidTypes', 'SrvMgmtTypes', 'Mtu', 'KeyStoreTypes', 'EncrTypes']

object.listMethods() - Introspection function. Return a list of all supported methods.
  Usage: object.listMethods()

object.methodHelp(method_name) - Introspection method. Return a description for a given function.
  Usage: object.methodHelp(method_name)

object.methodSignature(method_name) - Introspection method. Return a list of parameters for a given function. Function is not completly supported, please call object.methodHelp() to get a description of a parameters.
  Usage: object.methodSignature(method_name)

SERVICE BackupService
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method backupCreate
        Create the backup for given system.

  Method backupDoesExpire
        Returns false in case backup is protected from automatic removal after reaching expiration time.

  Method backupGetAbsoluteExpire
        Returns the absolute backup removal date.

  Method backupGetArchiveNodes
        Return the list of archive nodes for this backup.

  Method backupGetAvailableSpace
        Return the list of nodes and the available space.

  Method backupGetCorrupt
        Return whether the backup is corrupt.

  Method backupGetDetailedState
        Return details about state of backup.

  Method backupGetDirectory
        Return the directory to which the backup should be copied.

  Method backupGetDone
        Return whether the backup is done.

  Method backupGetExpire
        Return the backup remove date.

  Method backupGetList
        Return the list of backups.

  Method backupGetNote
        Return the note of the backup.

  Method backupGetOfflineMedia
        Return the name of the offline backup media.

  Method backupGetSize
        Return the list of nodes with size of the given backup per node.

  Method backupGetState
        Return the state of backup in procent.

  Method backupGetSystem
        Return the system name of the backup.

  Method backupRemove
        Remove the online backup files.

  Method backupSetAbsoluteExpire
        Set the absolute removal date of a backup.

  Method backupSetDoesExpireFlag
        Set doesexpire flag.

  Method backupSetDone
        Mark the backup as done.

  Method backupSetExpire
        Set the remove date to the given value.

  Method backupSetNote
        Set the note of backup.

  Method backupSetOfflineMedia
        Set the name of the offline backup media.

  Method backupSetSystem
        Set the system of backup.

  Method editBackupService
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * backup_disk, type: Choice, Disk where backups should be stored.
    * backup_removeafter, type: TextLine, Default time interval, after which backups should be removed.
    * backup_systems, type: List, Systems allowed to backup.
    * nodes_list, type: List, List of nodes to backup.
      redundancy_number, type: Int, Number of copies of backup files in cluster


  Method getProperties
        This object has no properties.

SERVICE BucketFS
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method addBucket
        Create a new object type BucketFSBucket

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
    * bucket_name, type: TextLine, The name of bucket.
      description, type: TextLine, Some description of this BucketFS Bucket.
    * public_bucket, type: Bool, Public buckets require no password for reading.
    * read_password, type: Password, Password readonly access.
    * write_password, type: Password, Password for write access.


  Method deleteSubObject
        Delete the subobject, defined by it's name and all settings

  Method editBucketFS
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
      description, type: TextLine, Some description of this BucketFS.
    * disk, type: Choice, Disk for BucketFS data.
      http_port, type: Int, Port for FS access.
      https_port, type: Int, Port for SSL encrypted FS access.


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    description: Some description of this BucketFS.
    disk: Disk for BucketFS data.
    http_port: Port for FS access.
    https_port: Port for SSL encrypted FS access.


SERVICE BucketFSBucket
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method editBucketFSBucket
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * bucket_name, type: TextLine, The name of bucket.
      description, type: TextLine, Some description of this BucketFS Bucket.
    * public_bucket, type: Bool, Public buckets require no password for reading.
    * read_password, type: Password, Password readonly access.
    * write_password, type: Password, Password for write access.


  Method getProperties
        This object has no properties.

SERVICE Database
Object: https://<user>:<pass>@<cluster_node>/cluster1/db_<object_name>/
Note: the EXASolution systems need prefix 'db_'
  Method abortBackup
        Abort running database backup.

  Method abortShrink
        Abort shrink operation of database.

  Method backupCleanup
        Stop backup processes remove created files.

  Method backupDatabase
        Start backup to given storage volume with given level and expiration time.

    Parameters:
      volume - name of volume where to write backup
      level  - backup level
      expire - expire time for backup

  Method backupGetSize
        Return the list of nodes with size of the given backup per node.

  Method backupInfo
        Return information for a backup.

  Method backupRemove
        Remove backup files.

  Method backupStart
        Create a new backup.

  Method backupState
        Return the % of prepare process or None if nothing started.

  Method changeBackupExpiration
        Change expiration time of a backup.

  Method cleanupDatabase
        Kill the processes and cleanup the database state, must exists.

  Method createDatabase
        Create a fresh database, must not exist jet.

  Method deleteBackups
        Delete given backups

    Usage: database.deleteBackups(backup_list)
    Parameters:
      backup_list - a list of backups, Can be recieved with database.backupList()


  Method deleteUnusableBackups
        Delete all unusable backups for current database.

    Usage: database.deleteUnusableBackups()


  Method editDatabase
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * add_redundancy_number, type: Int, Number of redundancy which should be added to existent.
    * clients_port_number, type: Int, Port for client connections.
      data_volume, type: Choice, Volume for EXASolution database data.
      database_comment, type: TextLine, User-defined comment for database (200 charachters max)
    * database_version, type: Choice, Version of EXASolution executables.
      enable_auditing, type: Bool, Enable auditing for database
      extra_params, type: TextLine, Extra parameters for startup of database.
      ldap_server, type: TextLine, LDAP Server to use for remote database authentication, e.g. ldap[s]://192.168.16.10 . Multiple servers must be separated by commas.
    * memory_usage, type: Int, Amount of database memory (in GiB).
      nodes_list_add_reserve, type: List, List of nodes, which should be added to the system as reserve nodes.
      nodes_list_deactivate, type: List, List of nodes which should be deactivated for this system.
      nodes_list_reactivate, type: List, List of nodes which should be reactivated for this system.
      nodes_list_remove_reserve, type: List, List of nodes which should be removed from the System as reserve nodes.
      used_storage, type: Bool, Enable/Disable usage of EXAStorage for keeping of database's data.
      vlan_list, type: List, Network interfaces to use for database. Leave empty to use all possible network interfaces.
      volume_quota, type: Int, Maximal size of volume in (GiB), the database tries to shrink it on start if required and possible.
      volume_restore_delay, type: TextLine, Move failed volume nodes to used reserve nodes automaticaly after given amount of time, or disable it with no value.


  Method enlargeDatabase
        Enlarge an existing database. Precondition: the database should be stopped.
    Warning - the changes made by this function could not be undone. Function increase
    the number of active nodes of the database.

    Usage: database.enlargeDatabase(count_of added_active_nodes)
    Parameters:
      count_of_added_active_nodes - a number of nodes, that will be ADDED to an existing number.


  Method existDatabase
        Return whether the database exists or not.

  Method forceShutdownDatabase
        Force shutdown of database, must be running.

  Method getBackgroundRestoreState
        Returns current background restore state.

  Method getBackupSchedule
        Return a list of scheduled backups

  Method getBackups
        Return a list of available backups for this database.

    Usage: database.getBackups(show_all_databases, show_expired_backups)
    Parameters:
      show_all_databases - show backups not for only this database
      show_expired_backups - not exclude expired backups from list


  Method getCurrentDatabaseSize
        Get current database size.

  Method getCurrentErrors
        Get current reasons for not starting a database.

  Method getDatabaseVersion
        Return current database version.

  Method getDatabaseVolumeNodesMatch
        Return information about database nodes match to volume nodes.

  Method getDatabaseVolumeOfflineSegments
        Return number of offline data volume segments.

  Method getNextSchedules
        Get scheduling for next period of time.

  Method getNodeState
        Return the state of a node: online, offline or failed.

  Method getPddProgress
        Get information about current PDD processes (Backup/Restore).

  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    add_redundancy_number: Number of redundancy which should be added to existent.
    clients_port_number: Port for client connections.
    data_volume: Volume for EXASolution database data.
    database_comment: User-defined comment for database (200 charachters max)
    database_version: Version of EXASolution executables.
    enable_auditing: Enable auditing for database
    extra_params: Extra parameters for startup of database.
    ldap_server: LDAP Server to use for remote database authentication, e.g. ldap[s]://192.168.16.10 . Multiple servers must be separated by commas.
    memory_usage: Amount of database memory (in GiB).
    nodes_list_add_reserve: List of nodes, which should be added to the system as reserve nodes.
    nodes_list_deactivate: List of nodes which should be deactivated for this system.
    nodes_list_reactivate: List of nodes which should be reactivated for this system.
    nodes_list_remove_reserve: List of nodes which should be removed from the System as reserve nodes.
    used_storage: Enable/Disable usage of EXAStorage for keeping of database's data.
    vlan_list: Network interfaces to use for database. Leave empty to use all possible network interfaces.
    volume_quota: Maximal size of volume in (GiB), the database tries to shrink it on start if required and possible.
    volume_restore_delay: Move failed volume nodes to used reserve nodes automaticaly after given amount of time, or disable it with no value.


  Method maintenanceDatabase
        Get maintenance state of database.

  Method operationGetCurrent
        Return the current operation

  Method restartDatabase
        Restart database which must be running.

  Method restoreCleanup
        Stop the restore process

  Method restoreDatabase
        Start restore from given backup ID and restore type.

      Usage: database.restoreDatabase(backup_id, restore_type)
      Parameters:
        backup_name - could be obtained by getBackups(), field 'id'. Must have three valus separated by space.
        restore_type - type of restore. Must be one of following - {'blocking'|'nonblocking'|'virtual access'}


  Method restoreStart
        Start the restore process from the given directory.

  Method restoreState
        Return the % of restore process done or None.

  Method runningDatabase
        Return whether the database is started.

  Method setBackupSchedule
        Set a list of all scheduled backups.

    Parameter:
      list of backup definitions

  Method shrinkDatabase
        Shrink a database. This operation can only be apply for running databases.

    Usage: database.shrinkDatabase(target_size_in_gb)
    Parameters:
      target_size_in_gb - target size for shrink operation.


  Method shutdownDatabase
        Shutdown the database, must be running.

  Method startDatabase
        Startup the database, must exists and must not be running.

  Method startDatabaseMaintenance
        Start database in maintenance mode, must exist and must not be running.

  Method stateDatabase
        Return human-readable state of database.

SERVICE JDBCDriver
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method editJDBCDriver
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
      comment, type: TextLine, Description of the driver, not required.
    * jdbc_main, type: TextLine, Name of the main class.
    * jdbc_name, type: TextLine, Name of the driver.
    * jdbc_prefix, type: TextLine, Prefix of the JDBC name, must begin with "jdbc:" and ends with ":", like in "jdbc:mysql:".


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    jdbc_jars: List of URLs to the JDBC JAR files.


  Method removeJARFiles
        Remove cached JAR files.

  Method uploadFile
        Upload given file.

SERVICE LogService
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method cleanupLogservice
        Cleanup the logservice directory structure before deleting it.

  Method editLogService
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
      default_interval, type: TextLine, This time interval is shown per default.
      description, type: TextLine, Some description of this logservice.
      exaclusteros_services, type: List, EXAClusterOS services which should be visible at monitor, possible values: 'EXAoperation', 'DWAd', 'Lockd', 'Load', 'Storage', 'Appserver'
      exasolution_systems, type: List, Database systems which should be visible at monitor.
    * priority, type: Choice, Specifies the lowest priority of messages that this logservice will show., allowed values: [u'Error', u'Warning', u'Notice', u'Information']
      remote_syslog_protocol, type: Choice, Protocol to use to communicate with remote syslog server (TCP/UDP)., allowed values: [u'TCP', u'UDP']
      remote_syslog_server, type: TextLine, Log messages periodically to the specified remote syslog server via TCP.


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    default_interval: This time interval is shown per default.
    description: Some description of this logservice.
    exaclusteros_services: EXAClusterOS services which should be visible at monitor, possible values: 'EXAoperation', 'DWAd', 'Lockd', 'Load', 'Storage', 'Appserver'
    exasolution_systems: Database systems which should be visible at monitor.
    priority: Specifies the lowest priority of messages that this logservice will show.
    remote_syslog_protocol: Protocol to use to communicate with remote syslog server (TCP/UDP).
    remote_syslog_server: Log messages periodically to the specified remote syslog server via TCP.


  Method logFetchEntries
        Fetch log entries from the Logd service.
        Parameters:
        start, halt - tuples (yyyy, mm, dd, hh, mi, ss, msec)
        errlevel    - lowest message level to fetch, possible values: ['Information', 'Notice', 'Warning', 'Error']
        priority    - tag


SERVICE Node
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method addNodeDisk
        Create a new object type NodeDisk

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
      devices, type: List, The List of disk devices used on the node, use cluster's defaults if not given.
      disk_number, type: Int, Disk number in the name of disk, if not specified, then given automatically.
      diskenc, type: Choice, Type of encryption to use on disks, use cluster's defaults if not given.
      disklabel, type: TextLine, Label for disk.
      diskraid, type: Choice, The type of RAID to use on disks, use cluster's defaults if not given.
      disksize, type: Int, The size of this disk in GiB or maximum if not entered.
    * disktype, type: Choice, Type of storage for which this disk will be used.
      raidredundancy, type: Int, Number of copies of each datablock on RAID 10.


  Method addStorageDisk
        Add aditional storage disk do an active node.

    Usage: node.addStorageDisk(devices, enc, label, size, number)
    Parameters: devices   - List of devices to use
                label     - Label of the new disk
                enc       - Encryption to use (none, aes128, aes256)
                number    - Use this disk number, if None or not given, generate new number

    Only storage disks and disks without redundancy can be added to an
    active node. Devices must not be used by any other disk.

  Method applyDefaultDiskLayout
        Apply default disk layout to this node.

  Method copyNode
        Copies node to another

    Parameters: number
                external_number
                mac_addr_eth0
                mac_addr_eth1
                mac_addr_ipmi
                ip_addr_ipmi
                idstring
                vlan_list
                public_network_list


  Method deleteDisks
        Remove disk with given name.

  Method deleteSubObject
        Delete the subobject, defined by it's name and all settings

  Method editNode
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * boot_interface, type: Choice, Interface to use for PXE boot.
      console_redirect, type: Bool, Redirect kernel output to serial console.
    * cpu_scaling_governor, type: Choice, Power scheme for Node CPU(s)
      devices, type: List, The List of disk devices used on the node, use cluster's defaults if not given.
      diskenc, type: Choice, Type of encryption to use on disks, use cluster's defaults if not given.
      diskraid, type: Choice, The type of RAID to use on disks, use cluster's defaults if not given.
      external_number, type: Int, The external node number, this number is added to network IP address.
      force_fsck, type: Bool, Force filesystem check on next boot of this node.
      force_no_fsck, type: Bool, Force no filesystem check on next boot of this node.
      hugepages, type: Int, Amount of hugepages in GiB to allocate for database usage on this node. This is recommended for nodes with RAM > 512 GiB. See manual for details.
      idstring, type: TextLine, String to identificate this node, not required.
      ip_addr_ipmi, type: TextLine, Public Server Management Card IP address (only if group uses public addresses).
      ipmi_group, type: Choice, Group that the IPMI card of this node belongs to (if any).
    * mac_addr_eth0, type: TextLine, The MAC address of the first LAN interface.
    * mac_addr_eth1, type: TextLine, The MAC address of the second LAN interface.
      mac_addr_ipmi, type: TextLine, The MAC address of the Server Management interface.
    * public_network_list, type: FixedDict, Additional public network interfaces in node.
      raidredundancy, type: Int, Number of copies of each datablock on RAID 10.
    * spool_disk, type: Choice, Disk for spool data of loading processes and other.
      to_install, type: Bool, Should this node to be installed next time when booted?
      to_wipe, type: Bool, Wipe disks of node on next boot. This process can take a lot of time
      use_4kib, type: Bool, Use 4 KiB alignment for hard disks to satisfy the 4 KiB sector size requirements.
    * vlan_list, type: FixedDict, Additional private network interfaces in node.


  Method fixChecksums
        Fix/delete checksums of disks.

  Method getAllDisks
        Return list of disk names.

  Method getDeviceInfo
        Return information about devices.

  Method getDiskInfo
        Return info about disk

  Method getNodeInfo
        Return node information.

  Method getProperties
        This object has no properties.

  Method getSrvMgmtConsoleParameters
        Return info about parameters necessary for Server Management console

  Method nodeRunning
        Return whether the node is running.

  Method poweroffNode
        Power off the node immediatly.

  Method rebootNode
        Reboot the node.

  Method resetNode
        Reset the node immediatly.

  Method setActiveMode
        Set the node to Active state. The node in active state is available to all cluster services.

    Usage: node.setActiveMode()

  Method setForceFSCKMode
        Set the node to Force fsck state.

    Usage: node.setFSCKMode()

  Method setForceNoFSCKMode
        Set the node to Force No fsck state.

    Usage: node.setNoFSCKMode()

  Method setInstallMode
        Set the node to Install state. After next reboot the node will be installed.

    Usage: node.setInstallMode()

  Method setWipeMode
        Set the node to To Wipe state. After boot the all data will be erased.

    Usage: node.setWipeMode()

  Method shutdownNode
        Shutdown the node.

  Method startClusterServices
        Start Core daemon on this node.

  Method startupNode
        Power on and startup the node.

  Method stopClusterServices
        Stop Core daemon on this node.

  Method toggleIdLed
        Toggle the ID LED on the given node.

SERVICE NodeCluster
Object: https://<user>:<pass>@<cluster_node>/cluster1/
  Method activateNodes
        Set nodes from a given list node_names to active state.
    Usage:
    nodes_list = [u'n0110', u'n0108']
    cluster.activateNodes(nodes_list)

  Method addBackupService
        Create a new object type BackupService

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
    * backup_disk, type: Choice, Disk where backups should be stored.
    * backup_removeafter, type: TextLine, Default time interval, after which backups should be removed.
    * backup_systems, type: List, Systems allowed to backup.
    * nodes_list, type: List, List of nodes to backup.
      redundancy_number, type: Int, Number of copies of backup files in cluster


  Method addBucketFS
        Create a new object type BucketFS

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
      description, type: TextLine, Some description of this BucketFS.
    * disk, type: Choice, Disk for BucketFS data.
      http_port, type: Int, Port for FS access.
      https_port, type: Int, Port for SSL encrypted FS access.


  Method addDatabase
        Create a new object type Database

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
    * clients_port_number, type: Int, Port for client connections.
    * data_disk, type: Choice, Disk for runtime data (log files and data/tmp files for non-storage databases)
      data_volume, type: Choice, Volume for EXASolution database data.
    * database_name, type: TextLine, The name of current database.
    * database_version, type: Choice, Version of EXASolution executables.
      enable_auditing, type: Bool, Enable auditing for database
      extra_params, type: TextLine, Extra parameters for startup of database.
      ldap_server, type: TextLine, LDAP Server to use for remote database authentication, e.g. ldap[s]://192.168.16.10 . Multiple servers must be separated by commas.
    * memory_usage, type: Int, Amount of database memory (in GiB).
    * nodes_list, type: List, List of active and reserve nodes for this database.
    * nodes_number, type: Int, Number of online nodes for this database.
      redundancy_number, type: Int, Obsolete option for non-Storage databases: Number of copies of database files in cluster
      used_storage, type: Bool, Enable/Disable usage of EXAStorage for keeping of database's data.
      vlan_list, type: List, Network interfaces to use for database. Leave empty to use all possible network interfaces.
      volume_quota, type: Int, Maximal size of volume in (GiB), the database tries to shrink it on start if required and possible.
      volume_restore_delay, type: TextLine, Move failed volume nodes to used reserve nodes automaticaly after given amount of time, or disable it with no value.


  Method addJDBCDriver
        Create a new object type JDBCDriver

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
      comment, type: TextLine, Description of the driver, not required.
    * jdbc_main, type: TextLine, Name of the main class.
    * jdbc_name, type: TextLine, Name of the driver.
    * jdbc_prefix, type: TextLine, Prefix of the JDBC name, must begin with "jdbc:" and ends with ":", like in "jdbc:mysql:".


  Method addKeyStore
        Create a new object type KeyStore

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
    * key_store_attributes, type: TextLine, Attributes for key store, e.g. LIB=/usr/lunasa/lib/libCryptoKI.so;SLOT=1
    * key_store_name, type: TextLine, Name of key store in EXAoperation
    * key_store_type, type: Choice, Type of key store.
    * keylabel, type: TextLine, Label to identify the key in the security module.


  Method addLogService
        Create a new object type LogService

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
      default_interval, type: TextLine, This time interval is shown per default.
      description, type: TextLine, Some description of this logservice.
      exaclusteros_services, type: List, EXAClusterOS services which should be visible at monitor, possible values: 'EXAoperation', 'DWAd', 'Lockd', 'Load', 'Storage', 'Appserver'
      exasolution_systems, type: List, Database systems which should be visible at monitor.
    * priority, type: Choice, Specifies the lowest priority of messages that this logservice will show., allowed values: [u'Error', u'Warning', u'Notice', u'Information']
      remote_syslog_protocol, type: Choice, Protocol to use to communicate with remote syslog server (TCP/UDP)., allowed values: [u'TCP', u'UDP']
      remote_syslog_server, type: TextLine, Log messages periodically to the specified remote syslog server via TCP.


  Method addNode
        Create a new object type Node

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
    * boot_interface, type: Choice, Interface to use for PXE boot.
      console_redirect, type: Bool, Redirect kernel output to serial console.
    * cpu_scaling_governor, type: Choice, Power scheme for Node CPU(s)
      devices, type: List, The List of disk devices used on the node, use cluster's defaults if not given.
      diskenc, type: Choice, Type of encryption to use on disks, use cluster's defaults if not given.
      diskraid, type: Choice, The type of RAID to use on disks, use cluster's defaults if not given.
      external_number, type: Int, The external node number, this number is added to network IP address.
      force_fsck, type: Bool, Force filesystem check on next boot of this node.
      force_no_fsck, type: Bool, Force no filesystem check on next boot of this node.
      hugepages, type: Int, Amount of hugepages in GiB to allocate for database usage on this node. This is recommended for nodes with RAM > 512 GiB. See manual for details.
      idstring, type: TextLine, String to identificate this node, not required.
      ip_addr_ipmi, type: TextLine, Public Server Management Card IP address (only if group uses public addresses).
      ipmi_group, type: Choice, Group that the IPMI card of this node belongs to (if any).
    * mac_addr_eth0, type: TextLine, The MAC address of the first LAN interface.
    * mac_addr_eth1, type: TextLine, The MAC address of the second LAN interface.
      mac_addr_ipmi, type: TextLine, The MAC address of the Server Management interface.
      node_unique_id, type: TextLine, Number to identify node for this cluster instance.
    * number, type: Int, The node number in cluster, numbers 0-10 are reserved.
    * public_network_list, type: FixedDict, Additional public network interfaces in node.
      raidredundancy, type: Int, Number of copies of each datablock on RAID 10.
    * spool_disk, type: Choice, Disk for spool data of loading processes and other.
      to_install, type: Bool, Should this node to be installed next time when booted?
      to_wipe, type: Bool, Wipe disks of node on next boot. This process can take a lot of time
      use_4kib, type: Bool, Use 4 KiB alignment for hard disks to satisfy the 4 KiB sector size requirements.
    * vlan_list, type: FixedDict, Additional private network interfaces in node.


  Method addNodesFromXML
        Parses a xml_description to a XML with node definition and add new nodes,
    When overwrite is set to True, it will overwrite the existing nodes with the same names.
    Usage : cluster.addNodesFromXMl(xml_description, [overwrite])

  Method addPublicNetwork
        Create a new object type PublicNetwork

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
      bonding_network, type: Choice, Public network to bond this network with.
    * mtu, type: Choice, MTU (maximum transfer unit) size to use for this VLAN.
      network_address, type: TextLine, IP address of the network (e.g. 192.168.16.0/24).
    * public_network_description, type: TextLine, Description of this public network.


  Method addRemoteVolume
        Create a new object type RemoteVolume

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
    * allowed_users, type: List, List of users allowed to access volume.
      labels, type: List, A List of labels to identify the volume.
      options, type: TextLine, cleanvolume, noverifypeer, nocompression, forcessl, webdav, webhdfs, or s3. Separated by comma. See manual for details.
      password, type: Password, Password for remote archive.
    * readonly_users, type: List, List of users allowed to read volume.
    * url, type: TextLine, Remote URL for archive volume, e.g. "ftp://192.168.2.1:12345" or "smb:////192.168.2.1/backupshare".
      user, type: TextLine, Username for remote archive.


  Method addRoute
        Create a new object type Route

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
    * route_destination, type: TextLine, Destination for this route.
    * route_gateway, type: TextLine, Gateway for this route.
    * route_type, type: Choice, Type of route., allowed values: [u'Network', u'Host']


  Method addScriptExtension
        Create a new object type ScriptExtension

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
      description, type: TextLine,
      http_proxy, type: TextLine,
      https_proxy, type: TextLine,
    * script_name, type: TextLine, Name of package, e.g. 3to2, ggplot2
    * script_type, type: Choice,
    * url, type: TextLine, URL of software repository, e.g. https://pypi.python.org/simple


  Method addSrvMgmtGroup
        Create a new object type SrvMgmtGroup

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
    * ipmi_description, type: TextLine, Name of this IPMI group.
      ipmi_password, type: Password, Password of the IPMI card.
      ipmi_password_multiline, type: Text, Multiline password of the IPMI card.
    * ipmi_type, type: Choice, Type of the IPMI card.
    * ipmi_username, type: TextLine, Username for the IPMI card.
      public_ip_addresses, type: Bool, Location of IPMI cards (private/public network).


  Method addUser
        Create an EXAoperation user.

    Function takes a dictionary as a parameter.
    Allowed keys ( required keys are marked with * ):
    * user_login     - name of a user
    * password       - password (must be defined even when LDAP Authentification used)
    * user_title     - is shown in a status line
    user_description - short description
    ldapServer       - URL of ldap(s) service
    ldapFullDN       - Full DN string to authenticate user on LDAP Service

  Method addVLAN
        Create a new object type VLAN

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
      bonding_network, type: Choice, Private network to bond this network with.
    * mtu, type: Choice, MTU (maximum transfer unit) size to use for this VLAN.
    * vlan_description, type: TextLine, Description of this private network.


  Method applyRemoteSyslogSettings
        Apply remote syslog settings.

  Method clusterDesc
        Return cluster description

  Method deleteDatabaseCheck
        Check the posibility of delete database.

  Method deleteLogs
        Delete logs/coredumps.

  Method deleteNodeCheck
        Check the posibility of delete node.

  Method deleteNodeDiskCheck
        Check the posibility of delete node disk.

  Method deleteSubObject
        Delete the subobject, defined by it's name and all settings

  Method deleteUserById
        Delete a user by given User ID

  Method deleteUserByLogin
        Delete a user by a given login

  Method deleteVolumeCheck
        Check the posibility of delete volume.

  Method editMonitorThresholds
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * coredump_deletion_time, type: Int, Number of days after which coredumps will be deleted.
    * disk_usage_error, type: Int, Level upon which errors about disk space will be issued.
    * disk_usage_warning, type: Int, Level upon which warnings about disk space will be issued.
    * load_error, type: Int, Level upon which errors about load will be issued.
    * load_warning, type: Int, Level upon which warnings about load will be issued.
    * sqllog_deletion_time, type: Int, Number of days after which SQL logs will be deleted.
    * swap_error, type: Int, Level upon which errors about swap space will be issued.
    * swap_warning, type: Int, Level upon which warnings about swap space will be issued.


  Method editNodeClusterDefaults
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * default_data_size, type: Int, Default size of the Data disk in GiB.
    * default_devices, type: List, A list of disk devices used for disks as default.
    * default_diskenc, type: Choice, The default type of encryption to use for data disks.
    * default_diskraid, type: Choice, The default type of software RAID to use on disks.
    * default_os_size, type: Int, Default size of the OS disk in GiB.
    * default_raidredundancy, type: Int, Default number of copies of each datablock on the RAID 10 arrays.
    * default_swap_size, type: Int, Default size of the swap disk in GiB.


  Method editNodeClusterLicense
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * license_comment, type: TextLine, Description of this license.
    * license_companyname, type: TextLine, Name of the company that owns license.
    * license_distributor, type: TextLine, Distributor of the given license.
    * license_distributorid, type: TextLine, ID of the license distributor.
    * license_expiration, type: TextLine, License's expiration date in format yyyy-mm-dd
    * license_idnumber, type: TextLine, Identification number of this license produced by EXASOL.
    * license_maxdbmemory, type: Int, Allowed memory size for all databases used in this cluster.
    * license_serial_number, type: Text, Serial number of this license.
    * license_validation_key, type: Text, Key created by EXASOL for license validation.


  Method editNodeClusterNetwork
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * backup_bandwidth, type: Int, Maximum network bandwidth per node that backup job is allowed to use.
      cluster_desc, type: TextLine, Cluster name, that is shown to user.
      default_gateway, type: TextLine, Gateway IP address to external network.
      disable_broadcast, type: Bool, Disable usage of broadcasts, activate if network does not allow broadcasts.
      dns_server1, type: TextLine, IP address of first DNS server.
      dns_server2, type: TextLine, IP address of second DNS server.
    * external_network, type: TextLine, IP address of the network (e.g. 10.12.1.0/24).
      mtu_private, type: Choice, MTU (maximum transfer unit) size to use for private network.
      mtu_public, type: Choice, MTU (maximum transfer unit) size to use for public network.
      no_allow_http, type: Bool, Disable HTTP for EXAoperation and HTTP/FTP access to archive volumes. Option will take effect after restart of EXAoperation.
      no_mac_check, type: Bool, Disable check of the MAC addresses on booting of nodes, it also disables the reordering of network interfaces.
      ntp_key, type: TextLine, Key for NTP server (consists of Key ID and key [space separated])
      ntp_server1, type: TextLine, IP address of the first NTP server.
      ntp_server2, type: TextLine, IP address of the second NTP server.
      ntp_server3, type: TextLine, IP address of the third NTP server.
    * protected_node_mem, type: Int, Memory that must not be used by EXASolution.
      search_domain, type: TextLine, Search domain to use with DNS servers.
    * time_zone, type: Choice, The time zone of cluster.


  Method editNodeClusterPasswords
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * backup_password, type: Password, Password for the backup shares.
    * node_disk_password, type: Password, Password of the disks. When changed, all nodes must be reintalled.
      password_keystore, type: Choice, The key store to use for encryption of passwords.
    * vm_password, type: Password, Password for the VM shares.


  Method editNodeClusterVersions
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * exacluster_version, type: TextLine, Installed EXAClusterOS version.
    * exasolution_versions, type: List, List of Installed EXASolution versions.
    * plugins, type: List, List of installed plugins.


  Method editRemoteSyslogSettings
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
      remote_syslog_ca_cert, type: Text, Text containing certificate of remote syslog server(s).
      remote_syslog_encrypted, type: Bool, Defines whether or not to use TLS for transmission of syslog messages.


  Method editUser
        Edit an EXAoperation user
    Usage: cluster.editUser(user_login, user_data)


  Method getAllArchiveVolumes
        Return a list of all archive volumes(local and remote).

    Usage: cluster.getAllArchiveVolumes()


  Method getAllDatabaseNames
        Return the list of databases' names.

  Method getAllDatabases
        Return the list with all databases' ids

  Method getAllJDBCDrivers
        Return a list of all installed JDBC drivers,

    Usage: cluster.getAllJDBCDrivers()


  Method getAllKeyStores
        Return list of all defined Password storages

  Method getAllLogServices
        Return a list of all logservices.

    Usage: cluster.getAllLogServices()

  Method getAllPublicNetworks
        Return names of all public networks (sorted).

  Method getAllRoutes
        Return a list of all routes.

    Usage: cluster.getAllRoutes()


  Method getAllScriptExtensions
        Return a list of all installed UDF Libraries

  Method getAllSrvMgmtCardGroups
        Return a list of all Server Management Card Groups

    Usage: cluster.getAllSrvMgmtCardGroups()


  Method getAllUserLogins
        Return a list of all user logins

  Method getAllUsers
        Return a list of all users

  Method getAllUsersById
        Return a dictionary of all users by id

  Method getAllUsersByLogin
        Return a dictionary of all users byl login

  Method getAllVLANs
        Return names of all VLANs (sorted).

  Method getAvailableUpdatesList
        Return a list of available updates, if the Update URL is defined.

  Method getClusterNodesAsXMLBase64
        Return a base64-encoded string, that represent luster nodes in XML format

    Usage: cluster.getClusterNodesAsXMLBase64()


  Method getCoredumpDeletionTime
        Get deletion time of coredumps.

  Method getCurrentLicenseServer
        Returns the license Server number.

  Method getDefaultParameters
         Get list of current license default parameters.

  Method getDomainName
        Returns the domain name.

  Method getEXACOSVersion
        Return a string with current COS Version

  Method getEXASolutionVersions
        Return a list with installed EXASolution Versions

  Method getEXASuiteVersion
        Returns the version of the installed EXASuite package.

  Method getEXAoperationNodes
        Get list of nodes, where EXAoperation could run

  Method getInstallationHistory
        Return list of relevant installation details.

  Method getInstalledJDBCDrivers
        Return list of ids of all installed JDBC Drivers

  Method getKeyStoreByName
        Return a Password storage defined by name

  Method getKeyStoreByObjName
        Return a Password storage defined by name

  Method getLegalInfo
        Get list of al used 3rd-party licenses.

  Method getLicenseFeatures
        Get list of current license features and expiration date.

  Method getLicenseLimits
         Get list of current license limits.

  Method getLicenseProperties
        Get current license properties

  Method getLoginRole
        Return login role of specified user.

  Method getMonitoringThresholdValues
        Get monitoring threshold values.

  Method getNTPServiceState
        Get state of all NTP servers.

  Method getObsoleteEXASuiteVersions
        Get all possible obsolete EXASuite versions.

  Method getPlugins
        Return a list of installed plugins

  Method getPossibleEXAoperationNodes
        Returns online nodes.

  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    node_disk_password: Password of the disks. When changed, all nodes must be reintalled.
    password_keystore: The key store to use for encryption of passwords.


  Method getPublicNetwork
        Return real public network name from descriptive name or None.

  Method getPublicNetworkDescription
        Return real public network name from descriptive name or None.

  Method getRolesForObject
        Return a list of users with grants

    Usage: cluster.getRolesForObject(object_name, user_id)
    Parameters:
      object_name - name of an object in the cluster
      user_id     - id of a user (can be retrieved from cluster.getAllUsers())
                    If user_id is an empty string, then will be returned the list
                    of all granted roles for this object.
    The return value is a list of dictionaries. The keys are:
      user     - user id (as returned by cluster.getAllUsers() or used in cluster.getUserById() )
      role     - the role given to a user
      default  - False, if the role is granted directly to this object
                 True , if the role is derived from its parent object


  Method getServiceStates
        Get state of all necessary EXAClusterOS services.

  Method getSoftware
        Get new software version from remote repository.

  Method getSqlLogDeletionTime
        Get deletion time of sql logs.

  Method getSrvMgmtGroup
        Return description of a Server Management group from descriptive name or None.

  Method getSrvMgmtGroupDescription
        Return descriptive name of a Server Management card group.

  Method getSupportData
        Return the information for EXASOL support.

  Method getUpdateURL
        Get connection URL of update repository (including username/password).

  Method getUploadPackageState
        Return a state of Upload Package's process

  Method getUserById
        Return a user description by a given id

    Usage cluster.getUserById(user_id)
    Parameters:
      user_id - user's id (number as int or string)


  Method getUserByName
        Return a user description by a given login

    Usage: cluster.getUserByName(user_name)
    Parameters:
      user_name - user's login

  Method getVLAN
        Return real VLAN name from descriptive name or None.

  Method getVLANDescription
        Return descriptive name of a VLAN net.

  Method grantRole
        Set a given role on cluster object to user.

    Usage: cluster.grantRole(object_name, user_id, role_name)
    Parameters:
      object_name - name of an object in the cluster
      user_id     - id of a user (can be retrieved from cluster.getAllUsers() )
      role_name   - one of [u'User', u'Supervisor', u'Administrator', u'Master']


  Method havePlugins
        Return True if plugins are installed

  Method licenseUpdate
        Check and update the license aggreenments.

    Usage: cluster.licenseUpdate(license_data)
    Parameters: license_data - license data as xml-formatted string


  Method needEXAoperationRestart
        Return True if EXAoperation should be restarted

  Method ntpServersConfigured
        Return true if any NTP server is configured.

  Method numberOfAvailableNodes
        Return number of nodes a user can add or 1024*1024 (unlimited).

  Method powerOffLicenseServer
        Restart license server.

  Method reinitEXAoperationPriorities
        Set priority of EXAoperation nodes.

  Method removeAllScripts
        Remove all installed UDF Libraries.

  Method removeDatabase
        Remove an old database version.

    Parameters:
      version - EXASolution version to be removed.
    Raises UsageError if a database with a given version is configured in a cluster
    or if an error occured during a deletion.

  Method removeObsoleteEXASuite
        Remove obsolete software to save space.

  Method removePlugin
        Remove a plugin.

    Parameters:
      name - name of plugin to be deleted.
    Raises UsageError if an eror occured.

  Method restartEXAoperation
        Restart EXAoperation server.

    Usage: cluster.restartEXAoperation(node).
    Parameters:
      -node - a node name to start EXAoperation on. If '', the EXaoperation will be restarted on a current node.

  Method restartLicenseServer
        Restart license server.

  Method saveBucketFSChanges
        Save changes of bucketfs properties to file.

  Method setDefaultRole
        Unset all granted roles and set a default role for user.

    Usage: cluster.setDefaultRole(object_name, user_id)
    Parameters:
      object_name - name of an object in the cluster
      user_id     - id of a user (can be retrieved from cluster.getAllUsers() )


  Method setDiskPassword
        Set a node disk password.

    Usage: cluster.setDiskPassword(new_node_disk_password)

  Method setKeyStore
        Set a new new key store for cluster.

    Usage: cluster.setKeyStore(key_store_name)
    Parameters:  key_store_name - name of a key store as it defined in object's properties.

  Method setPriorities
        Set EXAoperation node priorities.

  Method synchronizeNTP
        Synchronize license server with NTP servers.

  Method uploadSoftware
        Upload a new database version.

SERVICE NodeClusterAfterAdd
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method getProperties
        This object has no properties.

SERVICE NodeClusterKeyStore
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method editNodeClusterKeyStore
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * key_store_attributes, type: TextLine, Attributes for key store, e.g. LIB=/usr/lunasa/lib/libCryptoKI.so;SLOT=1
    * key_store_name, type: TextLine, Name of key store in EXAoperation
    * key_store_type, type: Choice, Type of key store.
    * keylabel, type: TextLine, Label to identify the key in the security module.


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    key_store_attributes: Attributes for key store, e.g. LIB=/usr/lunasa/lib/libCryptoKI.so;SLOT=1
    key_store_name: Name of key store in EXAoperation
    key_store_type: Type of key store.
    keylabel: Label to identify the key in the security module.


  Method getStatus
        Get status of key store.

  Method lock
        Lock key.

  Method unlock
        Unlock key.

SERVICE NodeClusterPublicNetwork
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method editNodeClusterPublicNetwork
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
      bonding_network, type: Choice, Public network to bond this network with.
    * mtu, type: Choice, MTU (maximum transfer unit) size to use for this VLAN.
      network_address, type: TextLine, IP address of the network (e.g. 192.168.16.0/24).
    * public_network_description, type: TextLine, Description of this public network.


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    bonding_network: Public network to bond this network with.
    mtu: MTU (maximum transfer unit) size to use for this VLAN.
    network_address: IP address of the network (e.g. 192.168.16.0/24).
    public_network_description: Description of this public network.


SERVICE NodeClusterRoute
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method editNodeClusterRoute
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * route_destination, type: TextLine, Destination for this route.
    * route_gateway, type: TextLine, Gateway for this route.
    * route_type, type: Choice, Type of route., allowed values: [u'Network', u'Host']


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    route_destination: Destination for this route.
    route_gateway: Gateway for this route.
    route_type: Type of route.


SERVICE NodeClusterSrvMgmtGroup
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method editNodeClusterSrvMgmtGroup
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * ipmi_description, type: TextLine, Name of this IPMI group.
      ipmi_password, type: Password, Password of the IPMI card.
      ipmi_password_multiline, type: Text, Multiline password of the IPMI card.
    * ipmi_type, type: Choice, Type of the IPMI card.
    * ipmi_username, type: TextLine, Username for the IPMI card.
      public_ip_addresses, type: Bool, Location of IPMI cards (private/public network).


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    ipmi_description: Name of this IPMI group.
    ipmi_password: Password of the IPMI card.
    ipmi_password_multiline: Multiline password of the IPMI card.
    ipmi_type: Type of the IPMI card.
    ipmi_username: Username for the IPMI card.
    public_ip_addresses: Location of IPMI cards (private/public network).


SERVICE NodeClusterVLAN
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method editNodeClusterVLAN
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
      bonding_network, type: Choice, Private network to bond this network with.
    * mtu, type: Choice, MTU (maximum transfer unit) size to use for this VLAN.
    * vlan_description, type: TextLine, Description of this private network.


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    bonding_network: Private network to bond this network with.
    mtu: MTU (maximum transfer unit) size to use for this VLAN.
    vlan_description: Description of this private network.


SERVICE NodeDisk
Object: https://<user>:<pass>@<cluster_node>/cluster1/<node_name>/<object_name>/
  Method addDevice
        Append device with given name to the current disk of an active node.

  Method diskIsExtendable
        Returns True if new devices could be added to this disk.

  Method editNodeDisk
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
      devices, type: List, The List of disk devices used on the node, use cluster's defaults if not given.
      diskenc, type: Choice, Type of encryption to use on disks, use cluster's defaults if not given.
      disklabel, type: TextLine, Label for disk.
      diskraid, type: Choice, The type of RAID to use on disks, use cluster's defaults if not given.
      disksize, type: Int, The size of this disk in GiB or maximum if not entered.
      raidredundancy, type: Int, Number of copies of each datablock on RAID 10.


  Method getProperties
        This object has no properties.

SERVICE RemoteVolume
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method editRemoteVolume
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * allowed_users, type: List, List of users allowed to access volume.
      labels, type: List, A List of labels to identify the volume.
      options, type: TextLine, cleanvolume, noverifypeer, nocompression, forcessl, webdav, webhdfs, or s3. Separated by comma. See manual for details.
      password, type: Password, Password for remote archive.
    * readonly_users, type: List, List of users allowed to read volume.
    * url, type: TextLine, Remote URL for archive volume, e.g. "ftp://192.168.2.1:12345" or "smb:////192.168.2.1/backupshare".
      user, type: TextLine, Username for remote archive.


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    allowed_users: List of users allowed to access volume.
    labels: A List of labels to identify the volume.
    options: cleanvolume, noverifypeer, nocompression, forcessl, webdav, webhdfs, or s3. Separated by comma. See manual for details.
    password: Password for remote archive.
    readonly_users: List of users allowed to read volume.
    url: Remote URL for archive volume, e.g. "ftp://192.168.2.1:12345" or "smb:////192.168.2.1/backupshare".
    user: Username for remote archive.


  Method getVolumeId
        Return 'virtual' volume ID of remote archive volume.

  Method state
        Return connectivity state of remote archive volume.

SERVICE ScriptExtension
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method editEXAPScript
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
      description, type: TextLine,
      http_proxy, type: TextLine,
      https_proxy, type: TextLine,
    * script_name, type: TextLine, Name of package, e.g. 3to2, ggplot2
    * script_type, type: Choice,
    * url, type: TextLine, URL of software repository, e.g. https://pypi.python.org/simple


  Method getInstallationLog
        Get installation log of script.

  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    description:
    http_proxy:
    https_proxy:
    script_name: Name of package, e.g. 3to2, ggplot2
    script_type:
    url: URL of software repository, e.g. https://pypi.python.org/simple


  Method getStatus
        Get installation status of script.

  Method installNow
        Install script now.

SERVICE SetupCommand
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    cmd: Command to execute.


SERVICE SetupNodeNumber
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    node_number: Node number of the EXAoperation node.


SERVICE SetupValue
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    value: Value of parameter.


SERVICE Storage
Object: https://<user>:<pass>@<cluster_node>/cluster1/storage/
  Method addStorageVolume
        Create a new object type StorageVolume

    Function takes a dictionary with parameters.
    Allowed keys are (required fields are marked  with * ):
    * allowed_users, type: List, List of users, who are allowed to access this volume.
      block_size, type: Int, Size of volume blocks in volume in KiB.
    * hdd_type, type: Choice, Disk to create volume on.
      labels, type: List, List of labels to identify the volume.
    * masternodes, type: Int, Number of master nodes for volume; must match to number of DB nodes in case of data volume.
    * nodes_list, type: List, List of nodes to use as volume storage.
      priority, type: Int, Priority of volume between 1 and 20, higher number means higher priority. Default value is 10.
      readonly_users, type: List, List of users, who are allowed to read this volume.
    * redundancy, type: Int, Number of redundancy segments per volume part.
    * size, type: Int, Size of volume in GiB.
    * volume_type, type: Choice, Type of data stored on this volume., allowed values: [u'Data', u'Archive']


  Method checkNodeDiskInformation
        Return node list about nodes whose disks can be checked.

  Method deleteMetadata
        Delete Storage metadata from all online nodes.

  Method editStorage
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
    * vlan_list, type: List, Network interfaces to use for storage. Leave empty to use the first network interface.


  Method getArchiveFilesystems
        Return dictionary with permitted for a user remote and archive volumes.
    The returned values are tupples (<OBJECT_TYPE>, <ID>, <PERMISSIONS>)

    Usage: storage.getArchiveFileSystems()


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    vlan_list: Network interfaces to use for storage. Leave empty to use the first network interface.


  Method getStorageInfo
        Returns information about storage.

  Method getVolumeInfo
        Returns information about volume.

    Usage: storage.getVolumeInfo(vid)
    Parameters:
      vid - volume id as returned by getVolumeList().


  Method getVolumeList
        Return a dictionary with description of volumes in EXAStorage.

    Usage: storage.getVolumeList()


  Method nodesInformation
        Returns information about nodes.

  Method nodesListInformation
        Returns information about Storage nodes.

  Method serviceHasAutoRestartFlag
        Return True if auto-restart flag is set for Storage service.

  Method serviceIsOnline
        Return True if the storage service is online.

  Method setAutoRestartFlag
        Set auto-restart flag for Storage service.

  Method storageHasQuorum
        Return a boolean, showing if storage service has quorum.

  Method volumeRemove
        Remove volume

SERVICE StorageNode
Object: https://<user>:<pass>@<cluster_node>/cluster1/storage/<object_name>/
  Method addUnusedDevices
        Add all disks, which are not added before.

    Usage: storage_node.addUnusedDevices(devices)
    Parameters: list of devices to add. If empty list ([]), all devives will be added.
    Return a list of dictionaries with added devices Keys are:
      name
      type
      disk.

  Method changeable
        Return whether node could contain Storage disks.

  Method clearDeviceErrors
        Clear device errors counter.

  Method disableBgRecovery
        Disable background recovery.

  Method disableDevices
        Disable list of devices.

  Method enableBgRecovery
        Enable background recovery.

  Method enableDevices
        Enable list of devices.

  Method enlargeDevices
        Enlarge list of devices.

  Method forceBgRecoveryLimitCalibration
        Force background recalibration.

  Method getAllDevices
        Return a list of disks on a node.

    Usage: storage_node.getAllDevices()


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    auto_bg_rec_limit: Automatic background recovery limit in MiB.
    bg_rec_limit: Background recovery limit in MiB.
    bg_recovery_enabled: Status of node background recovery
    disk_free_space: Space not used by volumes in GiB on given disk.
    disk_space: Overall disk space in GiB on this node.
    disk_sum_space: Size of disk in GiB.
    free_space: Space not used by volumes in GiB on this node.
    link_speed: Background recovery limit in MiB.
    nid: EXAClusterOS logical node ID of the given node.
    node_size: Space used by volumes in GiB on this node.
    phys_nid: EXAClusterOS physical node ID of the given node.
    state: State of the volume.


  Method getUnusedDevices
        Return a list of devices which are not used in storage.

    Usage: storage_node.getUnusedDevices(disk)

    Parameters:
      disk - to get unused devices on a specific disk. If disk is an empty string,
             a corresponding disk will be found

  Method nodeIsSuspended
        Return wheter node is suspended or not.

  Method removeDevices
        Remove list of devices.

    Usage: storage_node.removeDevices(devnames)
    Parameters:
      devnames - list of disk names. The name of disk is returned by storage_node.getAllDevices, dictionary key 'name'.


  Method restartNode
        Restart current node (only the storage service, not the node it self).

  Method resumeNode
        Resume node.

  Method setBgRecoveryLimit
        Set background recovery limit in MiB for node.

  Method suspendNode
        Suspend node.

SERVICE StorageNodeHDD
Object: https://<user>:<pass>@<cluster_node>/cluster1/storage/<storage_node_name>/<object_name>/
  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    crc_error: CRC error flag for given HDD.
    hid: ID of given HDD.
    io_error: IO error flag for given HDD.
    name: Name of the given HDD.
    num_sectors: Number of sectors on given HDD.
    read_only: Read only flag for given HDD.
    sector_size: Size of sector on given HDD.
    state: HDD State.
    type: Disk used for given HDD.


  Method isEnlargeable
        Deliver information about enlargeability of device.

SERVICE StorageVolume
Object: https://<user>:<pass>@<cluster_node>/cluster1/storage/<object_name>/
  Method checkPermissions
        Check permissions to access this volume.

  Method editStorageVolume
         Edits object.

    Function take a dictionary with parameters and return a list of fields, that was modified.
    Allowed keys are (required fields are marked  with * ):
      add_master_nodes, type: Int, Number of master nodes that should be added.
      add_nodes_list, type: List, List of nodes that should be added to volume.
    * allowed_users, type: List, List of users, who are allowed to access this volume.
      labels, type: List, List of labels to identify the volume.
      priority, type: Int, Priority of volume between 1 and 20, higher number means higher priority. Default value is 10.
      readonly_users, type: List, List of users, who are allowed to read this volume.
    * redundancy, type: Int, Number of redundancy segments per volume part.


  Method formatFilesystem
        Format SDFS Filesystem.

  Method getFilesList
        Return list of files in an archive node.

    usage: storage_archive_volume.getFilesList()


  Method getPermissions
        Get permissions to access this volume.

  Method getProperties
        This object has no properties.

  Method moveNodes
        Move nodes according to nodes map.

  Method removeFile
        Remove file with given ID.

  Method resizeVolume
        Add given amount of GiB's to volume size.

  Method setFileExpiration
        Set file expiration time, 'exptime' argument is number of seconds since the Epoch.

  Method setIoState
        Set IO state for Volume application or internal IO.

SERVICE StorageVolumeAddSchema
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    block_size: Size of volume blocks in volume in KiB.
    hdd_type: Disk to create volume on.
    masternodes: Number of master nodes for volume; must match to number of DB nodes in case of data volume.
    nodes_list: List of nodes to use as volume storage.
    size: Size of volume in GiB.
    volume_type: Type of data stored on this volume.


SERVICE StorageVolumeNode
Object: https://<user>:<pass>@<cluster_node>/cluster1/storage/<storage_volume_name>/<object_name>/
  Method getAllSegments
        Return list of volume node segments.

    Usage: storage_volume_node.getAllSegments()

  Method getProperties
        This object has no properties.

  Method getSegmentsDescriptions
        Return a list with descriptions of a segments

    Usage: storage_volume_node.getSegmentsDescription()

  Method moveNode
        Move node to destination node.

  Method recoverNode
        Recreate this node from redundancy.

  Method stopRecoverNode
        Stop node restore.

SERVICE StorageVolumeNodeSegment
Object: https://<user>:<pass>@<cluster_node>/cluster1/storage/<storage_volume_name>/<storage_volume_node>/<object_name>/
  Method getPartitions


  Method getProperties
        Function returns a dictionary that describes an object. Keys are:
    end_block: Block number, on which the segment ends in volume.
    index:
    partitions: List of Partitions.
    remote_sid: SID of the remote segment, in case of slave segments.
    segment_size: Size of this segment in KiB.
    sid: ID of the segment.
    snapshot_state: Snapshot done on volume node segment in percents.
    start_block: Block number, on which the segment begins in volume.
    state: State of the segment.
    type: Type of the segment.


SERVICE SupportDebugInfo
Object: https://<user>:<pass>@<license_server>/cluster1/<object_name>
  Method downloadDebugInfo
        Download debug information.

  Method estimateDebugInfoSize
        Get estimated size of debug information.

  Method getProperties
        This object has no properties.

  Method storeDebugInfo
        Store debug information into archive volume.

```
