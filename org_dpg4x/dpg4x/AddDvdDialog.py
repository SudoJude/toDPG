#Boa:Dialog:Dialog1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         AddDvdDialog.py
# Purpose:      A dialog to add Dvd media sources.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: AddDvdDialog.py $
# Copyright:    (c) 2010 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx

import dpg4x.Globals as Globals

[wxID_DIALOG1,
 wxID_DIALOG1SPINCTRL1, wxID_DIALOG1STATICTEXT1, wxID_DIALOG1STATICTEXT2, 
 wxID_DIALOG1TEXTCTRL1, wxID_PANEL1CHECKBOX1, wxID_DIALOG1SPINCTRL2, 
 wxID_DIALOG1SPINCTRL3, wxID_DIALOG1STATICTEXT3, wxID_DIALOG1STATICTEXT4
] = [wx.NewId() for _init_ctrls in range(10)]

class AddDvdDialog(wx.Dialog):
    def _init_coll_gridBagSizer1_Items(self, parent):
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
        parent.Add(self.checkBox1, (5, 2), border=0, 
            flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, span=(1, 4))
        parent.Add(self.staticText3, (6, 2), border=0, 
            flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL, span=(1, 1))
        parent.Add(self.spinCtrl2, (7, 1), border=0, flag=wx.ALIGN_RIGHT, span=(1, 2))
        parent.Add(self.staticText4, (6, 4), border=0, 
            flag=wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL, span=(1, 1))
        parent.Add(self.spinCtrl3, (7, 4), border=0, flag=wx.ALIGN_LEFT, span=(1, 2))
        parent.Add(self.button1, (9, 2), border=0, flag=0, span=(1, 1))
        parent.Add(self.button2, (9, 4), border=0, flag=0, span=(1, 1))

    def _init_sizers(self):
        # generated method, don't edit
        self.gridBagSizer1 = wx.GridBagSizer(hgap=0, vgap=0)

        self._init_coll_gridBagSizer1_Items(self.gridBagSizer1)

        self.SetSizer(self.gridBagSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              style=wx.DEFAULT_DIALOG_STYLE, title=_('Add DVD'))

        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1,
              label=_('Device'), name='staticText1', parent=self, style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl1',
              parent=self, style=0, value=Globals.dpg_dvddevice)

        self.staticText2 = wx.StaticText(id=wxID_DIALOG1STATICTEXT2,
              label=_('Track'), name='staticText2', parent=self, style=0)

        self.spinCtrl1 = wx.SpinCtrl(id=wxID_DIALOG1SPINCTRL1, value=str(1),
              max=99, min=1, name='spinCtrl1', parent=self, 
              style=wx.SP_ARROW_KEYS)

        self.checkBox1 = wx.CheckBox(id=wxID_PANEL1CHECKBOX1, 
              label=_('Filter chapters'), name='checkBox1', parent=self, style=0)
              
        self.staticText3 = wx.StaticText(id=wxID_DIALOG1STATICTEXT3,
              label=_('First'), name='staticText3', parent=self, style=0)
              
        self.spinCtrl2 = wx.SpinCtrl(id=wxID_DIALOG1SPINCTRL2, value=str(1),
              max=99, min=1, name='spinCtrl2', parent=self, 
              style=wx.SP_ARROW_KEYS)
              
        self.staticText4 = wx.StaticText(id=wxID_DIALOG1STATICTEXT4,
              label=_('Last'), name='staticText4', parent=self, style=0)
              
        self.spinCtrl3 = wx.SpinCtrl(id=wxID_DIALOG1SPINCTRL3, value=str(10),
              max=99, min=1, name='spinCtrl3', parent=self, 
              style=wx.SP_ARROW_KEYS)

        self.button1 = wx.Button(id=wx.ID_OK, parent=self, style=0)

        self.button2 = wx.Button(id=wx.ID_CANCEL, parent=self, style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # Disable the chapter controls
        self.spinCtrl2.Enable(False)
        self.spinCtrl3.Enable(False)
        
        # Events
        self.button1.Bind(wx.EVT_BUTTON, self.OnOK)
        self.checkBox1.Bind(wx.EVT_CHECKBOX, self.switchChapters)
        
        # Set the window size
        width = self.GetBestSize().x + 20
        height = self.GetBestSize().y + 20
        self.SetMinSize(wx.Size(width, height))
        self.SetClientSize(wx.Size(width, height))
        
    def getDevice(self):
        "Returns the selected media device"
        return self.textCtrl1.GetValue()
    
    def getTrack(self):
        "Returns the selected VCD track"
        return str(self.spinCtrl1.GetValue())
    
    def getChapter(self):
        "Returns the selected chapter range"
        if not self.checkBox1.IsChecked():
            return None
        else:
            return str(self.spinCtrl2.GetValue()) + '-' \
                '' + str(self.spinCtrl3.GetValue())
    
    def switchChapters(self, event):
        "Enable or disable the chapter controls"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        self.spinCtrl2.Enable(self.checkBox1.IsChecked())
        self.spinCtrl3.Enable(self.checkBox1.IsChecked())
    
    # Because wx.ID_OK is a special button we need a function with this name
    def OnOK( self, event ):
        "Manages the ID_OK OnClick event"
        # Check that the last chapter is higher than the first
        if self.checkBox1.IsChecked():
            if self.spinCtrl2.GetValue() > self.spinCtrl3.GetValue():
                message = _('The last chapter cannot be lower than the first.')
                dialog = wx.MessageDialog(self, message, _('ERROR'), 
                    style=wx.OK|wx.ICON_ERROR)
                dialog.ShowModal()
                return
        # Update the Globals.dpg_vcddevice value
        Globals.dpg_dvddevice = self.textCtrl1.GetValue()
        self.EndModal(wx.ID_OK)
