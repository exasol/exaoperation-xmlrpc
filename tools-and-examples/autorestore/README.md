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
database = exa_db1
archive  = v0001
```

"username" and "password" are EXAoperation credentials with at least "Supervisor" role, hostname is the hostname of the license server (FQDN can be used too instead of IPs), database is the name of the database instance which shall be used to restore your backup, archive is the archive volume ID of your archive which should be used to restore your  backups.

The scripts will find the latest backup set, shutdown the database instance and trigger the restore event. If somethings fails the script comes back with error messages and a return value of 1.
