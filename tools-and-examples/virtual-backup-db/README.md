# virtual-backup-db - starts up virtual access restores from your latest backup set

This script is very similar to the "autorestore" script, but there are three differences:
1. Instead of "blocking" the "virtual access" mode is used to trigger the database restore
2. Virtual Access requires to remove the expiration date of the used backup set, so the date will be removed before triggering the restore process
3. After the restore process has been triggered, the expiration date will get set again to prevent having a lot of old backup sets

-> Keep in mind that expired backups may get deleted while they are used by a virtual access database instance

In this directory you will find the following files:
* virtual-backup-db.cfg: example configuration file
* virtual-backup-db.py: automatic restore script

The configuraiton file looks like this:
```
[virtualbackup]
username = admin
password = admin
hostname = 10.0.0.10
foreign_database = source_db
database = virtual_restore_db
archive  = v0001
```

"username" and "password" are EXAoperation credentials with at least "Administrator" role, hostname is the hostname of the license server (FQDN can be used too instead of IPs), "database" is the name of the database instance which shall be used to provide the virtual access database, archive is the archive volume ID of your archive which should be used to restore your backups, "foreign\_database" is the name of the database which is used to provide the backup sets.

The scripts will find the latest backup set, shutdown the database instance and trigger the restore event. If somethings fails the script comes back with error messages and a return value of 1.
