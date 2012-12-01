#!/usr/bin/env python

'''
Copyright 2012 juan canete (jcazor@komlog.org)
Licensed under The Apache License (2.0) 
http://www.apache.org/licenses/LICENSE-2.0.html

sponge.py - main 
'''

import argparse
import os
import sys
from config import config
from connection import connection

def main():
    parser = argparse.ArgumentParser(prog='sponge.py')
    parser.add_argument('-s','--server', required=True, help='server to connect to (defined in servers.xml)')
    parser.add_argument('-c','--command', help='command to execute (defined in commands.xml)')
    
    
    args = parser.parse_args()
    sponge_dir = os.path.dirname(sys.argv[0])
    conf = config.Config(sponge_dir)
    serverchain = conf.get_serverschain(args.server)
    
    os.environ['INPUTRC'] = '/etc/inputrc'
    conn = connection.Connection(serverchain)
    conn.establish()
    if not args.command:
        conn.interact()
    else:
        command = conf.get_command(args.command)
        if command:
            conn.send_command(command)

if __name__=='__main__':
    main()