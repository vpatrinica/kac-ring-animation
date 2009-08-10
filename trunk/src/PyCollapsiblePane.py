# --------------------------------------------------------------------------------- #
# PYCOLLAPSIBLEPANE wxPython IMPLEMENTATION
# Generic Implementation Based On wx.CollapsiblePane.
#
# Andrea Gavana, @ 09 Aug 2007
# Latest Revision: 09 Aug 2007, 22.00 CET
#
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# gavana@kpo.kz
# andrea.gavana@gmail.com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
#
# End Of Comments
# --------------------------------------------------------------------------------- #

"""
Description
===========

A collapsible pane is a container with an embedded button-like control which
can be used by the user to collapse or expand the pane's contents.
Once constructed you should use the GetPane() function to access the pane and
add your controls inside it (i.e. use the window returned from GetPane as the
parent for the controls which must go in the pane, NOT the PyCollapsiblePane
itself!).

Note that because of its nature of control which can dynamically (and drastically)
change its size at run-time under user-input, when putting PyCollapsiblePane
inside a wx.Sizer you should be careful to add it with a proportion value of zero;
this is because otherwise all other windows with non-null proportion values would
automatically get resized each time the user expands or collapse the pane window
resulting usually in a weird, flickering effect.


Usage Sample
============

collpane = PyCollapsiblePane(self, -1, "Details:")

# add the pane with a zero proportion value to the 'sz' sizer which contains it
sz.Add(collpane, 0, wx.GROW|wx.ALL, 5)

# now add a test label in the collapsible pane using a sizer to layout it:
win = collpane.GetPane()
paneSz = wx.BoxSizer(wx.VERTICAL)
paneSz.Add(wx.StaticText(win, -1, "test!"), 1, wx.GROW|wx.ALL, 2)
win.SetSizer(paneSz)
paneSz.SetSizeHints(win)

"""

import wx

CP_GTK_EXPANDER = 4


class GTKExpander(wx.PyControl):

    def __init__(self, parent, id=wx.ID_ANY, label="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER):

        wx.PyControl.__init__(self, parent, id, pos, size, style)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self._parent = parent
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        

    def OnDrawGTKExpander(self, dc):

        size = self.GetSize()
        label = self._parent.GetBtnLabel()
        triangleWidth, triangleHeight = self._parent.GetExpanderDimensions()
        textWidth, textHeight, descent, externalLeading = dc.GetFullTextExtent(label, self.GetFont())
        
        dc.SetBrush(wx.BLACK_BRUSH)
        dc.SetPen(wx.BLACK_PEN)
        
        if self._parent.IsCollapsed():
            startX, startY = triangleWidth/2, size.y - triangleHeight - 1 - descent
            pt1 = wx.Point(startX, startY)
            pt2 = wx.Point(startX, size.y - 1 - descent)
            pt3 = wx.Point(startX + triangleWidth, size.y - triangleHeight/2 - 1 - descent)
        else:
            startX, startY = 0, size.y - triangleWidth - descent - 1
            pt1 = wx.Point(startX, startY)
            pt2 = wx.Point(startX + triangleHeight, startY)
            pt3 = wx.Point(startX + triangleHeight/2, size.y - descent - 1)

        dc.DrawPolygon([pt1, pt2, pt3])            
                

    def OnDrawGTKText(self, dc):

        size = self.GetSize()
        label = self._parent.GetBtnLabel()
        triangleWidth, triangleHeight = self._parent.GetExpanderDimensions()
        textWidth, textHeight, descent, externalLeading = dc.GetFullTextExtent(label, self.GetFont())
        dc.SetFont(self.GetFont())

        startX, startY = 2*triangleHeight+1, size.y - textHeight
        dc.DrawText(label, startX, startY)


    def DoGetBestSize(self):

        triangleWidth, triangleHeight = self._parent.GetExpanderDimensions()
        label = self._parent.GetBtnLabel()
        dc = wx.ClientDC(self)
        textWidth, textHeight, descent, externalLeading = dc.GetFullTextExtent(label, self.GetFont())

        maxHeight = max(textHeight+descent, triangleHeight)
        maxWidth = 2*triangleHeight+1 + textWidth

        return wx.Size(maxWidth, maxHeight)        


    def OnSize(self, event):

        self.Refresh()



#-----------------------------------------------------------------------------
# PyCollapsiblePane
#-----------------------------------------------------------------------------

class PyCollapsiblePane(wx.PyControl):

    def __init__(self, parent, id=wx.ID_ANY, label="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.CP_DEFAULT_STYLE, val=wx.DefaultValidator,
                 name="CollapsiblePane"):
        """
        Default class constructor.

        @param parent: Parent window, must not be non-NULL.
        @param id: The identifier for the control.
        @param label: The initial label shown in the button which allows the
        user to expand or collapse the pane window.
        @param pos: Initial position.
        @param size: Initial size.
        @param style: The window style, see wx.CP_* flags.
        @param validator: Validator which can be used for additional data checks.
        @param name: Control name.
        """
        
        wx.PyControl.__init__(self, parent, id, pos, size, style, val, name)
        
        self._pButton = self._pStaticLine = self._pPane = self._sz = None            
        self._strLabel = label
        self._bCollapsed = True

        if style & CP_GTK_EXPANDER == 0:
            # create children and lay them out using a wx.BoxSizer
            # (so that we automatically get RTL features)
            self._pButton = wx.Button(self, wx.ID_ANY, self.GetBtnLabel(), wx.Point(0, 0),
                                      wx.DefaultSize, wx.BU_EXACTFIT)
            self._pStaticLine = wx.StaticLine(self, wx.ID_ANY)

            if wx.Platform == "__WXMAC__": 
                # on Mac we put the static libe above the button
                self._sz = wx.BoxSizer(wx.VERTICAL)
                self._sz.Add(self._pStaticLine, 0, wx.ALL|wx.GROW, self.GetBorder())
                self._sz.Add(self._pButton, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, self.GetBorder())
            else:
                # on other platforms we put the static line and the button horizontally
                self._sz = wx.BoxSizer(wx.HORIZONTAL)
                self._sz.Add(self._pButton, 0, wx.LEFT|wx.TOP|wx.BOTTOM, self.GetBorder())
                self._sz.Add(self._pStaticLine, 1, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, self.GetBorder())
        else:
            self._sz = wx.BoxSizer(wx.HORIZONTAL)
            self._pButton = GTKExpander(self, wx.ID_ANY, self.GetBtnLabel(), wx.Point(0, 0),
                                        wx.DefaultSize)
            self._sz.Add(self._pButton, 0, wx.LEFT|wx.TOP|wx.BOTTOM, self.GetBorder())
            self.SetExpanderDimensions(3, 6)

            self._pButton.Bind(wx.EVT_PAINT, self.OnDrawGTKStyle)
            self._pButton.Bind(wx.EVT_LEFT_DOWN, self.OnButton)
            if wx.Platform == "__WXMSW__":
                self._pButton.Bind(wx.EVT_LEFT_DCLICK, self.OnButton)
            
        # do not set sz as our sizers since we handle the pane window without using sizers
        self._pPane = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                               wx.TAB_TRAVERSAL|wx.NO_BORDER)

        # start as collapsed
        self._pPane.Hide()

        self.Bind(wx.EVT_BUTTON, self.OnButton, self._pButton)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        

    def DoGetBestSize(self):

        # NB: do not use GetSize() but rather GetMinSize()
        sz = self._sz.GetMinSize()

        # when expanded, we need more vertical space
        if self.IsExpanded():
            sz.SetWidth(max(sz.GetWidth(), self._pPane.GetBestSize().x))
            sz.SetHeight(sz.y + self.GetBorder() + self._pPane.GetBestSize().y)
        
        return sz


    def GetBtnLabel(self):
        """ Returns the button label. """

        if self.GetWindowStyleFlag() & CP_GTK_EXPANDER:
            return self._strLabel
        
        return self._strLabel + (self.IsCollapsed() and [" >>"] or [" <<"])[0]


    def OnStateChange(self, sz):
        """ Handles the status changes (collapsing/expanding). """

        # minimal size has priority over the best size so set here our min size
        self.SetMinSize(sz)
        self.SetSize(sz)

        if self.HasFlag(wx.CP_NO_TLW_RESIZE):
            # the user asked to explicitely handle the resizing itself...
            return
        
        # NB: the following block of code has been accurately designed to
        #     as much flicker-free as possible be careful when modifying it!

        top = wx.GetTopLevelParent(self)
        if top:
            # NB: don't Layout() the 'top' window as its size has not been correctly
            #     updated yet and we don't want to do an initial Layout() with the old
            #     size immediately followed by a SetClientSize/Fit call for the new
            #     size that would provoke flickering!

            if top.GetSizer():
                if (wx.Platform == "__WXGTK__" and self.IsCollapsed()) or wx.Platform != "__WXGTK__":
                # FIXME: the SetSizeHints() call would be required also for GTK+ for
                #        the expanded.collapsed transition. Unfortunately if we
                #        enable this line, then the GTK+ top window won't always be
                #        resized by the SetClientSize() call below! As a side effect
                #        of this dirty fix, the minimal size for the pane window is
                #        not set in GTK+ and the user can hide it shrinking the "top"
                #        window...

                    top.GetSizer().SetSizeHints(top)


            # we shouldn't attempt to resize a maximized window, whatever happens
            if not top.IsMaximized():
                
                if self.IsCollapsed():
                    # expanded . collapsed transition
                    if top.GetSizer():
                        # we have just set the size hints...
                        sz = top.GetSizer().CalcMin()

                        # use SetClientSize() and not SetSize() otherwise the size for
                        # e.g. a wxFrame with a menubar wouldn't be correctly set
                        top.SetClientSize(sz)
                    
                    else:
                        
                        top.Layout()
                
                else:
                
                    # collapsed . expanded transition

                    # force our parent to "fit", i.e. expand so that it can honour
                    # our minimal size
                    top.Fit()
                

    def Collapse(self, collapse=True):
        """ Collapses or expands the pane window. """

        # optimization
        if self.IsCollapsed() == collapse:
            return

        self.Freeze()
        
        # update our state
        self._pPane.Show(not collapse)
        self._bCollapsed = collapse
        self.Thaw()

        # update button label
        # NB: this must be done after updating our "state"
        self._pButton.SetLabel(self.GetBtnLabel())

        self.OnStateChange(self.GetBestSize())
        

    def Expand(self):
        """ Same as Collapse(False). """

        self.Collapse(False)


    def IsCollapsed(self):
        """ Returns True if the pane window is currently hidden. """

        return self._bCollapsed        


    def IsExpanded(self):
        """ Returns True if the pane window is currently shown. """

        return not self.IsCollapsed()        


    def GetPane(self):
        """
        Returns a reference to the pane window. Use the returned wx.Window as
        the parent of widgets to make them part of the collapsible area.
        """

        return self._pPane
    
        
    def SetLabel(self, label):
        """ Sets the button label. """

        self._strLabel = label
        self._pButton.SetLabel(self.GetBtnLabel())
        self._pButton.SetInitialSize()
        self._pButton.Refresh()

        self.Layout()


    def SetButton(self, button):
        """
        Assign a new button to PyCollapsiblePane.
        This button can be the standard wx.Button or any of the generic
        implementations which live in wx.lib.buttons.
        """

        self._sz.Replace(self._pButton, button)
        self._pButton.Destroy()

        self._pButton = button
        self.SetLabel(button.GetLabel())
        self.Bind(wx.EVT_BUTTON, self.OnButton, self._pButton)
        
        self.Layout()
        

    def Layout(self):
        """ Layout the PyCollapsiblePane. """

        if not self._pButton or not self._pPane or not self._sz:
            return False     # we need to complete the creation first!

        oursz = self.GetSize()

        # move & resize the button and the static line
        self._sz.SetDimension(0, 0, oursz.GetWidth(), self._sz.GetMinSize().GetHeight())
        self._sz.Layout()

        if self.IsExpanded():
        
            # move & resize the container window
            yoffset = self._sz.GetSize().GetHeight() + self.GetBorder()
            self._pPane.SetDimensions(0, yoffset, oursz.x, oursz.y - yoffset)

            # this is very important to make the pane window layout show correctly
            self._pPane.Show()
            self._pPane.Layout()
        
        return True


    def GetBorder(self):
        """ Returns the PyCollapsiblePane border (platform dependent). """

        if wx.Platform == "__WXMAC__":
            return 6
        elif wx.Platform == "__WXGTK__":
            return 3
        elif wx.Platform == "__WXMSW__":
            return self._pButton.ConvertDialogSizeToPixels(wx.Size(2, 0)).x
        else:
            return 5
        

    def SetExpanderDimensions(self, width, height):

        self._expanderDimensions = width, height
        self._sz.Layout()
        self._pButton.Refresh()


    def GetExpanderDimensions(self):

        return self._expanderDimensions

    
#-----------------------------------------------------------------------------
# PyCollapsiblePane - event handlers
#-----------------------------------------------------------------------------

    def OnButton(self, event):
        """ Handles the wx.EVT_BUTTON event for PyCollapsiblePane. """

        if event.GetEventObject() != self._pButton:
            event.Skip()
            return

        self.Collapse(not self.IsCollapsed())

        # this change was generated by the user - send the event
        ev = wx.CollapsiblePaneEvent(self, self.GetId(), self.IsCollapsed())
        self.GetEventHandler().ProcessEvent(ev)


    def OnSize(self, event):
        """ Handles the wx.EVT_SIZE event for PyCollapsiblePane. """

        self.Layout()


    def OnDrawGTKStyle(self, event):
        """ Drawing routine to paint the GTK-style expander. """

        dc = wx.AutoBufferedPaintDC(self._pButton)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        
        self.OnDrawGTKExpander(dc)
        self.OnDrawGTKText(dc)
        

    def OnDrawGTKExpander(self, dc):
        """ Overridable method to draw the GTK-style expander. """

        self._pButton.OnDrawGTKExpander(dc)


    def OnDrawGTKText(self, dc):
        """ Overridable method to draw the PyCollapsiblePane text in the expander. """

        self._pButton.OnDrawGTKText(dc)

