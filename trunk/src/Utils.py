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

from numpy import *
from numpy.random import rand
from math import hypot, atan2
from PIL import Image

import wx

##################################################################################################################



def InitialComputation(size, basic_args):
    """
    This routine performs the routine of calculation the array of the pixels of the first
    frame.
    @param size: the size of the biggest square which fits in the current display
    @param basic_args: the triplet of parameters of the following form:
    (density, number of coarsegraining B{rings})
    @return: the computed values necessary for the first image frame, the array which
    retains the colours of the pixels, the colour pallette, the bounds rindex, sindex
    """

    random.seed(1)

    (mu, k, colour) = basic_args


    N = 2**k
    
    """
    B{N}: Size of Kac ring (=outermost ring)
    """

    T = N
    """
    B{T}: Number of time steps
    """

    """
    B{mu}: Probability that an edge carries a marker
    """
    
    nu = 0.0
    """
    B{nu}: Probability that a site is initially black
    """

    P = size
    """
    B{P}: Number of pixels in image
    """

    c = zeros((k+3,N), dtype=float)
    """ White """
    c[k+2,1] = 127
    c[k+2,0] = 255
    """ Black """

    c[k+1,:] = 127 + 128*array(rand(N) < mu*ones(N), dtype=float) 
    c[k,:]   = 254 * array(rand(N) < nu*ones(N), dtype=float)

    rindex = empty((P,P), dtype=intp)
    sindex = empty((P,P), dtype=intp)

    for i in range(P):
        for j in range(P):
            x = i-P/2.0
            y = j-P/2.0
            r = hypot (x,y)
            s = atan2 (y,x) + pi
            rindex[i,j] = intp ((k+1)*r/(0.46*P))
            if rindex[i,j] > k:
                if 0.47*P < r < 0.49*P:
                    s = s - pi/N
                    if s < 0.0:
                        s = s + 2*pi
                    rindex[i,j] = k+1
                    sindex[i,j] = min(N-1, intp(N*s/(2*pi)))
                elif r > 0.5*P:
                    rindex[i,j] = k+2
                    sindex[i,j] = 1
                else:
                    rindex[i,j] = k+2
                    sindex[i,j] = 0
            else:
                sindex[i,j] = min(2**rindex[i,j]-1,intp (2**rindex[i,j]*s/(2*pi)))


    
    red_th = colour.Red()
    green_th =colour.Green()
    blue_th = colour.Blue()
    

    def low_pass(i, low_pass_th):
        """
        Auxiliary function which has the shape of the spectrum of a low-pass filter in the
        log scale
        @param i: the index of the colour pallete element, integer from the interval 0..255
        @param low_pass_th: the maximal value of function
        @return: the colour of the given element
        """
        if i<64:
            return int(float((255 - low_pass_th+1)*i)/64.0) + low_pass_th
        elif i<128:
            return 255
        else:
            return int(float((low_pass_th+1)*(255-i))/128.0 -1)
        
    def band_pass(i, band_pass_th, low_pass_th):
        """
        Auxiliary function which has the shape of the spectrum of a band-pass filter in the
        log scale
        @param i: the index of the colour pallete element, integer from the interval 0..255
        @param band_pass_th: the initial value of function, i.e. when i = 0
        @param low_pass_th: the maximal value of function
        @return: the colour of the given element
        """
        if i<64:
            return int(float((low_pass_th - band_pass_th+1)*i)/64.0) + band_pass_th
        elif i<192:
            return low_pass_th
        else:
            return int(float((low_pass_th - band_pass_th+1)*(255-i)/64.0))

    def high_pass(i, high_pass_th, low_pass_th):
        """
        Auxiliary function which has the shape of the spectrum of a band-pass filter in the
        log scale
        @param i: the index of the colour pallete element, integer from the interval 0..255
        @param high_pass_th: the initial value of function, i.e. when i = 0
        @param low_pass_th: the maximal value of function
        @return: the colour of the given element
        """
        if i<64:
            return high_pass_th
        elif i<128:
            return int(float((low_pass_th - high_pass_th+1)*(i-64))/64.0) + high_pass_th
        else:
            return low_pass_th
        
    def decide(th, i):
        """
        The function which selects which transformation to apply to the pallete,
        whether low-pass or band-pass etc.
        @param th: the threshold from which the low-pass is appied
        @param i: the index of the pixel
        @return: the value of the transformation
        """
        if th>=192: return low_pass(i, th)
        if th<64: return high_pass(i, th, 255)
        return band_pass(i, th, 255)
    
    def list_col2(i, red_t, green_t, blue_t):
        """
        The function creates the pallete RGB for the image
        @param i: the index of the pixel
        @param red_t: the threshold for the red component
        @param green_t: the threshold for the green component
        @param blue_t: the threshold for the blue component
        @return: the triplet of the RGB values for the given index
        """
        return (decide(red_t, i), decide(green_t, i), decide(blue_t, i))

    def list_col(i):
        """
        @param i: the index of the pixel
        @return: the RGB triplet of the given pixel
        """
        if red_th >= green_th:
            if green_th >=blue_th:
                return [low_pass(i, red_th), band_pass(i, green_th, 255), high_pass(i, blue_th, 255)]
            else:
                if red_th>=blue_th:
                    return [low_pass(i, red_th), high_pass(i, green_th, 255), band_pass(i, blue_th, 255)]
                else:
                    return [band_pass(i, red_th, 255), high_pass(i, green_th, 255), low_pass(i, blue_th)]
        else:
            if red_th>=blue_th:
                return [band_pass(i, red_th, 255), low_pass(i, green_th), high_pass(i, blue_th, 255)]
            else:
                if green_th>=blue_th:
                    return [high_pass(i, red_th, 255), low_pass(i, green_th), band_pass(i, blue_th, 255)]
                else:
                    return [high_pass(i, red_th, 255), band_pass(i, green_th, 255), low_pass(i, blue_th)]

    
    lut = [] 
    for i in range(255):
        #lut.extend(list_col2(i, red_th, green_th, blue_th))
        lut.extend(list_col(i))
    lut.extend([0,0,0])  # Black


    return (c, lut, k, rindex, sindex)


def PILtoImage(pil, alpha=True):
    """
    A function which converts a PIL Image to wx.Image
    @param pil: the input PIL image
    @param alpha: the alpha channel
    @return: the wx.Image
    """
    if alpha:
        image = apply(wx.EmptyImage, pil.size)
        image.SetData(pil.convert("RGB").tostring())
        image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
    else:
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        new_image = pil.convert('RGB')
        data = new_image.tostring()
        image.SetData(data)
    return image


