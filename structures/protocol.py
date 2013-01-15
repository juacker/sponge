# coding: utf-8
'''
Copyright 2012 juan cañete (jcazor@komlog.org)
Licensed under The Apache License (2.0) 
http://www.apache.org/licenses/LICENSE-2.0.html

protocol.py - Protocol structures and methods
'''



class State:
    def __init__(self,receive,send,flag_initial=False,flag_final=False):
        self.receive = receive
        self.send = send
        self.flag_initial=flag_initial
        self.flag_final=flag_final
        
        
class Protocol:
    def __init__(self,protocol):
        self.protocol = str(protocol).lower()
        self.states=[]
        self.expected=[]
        
    def generate_states(self,host):
        if self.protocol == 'ssh':
            state = State(receive=None, send='ssh -p '+host.port+' '+host.user+'@'+host.host, flag_initial=True)
            self.states.append(state)
            state = State(receive='Are you sure',send='yes')
            self.states.append(state)
            state = State(receive='[pP]assword:',send=host.password)
            self.states.append(state)
            state = State(receive=host.prompt,send='',flag_final=True)
            self.states.append(state)
    
    def initialize(self,host):
        self.generate_states(host)
        for state in self.states:
            if state.receive:
                self.expected.append(u''+state.receive)
    
    def get_initial_state(self):
        for state in self.states:
            if state.flag_initial:
                return state
        return None
    
    def get_sendline(self,received):
        for state in self.states:
            if state.receive == received:
                if not state.flag_final:
                    return state.send
        return None
    
    
    