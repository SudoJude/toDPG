# Language: Swedish
# Language strings for the Windows Dpg4x NSIS installer.
#
#Save file as UTF-8 w/ BOM
#

!insertmacro LANGFILE_EXT "Swedish"

# Update checks
${LangFileString} ALREADY_INSTALLED "${Name} är redan installerad"

# Start menu entries
${LangFileString} UninstallLink "Avinstallera ${Name}"
${LangFileString} WebLink "${Name} websida"

# MPlayer Section
${LangFileString} MPLAYER_IS_DOWNLOADING "Laddar ned MPlayer..."
${LangFileString} MPLAYER_DL_RETRY "MPlayer kunde inte installeras, nytt försök?"
${LangFileString} MPLAYER_DL_FAILED "Kunde ej ladda ned MPlayer: '$R0'."
${LangFileString} MPLAYER_INST_FAILED "Kunde ej installera MPlayer som behövs för konvertering. Du behöver installera MPlayer separat."
${LangFileString} APPLICATION_DESCRIPTION "Kodar om video till DPG - ett format som spelas av Nintendo DS mediaspelare moonshell"
