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

import MainFrame
import Utils

##################################################################################################################





class MyApp(wx.App):
    """
    A simple class for the application
    """
    def OnInit(self):
        """
        The overriden default OnInit method of the class wx.App
        """
        wx.InitAllImageHandlers()
        (sizeX, sizeY) = wx.DisplaySize()
        start_args = (0.04, 10, wx.Color(255, 0, 0))
        App_args = Utils.InitialComputation(min([sizeX]+[sizeY])-20, start_args)
        self._MainFrame = MainFrame.MainFrame(None, -1, "An image on a panel", App_args)
        self._MainFrame.ShowFullScreen(True)
        self.SetTopWindow(self._MainFrame)
        return True


"""
The mainloop of the application and test.
"""
if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
