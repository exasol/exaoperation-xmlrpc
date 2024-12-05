# auto_update_exaop - a python script for updating exaoperation automatically

This script supports License server updates and security patches.
The following parameters are required:

```
usage: auto_update_exaop.py [-h] [--protocol PROTOCOL] [--user USER]
                            [--password PASSWORD] [--ip IP]
                            [--node_ips NODE_IPS [NODE_IPS ...]] [--port PORT]
                            [--packages PACKAGES [PACKAGES ...]]
                            [--loglevel [LOGLEVEL]] [--timeout TIMEOUT]
                            [--dest [DEST]]

Update EXASuite automatically

optional arguments:
  -h, --help            show this help message and exit

Required arguments:
  --protocol PROTOCOL   Communication protocol, https or http
  --user USER           Username to login to EXAoperation
  --password PASSWORD   Password of the given username
  --ip IP               IP address of license node
  --node_ips NODE_IPS [NODE_IPS ...]
                        List of ip addresses of cluster nodes
  --port PORT           Port number of license node
  --packages PACKAGES [PACKAGES ...]
                        List of package paths

Optional arguments:
  --loglevel [LOGLEVEL]
                        Logging level, default value is 20
  --timeout TIMEOUT     Timeout for upgrading the management node in minutes,
                        default value is 60
  --dest [DEST]         The destination directory, where the update packages
                        should be copied and uploaded. If the given directoy
                        does not exist, it will be created. This directory
                        will be removed after the update. Default destination
                        /tmp/exasuite_update
```

Example Call:
``auto_update_exaop.py --timeout 15 --protocol https --user admin --password admin --ip 192.168.0.10 --node_ips 192.168.0.11 192.168.0.12 --port 443 --packages https://x-up.s3.amazonaws.com/7.x/7.1.30/EXAClusterOS-7.1.30_LS-Update.pkg --dest "C:\Temp\updates\\" ``

## Troubleshooting
With the latest versions of Python, you may receive some sporadic SSL errors. In these cases, try running the script with an earlier version of Pythong, for example Python 3.8.