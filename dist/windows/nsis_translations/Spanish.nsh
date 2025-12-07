# Language: Spanish
# Language strings for the Windows Dpg4x NSIS installer.
#
#Save file as UTF-8 w/ BOM
#

!insertmacro LANGFILE_EXT "Spanish"

# Update checks
${LangFileString} ALREADY_INSTALLED "${Name} ya está instalado"

# Start menu entries
${LangFileString} UninstallLink "Desinstalar ${Name}"
${LangFileString} WebLink "${Name} en la web"

# MPlayer Section
${LangFileString} MPLAYER_IS_DOWNLOADING "Descargando MPlayer..."
${LangFileString} MPLAYER_DL_RETRY "MPlayer no se ha instalado correctamente. ¿Quiere intentarlo de nuevo?"
${LangFileString} MPLAYER_DL_FAILED "Ha fallado la descarga de MPlayer: '$R0'."
${LangFileString} MPLAYER_INST_FAILED "No se pudo instalar MPlayer. Debe instalarlo de forma separada o no podrá codificar vídeos."
${LangFileString} APPLICATION_DESCRIPTION "Codificador de vídeos DPG - crea vídeos para el reproductor de Nintendo DS moonshell"
