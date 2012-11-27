'''

servers.py Server configuration structurese and methods

created: 23/11/2012
by juacker
'''

class Servers(object):
    def __init__(self,user,password,host,port,name,previous=None):
        print "Creating servers"
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.name = name
        self.previous = previous
        self.protocol = 'ssh'
        if self.protocol == 'ssh':
            self.conn_cmd=self.protocol+' '+'-p '+self.port+' '+self.user+'@'+self.host



