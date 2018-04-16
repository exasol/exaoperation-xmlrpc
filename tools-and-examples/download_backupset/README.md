# download\_backupset - Download a backup set from an local archive volume

download\_backupset.py requires the following parameters:
```
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
```
This script automatically tries to download the backup files from the nodes which hold the local data and starts as many download threads as nodes are involved to speed up the download process. "wget" is used in this script to download the backup set.
