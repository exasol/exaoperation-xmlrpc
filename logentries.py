#!/usr/bin/env python

import os
from xmlrpclib import Server as xmlrpc

server = xmlrpc(open(os.path.join(os.path.expanduser('~'), '.exaopurl')).read().strip())
for lm in reversed(server.logservice1.logEntries()[2]):
    if 'executable overwritten:' in lm['message']: continue
    print lm['strtime'], lm['system'], lm['node'], lm['message']
