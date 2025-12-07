#Boa:FramePanel:Panel1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         SubtitlesPanel.py
# Purpose:      Panel with subtitle options.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: SubtitlesPanel.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import subprocess
import os

import wx

import dpg4x.Globals as Globals
from dpg4x.TreeCtrlComboPopup import TreeCtrlComboPopup
from dpg4x.CustomFontSelector import CustomFontSelector

[wxID_PANEL1, wxID_PANEL1BUTTON1, wxID_PANEL1BUTTON2, 
 wxID_PANEL1TREECTRLCOMBO1, wxID_PANEL1SPINCTRL1, wxID_PANEL1STATICTEXT1, 
 wxID_PANEL1STATICTEXT2, wxID_PANEL1STATICTEXT3, wxID_PANEL1STATICTEXT4, 
 wxID_PANEL1TEXTCTRL1, wxID_PANEL1TEXTCTRL2, wxID_PANEL1STATICTEXT5,
 wxID_PANEL1CHOICE2
] = [wx.NewId() for _init_ctrls in range(13)]

class SubtitlesPanel(wx.Panel):
    def _init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        # d0malaga f32: parent.AddSpacer(wx.Size(20, 20), (0, 0), border=0, flag=0, span=(1, 1))
        # d0malaga f32: parent.AddSpacer(wx.Size(100, 8), (0, 1), border=0, flag=0, span=(1, 2))
        #parent.AddSpacer(wx.Size(200, 8), (0, 3), border=0, flag=0, span=(1, 3))
        parent.Add(self.staticText5, (1, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.Add(self.choice2, (1, 3), border=0, flag=0, span=(1, 4))
        parent.Add(self.staticText1, (3, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.Add(self.spinCtrl1, (3, 3), border=0, flag=0, span=(1, 1))
        parent.Add(self.staticText2, (5, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,2))
        parent.Add(self.textCtrl1, (5, 3), border=0, flag=wx.EXPAND,
              span=(1, 3))
        parent.Add(self.button1, (5, 6), border=0, flag=0, span=(1, 1))
        parent.Add(self.staticText3, (8, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,2))
        parent.Add(self.textCtrl2, (8, 3), border=0, flag=wx.EXPAND,
              span=(1, 3))
        parent.Add(self.button2, (8, 6), border=0, flag=0, span=(1, 1))
        parent.Add(self.staticText4, (10, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.Add(self.choice1, (10, 3), border=0, flag=0, span=(1, 3))

    def _init_sizers(self):
        # generated method, don't edit
        self.gridBagSizer1 = wx.GridBagSizer(hgap=0, vgap=0)

        self._init_coll_gridBagSizer1_Items(self.gridBagSizer1)

        self.SetSizer(self.gridBagSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL1, name='', parent=prnt,
              style=wx.TAB_TRAVERSAL)
              
        self.staticText5 = wx.StaticText(id=wxID_PANEL1STATICTEXT5,
              label=_('Subtitles Source')+' ', name='staticText5', parent=self, 
              style=0)

        self.choice2 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE2,
              name='choice1', parent=self, style=0)

        self.staticText1 = wx.StaticText(id=wxID_PANEL1STATICTEXT1,
              label=_('Subtitles Track')+' ', name='staticText1', 
              parent=self, style=0)

        self.spinCtrl1 = wx.SpinCtrl(id=wxID_PANEL1SPINCTRL1, 
              value=str(Globals.subtitles_track),
              max=31, min=0, name='spinCtrl1', parent=self, 
              style=wx.SP_ARROW_KEYS)

        self.staticText2 = wx.StaticText(id=wxID_PANEL1STATICTEXT2,
              label=_('Subtitles File')+' ', name='staticText2', 
              parent=self, style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_PANEL1TEXTCTRL1, name='textCtrl1',
              parent=self, style=0, value=Globals.subtitles_file)

        self.button1 = wx.Button(id=wxID_PANEL1BUTTON1, label=_('Examine'),
              name='button1', parent=self, style=0)

        self.staticText3 = wx.StaticText(id=wxID_PANEL1STATICTEXT3,
              label=_('Font')+' ', name='staticText3', parent=self, style=0)

        self.textCtrl2 = wx.TextCtrl(id=wxID_PANEL1TEXTCTRL2, name='textCtrl2',
              parent=self, style=wx.TE_READONLY, value=Globals.subtitles_font)

        self.button2 = wx.Button(id=wxID_PANEL1BUTTON2, label=_('Examine'),
              name='button2', parent=self, style=0)

        self.staticText4 = wx.StaticText(id=wxID_PANEL1STATICTEXT4,
              label=_('Encoding')+' ', name='staticText4', parent=self, style=0)

        # Custom TreeCtrlComboPopup
        self.choice1 = wx.ComboCtrl(self, size=(280,-1), 
            style=wx.CB_READONLY, value=Globals.subtitles_encoding)
        self.treeCtrlCombo = TreeCtrlComboPopup()
        self.choice1.SetPopupControl(self.treeCtrlCombo)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # Init the subtitles source choice
        self.choice2.Append(_('Auto'),'auto')
        self.choice2.Append(_('Get track from input video file'),'sid')
        self.choice2.Append(_('Use subtitles file'),'file')
        self.choice2.Append(_('Disable subtitles'),'disable')
        if Globals.subtitles_source == 'auto':
            self.choice2.Select(0)
        elif Globals.subtitles_source == 'sid':
            self.choice2.Select(1)
        elif Globals.subtitles_source == 'file':
            self.choice2.Select(2)
        elif Globals.subtitles_source == 'disable':
            self.choice2.Select(3)
        self.changeSubsSource(None)
        
        # Init encoding choice
        default = Globals.subtitles_encoding
        if Globals.which('iconv'):
            iconvOut = subprocess.Popen(
                ['iconv', '-l'], 
                # On Windows when running under py2exe it is 
                # necessary to define stdin
                stdin=subprocess.PIPE,shell=Globals.shell(),
                stdout=subprocess.PIPE).communicate()[0]
            iconvOut = iconvOut.replace(b'/',b'')
            encodings = iconvOut.split(b'\n')
            encodings.sort()
            # Load the encodings in the tree
            currentLetter = chr(0)
            currentNode = None               
            for e in encodings:
                encode = e.decode()
                # Careful with empty strings
                if len(encode) > 1:
                    firstLetter = encode[0].upper()
                    # Detect numbers
                    if firstLetter >= '0' and firstLetter <= '9':
                        firstLetter = '#'
                    # If the firs letter has changed create a new node
                    if firstLetter != currentLetter:
                        currentLetter = firstLetter
                        currentNode = self.treeCtrlCombo.AddItem(currentLetter)
                    # Add the encoding to the tree
                    sub = self.treeCtrlCombo.AddItem(encode, parent=currentNode)
                    # Check if it's de default and select it
                    if encode == default:
                        self.treeCtrlCombo.GetControl().SelectItem(sub)
                    
        # If iconv is not available, disable encoding
        else:
            self.choice1.SetValue('')
            self.choice1.Enable(False)
            Globals.debug(_('WARNING: iconv not found. Subtitles encoding ' \
                'option disabled.'))
        
        # Events
        self.button1.Bind(wx.EVT_BUTTON, self.selectSubsFile)
        self.button2.Bind(wx.EVT_BUTTON, self.selectSubsFont)
        self.choice2.Bind(wx.EVT_CHOICE, self.changeSubsSource)
        
    def changeSubsSource(self, event):
        "Change the source for the subtitles"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        #source = event.GetClientData()
        source = self.choice2.GetClientData(self.choice2.GetSelection())
        # Start enabling all the controls
        self.spinCtrl1.Enable(True)
        self.textCtrl1.Enable(True)
        self.button1.Enable(True)
        self.textCtrl2.Enable(True)
        self.button2.Enable(True)
        self.choice1.Enable(True)
        # If auto, disable the sid and the subs file
        if source == 'auto':
            self.spinCtrl1.Enable(False)
            self.textCtrl1.Enable(False)
            self.button1.Enable(False)
        # If sid, disable the subs file
        elif source == 'sid':
            self.textCtrl1.Enable(False)
            self.button1.Enable(False)
        # If file, disable the sid
        elif source == 'file':
            self.spinCtrl1.Enable(False)
        # Else disable all the controls
        else:
            self.spinCtrl1.Enable(False)
            self.textCtrl1.Enable(False)
            self.button1.Enable(False)
            self.textCtrl2.Enable(False)
            self.button2.Enable(False)
            self.choice1.Enable(False)
        
    def selectSubsFile(self, event):
        "Dialog to select a subtitles file"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        dialog = wx.FileDialog(self, _('Select a subtitles file'), style=wx.OPEN, 
            defaultDir=os.path.dirname(self.textCtrl1.GetValue()))
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl1.SetValue(dialog.GetPath())
        dialog.Destroy()
        
    def selectSubsFont(self, event):
        "Dialog to select a subtitles font"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        dialog = CustomFontSelector(
            self, _('Select the subtitles font'), 
            self.textCtrl2.GetValue())
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl2.SetValue(dialog.GetData())
        dialog.Destroy()
        
    def loadOptions(self):
        "Load the subtitle options as global variables"
        Globals.subtitles_source = self.choice2.GetClientData(
            self.choice2.GetSelection())
        # If subtitles track selected
        if Globals.subtitles_source == 'sid':
            Globals.subtitles_track = self.spinCtrl1.GetValue()
        # If subtitles file selected
        elif Globals.subtitles_source == 'file':
            Globals.subtitles_file = self.textCtrl1.GetValue()
            # Check the subtitles file can be read
            if not (os.path.isfile(Globals.subtitles_file) and os.access(
                Globals.subtitles_file, os.R_OK)):
                raise Exception(_('The subtitles file cannot be read.'))
        # Get also fonts and encoding
        Globals.subtitles_font = self.textCtrl2.GetValue()
        Globals.subtitles_encoding = self.choice1.GetValue()
