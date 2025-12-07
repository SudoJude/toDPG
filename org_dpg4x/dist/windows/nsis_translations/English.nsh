# Language: English
# Language strings for the Windows Dpg4x NSIS installer.
#
#Save file as UTF-8 w/ BOM
#

!insertmacro LANGFILE_EXT "English"

# Update checks
${LangFileString} ALREADY_INSTALLED "${Name} is already installed"

# Start menu entries
${LangFileString} UninstallLink "Uninstall ${Name}"
${LangFileString} WebLink "${Name} on the web"

# MPlayer Section
${LangFileString} MPLAYER_IS_DOWNLOADING "Downloading MPlayer..."
${LangFileString} MPLAYER_DL_RETRY "MPlayer was not successfully installed. Retry?"
${LangFileString} MPLAYER_DL_FAILED "Failed to download MPlayer: '$R0'."
${LangFileString} MPLAYER_INST_FAILED "Failed to install MPlayer, needed for encoding. Please install separately."
${LangFileString} APPLICATION_DESCRIPTION "DPG encoder GUI - encodes videos for the Nintendo DS player moonshell"
