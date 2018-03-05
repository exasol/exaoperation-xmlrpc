# manageexaop - a python script for shutting down / starting the cluster, required services and all databases

This script allows you to completely start up or shutdown an existing Exasol cluster on Amazon Web Services and automatically start all necessary services and databases. Only a few parameters are necessary:

```
./manageexaop.py -h

    Options:
        -h                  shows this help
        -s                  start up cluster
        -o                  shutdown cluster
        -d                  trigger more output for debugging purposes
        -l <license server>
        -u <exaoperation user>
        -p <exaoperation pwd>
        -v <vpc id>
        -i <instances>
        -j <jump host instance>

```
## Startup
At least the following switches needs to be specified:

Parameter				| Comment												
------------------------|-----------------------------------------------------------
-s						| start up cluster
-l <license server>		| IP or domain name of the license server of your cluster
-u <exaoperation user> 	| EXAoperation user with at least "Administrator" role
-p <exaoperation pwd>	| Password used by your EXAoperation user
-v <vpc id>				| VPC ID - Id of your AWS Virtual Private Cloud network
-i <instance ids>		| comma separated list of instance Ids

You need to specify either -v <vpc id> or -i <comma separated list of instance Ids> but not both at the same time. If you use the -i option your list have to cover all AWS instances within the EXASOL cluster (otherwise the startup of services/database will fail).

## Shutdown
At least the following switches needs to be specified:

Parameter				| Comment												
------------------------|-----------------------------------------------------------
-o						| shutdown cluster
-l <license server>		| IP or domain name of the license server of your cluster
-u <exaoperation user> 	| EXAoperation user with at least "Administrator" role
-p <exaoperation pwd>	| Password used by your EXAoperation user
-v <vpc id>				| VPC ID - Id of your AWS Virtual Private Cloud network
-i <instance ids>		| comma separated list of instance Ids
-j <instance id>		| instance Id of your jump host (to prevent a shutdown)

Like on startup mode you need to specify either -v <vpc id> or -i <comma separated list of instance Ids> but not both at the same time. 

