'''Created by Dmytro Konobrytskyi, 2012(C)'''
import json
from RCP2Console.Subwindow.Pipeline.CommandsProcessor import CommandsProcessor

class Message(object):
    def __init__(self, rawMessage):
        messageComponents = rawMessage.split(chr(0), 2)
        #print messageComponents

        self.Stream = messageComponents[0]
        
        #Try to parse JSON, if it does not work, just add value as a string
        self.Info = {}
        try:
            self.Info = json.loads(messageComponents[1])
        except:
            pass
        
        self.Data = {"Value":messageComponents[2]}
        

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
        
        self._pipelineComponents = [CommandsProcessor()]
        
    def ProcessMessage(self, message):
        parsedMessage = Message(message)
        
        #Move message through pipeline
        for pipelineComponent in self._pipelineComponents:
            pipelineComponent.ProcessMessage(parsedMessage)
        
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