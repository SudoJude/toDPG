#Boa:Dialog:Dialog1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         AddVcdDialog.py
# Purpose:      A dialog to add Vcd media sources.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: AddVcdDialog.py $
# Copyright:    (c) 2010 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx

import dpg4x.Globals as Globals

[wxID_DIALOG1,
 wxID_DIALOG1SPINCTRL1, wxID_DIALOG1STATICTEXT1, wxID_DIALOG1STATICTEXT2, 
 wxID_DIALOG1STATICTEXT3, wxID_DIALOG1TEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(6)]

class AddVcdDialog(wx.Dialog):
    def _init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        #parent.AddSpacer(wx.Size(1, 20), (0, 0), border=0, flag=0, span=(1, 1))
        #parent.AddSpacer(wx.Size(100, 10), (0, 1), border=0, flag=0, span=(1, 2))
        #parent.AddSpacer(wx.Size(110, 10), (0, 4), border=0, flag=0, span=(1, 2))
        parent.Add(self.staticText1, (1, 1), border=0, 
            flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.Add(self.textCtrl1, (1, 4), border=0, flag=wx.EXPAND, 
            span=(1, 2))
        parent.Add(self.staticText2, (3, 1), border=0, 
            flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.Add(self.spinCtrl1, (3, 4), border=0, flag=0, span=(1, 2))
        parent.Add(self.staticText3, (4, 0), border=0, 
            flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL, span=(1, 8))
        parent.Add(self.button1, (6, 2), border=0, flag=0, span=(1, 1))
        parent.Add(self.button2, (6, 4), border=0, flag=0, span=(1, 1))

    def _init_sizers(self):
        # generated method, don't edit
        self.gridBagSizer1 = wx.GridBagSizer(hgap=0, vgap=0)

        self._init_coll_gridBagSizer1_Items(self.gridBagSizer1)

        self.SetSizer(self.gridBagSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              style=wx.DEFAULT_DIALOG_STYLE, title=_('Add VCD'))

        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label=_('Device'), name='staticText1', parent=self, style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl1',
              parent=self, style=0, value=Globals.dpg_vcddevice)

        self.staticText2 = wx.StaticText(id=wxID_DIALOG1STATICTEXT2,
              label=_('Track'), name='staticText2', parent=self, style=0)

        self.spinCtrl1 = wx.SpinCtrl(id=wxID_DIALOG1SPINCTRL1, value=str(2),
              max=99, min=1, name='spinCtrl1', parent=self, 
              style=wx.SP_ARROW_KEYS)

        self.staticText3 = wx.StaticText(id=wxID_DIALOG1STATICTEXT3,
              label=_('Track 1 does not contain video'), 
              name='staticText3', parent=self, style=0)

        self.button1 = wx.Button(id=wx.ID_OK, parent=self, style=0)

        self.button2 = wx.Button(id=wx.ID_CANCEL, parent=self, style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # Events
        self.button1.Bind(wx.EVT_BUTTON, self.OnOK)
        
        # Set the window size
        width = self.GetBestSize().x
        height = self.GetBestSize().y + 20
        self.SetMinSize(wx.Size(width, height))
        self.SetClientSize(wx.Size(width, height))

    def getDevice(self):
        "Returns the selected media device"
        return self.textCtrl1.GetValue()
    
    def getTrack(self):
        "Returns the selected VCD track"
        return str(self.spinCtrl1.GetValue())
    
    # Because wx.ID_OK is a special button we need a function with this name
    def OnOK( self, event ):
        "Manages the ID_OK OnClick event"
        # Update the Globals.dpg_vcddevice value
        Globals.dpg_vcddevice = self.textCtrl1.GetValue()
        self.EndModal(wx.ID_OK)
