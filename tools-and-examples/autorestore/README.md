# autorestore - restore your last backup set automatically 

In this directory you will find two files:
* autorestore.cfg: example configuration file
* autorestore.py: automatic restore script

The configuraiton file looks like this:
```
[autorestore]
username = admin
password = admin
hostname = 10.0.0.10
foreign_database = dbname_of_backup
database = exa_db1
archive  = v0001
```

"username" and "password" are EXAoperation credentials with at least "Administrator" role, hostname is the hostname of the license server (FQDN can be used too instead of IPs), "database" is the name of the database instance which shall be used to restore your backup, archive is the archive volume ID of your archive which should be used to restore your backups. If the database name of your backup differs from the database you're going to restore your backup in, you have to set "foreign_database" to the name which is used in your backup sets. Otherwise you have to set it to the same value which is used in "database".

The scripts will find the latest backup set, shutdown the database instance and trigger the restore event. If somethings fails the script comes back with error messages and a return value of 1.
