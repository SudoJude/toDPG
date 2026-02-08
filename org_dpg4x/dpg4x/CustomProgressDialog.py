#Boa:Dialog:Dialog1
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         CustomProgressDialog.py
# Purpose:      Dialog to show the progress of the encoding.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: CustomProgressDialog.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import wx

[wxID_DIALOG1, wxID_DIALOG1BUTTON1, wxID_DIALOG1GAUGE1, wxID_DIALOG1GAUGE2, 
 wxID_DIALOG1STATICTEXT1, wxID_DIALOG1STATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(6)]


import sys
class TextProgress():    
    "Basic class to run without a GUI"
    def __init__(self, parent, numFiles, totalProgress):        
        # Save the progress values
        self.currProgress = 0
        self.totalProgress = totalProgress
        self.currProgOverall = 0
        self.totalProgOverall = totalProgress * numFiles
        self.remainFiles = numFiles
                 
    def doProgress(self, amount, message):
        "Advance the progress dialog in 1 step"
        # Increase the current progress
        self.currProgress += amount
        self.currProgOverall += amount
        # Check if we have finished with the current file
        if self.currProgress >= self.totalProgress:
            self.currProgress -= self.totalProgress
            self.remainFiles -= 1
        sys.stderr.write(".")
        print(message)
        return False
    
    def getCurrentProgress(self):
        "Returns the current progress"
        return self.currProgress
        

class CustomProgressDialog(wx.Dialog):
    def _init_coll_gridBagSizer1_Items(self, parent):
        # generated method, don't edit

        #parent.AddSpacer(wx.Size(20, 20), (0, 0), border=0, flag=0, span=(1,1))
        #parent.AddSpacer(wx.Size(500, 20), (0, 1), border=0, flag=0, span=(1,7))
        parent.Add(self.staticText1, (1, 1), border=0, flag=wx.EXPAND,
              span=(1, 7))
        parent.Add(self.gauge1, (2, 1), border=0, flag=wx.EXPAND, span=(1,
              7))
        parent.Add(self.staticText2, (4, 1), border=0, flag=wx.EXPAND,
              span=(1, 7))
        parent.Add(self.gauge2, (5, 1), border=0, flag=wx.EXPAND, span=(1,
              7))
        parent.Add(self.button1, (7, 4), border=0,
              flag=wx.EXPAND | wx.ALIGN_CENTER, span=(1, 1))

    def _init_sizers(self):
        # generated method, don't edit
        self.gridBagSizer1 = wx.GridBagSizer(hgap=0, vgap=0)

        self._init_coll_gridBagSizer1_Items(self.gridBagSizer1)

        self.SetSizer(self.gridBagSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              style=wx.CAPTION, title=_('ENCODING'))

        self.staticText1 = wx.StaticText(id=wxID_DIALOG1STATICTEXT1, label='',
              name='staticText1', parent=self, pos=wx.Point(20, 20),
              style=0)

        self.gauge1 = wx.Gauge(id=wxID_DIALOG1GAUGE1, name='gauge1',
              parent=self, pos=wx.Point(20, 35), range=100, size=wx.Size(500,
              28), style=wx.GA_HORIZONTAL)

        self.staticText2 = wx.StaticText(id=wxID_DIALOG1STATICTEXT2,
              label='', name='staticText2', parent=self,
              pos=wx.Point(20, 83), style=0)

        self.gauge2 = wx.Gauge(id=wxID_DIALOG1GAUGE2, name='gauge2',
              parent=self, pos=wx.Point(20, 98), range=100, size=wx.Size(500,
              28), style=wx.GA_HORIZONTAL)

        self.button1 = wx.Button(id=wxID_DIALOG1BUTTON1, label=_('Abort'),
              name='button1', parent=self, pos=wx.Point(233, 146),
              style=0)

        self._init_sizers()

    def __init__(self, parent, numFiles, totalProgress):
        self._init_ctrls(parent)
        
        # Abort flag
        self.abortFlag = False
        
        # Save the progress values
        self.currProgress = 0
        self.totalProgress = totalProgress
        self.currProgOverall = 0
        self.totalProgOverall = totalProgress * numFiles
        self.remainFiles = numFiles
        
        # Set the gauge ranges
        self.gauge1.SetRange(self.totalProgress)
        self.gauge2.SetRange(self.totalProgOverall)
        
        # Set the overal progress label
        self.staticText2.SetLabel(_('Starting encoding process'))
        self.staticText2.SetLabel(_('Overall progress - %s files remain') %
            str(self.remainFiles))
            
        # Events
        self.button1.Bind(wx.EVT_BUTTON, self.abort)
        
        # Set the window size
        width = self.GetBestSize().x + 20
        height = self.GetBestSize().y + 20
        self.SetMinSize(wx.Size(width, height))
        self.SetClientSize(wx.Size(width, height))
        
    def doFile(self, message):
        "Advance the progress dialog 1 file, adjust all gauges"
        self.currProgress = 0
        self.remainFiles -= 1
        self.currProgOverall = self.totalProgOverall - \
            self.totalProgress * self.remainFiles 
        return self.doProgress(0, message)

    def doProgress(self, amount, message):
        "Advance the progress dialog in 1 step"
        # Increase the current progress
        self.currProgress += amount
        self.currProgOverall += amount
        # Check if we have finished with the current file
        if self.currProgress >= self.totalProgress:
            self.currProgress -= self.totalProgress
            self.remainFiles -= 1
        # Update the gauges
        #print("self.gauge1.SetValue %i, %i" % (self.currProgress, 100))
        self.gauge1.SetValue(self.currProgress)
        #print("self.gauge2.SetValue %i, %i" % (self.currProgOverall, 100))
        if self.currProgOverall < 101:
            self.gauge2.SetValue(self.currProgOverall)
        # Update the text messages
        self.staticText1.SetLabel(message)
        self.staticText2.SetLabel(_('Overall progress - %s files remain') %
            str(self.remainFiles))
        # Force the dialog to be refreshed
        self.Update()
        wx.Yield()
        # Return the abort flag
        return self.abortFlag
    
    def getCurrentProgress(self):
        "Returns the current progress"
        return self.currProgress
        
    def abort(self, event):
        "Stop encoding NOW!"
        # If None event we called it
        if (event is not None):
            event.StopPropagation()
        # Request for confirmation
        dialog = wx.MessageDialog(self, 
            _('Do you want to abort the encoding process?'), _('QUESTION'), 
            style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        confirmation = dialog.ShowModal()
        # Set the abort flag
        if confirmation == wx.ID_YES:
            self.abortFlag = True
            
        

