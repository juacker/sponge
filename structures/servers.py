# coding: utf-8
'''
Copyright 2012 juan cañete (jcazor@komlog.org)
Licensed under The Apache License (2.0) 
http://www.apache.org/licenses/LICENSE-2.0.html


servers.py - Servers structures and methods
'''

import sys
from config import logger
import protocol

class Server(object):
    def __init__(self,xml_server):
        for attr in ['user','password','host','port','name','protocol','parent','prompt']:
            try:
                setattr(self,attr,xml_server.getElementsByTagName(attr)[0].childNodes[0].data)
            except IndexError:
                if attr == 'parent':
                    self.parent = None
                elif attr == 'prompt':
                    self.prompt = self.user+'@'+self.host
                else:
                    logger.log("Attribute not found: "+attr)
                    sys.exit(0)
        proto = protocol.Protocol(self.protocol)
        proto.initialize(self)
        self.protocol = proto
        


