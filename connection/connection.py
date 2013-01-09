'''
Copyright 2012 juan canete (jcazor@komlog.org)
Licensed under The Apache License (2.0) 
http://www.apache.org/licenses/LICENSE-2.0.html

connection.py - Connection structures and methods
'''

import pexpect,sys
import time
from config import logger

class Connection(object):
    def __init__(self, conn_chain):
        self.conn_chain = conn_chain
        self.interactive = False
        

    def establish(self):
        self.host = self.conn_chain[0]
        self.conn_chain.pop(0)
        print "Connecting to: "+self.host.name
        out = -1
        t=0
        cmd_list = []
        expected = [self.host.prompt,'Are you sure','[pP]assword:',pexpect.EOF, pexpect.TIMEOUT]
        self.connection = pexpect.spawn(self.host.conn_cmd)
        self.connection.delaybeforesend = 0.2
        self.connection.setecho(False)
        while not out == 0:
            for cmd in cmd_list:
                self.connection.sendline(cmd)
                time.sleep(1)                
            out=self.connection.expect(expected)
            if out==0:
                pass
            if out==1:
                cmd_list=['yes',self.host.prompt_cmd]
            if out==2:
                cmd_list = [self.host.password,self.host.prompt_cmd]
            if out==3:
                cmd_list = [self.host.prompt_cmd,]
                logger.log("I either got key or connection timeout connection to "+self.host.host)
                sys.exit(1)
            if out==4:
                if t==0:
                    cmd_list = [self.host.prompt_cmd,]
                    t=1
                else:
                    logger.log("Timeout connecting to host: "+self.host.host)
                    sys.exit(1)


        for self.host in self.conn_chain:
            print "Connecting to: "+self.host.name
            out = -1
            cmd_list = [self.host.conn_cmd,]
            expected = [self.host.prompt,'Are you sure','[pP]assword:',pexpect.EOF]
            while not out == 0:
                for cmd in cmd_list:
                    self.connection.sendline(cmd)
                    time.sleep(1)
                out=self.connection.expect(expected)
                if out==0:
                    pass
                if out==1:
                    cmd_list =['yes',self.host.prompt_cmd]
                if out==2:
                    cmd_list = [self.host.password,self.host.prompt_cmd]
                if out==3:
                    cmd_list = [self.host.prompt_cmd,]
                    logger.log("I either got key or connection timeout connection to "+self.host.host)
                    sys.exit(1)
                if out==4:
                    logger.log("Timeout connecting to host: "+self.host.host)
                    sys.exit(1)
        self.connection.sendline('\n')

    
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
        self.connection.sendline('########## COMMAND END ###########\n')
        expected = ['###########']
        self.connection.expect(expected, timeout=None)
        
        
        
        


