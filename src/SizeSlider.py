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
import SuperScript

##################################################################################################################


class SizeSlider(wx.Panel):
    """
    This class is used to create a slider like widget, for the size parameter modifier
    """
    def __init__(self, parent, id, def_value):
        """
        The constructor of the SizeSlider class
        @param self: default self parameter
        @param parent: the parent of the SizeSlider class(a wx.Window child)
        @param id: the id of the wx object    
        """

        wx.Panel.__init__(self, parent, -1)
        self.slider = wx.Slider(self, -1, 0, 4, 20, style = wx.SL_HORIZONTAL)
       
        self.text = wx.StaticText(self, -1, "Ring size:         ")
        self.value = SuperScript.Superscript(self, -1)
        self.panel_dummy = wx.Panel(self, -1)
        self.__set_properties_(def_value)
        self.__do_layout_()
        self.slider.Bind(wx.EVT_SLIDER, self.value.OnPaint)
        
    def __set_properties_(self, default_value):
        """
        The method which takes care to set the necessary customizabe properties to the
        components of the widget
        @param self: the default self parameter
        @param default_value: the default value of the exponent(size)
        """
        self.value.SetValue(str(default_value))
        font1 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        self.text.SetFont(font1)

        self.slider.SetValue(default_value)

    def __do_layout_(self):
        """
        A method which takes care of the layout of the components of the widget(sizers and inheritance)
        @param self: the default self parameter
        """
        size_widget_sizer = wx.BoxSizer(wx.VERTICAL)
        size_widget_sizer_horiz = wx.BoxSizer(wx.HORIZONTAL)
        
        size_widget_sizer.Add(self.slider, 1, wx.EXPAND)
        
        size_widget_sizer_horiz.Add(self.text, 1, wx.EXPAND)
        size_widget_sizer_horiz.Add(self.value, 1, wx.EXPAND)
        
        size_widget_sizer.Add(size_widget_sizer_horiz, 1, wx.EXPAND)
        size_widget_sizer.Add(self.panel_dummy, 1, wx.EXPAND)
        self.SetSizer(size_widget_sizer)
        
    def SetValue(self, new_value):
        """
        The setter method of the class, which modifies the value of the size of the ring
        @param self: the default self parameter
        @param new_value: the new value of the exponent(size of the ring)
        """
        self.slider.SetValue(new_value)
        self.value.SetValue(new_value)

    def GetValue(self):
        """
        The getter method of the SizeSlider class
        @param self: the default self parameter
        @return: integer between 4 and 20 which represents the current size
        """
        return self.slider.GetValue()


