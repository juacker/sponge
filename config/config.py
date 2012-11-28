'''

xml.py xml methods

created: 23/11/2012
by juacker

'''

from xml.sax.handler import ContentHandler
import xml.sax
from xml.dom import minidom
import sys, os
import servers


class Config(object):
    def __init__(self, path):
        self.xml_analyzer = xml.sax.make_parser()
        self.xml_analyzer.setContentHandler(ContentHandler())
        self.servers_file = os.path.join(path,'servers.xml')
        self.commands_file = os.path.join(path, 'commands.xml')
        
        for file in (self.servers_file,self.commands_file):
            if os.path.isfile(file):
                try:
                    self.xml_analyzer.parse(file)
                except Exception,err:
                    print "Error analyzing XML file: "+str(os.path.basename(file))+' Error:'+str(err)
                    sys.exit(0)
            else:
                print "Required file not found:"+str(file)
                sys.exit(0)
        self.servers_xml = minidom.parse(os.path.join(path,self.servers_file))
        self.commands_xml = minidom.parse(os.path.join(path,self.commands_file))
    
    def get_serverschain(self, servername):
        serverchain = []
        server_list = self.servers_xml.childNodes
        xml_servers = server_list[0].childNodes
        def get_serverandparent(xml_servers, servername):
            for i in range(len(xml_servers)):
                try:
                    server = servers.Servers(xml_servers[i])
                    if server.name == servername:
                        return server
                except IndexError as e:
                    pass
                except AttributeError as e:
                    pass
                except Exception as e:
                    print "Error generating server chain "+str(e)
                    sys.exit(1)
            return None
        server = get_serverandparent(xml_servers, servername)
        if not server:
            print "Server not found: "+servername
            sys.exit(0)
        else:
            serverchain.insert(0,server)
            while server.parent:
                server = get_serverandparent(xml_servers, server.parent)
                if server:
                    serverchain.insert(0,server)
        return serverchain
        