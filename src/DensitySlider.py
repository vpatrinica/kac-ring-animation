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
from math import log, exp

##################################################################################################################

class DensitySlider(wx.Panel):
    """
    This class creates the custom widget for the marker density parameter, which includes
    a slider in logarithmical scale, and a panel for displaying the current marker density
    """
    def __init__(self, parent, id, def_value):
        """
        The constructor of the DensitySlider class
        @param self: default self parameter
        @param parent: the parent of the DensitySlider class(a wx.Window child) instance
        @param id: the id of the wx object
        @param def_value: default initial vaue of the density
        """

        wx.Panel.__init__(self, parent, -1)
        self.slider = wx.Slider(self, -1, 0, 0, 1000, style = wx.SL_HORIZONTAL)
       
        self.text = wx.StaticText(self, -1, "Marker density:")
        self.value = wx.TextCtrl(self, -1)
        self.panel_dummy = wx.Panel(self, -1)
        self.slider.Bind(wx.EVT_SLIDER, self.OnValueChanged)
        self.__set_properties_(def_value)
        self.__do_layout_()
        
    def __set_properties_(self, default_value):
        """
        The method which takes care to set the necessary customizabe properties to the
        components of the widget
        @param self: the default self parameter
        @param default_value: the default value of the density, float from 0 to 1 
        """
        self.value.SetValue(str(default_value))
        font1 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        font2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        self.text.SetFont(font1)
        self.value.SetFont(font1)
        self.slider.SetValue(int(log(default_value*1000+1)*1000/log(1001)))
        self.value.SetEditable(0)

        
    def __do_layout_(self):
        """
        A method which takes care of the layout of the components of the widget(sizers and inheritance)
        @param self: the default self parameter
        """
        density_widget_sizer = wx.BoxSizer(wx.VERTICAL)
        density_widget_sizer_horiz = wx.BoxSizer(wx.HORIZONTAL)
        
        density_widget_sizer.Add(self.slider, 1, wx.EXPAND)
        
        density_widget_sizer_horiz.Add(self.text, 1, wx.EXPAND)
        density_widget_sizer_horiz.Add(self.value, 1, wx.EXPAND)
        
        density_widget_sizer.Add(density_widget_sizer_horiz, 1, wx.EXPAND)
        density_widget_sizer.Add(self.panel_dummy, 1, wx.EXPAND)
        self.SetSizer(density_widget_sizer)
        
        
    def OnValueChanged(self, event):
        """
        The function which handles the event of user-changed value of the density slider
        @param self: default self parameter
        @param event: the event which is handled by this function 
        """
        value = self.slider.GetValue()
        new_value = (exp(value*log(1001)/1000) -1)/1000.0
        str_value = "%.3f" % new_value
        self.value.ChangeValue(str_value)
        event.Skip()
        
    def SetValue(self, new_value):
        """
        The setter method of the class, which modifies the value of the density of the markers
        @param self: the default self parameter
        @param new_value: the new value of the density of the markers
        """
        slider_value = int(log(new_value*1000+1)*1000/log(1001))
        self.slider.SetValue(slider_value)        
        converted_value = (exp(slider_value*log(1001)/1000) -1)/1000.0
        str_value = "%.3f" % converted_value
        self.value.ChangeValue(str_value)

    def GetValue(self):
        """
        The getter method of the DensitySlider class
        @param self: the default self parameter
        @return: integer between 0 and 1 which represents the current density
        """
        return float(self.value.GetValue())


