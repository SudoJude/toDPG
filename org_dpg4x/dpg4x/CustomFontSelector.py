# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         CustomFontSelector.py
# Purpose:      Dialog to select fonts (only faces).
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: CustomFontSelector.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx

class CustomFontSelector(wx.Dialog):
    "Dialog to select font faces"
    
    def __init__(self, parent, title, oldFont):
        "Creates a font selector dialog"
        
        # Call the panel constructor
        wx.Dialog.__init__(self, parent, title=title, 
            style=wx.DEFAULT_DIALOG_STYLE)

        # The font enumerator can return a list with the available fonts
        e = wx.FontEnumerator()
        e.EnumerateFacenames()
        list = e.GetFacenames()

        # Sort the given list
        list.sort()

        # Create the controls in the dialog
        self.listBox1 = wx.ListBox(self, -1, wx.DefaultPosition, (200, 200),
                             list, wx.LB_SINGLE)

        self.staticText1 = wx.StaticText(self, -1, '', (200, 200))
        
        self.button1 = wx.Button(self, id=wx.ID_OK)
        self.button2 = wx.Button(self, id=wx.ID_CANCEL)

        # Sizers
        self.gridBagSizer1 = wx.GridBagSizer(hgap=0, vgap=0)
        #self.gridBagSizer1.AddSpacer(wx.Size(20, 20), (0, 0), 
        #      border=0, flag=0, span=(1, 1))
        #self.gridBagSizer1.AddSpacer(wx.Size(280, 20), (0, 2), 
        #      border=0, flag=0, span=(1, 3))
        self.gridBagSizer1.Add(self.listBox1, (1, 1), border=0, 
              flag=0, span=(3, 1))
        self.gridBagSizer1.Add(self.staticText1, (2, 2), border=5, 
              flag=wx.ALL, span=(3, 1))
        self.gridBagSizer1.Add(self.button1, (3, 3), border=0, 
              flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM, span=(1, 1))
        self.gridBagSizer1.Add(self.button2, (3, 4), border=0, 
              flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM, span=(1, 1))
        self.SetSizer(self.gridBagSizer1)
        self.Layout()

        # Make the first selection to the old font
        oldIndex = self.listBox1.FindString(oldFont)
        if oldIndex != wx.NOT_FOUND:
            self.listBox1.SetSelection(oldIndex)
            self.OnSelect(None)
    
        # Events
        self.Bind(wx.EVT_LISTBOX, self.OnSelect, id=self.listBox1.GetId())
        
        # Set the window size
        width = self.GetBestSize().x + 20
        height = self.GetBestSize().y + 20
        self.SetMinSize(wx.Size(width, height))
        self.SetClientSize(wx.Size(width, height))

    def OnSelect(self, evt):
        "Change the current font when selected by the user"
        self.face = self.listBox1.GetStringSelection()
        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, 
            wx.FONTWEIGHT_NORMAL, False, self.face)
        self.staticText1.SetLabel(self.face)
        self.staticText1.SetFont(font)
        
    def GetData(self):
        "Return the selected font"
        return self.face
