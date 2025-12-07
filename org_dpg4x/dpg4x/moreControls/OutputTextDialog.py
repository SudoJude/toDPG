# -*- coding: utf-8 -*-
#Boa:Dialog:Dialog1

#----------------------------------------------------------------------------
# Name:         OutputTextDialog.py
# Purpose:      Dialog with a TextCtrl to show program's output.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: OutputTextCtrl.py $
# Copyright:    (c) 2010 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx

[wxID_DIALOG1, wxID_DIALOG1PANEL1, wxID_DIALOG1TEXTCTRL1,
 wxID_DIALOG1TIMER1
] = [wx.NewId() for _init_ctrls in range(4)]

class OutputTextDialog(wx.Dialog):
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.textCtrl1, 1, border=0, flag=wx.EXPAND)
        parent.Add(self.button1, 0, border=0, flag=wx.CENTER)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.panel1.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt, titl=''):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              pos=wx.Point(271, 143), size=wx.Size(683, 445),
              style=wx.CAPTION | wx.RESIZE_BORDER, title=titl)
        self.SetClientSize(wx.Size(683, 445))

        self.panel1 = wx.Panel(id=wxID_DIALOG1PANEL1, name='panel1',
              parent=self, style=wx.TAB_TRAVERSAL)

        self.textCtrl1 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl1',
              parent=self.panel1,
              style=wx.TE_MULTILINE | wx.TE_READONLY, value='')

        self.button1 = wx.Button(id=wx.ID_CLOSE,
              parent=self.panel1, style=0)

        self._init_sizers()

    def __init__(self, parent, text='', title=''):
        self._init_ctrls(parent, title)
        # Show the text
        self.textCtrl1.AppendText(text)
        self.textCtrl1.ShowPosition(0)
        # Events
        self.button1.Bind(wx.EVT_BUTTON, self.OnClose)
        #wx.EVT_BUTTON(self.button1, wx.ID_CLOSE, self.OnClose)
        
    def OnClose(self, event):
        "Close the dialog"
        self.EndModal(wx.ID_OK)


