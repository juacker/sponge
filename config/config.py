'''

xml.py xml methods

created: 23/11/2012
by juacker

'''

from xml.sax.handler import ContentHandler
import xml.sax
from xml.dom import minidom
import sys, os


class Config(object):
    def __init__(self, file):
        self.xml_analyzer = xml.sax.make_parser()
        self.xml_analyzer.setContentHandler(ContentHandler())
        if os.path.isfile(file):
            try:
                self.xml_analyzer.parse(file)
                self.xml_dom = minidom.parse(file)
            except Exception,err:
                print "Error analyzing XML file: "+str(file)+' '+err
                sys.exit(0)
        else:
            print "File not found:"+str(file)
            sys.exit(0)



