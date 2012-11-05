'''Created by Dmytro Konobrytskyi, 2012(C)'''
from RCP2Console.Subwindow.Pipeline.Pipeline import Pipeline
from RCP2Console.Subwindow.Output.OutputView import OutputView
import wx

class Subwindow(wx.Panel):
    '''
    This class represents a subwindow including a set of message processing pipelines and an actual view
    '''

    def __init__(self, parentWindow, dataSource):
        '''
        Initialize default transparent pipeline and a view 
        '''
        wx.Panel.__init__(self, parentWindow, -1, size=wx.Size(200,150))

        self._dataSource = dataSource
        self._outputView = OutputView(self)
        self._pipelinesList = [Pipeline(self._dataSource, self._outputView)]

        #Disconnect all pipes when this window is destroyed
        self.Bind(wx.EVT_WINDOW_DESTROY, lambda event: Subwindow.DisconnectFromRouter(self))

        #Create a main sizer which will contain a view
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)
        self._sizer.Add(self._outputView, 1, wx.EXPAND)
        self.Layout()
        
    def DisconnectFromRouter(self):
        for pipeline in self._pipelinesList:
            pipeline.DisconnectFromRouter()

    def SaveConfiguration(self):
        return {"name":"aaa"}
    
    def LoadConfiguration(self, config):
        print config