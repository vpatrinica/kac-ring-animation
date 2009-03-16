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

##################################################################################################################



class SpeedSlider(wx.Panel):
    """
    This class creates the custom widget for the speed parameter, which includes
    a slider in frames per second scale, with correspondent ticks and label
    """
    def __init__(self, parent, id, def_value):
        """
        The constructor of the SpeedSlider class
        @param self: default self parameter
        @param parent: the parent of the SpeedSlider class(a wx.Window child) instance
        @param id: the id of the wx object
        @param def_value: default initial value of the speed
        """

        wx.Panel.__init__(self, parent, -1)
        self.slider = wx.Slider(self, -1, 3, 1, 100, style = wx.SL_HORIZONTAL)
        self.value = wx.TextCtrl(self, -1)
        self.text = wx.StaticText(self, -1, "Speed:              ")
        
        self.panel_dummy = wx.Panel(self, -1)

        self.slider.Bind(wx.EVT_SLIDER, self.OnValueChanged)
        self.__set_properties_(def_value)
        self.__do_layout_()
        
    def __set_properties_(self, default_value):
        """
        The method which takes care to set the necessary customizabe properties to the
        components of the widget
        @param self: the default self parameter
        @param default_value: the default value of the density, integer from 1 to 100 
        """
        
        font1 = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        self.value.SetFont(font1)
        self.text.SetFont(font1)
        self.slider.SetValue(default_value)
        self.value.ChangeValue(str(default_value))
        self.value.SetEditable(0)


        
    def __do_layout_(self):
        """
        A method which takes care of the layout of the components of the widget(sizers and inheritance)
        @param self: the default self parameter
        """

        speed_widget_sizer = wx.BoxSizer(wx.VERTICAL)
        speed_widget_sizer_horiz = wx.BoxSizer(wx.HORIZONTAL)
        
        speed_widget_sizer.Add(self.slider, 1, wx.EXPAND)

        speed_widget_sizer_horiz.Add(self.text, 1, wx.EXPAND)
        speed_widget_sizer_horiz.Add(self.value, 1, wx.EXPAND)
        
        
        speed_widget_sizer.Add(speed_widget_sizer_horiz, 1, wx.EXPAND)
        speed_widget_sizer.Add(self.panel_dummy, 1, wx.EXPAND)
  
        self.SetSizer(speed_widget_sizer)
        
    def OnValueChanged(self, event):
        """
        The function which handles the event of user-changed value of the speed slider
        @param self: default self parameter
        @param event: the event which is handled by this function 
        """
        value = self.slider.GetValue()
        self.value.ChangeValue(str(value))
        event.Skip()
        
    def SetValue(self, new_value):
        """
        The setter method of the class, which modifies the value of the speed of the animation
        @param self: the default self parameter
        @param new_value: the new value of the speed, integer between 1 and 100
        """
        self.value.ChangeValue(str(new_value))
        self.slider.SetValue(new_value)        
        

    def GetValue(self):
        """
        The getter method of the SpeedSlider class
        @param self: the default self parameter
        @return: integer between 1 and 100 which represents the current speed
        """
        return self.slider.GetValue()
    
