'''
Copyright 2012 juan canete (jcazor@komlog.org)
Licensed under The Apache License (2.0) 
http://www.apache.org/licenses/LICENSE-2.0.html

config.py - Configuration management
'''

from xml.sax.handler import ContentHandler
import xml.sax
from xml.dom import minidom
import sys, os
from structures import servers,commands
import logger


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
                    logger.log("Error analyzing XML file: "+str(os.path.basename(file))+' Error:'+str(err))
                    sys.exit(0)
            else:
                logger.log("Required file not found:"+str(file))
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
                    server = servers.Server(xml_servers[i])
                    if server.name == servername:
                        return server
                except IndexError as e:
                    pass
                except AttributeError as e:
                    pass
                except Exception as e:
                    logger.log("Error generating server chain "+str(e))
                    sys.exit(1)
            return None
        server = get_serverandparent(xml_servers, servername)
        if not server:
            logger.log("Server not found: "+servername)
            sys.exit(0)
        else:
            serverchain.insert(0,server)
            while server.parent:
                server = get_serverandparent(xml_servers, server.parent)
                if server:
                    serverchain.insert(0,server)
        return serverchain
    
    def get_command(self, commandname):
        command_list = self.commands_xml.childNodes
        xml_commands = command_list[0].childNodes
        def get_command(xml_commands, commandname):
            for i in range(len(xml_commands)):
                try:
                    command = commands.Command(xml_commands[i])
                    if command.name == commandname:
                        return command
                except IndexError as e:
                    pass
                except AttributeError as e:
                    pass
                except Exception as e:
                    logger.log("Error obtaining command "+str(e))
                    sys.exit(1)
            return None
        command = get_command(xml_commands, commandname)
        if not command:
            logger.log("command not found: "+commandname)
            sys.exit(0)
        else:
            return command
            
        