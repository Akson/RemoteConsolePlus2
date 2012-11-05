'''Created by Dmytro Konobrytskyi, 2012(C)'''
import wx.html
from RCP2Console.Subwindow.Pipeline import Pipeline

class HTMLConsole(wx.Panel):
    '''
    This destination class is the default console window
    which does show messages as HTML
    '''

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._messagesList = []
        
        self._htmlWindow = wx.html.HtmlWindow(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._htmlWindow, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def ProcessMessage(self, newMessage):
        #Save new message to buffer
        self._messagesList.append(newMessage)
        
        #Limit buffer size
        self._messagesList = self._messagesList[-1000:]
        
        #Construct 
        #consoleText = '<body bgcolor="black"><font face="Consolas" color="white" size=4>'
        consoleText = '<body><font face="Consolas">'
        
        for message in self._messagesList:
            consoleText += "%s<br>" % message

        consoleText += "</font></body>"

        #Update console content and scroll to the bottom
        self._htmlWindow.Freeze()    
        self._htmlWindow.SetPage(consoleText)
        self._htmlWindow.Scroll(0, self._htmlWindow.GetScrollRange(wx.VERTICAL)) 
        self._htmlWindow.Thaw()


class Subwindow(wx.Panel):
    '''
    This class represents a subwindow including a set of message processing pipelines and an actual view
    '''

    def __init__(self, parentWindow, dataSource):
        '''
        Initialize default transparent pipeline and HTML view 
        '''
        wx.Panel.__init__(self, parentWindow, -1, size=wx.Size(200,150))

        self._dataSource = dataSource
        self._pipelinesList = []
        self._view = None

        #Disconnect all pipes when this window is destroyed
        self.Bind(wx.EVT_WINDOW_DESTROY, lambda event: Subwindow.DisconnectFromRouter(self))

        #Create a main sizer which will contain a view
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)

        #Create default view and pipeline        
        self.SetView(HTMLConsole(self))
        self.AddPipeline(Pipeline())
        
    def SetView(self, newView):
        #Remove an old view if it exists
        if self._view != None:
            self._sizer.Remove(self._view)
        self._view = newView
        
        #Change pipeline destinations
        for pipeline in self._pipelinesList:
            pipeline.SetView(self._view)

        #Add the new view to a screen        
        self._sizer.Add(self._view, 1, wx.EXPAND)
        self.Layout()
        
    def AddPipeline(self, newPipeline):
        self._pipelinesList.append(newPipeline)
        newPipeline.SetView(self._view)
        self._dataSource.ConnectDataConsumer(newPipeline)
        
    def DisconnectFromRouter(self):
        for pipeline in self._pipelinesList:
            self._dataSource.DisconnectDataConsumer(pipeline)

    def SaveConfiguration(self):
        return {"name":"aaa"}
    
    def LoadConfiguration(self, config):
        print config