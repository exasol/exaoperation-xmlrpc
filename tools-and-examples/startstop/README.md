#startstop - ordinary starting and stopping of Exasol clusters and services

In this directory you will find three files:
* start.py: automatically starts all services and databases
* stop.py: stops alls database instances and shuts down cluster and all nodes
* startstop.cfg: configuration file

The configuration files looks like this:
```
[startstop]
username = admin
password = admin
hostname = 10.0.0.10
licenseServerNode = n0010
exaOperationTimeout = 150
```
"username" and "passwords" are EXAoperation credentials, "hostname" is the hostname or IP of your license server. "licenseServerNode" is the node name of your license server. This script is currently limited to configurations with only one license server.
"exaOperationTimeout" is the time span for restarting the EXAoperation service and getting back the web (and XMLRPC) interface.
