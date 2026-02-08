# Language: French
# Language strings for the Windows Dpg4x NSIS installer.
#
#Save file as UTF-8 w/ BOM
#

!insertmacro LANGFILE_EXT "French"

# Update checks
${LangFileString} ALREADY_INSTALLED "${Name} est déjà installé"

# Start menu entries
${LangFileString} UninstallLink "Désinstallation de ${Name}"
${LangFileString} WebLink "${Name} sur internet"

# MPlayer Section
${LangFileString} MPLAYER_IS_DOWNLOADING "Téléchargement  de MPlayer"
${LangFileString} MPLAYER_DL_RETRY "MPlayer n'est pas correctement installé. Recommencer ?"
${LangFileString} MPLAYER_DL_FAILED "Échec du téléchargement de MPlayer : '$R0'."
${LangFileString} MPLAYER_INST_FAILED "Échec de l'installation de MPlayer, requis pour l'encodage. SVP installez-le séparément."
${LangFileString} APPLICATION_DESCRIPTION "Interface d'encodage DPG - Codeur vidéo pour lecteur moonshell de la Nintendo DS"
