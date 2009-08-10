# create a simple media player with wxPython's
# wx.lib.filebrowsebutton.FileBrowseButton(parent,labelText,fileMask)
# wx.media.MediaCtrl(parent, id, pos, size, style, szBackend)
# tested with Python25 and wxPython28
# by  vegaseat   12nov2008

import wx
import wx.media
import wx.lib.filebrowsebutton



class MyFrame(wx.Frame):
    def __init__(self, parent, mytitle, mysize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle, 
            size=mysize)
        self.panel = wx.Panel(self, wx.ID_ANY)
        tan = '#D2B48C'
        self.panel.SetBackgroundColour('tan')
        
        # check if the media control is implemented
        try:
            self.mc = wx.media.MediaCtrl(self.panel)
        except NotImplementedError:
            self.Destroy()
        
        # this file browser masked to look for media files
        mask = "*.mp3;*.mpg;*.mid;*.wav;*.au;*.avi" 
        self.fbb = wx.lib.filebrowsebutton.FileBrowseButton(self.panel,
            labelText="Select a media file:", fileMask=mask)
        load_button = wx.Button(self.panel, wx.ID_ANY, " Load ")
        load_button.SetToolTip(wx.ToolTip("Load media file"))
        self.Bind(wx.EVT_BUTTON, self.onFileLoad, load_button)
        
        # layout ...
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.fbb, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(load_button, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        # also creates a border space
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer, 1, wx.EXPAND|wx.ALL, border=10)
        vsizer.Add(self.mc, 5, wx.EXPAND|wx.ALL, border=10)
        self.panel.SetSizer(vsizer)
        
        # this activates the full player with its controls
        # this works on Vista too
        self.mc.ShowPlayerControls()
        
    def onFileLoad(self, event):
        self.path = self.fbb.GetValue()
        self.mc.Load(self.path)
        
    def onPlay(self):
        self.mc.Play()


app = wx.App(0)
# create a MyFrame instance and show the frame
MyFrame(None, "Simple Media Player", (600, 400)).Show()
app.MainLoop()