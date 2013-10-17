'''Created by Dmytro Konobrytskyi, 2012(C)'''

import wx.html
import time
from multiprocessing import Lock
class HTMLConsole(wx.Panel):
    '''
    This destination class is the default console window
    which does show messages as HTML
    '''

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._messagesList = []
        self._needUpdate = False;
        
        self._htmlWindow = wx.html.HtmlWindow(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._htmlWindow, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_IDLE, self.CheckIfNeedUpdate)
        
        #Check every 50ms if there is a need to update the view due to recent messages
        self._mainTimer = wx.Timer(self, wx.ID_ANY)
        self._mainTimer.Start(50)
        self.Bind(wx.EVT_TIMER, self.CheckIfNeedUpdate, self._mainTimer)
        
        self._messagesListLock = Lock()
        
    def CheckIfNeedUpdate(self, event=None):
        if self._needUpdate:
            self.Refresh()
        
    def OnPaint(self, event=None):
        if self._needUpdate:
            
            self._messagesListLock.acquire()

            consoleText = '<body><font face="Consolas">'
            for message in self._messagesList:
                consoleText += "%s<br>" % message
            consoleText += "</font></body>"
    
            self._needUpdate = False
            
            self._messagesListLock.release()
            
            #Update console content and scroll to the bottom
            self._htmlWindow.Freeze()    
            self._htmlWindow.SetPage(consoleText)
            self._htmlWindow.Scroll(0, self._htmlWindow.GetScrollRange(wx.VERTICAL)) 
            self._htmlWindow.Thaw()
        
        dc = wx.PaintDC(self)#We need to create for solving infinity EVT_PAINT problem


    def ProcessMessage(self, newMessage):
        self._messagesListLock.acquire()

        #Save new message to buffer
        self._messagesList.append(newMessage)
        
        #Limit buffer size
        self._messagesList = self._messagesList[-1000:]
        
        self._needUpdate = True

        self._messagesListLock.release()
        
class OutputView(wx.Panel):
    '''
    OutputView manages views
    '''

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self._view = HTMLConsole(self)
        
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