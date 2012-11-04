'''Created by Dmytro Konobrytskyi, 2012(C)'''

import zmq

class Router(object):
    '''
    classdocs
    '''

    def __init__(self, inputAddress, outputAddress):
        '''
        Here we initialize input and output ZMQ sockets
        '''
        self._inputAddress = inputAddress        
        self._outputAddress = outputAddress
        
        #Initialize ZMQ
        self._context = zmq.Context()
        
        #Create an input socket and subscribe for everything
        self._inputSocket = self._context.socket(zmq.SUB)
        self._inputSocket.bind(self._inputAddress)
        self._inputSocket.setsockopt(zmq.SUBSCRIBE, "")

        #Create an output socket
        self._outputSocket = self._context.socket(zmq.PUB)
        self._outputSocket.bind(self._outputAddress)

    def Run(self):
        while True:
            message = self._inputSocket.recv()
            self._outputSocket.send(message)
            #print message
