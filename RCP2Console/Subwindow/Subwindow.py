'''Created by Dmytro Konobrytskyi, 2012(C)'''
import wx


import wx.html
import string

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
    classdocs
    '''


    def __init__(self, parentWindow, dataSource):
        '''
        Constructor
        '''
        wx.Panel.__init__(self, parentWindow, -1, size=wx.Size(200,150))
        self._dataSource = dataSource
        self._dataSource.ConnectDataConsumer(self) #TEST ONLY!!!!!!!!!!!
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._view = HTMLConsole(self)
        sizer.Add(self._view, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
        
    def ProcessMessage(self, message):
        self._view.ProcessMessage(message)

    def DisconnectFromRouter(self):
        self._dataSource.DisconnectDataConsumer(self) #TEST ONLY!!!!!!!!!!!

    def SaveConfiguration(self):
        return {"name":"aaa"}
    
    def LoadConfiguration(self, config):
        print config