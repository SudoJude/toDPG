# This file contains the language specific settings.
# If you add a new translation you should define the new language here.

# Installer languages
!insertmacro MUI_LANGUAGE English
!insertmacro MUI_LANGUAGE French
!insertmacro MUI_LANGUAGE Spanish
!insertmacro MUI_LANGUAGE Swedish
!insertmacro MUI_LANGUAGE Catalan

# Custom translations for setup
# UMUI modified LANGFILE_INCLUDE macro to take another file too, see Contrib/UltraModernUI/UMUI.nsh
!insertmacro LANGFILE_INCLUDE "nsis_translations\English.nsh" "nsis_translations\UMUI.nsh"
!insertmacro LANGFILE_INCLUDE "nsis_translations\French.nsh" "nsis_translations\UMUI.nsh"
!insertmacro LANGFILE_INCLUDE "nsis_translations\Spanish.nsh" "nsis_translations\UMUI.nsh"
!insertmacro LANGFILE_INCLUDE "nsis_translations\Swedish.nsh" "nsis_translations\UMUI.nsh"
!insertmacro LANGFILE_INCLUDE "nsis_translations\Catalan.nsh" "nsis_translations\UMUI.nsh"
