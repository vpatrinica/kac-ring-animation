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
from numpy import *
from PIL import Image
from scipy.misc import toimage
import Utils

##################################################################################################################



class Canvas(wx.Panel):
    """
    This class is used to display the images-frames of the animation for the Kac's Ring Model
    """
    def __init__(self, parent, id, app_args):
        """
        The constructor of the Canvas class
        @param self: default self parameter
        @param parent: the parent of the Canvas class(a wx.Window child) instance
        @param id: the id of the wx object
        @param app_args: default initial values of the density, pixel array, 
        """
        (sideX, sideY) = wx.DisplaySize()
        if sideX < sideY:
            aux = sideX
            sideX = sideY
            sideY = aux

        wx.Panel.__init__(self, parent, -1, size = (sideY, sideY))
        #(self.c, self.lut, self.k, self.rindex, self.sindex) = app_args


    def OnRepaint(self):
        """
        A method which handles the refreshing of the panel
        @param self: the default self parameter
        """
        self.image = wx.EmptyBitmap(0,0)
        mainDC = wx.ClientDC(self)
        mainDC.BeginDrawing()
        mainDC.DrawBitmap(self.image, 5, 5)
        mainDC.EndDrawing()
        
    def OnNextFrame(self, event):
        """
        @param self: the default self parameter
        @param event: the event of computing the next frame 
        """
        for i in range(self.k,0,-1):
            self.c[i-1,:2**(i-1)] = mean(self.c[i,:2**i].reshape(-1,2),1)
        im = self.c[self.rindex, self.sindex]
        I = toimage(im, cmin=0, cmax=255)
        I.putpalette(self.lut)

        data = Utils.PILtoImage(I, 1)
        
        self.image = wx.BitmapFromImage(data)
        mainDC = wx.ClientDC(self)
        mainDC.BeginDrawing()
        mainDC.DrawBitmap(self.image, 5, 5)
        mainDC.EndDrawing()
        
        
        m = 254.0*(self.c[self.k+1,:]>128)
        self.c[self.k,:] = abs(self.c[self.k,:]-m)
        
        x = self.c[self.k+1,0]
        self.c[self.k+1,:-1] = self.c[self.k+1,1:]
        self.c[self.k+1,-1] = x

        event.Skip()

    def OnBackFrame(self, event):
        """
        @param self: the default self parameter
        @param event: the event of computing the previous frame 
        """
        x = self.c[self.k+1, -1]
        self.c[self.k+1, 1:] = self.c[self.k+1,:-1]
        self.c[self.k+1,0] = x
        
        
        m = 254.0*(self.c[self.k+1,:]>128)
        self.c[self.k,:] = abs(self.c[self.k,:]-m)
        
        for i in range(self.k,0,-1):
            self.c[i-1,:2**(i-1)] = mean(self.c[i,:2**i].reshape(-1,2),1)

        im = self.c[self.rindex, self.sindex]
        I = toimage(im, cmin=0, cmax=255)
        I.putpalette(self.lut)

        data = Utils.PILtoImage(I, 1)
        
        self.image = wx.BitmapFromImage(data)
        mainDC = wx.ClientDC(self)
        mainDC.BeginDrawing()
        mainDC.DrawBitmap(self.image, 5, 5)
        mainDC.EndDrawing()

        event.Skip()

        
        
