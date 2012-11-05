'''Created by Dmytro Konobrytskyi, 2012(C)'''

class Pipeline(object):
    '''
    Pipeline receives, filters and processes messages before passing them to a view
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._view = None
        
    def SetView(self, view):
        self._view = view
        
    def ProcessMessage(self, message):
        self._view.ProcessMessage(message)
