'''Created by Dmytro Konobrytskyi, 2013(C)'''

import zmq
import json
import time

class RCP2Client(object):
    def __init__(self):
        pass
    
    def Connect(self, address):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._socket.connect(address)
    
    def SendMessage(self, value, streamName=None, commands=None):
        if self._socket == None:
            raise Exception("Attempt to send message without connection.")

        additionalInfo = dict()
        additionalInfo["TimeStamp"] = int(time.time()*1000)
        if commands!=None: additionalInfo["Commands"] = commands
        
        message = "%s%c%s%c%s"%("" if streamName == None else streamName, chr(0), json.dumps(additionalInfo), chr(0), str(value))
    
        #print message
        self._socket.send(message)