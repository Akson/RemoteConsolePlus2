'''Created by Dmytro Konobrytskyi, 2012(C)'''
import wx
from agw import aui
import json

from RCP2Console.ConsoleRouter import ConsoleRouter
from RCP2Console.Subwindow.Subwindow import Subwindow
from RCP2Console.SubwindowCreationDialog import SubwindowCreationDialog

class Console(wx.Frame):
    '''
    This is a main window class which can have multiple subwindows. 
    It stores a ConsoleRouter object that routes messages to each subwindow
    and AuiManager that manages panes with subwindows inside.
    '''

    def __init__(self, routerAddress):
        '''
        Here we create wx.App and run a main loop.
        '''
        app = wx.App(redirect=False)  #default error output to console

        #ConsoleRouter receives messages and passes them to views 
        self._routerAddress = routerAddress
        self._router = ConsoleRouter(self._routerAddress)
        
        self.InitializeUI()

        #Run main message receiving timer
        timerOwner = wx.EvtHandler()
        mainTimer = wx.Timer(timerOwner, wx.ID_ANY)
        mainTimer.Start(100)
        timerOwner.Bind(wx.EVT_TIMER, self.ProcessMessagess, mainTimer)
        timerOwner.Bind(wx.EVT_IDLE, self.ProcessMessagess, mainTimer)
        
        #Run main message loop
        app.MainLoop()
        
    def ProcessMessagess(self, event):
        self._router.ProcessIncomingMessages()

    def InitializeUI(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="RCP2 Console", size=(800, 600))

        self.CreateMenuBar()
        
        self._auiMgr = aui.AuiManager()
        self._auiMgr.SetManagedWindow(self)

        #Add default console
        self.CreateNewSubwindow(wx.CENTER, "Default console")

        self.Show()
        
    def CreateMenuBar(self):
        mb = wx.MenuBar()

        windowsMenu = wx.Menu()
        mb.Append(windowsMenu, "&Layout")
        self.Bind(wx.EVT_MENU, self.OnAddSubwindow, windowsMenu.Append(wx.NewId(), "Add subwindow"))
        windowsMenu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.OnSaveLayout, windowsMenu.Append(wx.NewId(), "Save layout"))
        self.Bind(wx.EVT_MENU, self.OnLoadLayout, windowsMenu.Append(wx.NewId(), "Load layout"))

        self.SetMenuBar(mb)

    def CreateNewSubwindow(self, pos=wx.TOP, caption=None):
        subwindow = Subwindow(self, self._router)
        self._auiMgr.AddPane(subwindow, pos, caption)
        self._auiMgr.GetPaneByWidget(subwindow).DestroyOnClose(True)
        self._auiMgr.Update()
        return subwindow

    def OnAddSubwindow(self, event):
        dialog = SubwindowCreationDialog(None)
        if dialog.ShowModal() == wx.ID_OK:
            self.CreateNewSubwindow(dialog.GetPosition(), dialog.GetName())
        dialog.Destroy()      
        
    def OnSaveLayout(self, event):
        #Generate config dictionary
        layout = {}
        layout["SubwindowsLayout"] = self._auiMgr.SavePerspective()
        panes = {}
        for pane in self._auiMgr.GetAllPanes():
            panes[pane.name] = pane.window.SaveConfiguration()
        layout["SubwindowsConfigs"] = panes 
        
        #Save to file
        f = open("layout.cfg", "w")
        f.write(json.dumps(layout))
        f.close()

    def OnLoadLayout(self, event):
        #Load from file
        f = open("layout.cfg", "r")
        layout = json.load(f)
        f.close()

        #Close existing panes
        for pane in list(self._auiMgr.GetAllPanes()):
            self._auiMgr.ClosePane(pane)

        #Create new panes with names from the config file   
        subwindowsConfigs = layout["SubwindowsConfigs"]
        for paneName in subwindowsConfigs.iterkeys():
            subwindow = self.CreateNewSubwindow()
            self._auiMgr.GetPaneByWidget(subwindow).Name(paneName)
            subwindow.LoadConfiguration(subwindowsConfigs[paneName])
            
        #Load the stored perspective
        self._auiMgr.LoadPerspective(layout["SubwindowsLayout"])