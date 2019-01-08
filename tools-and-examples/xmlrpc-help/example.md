# Exasol XML-RPC help
## cluster = XmlRpcCall('/')
### cluster.getDomainName()
```
Returns the domain name.
```


### cluster.getPossibleEXAoperationNodes()
```
Returns online nodes.
```


### cluster.haltLicenseServer()
```
Shutdown license server.
```


### cluster.getRolesForObject()
```
Return a list of users with grants.
    
Usage: `cluster.getRolesForObject(object_name, user_id)`
Parameters:
* `object_name`
  Name of an object in the cluster
* `user_id`
  Id of a user (can be retrieved from cluster.getAllUsers()) If
  user_id is an empty string, then will be returned the list of all
  granted roles for this object.

The return value is a list of dictionaries. The keys are:
* `user`
  User id (as returned by cluster.getAllUsers() or used in cluster.getUserById() )
* `role`
  The role given to a user
* `default`
  False, if the role is granted directly to this object.
  True, if the role is derived from its parent object.

```


### cluster.needEXAoperationRestart()
```
Return True if EXAoperation should be restarted
```


### cluster.showPluginFunctions()
```
Function returns a list of function in a specified plugin. 

DUPLICATE OF: `showPluginFunctions`
```


### cluster.editUser()
```
Edit an EXAoperation user.

Usage: `cluster.editUser(user_login, user_data)`

Parameters:
* `user_login`
  Login name of the user to edit.
* `user_data`
  A dictionary wih following keys: `user_login`, `password`, `user_title`, `ldapServer`, `ldapFullDN`

```


### cluster.getObsoleteEXASuiteVersions()
```
Get all possible obsolete EXASuite versions.
```


### cluster.setDiskPassword()
```
Set a node disk password. 
    
Usage: cluster.setDiskPassword(new_node_disk_password)
```


### cluster.getServiceStates()
```
Get state of all necessary EXAClusterOS services.
```


### cluster.getCoredumpDeletionTime()
```
Get deletion time of coredumps.
```


### cluster.deleteSubObject()
```
Delete the subobject, defined by it's name and all settings
```


### cluster.uploadSoftware()
```
Upload a new database version.
```


### cluster.addKeyStore()
```
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

```


### cluster.getUploadPackageState()
```
Return a state of Upload Package's process
```


### cluster.restartEXAoperation()
```
Restart EXAoperation server.
    
Usage: cluster.restartEXAoperation(node).
Parameters: 
  -node - a node name to start EXAoperation on. If '', the EXaoperation will be restarted on a current node.
```


### cluster.deleteLogs()
```
Delete logs/coredumps.

Usage: `object.deleteLogs(delete_coredumps, db_name_list, start_date, stop_date)`

Parameters:
* `delete_coredumps`
  If True, delete also the coredumps.
* `db_same_list`
  List of DBs, which logs should be deleted.
* `start_date`
  From which starting date the logs should be deleted.
* `stop_date`
  Up to which date, logs should be deleted.

```


### cluster.getSoftware()
```
Get new software version from remote repository.
```


### cluster.getEXAoperationNodes()
```
Get list of nodes, where EXAoperation could run
```


### cluster.getAllUsersByLogin()
```
Return a dictionary of all users byl login
```


### cluster.removeDatabase()
```
Remove an old database version.

Parameters:
  version - EXASolution version to be removed.
Raises UsageError if a database with a given version is configured in a cluster 
or if an error occured during a deletion.
```


### cluster.addRemoteVolume()
```
Create a new object type RemoteVolume

Function takes a dictionary with parameters, allowed keys are:
* `allowed_users` (`List`)
  List of users, who are allowed to access this volume, in XMLRPC a list of user IDs as returned by `getUserByName`.
* `labels` (`List`, optional)
  A List of labels to identify the volume.
* `options` (`TextLine`, optional)
  cleanvolume, noverifypeer, nocompression, forcessl, webdav, webhdfs, delegation_token, noearlytls or s3. Separated by comma. See manual for details.
* `password` (`Password`, optional)
  Password for remote archive.
* `readonly_users` (`List`)
  List of users, who are allowed to read this volume, in XMLRPC a list of user IDs, as returned by `getUserByName`.
* `url` (`TextLine`)
  Remote URL for archive volume, e.g. "ftp://192.168.2.1:12345" or "smb:////192.168.2.1/backupshare".
* `user` (`TextLine`, optional)
  Username for remote archive.
* `vid` (`Int`, optional, readonly)
  ID of remote volume

```


### cluster.addLogService()
```
Create a new object type LogService

Function takes a dictionary with parameters, allowed keys are:
* `default_interval` (`TextLine`, optional)
  This time interval is shown per default.
* `description` (`TextLine`, optional)
  Some description of this logservice.
* `exaclusteros_services` (`List`)
  EXAClusterOS services which should be visible at monitor, possible values: 'EXAoperation', 'DWAd', 'Lockd', 'Load', 'Storage', 'Authentication'
* `exasolution_systems` (`List`)
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

```


### cluster.getInstallationHistory()
```
Return list of relevant installation details.
```


### cluster.getAllLogServices()
```
Return a list of all logservices.
    
Usage: cluster.getAllLogServices()
```


### cluster.getEXAoperationMaster()
```
None
```


### cluster.getPlugins()
```
Return a list of installed plugins
```


### cluster.getAllJDBCDrivers()
```
Return a list of all installed JDBC drivers,
    
Usage: cluster.getAllJDBCDrivers()
    
```


### cluster.methodSignature()
```
Introspection method. Return a list of parameters for a given method.

Usage: `object.methodHelp(method_name)`

Note: this function is not really supported. For a list of parameters please use `methodHelp`

```


### cluster.removeObsoleteEXASuite()
```
Remove obsolete software to save space.
```


### cluster.saveBucketFSChanges()
```
Save changes of bucketfs properties to file.
```


### cluster.getLicenseLimits()
```
 Get list of current license limits. 
```


### cluster.getLicenseProperties()
```
Get current license properties
```


### cluster.editRemoteSyslogSettings()
```
Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `remote_syslog_ca_cert` (`Text`, optional)
  Text containing certificate of remote syslog server(s).
* `remote_syslog_encrypted` (`Bool`, optional)
  Defines whether or not to use TLS for transmission of syslog messages.

```


### cluster.restartLicenseServer()
```
Restart license server.
```


### cluster.submitFirewallConfiguration()
```
None
```


### cluster.getVLANDescription()
```
Return descriptive name of a VLAN net.
```


### cluster.methodHelp()
```
Introspection method. Return a help for a given method.

Usage: `object.methodHelp(method_name)`
```


### cluster.getAllUsersById()
```
Return a dictionary of all users by id
```


### cluster.grantRole()
```
Set a given role on cluster object to user.

Usage: cluster.grantRole(object_name, user_id, role_name)
Parameters:
  object_name - name of an object in the cluster
  user_id     - id of a user (can be retrieved from cluster.getAllUsers() )
  role_name   - one of [u'User', u'Supervisor', u'Administrator', u'Master']

```


### cluster.getSqlLogDeletionTime()
```
Get deletion time of sql logs.
```


### cluster.callPlugin()
```
Function calls a specified plugin. 

Parameters:
* `plugin`
  Plugin name, could be found through `showPluginList`.
* `node`
* `command`
* `extra`

DUPLICATE OF: `callPlugin`
    
```


### cluster.getAllUsers()
```
Return a list of all users
```


### cluster.editMonitorThresholds()
```
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
* `rawmem_warning` (`Int`)
  Level upon which warnings about RAW/MEM license limit will be issued.
* `sqllog_deletion_time` (`Int`)
  Number of days after which SQL logs will be deleted.
* `storage_usage_error` (`Int`)
  Level upon which errors about storage space will be issued.
* `storage_usage_warning` (`Int`)
  Level upon which warnings about storage space will be issued.
* `swap_error` (`Int`)
  Level upon which errors about swap space will be issued.
* `swap_warning` (`Int`)
  Level upon which warnings about swap space will be issued.

```


### cluster.getProperties()
```
Function returns a dictionary that describes an object. Keys are:
* `cluster_desc`
  Cluster name, that is shown to user.
* `coredump_deletion_time`
  Number of days after which coredumps will be deleted.
* `default_data_size`
  Default size of the Data disk in GiB.
* `default_devices`
  A list of disk devices used for disks as default.
* `default_diskenc`
  The default type of encryption to use for data disks.
* `default_diskraid`
  The default type of software RAID to use on disks.
* `default_gateway`
  Gateway IP address to external network.
* `default_os_size`
  Default size of the OS disk in GiB.
* `default_raidredundancy`
  Default number of copies of each datablock on the RAID 10 arrays, used only if RAID 10 is selected in "Default RAID" field.
* `default_swap_size`
  Default size of the swap disk in GiB.
* `disable_broadcast`
  Disable usage of broadcasts, activate if network does not allow broadcasts.
* `disable_earlytls`
  Disable Early TLS for EXAoperation Interfaces.
* `disk_usage_error`
  Level upon which errors about disk space will be issued.
* `disk_usage_warning`
  Level upon which warnings about disk space will be issued.
* `dns_server1`
  IP address of first DNS server.
* `dns_server2`
  IP address of second DNS server.
* `exacluster_version`
  Installed EXAClusterOS version.
* `exasolution_versions`
  List of Installed EXASolution versions.
* `external_network`
  IP address of the network (e.g. 10.12.1.0/24).
* `license_comment`
  Description of this license.
* `license_companyname`
  Name of the company that owns license.
* `license_distributor`
  Distributor of the given license.
* `license_distributorid`
  ID of the license distributor.
* `license_expiration`
  License's expiration date in format yyyy-mm-dd
* `license_idnumber`
  Identification number of this license produced by EXASOL.
* `license_maxdbmemory`
  Allowed memory size for all databases used in this cluster.
* `license_serial_number`
  Serial number of this license.
* `license_validation_key`
  Key created by EXASOL for license validation.
* `load_error`
  Level upon which errors about load will be issued.
* `load_warning`
  Level upon which warnings about load will be issued.
* `mtu_private`
  MTU (maximum transfer unit) size to use for private network.
* `mtu_public`
  MTU (maximum transfer unit) size to use for public network.
* `no_allow_backup_download`
  Disable access to archive volumes completely. Option will take effect after restart of EXAoperation.
* `no_allow_http`
  Disable HTTP for EXAoperation and HTTP/FTP access to archive volumes. Option will take effect after restart of EXAoperation.
* `no_mac_check`
  Disable check of the MAC addresses on booting of nodes, it also disables the reordering of network interfaces.
* `node_disk_password`
  Password of the disks. When changed, all nodes must be reintalled.
* `ntp_key`
  Key for NTP server (consists of Key ID and key [space separated])
* `ntp_server1`
  IP address of the first NTP server.
* `ntp_server2`
  IP address of the second NTP server.
* `ntp_server3`
  IP address of the third NTP server.
* `password_keystore`
  The key store to use for encryption of passwords.
* `plugins`
  List of installed plugins.
* `protected_node_mem`
  Memory that must not be used by EXASolution.
* `rawmem_warning`
  Level upon which warnings about RAW/MEM license limit will be issued.
* `remote_syslog_ca_cert`
  Text containing certificate of remote syslog server(s).
* `remote_syslog_encrypted`
  Defines whether or not to use TLS for transmission of syslog messages.
* `search_domain`
  Search domain to use with DNS servers.
* `software_update_password`
  Password for software update URL.
* `software_update_url`
  Remote URL for software updates.
* `software_update_user`
  Username for software update URL.
* `sqllog_deletion_time`
  Number of days after which SQL logs will be deleted.
* `storage_usage_error`
  Level upon which errors about storage space will be issued.
* `storage_usage_warning`
  Level upon which warnings about storage space will be issued.
* `swap_error`
  Level upon which errors about swap space will be issued.
* `swap_warning`
  Level upon which warnings about swap space will be issued.
* `time_zone`
  Time zone of cluster. Databases must be stopped and afterwards started to recognize a change of this setting.

```


### cluster.getSrvMgmtGroup()
```
Return description of a Server Management group from descriptive name or None.
```


### cluster.addDatabase()
```
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
* `krb_host` (`TextLine`, optional)
  Kerberos Host Name used for Kerberos authentication
* `krb_realm` (`TextLine`, optional)
  Kerberos Realm
* `krb_service` (`TextLine`, optional)
  Kerberos Service Name used for Kerberos authentication, e.g. exasol
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

```


### cluster.getAllUserLogins()
```
Return a list of all user logins
```


### cluster.getNodeList()
```
Return a list of defined nodes.
    
Usage: `cluster.getNodeList()`

```


### cluster.addSrvMgmtGroup()
```
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

```


### cluster.getPublicNetworkDescription()
```
Return public network descriptive name from real name or None.
```


### cluster.getAllRoutes()
```
Return a list of all routes.

Usage: cluster.getAllRoutes()
    
```


### cluster.getServiceState()
```
None
```


### cluster.getCurrentLicenseServer()
```
None
```


### cluster.getKeyStoreByName()
```
Return a Password storage defined by name.
```


### cluster.showPluginList()
```
Function returns a list of all installed plugins
```


### cluster.setKeyStore()
```
Set a new new key store for cluster.
    
Usage: cluster.setKeyStore(key_store_name)
Parameters:  key_store_name - name of a key store as it defined in object's properties.
```


### cluster.addPublicNetwork()
```
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

```


### cluster.addVLAN()
```
Create a new object type VLAN

Function takes a dictionary with parameters, allowed keys are:
* `bonding_network` (`Choice`, optional)
  Private network to bond this network with.
* `mtu` (`Choice`)
  MTU (maximum transfer unit) size to use for this VLAN.
* `vlan_description` (`TextLine`)
  Description of this private network.

```


### cluster.getInstalledJDBCDrivers()
```
Return list of ids of all installed JDBC Drivers
```


### cluster.getMonitoringThresholdValues()
```
Get monitoring threshold values.
```


### cluster.deleteUserByLogin()
```
Delete a user by a given login
```


### cluster.addRoute()
```
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


```


### cluster.addNodesFromXML()
```
Parses a xml_description to a XML with node definition and add new nodes,
When overwrite is set to True, it will overwrite the existing nodes with the same names.
Usage : cluster.addNodesFromXMl(xml_description, overwrite)
```


### cluster.getSrvMgmtGroupDescription()
```
Return descriptive name of a Server Management card group.
```


### cluster.addBucketFS()
```
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

```


### cluster.getAllSrvMgmtCardGroups()
```
Return a list of all Server Management Card Groups

Usage: cluster.getAllSrvMgmtCardGroups()
    
```


### cluster.getPath()
```
Return absolute and relative pathes to object in cluster
```


### cluster.getDatabaseList()
```
Return list of databases' names.

DUPLICATE OF: `getAllDatabaseNames`

```


### cluster.removePlugin()
```
Remove a plugin.

Parameters: 
  name - name of plugin to be deleted.
Raises UsageError if an eror occured.
```


### cluster.getUserByName()
```
Return a user description by a given login

Usage: cluster.getUserByName(user_name)
Parameters:
  user_name - user's login
```


### cluster.getEXACOSVersion()
```
Return a string with current COS Version
```


### cluster.getHardwareInformation()
```
Return nodes dump of DMI table in human-readable format.

More information in man page dmidecode(8).

Usage: `cluster.getHardwareInformation('n0011', 1)

Parameters:
* `node`
  Name of the node or the node number
* `infotype`
  Optional, default is 1, table number to dump

```


### cluster.getAllDatabaseNames()
```
Return the list of databases' names.
```


### cluster.licenseUpdate()
```
Check and update the license aggreenments.

Usage: cluster.licenseUpdate(license_data)
Parameters: license_data - license data as xml-formatted string
    
```


### cluster.shutdownNode()
```
None
```


### cluster.synchronizeNTP()
```
Synchronize license server with NTP servers.
```


### cluster.getKeyStoreByObjName()
```
Return a Password storage defined by key store object name
```


### cluster.addNode()
```
Create a new object type Node

Function takes a dictionary with parameters, allowed keys are:
* `boot_interface` (`Choice`, optional)
  Interface to use for PXE boot.
* `console_redirect` (`Bool`, optional)
  Redirect kernel output to serial console.
* `cpu_scaling_governor` (`Choice`, optional)
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
* `public_network_list` (`FixedDict`, optional)
  Additional public network interfaces in node.
* `raidredundancy` (`Int`, optional)
  Number of copies of each datablock on RAID 10, only used if RAID 10 is selected in "Disk RAID" field.
* `spool_disk` (`Choice`)
  Disk for spool data of loading processes and other.
* `to_install` (`Bool`, optional)
  Should this node to be installed next time when booted?
* `to_wipe` (`Bool`, optional)
  Wipe disks of node on next boot. This process can take a lot of time
* `use_4kib` (`Bool`, optional)
  Use 4 KiB alignment for hard disks to satisfy the 4 KiB sector size requirements.
* `vlan_list` (`FixedDict`, optional)
  Additional private network interfaces in node.

```


### cluster.getLicenseFeatures()
```
Get list of current license features and expiration date. 
```


### cluster.addJDBCDriver()
```
Create a new object type JDBCDriver

Function takes a dictionary with parameters, allowed keys are:
* `comment` (`TextLine`, optional)
  Description of the driver, not required.
* `disable_security_manager` (`Bool`, optional)
  This option may be required to allow unsupported JDBC drivers to be run. However, it is not recommended to use this option.
* `jdbc_main` (`TextLine`)
  Name of the main class.
* `jdbc_name` (`TextLine`)
  Name of the driver.
* `jdbc_prefix` (`TextLine`)
  Prefix of the JDBC name, must begin with "jdbc:" and ends with ":", like in "jdbc:mysql:".

```


### cluster.havePlugins()
```
Return True if plugins are installed
```


### cluster.getVLAN()
```
Return real VLAN name from descriptive name or None.
```


### cluster.listObjects()
```
Introspection methon. Return a list of all objects.

Usage: `object.listObjects()`

```


### cluster.clusterDesc()
```
Return cluster description
```


### cluster.getAllPublicNetworks()
```
Return names of all public networks (sorted).
```


### cluster.uploadTlsFiles()
```
Upload and update TLS files(cert & private key) 

Usage:  cluster.uploadTlsFiles(cert, private_key)
        To use the new cert/key you have to restart ExaOperation

Parameter: cert[string] - The new certificate encoded as PEM
Parameter: private_key[string] - The new private key encoded as PEM
    
```


### cluster.getAllDatabases()
```
Return the list with all databases' ids
```


### cluster.getPublicNetwork()
```
Return real public network name from descriptive name or None.
```


### cluster.getAvailableUpdatesList()
```
Return a list of available updates, if the Update URL is defined.
```


### cluster.getNodeState()
```
None
```


### cluster.getAllVLANs()
```
Return names of all VLANs (sorted).
```


### cluster.getLegalInfo()
```
Get list of al used 3rd-party licenses.
```


### cluster.getEXASuiteVersion()
```
None
```


### cluster.getUserById()
```
Return a user description by a given id

Usage cluster.getUserById(user_id)
Parameters:
  user_id - user's id (number as int or string)

```


### cluster.getUpdateURL()
```
Get connection URL of update repository (including username/password).
```


### cluster.setClusterTime()
```
Set cluster time to specified time.
    
Usage: cluster.setClusterTime('2017-01-01 00:00:00')
```


### cluster.getListValues()
```
Return various list values depending on a type of object.

Usage: `object.getListValues(list)`

Parameters:
* `list`
  Name of a list, possible values are:
  * `Users`
  * `TimeZones`
  * `Days`
  * `Databases`
  * `DataDisks`
  * `StorageDisks`
  * `StorageVolumeNodes`
  * `ScalingGovernor`
  * `VLAN`
  * `PublicNetwork`
  * `SrvMgmtGroup`
  * `KeyStore`
  * `BootInterface`
  * `DatabaseNetworkInterfaces`
  * `EXASolutionVersions`
  * `VMBootDevice`
  * `Nodes`
  * `NodesReserve`
  * `NodesRemoveReserve`
  * `NodesDeactivate`
  * `NodesReactivate`
  * `BackupManager`
  * `BackupSystems`
  * `Disks`
  * `Volumes`
  * `DiskTypes`
  * `RaidTypes`
  * `SrvMgmtTypes`
  * `Mtu`
  * `KeyStoreTypes`
  * `EncrTypes`

```


### cluster.activateNodes()
```
Set nodes from a given list node_names to active state.
Usage:
nodes_list = [u'n0110', u'n0108']
cluster.activateNodes(nodes_list)
```


### cluster.getClusterNodesAsXMLBase64()
```
Return a base64-encoded string, that represent luster nodes in XML format

Usage: cluster.getClusterNodesAsXMLBase64()
    
```


### cluster.numberOfAvailableNodes()
```
Return number of nodes a user can add or 1024*1024 (unlimited).
```


### cluster.editNodeClusterNetwork()
```
Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `cluster_desc` (`TextLine`, optional)
  Cluster name, that is shown to user.
* `default_gateway` (`TextLine`, optional)
  Gateway IP address to external network.
* `disable_broadcast` (`Bool`, optional)
  Disable usage of broadcasts, activate if network does not allow broadcasts.
* `disable_earlytls` (`Bool`, optional)
  Disable Early TLS for EXAoperation Interfaces.
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
* `no_allow_backup_download` (`Bool`, optional)
  Disable access to archive volumes completely. Option will take effect after restart of EXAoperation.
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
  Time zone of cluster. Databases must be stopped and afterwards started to recognize a change of this setting.

```


### cluster.editNodeClusterDefaults()
```
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
  Default number of copies of each datablock on the RAID 10 arrays, used only if RAID 10 is selected in "Default RAID" field.
* `default_swap_size` (`Int`)
  Default size of the swap disk in GiB.

```


### cluster.getNTPServiceState()
```
Get state of all NTP servers.
```


### cluster.reinitEXAoperationPriorities()
```
Set priority of EXAoperation nodes.
```


### cluster.setPriorities()
```
Set EXAoperation node priorities.
```


### cluster.objectRepresentation()
```
Introspection method. Return the object representation.
```


### cluster.getEXASolutionVersions()
```
Return a list with installed EXASolution Versions
```


### cluster.setDefaultRole()
```
Unset all granted roles and set a default role for user.

Usage: cluster.setDefaultRole(object_name, user_id)
Parameters:
  object_name - name of an object in the cluster
  user_id     - id of a user (can be retrieved from cluster.getAllUsers() )

```


### cluster.listMethods()
```
Introspection method. Return a list of all methods.
    
Usage: `object.listMethods()`

```


### cluster.getLoginRole()
```
Return login role of specified user.
```


### cluster.addUser()
```
Create an EXAoperation user.

Function takes a dictionary as a parameter.
Allowed keys ( required keys are marked with * ):
* user_login     - name of a user 
* password       - password (must be defined even when LDAP Authentification used) 
* user_title     - is shown in a status line
user_description - short description
ldapServer       - URL of ldap(s) service
ldapFullDN       - Full DN string to authenticate user on LDAP Service
```


### cluster.startupNode()
```
Send boot signal to node over Server Manageent card.

Usage: `cluster.startupNode(nodename)`

```


### cluster.deleteUserById()
```
Delete a user by given User ID
```


### cluster.getFirewallConfiguration()
```
Returns content of /etc/fw.conf.

Usage: `cluster.getFirewallConfiguration('n0011')`

```


### cluster.getAllKeyStores()
```
Return list of all defined Password storages
```


### cluster.getAllArchiveVolumes()
```
Return a list of all archive volumes(local and remote).

Usage: cluster.getAllArchiveVolumes()
    
```


## storage = XmlRpcCall('/storage')
### storage.stopEXAStorage()
```
Stop EXAStorage service.

Tries to stop EXAStorage. Raises UsageError in case of error.

Usage: `storage.stopEXAStorage()`

```


### storage.getListValues()
```
Return various list values depending on a type of object.

Usage: `object.getListValues(list)`

Parameters:
* `list`
  Name of a list, possible values are:
  * `Users`
  * `TimeZones`
  * `Days`
  * `Databases`
  * `DataDisks`
  * `StorageDisks`
  * `StorageVolumeNodes`
  * `ScalingGovernor`
  * `VLAN`
  * `PublicNetwork`
  * `SrvMgmtGroup`
  * `KeyStore`
  * `BootInterface`
  * `DatabaseNetworkInterfaces`
  * `EXASolutionVersions`
  * `VMBootDevice`
  * `Nodes`
  * `NodesReserve`
  * `NodesRemoveReserve`
  * `NodesDeactivate`
  * `NodesReactivate`
  * `BackupManager`
  * `BackupSystems`
  * `Disks`
  * `Volumes`
  * `DiskTypes`
  * `RaidTypes`
  * `SrvMgmtTypes`
  * `Mtu`
  * `KeyStoreTypes`
  * `EncrTypes`

```


### storage.editStorage()
```
Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `vlan_list` (`List`)
  Network interfaces to use for storage. Leave empty to use the first network interface.

```


### storage.checkNodeDiskInformation()
```
Return node list about nodes whose disks can be checked.
```


### storage.deleteMetadata()
```
Delete Storage metadata from all online nodes.
```


### storage.volumeRemove()
```
Remove volume.

Usage: `storage.volumeRemove(vname)`
Parameters:
* `vname`
  Name of the as returned by `getVolumeList()`.
  Or volume object name returned by `getVolumeInfo(volume_id)`

```


### storage.methodHelp()
```
Introspection method. Return a help for a given method.

Usage: `object.methodHelp(method_name)`
```


### storage.getStorageInfo()
```
Returns information about storage.
```


### storage.getPath()
```
Return absolute and relative pathes to object in cluster
```


### storage.getVolumeList()
```
Return a dictionary with description of volumes in EXAStorage.

Usage: `storage.getVolumeList()`

```


### storage.serviceHasAutoRestartFlag()
```
Return True if auto-restart flag is set for Storage service.
```


### storage.addStorageVolume()
```
Create a new object type StorageVolume

Function takes a dictionary with parameters, allowed keys are:
* `allowed_users` (`List`)
  List of users, who are allowed to access this volume, in XMLRPC a list of user IDs as returned by `getUserByName`.
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
  List of users, who are allowed to read this volume, in XMLRPC a list of user IDs, as returned by `getUserByName`.
* `redundancy` (`Int`)
  Number of redundancy segments per volume part.
* `size` (`Int`)
  Size of volume in GiB.
* `volume_type` (`Choice`)
  Type of data stored on this volume.

  Allowed values:
  * Data
  * Archive


```


### storage.objectRepresentation()
```
Introspection method. Return the object representation.
```


### storage.getArchiveFilesystems()
```
Return dictionary with permitted for a user remote and archive volumes.
The returned values are tupples (<OBJECT_TYPE>, <ID>, <PERMISSIONS>)

Usage: `storage.getArchiveFileSystems()`

```


### storage.startEXAStorage()
```
Start EXAStorage service.

Tries to start EXAStorage. Raises UsageError in case of error.

Usage: `storage.startEXAStorage(ignored_nodes)`
Parameters:
* `ignored_nodes`
  List of nodes, where EXAStorage will not be started, or an empty list.

```


### storage.getVolumeInfo()
```
Returns information about volume.
    
Usage: `storage.getVolumeInfo(vid or remote volume object name)`
Parameters:
* `vid`
  Volume id as returned by `getVolumeList()`.
* `remote volume object name`
  Remote volume object name as returnedbvy `cluster.listObjects()`, for example 'remote1'

```


### storage.listMethods()
```
Introspection method. Return a list of all methods.
    
Usage: `object.listMethods()`

```


### storage.listObjects()
```
Introspection methon. Return a list of all objects.

Usage: `object.listObjects()`

```


### storage.setAutoRestartFlag()
```
Set auto-restart flag for Storage service.
```


### storage.getProperties()
```
Function returns a dictionary that describes an object. Keys are:
* `vlan_list`
  Network interfaces to use for storage. Leave empty to use the first network interface.

```


### storage.nodesListInformation()
```
Returns information about Storage nodes.
```


### storage.nodesInformation()
```
Returns information about nodes.
```


### storage.methodSignature()
```
Introspection method. Return a list of parameters for a given method.

Usage: `object.methodHelp(method_name)`

Note: this function is not really supported. For a list of parameters please use `methodHelp`

```


### storage.storageHasQuorum()
```
Return a boolean, showing if storage service has quorum.
```


### storage.serviceIsOnline()
```
Return True if the storage service is online.
```


## users = XmlRpcCall('/users')
### users.listMethods()
```
Introspection method. Return a list of all methods.
    
Usage: `object.listMethods()`

```


### users.listObjects()
```
Introspection methon. Return a list of all objects.

Usage: `object.listObjects()`

```


### users.methodHelp()
```
Introspection method. Return a help for a given method.

Usage: `object.methodHelp(method_name)`
```


### users.objectRepresentation()
```
Introspection method. Return the object representation.
```


### users.getPath()
```
Return absolute and relative pathes to object in cluster
```


### users.getListValues()
```
Return various list values depending on a type of object.

Usage: `object.getListValues(list)`

Parameters:
* `list`
  Name of a list, possible values are:
  * `Users`
  * `TimeZones`
  * `Days`
  * `Databases`
  * `DataDisks`
  * `StorageDisks`
  * `StorageVolumeNodes`
  * `ScalingGovernor`
  * `VLAN`
  * `PublicNetwork`
  * `SrvMgmtGroup`
  * `KeyStore`
  * `BootInterface`
  * `DatabaseNetworkInterfaces`
  * `EXASolutionVersions`
  * `VMBootDevice`
  * `Nodes`
  * `NodesReserve`
  * `NodesRemoveReserve`
  * `NodesDeactivate`
  * `NodesReactivate`
  * `BackupManager`
  * `BackupSystems`
  * `Disks`
  * `Volumes`
  * `DiskTypes`
  * `RaidTypes`
  * `SrvMgmtTypes`
  * `Mtu`
  * `KeyStoreTypes`
  * `EncrTypes`

```


### users.getProperties()
```
This object has no properties.
```


### users.methodSignature()
```
Introspection method. Return a list of parameters for a given method.

Usage: `object.methodHelp(method_name)`

Note: this function is not really supported. For a list of parameters please use `methodHelp`

```


## database = XmlRpcCall('/db_training2')
### database.backupInfo()
```
Return information for a backup.
```


### database.startDatabaseMaintenance()
```
Start database in maintenance mode, must exist and must not be running.
```


### database.shrinkDatabase()
```
Shrink a database. This operation can only be apply for running databases.

Usage: database.shrinkDatabase(target_size_in_gb)
Parameters:
  target_size_in_gb - target size for shrink operation.
    
```


### database.getBackupInfo()
```
Return a backup info as a list.

Parameters:
* `timestamp`   - could have three types of value:
  1. Backup's ID
  2. timestamp
  3. tuple (BackupID, VolumeID)

DUPLICATE OF: `backupInfo`

```


### database.existsKeyTab()
```
Return whether a keytab exists.
```


### database.startDatabase()
```
Start a database.

DUPLICATE OF: startDatabase().
Remark: was omited by generation
```


### database.deleteBackups()
```
Delete given backups.

Usage: `database.deleteBackups(backup_list)`
Parameters: 
* `backup_list`
  A list of backup IDs as returned by `getBackups()` in key `id`.

```


### database.setBackupSchedule()
```
Set a list of all scheduled backups.
    
Parameter:
  list of backup definitions
```


### database.restartDatabase()
```
Restart database which must be running.
```


### database.createDatabase()
```
Create a fresh database, must not exist jet.
```


### database.getDatabaseStatistics()
```
Return Base64-encoded database statistics data as ZIP compressed CSV files.

Parameters:
* `user`
  Database user with corresponding permissions
* `password`
  Database user password
* `start = ''`, `stop = ''`
  Start and stop date to get statistics. When not specified, the
  statistics for the last 30 days will be collected.

Almost DUPLICATE OF: `getStatistics`

```


### database.getDatabaseConnectionState()
```
Return a state in a string format either database connectable or not.
```


### database.runningDatabase()
```
Return whether the database is started.
```


### database.getNextSchedules()
```
Get scheduling for next period of time.
```


### database.stateDatabase()
```
Return human-readable state of database.
```


### database.abortBackup()
```
Abort running database backup.
```


### database.methodHelp()
```
Introspection method. Return a help for a given method.

Usage: `object.methodHelp(method_name)`
```


### database.abortShrink()
```
Abort shrink operation of database.
```


### database.getPath()
```
Return absolute and relative pathes to object in cluster
```


### database.getDatabaseOperation()
```
Returns a current database's operation.

DUPLICATE OF: `operationGetCurrent`

```


### database.startStorageBackup()
```
Start a backup process. 

Parameters:
* `volume`
  EXAStorage volume's (or remote volume's) ID.
* `level`
  Level of a backup to start, integer value starts from 0.
* `expire`
  Time interval, after that the backup will expire

DUPLICATE OF: `backupDatabase`

```


### database.backupDatabase()
```
Start backup to given storage volume with given level and expiration time.

Parameters:
* `volume`
  Name of volume where to write backup
* `level`
  Backup level
* `expire`
  Expire time for backup

```


### database.listObjects()
```
Introspection methon. Return a list of all objects.

Usage: `object.listObjects()`

```


### database.getProperties()
```
Function returns a dictionary that describes an object. Keys are:
* `clients_port_number`
  Port for client connections.
* `data_disk`
  Disk for runtime data (log files and data/tmp files for non-storage databases)
* `data_volume`
  Volume for EXASolution database data.
* `database_comment`
  User-defined comment for database (200 charachters max)
* `database_name`
  The name of current database.
* `database_version`
  Version of EXASolution executables.
* `enable_auditing`
  Enable auditing for database
* `extra_params`
  Extra parameters for startup of database.
* `krb_host`
  Kerberos Host Name used for Kerberos authentication
* `krb_realm`
  Kerberos Realm
* `krb_service`
  Kerberos Service Name used for Kerberos authentication, e.g. exasol
* `ldap_server`
  LDAP Server to use for remote database authentication, e.g. ldap[s]://192.168.16.10 . Multiple servers must be separated by commas.
* `memory_usage`
  Amount of database memory (in GiB).
* `nodes_list`
  List of active and reserve nodes for this database.
* `nodes_list_add_reserve`
  List of nodes, which should be added to the system as reserve nodes.
* `nodes_list_deactivate`
  List of nodes which should be deactivated for this system.
* `nodes_list_reactivate`
  List of nodes which should be reactivated for this system.
* `nodes_list_remove_reserve`
  List of nodes which should be removed from the System as reserve nodes.
* `nodes_number`
  Number of online nodes for this database.
* `vlan_list`
  Network interfaces to use for database. Leave empty to use all possible network interfaces.
* `volume_quota`
  Maximal size of volume in (GiB), the database tries to shrink it on start if required and possible.
* `volume_restore_delay`
  Move failed volume nodes to used reserve nodes automaticaly after given amount of time, or disable it with no value.

```


### database.removeKeyTab()
```
Remove an uploaded keytab file.
```


### database.uploadKeyTab()
```
Upload keytab file.
```


### database.deleteUnusableBackups()
```
Delete all unusable backups for current database.

Usage: `database.deleteUnusableBackups()`
* `use_all_databases`
  If True, delete unusable backups from all databases, default False.

```


### database.objectRepresentation()
```
Introspection method. Return the object representation.
```


### database.getBackups()
```
Return a list of available backups for this database.

Usage: `database.getBackups(show_all_databases = False, show_expired_backups = True)`
Parameters:
  `show_all_databases` - show backups not for only this database
  `show_expired_backups` - not exclude expired backups from list
    
```


### database.getBackupSchedule()
```
Return a list of scheduled backups
```


### database.getCurrentErrors()
```
Get current reasons for not starting a database.
```


### database.operationGetCurrent()
```
Return the current operation
```


### database.forceShutdownDatabase()
```
Force shutdown of database, must be running.
```


### database.restoreDatabase()
```
Start restore from given backup ID and restore type.

Usage: `database.restoreDatabase(backup_id, restore_type)`
Parameters: 
* `backup_name`
  Could be obtained by getBackups(), field 'id'. Must have three valus separated by space.
* `restore_type`
  Type of restore. Must be one of following - {'blocking'|'nonblocking'|'virtual access'} 

```


### database.changeBackupExpiration()
```
Change expiration time of a backup.

Usage: `database.changeBackupExpiration(volume, backup_files, expire_time)`
Parameters:
* `volume`
  Volume ID.
* `backup_files`
  Prefix of the backup files, like `exa_db1/id_1/level_0`.
* `expire_time`
  Timestamp in seconds since the Epoch on which the backup should expire.

```


### database.getNodeState()
```
Return the state of a node: online, offline or failed.
```


### database.shutdownDatabase()
```
Shutdown the database, must be running.
```


### database.editDatabase()
```
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
* `krb_host` (`TextLine`, optional)
  Kerberos Host Name used for Kerberos authentication
* `krb_realm` (`TextLine`, optional)
  Kerberos Realm
* `krb_service` (`TextLine`, optional)
  Kerberos Service Name used for Kerberos authentication, e.g. exasol
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

```


### database.listMethods()
```
Introspection method. Return a list of all methods.
    
Usage: `object.listMethods()`

```


### database.getPddProgress()
```
Get information about current PDD processes (Backup/Restore). 
```


### database.maintenanceDatabase()
```
Get maintenance state of database.
```


### database.getBackupList()
```
Return a list of backups for the current system

This function is deprecated, please use: `getBackups`

```


### database.getCurrentDatabaseSize()
```
Get current database size.
```


### database.getDatabaseNodes()
```
Return a dictionary with 3 keys: 'active', 'failed' and 'reserve'. ,
```


### database.getDatabaseVersion()
```
Return current database version.
```


### database.getDatabaseInfo()
```
Return a dictionary with main database parameters.

If a database uses EXAStorage, it returns a volume's preperties too.
```


### database.enlargeDatabase()
```
Enlarge an existing database. Precondition: the database should be stopped.
Warning - the changes made by this function could not be undone. Function increase
the number of active nodes of the database.

Usage: database.enlargeDatabase(count_of added_active_nodes)
Parameters:
  count_of_added_active_nodes - a number of nodes, that will be ADDED to an existing number.
    
```


### database.existDatabase()
```
Return whether the database exists or not.
```


### database.getListValues()
```
Return various list values depending on a type of object.

Usage: `object.getListValues(list)`

Parameters:
* `list`
  Name of a list, possible values are:
  * `Users`
  * `TimeZones`
  * `Days`
  * `Databases`
  * `DataDisks`
  * `StorageDisks`
  * `StorageVolumeNodes`
  * `ScalingGovernor`
  * `VLAN`
  * `PublicNetwork`
  * `SrvMgmtGroup`
  * `KeyStore`
  * `BootInterface`
  * `DatabaseNetworkInterfaces`
  * `EXASolutionVersions`
  * `VMBootDevice`
  * `Nodes`
  * `NodesReserve`
  * `NodesRemoveReserve`
  * `NodesDeactivate`
  * `NodesReactivate`
  * `BackupManager`
  * `BackupSystems`
  * `Disks`
  * `Volumes`
  * `DiskTypes`
  * `RaidTypes`
  * `SrvMgmtTypes`
  * `Mtu`
  * `KeyStoreTypes`
  * `EncrTypes`

```


### database.getDatabaseState()
```
Return state of a database.

DUPLICATE OF: stateDatabase()
```


### database.stopDatabase()
```
Stop a database.

DUPLICATE OF: shutdownDatabase()
```


### database.getDatabaseConnectionString()
```
Return a fully qualified connection string.
```


### database.methodSignature()
```
Introspection method. Return a list of parameters for a given method.

Usage: `object.methodHelp(method_name)`

Note: this function is not really supported. For a list of parameters please use `methodHelp`

```


## logservice = XmlRpcCall('/')
### logservice.editLogService()
```
Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `default_interval` (`TextLine`, optional)
  This time interval is shown per default.
* `description` (`TextLine`, optional)
  Some description of this logservice.
* `exaclusteros_services` (`List`)
  EXAClusterOS services which should be visible at monitor, possible values: 'EXAoperation', 'DWAd', 'Lockd', 'Load', 'Storage', 'Authentication'
* `exasolution_systems` (`List`)
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

```


### logservice.listMethods()
```
Introspection method. Return a list of all methods.
    
Usage: `object.listMethods()`

```


### logservice.listObjects()
```
Introspection methon. Return a list of all objects.

Usage: `object.listObjects()`

```


### logservice.methodHelp()
```
Introspection method. Return a help for a given method.

Usage: `object.methodHelp(method_name)`
```


### logservice.objectRepresentation()
```
Introspection method. Return the object representation.
```


### logservice.getPath()
```
Return absolute and relative pathes to object in cluster
```


### logservice.getListValues()
```
Return various list values depending on a type of object.

Usage: `object.getListValues(list)`

Parameters:
* `list`
  Name of a list, possible values are:
  * `Users`
  * `TimeZones`
  * `Days`
  * `Databases`
  * `DataDisks`
  * `StorageDisks`
  * `StorageVolumeNodes`
  * `ScalingGovernor`
  * `VLAN`
  * `PublicNetwork`
  * `SrvMgmtGroup`
  * `KeyStore`
  * `BootInterface`
  * `DatabaseNetworkInterfaces`
  * `EXASolutionVersions`
  * `VMBootDevice`
  * `Nodes`
  * `NodesReserve`
  * `NodesRemoveReserve`
  * `NodesDeactivate`
  * `NodesReactivate`
  * `BackupManager`
  * `BackupSystems`
  * `Disks`
  * `Volumes`
  * `DiskTypes`
  * `RaidTypes`
  * `SrvMgmtTypes`
  * `Mtu`
  * `KeyStoreTypes`
  * `EncrTypes`

```


### logservice.logEntries()
```
None
```


### logservice.getProperties()
```
Function returns a dictionary that describes an object. Keys are:
* `default_interval`
  This time interval is shown per default.
* `description`
  Some description of this logservice.
* `exaclusteros_services`
  EXAClusterOS services which should be visible at monitor, possible values: 'EXAoperation', 'DWAd', 'Lockd', 'Load', 'Storage', 'Authentication'
* `exasolution_systems`
  Database systems which should be visible at monitor.
* `priority`
  Specifies the lowest priority of messages that this logservice will show.
* `remote_syslog_protocol`
  Protocol to use to communicate with remote syslog server (TCP/UDP).
* `remote_syslog_server`
  Log messages periodically to the specified remote syslog server via TCP.

```


### logservice.logEntriesTagged()
```
None
```


### logservice.methodSignature()
```
Introspection method. Return a list of parameters for a given method.

Usage: `object.methodHelp(method_name)`

Note: this function is not really supported. For a list of parameters please use `methodHelp`

```


## node = XmlRpcCall('/n0011')
### node.setForceFSCKMode()
```
Set the node to Force fsck state.

Usage: node.setFSCKMode()
```


### node.getBondingActiveSlaves()
```
Return active slaves for bondings
```


### node.poweroffNode()
```
Power off the node immediatly.
```


### node.getListValues()
```
Return various list values depending on a type of object.

Usage: `object.getListValues(list)`

Parameters:
* `list`
  Name of a list, possible values are:
  * `Users`
  * `TimeZones`
  * `Days`
  * `Databases`
  * `DataDisks`
  * `StorageDisks`
  * `StorageVolumeNodes`
  * `ScalingGovernor`
  * `VLAN`
  * `PublicNetwork`
  * `SrvMgmtGroup`
  * `KeyStore`
  * `BootInterface`
  * `DatabaseNetworkInterfaces`
  * `EXASolutionVersions`
  * `VMBootDevice`
  * `Nodes`
  * `NodesReserve`
  * `NodesRemoveReserve`
  * `NodesDeactivate`
  * `NodesReactivate`
  * `BackupManager`
  * `BackupSystems`
  * `Disks`
  * `Volumes`
  * `DiskTypes`
  * `RaidTypes`
  * `SrvMgmtTypes`
  * `Mtu`
  * `KeyStoreTypes`
  * `EncrTypes`

```


### node.toggleIdLed()
```
Toggle the ID LED on the given node.
```


### node.getSrvMgmtSensorStatus()
```
Return a status of Server Management card's sensors. 

Usage: `cluster.getSrvMgmtSensorStatus()`
```


### node.getDeviceInfo()
```
Return information about devices.
```


### node.nodeRunning()
```
Return whether the node is running.
```


### node.setActiveMode()
```
Set the node to Active state. The node in active state is available to all cluster services.

Usage: node.setActiveMode()
```


### node.methodHelp()
```
Introspection method. Return a help for a given method.

Usage: `object.methodHelp(method_name)`
```


### node.deleteSubObject()
```
Delete the subobject, defined by it's name and all settings
```


### node.getDiskStates()
```
None
```


### node.getPath()
```
Return absolute and relative pathes to object in cluster
```


### node.setForceNoFSCKMode()
```
Set the node to Force No fsck state.

Usage: node.setNoFSCKMode()
```


### node.getDiskInfo()
```
Return info about disk.

Usage: `storage.getDiskInfo(diskname)`
Parameters:
* `diskname`
  Name of the disk to show, like `d00_os`

```


### node.addNodeDisk()
```
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
  Number of copies of each datablock on RAID 10, only used if RAID 10 is selected in "Disk RAID" field.

```


### node.copyNode()
```
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
    
```


### node.shutdownNode()
```
Shutdown the node.
```


### node.addStorageDisk()
```
Add aditional storage disk do an active node.

Usage: node.addStorageDisk(devices, enc, label, size, number)
Parameters: devices   - List of devices to use
            label     - Label of the new disk
            enc       - Encryption to use (none, aes128, aes256)
            number    - Use this disk number, if None or not given, generate new number

Only storage disks and disks without redundancy can be added to an
active node. Devices must not be used by any other disk.
```


### node.getIPMISensorStatus()
```
Return a status of IPMI sensors. 

Function is deprecated, please use getSrvMgmtSensorStatus() instead.

Usage: `cluster.getIPMISensorStatus()`
```


### node.editNode()
```
Edits object.

Function take a dictionary with parameters and return a list of fields, that was modified, allowed keys are:
* `boot_interface` (`Choice`, optional)
  Interface to use for PXE boot.
* `console_redirect` (`Bool`, optional)
  Redirect kernel output to serial console.
* `cpu_scaling_governor` (`Choice`, optional)
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
* `public_network_list` (`FixedDict`, optional)
  Additional public network interfaces in node.
* `raidredundancy` (`Int`, optional)
  Number of copies of each datablock on RAID 10, only used if RAID 10 is selected in "Disk RAID" field.
* `spool_disk` (`Choice`)
  Disk for spool data of loading processes and other.
* `to_install` (`Bool`, optional)
  Should this node to be installed next time when booted?
* `to_wipe` (`Bool`, optional)
  Wipe disks of node on next boot. This process can take a lot of time
* `use_4kib` (`Bool`, optional)
  Use 4 KiB alignment for hard disks to satisfy the 4 KiB sector size requirements.
* `vlan_list` (`FixedDict`, optional)
  Additional private network interfaces in node.

```


### node.rebootNode()
```
Reboot the node.
```


### node.objectRepresentation()
```
Introspection method. Return the object representation.
```


### node.operationGetCurrent()
```
Return the current operation
```


### node.stopClusterServices()
```
Stop Core daemon on this node.
```


### node.deleteDisks()
```
Remove disk with given list of names.
```


### node.startClusterServices()
```
Start Core daemon on this node.
```


### node.fixChecksums()
```
Fix/delete checksums of disks.
```


### node.listMethods()
```
Introspection method. Return a list of all methods.
    
Usage: `object.listMethods()`

```


### node.applyDefaultDiskLayout()
```
Apply default disk layout to this node.
```


### node.getNodeInfo()
```
Return node information.
```


### node.startupNode()
```
Power on and startup the node.
```


### node.listObjects()
```
Introspection methon. Return a list of all objects.

Usage: `object.listObjects()`

```


### node.resetNode()
```
Reset the node immediatly.
```


### node.getAllDisks()
```
Return list of disk names.
```


### node.getNodeState()
```
None
```


### node.getProperties()
```
Function returns a dictionary that describes an object. Keys are:
* `boot_interface`
  Interface to use for PXE boot.
* `console_redirect`
  Redirect kernel output to serial console.
* `cpu_scaling_governor`
  Power scheme for Node CPU(s)
* `devices`
  The List of disk devices used on the node, use cluster's defaults if not given.
* `diskenc`
  Type of encryption to use on disks, use cluster's defaults if not given.
* `diskraid`
  The type of RAID to use on disks, use cluster's defaults if not given.
* `external_number`
  The external node number, this number is added to network IP address.
* `force_fsck`
  Force filesystem check on next boot of this node.
* `force_no_fsck`
  Force no filesystem check on next boot of this node.
* `hugepages`
  Amount of hugepages in GiB to allocate for database usage on this node. This is recommended for nodes with RAM > 512 GiB. See manual for details.
* `idstring`
  String to identificate this node, not required.
* `ip_addr_ipmi`
  Public Server Management Card IP address (only if group uses public addresses).
* `ipmi_group`
  Group that the IPMI card of this node belongs to (if any).
* `mac_addr_eth0`
  The MAC address of the first LAN interface.
* `mac_addr_eth1`
  The MAC address of the second LAN interface.
* `mac_addr_ipmi`
  The MAC address of the Server Management interface.
* `node_unique_id`
  Number to identify node for this cluster instance.
* `number`
  The node number in cluster, numbers 0-10 are reserved.
* `public_network_list`
  Additional public network interfaces in node.
* `raidredundancy`
  Number of copies of each datablock on RAID 10, only used if RAID 10 is selected in "Disk RAID" field.
* `spool_disk`
  Disk for spool data of loading processes and other.
* `to_install`
  Should this node to be installed next time when booted?
* `to_wipe`
  Wipe disks of node on next boot. This process can take a lot of time
* `use_4kib`
  Use 4 KiB alignment for hard disks to satisfy the 4 KiB sector size requirements.
* `vlan_list`
  Additional private network interfaces in node.

```


### node.setWipeMode()
```
Set the node to To Wipe state. After boot the all data will be erased.
    
Usage: node.setWipeMode()
```


### node.setInstallMode()
```
Set the node to Install state. After next reboot the node will be installed.

Usage: node.setInstallMode()
```


### node.methodSignature()
```
Introspection method. Return a list of parameters for a given method.

Usage: `object.methodHelp(method_name)`

Note: this function is not really supported. For a list of parameters please use `methodHelp`

```


