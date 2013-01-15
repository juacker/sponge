# coding: utf-8
'''
Copyright 2012 juan cañete (jcazor@komlog.org)
Licensed under The Apache License (2.0) 
http://www.apache.org/licenses/LICENSE-2.0.html


logger.py - Logs methods
'''

from datetime import datetime

def log(message):
    print str(datetime.now())+' - '+str(message)