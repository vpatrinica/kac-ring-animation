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
import wx.lib.fancytext as fancytext

##################################################################################################################

class Superscript(wx.Panel):
    """
    This class is used for creating the superscript graphics effect
    for the powers of 2.
    """
    def __init__(self, parent, id):
        """
        The constructor of the superscript class
        @param self: default self parameter
        @param parent: the parent of the superscript class(a wx.Window child)
        @param id: the id of the wx object    
        """
        wx.Panel.__init__(self, parent, -1)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    

    def OnPaint(self, event):
        """
        The method overrides the default OnPaint behavior
        If the wx.EVT_PAINT event is triggered then this method catches and
        displays the current value of the power of 2.
        @param self: default self parameter
        @param event: the event which is being caught and handled by the method
        """
        value = self.GetParent().GetValue()
        self.ClearBackground()
	tryDC = wx.ClientDC(self)
        tryDC.BeginDrawing()
	tryDC.Clear()
	tryDC.EndDrawing()
        supDC = wx.ClientDC(self)
        supDC.BeginDrawing()

        xml_str1 = ('<font size="10" style="italic" family="swiss" color="black" weight="bold" >'
'2<sup>')
        
        xml_str2 = ('</sup></font>')
        xml_str = xml_str1+str(value)+xml_str2
        w, h = fancytext.GetExtent(xml_str, supDC)
        fancytext.RenderToDC(xml_str, supDC, 5, 5)
        supDC.EndDrawing()
        event.Skip()
        
    def SetValue(self, new_value):
        """
        The setter method of the class, which repaints the region so that the new value is diplayed
        @param self: default self parameter
        @param new_value: integer value between 4 and 20, which is the new value of the exponent
        """
        self.ClearBackground()
	tryDC = wx.ClientDC(self)
        tryDC.BeginDrawing()
	tryDC.Clear()
	tryDC.EndDrawing()

        supDC = wx.ClientDC(self)
        supDC.BeginDrawing()
        
        xml_str1 = ('<font size="10" style="italic" family="swiss" color="black" weight="bold" >'
'2<sup>')
        
        xml_str2 = ('</sup></font>')
        xml_str = xml_str1+str(new_value)+xml_str2
        w, h = fancytext.GetExtent(xml_str, supDC)
        
        fancytext.RenderToDC(xml_str, supDC, 5, 5)
        supDC.EndDrawing()



