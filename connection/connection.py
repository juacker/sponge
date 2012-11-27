'''
created on 22/11/2012
by juacker

'''

import pexpect,sys

msg_newkey='Are you sure'
msg_password='[pP]assword:'
msg_nopassword='\$ '


class Connection(object):
    def __init__(self, conn_chain, interactive=True, command=None):
        print "Creating connection"
        self.conn_chain = conn_chain
        self.interactive = interactive
        self.command = command

    def establish(self):
        first_hop = self.conn_chain[0]
        self.conn_chain.pop(0)
        print "Connecting to: "+first_hop.host
        self.connection = pexpect.spawn(first_hop.conn_cmd)
        out=self.connection.expect([msg_newkey,msg_password,msg_nopassword,pexpect.EOF])
        if out==0:
            self.connection.sendline('yes')
            out=self.connection.expect([msg_newkey,msg_password,msg_nopassword,pexpect.EOF])
        if out==1:
            self.connection.sendline(first_hop.password)
            out = self.connection.expect([msg_nopassword])
        elif out==2:
            print "recibido"
            print out
        elif out==3:
            print "I either got key or connection timeout"
            sys.exit()
        elif out==4: #timeout
            print "Timeout connecting to host:"+first_hop.host
            sys.exit()
        a = self.connection.before
        print self.connection.before
        self.connection.sendline('\r\n')

        for host in self.conn_chain:
            print "Connecting to "+host.host
            print host.conn_cmd
            self.connection.sendline(host.conn_cmd)
            out=self.connection.expect([msg_newkey,msg_password,msg_nopassword,pexpect.EOF])
            if out==0:
                self.connection.sendline('yes')
                out=self.connection.expect([msg_newkey,msg_password,msg_nopassword,pexpect.EOF])
            if out==1:
                self.connection.sendline(host.password)
            elif out==2:
                print "recibido nopasswd: "+str(out)
                pass
            elif out==3:
                print "I either got key or connection timeout connection to "+host.host
                sys.exit(1)
            elif out==4:
                print "Timeout connecting to host: "+host.host
                sys.exit(1)
            self.connection.sendline('\r\n')

        if self.interactive:
            try:
                self.connection.interact()
                sys.exit(0)
            except:
                sys.exit(1)
        elif (not self.interactive and not self.command==None):
            sys.exit(0)
        else:
            sys.exit(0)


