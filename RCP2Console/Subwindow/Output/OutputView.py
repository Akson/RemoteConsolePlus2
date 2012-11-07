'''Created by Dmytro Konobrytskyi, 2012(C)'''

import wx.html
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
        
class OutputView(wx.Panel):
    '''
    OutputView manages views
    '''

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self._view = HTMLConsole(parent)
        
        #Create a main sizer which will contain an output view
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)
        self._sizer.Add(self._view, 1, wx.EXPAND)
        self.Layout()

    def ProcessMessage(self, newMessage):
        self._view.ProcessMessage(newMessage)

    def SaveConfiguration(self):
        return {"Class":str(type(self._view))}

    def LoadConfiguration(self, config):
        print config