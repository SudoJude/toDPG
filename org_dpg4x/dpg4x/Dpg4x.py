#----------------------------------------------------------------------------
# Name:         Dpg4x.py
# Purpose:      A dpg encoder for Linux (and maybe others).
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Dpg4x.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import sys
import os
import importlib

# On Windows wxPython 2.9.1.1 works better than 2.8.11.0.
# In particuliar OutputTextDialog() is unreadable and unusable. You can only
# see the first couple of letters of the text and the close button is missing.

# d0malaga f32:
# https://wxpython.org/Phoenix/docs/html/MigrationGuide.html: wxversion is gone
'''
# wxPython running from py2exe fails with wxversion.select()
# See: http://www.wxpython.org/docs/api/wxversion-module.html
if not hasattr(sys, 'frozen'):
    import wxversion
    wxversion.select(['2.8','2.9'])
'''
import wx

import dpg4x.Globals as Globals
import dpg4x.MainFrame
from dpg4x.DpgThumbnail import DpgThumbnail
import dpg4x.Encoder

modules ={'AddDvdDialog': [0,
                   'A dialog to add Dvd media sources.',
                   'AddDvdDialog.py'],
 'AddVcdDialog': [0,
                   'A dialog to add Vcd media sources.',
                   'AddVcdDialog.py'],
 'AudioPanel': [0, 'Panel with audio options.', 'AudioPanel.py'],
 'ConfigurationManager': [0,
                           'Manages the configuration variables.',
                           'ConfigurationManager.py'],
 'CustomFontSelector': [0,
                         'Dialog to select fonts (only faces).',
                         'CustomFontSelector.py'],
 'CustomProgressDialog': [0,
                           'Dialog to show the progress of the encoding.',
                           'CustomProgressDialog.py'],
 'DpgHeader': [0, 'DPG header management.', 'DpgHeader.py'],
 'DpgInfoDialog': [0,
                    'Dialog with a thumbail image and TextCtrls to show DPG info.',
                    'moreControls/DpgInfoDialog.py'],
 'DpgThumbnail': [0, 'Class to handle DPG thumbnails.', 'DpgThumbnail.py'],
 'Encoder': [0, 'Performs the encoding duties.', 'Encoder.py'],
 'FilesPanel': [0, 'Panel with files to be encoded.', 'FilesPanel.py'],
 'Globals': [0,
              'Source file with global variables and functions.',
              'Globals.py'],
 'MainFrame': [1, 'Main frame of Application.', 'MainFrame.py'],
 'MediaAudioPanel': [0,
                      'Panel with per-media audio options.',
                      'MediaAudioPanel.py'],
 'MediaMainFrame': [0,
                     'Frame with per-media settings.',
                     'MediaMainFrame.py'],
 'MediaOtherPanel': [0,
                      'Panel with per-media aditional options.',
                      'MediaOtherPanel.py'],
 'MediaSubtitlesPanel': [0,
                          'Panel with per-media subtitle options.',
                          'MediaSubtitlesPanel.py'],
 'MediaVideoPanel': [0,
                      'Panel with per-media video options.',
                      'MediaVideoPanel.py'],
 'OtherPanel': [0, 'Panel with aditional options.', 'OtherPanel.py'],
 'OutputTextDialog': [0,
                       "Dialog with a TextCtrl to show program's output.",
                       'moreControls/OutputTextDialog.py'],
 'Previewer': [0, 'Allows advanced preview options.', 'Previewer.py'],
 'SubtitlesPanel': [0, 'Panel with subtitle options.', 'SubtitlesPanel.py'],
 'TreeCtrlComboPopup': [0,
                         'Popup control containing a TreeCtrl.',
                         'TreeCtrlComboPopup.py'],
 'VideoPanel': [0, 'Panel with video options.', 'VideoPanel.py']}
    
def checkDependencies():
    "Check that the mandatory dependecies are present"
    # Mandatory programs
    mandatory = ['mplayer','mencoder']
    # Check that all of them are present
    for program in mandatory:
        if not Globals.which(program):
            message = _('%s not found in PATH. Please install it.') % program
            # Show an error in the console
            Globals.debug(_('ERROR') + ': ' + message)
            # Show a dialog to the user
            dialog = wx.MessageDialog(None, message, _('ERROR'), style=wx.OK|wx.ICON_ERROR)
            dialog.ShowModal()
            sys.exit(1)

def checkArgs():
    usage=_("""Usage: dpg4x [options] file1 file2... (starts GUI if no options)

Options:
  -h, --help        show this help message and exit
  --thumbnail=FILE  use image file as thumbnail in DPG files
  --dpg             convert files to DPG, using settings from GUI
  --avi             convert DPG files to AVI, no transformation
""")

    # Naive parser because optparse does not support i18n
    options_image = None
    options_avi = False
    options_dpg = False
    args = []
    for arg in sys.argv[1:]:
        if arg == '--dpg':
            options_dpg = True
        elif arg == '--avi':
            options_avi = True
        elif arg.startswith('--thumbnail='): 
            options_image = arg.split('=')[1]
        elif arg == '-h' or arg == '--help':
            Globals.debug(usage)
            return False,[]
        elif arg.startswith('-'):
            Globals.debug(_('Non supported option: %s') % arg)
            Globals.debug(usage)
            return False,[]
        else:
            args += [arg]

    if len(args)>0:
        try:
            if options_image:
                thumb = DpgThumbnail(options_image)
                for a in args:
                    a = Globals.Decode(a)
                    Globals.debug(a)
                    thumb.inject(a)
                return False,[]
            elif options_avi:
                for a in args:
                    a = Globals.Decode(a)
                    Globals.debug(a)
                    dpg4x.Encoder.encode_Dpg2Avi(a)
                    return False,[]
            elif options_dpg:
                for a in args:
                    a = Globals.Decode(a)
                    Globals.debug(a)
                    dpg4x.Encoder.encode_files([a])
                return False,[]
        except Exception as e:
            Globals.debug(_('ERROR') + ': ' + str(e.args[0]))
            return False,[]
    return True, args

def main():
    Globals.SetupTranslation()
    checkDependencies()
    application = wx.App(redirect=False,clearSigInt=False)
    firstExec,filesToLoad = checkArgs()
    while firstExec or Globals.restart:
        # Reload the Globals module on restart
        if Globals.restart:
            importlib.reload(Globals)
        firstExec = False
        mainFrame = dpg4x.MainFrame.create(None, Globals.getIconDir())
        mainFrame.Show()
        Globals.mainPanel = mainFrame
        if filesToLoad:
            Globals.filesPanel.addFilesFromList(filesToLoad)
        application.SetTopWindow(mainFrame)
        application.MainLoop()
    sys.exit(0)

# Main function
if __name__ == '__main__':
    main()
