#Boa:Frame:Frame1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         VideoPanel.py
# Purpose:      Main frame of Application.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: VideoPanel.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import os

import wx

import dpg4x.Globals as Globals
from dpg4x.FilesPanel import FilesPanel
from dpg4x.VideoPanel import VideoPanel
from dpg4x.AudioPanel import AudioPanel
from dpg4x.SubtitlesPanel import SubtitlesPanel
from dpg4x.OtherPanel import OtherPanel

def create(parent, icon_dir):
    return Frame1(parent, icon_dir)

[wxID_FRAME1, wxID_FRAME1NOTEBOOK1, 
] = [wx.NewId() for _init_ctrls in range(2)]

class Frame1(wx.Frame):
    def _init_sizers(self):
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self.SetSizer(self.boxSizer1)

    def _init_coll_boxSizer1_Items(self, parent):
        parent.Add(self.notebook1, 1, border=0, flag=wx.EXPAND)

    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | 
                    wx.CLOSE_BOX | wx.CLIP_CHILDREN,
              title='DPG4X')

        self.notebook1 = wx.Toolbook(id=wxID_FRAME1NOTEBOOK1, name='notebook1',
              parent=self, style=wx.BK_TOP)

        self._init_sizers()

    def __init__(self, parent, icon_dir):
        self._init_ctrls(parent)
        
        # Set the icons for the main window
        bundle = wx.IconBundle()
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
        imageList.Add(wx.Icon(icon_dir+'/help.png',
            wx.BITMAP_TYPE_PNG))
        self.notebook1.AssignImageList(imageList)
        
        # Panel with files to be processed
        filesPanel = FilesPanel(self.notebook1)
        # wx.Toolbook is buggy on MacOSX. wxPython 2.8 and 2.9 will not display
        # the AddPage() caption text and icons disappear after being clicked
        # with 2.9. Problem is evident in the wxPython demo as well as dpg4x.
        self.notebook1.AddPage(filesPanel,
            Globals.fillString(_('MAIN'),10),imageId=0)
        Globals.filesPanel = filesPanel
        
        # Panel with video options
        videoPanel = VideoPanel(self.notebook1)
        self.notebook1.AddPage(videoPanel,
            Globals.fillString(_('VIDEO'),10),imageId=1)
        Globals.videoPanel = videoPanel
        
        # Panel with audio options
        audioPanel = AudioPanel(self.notebook1)
        self.notebook1.AddPage(audioPanel,
            Globals.fillString(_('AUDIO'),10),imageId=2)
        Globals.audioPanel = audioPanel
        
        # Panel with subtitle options
        subtitlesPanel = SubtitlesPanel(self.notebook1)
        self.notebook1.AddPage(subtitlesPanel,
            Globals.fillString(_('SUBTITLES'),10),imageId=3)
        Globals.subtitlesPanel = subtitlesPanel
        
        # Panel with aditional options
        otherPanel = OtherPanel(self.notebook1)
        self.notebook1.AddPage(otherPanel,
            Globals.fillString(_('MISC'),10),imageId=4)
        Globals.otherPanel = otherPanel
        
        # User Guide
        self.notebook1.AddPage(filesPanel,
            Globals.fillString(_('HELP'),10),imageId=5)
        
        # Set the window size
        width = self.GetBestSize().x + 20
        height = self.GetBestSize().y + 20
        self.SetMinSize(wx.Size(width, height))
        self.SetClientSize(wx.Size(width, height))
        
        # Events
        self.notebook1.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.PageChanged)
        
    def PageChanged(self, event):
        "A page changes in the notebook, used to open the user guide"
        if event.GetSelection() == 5:
            self.notebook1.SetSelection(event.GetOldSelection())
            wx.LaunchDefaultBrowser('http://dpg4x.sourceforge.net/user-guide.html')
            

        
        
