#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python script to find all installer translations and generate files:
# - NSIS installer for Windows
# - desktop entry for Linux
#
# The files are created in the current directory and should be copied
# to their real directoties

import sys
import os
import gettext
import glob
import babel

translation = u"""# Language: %s
# Language strings for the Windows Dpg4x NSIS installer.
#
#Save file as UTF-8 w/ BOM
#

!insertmacro LANGFILE "%s" "%s"

# Update checks
${LangFileString} ALREADY_INSTALLED "%s"

# Start menu entries
${LangFileString} UninstallLink "%s"
${LangFileString} WebLink "%s"

# MPlayer Section
${LangFileString} MPLAYER_IS_DOWNLOADING "%s"
${LangFileString} MPLAYER_DL_RETRY "%s"
${LangFileString} MPLAYER_DL_FAILED "%s"
${LangFileString} MPLAYER_INST_FAILED "%s"
${LangFileString} APPLICATION_DESCRIPTION "%s"
"""

def nsis_language(lang, translatedLang):
    """ Creates one NSIS translation file """
    fd = open(lang + '.nsh', 'w+')
    o = translation % (lang, lang, translatedLang,
                            _(u"${Name} is already installed"), 
                            _(u"Uninstall ${Name}"), 
                            _(u"${Name} on the web"), 
                            _(u"Downloading MPlayer..."), 
                            _(u"MPlayer was not successfully installed. Retry?"), 
                            _(u"Failed to download MPlayer: '$R0'."),
                            _(u"Failed to install MPlayer, needed for encoding. Please install separately."),
                           _(u"DPG encoder GUI - encodes videos for the Nintendo DS player moonshell"))
    fd.write(o.encode('UTF-8'))
    fd.close()
    

def nsis_translations():
    """ Find all translations and generate NSIS files """
    langList = []
    i18n_dir = "./.."
    for f in glob.glob(os.path.join(i18n_dir, '*', "LC_MESSAGES", "dpg4x_installer.mo")):
        l = os.path.basename(os.path.dirname(os.path.dirname(f)))
        print "NSIS:", l, f
        lang = gettext.translation('dpg4x_installer', i18n_dir, languages=[l])
        # print lang.info()
        lang.install(unicode=True)
        locale = babel.Locale(l)
        e = locale.english_name
        nsis_language(e, locale.display_name)
        langList.append(e)
        
    # Define a main file listing all translations
    fd = open('translations.nsh', 'w+')
    fd.write("""# This file contains the language specific settings.
# If you add a new translation you should define the new language here.

# Installer languages\n""")
    for l in langList:
        fd.write("!insertmacro MUI_LANGUAGE %s\n" % l)
    fd.write("\n# Custom translations for setup\n")    
    for l in langList:
        fd.write('!insertmacro LANGFILE_INCLUDE "nsis_translations\%s.nsh"\n' % l)
    fd.close()    

def generate_desktop_file():
    langList = []
    i18n_dir = ".."
    # Find all translations
    for f in glob.glob(os.path.join(i18n_dir, '*', "LC_MESSAGES", "dpg4x_installer.mo")):
        l = os.path.basename(os.path.dirname(os.path.dirname(f)))
        print "dpg4x.desktop:", l, f
        lang = gettext.translation('dpg4x_installer', i18n_dir, languages=[l])
        # print lang.info()
        lang.install(unicode=True)
        longname = _(u'DPG4X Video Encoder')
        comment = _(u'DPG encoder GUI - encodes videos for the Nintendo DS player moonshell')
        genericname = _(u'Video Encoder')
        langList.append((l, longname, comment, genericname))
 
    fd = open('dpg4x.desktop', 'w+')
    fd.write(u'[Desktop Entry]\n')
    for (l,ln,c,gn) in langList:
        if l == "en":
            fd.write((u'Name=%s\n' % ln).encode('utf-8'))
        else:
            fd.write((u'Name[%s]=%s\n' % (l,ln)).encode('utf-8'))
    for (l,ln,c,gn) in langList:
        if l == "en":
            fd.write((u'Comment=%s\n' % c).encode('utf-8'))
        else:
            fd.write((u'Comment[%s]=%s\n' % (l,c)).encode('utf-8'))
    for (l,ln,c,gn) in langList:
        if l == "en":
            fd.write((u'GenericName=%s\n' % gn).encode('utf-8'))
        else:
            fd.write((u'GenericName[%s]=%s\n' % (l,gn)).encode('utf-8'))
    fd.write(u"""Icon=dpg4x
Exec=dpg4x
Terminal=false
Type=Application
Categories=AudioVideo;AudioVideoEditing;
\n""")    
    fd.close()    
        
                
        
# Main function
if __name__ == '__main__':
    nsis_translations()
    generate_desktop_file()
    
    
