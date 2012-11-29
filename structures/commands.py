'''

commands.py Command configuration structures and methods

created: 29/11/2012
by juacker
'''

import sys

class Command(object):
    def __init__(self,xml_command):
        try:
            for attr in ['name','cmd_line']:
                setattr(self,attr,str(xml_command.getElementsByTagName(attr)[0].childNodes[0].toxml()))
        except IndexError:
            print "Attribute not found: "+attr
            sys.exit(0)
        