# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
# Name:         Globals.py
# Purpose:      Source file with global variables and functions.
#
# Author:       Félix Medrano Sanz
#
# Created:      
# RCS-ID:       $Id: Globals.py $
# Copyright:    (c) 2009 Félix Medrano Sanz
# Licence:      GPL v3
#----------------------------------------------------------------------------

import os
import glob
import stat
import sys
import string
import tempfile
import shutil
import importlib

import wx

import dpg4x.ConfigurationManager

if sys.platform == 'win32':
    import win32api

# Path to data files when packed in pyinstaller
# https://pyinstaller.readthedocs.io/en/stable/runtime-information.html
# https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller/404750#404750
if getattr(sys, 'frozen', False):
    application_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
else:
    application_path = os.path.dirname(sys.argv[0])
    # An rpm/deb installation has the data files in /usr/share
    if (application_path == '/usr/bin'):
        application_path = '/usr/share'

# Debug printouts to verify that files are included in exe file
#print('application_path:', application_path)

#icon_files=[(os.path.join(application_path, 'dpg4x', 'icons'), glob.glob(os.path.join(application_path, 'dpg4x', 'icons', '*.png')))]
#print("icon_files:", icon_files)

#i18n_files=[(os.path.join(application_path, 'dpg4x', 'i18n'), glob.glob(os.path.join(application_path, 'dpg4x', 'i18n', '*', '*')))]
#print("i18n_files:", i18n_files)

###############
## VARIABLES ##
###############

# Variable used to restart the program
restart = False

# Configuration files
FILECONFIG = [os.path.expanduser("~/.config/dpg4x/config.ini")]
# User config file
USERFILECONFIG = FILECONFIG[0]

# Temporary files
TMP_AUDIO = None
TMP_FIFO = None
TMP_VIDEO = None
TMP_HEADER = None
TMP_GOP = None
TMP_STAT = None
TMP_THUMB = None
TMP_SHOT = None
TMP_DIVX2PASS = None
	
# Option panels
mainPanel = None
filesPanel = None
videoPanel = None
audioPanel = None
subtitlesPanel = None
otherPanel = None

# Media Option panels
mediaMainPanel = None
mediaVideoPanel = None
mediaAudioPanel = None
mediaSubtitlesPanel = None
mediaOtherPanel = None

# General options
dpg_version = 4
dpg_quality = 'normal'
# Used to remember the last DVD/VCD device used
if sys.platform != 'win32':
    dpg_vcddevice = '/dev/cdrom'
    dpg_dvddevice = '/dev/dvd'
else:
    dpg_vcddevice = 'D:'
    dpg_dvddevice = 'D:'

# Video options
video_keepaspect = False
video_width = 256
video_height = 192
video_track = 0
video_autotrack = True
video_bitrate = 288
video_fps = 15
video_autofps = True
video_pixel = 3
# 0 RGB15
# 1 RGB18
# 2 RGB21
# 3 RGB24 

# Audio options
audio_codec = 'mp2'
audio_track = 0
audio_autotrack = True
audio_bitrate_mp2 = 128
audio_bitrate_vorbis = 128
audio_frequency = 32000
audio_normalize = False
audio_mono = False

# Subtitle options
subtitles_source = 'auto'
subtitles_track = 0
subtitles_file = ''
subtitles_font = 'Sans'
subtitles_encoding = sys.getfilesystemencoding()

# Other output
other_output = ''
if sys.platform != 'win32':
    other_temporary = '/tmp'
else:
    other_temporary = os.getenv('TEMP')
other_thumbnail = ''
other_previewsize = 10

###############
## FUNCTIONS ##
###############

def SetupTranslation():
    # Check if a gettext resource is available for the current LANG
    import locale
    import gettext

    # If no env variable defined, assume that i18n files are located below the top directory
    i18n_dir = os.getenv('DPG4X_I18N')
    if not(i18n_dir):
        i18n_dir = os.path.join(application_path, "dpg4x", "i18n")
        # gettext will search in default directories if no other path given
    if not os.path.isdir(i18n_dir):
        i18n_dir = None
                    
    if not gettext.find('dpg4x', i18n_dir) and sys.platform == 'win32':
        # On Windows this fails every time, no default Language environment
        # variables, but defaults to English.
        # locale.getdefaultlocale() returns ('en_US', 'cp1252') could be useful.
        os.environ['LANG']=locale.getdefaultlocale()[0]
    if not gettext.find('dpg4x', i18n_dir):
        debug('WARNING: dpg4x is not available in your language (%s), ' \
                'please help us to translate it.' % os.environ['LANG'])
        gettext.install('dpg4x', i18n_dir)
    else:
        # d0malaga f32:
        #        gettext.translation('dpg4x', i18n_dir).install(str=True)
        gettext.translation('dpg4x', i18n_dir).install()


def debug(message):
    "Shows a message in the error output"
    if not hasattr(sys, 'frozen'):
        # d0malaga f32:
        # sys.stderr.write((message+"\n").encode(sys.getfilesystemencoding(),'replace'))
        sys.stderr.write(message+"\n")
    # Exe file to be run from a DOS prompt 
    elif sys.frozen == "console_exe":
        sys.stderr.write(message+"\n")
    else:
        # sys.frozen == "windows_exe":
        # py2exe programs without a console writes stderr to a log file in the installation
        # directory. this is not recommended if the program is installed in C:\Program files
        # (or even allowed for non admin users on Windows 7). 
        # see also: http://www.py2exe.org/index.cgi/StderrLog
        global other_temporary
        f = os.path.join(other_temporary, 'dpg4x.log')
        fd = open(f,"a")
        fd.write(message+"\n")
        fd.close()

def Encode(text):
    """TBD: verify how much this neeeded in Python 3:
    Encode text to be system-encoding compatible"""
    if isinstance(text, str):
        return text

    return text.encode(sys.getfilesystemencoding(),'replace')

def Decode(text):
    """TBD: verify how much this neeeded in Python 3:
      Decode text to be system-encoding compatible"""
    if isinstance(text, str):
        return text

    #print("Decoding: %s" % text)
    e = sys.getfilesystemencoding() or 'utf-8'
    #print("Using system encoding: %s" % e)
    r = text.decode(e,'replace')
    #print("result: %s" % r1)
    return r

# Note: subprocess.Popen doesn't support unicode options arguments
# (http://bugs.python.org/issue1759845) so we have to encode them.
def ListUnicodeEncode(list):
    "Run through the given list and encode unicode items"
    encoded_list = []
    for item in list:
        # Handle East Asian characters by avoiding them
        if os.path.isfile(item) and sys.platform == 'win32':
            item = win32api.GetShortPathName(item)
        if isinstance(item, str):
            item = Encode(item)
        encoded_list.append(item)  
    return encoded_list
        
def getIconDir():
    "Returns the path to the icon files"
    icon_dir = os.getenv('DPG4X_ICONS')
    # If no env variable defined, assume that icons are located below the top directory
    if not(icon_dir):
        icon_dir = os.path.join(application_path,  "dpg4x", "icons")
    return icon_dir

def CreateFolder(dir):
    "Create a folder with full path"
    if not os.path.isdir(dir):
        chunks = dir.split("/")
        subchunk = "/"
        for chunk in chunks:
            subchunk = os.path.join(subchunk, chunk)
            if not os.path.isdir(subchunk):
                #os.mkdir(subchunk, stat.S_IRWXU) UMASK?
                os.mkdir(subchunk)

# Stolen from Noah Spurrier's pexpect. Thank you Noah!
# Pexpect it's a great library and I use it often. 
# But now, I just need this function, so I'll try to save on dependencies...
def which (filename):

    """This takes a given filename; tries to find it in the environment path;
    then checks if it is executable. This returns the full path to the filename
    if found and executable. Otherwise this returns None."""

    # On Windows, we need to make sure we add the .exe extension otherwise
    # this test always fails.
    if sys.platform == 'win32':
        filename = filename + '.exe'

    # Special case where filename already contains a path.
    if os.path.dirname(filename) != '':
        if os.access (filename, os.X_OK):
            return filename

    if 'PATH' not in os.environ or os.environ['PATH'] == '':
        p = os.defpath
    else:
        p = os.environ['PATH']

    # Oddly enough this was the one line that made Pexpect
    # incompatible with Python 1.5.2.
    # d0malaga f32:
    # pathlist = string.split (p, os.pathsep)
    pathlist = p.split (os.pathsep)

    for path in pathlist:
        f = os.path.join(path, filename)
        if os.access(f, os.X_OK):
            return f
    if sys.platform == 'win32':
        return windows_extend_path(filename)
    return None

def windows_extend_path(filename):
    """ Searches for program name in:
        1) Directory below dpg4x directory
        2) %ProgramFiles% 
    and extends path with first match if found """ 
    import glob
    d = glob.glob(os.path.join(os.path.dirname(sys.argv[0]), '*', filename))
    if d:
        os.environ['PATH'] = os.getenv('PATH') + os.pathsep + os.path.dirname(d[0])
        return d[0]
    d = glob.glob(os.path.join(os.getenv('ProgramFiles'), '*', filename))
    if d:
        os.environ['PATH'] = os.getenv('PATH') + os.pathsep + os.path.dirname(d[0])
        return d[0]
    return None

def concat(out,*files):
    "Concatenate a list of files"
    # Be sure to use 'b' or Windows just destroys binary files and the final
    # .dpg output is junk.
    outfile = open(out,'wb')
    for name in files:
        outfile.write( open(name,'rb').read() )
    outfile.close()
    
def fillString(string, length):
    "Fills a string with spaces until length is reached"
    stringAux = string
    while len(stringAux) < length:
        stringAux = ' ' + stringAux
        if len(stringAux) < length:
            stringAux = stringAux + ' '
    return stringAux

def shell():
    "Decides if shell should be enabled"
    if sys.platform == 'win32':
        return True
    else:
        return False
    
def createTemporary():
    "Create the temporary files needed to encode"
    
    # Folder for the temporary files
    global other_temporary
    tmpDir = other_temporary
    
    # Audio temporary file
    global TMP_AUDIO
    fd,TMP_AUDIO = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
    # Audio temporary fifo - maybe there is a better way to do it...
    global TMP_FIFO
    fd,TMP_FIFO = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
    os.remove(TMP_FIFO)
    # os.mkfifo does not work on Windows and causes the script to fail.
    # Should use os.pipe() instead. I never need this though.
    if sys.platform != 'win32':
        os.mkfifo(TMP_FIFO,0o600)
    # Video temporary file
    global TMP_VIDEO
    fd,TMP_VIDEO = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
    # Header temporary file
    global TMP_HEADER
    fd,TMP_HEADER = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
    # GOP offsets temporaries
    # Only needed with dpg_version >= 2
    global dpg_version
    global TMP_GOP
    global TMP_STAT
    if dpg_version >= 2:
        fd,TMP_GOP = tempfile.mkstemp(dir=tmpDir)
        os.close(fd)
    # TMP_STAT always needed for frames calculation
    fd,TMP_STAT = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
    # Thumbnail temporary files
    global other_thumbnail
    global TMP_THUMB
    global TMP_SHOT
    fd,TMP_THUMB = tempfile.mkstemp(dir=tmpDir)
    os.close(fd)
    # Only needed on autogenerate
    if not other_thumbnail:
        # On Windows tempfile.mkdtemp() creates a path like:
        # /tmp\tmpyr6x2v
        # While tempfile.mkstemp() creates a path like:
        # C:\tmp\tmpyr6x2v
        # If we do not use tempfile.mkstemp(), wx.Image() fails later
        # http://bugs.python.org/issue7325
        fd,TMP_SHOT = tempfile.mkstemp(dir=tmpDir)
        os.close(fd)
        os.remove(TMP_SHOT)
        os.makedirs(TMP_SHOT)
    # Divx 2-pass log file
    # Only needed for very high quality encode
    global TMP_DIVX2PASS
    if dpg_quality == 'doublepass':
        fd,TMP_DIVX2PASS = tempfile.mkstemp(dir=tmpDir)
        os.close(fd)
        os.remove(TMP_DIVX2PASS)
        os.makedirs(TMP_DIVX2PASS)
        
def clearTemporary():
    "Delete the temporary files"

    try:
        # Audio temporary file
        global TMP_AUDIO
        if TMP_AUDIO and os.path.isfile(TMP_AUDIO):
            os.remove(TMP_AUDIO)
        # Audio temporary fifo
        global TMP_FIFO
        if TMP_FIFO and os.path.exists(TMP_FIFO):
            os.remove(TMP_FIFO)
        # Video temporary file
        global TMP_VIDEO
        if TMP_VIDEO and os.path.isfile(TMP_VIDEO):
            os.remove(TMP_VIDEO)
        # Header temporary file
        global TMP_HEADER
        if TMP_HEADER and os.path.isfile(TMP_HEADER):
            os.remove(TMP_HEADER)
        # GOP offsets temporaries
        global TMP_GOP
        global TMP_STAT
        if TMP_GOP and os.path.isfile(TMP_GOP):
            os.remove(TMP_GOP)
        if TMP_STAT and os.path.isfile(TMP_STAT):
            os.remove(TMP_STAT)
        # Thumbnail temporary files
        global TMP_THUMB
        global TMP_SHOT
        if TMP_THUMB and os.path.isfile(TMP_THUMB):
            os.remove(TMP_THUMB)
        # Note that TMP_SHOT is a folder, not a file
        if TMP_SHOT and os.path.isdir(TMP_SHOT):
            # On Windows shutil.rmtree() fails on read-only directories
            if sys.platform == 'win32':
                os.chmod(TMP_SHOT, stat.S_IWUSR)
            shutil.rmtree(TMP_SHOT, ignore_errors = True)
        # Same with TMP_DIVX2PASS
        global TMP_DIVX2PASS
        if TMP_DIVX2PASS and os.path.isdir(TMP_DIVX2PASS):
            if sys.platform == 'win32':
                os.chmod(TMP_SHOT, stat.S_IWUSR)
            shutil.rmtree(TMP_DIVX2PASS, ignore_errors = True)
            
    # Warn if there is a problem when deleting files
    except Exception as e:
        debug(_('WARNING: Temporary files were not properly deleted:') + '' \
            ' ' + str(e.args[0]))
            
            
# Load the configuration file
importlib.reload(dpg4x.ConfigurationManager)
dpg4x.ConfigurationManager.loadConfiguration()
