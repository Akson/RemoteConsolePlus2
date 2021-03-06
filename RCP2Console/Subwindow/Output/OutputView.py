'''Created by Dmytro Konobrytskyi, 2012(C)'''

import wx.html
import wx.lib.agw.aui as aui
import time
from multiprocessing import Lock
import json
class HTMLConsole(wx.Panel):
    '''
    This destination class is the default console window
    which does show messages as HTML
    '''

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._messagesList = []
        self._needUpdate = False
        self._lockedView = False
        
        self._htmlWindow = wx.html.HtmlWindow(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        tb = self.BuildToolbar()
        sizer.Add( tb, 0, wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, 4 ) # add the toolbar to the sizer

        sizer.Add(self._htmlWindow, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_IDLE, self.CheckIfNeedUpdate)
        
        #Check every 50ms if there is a need to update the view due to recent messages
        self._mainTimer = wx.Timer(self, wx.ID_ANY)
        self._mainTimer.Start(50)
        self.Bind(wx.EVT_TIMER, self.CheckIfNeedUpdate, self._mainTimer)

        self._messagesListLock = Lock()

    def BuildToolbar( self ) :
        tb = aui.AuiToolBar( self, -1 )
        self.ToolBar = tb
        tb.SetToolBitmapSize( ( 8, 8) )# this required for non-standard size buttons on MSW

        self.Bind(wx.EVT_TOOL, self.OnToolLock, source = tb.AddSimpleTool(wx.ID_ANY, 'Lock view', wx.Image(r'RCP2Console\Resources\Lock.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Lock current view while processing messagse'))
        self.Bind(wx.EVT_TOOL, self.OnToolSettings, source = tb.AddSimpleTool(wx.ID_ANY, 'Settings', wx.Image(r'RCP2Console\Resources\Configure.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Open settings window'))
        self.Bind(wx.EVT_TOOL, self.OnToolClear, source = tb.AddSimpleTool(wx.ID_ANY, 'Clear', wx.Image(r'RCP2Console\Resources\Clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Clear all HTML text from console'))
        
        tb.Realize()

        return tb
            
    def OnToolClear(self, event=None):
        self._messagesListLock.acquire()
        self._messagesList = []
        self._needUpdate = True
        self._messagesListLock.release()
            
    def OnToolLock(self, event=None):
        self._lockedView = not self._lockedView
            
    def OnToolSettings(self, event=None):
        print "OnToolSettings"
            
    def CheckIfNeedUpdate(self, event=None):
        if self._needUpdate:
            self.Refresh()
        
    def OnPaint(self, event=None):
        if self._needUpdate and not self._lockedView:
            self._messagesListLock.acquire()

            consoleText = '<body><font face="Consolas">'
            consoleText += "<br>".join(self._messagesList)
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
        self._messagesList.append("%s: %s"%(newMessage.Stream, str(newMessage.Data["Value"])))
        
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