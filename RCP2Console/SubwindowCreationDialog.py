'''Created by Dmytro Konobrytskyi, 2012(C)'''
import wx

class SubwindowCreationDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self._position = wx.RadioBox(self, -1, "Select position", choices=["Top", "Bottom", "Left", "Right", "Center"], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
        self._name = wx.TextCtrl(self, -1, "Default name")
        self.sizer_3_staticbox = wx.StaticBox(self, -1, "Select name")
        self.OkButton = wx.Button(self, wx.ID_OK, "Ok")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle("Create subwindow")
        self._position.SetSelection(0)
        self.OkButton.SetFocus()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_3_staticbox.Lower()
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.HORIZONTAL)
        sizer_1.Add(self._position, 0, wx.ALL | wx.EXPAND, 3)
        sizer_3.Add(self._name, 0, wx.ALL, 0)
        sizer_1.Add(sizer_3, 0, wx.ALL | wx.EXPAND, 3)
        sizer_1.Add(self.OkButton, 0, wx.ALL | wx.EXPAND, 3)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def GetPosition(self):
        return [wx.TOP, wx.BOTTOM, wx.LEFT, wx.RIGHT, wx.CENTER][self._position.GetSelection()]
    
    def GetName(self):
        return self._name.GetValue()