'''Created by Dmytro Konobrytskyi, 2012(C)'''
import zmq
import time

class ConsoleRouter(object):
    '''
    A console router receives messages from an external router 
    and routes them to all connected data consumers (fronts of pipelines)  
    '''

    def __init__(self, routerAddress):
        '''
        Creates required connections and initialize data
        '''
        
        self._routerAddress = routerAddress

        #Initialize ZMQ
        self._context = zmq.Context()
        
        #Create an input socket and subscribe for everything
        self._inputSocket = self._context.socket(zmq.SUB)
        self._inputSocket.connect(self._routerAddress)
        self._inputSocket.setsockopt(zmq.SUBSCRIBE, "")

        #Here we will store all data consumers where messages have to be routed
        self._dataConsumersList = []
        
    def ProcessIncomingMessages(self):
        try:
            message = self._inputSocket.recv(zmq.NOBLOCK)
            for consumer in self._dataConsumersList:
                consumer.ProcessMessage(message)
        except zmq.ZMQError, e:
            print e
            time.sleep(0.001)

    def ConnectDataConsumer(self, dataConsumer):
        self._dataConsumersList.append(dataConsumer)
        
    def DisconnectDataConsumer(self, dataConsumer):
        print "DisconnectDataConsumer"
        self._dataConsumersList.remove(dataConsumer)
