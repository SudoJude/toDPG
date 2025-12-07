#Boa:Dialog:MediaMain
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         MediaMainFrame.py
# Purpose:      Frame with per-media settings.
#
# Author:       Marc P. Davignon
#
# Created:
# RCS-ID:       $Id: MediaMainFrame.py $
# Copyright:    (c) 2010 Marc P. Davignon
# Licence:      GPL v3
#----------------------------------------------------------------------------

import os

import wx

import dpg4x.Globals as Globals
import dpg4x.ConfigurationManager as ConfigurationManager
from dpg4x.MediaVideoPanel import MediaVideoPanel
from dpg4x.MediaAudioPanel import MediaAudioPanel
from dpg4x.MediaSubtitlesPanel import MediaSubtitlesPanel
from dpg4x.MediaOtherPanel import MediaOtherPanel

def show_settings(file, parent):
    "Allows individual media settings which override global defaults"
    mediaMainFrame = MediaMain(file, parent)

    Globals.mediaMainPanel = mediaMainFrame
    try:
        Globals.mainPanel.Enable(False)
        mediaMainFrame.ShowModal()
    finally:
        Globals.mainPanel.Enable(True)
        mediaMainFrame.Destroy()

[wxID_DIALOG1, wxID_FRAME2NOTEBOOK1,
] = [wx.NewId() for _init_ctrls in range(2)]

class MediaMain(wx.Dialog):
    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.SetSizer(self.boxSizer1)


    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.notebook1, 1, border=0, flag=wx.EXPAND)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                    wx.CLIP_CHILDREN,
              title=self.file)

        self.notebook1 = wx.Toolbook(id=wxID_FRAME2NOTEBOOK1, name='notebook1',
              parent=self, style=wx.BK_TOP)

        self._init_sizers()

    def __init__(self, file, parent):
        
        # Do not try to remove the path from dvd or vcd
        if (file[:6] == 'vcd://') or (file[:6] == 'dvd://'):
            basename = file
        else:
            basename = os.path.basename(file)
        self.file = basename
        # Read options from the media specific config file (if one exists)
        # This allows media specific options to be saved between sessions
        ConfigurationManager.loadConfiguration(self.file)
        # Create the dialog
        self._init_ctrls(parent)
        
        # Set the icons for the main window
        bundle = wx.IconBundle()
        icon_dir = Globals.getIconDir()
        bundle.AddIcon(icon_dir+'/dpg4x_64.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIcon(icon_dir+'/dpg4x_48.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIcon(icon_dir+'/dpg4x_32.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIcon(icon_dir+'/dpg4x_22.png',
            wx.BITMAP_TYPE_PNG)
        bundle.AddIcon(icon_dir+'/dpg4x_16.png',
            wx.BITMAP_TYPE_PNG)
        self.SetIcons(bundle)

        # Set the icons for the menu
        imageList = wx.ImageList(32, 32)
        imageList.Add(wx.Icon(icon_dir+'/files.png',
            wx.BITMAP_TYPE_PNG))
        imageList.Add(wx.Icon(icon_dir+'/video.png',
            wx.BITMAP_TYPE_PNG))
        imageList.Add(wx.Icon(icon_dir+'/audio.png',
            wx.BITMAP_TYPE_PNG))
        imageList.Add(wx.Icon(icon_dir+'/subtitles.png',
            wx.BITMAP_TYPE_PNG))
        imageList.Add(wx.Icon(icon_dir+'/other.png',
            wx.BITMAP_TYPE_PNG))
        self.notebook1.AssignImageList(imageList)

        # Panel with media video options
        mediaVideoPanel = MediaVideoPanel(self.notebook1)
        self.notebook1.AddPage(mediaVideoPanel,
            Globals.fillString(_('VIDEO'),10),imageId=1)
        Globals.mediaVideoPanel = mediaVideoPanel

        # Panel with media audio options
        mediaAudioPanel = MediaAudioPanel(self.notebook1)
        self.notebook1.AddPage(mediaAudioPanel,
            Globals.fillString(_('AUDIO'),10),imageId=2)
        Globals.mediaAudioPanel = mediaAudioPanel

        # Panel with media subtitle options
        mediaSubtitlesPanel = MediaSubtitlesPanel(self.notebook1)
        self.notebook1.AddPage(mediaSubtitlesPanel,
            Globals.fillString(_('SUBTITLES'),10),imageId=3)
        Globals.mediaSubtitlesPanel = mediaSubtitlesPanel

        # Panel with aditional media options
        mediaOtherPanel = MediaOtherPanel(self.notebook1)
        self.notebook1.AddPage(mediaOtherPanel,
            Globals.fillString(_('MISC'),10),imageId=4)
        Globals.mediaOtherPanel = mediaOtherPanel
        
        # Help to set the buttons at the same height
        
        # Get the max buttons heigh
        height = mediaVideoPanel.getPanelButtonsHeigh()
        if mediaAudioPanel.getPanelButtonsHeigh() > height:
            height = mediaAudioPanel.getPanelButtonsHeigh()
        if mediaSubtitlesPanel.getPanelButtonsHeigh() > height:
            height = mediaSubtitlesPanel.getPanelButtonsHeigh()
        if mediaOtherPanel.getPanelButtonsHeigh() > height:
            height = mediaOtherPanel.getPanelButtonsHeigh()
        # Set the same heigh for all the panels
        mediaVideoPanel.setPanelButtonsHeigh(height)
        mediaAudioPanel.setPanelButtonsHeigh(height)
        mediaSubtitlesPanel.setPanelButtonsHeigh(height)
        mediaOtherPanel.setPanelButtonsHeigh(height)

        # Set the window size
        width = self.GetBestSize().x + 20
        height = self.GetBestSize().y + 20
        self.SetMinSize(wx.Size(width, height))
        self.SetClientSize(wx.Size(width, height))
        
        # Go to the misc page by default
        self.notebook1.ChangeSelection(3)

    def saveAndCloseFrame(self, event):
        "Save and close the media settings window"
        # Get the options from the panels
        Globals.mediaVideoPanel.loadOptions()
        Globals.mediaAudioPanel.loadOptions()
        Globals.mediaSubtitlesPanel.loadOptions()
        Globals.mediaOtherPanel.loadOptions(None)
        # Save options to the media specific config file
        ConfigurationManager.saveConfiguration(self.file)
        self.Close()

