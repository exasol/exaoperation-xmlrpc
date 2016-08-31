# EXAoperation XMLRPC API

## Generic methods

Methods, which are available for every service.

### Method `getPath`

Return absolute and relative pathes to current object

Usage: `object.getPath()`

### Method `getListValues`

Return various list values depending on a type of object.

Usage: `object.getListValues(list)`
Parameters:
* `list`
  Name of a list, possible values are:
  * `BootInterface`
  * `DataDisks`
  * `DatabaseNetworkInterfaces`
  * `Databases`
  * `Days`
  * `DiskTypes`
  * `Disks`
  * `EXASolutionVersions`
  * `EncrTypes`
  * `ExapScriptTypes`
  * `KeyStoreTypes`
  * `KeyStore`
  * `Mtu`
  * `NodesDeactivate`
  * `NodesReactivate`
  * `NodesReserve`
  * `Nodes`
  * `PublicNetwork`
  * `RaidTypes`
  * `ScalingGovernor`
  * `SrvMgmtGroup`
  * `SrvMgmtTypes`
  * `StorageDisks`
  * `StorageVolumeNodes`
  * `TimeZones`
  * `Users`
  * `VLAN`
  * `Volumes`

### Method `listMethods`

Introspection function. Return a list of all supported methods.

Usage: `object.listMethods()`

### Method `methodHelp`

Introspection method. Return a description for a given function.

Usage: `object.methodHelp(method_name)`
  
### Method `methodSignature`

Introspection method. Return a list of parameters for a given function. Function is not completly supported, please call object.methodHelp() to get a description of a parameters.

Usage: `object.methodSignature(method_name)`

## Service `BucketFS`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `addBucket`

Create a new object type BucketFSBucket

Function takes a dictionary with parameters, allowed keys are:
* `bucket_name` (`TextLine`)
  The name of bucket.
* `description` (`TextLine`, optional)
  Some description of this BucketFS Bucket.
* `public_bucket` (`Bool`)
  Public buckets require no password for reading.
* `read_password` (`Password`)
  Password readonly access.
* `write_password` (`Password`)
  Password for write access.

### Method `deleteSubObject`

Delete the subobject, defined by it's name and all settings

### Method `editBucketFS`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `description` (`TextLine`, optional)
  Some description of this BucketFS.
* `disk` (`Choice`)
  Disk for BucketFS data.
* `http_port` (`Int`, optional)
  Port for FS access.
* `https_port` (`Int`, optional)
  Port for SSL encrypted FS access.

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `description`
  Some description of this BucketFS.
* `disk`
  Disk for BucketFS data.
* `http_port`
  Port for FS access.
* `https_port`
  Port for SSL encrypted FS access.

## Service `BucketFSBucket`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `editBucketFSBucket`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `bucket_name` (`TextLine`)
  The name of bucket.
* `description` (`TextLine`, optional)
  Some description of this BucketFS Bucket.
* `public_bucket` (`Bool`)
  Public buckets require no password for reading.
* `read_password` (`Password`)
  Password readonly access.
* `write_password` (`Password`)
  Password for write access.

### Method `getProperties`

This object has no properties.

## Service `Database`

URL: `https://<user>:<pass>@<cluster_node>/cluster1/db_<object_name>/`

Note: the EXASolution systems need prefix 'db_'

### Method `abortBackup`

Abort running database backup.

### Method `abortShrink`

Abort shrink operation of database.

### Method `backupDatabase`

Start backup to given storage volume with given level and expiration time.

Parameters:
  volume - name of volume where to write backup
  level  - backup level
  expire - expire time for backup

### Method `backupInfo`

Return information for a backup.

### Method `changeBackupExpiration`

Change expiration time of a backup.

### Method `createDatabase`

Create a fresh database, must not exist jet.

### Method `deleteBackups`

Delete given backups

Usage: database.deleteBackups(backup_list)
Parameters: 
  backup_list - a list of backups, Can be recieved with database.backupList()

### Method `deleteUnusableBackups`

Delete all unusable backups for current database.

Usage: database.deleteUnusableBackups()

### Method `editDatabase`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `clients_port_number` (`Int`)
  Port for client connections.
* `data_volume` (`Choice`)
  Volume for EXASolution database data.
* `database_comment` (`TextLine`, optional)
  User-defined comment for database (200 charachters max)
* `database_version` (`Choice`)
  Version of EXASolution executables.
* `enable_auditing` (`Bool`, optional)
  Enable auditing for database
* `extra_params` (`TextLine`, optional)
  Extra parameters for startup of database.
* `ldap_server` (`TextLine`, optional)
  LDAP Server to use for remote database authentication, e.g. ldap[s]://192.168.16.10 . Multiple servers must be separated by commas.
* `memory_usage` (`Int`)
  Amount of database memory (in GiB).
* `nodes_list_add_reserve` (`List`, optional)
  List of nodes, which should be added to the system as reserve nodes.
* `nodes_list_deactivate` (`List`, optional)
  List of nodes which should be deactivated for this system.
* `nodes_list_reactivate` (`List`, optional)
  List of nodes which should be reactivated for this system.
* `nodes_list_remove_reserve` (`List`, optional)
  List of nodes which should be removed from the System as reserve nodes.
* `vlan_list` (`List`, optional)
  Network interfaces to use for database. Leave empty to use all possible network interfaces.
* `volume_quota` (`Int`, optional)
  Maximal size of volume in (GiB), the database tries to shrink it on start if required and possible.
* `volume_restore_delay` (`TextLine`, optional)
  Move failed volume nodes to used reserve nodes automaticaly after given amount of time, or disable it with no value.

### Method `enlargeDatabase`

Enlarge an existing database. Precondition: the database should be stopped.
Warning - the changes made by this function could not be undone. Function increase
the number of active nodes of the database.

Usage: database.enlargeDatabase(count_of added_active_nodes)
Parameters:
  count_of_added_active_nodes - a number of nodes, that will be ADDED to an existing number.

### Method `existDatabase`

Return whether the database exists or not.

### Method `forceShutdownDatabase`

Force shutdown of database, must be running.

### Method `getBackgroundRestoreState`

Returns current background restore state.

### Method `getBackupSchedule`

Return a list of scheduled backups

### Method `getBackups`

Return a list of available backups for this database.

Usage: database.getBackups(show_all_databases, show_expired_backups)
Parameters:
  show_all_databases - show backups not for only this database
  show_expired_backups - not exclude expired backups from list

### Method `getCurrentDatabaseSize`

Get current database size.

### Method `getCurrentErrors`

Get current reasons for not starting a database.

### Method `getDatabaseVersion`

Return current database version.

### Method `getDatabaseVolumeNodesMatch`

Return information about database nodes match to volume nodes.

### Method `getDatabaseVolumeOfflineSegments`

Return number of offline data volume segments.

### Method `getNextSchedules`

Get scheduling for next period of time.

### Method `getNodeState`

Return the state of a node: online, offline or failed.

### Method `getPddProgress`

Get information about current PDD processes (Backup/Restore).

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `clients_port_number`
  Port for client connections.
* `data_volume`
  Volume for EXASolution database data.
* `database_comment`
  User-defined comment for database (200 charachters max)
* `database_version`
  Version of EXASolution executables.
* `enable_auditing`
  Enable auditing for database
* `extra_params`
  Extra parameters for startup of database.
* `ldap_server`
  LDAP Server to use for remote database authentication, e.g. ldap[s]://192.168.16.10 . Multiple servers must be separated by commas.
* `memory_usage`
  Amount of database memory (in GiB).
* `nodes_list_add_reserve`
  List of nodes, which should be added to the system as reserve nodes.
* `nodes_list_deactivate`
  List of nodes which should be deactivated for this system.
* `nodes_list_reactivate`
  List of nodes which should be reactivated for this system.
* `nodes_list_remove_reserve`
  List of nodes which should be removed from the System as reserve nodes.
* `vlan_list`
  Network interfaces to use for database. Leave empty to use all possible network interfaces.
* `volume_quota`
  Maximal size of volume in (GiB), the database tries to shrink it on start if required and possible.
* `volume_restore_delay`
  Move failed volume nodes to used reserve nodes automaticaly after given amount of time, or disable it with no value.

### Method `maintenanceDatabase`

Get maintenance state of database.

### Method `operationGetCurrent`

Return the current operation

### Method `restartDatabase`

Restart database which must be running.

### Method `restoreDatabase`

Start restore from given backup ID and restore type.

  Usage: database.restoreDatabase(backup_id, restore_type)
  Parameters: 
    backup_name - could be obtained by getBackups(), field 'id'. Must have three valus separated by space.
    restore_type - type of restore. Must be one of following - {'blocking'|'nonblocking'|'virtual access'}

### Method `runningDatabase`

Return whether the database is started.

### Method `setBackupSchedule`

Set a list of all scheduled backups.
    
Parameter:
  list of backup definitions

### Method `shrinkDatabase`

Shrink a database. This operation can only be apply for running databases.

Usage: database.shrinkDatabase(target_size_in_gb)
Parameters:
  target_size_in_gb - target size for shrink operation.

### Method `shutdownDatabase`

Shutdown the database, must be running.

### Method `startDatabase`

Startup the database, must exists and must not be running.

### Method `startDatabaseMaintenance`

Start database in maintenance mode, must exist and must not be running.

### Method `stateDatabase`

Return human-readable state of database.

## Service `JDBCDriver`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `editJDBCDriver`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `comment` (`TextLine`, optional)
  Description of the driver, not required.
* `jdbc_main` (`TextLine`)
  Name of the main class.
* `jdbc_name` (`TextLine`)
  Name of the driver.
* `jdbc_prefix` (`TextLine`)
  Prefix of the JDBC name, must begin with "jdbc:" and ends with ":", like in "jdbc:mysql:".

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `jdbc_jars`
  List of URLs to the JDBC JAR files.

### Method `removeJARFiles`

Remove cached JAR files.

### Method `uploadFile`

Upload given file.

## Service `LogService`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `cleanupLogservice`

Cleanup the logservice directory structure before deleting it.

### Method `editLogService`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `default_interval` (`TextLine`, optional)
  This time interval is shown per default.
* `description` (`TextLine`, optional)
  Some description of this logservice.
* `exaclusteros_services` (`List`, optional)
  EXAClusterOS services which should be visible at monitor, possible values: 'EXAoperation', 'DWAd', 'Lockd', 'Load', 'Storage'
* `exasolution_systems` (`List`, optional)
  Database systems which should be visible at monitor.
* `priority` (`Choice`)
  Specifies the lowest priority of messages that this logservice will show.

  Allowed values:
  * Error
  * Warning
  * Notice
  * Information

* `remote_syslog_protocol` (`Choice`, optional)
  Protocol to use to communicate with remote syslog server (TCP/UDP).

  Allowed values:
  * TCP
  * UDP

* `remote_syslog_server` (`TextLine`, optional)
  Log messages periodically to the specified remote syslog server via TCP.

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `default_interval`
  This time interval is shown per default.
* `description`
  Some description of this logservice.
* `exaclusteros_services`
  EXAClusterOS services which should be visible at monitor, possible values: 'EXAoperation', 'DWAd', 'Lockd', 'Load', 'Storage'
* `exasolution_systems`
  Database systems which should be visible at monitor.
* `priority`
  Specifies the lowest priority of messages that this logservice will show.
* `remote_syslog_protocol`
  Protocol to use to communicate with remote syslog server (TCP/UDP).
* `remote_syslog_server`
  Log messages periodically to the specified remote syslog server via TCP.

### Method `logFetchEntries`

Fetch log entries from the Logd service.
    Parameters:
    start, halt - tuples (yyyy, mm, dd, hh, mi, ss, msec)
    errlevel    - lowest message level to fetch, possible values: ['Information', 'Notice', 'Warning', 'Error']
    priority    - tag

## Service `Node`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `addNodeDisk`

Create a new object type NodeDisk

Function takes a dictionary with parameters, allowed keys are:
* `devices` (`List`, optional)
  The List of disk devices used on the node, use cluster's defaults if not given.
* `disk_number` (`Int`, optional)
  Disk number in the name of disk, if not specified, then given automatically.
* `diskenc` (`Choice`, optional)
  Type of encryption to use on disks, use cluster's defaults if not given.
* `disklabel` (`TextLine`, optional)
  Label for disk.
* `diskraid` (`Choice`, optional)
  The type of RAID to use on disks, use cluster's defaults if not given.
* `disksize` (`Int`, optional)
  The size of this disk in GiB or maximum if not entered.
* `disktype` (`Choice`)
  Type of storage for which this disk will be used.
* `raidredundancy` (`Int`, optional)
  Number of copies of each datablock on RAID 10.

### Method `addStorageDisk`

Add aditional storage disk do an active node.

Usage: node.addStorageDisk(devices, enc, label, size, number)
Parameters: devices   - List of devices to use
            label     - Label of the new disk
            enc       - Encryption to use (none, aes128, aes256)
            number    - Use this disk number, if None or not given, generate new number

Only storage disks and disks without redundancy can be added to an
active node. Devices must not be used by any other disk.

### Method `applyDefaultDiskLayout`

Apply default disk layout to this node.

### Method `copyNode`

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

### Method `deleteDisks`

Remove disk with given name.

### Method `deleteSubObject`

Delete the subobject, defined by it's name and all settings

### Method `editNode`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `boot_interface` (`Choice`)
  Interface to use for PXE boot.
* `console_redirect` (`Bool`, optional)
  Redirect kernel output to serial console.
* `cpu_scaling_governor` (`Choice`)
  Power scheme for Node CPU(s)
* `devices` (`List`, optional)
  The List of disk devices used on the node, use cluster's defaults if not given.
* `diskenc` (`Choice`, optional)
  Type of encryption to use on disks, use cluster's defaults if not given.
* `diskraid` (`Choice`, optional)
  The type of RAID to use on disks, use cluster's defaults if not given.
* `external_number` (`Int`, optional)
  The external node number, this number is added to network IP address.
* `force_fsck` (`Bool`, optional)
  Force filesystem check on next boot of this node.
* `force_no_fsck` (`Bool`, optional)
  Force no filesystem check on next boot of this node.
* `hugepages` (`Int`, optional)
  Amount of hugepages in GiB to allocate for database usage on this node. This is recommended for nodes with RAM > 512 GiB. See manual for details.
* `idstring` (`TextLine`, optional)
  String to identificate this node, not required.
* `ip_addr_ipmi` (`TextLine`, optional)
  Public Server Management Card IP address (only if group uses public addresses).
* `ipmi_group` (`Choice`, optional)
  Group that the IPMI card of this node belongs to (if any).
* `mac_addr_eth0` (`TextLine`)
  The MAC address of the first LAN interface.
* `mac_addr_eth1` (`TextLine`)
  The MAC address of the second LAN interface.
* `mac_addr_ipmi` (`TextLine`, optional)
  The MAC address of the Server Management interface.
* `public_network_list` (`FixedDict`)
  Additional public network interfaces in node.
* `raidredundancy` (`Int`, optional)
  Number of copies of each datablock on RAID 10.
* `spool_disk` (`Choice`)
  Disk for spool data of loading processes and other.
* `to_install` (`Bool`, optional)
  Should this node to be installed next time when booted?
* `to_wipe` (`Bool`, optional)
  Wipe disks of node on next boot. This process can take a lot of time
* `use_4kib` (`Bool`, optional)
  Use 4 KiB alignment for hard disks to satisfy the 4 KiB sector size requirements.
* `vlan_list` (`FixedDict`)
  Additional private network interfaces in node.

### Method `fixChecksums`

Fix/delete checksums of disks.

### Method `getAllDisks`

Return list of disk names.

### Method `getDeviceInfo`

Return information about devices.

### Method `getDiskInfo`

Return info about disk

### Method `getNodeInfo`

Return node information.

### Method `getProperties`

This object has no properties.

### Method `getSrvMgmtConsoleParameters`

Return info about parameters necessary for Server Management console

### Method `nodeRunning`

Return whether the node is running.

### Method `poweroffNode`

Power off the node immediatly.

### Method `rebootNode`

Reboot the node.

### Method `resetNode`

Reset the node immediatly.

### Method `setActiveMode`

Set the node to Active state. The node in active state is available to all cluster services.

Usage: node.setActiveMode()

### Method `setForceFSCKMode`

Set the node to Force fsck state.

Usage: node.setFSCKMode()

### Method `setForceNoFSCKMode`

Set the node to Force No fsck state.

Usage: node.setNoFSCKMode()

### Method `setInstallMode`

Set the node to Install state. After next reboot the node will be installed.

Usage: node.setInstallMode()

### Method `setWipeMode`

Set the node to To Wipe state. After boot the all data will be erased.
    
Usage: node.setWipeMode()

### Method `shutdownNode`

Shutdown the node.

### Method `startClusterServices`

Start Core daemon on this node.

### Method `startupNode`

Power on and startup the node.

### Method `stopClusterServices`

Stop Core daemon on this node.

### Method `toggleIdLed`

Toggle the ID LED on the given node.

## Service `NodeCluster`

URL: `https://<user>:<pass>@<cluster_node>/cluster1/`

### Method `activateNodes`

Set nodes from a given list node_names to active state.
Usage:
nodes_list = [u'n0110', u'n0108']
cluster.activateNodes(nodes_list)

### Method `addBucketFS`

Create a new object type BucketFS

Function takes a dictionary with parameters, allowed keys are:
* `description` (`TextLine`, optional)
  Some description of this BucketFS.
* `disk` (`Choice`)
  Disk for BucketFS data.
* `http_port` (`Int`, optional)
  Port for FS access.
* `https_port` (`Int`, optional)
  Port for SSL encrypted FS access.

### Method `addDatabase`

Create a new object type Database

Function takes a dictionary with parameters, allowed keys are:
* `clients_port_number` (`Int`)
  Port for client connections.
* `data_disk` (`Choice`)
  Disk for runtime data (log files and data/tmp files for non-storage databases)
* `data_volume` (`Choice`)
  Volume for EXASolution database data.
* `database_name` (`TextLine`)
  The name of current database.
* `database_version` (`Choice`)
  Version of EXASolution executables.
* `enable_auditing` (`Bool`, optional)
  Enable auditing for database
* `extra_params` (`TextLine`, optional)
  Extra parameters for startup of database.
* `ldap_server` (`TextLine`, optional)
  LDAP Server to use for remote database authentication, e.g. ldap[s]://192.168.16.10 . Multiple servers must be separated by commas.
* `memory_usage` (`Int`)
  Amount of database memory (in GiB).
* `nodes_list` (`List`)
  List of active and reserve nodes for this database.
* `nodes_number` (`Int`)
  Number of online nodes for this database.
* `vlan_list` (`List`, optional)
  Network interfaces to use for database. Leave empty to use all possible network interfaces.
* `volume_quota` (`Int`, optional)
  Maximal size of volume in (GiB), the database tries to shrink it on start if required and possible.
* `volume_restore_delay` (`TextLine`, optional)
  Move failed volume nodes to used reserve nodes automaticaly after given amount of time, or disable it with no value.

### Method `addJDBCDriver`

Create a new object type JDBCDriver

Function takes a dictionary with parameters, allowed keys are:
* `comment` (`TextLine`, optional)
  Description of the driver, not required.
* `jdbc_main` (`TextLine`)
  Name of the main class.
* `jdbc_name` (`TextLine`)
  Name of the driver.
* `jdbc_prefix` (`TextLine`)
  Prefix of the JDBC name, must begin with "jdbc:" and ends with ":", like in "jdbc:mysql:".

### Method `addKeyStore`

Create a new object type KeyStore

Function takes a dictionary with parameters, allowed keys are:
* `key_store_attributes` (`TextLine`)
  Attributes for key store, e.g. LIB=/usr/lunasa/lib/libCryptoKI.so;SLOT=1
* `key_store_name` (`TextLine`)
  Name of key store in EXAoperation
* `key_store_type` (`Choice`)
  Type of key store.
* `keylabel` (`TextLine`)
  Label to identify the key in the security module.

### Method `addLogService`

Create a new object type LogService

Function takes a dictionary with parameters, allowed keys are:
* `default_interval` (`TextLine`, optional)
  This time interval is shown per default.
* `description` (`TextLine`, optional)
  Some description of this logservice.
* `exaclusteros_services` (`List`, optional)
  EXAClusterOS services which should be visible at monitor, possible values: 'EXAoperation', 'DWAd', 'Lockd', 'Load', 'Storage'
* `exasolution_systems` (`List`, optional)
  Database systems which should be visible at monitor.
* `priority` (`Choice`)
  Specifies the lowest priority of messages that this logservice will show.

  Allowed values:
  * Error
  * Warning
  * Notice
  * Information

* `remote_syslog_protocol` (`Choice`, optional)
  Protocol to use to communicate with remote syslog server (TCP/UDP).

  Allowed values:
  * TCP
  * UDP

* `remote_syslog_server` (`TextLine`, optional)
  Log messages periodically to the specified remote syslog server via TCP.

### Method `addNode`

Create a new object type Node

Function takes a dictionary with parameters, allowed keys are:
* `boot_interface` (`Choice`)
  Interface to use for PXE boot.
* `console_redirect` (`Bool`, optional)
  Redirect kernel output to serial console.
* `cpu_scaling_governor` (`Choice`)
  Power scheme for Node CPU(s)
* `devices` (`List`, optional)
  The List of disk devices used on the node, use cluster's defaults if not given.
* `diskenc` (`Choice`, optional)
  Type of encryption to use on disks, use cluster's defaults if not given.
* `diskraid` (`Choice`, optional)
  The type of RAID to use on disks, use cluster's defaults if not given.
* `external_number` (`Int`, optional)
  The external node number, this number is added to network IP address.
* `force_fsck` (`Bool`, optional)
  Force filesystem check on next boot of this node.
* `force_no_fsck` (`Bool`, optional)
  Force no filesystem check on next boot of this node.
* `hugepages` (`Int`, optional)
  Amount of hugepages in GiB to allocate for database usage on this node. This is recommended for nodes with RAM > 512 GiB. See manual for details.
* `idstring` (`TextLine`, optional)
  String to identificate this node, not required.
* `ip_addr_ipmi` (`TextLine`, optional)
  Public Server Management Card IP address (only if group uses public addresses).
* `ipmi_group` (`Choice`, optional)
  Group that the IPMI card of this node belongs to (if any).
* `mac_addr_eth0` (`TextLine`)
  The MAC address of the first LAN interface.
* `mac_addr_eth1` (`TextLine`)
  The MAC address of the second LAN interface.
* `mac_addr_ipmi` (`TextLine`, optional)
  The MAC address of the Server Management interface.
* `node_unique_id` (`TextLine`, optional)
  Number to identify node for this cluster instance.
* `number` (`Int`)
  The node number in cluster, numbers 0-10 are reserved.
* `public_network_list` (`FixedDict`)
  Additional public network interfaces in node.
* `raidredundancy` (`Int`, optional)
  Number of copies of each datablock on RAID 10.
* `spool_disk` (`Choice`)
  Disk for spool data of loading processes and other.
* `to_install` (`Bool`, optional)
  Should this node to be installed next time when booted?
* `to_wipe` (`Bool`, optional)
  Wipe disks of node on next boot. This process can take a lot of time
* `use_4kib` (`Bool`, optional)
  Use 4 KiB alignment for hard disks to satisfy the 4 KiB sector size requirements.
* `vlan_list` (`FixedDict`)
  Additional private network interfaces in node.

### Method `addNodesFromXML`

Parses a xml_description to a XML with node definition and add new nodes,
When overwrite is set to True, it will overwrite the existing nodes with the same names.
Usage : cluster.addNodesFromXMl(xml_description, overwrite)

### Method `addPublicNetwork`

Create a new object type PublicNetwork

Function takes a dictionary with parameters, allowed keys are:
* `bonding_network` (`Choice`, optional)
  Public network to bond this network with.
* `mtu` (`Choice`)
  MTU (maximum transfer unit) size to use for this VLAN.
* `network_address` (`TextLine`, optional)
  IP address of the network (e.g. 192.168.16.0/24).
* `public_network_description` (`TextLine`)
  Description of this public network.

### Method `addRemoteVolume`

Create a new object type RemoteVolume

Function takes a dictionary with parameters, allowed keys are:
* `allowed_users` (`List`)
  List of users allowed to access volume.
* `labels` (`List`, optional)
  A List of labels to identify the volume.
* `options` (`TextLine`, optional)
  cleanvolume, noverifypeer, nocompression, forcessl, webdav, webhdfs, or s3. Separated by comma. See manual for details.
* `password` (`Password`, optional)
  Password for remote archive.
* `readonly_users` (`List`)
  List of users allowed to read volume.
* `url` (`TextLine`)
  Remote URL for archive volume, e.g. "ftp://192.168.2.1:12345" or "smb:////192.168.2.1/backupshare".
* `user` (`TextLine`, optional)
  Username for remote archive.

### Method `addRoute`

Create a new object type Route

Function takes a dictionary with parameters, allowed keys are:
* `route_destination` (`TextLine`)
  Destination for this route.
* `route_gateway` (`TextLine`)
  Gateway for this route.
* `route_type` (`Choice`)
  Type of route.

  Allowed values:
  * Network
  * Host

### Method `addScriptExtension`

Create a new object type ScriptExtension

Function takes a dictionary with parameters, allowed keys are:
* `description` (`TextLine`, optional)
  
* `http_proxy` (`TextLine`, optional)
  
* `https_proxy` (`TextLine`, optional)
  
* `script_name` (`TextLine`)
  Name of package, e.g. 3to2, ggplot2
* `script_type` (`Choice`)
  
* `url` (`TextLine`)
  URL of software repository, e.g. https://pypi.python.org/simple

### Method `addSrvMgmtGroup`

Create a new object type SrvMgmtGroup

Function takes a dictionary with parameters, allowed keys are:
* `ipmi_description` (`TextLine`)
  Name of this IPMI group.
* `ipmi_password` (`Password`, optional)
  Password of the IPMI card.
* `ipmi_password_multiline` (`Text`, optional)
  Multiline password of the IPMI card.
* `ipmi_type` (`Choice`)
  Type of the IPMI card.
* `ipmi_username` (`TextLine`)
  Username for the IPMI card.
* `public_ip_addresses` (`Bool`, optional)
  Location of IPMI cards (private/public network).

### Method `addUser`

Create an EXAoperation user.

Function takes a dictionary as a parameter.
Allowed keys ( required keys are marked with * ):
* user_login     - name of a user 
* password       - password (must be defined even when LDAP Authentification used) 
* user_title     - is shown in a status line
user_description - short description
ldapServer       - URL of ldap(s) service
ldapFullDN       - Full DN string to authenticate user on LDAP Service

### Method `addVLAN`

Create a new object type VLAN

Function takes a dictionary with parameters, allowed keys are:
* `bonding_network` (`Choice`, optional)
  Private network to bond this network with.
* `mtu` (`Choice`)
  MTU (maximum transfer unit) size to use for this VLAN.
* `vlan_description` (`TextLine`)
  Description of this private network.

### Method `applyRemoteSyslogSettings`

Apply remote syslog settings.

### Method `clusterDesc`

Return cluster description

### Method `deleteDatabaseCheck`

Check the posibility of delete database.

### Method `deleteLogs`

Delete logs/coredumps.

### Method `deleteNodeCheck`

Check the posibility of delete node.

### Method `deleteNodeDiskCheck`

Check the posibility of delete node disk.

### Method `deleteSubObject`

Delete the subobject, defined by it's name and all settings

### Method `deleteUserById`

Delete a user by given User ID

### Method `deleteUserByLogin`

Delete a user by a given login

### Method `deleteVolumeCheck`

Check the posibility of delete volume.

### Method `editMonitorThresholds`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `coredump_deletion_time` (`Int`)
  Number of days after which coredumps will be deleted.
* `disk_usage_error` (`Int`)
  Level upon which errors about disk space will be issued.
* `disk_usage_warning` (`Int`)
  Level upon which warnings about disk space will be issued.
* `load_error` (`Int`)
  Level upon which errors about load will be issued.
* `load_warning` (`Int`)
  Level upon which warnings about load will be issued.
* `sqllog_deletion_time` (`Int`)
  Number of days after which SQL logs will be deleted.
* `swap_error` (`Int`)
  Level upon which errors about swap space will be issued.
* `swap_warning` (`Int`)
  Level upon which warnings about swap space will be issued.

### Method `editNodeClusterDefaults`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `default_data_size` (`Int`)
  Default size of the Data disk in GiB.
* `default_devices` (`List`)
  A list of disk devices used for disks as default.
* `default_diskenc` (`Choice`)
  The default type of encryption to use for data disks.
* `default_diskraid` (`Choice`)
  The default type of software RAID to use on disks.
* `default_os_size` (`Int`)
  Default size of the OS disk in GiB.
* `default_raidredundancy` (`Int`)
  Default number of copies of each datablock on the RAID 10 arrays.
* `default_swap_size` (`Int`)
  Default size of the swap disk in GiB.

### Method `editNodeClusterLicense`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `license_comment` (`TextLine`)
  Description of this license.
* `license_companyname` (`TextLine`)
  Name of the company that owns license.
* `license_distributor` (`TextLine`)
  Distributor of the given license.
* `license_distributorid` (`TextLine`)
  ID of the license distributor.
* `license_expiration` (`TextLine`)
  License's expiration date in format yyyy-mm-dd
* `license_idnumber` (`TextLine`)
  Identification number of this license produced by EXASOL.
* `license_maxdbmemory` (`Int`)
  Allowed memory size for all databases used in this cluster.
* `license_serial_number` (`Text`)
  Serial number of this license.
* `license_validation_key` (`Text`)
  Key created by EXASOL for license validation.

### Method `editNodeClusterNetwork`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `cluster_desc` (`TextLine`, optional)
  Cluster name, that is shown to user.
* `default_gateway` (`TextLine`, optional)
  Gateway IP address to external network.
* `disable_broadcast` (`Bool`, optional)
  Disable usage of broadcasts, activate if network does not allow broadcasts.
* `dns_server1` (`TextLine`, optional)
  IP address of first DNS server.
* `dns_server2` (`TextLine`, optional)
  IP address of second DNS server.
* `external_network` (`TextLine`)
  IP address of the network (e.g. 10.12.1.0/24).
* `mtu_private` (`Choice`, optional)
  MTU (maximum transfer unit) size to use for private network.
* `mtu_public` (`Choice`, optional)
  MTU (maximum transfer unit) size to use for public network.
* `no_allow_http` (`Bool`, optional)
  Disable HTTP for EXAoperation and HTTP/FTP access to archive volumes. Option will take effect after restart of EXAoperation.
* `no_mac_check` (`Bool`, optional)
  Disable check of the MAC addresses on booting of nodes, it also disables the reordering of network interfaces.
* `ntp_key` (`TextLine`, optional)
  Key for NTP server (consists of Key ID and key [space separated])
* `ntp_server1` (`TextLine`, optional)
  IP address of the first NTP server.
* `ntp_server2` (`TextLine`, optional)
  IP address of the second NTP server.
* `ntp_server3` (`TextLine`, optional)
  IP address of the third NTP server.
* `protected_node_mem` (`Int`)
  Memory that must not be used by EXASolution.
* `search_domain` (`TextLine`, optional)
  Search domain to use with DNS servers.
* `time_zone` (`Choice`)
  The time zone of cluster.

### Method `editNodeClusterPasswords`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `backup_password` (`Password`)
  Password for the backup shares.
* `node_disk_password` (`Password`)
  Password of the disks. When changed, all nodes must be reintalled.
* `password_keystore` (`Choice`, optional)
  The key store to use for encryption of passwords.
* `vm_password` (`Password`)
  Password for the VM shares.

### Method `editNodeClusterVersions`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `exacluster_version` (`TextLine`)
  Installed EXAClusterOS version.
* `exasolution_versions` (`List`)
  List of Installed EXASolution versions.
* `plugins` (`List`)
  List of installed plugins.

### Method `editRemoteSyslogSettings`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `remote_syslog_ca_cert` (`Text`, optional)
  Text containing certificate of remote syslog server(s).
* `remote_syslog_encrypted` (`Bool`, optional)
  Defines whether or not to use TLS for transmission of syslog messages.

### Method `editUser`

Edit an EXAoperation user
Usage: cluster.editUser(user_login, user_data)

### Method `getAllArchiveVolumes`

Return a list of all archive volumes(local and remote).

Usage: cluster.getAllArchiveVolumes()

### Method `getAllDatabaseNames`

Return the list of databases' names.

### Method `getAllDatabases`

Return the list with all databases' ids

### Method `getAllJDBCDrivers`

Return a list of all installed JDBC drivers,
    
Usage: cluster.getAllJDBCDrivers()

### Method `getAllKeyStores`

Return list of all defined Password storages

### Method `getAllLogServices`

Return a list of all logservices.
    
Usage: cluster.getAllLogServices()

### Method `getAllPublicNetworks`

Return names of all public networks (sorted).

### Method `getAllRoutes`

Return a list of all routes.

Usage: cluster.getAllRoutes()

### Method `getAllScriptExtensions`

Return a list of all installed UDF Libraries

### Method `getAllSrvMgmtCardGroups`

Return a list of all Server Management Card Groups

Usage: cluster.getAllSrvMgmtCardGroups()

### Method `getAllUserLogins`

Return a list of all user logins

### Method `getAllUsers`

Return a list of all users

### Method `getAllUsersById`

Return a dictionary of all users by id

### Method `getAllUsersByLogin`

Return a dictionary of all users byl login

### Method `getAllVLANs`

Return names of all VLANs (sorted).

### Method `getAvailableUpdatesList`

Return a list of available updates, if the Update URL is defined.

### Method `getClusterNodesAsXMLBase64`

Return a base64-encoded string, that represent luster nodes in XML format

Usage: cluster.getClusterNodesAsXMLBase64()

### Method `getCoredumpDeletionTime`

Get deletion time of coredumps.

### Method `getCurrentLicenseServer`

Returns the license Server number.

### Method `getDefaultParameters`

Get list of current license default parameters.

### Method `getDomainName`

Returns the domain name.

### Method `getEXACOSVersion`

Return a string with current COS Version

### Method `getEXASolutionVersions`

Return a list with installed EXASolution Versions

### Method `getEXASuiteVersion`

Returns the version of the installed EXASuite package.

### Method `getEXAoperationNodes`

Get list of nodes, where EXAoperation could run

### Method `getInstallationHistory`

Return list of relevant installation details.

### Method `getInstalledJDBCDrivers`

Return list of ids of all installed JDBC Drivers

### Method `getKeyStoreByName`

Return a Password storage defined by name

### Method `getKeyStoreByObjName`

Return a Password storage defined by name

### Method `getLegalInfo`

Get list of al used 3rd-party licenses.

### Method `getLicenseFeatures`

Get list of current license features and expiration date.

### Method `getLicenseLimits`

Get list of current license limits.

### Method `getLicenseProperties`

Get current license properties

### Method `getLoginRole`

Return login role of specified user.

### Method `getMonitoringThresholdValues`

Get monitoring threshold values.

### Method `getNTPServiceState`

Get state of all NTP servers.

### Method `getObsoleteEXASuiteVersions`

Get all possible obsolete EXASuite versions.

### Method `getPlugins`

Return a list of installed plugins

### Method `getPossibleEXAoperationNodes`

Returns online nodes.

### Method `getProperties`

This object has no properties.

### Method `getPublicNetwork`

Return real public network name from descriptive name or None.

### Method `getPublicNetworkDescription`

Return real public network name from descriptive name or None.

### Method `getRolesForObject`

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

### Method `getServiceStates`

Get state of all necessary EXAClusterOS services.

### Method `getSoftware`

Get new software version from remote repository.

### Method `getSqlLogDeletionTime`

Get deletion time of sql logs.

### Method `getSrvMgmtGroup`

Return description of a Server Management group from descriptive name or None.

### Method `getSrvMgmtGroupDescription`

Return descriptive name of a Server Management card group.

### Method `getSupportData`

Return the information for EXASOL support.

### Method `getUpdateURL`

Get connection URL of update repository (including username/password).

### Method `getUploadPackageState`

Return a state of Upload Package's process

### Method `getUserById`

Return a user description by a given id

Usage cluster.getUserById(user_id)
Parameters:
  user_id - user's id (number as int or string)

### Method `getUserByName`

Return a user description by a given login

Usage: cluster.getUserByName(user_name)
Parameters:
  user_name - user's login

### Method `getVLAN`

Return real VLAN name from descriptive name or None.

### Method `getVLANDescription`

Return descriptive name of a VLAN net.

### Method `grantRole`

Set a given role on cluster object to user.

Usage: cluster.grantRole(object_name, user_id, role_name)
Parameters:
  object_name - name of an object in the cluster
  user_id     - id of a user (can be retrieved from cluster.getAllUsers() )
  role_name   - one of [u'User', u'Supervisor', u'Administrator', u'Master']

### Method `havePlugins`

Return True if plugins are installed

### Method `licenseUpdate`

Check and update the license aggreenments.

Usage: cluster.licenseUpdate(license_data)
Parameters: license_data - license data as xml-formatted string

### Method `needEXAoperationRestart`

Return True if EXAoperation should be restarted

### Method `ntpServersConfigured`

Return true if any NTP server is configured.

### Method `numberOfAvailableNodes`

Return number of nodes a user can add or 1024*1024 (unlimited).

### Method `powerOffLicenseServer`

Restart license server.

### Method `reinitEXAoperationPriorities`

Set priority of EXAoperation nodes.

### Method `removeAllScripts`

Remove all installed UDF Libraries.

### Method `removeDatabase`

Remove an old database version.

Parameters:
  version - EXASolution version to be removed.
Raises UsageError if a database with a given version is configured in a cluster 
or if an error occured during a deletion.

### Method `removeObsoleteEXASuite`

Remove obsolete software to save space.

### Method `removePlugin`

Remove a plugin.

Parameters: 
  name - name of plugin to be deleted.
Raises UsageError if an eror occured.

### Method `restartEXAoperation`

Restart EXAoperation server.
    
Usage: cluster.restartEXAoperation(node).
Parameters: 
  -node - a node name to start EXAoperation on. If '', the EXaoperation will be restarted on a current node.

### Method `restartLicenseServer`

Restart license server.

### Method `saveBucketFSChanges`

Save changes of bucketfs properties to file.

### Method `setDefaultRole`

Unset all granted roles and set a default role for user.

Usage: cluster.setDefaultRole(object_name, user_id)
Parameters:
  object_name - name of an object in the cluster
  user_id     - id of a user (can be retrieved from cluster.getAllUsers() )

### Method `setDiskPassword`

Set a node disk password. 
    
Usage: cluster.setDiskPassword(new_node_disk_password)

### Method `setKeyStore`

Set a new new key store for cluster.
    
Usage: cluster.setKeyStore(key_store_name)
Parameters:  key_store_name - name of a key store as it defined in object's properties.

### Method `setPriorities`

Set EXAoperation node priorities.

### Method `synchronizeNTP`

Synchronize license server with NTP servers.

### Method `uploadSoftware`

Upload a new database version.

## Service `NodeClusterAfterAdd`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `getProperties`

This object has no properties.

## Service `NodeClusterKeyStore`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `editNodeClusterKeyStore`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `key_store_attributes` (`TextLine`)
  Attributes for key store, e.g. LIB=/usr/lunasa/lib/libCryptoKI.so;SLOT=1
* `key_store_name` (`TextLine`)
  Name of key store in EXAoperation
* `key_store_type` (`Choice`)
  Type of key store.
* `keylabel` (`TextLine`)
  Label to identify the key in the security module.

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `key_store_attributes`
  Attributes for key store, e.g. LIB=/usr/lunasa/lib/libCryptoKI.so;SLOT=1
* `key_store_name`
  Name of key store in EXAoperation
* `key_store_type`
  Type of key store.
* `keylabel`
  Label to identify the key in the security module.

### Method `getStatus`

Get status of key store.

### Method `lock`

Lock key.

### Method `unlock`

Unlock key.

## Service `NodeClusterPublicNetwork`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `editNodeClusterPublicNetwork`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `bonding_network` (`Choice`, optional)
  Public network to bond this network with.
* `mtu` (`Choice`)
  MTU (maximum transfer unit) size to use for this VLAN.
* `network_address` (`TextLine`, optional)
  IP address of the network (e.g. 192.168.16.0/24).
* `public_network_description` (`TextLine`)
  Description of this public network.

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `bonding_network`
  Public network to bond this network with.
* `mtu`
  MTU (maximum transfer unit) size to use for this VLAN.
* `network_address`
  IP address of the network (e.g. 192.168.16.0/24).
* `public_network_description`
  Description of this public network.

## Service `NodeClusterRoute`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `editNodeClusterRoute`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `route_destination` (`TextLine`)
  Destination for this route.
* `route_gateway` (`TextLine`)
  Gateway for this route.
* `route_type` (`Choice`)
  Type of route.

  Allowed values:
  * Network
  * Host

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `route_destination`
  Destination for this route.
* `route_gateway`
  Gateway for this route.
* `route_type`
  Type of route.

## Service `NodeClusterSrvMgmtGroup`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `editNodeClusterSrvMgmtGroup`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `ipmi_description` (`TextLine`)
  Name of this IPMI group.
* `ipmi_password` (`Password`, optional)
  Password of the IPMI card.
* `ipmi_password_multiline` (`Text`, optional)
  Multiline password of the IPMI card.
* `ipmi_type` (`Choice`)
  Type of the IPMI card.
* `ipmi_username` (`TextLine`)
  Username for the IPMI card.
* `public_ip_addresses` (`Bool`, optional)
  Location of IPMI cards (private/public network).

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `ipmi_description`
  Name of this IPMI group.
* `ipmi_password`
  Password of the IPMI card.
* `ipmi_password_multiline`
  Multiline password of the IPMI card.
* `ipmi_type`
  Type of the IPMI card.
* `ipmi_username`
  Username for the IPMI card.
* `public_ip_addresses`
  Location of IPMI cards (private/public network).

## Service `NodeClusterVLAN`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `editNodeClusterVLAN`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `bonding_network` (`Choice`, optional)
  Private network to bond this network with.
* `mtu` (`Choice`)
  MTU (maximum transfer unit) size to use for this VLAN.
* `vlan_description` (`TextLine`)
  Description of this private network.

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `bonding_network`
  Private network to bond this network with.
* `mtu`
  MTU (maximum transfer unit) size to use for this VLAN.
* `vlan_description`
  Description of this private network.

## Service `NodeDisk`

URL: `https://<user>:<pass>@<cluster_node>/cluster1/<node_name>/<object_name>/`

### Method `addDevice`

Append device with given name to the current disk of an active node.

### Method `diskIsExtendable`

Returns True if new devices could be added to this disk.

### Method `editNodeDisk`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `devices` (`List`, optional)
  The List of disk devices used on the node, use cluster's defaults if not given.
* `diskenc` (`Choice`, optional)
  Type of encryption to use on disks, use cluster's defaults if not given.
* `disklabel` (`TextLine`, optional)
  Label for disk.
* `diskraid` (`Choice`, optional)
  The type of RAID to use on disks, use cluster's defaults if not given.
* `disksize` (`Int`, optional)
  The size of this disk in GiB or maximum if not entered.
* `raidredundancy` (`Int`, optional)
  Number of copies of each datablock on RAID 10.

### Method `getProperties`

This object has no properties.

## Service `RemoteVolume`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `editRemoteVolume`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `allowed_users` (`List`)
  List of users allowed to access volume.
* `labels` (`List`, optional)
  A List of labels to identify the volume.
* `options` (`TextLine`, optional)
  cleanvolume, noverifypeer, nocompression, forcessl, webdav, webhdfs, or s3. Separated by comma. See manual for details.
* `password` (`Password`, optional)
  Password for remote archive.
* `readonly_users` (`List`)
  List of users allowed to read volume.
* `url` (`TextLine`)
  Remote URL for archive volume, e.g. "ftp://192.168.2.1:12345" or "smb:////192.168.2.1/backupshare".
* `user` (`TextLine`, optional)
  Username for remote archive.

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `allowed_users`
  List of users allowed to access volume.
* `labels`
  A List of labels to identify the volume.
* `options`
  cleanvolume, noverifypeer, nocompression, forcessl, webdav, webhdfs, or s3. Separated by comma. See manual for details.
* `password`
  Password for remote archive.
* `readonly_users`
  List of users allowed to read volume.
* `url`
  Remote URL for archive volume, e.g. "ftp://192.168.2.1:12345" or "smb:////192.168.2.1/backupshare".
* `user`
  Username for remote archive.

### Method `getVolumeId`

Return 'virtual' volume ID of remote archive volume.

### Method `state`

Return connectivity state of remote archive volume.

## Service `ScriptExtension`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `editEXAPScript`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `description` (`TextLine`, optional)
  
* `http_proxy` (`TextLine`, optional)
  
* `https_proxy` (`TextLine`, optional)
  
* `script_name` (`TextLine`)
  Name of package, e.g. 3to2, ggplot2
* `script_type` (`Choice`)
  
* `url` (`TextLine`)
  URL of software repository, e.g. https://pypi.python.org/simple

### Method `getInstallationLog`

Get installation log of script.

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `description`
  
* `http_proxy`
  
* `https_proxy`
  
* `script_name`
  Name of package, e.g. 3to2, ggplot2
* `script_type`
  
* `url`
  URL of software repository, e.g. https://pypi.python.org/simple

### Method `getStatus`

Get installation status of script.

### Method `installNow`

Install script now.

## Service `SetupCommand`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `cmd`
  Command to execute.

## Service `SetupNodeNumber`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `node_number`
  Node number of the EXAoperation node.

## Service `SetupValue`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `value`
  Value of parameter.

## Service `Storage`

URL: `https://<user>:<pass>@<cluster_node>/cluster1/storage/`

### Method `addStorageVolume`

Create a new object type StorageVolume

Function takes a dictionary with parameters, allowed keys are:
* `allowed_users` (`List`)
  List of users, who are allowed to access this volume.
* `block_size` (`Int`, optional)
  Size of volume blocks in volume in KiB.
* `hdd_type` (`Choice`)
  Disk to create volume on.
* `labels` (`List`, optional)
  List of labels to identify the volume.
* `masternodes` (`Int`)
  Number of master nodes for volume; must match to number of DB nodes in case of data volume.
* `nodes_list` (`List`)
  List of nodes to use as volume storage.
* `priority` (`Int`, optional)
  Priority of volume between 1 and 20, higher number means higher priority. Default value is 10.
* `readonly_users` (`List`, optional)
  List of users, who are allowed to read this volume.
* `redundancy` (`Int`)
  Number of redundancy segments per volume part.
* `size` (`Int`)
  Size of volume in GiB.
* `volume_type` (`Choice`)
  Type of data stored on this volume.

  Allowed values:
  * Data
  * Archive

### Method `checkNodeDiskInformation`

Return node list about nodes whose disks can be checked.

### Method `deleteMetadata`

Delete Storage metadata from all online nodes.

### Method `editStorage`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `vlan_list` (`List`)
  Network interfaces to use for storage. Leave empty to use the first network interface.

### Method `getArchiveFilesystems`

Return dictionary with permitted for a user remote and archive volumes.
The returned values are tupples (<OBJECT_TYPE>, <ID>, <PERMISSIONS>)

Usage: storage.getArchiveFileSystems()

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `vlan_list`
  Network interfaces to use for storage. Leave empty to use the first network interface.

### Method `getStorageInfo`

Returns information about storage.

### Method `getVolumeInfo`

Returns information about volume.
    
Usage: storage.getVolumeInfo(vid)
Parameters:
  vid - volume id as returned by getVolumeList().

### Method `getVolumeList`

Return a dictionary with description of volumes in EXAStorage.

Usage: storage.getVolumeList()

### Method `nodesInformation`

Returns information about nodes.

### Method `nodesListInformation`

Returns information about Storage nodes.

### Method `serviceHasAutoRestartFlag`

Return True if auto-restart flag is set for Storage service.

### Method `serviceIsOnline`

Return True if the storage service is online.

### Method `setAutoRestartFlag`

Set auto-restart flag for Storage service.

### Method `storageHasQuorum`

Return a boolean, showing if storage service has quorum.

### Method `volumeRemove`

Remove volume

## Service `StorageNode`

URL: `https://<user>:<pass>@<cluster_node>/cluster1/storage/<object_name>/`

### Method `addUnusedDevices`

Add all disks, which are not added before.

Usage: storage_node.addUnusedDevices(devices)
Parameters: list of devices to add. If empty list ([]), all devives will be added.
Return a list of dictionaries with added devices Keys are:
  name
  type
  disk.

### Method `changeable`

Return whether node could contain Storage disks.

### Method `clearDeviceErrors`

Clear device errors counter.

### Method `disableBgRecovery`

Disable background recovery.

### Method `disableDevices`

Disable list of devices.

### Method `enableBgRecovery`

Enable background recovery.

### Method `enableDevices`

Enable list of devices.

### Method `enlargeDevices`

Enlarge list of devices.

### Method `forceBgRecoveryLimitCalibration`

Force background recalibration.

### Method `getAllDevices`

Return a list of disks on a node.

Usage: storage_node.getAllDevices()

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `auto_bg_rec_limit`
  Automatic background recovery limit in MiB.
* `bg_rec_limit`
  Background recovery limit in MiB.
* `bg_recovery_enabled`
  Status of node background recovery
* `disk_free_space`
  Space not used by volumes in GiB on given disk.
* `disk_space`
  Overall disk space in GiB on this node.
* `disk_sum_space`
  Size of disk in GiB.
* `free_space`
  Space not used by volumes in GiB on this node.
* `link_speed`
  Background recovery limit in MiB.
* `nid`
  EXAClusterOS logical node ID of the given node.
* `node_size`
  Space used by volumes in GiB on this node.
* `phys_nid`
  EXAClusterOS physical node ID of the given node.
* `state`
  State of the volume.

### Method `getUnusedDevices`

Return a list of devices which are not used in storage.
    
Usage: storage_node.getUnusedDevices(disk)

Parameters:
  disk - to get unused devices on a specific disk. If disk is an empty string,
         a corresponding disk will be found

### Method `nodeIsSuspended`

Return wheter node is suspended or not.

### Method `removeDevices`

Remove list of devices.

Usage: storage_node.removeDevices(devnames)
Parameters:
  devnames - list of disk names. The name of disk is returned by storage_node.getAllDevices, dictionary key 'name'.

### Method `restartNode`

Restart current node (only the storage service, not the node it self).

### Method `resumeNode`

Resume node.

### Method `setBgRecoveryLimit`

Set background recovery limit in MiB for node.

### Method `suspendNode`

Suspend node.

## Service `StorageNodeHDD`

URL: `https://<user>:<pass>@<cluster_node>/cluster1/storage/<storage_node_name>/<object_name>/`

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `crc_error`
  CRC error flag for given HDD.
* `hid`
  ID of given HDD.
* `io_error`
  IO error flag for given HDD.
* `name`
  Name of the given HDD.
* `num_sectors`
  Number of sectors on given HDD.
* `read_only`
  Read only flag for given HDD.
* `sector_size`
  Size of sector on given HDD.
* `state`
  HDD State.
* `type`
  Disk used for given HDD.

### Method `isEnlargeable`

Deliver information about enlargeability of device.

## Service `StorageVolume`

URL: `https://<user>:<pass>@<cluster_node>/cluster1/storage/<object_name>/`

### Method `checkPermissions`

Check permissions to access this volume.

### Method `editStorageVolume`

Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `add_master_nodes` (`Int`, optional)
  Number of master nodes that should be added.
* `add_nodes_list` (`List`, optional)
  List of nodes that should be added to volume.
* `allowed_users` (`List`)
  List of users, who are allowed to access this volume.
* `labels` (`List`, optional)
  List of labels to identify the volume.
* `priority` (`Int`, optional)
  Priority of volume between 1 and 20, higher number means higher priority. Default value is 10.
* `readonly_users` (`List`, optional)
  List of users, who are allowed to read this volume.
* `redundancy` (`Int`)
  Number of redundancy segments per volume part.

### Method `formatFilesystem`

Format SDFS Filesystem.

### Method `getFilesList`

Return list of files in an archive node.
     
usage: storage_archive_volume.getFilesList()

### Method `getPermissions`

Get permissions to access this volume.

### Method `getProperties`

This object has no properties.

### Method `moveNodes`

Move nodes according to nodes map.

### Method `removeFile`

Remove file with given ID.

### Method `resizeVolume`

Add given amount of GiB's to volume size.

### Method `setFileExpiration`

Set file expiration time, 'exptime' argument is number of seconds since the Epoch.

### Method `setIoState`

Set IO state for Volume application or internal IO.

## Service `StorageVolumeAddSchema`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `block_size`
  Size of volume blocks in volume in KiB.
* `hdd_type`
  Disk to create volume on.
* `masternodes`
  Number of master nodes for volume; must match to number of DB nodes in case of data volume.
* `nodes_list`
  List of nodes to use as volume storage.
* `size`
  Size of volume in GiB.
* `volume_type`
  Type of data stored on this volume.

## Service `StorageVolumeNode`

URL: `https://<user>:<pass>@<cluster_node>/cluster1/storage/<storage_volume_name>/<object_name>/`

### Method `getAllSegments`

Return list of volume node segments.
    
Usage: storage_volume_node.getAllSegments()

### Method `getProperties`

This object has no properties.

### Method `getSegmentsDescriptions`

Return a list with descriptions of a segments

Usage: storage_volume_node.getSegmentsDescription()

### Method `moveNode`

Move node to destination node.

### Method `recoverNode`

Recreate this node from redundancy.

### Method `stopRecoverNode`

Stop node restore.

## Service `StorageVolumeNodeSegment`

URL: `https://<user>:<pass>@<cluster_node>/cluster1/storage/<storage_volume_name>/<storage_volume_node>/<object_name>/`

### Method `getPartitions`

### Method `getProperties`

Function returns a dictionary that describes an object. Keys are:
* `end_block`
  Block number, on which the segment ends in volume.
* `index`
  
* `partitions`
  List of Partitions.
* `remote_sid`
  SID of the remote segment, in case of slave segments.
* `segment_size`
  Size of this segment in KiB.
* `sid`
  ID of the segment.
* `snapshot_state`
  Snapshot done on volume node segment in percents.
* `start_block`
  Block number, on which the segment begins in volume.
* `state`
  State of the segment.
* `type`
  Type of the segment.

## Service `SupportDebugInfo`

URL: `https://<user>:<pass>@<license_server>/cluster1/<object_name>`

### Method `downloadDebugInfo`

Download debug information.

### Method `estimateDebugInfoSize`

Get estimated size of debug information.

### Method `getProperties`

This object has no properties.

### Method `storeDebugInfo`

Store debug information into archive volume.

