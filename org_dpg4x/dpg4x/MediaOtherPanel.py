#Boa:FramePanel:Panel1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         MediaOtherPanel.py
# Purpose:      Panel with per-media aditional options.
#
# Author:       Marc P. Davignon
#
# Created:
# RCS-ID:       $Id: MediaOtherPanel.py $
# Copyright:    (c) 2010 Marc P. Davignon
# Licence:      GPL v3
#----------------------------------------------------------------------------

# NOTE: "OTHER" is not longer used, now we call it "MISC".

import os

import wx

import dpg4x.Globals as Globals

[wxID_PANEL1, wxID_PANEL1BUTTON1, wxID_PANEL1BUTTON2, wxID_PANEL1BUTTON3,
 wxID_PANEL1STATICTEXT1, wxID_PANEL1STATICTEXT2, wxID_PANEL1STATICTEXT3,
 wxID_PANEL1TEXTCTRL1, wxID_PANEL1TEXTCTRL2, wxID_PANEL1TEXTCTRL3,
 wxID_PANEL1STATICTEXT4, wxID_PANEL1STATICTEXT5, wxID_PANEL1STATICTEXT6,
 wxID_DIALOG1SPINCTRL1, wxID_PANEL1STATICTEXT7, wxID_PANEL1STATICTEXT8, 
 wxID_PANEL1CHOICE1, wxID_PANEL1CHOICE2, wxID_PANEL2
] = [wx.NewId() for _init_ctrls in range(19)]

class MediaOtherPanel(wx.Panel):
    def _init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        #parent.AddSpacer(wx.Size(20, 20), (0, 0), border=0, flag=0, span=(1, 1))
        #parent.AddSpacer(wx.Size(100, 8), (0, 1), border=0, flag=0, span=(1, 2))
        #parent.AddSpacer(wx.Size(280, 8), (0, 3), border=0, flag=0, span=(1, 3))
        parent.Add(self.staticText7, (1, 4), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 1))
        parent.Add(self.staticText8, (1, 2), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 1))
        parent.Add(self.choice1, (1, 5), border=0, flag=0, span=(1, 1))
        parent.Add(self.choice2, (1, 3), border=0, flag=0, span=(1, 1)) 
        parent.Add(self.staticText1, (3, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.Add(self.textCtrl1, (3, 3), border=0, flag=wx.EXPAND,
              span=(1, 3))
        parent.Add(self.button1, (3, 6), border=0, flag=0, span=(1, 1))
        parent.Add(self.staticText4, (4, 1), border=0,
              flag=wx.ALIGN_CENTER, span=(1,7))
        parent.Add(self.staticText2, (6, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1,2))
        parent.Add(self.textCtrl2, (6, 3), border=0, flag=wx.EXPAND,
              span=(1, 3))
        parent.Add(self.button2, (6, 6), border=0, flag=0, span=(1, 1))
        parent.Add(self.staticText3, (8, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 2))
        parent.Add(self.textCtrl3, (8, 3), border=0, flag=wx.EXPAND,
              span=(1, 3))
        parent.Add(self.button3, (8, 6), border=0, flag=0, span=(1, 1))
        parent.Add(self.staticText5, (9, 1), border=0,
              flag=wx.ALIGN_CENTER, span=(1,7))
        parent.Add(self.staticText6, (11, 1), border=0,
              flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, span=(1, 3))
        parent.Add(self.spinCtrl1, (11, 4), border=0, flag=0,
              span=(1, 1))   
        parent.Add(self.panel2, (13, 1), border=0, flag=0, span=(1, 4))
        
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit
        
        parent.Add(self.button7, 1, border=0, flag=0)
        parent.Add(self.button8, 1, border=0, flag=0)

    def _init_sizers(self):
        # generated method, don't edit
        self.gridBagSizer1 = wx.GridBagSizer(hgap=0, vgap=0)
        self.boxSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self._init_coll_gridBagSizer1_Items(self.gridBagSizer1)
        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.SetSizer(self.gridBagSizer1)
        self.panel2.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL1, name='', parent=prnt,
              style=wx.TAB_TRAVERSAL)
              
        self.panel2 = wx.Panel(id=wxID_PANEL2, name='', parent=self)

        self.staticText1 = wx.StaticText(id=wxID_PANEL1STATICTEXT1,
              label=_('Output Folder')+' ', name='staticText1',
              parent=self, style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_PANEL1TEXTCTRL1, name='textCtrl1',
              parent=self, style=0, value=Globals.other_output)

        self.button1 = wx.Button(id=wxID_PANEL1BUTTON1, label=_('Examine'),
              name='button1', parent=self, style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANEL1STATICTEXT2,
              label=_('Temporary Folder')+' ', name='staticText2',
              parent=self, style=0)

        self.textCtrl2 = wx.TextCtrl(id=wxID_PANEL1TEXTCTRL2, name='textCtrl2',
              parent=self, style=0, value=Globals.other_temporary)

        self.button2 = wx.Button(id=wxID_PANEL1BUTTON2, label=_('Examine'),
              name='button2', parent=self, style=0)

        self.staticText3 = wx.StaticText(id=wxID_PANEL1STATICTEXT3,
              label=_('Select Thumbnail')+' ', name='staticText3',
              parent=self, style=0)

        self.textCtrl3 = wx.TextCtrl(id=wxID_PANEL1TEXTCTRL3, name='textCtrl3',
              parent=self, style=0, value=Globals.other_thumbnail)

        self.button3 = wx.Button(id=wxID_PANEL1BUTTON3, label=_('Examine'),
              name='button3', parent=self, style=0)

        self.staticText4 = wx.StaticText(id=wxID_PANEL1STATICTEXT4,
              label=_('The input folder will be used by default'),
              name='staticText4', parent=self, style=0)

        self.staticText5 = wx.StaticText(id=wxID_PANEL1STATICTEXT5,
              label=_('Thumbnails are autogenerated by default (DPG4 only)'),
              name='staticText5', parent=self, style=0)

        self.staticText6 = wx.StaticText(id=wxID_PANEL1STATICTEXT6,
              label=_('Preview size (seconds)'),
              name='staticText6', parent=self, style=0)

        self.spinCtrl1 = wx.SpinCtrl(id=wxID_DIALOG1SPINCTRL1,
              value=str(Globals.other_previewsize), max=9999, min=1,
              name='spinCtrl1', parent=self, style=wx.SP_ARROW_KEYS)

        self.staticText7 = wx.StaticText(id=wxID_PANEL1STATICTEXT7,
              label=_('Quality')+' ', name='staticText7', parent=self, style=0)

        self.staticText8 = wx.StaticText(id=wxID_PANEL1STATICTEXT8,
              label=_('DPG Version')+' ', name='staticText8', parent=self,
              style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE1,
              name='choice1', parent=self, style=0)

        self.choice2 = wx.Choice(choices=[], id=wxID_PANEL1CHOICE2,
              name='choice2', parent=self, style=0)

        self.button7 = wx.Button(id=wx.ID_SAVE,
              name='button7', parent=self.panel2, style=0)

        self.button8 = wx.Button(id=wx.ID_CANCEL,
              name='button8', parent=self.panel2, style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)

        # Init version choice
        self.choice2.Append('0',0)
        self.choice2.Append('1',1)
        self.choice2.Append('2',2)
        self.choice2.Append('3',3)
        self.choice2.Append('4',4)
        self.choice2.Select(Globals.dpg_version)

        # Init quality choice
        self.choice1.Append(_('Low'),'low')
        self.choice1.Append(_('Normal'),'normal')
        self.choice1.Append(_('High'),'high')
        self.choice1.Append(_('Extra High'),'doublepass')
        if Globals.dpg_quality == 'low':
            self.choice1.Select(0)
        elif Globals.dpg_quality == 'normal':
            self.choice1.Select(1)
        elif Globals.dpg_quality == 'high':
            self.choice1.Select(2)
        elif Globals.dpg_quality == 'doublepass':
            self.choice1.Select(3)

        # Thumbnails only available for DPG version 4
        if Globals.dpg_version < 4:
            self.textCtrl3.Enable(False)
            self.button3.Enable(False)

        # Events
        self.button1.Bind(wx.EVT_BUTTON, self.selectOuputDir)
        self.button2.Bind(wx.EVT_BUTTON, self.selectTemporaryDir)
        self.button3.Bind(wx.EVT_BUTTON, self.selectThumbnail)

        self.choice2.Bind(wx.EVT_CHOICE, self.changeDPGLevel)
        self.choice1.Bind(wx.EVT_CHOICE, self.changeQuality)

        self.button7.Bind(wx.EVT_BUTTON, self.saveAndCloseFrame)

    def selectOuputDir(self, event):
        "Dialog to select the output folder"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        dialog = wx.DirDialog(self, _('Select the ouput folder'),
            style=wx.DD_DEFAULT_STYLE,
            defaultPath=os.path.dirname(self.textCtrl1.GetValue()))
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl1.SetValue(dialog.GetPath())
        dialog.Destroy()

    def selectTemporaryDir(self, event):
        "Dialog to select the output folder"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        dialog = wx.DirDialog(self, _('Select the temporary folder'),
            style=wx.DD_DEFAULT_STYLE,
            defaultPath=os.path.dirname(self.textCtrl2.GetValue()))
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl2.SetValue(dialog.GetPath())
        dialog.Destroy()

    def selectThumbnail(self, event):
        "Dialog to select a subtitles file"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        dialog = wx.FileDialog(self, _('Select a thumbnail file'), style=wx.FD_OPEN,
            defaultDir=os.path.dirname(self.textCtrl3.GetValue()))
        if dialog.ShowModal() == wx.ID_OK:
            self.textCtrl3.SetValue(dialog.GetPath())
        dialog.Destroy()

    def changeDPGLevel(self, event):
        "Update the GUI when the dpg level changes"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        version = event.GetClientData()

        # Only DPG4 uses thumbnails
        if (version == 4):
            Globals.mediaOtherPanel.textCtrl3.Enable(True)
            Globals.mediaOtherPanel.button3.Enable(True)
        else:
            Globals.mediaOtherPanel.textCtrl3.Enable(False)
            Globals.mediaOtherPanel.button3.Enable(False)

        # OGG can be used only with DPG3 or better
        oldSelection = Globals.mediaAudioPanel.choice1.GetSelection()
        if version>2 and Globals.mediaAudioPanel.choice1.GetCount()<3:
            Globals.mediaAudioPanel.choice1.Append('OGG','vorbis')
        elif version<3 and Globals.mediaAudioPanel.choice1.GetCount()>2:
            Globals.mediaAudioPanel.choice1.Delete(2)
            if oldSelection < 2:
                Globals.mediaAudioPanel.choice1.SetSelection(oldSelection)
            else:
                Globals.mediaAudioPanel.choice1.SetSelection(1)
        Globals.mediaAudioPanel.changeAudioCodec(None)
        
        # Only mono audio for DPG0
        if (version == 0):
            Globals.mediaAudioPanel.checkBox2.Enable(False)
        else:
            Globals.mediaAudioPanel.checkBox2.Enable(True)

    def changeQuality(self, event):
        "Update the GUI when the quality level changes"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        quality = event.GetClientData()
        # Mencoder won't work with double pass and fps < 24
        currFPS = Globals.mediaVideoPanel.spinCtrl3.GetValue()
        autoFPS = Globals.mediaVideoPanel.checkBox2.IsChecked()
        if quality == 'doublepass':
            if (not autoFPS) and (currFPS < 24):
                message = _('With extra high quality, the video FPS cannot ' \
                    'be lower than 24. Raising video FPS to 24.')
                Globals.debug(_('WARNING') + ': ' + message)
                # Show a dialog to the user
                dialog = wx.MessageDialog(self, message, _('WARNING'),
                    style=wx.ICON_EXCLAMATION)
                dialog.ShowModal()
            # Set the min FPS to 24
            Globals.mediaVideoPanel.spinCtrl3.SetRange(24,
                Globals.mediaVideoPanel.spinCtrl3.GetMax())
        # With other qualities, we can user lower FPS
        else:
            Globals.mediaVideoPanel.spinCtrl3.SetRange(1,
                Globals.mediaVideoPanel.spinCtrl3.GetMax())
            # With autoFPS set it back to 15 (default) again
            if autoFPS:
                Globals.mediaVideoPanel.spinCtrl3.SetValue(15)

    def loadOptions(self, files):
        "Load the other options as global variables"
        Globals.other_output = self.textCtrl1.GetValue()
        # Check the output folder exists and is writable
        if Globals.other_output:
            if not (os.path.isdir(Globals.other_output) and os.access(
                Globals.other_output, os.W_OK)):
                raise Exception(_('The output folder cannot be written.' \
                    ' Please select another one.'))
        # If no output folder given, check the input folders
        elif files is not None:
            for file in files:
                # Check for DVD and VCD sources
                if (file[:6] == 'vcd://') or (file[:6] == 'dvd://'):
                    raise Exception(_('If you want to encode from DVD or VCD' \
                        ' you need to select an output folder in "MISC".'))
                # Check for normal files
                else:
                    outDir = os.path.dirname(file)
                    if not (os.path.isdir(outDir) and os.access(outDir, os.W_OK)):
                        raise Exception(_('The folder %s cannot be written.' \
                            ' Please select an output folder in "MISC".') % outDir)

        Globals.other_temporary = self.textCtrl2.GetValue()
        # Check the temporary folder exists and is writable
        if not (os.path.isdir(Globals.other_temporary) and os.access(
            Globals.other_temporary, os.W_OK)):
            raise Exception(_('The temporary folder cannot be written.' \
                ' Please select another one.'))

        Globals.other_thumbnail = self.textCtrl3.GetValue()
        # Check the thumbnail file can be read
        if Globals.other_thumbnail:
            if not (os.path.isfile(Globals.other_thumbnail) and os.access(
                Globals.other_thumbnail, os.R_OK)):
                raise Exception(_('The thumbnail file cannot be read.'))
            # Check the thumbnail file can be processed by wx.Image
            imageAux = wx.Image(Globals.other_thumbnail)
            if not imageAux.IsOk():
                raise Exception(_('The thumbnail file has an unknown format.'))

        Globals.other_previewsize = self.spinCtrl1.GetValue()

        Globals.dpg_version = self.choice2.GetClientData(
            self.choice2.GetSelection())
        Globals.dpg_quality = self.choice1.GetClientData(
            self.choice1.GetSelection())

    def saveAndCloseFrame(self, event):
        "Save and close the media settings window"
        Globals.mediaMainPanel.saveAndCloseFrame(event)
        
    def getPanelButtonsHeigh(self):
        "Return the current buttons position"
        p = self.panel2.GetPosition()
        return p.y
        
    def setPanelButtonsHeigh(self, height):
        "Set the height for the save and close buttons"
        # Calculate the difference between max and current
        currentPosition = self.getPanelButtonsHeigh()
        difference = height - currentPosition
        # Add the current empty space
        difference += self.gridBagSizer1.GetEmptyCellSize().GetHeight()
        # Resize the space up to the buttons
        #self.gridBagSizer1.AddSpacer(wx.Size(1, difference), (12, 0), border=0, 
        #    flag=0, span=(1, 1))
