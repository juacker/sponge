'''
Copyright 2012 juan canete (jcazor@komlog.org)
Licensed under The Apache License (2.0) 
http://www.apache.org/licenses/LICENSE-2.0.html


servers.py - Servers structures and methods
'''

import sys
from config import logger

class Server(object):
    def __init__(self,xml_server):
        try:
            for attr in ['user','password','host','port','name','parent']:
                setattr(self,attr,str(xml_server.getElementsByTagName(attr)[0].childNodes[0].toxml()))
        except IndexError:
            if attr == 'parent':
                self.parent = None
            else:
                logger.log("Attribute not found: "+attr)
                sys.exit(0)
        self.protocol = 'ssh'
        if self.protocol == 'ssh':
            self.prompt = self.user+'@'+self.name+': '
            self.prompt_cmd = 'export PS1="'+self.prompt+'"'
            self.conn_cmd=self.protocol+' '+'-p '+self.port+' '+self.user+'@'+self.host



