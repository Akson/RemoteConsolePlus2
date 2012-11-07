'''Created by Dmytro Konobrytskyi, 2012(C)'''

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
        self._destination.ProcessMessage(message)

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