#!/usr/bin/env python


from numpy import *
from numpy.random import rand
from scipy.misc import toimage
from math import hypot, atan2, exp, log

import wx
import wx.lib.fancytext as fancytext
    
from PIL import Image

def InitialComputation(size, basic_args):
    random.seed(1)

    (mu, k, colour) = basic_args
    
         
    #k = 18           # number of coarsegraining "rings"
    N = 2**k          # Size of Kac ring (=outermost ring)
    T = N             # Number of time steps
    #mu = 0.04        # Probability that an edge carries a marker
    nu = 0.0          # Probability that a site is initially black
    P = size          # Number of pixels in image

    c = zeros((k+3,N), dtype=float)
    c[k+2,1] = 127    # White
    c[k+2,0] = 255    # Black

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
        if i<64:
            return int(float((255 - low_pass_th+1)*i)/64.0) + low_pass_th
        elif i<128:
            return 255
        #elif i<191:
        #    return int(float((low_pass_th+1)*(191-i))/64.0 -1)
        else:
            return int(float((low_pass_th+1)*(255-i))/128.0 -1)
        
    def band_pass(i, band_pass_th, low_pass_th):
        if i<64:
            return int(float((low_pass_th - band_pass_th+1)*i)/64.0) + band_pass_th
        elif i<192:
            return low_pass_th
        else:
            return int(float((low_pass_th - band_pass_th+1)*(255-i)/64.0))

    def high_pass(i, high_pass_th, low_pass_th):
        if i<64:
            return high_pass_th
        elif i<128:
            return int(float((low_pass_th - high_pass_th+1)*(i-64))/64.0) + high_pass_th
        else:
            return low_pass_th
    def decide(th, i):
        if th>=192: return low_pass(i, th)
        if th<64: return high_pass(i, th, 255)
        return band_pass(i, th, 255)
    
    def list_col2(i, red_t, green_t, blue_t):
        return (decide(red_t, i), decide(green_t, i), decide(blue_t, i))
    """
    def list_col(i):
        if red_th >= green_th:
            if green_th >=blue_th:
                return [low_pass(i, red_th), band_pass(i, green_th, red_th), high_pass(i, blue_th, red_th)]
            else:
                if red_th>=blue_th:
                    return [low_pass(i, red_th), high_pass(i, green_th, red_th), band_pass(i, blue_th, red_th)]
                else:
                    return [band_pass(i, red_th, blue_th), high_pass(i, green_th, blue_th), low_pass(i, blue_th)]
        else:
            if red_th>=blue_th:
                return [band_pass(i, red_th, green_th), low_pass(i, green_th), high_pass(i, blue_th, green_th)]
            else:
                if green_th>=blue_th:
                    return [high_pass(i, red_th, green_th), low_pass(i, green_th), band_pass(i, blue_th, green_th)]
                else:
                    return [high_pass(i, red_th, blue_th), band_pass(i, green_th, blue_th), low_pass(i, blue_th)]
        """
    def list_col(i):
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


    return (c,lut, k, rindex, sindex)


def piltoimage(pil,alpha=True):
    """Convert PIL Image to wx.Image."""
    if alpha:
        image = apply( wx.EmptyImage, pil.size )
        image.SetData( pil.convert( "RGB").tostring() )
        image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
    else:
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        new_image = pil.convert('RGB')
        data = new_image.tostring()
        image.SetData(data)
    return image


class Superscript(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, -1)
        self.Bind(wx.EVT_PAINT, self.OnRefresh)
    

    def OnPaint(self, evt):
        value = self.GetParent().GetValue()
        self.ClearBackground()
        supDC = wx.ClientDC(self)
        supDC.BeginDrawing()

        xml_str1 = ('<font size="18" style="italic" family="swiss" color="black" weight="bold" >'
'2<sup>')
        
        xml_str2 = ('</sup></font>')
        xml_str = xml_str1+str(value)+xml_str2
        w, h = fancytext.GetExtent(xml_str, supDC)
        fancytext.RenderToDC(xml_str, supDC, 5, 5)
        supDC.EndDrawing()
        evt.Skip()

    def OnRefresh(self, evt):
        self.SetValue(self.GetParent().GetValue())
        evt.Skip()
    def SetValue(self, new_value):
        self.ClearBackground()
        supDC = wx.ClientDC(self)
        supDC.BeginDrawing()
        
        xml_str1 = ('<font size="16" style="italic" family="swiss" color="black" weight="bold" >'
'2<sup>')
        
        xml_str2 = ('</sup></font>')
        xml_str = xml_str1+str(new_value)+xml_str2
        w, h = fancytext.GetExtent(xml_str, supDC)
        
        fancytext.RenderToDC(xml_str, supDC, 5, 5)
        supDC.EndDrawing()

class SizeSlider(wx.Panel):
    def __init__(self, parent, id, def_value):
        

        wx.Panel.__init__(self, parent, -1)
        self.slider = wx.Slider(self, -1, 0, 4, 20, style = wx.SL_HORIZONTAL)
       
        self.text = wx.StaticText(self, -1, "Ring size:")
        self.value = Superscript(self, -1)
        self.panel_dummy = wx.Panel(self, -1)
        self.__set_properties_(def_value)
        self.__do_layout_()
        self.slider.Bind(wx.EVT_SLIDER, self.value.OnPaint)
        
    def __set_properties_(self, default_value):
        self.value.SetValue(str(default_value))
        font1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        self.text.SetFont(font1)

        self.slider.SetValue(default_value)

    def __do_layout_(self):
        
        density_widget_sizer = wx.BoxSizer(wx.VERTICAL)
        density_widget_sizer_horiz = wx.BoxSizer(wx.HORIZONTAL)
        
        density_widget_sizer.Add(self.slider, 1, wx.EXPAND|wx.SHAPED)
        
        density_widget_sizer_horiz.Add(self.text, 1, wx.EXPAND)
        density_widget_sizer_horiz.Add(self.value, 1, wx.EXPAND)
        
        density_widget_sizer.Add(density_widget_sizer_horiz, 1, wx.EXPAND)
        density_widget_sizer.Add(self.panel_dummy, 1, wx.EXPAND)
        self.SetSizer(density_widget_sizer)
        
    def SetValue(self, new_value):
        self.slider.SetValue(new_value)
        self.value.SetValue(new_value)

    def GetValue(self):        
        return self.slider.GetValue()

class DensitySlider(wx.Panel):
    def __init__(self, parent, id, def_value):
        

        wx.Panel.__init__(self, parent, -1)
        self.slider = wx.Slider(self, -1, 0, 0, 1000, style = wx.SL_HORIZONTAL)
       
        self.text = wx.StaticText(self, -1, "Marker density:")
        self.value = wx.TextCtrl(self, -1)
        self.panel_dummy = wx.Panel(self, -1)
        self.slider.Bind(wx.EVT_SLIDER, self.OnValueChanged)
        self.__set_properties_(def_value)
        self.__do_layout_()
        
    def __set_properties_(self, default_value):
        self.value.SetValue(str(default_value))
        font1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        font2 = wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        self.text.SetFont(font1)
        self.value.SetFont(font1)
        self.slider.SetValue(int(log(default_value*1000+1)*1000/log(1001)))
        self.value.SetEditable(0)
        
        #self.value.SetMultiLine(False)
    def __do_layout_(self):
        
        density_widget_sizer = wx.BoxSizer(wx.VERTICAL)
        density_widget_sizer_horiz = wx.BoxSizer(wx.HORIZONTAL)
        
        density_widget_sizer.Add(self.slider, 1, wx.EXPAND|wx.SHAPED)
        
        density_widget_sizer_horiz.Add(self.text, 1, wx.EXPAND)
        density_widget_sizer_horiz.Add(self.value, 1, wx.EXPAND)
        
        density_widget_sizer.Add(density_widget_sizer_horiz, 1, wx.EXPAND)
        density_widget_sizer.Add(self.panel_dummy, 1, wx.EXPAND)
        self.SetSizer(density_widget_sizer)
        
        
    def OnValueChanged(self, evt):
        value = self.slider.GetValue()
        new_value = (exp(value*log(1001)/1000) -1)/1000.0
        str_value = "%.3f" % new_value
        self.value.ChangeValue(str_value)
        #self.Refresh()
        evt.Skip()
        
    def SetValue(self, new_value):
        slider_value = int(log(new_value*1000+1)*1000/log(1001))
        self.slider.SetValue(slider_value)        
        converted_value = (exp(slider_value*log(1001)/1000) -1)/1000.0
        str_value = "%.3f" % converted_value
        self.value.ChangeValue(str_value)

    def GetValue(self):        
        return float(self.value.GetValue())

    
class Canvas(wx.Panel):
    def __init__(self, parent, id, app_args):
        #Modify to fit the maximum size
        (sideX, sideY) = wx.DisplaySize()
        if sideX < sideY:
            aux = sideX
            sideX = sideY
            sideY = aux

        wx.Panel.__init__(self, parent, -1, size = (sideY, sideY))
        (self.c, self.lut, self.k, self.rindex, self.sindex) = app_args

        #wx.EVT_ERASE_BACKGROUND(self, lambda e : None)


        

    def OnRepaint(self):

        self.image = wx.EmptyBitmap(0,0)
        mainDC = wx.ClientDC(self)
        mainDC.BeginDrawing()
        mainDC.DrawBitmap(self.image, 5, 5)
        mainDC.EndDrawing()
        
    def OnNextFrame(self, event):
        for i in range(self.k,0,-1):
            self.c[i-1,:2**(i-1)] = mean(self.c[i,:2**i].reshape(-1,2),1)
        im = self.c[self.rindex, self.sindex]
        I = toimage(im, cmin=0, cmax=255)
        I.putpalette(self.lut)
        #print self.c[self.rindex, self.sindex]
        data = piltoimage(I, 1)
        
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


    def OnBackFrame(self, event):
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

        data = piltoimage(I, 1)
        
        self.image = wx.BitmapFromImage(data)
        mainDC = wx.ClientDC(self)
        mainDC.BeginDrawing()
        mainDC.DrawBitmap(self.image, 5, 5)
        mainDC.EndDrawing()
    



[wxID_EXIT_FRAME, wxID_EXIT_FRAMEBUTTON_EXIT_CANCEL, wxID_EXIT_FRAMEBUTTON_EXIT_OK, wxID_EXIT_FRAMEEXIT_QUESTION,] = [wx.NewId() for _init_ctrls in range(4)]

class Exit_Frame(wx.Dialog):
    def _init_ctrls(self, prnt):

        wx.Dialog.__init__(self, id=wxID_EXIT_FRAME, name='Exit_Frame',
              parent=prnt, pos=wx.Point(490, 280), size=wx.Size(280, 140),
              style=wx.DEFAULT_DIALOG_STYLE, title='Exit Animation?')
        self.SetClientSize(wx.Size(350, 105))
        
        self.SetBackgroundStyle(wx.BG_STYLE_COLOUR)
        #self.SetIcon(wx.Icon(u'C:\\.ico',
        #      wx.BITMAP_TYPE_ICO))

        self.button_EXIT_OK = wx.Button(id=wxID_EXIT_FRAMEBUTTON_EXIT_OK,
              label='YES', name='button_EXIT_OK', parent=self, pos=wx.Point(48,
              64), size=wx.Size(75, 23), style=0)
        self.button_EXIT_OK.Bind(wx.EVT_BUTTON, self.OnButton_EXIT_OKButton,
              id=wxID_EXIT_FRAMEBUTTON_EXIT_OK)

        self.button_EXIT_CANCEL = wx.Button(id=wxID_EXIT_FRAMEBUTTON_EXIT_CANCEL,
              label='NO', name='button_EXIT_CANCEL', parent=self,
              pos=wx.Point(232, 64), size=wx.Size(75, 23), style=0)
        self.button_EXIT_CANCEL.Bind(wx.EVT_BUTTON, self.OnButton_EXIT_CANCELButton,
              id=wxID_EXIT_FRAMEBUTTON_EXIT_CANCEL)

        self.Exit_question = wx.StaticText(id=wxID_EXIT_FRAMEEXIT_QUESTION,
              label='Do you wish to quit the program?',
              name='Exit_question', parent=self, pos=wx.Point(60, 32),
              size=wx.Size(327, 19), style=0)
        self.Exit_question.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Times'))

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton_EXIT_OKButton(self, event):
        #Here one should clean the things nicely,
        #destroy should be propagated to the children
        
        parentFrame = self.GetParent()
        parentFrame.forwtimer.Stop()
        parentFrame.backtimer.Stop()
        children = parentFrame.GetChildren()
        for child in children:
            child.Destroy()
            del child
        self.GetParent().Destroy()
        del parentFrame

        self.Close()
        
    def OnButton_EXIT_CANCELButton(self, event):
        self.Close()
        
        
class MainFrame(wx.Frame):
    def __init__(self, parent, ID, title, prec_args):
        
        sizeFullScreen = wx.DisplaySize()
        wx.Frame.__init__(self, parent, ID, title, size=sizeFullScreen)
     
        self.def_speed = 100
        
        self.def_density = 0.04
        self.def_size = 18
        self.def_colour = wx.Color(255, 0, 0)
        self.speed = 100
        self.density = 0.04
        self.size = 18
        self.colour = wx.Color(255, 0, 0)

        self.main_panel = wx.Panel(self, -1)       
        self.control_panel = wx.Panel(self, -1)
        
        self.panel_canvas = Canvas(self.main_panel, -1, prec_args)
        
        
        self.panel_dummy_1 = wx.Panel(self.control_panel, -1)        
        self.bitmap_button_PlayBack = wx.BitmapButton(self.control_panel, -1, wx.Bitmap("E:\\workspace\\KacRing\\control_rewind.png", wx.BITMAP_TYPE_ANY))
        self.panel_dummy_2 = wx.Panel(self.control_panel, -1)

        self.bitmap_button_FrameBack = wx.BitmapButton(self.control_panel, -1, wx.Bitmap("E:\\workspace\\KacRing\\control_back.png", wx.BITMAP_TYPE_ANY))
        self.panel_dummy_3 = wx.Panel(self.control_panel, -1)

        self.bitmap_button_Stop = wx.BitmapButton(self.control_panel, -1, wx.Bitmap("E:\\workspace\\KacRing\\control_stop.png", wx.BITMAP_TYPE_ANY))
        self.panel_dummy_4 = wx.Panel(self.control_panel, -1)

        self.bitmap_button_FrameNext = wx.BitmapButton(self.control_panel, -1, wx.Bitmap("E:\\workspace\\KacRing\\control_play.png", wx.BITMAP_TYPE_ANY))
        self.panel_dummy_5 = wx.Panel(self.control_panel, -1)

        self.bitmap_button_PlayNext = wx.BitmapButton(self.control_panel, -1, wx.Bitmap("E:\\workspace\\KacRing\\control_fastforward.png", wx.BITMAP_TYPE_ANY))
        self.panel_dummy_6 = wx.Panel(self.control_panel, -1)



        self.panel_dummy_7 = wx.Panel(self.control_panel, -1)
        self.button_Restart = wx.Button(self.control_panel, -1, "Restart animation", style=wx.BU_EXACTFIT)
        self.panel_dummy_8 = wx.Panel(self.control_panel, -1)


        self.panel_dummy_9 = wx.Panel(self.control_panel, -1)
        self.button_ResetDefault = wx.Button(self.control_panel, -1, "Restore defaults", style=wx.BU_EXACTFIT)
        self.panel_dummy_10 = wx.Panel(self.control_panel, -1)


        self.panel_dummy_11 = wx.Panel(self.control_panel, -1)
        self.label_speed = wx.StaticText(self.control_panel, -1, "Speed (frames per second)")
        self.slider_speed = wx.Slider(self.control_panel, -1, 0, 1, 100, style=wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.panel_dummy_12 = wx.Panel(self.control_panel, -1)


        self.panel_dummy_13 = wx.Panel(self.control_panel, -1)
        self.slider_density = DensitySlider(self.control_panel, -1, self.def_density)
        self.panel_dummy_14 = wx.Panel(self.control_panel, -1)


        self.panel_dummy_15 = wx.Panel(self.control_panel, -1)
        self.slider_size = SizeSlider(self.control_panel, -1, self.def_size)
        self.panel_dummy_16 = wx.Panel(self.control_panel, -1)


        self.panel_dummy_17 = wx.Panel(self.control_panel, -1)
        self.label_colour = wx.StaticText(self.control_panel, -1, "Initial colour")

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

        self.colour_picker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
    def OnColourChanged(self, evt):
        #print self.colour_picker.GetColour()
        evt.Skip()
    def SetSpeed(self):
        self.speed = self.GetSpeed()
        return

    def GetSpeed(self):
        return self.slider_speed.GetValue()
    
    def OnPlayNext(self, evt):
        self.backtimer.Stop()
        self.forwtimer.Start(1000.0/float(self.speed))
        evt.Skip()

    def OnPlayBack(self, evt):
        self.forwtimer.Stop()
        self.backtimer.Start(1000.0/float(self.speed))
        evt.Skip()
        
    def OnStop(self, evt):
        self.forwtimer.Stop()
        self.backtimer.Stop()
        evt.Skip()
        
    def OnFrameNext(self, evt):
        self.backtimer.Stop()
        self.forwtimer.Stop()
        self.panel_canvas.OnNextFrame(evt)
        evt.Skip()

    def OnFrameBack(self, evt):
        self.forwtimer.Stop()
        self.backtimer.Stop()
        self.panel_canvas.OnBackFrame(evt)
        evt.Skip()


    def OnRestart(self, evt):
        self.forwtimer.Stop()
        self.backtimer.Stop()
        (sizeX, sizeY) = wx.DisplaySize()
        
        self.SetSpeed()
        self.SetDensity()
        self.SetSize()
        self.SetColour()
        
        new_parameters = (self.density, self.size, self.colour)
        print new_parameters
        restart_args = InitialComputation(min([sizeX]+[sizeY])-60, new_parameters)

        (self.panel_canvas.c, self.panel_canvas.lut, self.panel_canvas.k, self.panel_canvas.rindex, self.panel_canvas.sindex) = restart_args
        self.panel_canvas.OnRepaint()
        self.Refresh()

    def OnResetDefault(self, evt):
        self.speed = self.def_speed
        self.density = self.def_density
        self.size = self.def_size
        self.colour = self.def_colour

        self.slider_speed.SetValue(self.speed)
        self.slider_density.SetValue(self.density)
        self.slider_size.SetValue(self.size)
        self.colour_picker.SetColour(self.colour)
        evt.Skip()
    

    def GetColour(self):
        new_colour = self.colour_picker.GetColour()
        return new_colour
    
    def SetColour(self):
        self.colour = self.GetColour()
        return
    
    def GetDensity(self):
        new_density = float(self.slider_density.GetValue())
        return new_density

    def SetDensity(self):
        self.density = self.GetDensity()
        print self.density
        return

    def GetSize(self):
        new_size = self.slider_size.GetValue()
        return new_size
    
    def SetSize(self):
        self.size = self.GetSize()
        return
   
    def OnCloseWindow(self, evt):

        dlg = Exit_Frame(self)
        try:
            dlg.ShowModal()
            
        finally:
            dlg.Destroy()
        

    def __set_properties(self):

        self.SetTitle("Kac Ring Animation")
        self.bitmap_button_PlayBack.SetSize(self.bitmap_button_PlayBack.GetBestSize())
        self.bitmap_button_FrameBack.SetSize(self.bitmap_button_FrameBack.GetBestSize())
        self.bitmap_button_Stop.SetSize(self.bitmap_button_Stop.GetBestSize())
        self.bitmap_button_FrameNext.SetSize(self.bitmap_button_FrameNext.GetBestSize())
        self.bitmap_button_PlayNext.SetSize(self.bitmap_button_PlayNext.GetBestSize())
        self.button_Restart.SetSize(self.button_Restart.GetBestSize())
        self.button_ResetDefault.SetSize(self.button_ResetDefault.GetBestSize())
        font1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
        self.button_Restart.SetFont(font1)
        self.button_ResetDefault.SetFont(font1)
        self.label_speed.SetFont(font1)
        self.label_colour.SetFont(font1)
        self.colour_picker.SetPickerCtrlProportion(1)
        self.colour_picker.GetTextCtrl().SetFont(font1)
        
        ####

        self.slider_speed.SetFont(font1)
        

    def __do_layout(self):

        sizeFullScreen = wx.DisplaySize()
        (size_X, size_Y) = sizeFullScreen

        if size_X < size_Y:
            aux = size_X
            size_X = size_Y
            size_Y = aux
        
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
        sizer_speed_vertical = wx.BoxSizer(wx.VERTICAL)
        
        sizer_canvas.Add(self.panel_canvas, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
        
        sizer_play_buttons.Add(self.panel_dummy_1, 1, wx.EXPAND, 0)
        sizer_play_buttons.Add(self.bitmap_button_PlayBack, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 5)
        sizer_play_buttons.Add(self.panel_dummy_2, 1, wx.EXPAND, 0)
        sizer_play_buttons.Add(self.bitmap_button_FrameBack, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 5)
        sizer_play_buttons.Add(self.panel_dummy_3, 1, wx.EXPAND, 0)
        sizer_play_buttons.Add(self.bitmap_button_Stop, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 5)
        sizer_play_buttons.Add(self.panel_dummy_4, 1, wx.EXPAND, 0)
        sizer_play_buttons.Add(self.bitmap_button_FrameNext, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 5)
        sizer_play_buttons.Add(self.panel_dummy_5, 1, wx.EXPAND, 0)
        sizer_play_buttons.Add(self.bitmap_button_PlayNext, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 5)
        sizer_play_buttons.Add(self.panel_dummy_6, 1, wx.EXPAND, 0)
        
        sizer_controls.Add(sizer_play_buttons, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)


        sizer_restart.Add(self.panel_dummy_7, 1, wx.EXPAND, 0)
        sizer_restart.Add(self.button_Restart, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 5)
        sizer_restart.Add(self.panel_dummy_8, 1, wx.EXPAND, 0)

        sizer_controls.Add(sizer_restart, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)


        sizer_reset.Add(self.panel_dummy_9, 1, wx.EXPAND, 0)
        sizer_reset.Add(self.button_ResetDefault, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 5)

        sizer_reset.Add(self.panel_dummy_10, 1, wx.EXPAND, 0)
        
        sizer_controls.Add(sizer_reset, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_speed_vertical.Add(self.label_speed, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_speed_vertical.Add(self.slider_speed, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 5)

        sizer_speed.Add(self.panel_dummy_11, 1, wx.EXPAND, 0)
        sizer_speed.Add(sizer_speed_vertical, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_speed.Add(self.panel_dummy_12, 1, wx.EXPAND, 0)

        sizer_controls.Add(sizer_speed, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)


        sizer_density.Add(self.panel_dummy_13, 1, wx.EXPAND, 0)
        sizer_density.Add(self.slider_density, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 5)
        
        sizer_density.Add(self.panel_dummy_14, 1, wx.EXPAND, 0)

        sizer_controls.Add(sizer_density, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)


        sizer_size.Add(self.panel_dummy_15, 1, wx.EXPAND, 0)
        sizer_size.Add(self.slider_size, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 5)
        sizer_size.Add(self.panel_dummy_16, 1, wx.EXPAND, 0)

        sizer_controls.Add(sizer_size, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_colour_vertical.Add(self.label_colour, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_colour_vertical.Add(self.colour_picker, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        sizer_colour.Add(self.panel_dummy_17, 1, wx.EXPAND, 0)
        sizer_colour.Add(sizer_colour_vertical, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_colour.Add(self.panel_dummy_18, 1, wx.EXPAND, 0)

        sizer_controls.Add(sizer_colour, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)


        #self.panel_2.SetAutoLayout(True)
        self.control_panel.SetSizer(sizer_controls)
        #sizer_3_copy.Fit(self.control_panel)
        #sizer_3_copy.SetSizeHints(self.control_panel)
        #sizer_2.Add(self.panel_2, 1, wx.EXPAND, 0)
        #self.SetAutoLayout(True)
        self.SetSizer(sizer_main)
        #sizer_2.Fit(self)
        #sizer_2.SetSizeHints(self)
        #self.Layout()
  


class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        (sizeX, sizeY) = wx.DisplaySize()
        start_args = (0.04, 18, wx.Color(255, 0, 0))
        App_args = InitialComputation(min([sizeX]+[sizeY])-60, start_args)
        self._MainFrame = MainFrame(None, -1, "An image on a panel", App_args)
        self._MainFrame.Show(True)
        self.SetTopWindow(self._MainFrame)
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
