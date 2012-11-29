#!/usr/bin/env python


import argparse
import os
import sys
from config import config
from connection import connection

def main():
    parser = argparse.ArgumentParser(prog='sponge.py')
    parser.add_argument('-s','--server', required=True, help='server to connect to')
    parser.add_argument('-c','--command', help='command to execute')
    
    
    args = parser.parse_args()
    sponge_dir = os.path.dirname(sys.argv[0])
    conf = config.Config(sponge_dir)
    serverchain = conf.get_serverschain(args.server)
    
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