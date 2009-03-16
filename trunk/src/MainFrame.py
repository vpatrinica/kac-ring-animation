#!/usr/bin/env python
##################################################################################################################
##                                                                                                               #
##   Animation.py illustrates the behaviour of the Kac's Ring Model                                              #
##                                                                                                               #
##   Copyright (C) 2008  Patrinica Vitalie, Prof. Dr. Marcel Oliver, Jacobs University Bremen                    #
##                                                                                                               #
##   This program is free software: you can redistribute it and/or modify it under the terms                     #
##   of the GNU General Public License as published by the Free Software Foundation, version 3.                  #
##                                                                                                               #
##   This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;                   #
##   without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                   #
##   See the GNU General Public License for more details.                                                        #
##                                                                                                               #
##   You should have received a copy of the GNU General Public License along with this program.                  #
##   If not, see <http://www.gnu.org/licenses/>.                                                                 #
##################################################################################################################
################################ IMPORT LIST #####################################################################
##################################################################################################################

import wx

import Canvas, SpeedSlider, DensitySlider, SizeSlider, SuperScript, Utils

##################################################################################################################


class MainFrame(wx.Frame):
    """
    This class is used to create the main frame of the program
    """
    def __init__(self, parent, ID, title, prec_args):
        """
        The constructor of the Exit_Frame class
        @param self: default self parameter
        @param parent: the parent of the Exit_Frame class(a wx.Window child) instance
        @param ID: the id of the wx object
        @param title: the title of the main frame
        @param prec_args: the precomputed values necessary for the first image frame, the array which
        retains the colours of the pixels, the colour pallette, the bounds rindex, sindex
        """

	"""
	Changed! def_speed, speed from 100 fps to 5 fps
		def_size, size from 18 to 10
	"""

        sizeFullScreen = wx.DisplaySize()
        wx.Frame.__init__(self, parent, ID, title, size=sizeFullScreen)
        self.SetIcon(wx.Icon(u'../pngs/iconKacRing.ico', wx.BITMAP_TYPE_ICO))
        self.def_speed = 3
        
        self.def_density = 0.04
        self.def_size = 10
        self.def_colour = wx.Color(255, 0, 0)
        self.speed = 3
        self.density = 0.04
        self.size = 10
        self.colour = wx.Color(255, 0, 0)

        self.main_panel = wx.Panel(self, -1)       
        self.control_panel = wx.Panel(self, -1)
        
        self.panel_canvas = Canvas.Canvas(self.main_panel, -1, prec_args)
        
        
        #self.panel_dummy_1 = wx.Panel(self.control_panel, -1)        
        self.bitmap_button_PlayBack = wx.BitmapButton(self.control_panel, -1, wx.Bitmap("../pngs/control_rewind.png", wx.BITMAP_TYPE_ANY))
        #self.panel_dummy_2 = wx.Panel(self.control_panel, -1)

        self.bitmap_button_FrameBack = wx.BitmapButton(self.control_panel, -1, wx.Bitmap("../pngs/control_back.png", wx.BITMAP_TYPE_ANY))
        #self.panel_dummy_3 = wx.Panel(self.control_panel, -1)

        self.bitmap_button_Stop = wx.BitmapButton(self.control_panel, -1, wx.Bitmap("../pngs/control_stop.png", wx.BITMAP_TYPE_ANY))
        #self.panel_dummy_4 = wx.Panel(self.control_panel, -1)

        self.bitmap_button_FrameNext = wx.BitmapButton(self.control_panel, -1, wx.Bitmap("../pngs/control_play.png", wx.BITMAP_TYPE_ANY))
        #self.panel_dummy_5 = wx.Panel(self.control_panel, -1)

        self.bitmap_button_PlayNext = wx.BitmapButton(self.control_panel, -1, wx.Bitmap("../pngs/control_fastforward.png", wx.BITMAP_TYPE_ANY))
        #self.panel_dummy_6 = wx.Panel(self.control_panel, -1)



        self.panel_dummy_7 = wx.Panel(self.control_panel, -1)
        self.button_Restart = wx.Button(self.control_panel, -1, "    Restart animation    ")
        self.panel_dummy_8 = wx.Panel(self.control_panel, -1)


        self.panel_dummy_9 = wx.Panel(self.control_panel, -1)
        self.button_ResetDefault = wx.Button(self.control_panel, -1, "    Restore defaults     ")
        self.panel_dummy_10 = wx.Panel(self.control_panel, -1)


        self.panel_dummy_11 = wx.Panel(self.control_panel, -1)
        self.slider_speed = SpeedSlider.SpeedSlider(self.control_panel, -1, self.def_speed)
        self.panel_dummy_12 = wx.Panel(self.control_panel, -1)


        self.panel_dummy_13 = wx.Panel(self.control_panel, -1)
        self.slider_density = DensitySlider.DensitySlider(self.control_panel, -1, self.def_density)
        self.panel_dummy_14 = wx.Panel(self.control_panel, -1)


        self.panel_dummy_15 = wx.Panel(self.control_panel, -1)
        self.slider_size = SizeSlider.SizeSlider(self.control_panel, -1, self.def_size)
        self.panel_dummy_16 = wx.Panel(self.control_panel, -1)


        self.panel_dummy_17 = wx.Panel(self.control_panel, -1)
        self.label_colour = wx.StaticText(self.control_panel, -1, "Initial colour:")

        self.colour_picker = wx.ColourPickerCtrl(self.control_panel, style=wx.CLRP_DEFAULT_STYLE|wx.CLRP_USE_TEXTCTRL|wx.CLRP_SHOW_LABEL)
        

        self.panel_dummy_18 = wx.Panel(self.control_panel, -1)

        self.__set_properties()
        self.__do_layout()

        tid_forward = wx.NewId()
        self.forwtimer = wx.Timer(self, tid_forward)

        tid_backward = wx.NewId()
        self.backtimer = wx.Timer(self, tid_backward)
        
        self.Bind(wx.EVT_TIMER, self.panel_canvas.OnNextFrame, id = tid_forward)
        self.Bind(wx.EVT_TIMER, self.panel_canvas.OnBackFrame, id = tid_backward)
        
        self.bitmap_button_PlayNext.Bind(wx.EVT_BUTTON, self.OnPlayNext)
        self.bitmap_button_PlayBack.Bind(wx.EVT_BUTTON, self.OnPlayBack)
        self.bitmap_button_Stop.Bind(wx.EVT_BUTTON, self.OnStop)
        
        self.bitmap_button_FrameNext.Bind(wx.EVT_BUTTON, self.OnFrameNext)
        self.bitmap_button_FrameBack.Bind(wx.EVT_BUTTON, self.OnFrameBack)

        self.button_Restart.Bind(wx.EVT_BUTTON, self.OnRestart)
        self.button_ResetDefault.Bind(wx.EVT_BUTTON, self.OnResetDefault)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
    def SetSpeed(self):
        """
        The setter method for the speed slider
        @param self: the default self parameter
        """
        self.speed = self.GetSpeed()
        return

    def GetSpeed(self):
        """
        The getter method for the speed slider
        @param self: the default self parameter
        @return: the speed of the animation
        """
        return self.slider_speed.GetValue()
    
    def OnPlayNext(self, event):
        """
        The method which handles the forward timer event
        @param self: the default self parameter
        @param event: the event of computing the next frames
        """
        self.backtimer.Stop()
        self.forwtimer.Start(1000.0/float(self.speed))
        event.Skip()

    def OnPlayBack(self, event):
        """
        The method which handles the backward timer event
        @param self: the default self parameter
        @param event: the event of computing the previous frames
        """
        self.forwtimer.Stop()
        self.backtimer.Start(1000.0/float(self.speed))
        event.Skip()
        
    def OnStop(self, event):
        """
        The method which handles the stop timer event
        @param self: the default self parameter
        @param event: the event of stopping the animation 
        """
        self.forwtimer.Stop()
        self.backtimer.Stop()
        event.Skip()
        
    def OnFrameNext(self, event):
        """
        The method which handles the next frame button event
        @param self: the default self parameter
        @param event: the event of computing the next frame
        """
        self.backtimer.Stop()
        self.forwtimer.Stop()
        self.panel_canvas.OnNextFrame(event)
        event.Skip()

    def OnFrameBack(self, event):
        """
        The method which handles the back frame button event
        @param self: the default self parameter
        @param event: the event of computing the previous frame
        """
        self.forwtimer.Stop()
        self.backtimer.Stop()
        self.panel_canvas.OnBackFrame(event)
        event.Skip()


    def OnRestart(self, event):
        """
        The method which handles the button event of the restart button
        @param self: the default self parameter
        @param event: the user triggered event of the button restart handled by the method
        """
        self.forwtimer.Stop()
        self.backtimer.Stop()
        (sizeX, sizeY) = wx.DisplaySize()
        
        self.SetSpeed()
        self.SetDensity()
        self.SetSize()
        self.SetColour()
        
        new_parameters = (self.density, self.size, self.colour)
        restart_args = Utils.InitialComputation(min([sizeX]+[sizeY])-20, new_parameters)

        (self.panel_canvas.c, self.panel_canvas.lut, self.panel_canvas.k, self.panel_canvas.rindex, self.panel_canvas.sindex) = restart_args
        self.panel_canvas.OnRepaint()
        self.Refresh()
        event.Skip()

    def OnResetDefault(self, event):
        """
        The method which handles the button event of the reset defaults button
        @param self: the default self parameter
        @param event: the user triggered event of the button reset defaults handled by the method
        """
        self.speed = self.def_speed
        self.density = self.def_density
        self.size = self.def_size
        self.colour = self.def_colour

        self.slider_speed.SetValue(self.speed)
        self.slider_density.SetValue(self.density)
        self.slider_size.SetValue(self.size)
        self.colour_picker.SetColour(self.colour)
        event.Skip()
    

    def GetColour(self):
        """
        The getter method for the colour widget
        @param self: the default self parameter
        @return: the initial colour of the animation
        """
        new_colour = self.colour_picker.GetColour()
        return new_colour
    
    def SetColour(self):
        """
        The setter method for the colour widget
        @param self: the default self parameter
        """
        self.colour = self.GetColour()
        return
    
    def GetDensity(self):
        """
        The getter method for the density slider
        @param self: the default self parameter
        @return: the density of the markers
        """
        new_density = float(self.slider_density.GetValue())
        return new_density

    def SetDensity(self):
        """
        The setter method for the density slider
        @param self: the default self parameter
        """
        self.density = self.GetDensity()
        return

    def GetSize(self):
        """
        The getter method for the size slider
        @param self: the default self parameter
        @return: the size of the Kac's Ring
        """
        new_size = self.slider_size.GetValue()
        return new_size
    
    def SetSize(self):
        """
        The setter method for the size slider
        @param self: the default self parameter
        """
        self.size = self.GetSize()
        return
   
    def OnCloseWindow(self, event):
        """
        The handler method of the closing of the main frame event
        @param self: the default self parameter
        @param event: the event handled by the method
        """
    #dialog to verify exit (including menuExit)
    #the cleanup is no longer forced, the core seems not to dump anymore :)
        dlg = wx.MessageDialog(self, "Exit Animation?", "Exit", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.forwtimer.Stop()
            self.backtimer.Stop()
            children = self.GetChildren()
            for child in children:
                #print child
                child.Destroy()
                #del child
                dlg.Destroy()
                self.Destroy()
                #del self
        else:	
            dlg.Destroy()

    def __set_properties(self):
        """
        The method which takes care to set the necessary customizabe properties to the
        components of the main frame
        @param self: the default self parameter 
        """

        self.SetTitle("Kac Ring Animation")
        self.bitmap_button_PlayBack.SetSize(self.bitmap_button_PlayBack.GetBestSize())
        self.bitmap_button_FrameBack.SetSize(self.bitmap_button_FrameBack.GetBestSize())
        self.bitmap_button_Stop.SetSize(self.bitmap_button_Stop.GetBestSize())
        self.bitmap_button_FrameNext.SetSize(self.bitmap_button_FrameNext.GetBestSize())
        self.bitmap_button_PlayNext.SetSize(self.bitmap_button_PlayNext.GetBestSize())
        self.button_Restart.SetSize(self.button_Restart.GetBestSize())
        self.button_ResetDefault.SetSize(self.button_ResetDefault.GetBestSize())
        font1 = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        self.button_Restart.SetFont(font1)
        self.button_ResetDefault.SetFont(font1)
        self.label_colour.SetFont(font1)
        self.colour_picker.SetPickerCtrlProportion(1)
        self.colour_picker.GetTextCtrl().SetFont(font1)
        self.colour_picker.SetColour("red")
        self.slider_speed.SetFont(font1)
        

    def __do_layout(self):
        """
        A method which takes care of the layout of the components of the main frame(sizers and inheritance)
        @param self: the default self parameter
        """
        sizeFullScreen = wx.DisplaySize()
        (size_X, size_Y) = sizeFullScreen

        if size_X < size_Y:
            aux = size_X-10
            size_X = size_Y-10
            size_Y = aux
	else:
	    size_X = size_X - 10
	    size_Y = size_Y - 10
        
        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(self.main_panel, size_Y/((size_X-size_Y)*1.0), wx.EXPAND, 0)
        sizer_main.Add(self.control_panel, 1, wx.EXPAND)
        
        sizer_canvas = wx.BoxSizer(wx.HORIZONTAL)
        sizer_controls = wx.BoxSizer(wx.VERTICAL)

        sizer_play_buttons = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_restart = wx.BoxSizer(wx.HORIZONTAL)
        sizer_reset = wx.BoxSizer(wx.HORIZONTAL)

        sizer_speed = wx.BoxSizer(wx.HORIZONTAL)
        sizer_density = wx.BoxSizer(wx.HORIZONTAL)
        sizer_size = wx.BoxSizer(wx.HORIZONTAL)
        sizer_colour = wx.BoxSizer(wx.HORIZONTAL)
        sizer_colour_vertical = wx.BoxSizer(wx.VERTICAL)
        #sizer_speed_vertical = wx.BoxSizer(wx.VERTICAL)
        
        sizer_canvas.Add(self.panel_canvas, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
        
        #sizer_play_buttons.Add(self.panel_dummy_1, 1, wx.EXPAND, 0)
        sizer_play_buttons.Add(self.bitmap_button_PlayBack, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        #sizer_play_buttons.Add(self.panel_dummy_2, 1, wx.EXPAND, 0)
        sizer_play_buttons.Add(self.bitmap_button_FrameBack, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        #sizer_play_buttons.Add(self.panel_dummy_3, 1, wx.EXPAND, 0)
        sizer_play_buttons.Add(self.bitmap_button_Stop, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        #sizer_play_buttons.Add(self.panel_dummy_4, 1, wx.EXPAND, 0)
        sizer_play_buttons.Add(self.bitmap_button_FrameNext, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        #sizer_play_buttons.Add(self.panel_dummy_5, 1, wx.EXPAND, 0)
        sizer_play_buttons.Add(self.bitmap_button_PlayNext, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        #sizer_play_buttons.Add(self.panel_dummy_6, 1, wx.EXPAND, 0)
        
        sizer_controls.Add(sizer_play_buttons, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)


        sizer_restart.Add(self.panel_dummy_7, 1, wx.EXPAND, 0)
        sizer_restart.Add(self.button_Restart, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 25)
        sizer_restart.Add(self.panel_dummy_8, 1, wx.EXPAND, 0)

        sizer_controls.Add(sizer_restart, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)


        sizer_reset.Add(self.panel_dummy_9, 1, wx.EXPAND, 0)
        sizer_reset.Add(self.button_ResetDefault, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 25)
        sizer_reset.Add(self.panel_dummy_10, 1, wx.EXPAND, 0)
        
        sizer_controls.Add(sizer_reset, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)

        #sizer_speed_vertical.Add(self.label_speed, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_speed.Add(self.panel_dummy_11, 1, wx.EXPAND, 0)
        sizer_speed.Add(self.slider_speed, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_speed.Add(self.panel_dummy_12, 1, wx.EXPAND, 0)


        sizer_controls.Add(sizer_speed, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)


        sizer_density.Add(self.panel_dummy_13, 1, wx.EXPAND, 0)
        sizer_density.Add(self.slider_density, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_density.Add(self.panel_dummy_14, 1, wx.EXPAND, 0)

        sizer_controls.Add(sizer_density, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)


        sizer_size.Add(self.panel_dummy_15, 1, wx.EXPAND, 0)
        sizer_size.Add(self.slider_size, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_size.Add(self.panel_dummy_16, 1, wx.EXPAND, 0)

        sizer_controls.Add(sizer_size, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_colour_vertical.Add(self.label_colour, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_colour_vertical.Add(self.colour_picker, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        sizer_colour.Add(self.panel_dummy_17, 1, wx.EXPAND, 0)
        sizer_colour.Add(sizer_colour_vertical, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_colour.Add(self.panel_dummy_18, 1, wx.EXPAND, 0)

        sizer_controls.Add(sizer_colour, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)


        self.control_panel.SetAutoLayout(True)
        self.control_panel.SetSizer(sizer_controls)
        #sizer_3_copy.Fit(self.control_panel)
        #sizer_3_copy.SetSizeHints(self.control_panel)
        #sizer_2.Add(self.panel_2, 1, wx.EXPAND, 0)
        #self.SetAutoLayout(True)
        self.SetSizer(sizer_main)
        #sizer_2.Fit(self)
        #sizer_2.SetSizeHints(self)
        self.Layout()
  

