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

        #Create all subwindow components
        self._dataSource = dataSource
        self._outputView = OutputView(self)
        self._pipelinesList = [Pipeline(self._dataSource, self._outputView)]

        #Create a main sizer which will contain an output view
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        sizer.Add(self._outputView, 1, wx.EXPAND)
        self.Layout()

        #Disconnect all pipes when this window is destroyed
        self.Bind(wx.EVT_WINDOW_DESTROY, lambda event: Subwindow.DisconnectFromRouter(self))

    def DisconnectFromRouter(self):
        #Disconnect all pipes from the router
        for pipeline in self._pipelinesList:
            pipeline.DisconnectFromRouter()

    def SaveConfiguration(self):
        config = {}
        config["outputView"] = self._outputView.SaveConfiguration()
        pipelinesConfig = {}
        for pipeline in self._pipelinesList:
            pipelinesConfig[pipeline.GetName()] = pipeline.SaveConfiguration()
        config["pipelines"] = pipelinesConfig
        return config
    
    def LoadConfiguration(self, config):
        self.DisconnectFromRouter()
        
        self._outputView.LoadConfiguration(config["outputView"])

        self.DisconnectFromRouter()
        self._pipelinesList = []
        pipelinesConfig = config["pipelines"]
        for pipelineConfigName in pipelinesConfig.iterkeys():
            pipeline = Pipeline(self._dataSource, self._outputView)
            pipeline.LoadConfiguration(pipelinesConfig[pipelineConfigName])
            self._pipelinesList.append(pipeline)

    def EditOutputView(self):
        print "EditOutputView"
            
    def ManagePipelines(self):
        print "ManagePipelines"