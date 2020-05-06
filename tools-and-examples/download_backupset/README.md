# download\_backupset - Download a backup set from an local archive volume

download\_backupset.py requires the following parameters:
```
    -l  <license server>        (EXAoperation mgmt. server IP address)
    -u  <user name>             (EXAoperation User that has read access to the storage volumes)
    -p  <password>              (EXAoperation User password)
    -s  <source database name>  (download backups from this database)
    -b  <backup path>           (local directory)
    -i  <backup id>             (optional, get backup set with id xxx instead of latest backup)
    -a  <archive volume vXXXX>  (optional, helps to resolve id conflicts on different volumes FORMAT: v00xx)
    -c  <connection string>     (optional, neccessary for additional public networks)
    -d                          (optional, resolve backup depencies and download all files)
    -o                          (optional, overwrite existing backup sets)
```


This script automatically tries to download the backup files from the nodes which hold the local data and starts as many download threads as nodes are involved to speed up the download process. "wget" is used in this script to download the backup set.

Example:
```
download_backupset.py -l 10.70.0.10 -u admin -p admin -s exa_b1 -b /home/backupuser/backupdir -a v0010 -i 23 -o -d
```
Download backup ID 23 from volume ID v0010 of exa_db1, resolve backup dependencies and overwrite existing files. Tested with Exasol version 6.2.x
