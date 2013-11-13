'''
Created on Oct 21, 2013

@author: dima
'''
import string
import json

class CommandsProcessor(object):
    '''
    Pipeline receives, filters and processes messages before passing them to a view
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def ProcessMessage(self, message):
        if "Commands" not in message.Info: return #No commands, no processing:) 
        
        commands = message.Info["Commands"]
        commands = map(string.strip, commands)
        
        for command in commands:
            commandName = command[0:command.find("(")]
            if commandName == "ParseJson":
                message.Data.update(json.loads(message.Data["Value"]))
            if commandName == "Variable":
                message.Data["Value"] = "<b>%s</b> = %s"%(message.Data["Name"], message.Data["Value"])