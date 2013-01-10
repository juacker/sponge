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
from config import config, logger
from connection import connection

DEFAULT_DIR='.sponge'

def main():
    parser = argparse.ArgumentParser(prog='sponge.py')
    parser.add_argument('-s','--server', required=True, help='server to connect to (defined in servers.xml)')
    parser.add_argument('-c','--command', help='command to execute (defined in commands.xml)')
    
    
    args = parser.parse_args()
    sponge_dir = os.path.join(os.getenv('HOME'),DEFAULT_DIR)
    conf = config.Config(sponge_dir)
    serverchain = conf.get_serverschain(args.server)
    command = None
    if args.command:
        command = conf.get_command(args.command)
    if args.command and not command:
        logger.log('Error: Command not found. Exiting')
        sys.exit()
    #os.environ['INPUTRC'] = '/etc/inputrc'
    conn = connection.Connection(serverchain)
    conn.establish()
    if not args.command:
        conn.interact()
    else:
        conn.send_command(command)

if __name__=='__main__':
    main()