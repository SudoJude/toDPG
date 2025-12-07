#Boa:FramePanel:Panel1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         AudioPanel.py
# Purpose:      Panel with audio options.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: AudioPanel.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx

import dpg4x.Globals as Globals

[wxID_PANEL1, wxID_PANEL1CHECKBOX1, wxID_PANEL1CHECKBOX2, wxID_PANEL1CHOICE1, 
 wxID_PANEL1CHOICE2, wxID_PANEL1CHOICE3, wxID_PANEL1SPINCTRL1, 
 wxID_PANEL1STATICTEXT1, wxID_PANEL1STATICTEXT2, wxID_PANEL1STATICTEXT3, 
 wxID_PANEL1STATICTEXT4, wxID_PANEL1CHECKBOX3
] = [wx.NewId() for _init_ctrls in range(12)]

class AudioPanel(wx.Panel):
    def _init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        # d0malaga f32: parent.AddSpacer(wx.Size(20, 40), (0, 0), border=0, flag=0, span=(1, 1))
        # d0malaga f32: parent.AddSpacer(wx.Size(150, 20), (0, 1), border=0, flag=0, span=(1,2))
        # d0malaga f32: parent.AddSpacer(wx.Size(40, 20), (0, 4), border=0, flag=0, span=(1, 1))
        parent.Add(self.staticText1, (1, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,2))
        parent.Add(self.choice1, (1, 3), border=0, flag=0, span=(1, 1))
        parent.Add(self.staticText2, (4, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,2))
        parent.Add(self.spinCtrl1, (4, 3), border=0, flag=0, span=(1, 1))
        parent.Add(self.checkBox3, (4, 5), border=0, flag=0, span=(1, 1))
        parent.Add(self.checkBox1, (7, 5), border=0, flag=0, span=(1, 1))
        parent.Add(self.staticText3, (7, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,
              2))
        parent.Add(self.choice2, (7, 3), border=0, flag=0, span=(1, 1))
        parent.Add(self.staticText4, (9, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,
              2))
        parent.Add(self.choice3, (9, 3), border=0, flag=0, span=(1, 1))
        parent.Add(self.checkBox2, (9, 5), border=0, flag=0, span=(1, 1))

    def _init_sizers(self):
        # generated method, don't edit
        self.gridBagSizer1 = wx.GridBagSizer(hgap=0, vgap=0)

        self._init_coll_gridBagSizer1_Items(self.gridBagSizer1)

        self.SetSizer(self.gridBagSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL1, name='', parent=prnt,
              style=wx.TAB_TRAVERSAL)

        self.staticText1 = wx.StaticText(id=wxID_PANEL1STATICTEXT1,
              label=_('Audio Codec')+' ', name='staticText1', parent=self, 
              style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE1,
              name='choice1', parent=self, style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANEL1STATICTEXT2,
              label=_('Audio Track')+' ', name='staticText2', 
              parent=self, style=0)

        self.spinCtrl1 = wx.SpinCtrl(id=wxID_PANEL1SPINCTRL1, 
              # MacOSX issue, initial= results in empty SpinCtrl values.
              # Using value= (which requires a string) fixes this.
              # This certainly seems like a bug however since we use .SetValue
              # later on so this does seem like a more appropriate option.
              # Works fine on Windows and Linux as well.
              # Tested with Python 2.6.1 (ships with OS) and wxPython 2.8.8.1
              # (ships with OS), 2.8.11.0, and 2.9.1.1 with the same result.
              value=str(Globals.audio_track),
              max=191, min=0, name='spinCtrl1', parent=self, 
              style=wx.SP_ARROW_KEYS)

        self.checkBox1 = wx.CheckBox(id=wxID_PANEL1CHECKBOX1, 
              label=_('Normalize Volume'), name='checkBox1', parent=self, style=0)

        self.staticText3 = wx.StaticText(id=wxID_PANEL1STATICTEXT3,
              label=_('Audio Bitrate')+' ', name='staticText3', 
              parent=self, style=0)

        self.choice2 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE2,
              name='choice2', parent=self, style=0)

        self.staticText4 = wx.StaticText(id=wxID_PANEL1STATICTEXT4,
              label=_('Audio Frequency')+' ', name='staticText4', parent=self, 
              style=0)

        self.choice3 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE3,
              name='choice3', parent=self, style=0)

        self.checkBox2 = wx.CheckBox(id=wxID_PANEL1CHECKBOX2, 
              label=_('Force Mono Channel'), name='checkBox2', 
              parent=self, style=0)
              
        self.checkBox3 = wx.CheckBox(id=wxID_PANEL1CHECKBOX3, 
              label=_('Auto Audio Track'), name='checkBox3', 
              parent=self, style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # Init the audio codec choice
        self.choice1.Append('GSM','libgsm')
        self.choice1.Append('MP2','mp2')
        # OGG can be used only with DPG3 or better
        if Globals.dpg_version >= 3:
            self.choice1.Append('OGG','vorbis')
        # Load the stored selection
        if Globals.audio_codec == 'libgsm':
            self.choice1.Select(0)
        elif Globals.audio_codec == 'mp2':
            self.choice1.Select(1)
        elif Globals.audio_codec == 'vorbis':
            self.choice1.Select(2)
         
        # OGG and GSM support is in alpha status
        self.choice1.Enable(False)
            
        # Check if sox is available
        #if not Globals.which('sox'):
        #    self.choice1.Enable(False)
        #    Globals.debug(_(u'WARNING: sox not found. OGG and GSM audio ' \
        #        u'support disabled.'))
            
        self.changeAudioCodec(None)
        
        # Init the audio frequency choice
        self.choice3.Append('22050',22050)
        self.choice3.Append('32000',32000)
        self.choice3.Append('44100',44100)
        self.choice3.SetStringSelection(str(Globals.audio_frequency))
        
        # Only audio at 32000 works with current versions. Disabled.
        self.choice3.SetSelection(1)
        self.choice3.Enable(False)
        
        # Init the auto track check
        if Globals.audio_autotrack:
            self.checkBox3.SetValue(True)
        self.switchAutoTrack(None)
        
        # Check normalize if needed
        if Globals.audio_normalize:
            self.checkBox1.SetValue(True)
            
        # Check mono if needed
        if Globals.audio_mono:
            self.checkBox2.SetValue(True)
            
        # Stereo is not available for DPG0
        if (Globals.dpg_version == 0):
            self.checkBox2.Enable(False)
        
        # Events
        self.checkBox3.Bind(wx.EVT_CHECKBOX, self.switchAutoTrack)
        self.choice1.Bind(wx.EVT_CHOICE, self.changeAudioCodec)
        
    def switchAutoTrack(self, event):
        "Enable or disable the track selector"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        self.spinCtrl1.Enable(not self.checkBox3.IsChecked())
        
    def loadOptions(self):
        "Load the audio options as global variables"
        Globals.audio_codec = self.choice1.GetClientData(
            self.choice1.GetSelection())
        Globals.audio_track = self.spinCtrl1.GetValue()
        Globals.audio_autotrack = self.checkBox3.IsChecked()
        # The bitrate depends on the codec
        if Globals.audio_codec == 'mp2':
            Globals.audio_bitrate_mp2 = self.choice2.GetClientData(
                self.choice2.GetSelection())
        elif Globals.audio_codec == 'vorbis':
            Globals.audio_bitrate_vorbis = self.choice2.GetClientData(
                self.choice2.GetSelection())
        Globals.audio_frequency = self.choice3.GetClientData(
            self.choice3.GetSelection())
        Globals.audio_normalize = self.checkBox1.IsChecked()
        Globals.audio_mono = self.checkBox2.IsChecked()
        
    def changeAudioCodec(self, event):
        "Used to adapt the options to the new audio codec"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
            codec = event.GetClientData()
        else:
            codec = self.choice1.GetClientData(self.choice1.GetSelection())
        
        # Sox supports GSM at full rate 13kbps
        if codec == 'libgsm':
            self.choice2.Clear()
            # The spaces behind 13 avoid the choice to be too small
            self.choice2.Append('13  ','')
            self.choice2.SetSelection(0)
            # GSM only supports mono audio
            self.checkBox2.Enable(False)
            
        # Ogg vorbis - these are official Xiph.org values, but they are
        #              orientative only
        elif codec == 'vorbis':
            self.choice2.Clear()
            self.choice2.Append('45',45)   # -1
            self.choice2.Append('64',64)   #  0
            self.choice2.Append('80',80)   #  1
            self.choice2.Append('96',96)   #  2
            self.choice2.Append('112',112) #  3
            self.choice2.Append('128',128) #  4
            self.choice2.Append('160',160) #  5
            self.choice2.Append('192',192) #  6
            self.choice2.Append('224',224) #  7
            self.choice2.Append('256',256) #  8
            self.choice2.Append('320',320) #  9
            self.choice2.Append('500',500) # 10
            self.choice2.SetStringSelection(str(Globals.audio_bitrate_vorbis))
            # GSM only supports mono audio
            self.checkBox2.Enable(True)
            
        # Default mp2 codec
        else:
            self.choice2.Clear()
            self.choice2.Append('32',32)
            self.choice2.Append('48',48)
            self.choice2.Append('56',56)
            self.choice2.Append('64',64)
            self.choice2.Append('80',80)
            self.choice2.Append('96',96)
            self.choice2.Append('112',112)
            self.choice2.Append('128',128)
            self.choice2.Append('160',160)
            self.choice2.Append('192',192)
            self.choice2.Append('224',224)
            self.choice2.Append('256',256)
            self.choice2.Append('320',320)
            self.choice2.Append('384',384)
            self.choice2.SetStringSelection(str(Globals.audio_bitrate_mp2))
            # GSM only supports mono audio
            self.checkBox2.Enable(True)
