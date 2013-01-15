# coding: utf-8
'''
Copyright 2012 juan cañete (jcazor@komlog.org)
Licensed under The Apache License (2.0) 
http://www.apache.org/licenses/LICENSE-2.0.html

connection.py - Connection structures and methods
'''

import pexpect,sys
from config import logger

LOCAL_SHELL='/bin/bash'

class Connection(object):
    def __init__(self, conn_chain):
        self.conn_chain = conn_chain
        self.interactive = False
        self.expected=[]       

    def establish(self):
        self.connection = pexpect.spawn(LOCAL_SHELL)
        self.connection.delaybeforesend = 0.5
                
        for host in self.conn_chain:
            logger.log('Connecting to: '+host.name)
            self.expected= host.protocol.expected
            self.expected.append(pexpect.EOF)
            self.expected.append(pexpect.TIMEOUT)
            initial_state = host.protocol.get_initial_state()
            self.connection.sendline(initial_state.send)
            self.connection.setecho(False)
            received = self.connection.expect(self.expected)
            sendline = '$$$'
            while sendline:
                sendline = host.protocol.get_sendline(self.expected[received])
                if sendline:
                    self.connection.sendline(sendline)
                    self.connection.setecho(False)
                    received = self.connection.expect(self.expected)               

    def interact(self):
        self.interactive = True
        try:
            self.connection.sendline('reset')
            self.connection.interact()
            sys.exit(0)
        except Exception as e:
            logger.log(str(e))
            logger.log("Error switching to interactive mode")
            sys.exit(1)
    
    def send_command(self,command):
        logger.log("Executing: "+command.cmd_line)

        self.connection.buffer = ''
        self.connection.logfile_read = sys.stdout
        self.connection.sendline(command.cmd_line)
        self.connection.expect(self.expected, timeout=None)
