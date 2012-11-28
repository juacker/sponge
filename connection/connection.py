'''
created on 22/11/2012
by juacker

'''

import pexpect,sys
import time

class Connection(object):
    def __init__(self, conn_chain):
        self.conn_chain = conn_chain
        self.interactive = False
        

    def establish(self):
        host = self.conn_chain[0]
        self.conn_chain.pop(0)
        print "Connecting to: "+host.name
        out = -1
        cmd_list = []
        expected = [host.prompt,'Are you sure','[pP]assword:',pexpect.EOF]
        self.connection = pexpect.spawn(host.conn_cmd)
        while not out == 0:
            for cmd in cmd_list:
                self.connection.sendline(cmd)
                time.sleep(1)
                
            out=self.connection.expect(expected)
            if out==0:
                pass
            if out==1:
                cmd_list=['yes',host.prompt_cmd]
            if out==2:
                cmd_list = [host.password,host.prompt_cmd]
            if out==3:
                cmd_list = [host.prompt_cmd,]
                print "I either got key or connection timeout connection to "+host.host
                sys.exit(1)
            if out==4:
                print "Timeout connecting to host: "+host.host
                sys.exit(1)
                            
        a = self.connection.before
        #print self.connection.before
        self.connection.sendline('\r\n')

        for host in self.conn_chain:
            print "Connecting to: "+host.name
            out = -1
            cmd_list = [host.conn_cmd,]
            expected = [host.prompt,'Are you sure','[pP]assword:',pexpect.EOF]
            while not out == 0:
                for cmd in cmd_list:
                    self.connection.sendline(cmd)
                out=self.connection.expect(expected)
                if out==0:
                    pass
                if out==1:
                    cmd_list =['yes',host.prompt_cmd]
                if out==2:
                    cmd_list = [host.password,host.prompt_cmd]
                if out==3:
                    cmd_list = [host.prompt_cmd,]
                    print "I either got key or connection timeout connection to "+host.host
                    sys.exit(1)
                if out==4:
                    print "Timeout connecting to host: "+host.host
                    sys.exit(1)
            a = self.connection.before
            self.connection.sendline('\r\n')
    
    def interact(self):
        self.interactive = True
        try:
            self.connection.interact()
            sys.exit(0)
        except:
            print "Error switching to interactive mode"
            sys.exit(1)


