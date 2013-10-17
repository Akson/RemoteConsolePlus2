'''Created by Dmytro Konobrytskyi, 2012(C)'''
import json

class Pipeline(object):
    '''
    Pipeline receives, filters and processes messages before passing them to a view
    '''

    def __init__(self, source, destination):
        '''
        Constructor
        '''
        self._name = "Pipeline name"
        
        self._source = source
        self._destination = destination
        
        self._source.ConnectDataConsumer(self)#TEST
        
    def ProcessMessage(self, message):
        messageComponents = message.split(chr(0), 2)

        parsedMessage = {}
        parsedMessage["StreamName"] = messageComponents[0]
        
        
        #Try to parse JSON, if it does not work, just add value as a string
        value = None
        try:
            value = json.loads(messageComponents[1])
            parsedMessage.update(value)
        except:
            pass
        
        if value == None:
            parsedMessage["Value"] = messageComponents[1]
        
        
        self._destination.ProcessMessage(parsedMessage)

    def DisconnectFromRouter(self):
        self._source.DisconnectDataConsumer(self)
        
    def GetName(self):
        return self._name
    
    def SaveConfiguration(self):
        return {"xxx":"aaa"}

    def LoadConfiguration(self, config):
        print config
        
    def EditPipeline(self):
        print "EditPipeline"