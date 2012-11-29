'''

commands.py Command configuration structures and methods

created: 29/11/2012
by juacker
'''

import sys
from config import logger

class Command(object):
    def __init__(self,xml_command):
        try:
            for attr in ['name','cmd_line']:
                setattr(self,attr,str(xml_command.getElementsByTagName(attr)[0].childNodes[0].toxml()))
        except IndexError:
            logger.log("Attribute not found: "+attr)
            sys.exit(0)
        