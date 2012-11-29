'''
created on 22/11/2012
by juacker

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
        cmd_list = []
        expected = [self.host.prompt,'Are you sure','[pP]assword:',pexpect.EOF]
        self.connection = pexpect.spawn(self.host.conn_cmd)
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

    
    def interact(self):
        self.interactive = True
        try:
            self.connection.interact()
            sys.exit(0)
        except Exception as e:
            logger.log(str(e))
            logger.log("Error switching to interactive mode")
            sys.exit(1)
    
    def send_command(self,command):
        logger.log("Executing: "+command.cmd_line)
        self.connection.setecho(False)
        #clean the buffer
        self.connection.buffer = ''
        self.connection.sendline(command.cmd_line)
        expected = [self.host.prompt]
        self.connection.expect(expected)
        print self.connection.before.strip(command.cmd_line)
        
        


