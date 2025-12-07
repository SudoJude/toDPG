# NSIS definitions for dpg4
!define VERSION "3.0"
!define RELEASE "1"
!define UMUI_VERSION "${VERSION}-${RELEASE}"
!define /date NOW "%Y-%m-%d"
!define UMUI_VERBUILD "1.0_${NOW}"

# Must contain four parts, used for internal comparisons of patch levels
!define  VIProduct_Ver "${VERSION}.${RELEASE}.0"

Name dpg4x
# Needed because $(^Name) sometimes does not seem to expand correctly
!define NAME dpg4x
!define PROGRAM_FILE dpg4x_main.exe

# Only tested on Win10 so far: Win7|Win8|Win8.1|Win10
ManifestSupportedOS "Win10"

# General Symbol Definitions
!define REGKEY "SOFTWARE\${Name}"
!define CLIENT_REGKEY "SOFTWARE\CLIENTS\MEDIA\${Name}"
!define COMPANY "Dpg4x Sourceforge project"
!define URL http://sourceforge.net/projects/dpg4x/

# Dependencies: Visual C libraries are installed
#!define DLLMSVC dependencies\vc_redist.x86.exe
#!define DLLMSVC dependencies\vc_redist.x64.exe
!define DLLMSVC dependencies\vc_redist.*.exe
# Seems to have changed in Win10 (not needed any longer, but older windowses needs this)
# install https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/
# copy all dlls from C:\Program Files (x86)\Windows Kits\10\Redist\10.0.19041.0\ucrt\DLLs\x86
# and/or C:\Program Files (x86)\Windows Kits\10\Redist\10.0.19041.0\ucrt\DLLs\x64 (or maybe arm...)

# Dependencies: mplayer and encoder are installed by downloading from the SourceForge
# project: MPlayer for Win32 / Win64
!define MPLAYER_URL_REV r38188%2Bg6e1903938b
!define MPLAYER_FILE_REV r38188+g6e1903938b
!define MPLAYER_SRC MPlayer-x86_64-${MPLAYER_URL_REV}
# '+' encoded as %2B in url and saved download, but unpacks as '+'
!define MPLAYER_URLREV r38188+g6e1903938b
!define MPLAYER_target MPlayer-x86_64-${MPLAYER_FILE_REV}
!define MPLAYER7Z dependencies\${MPLAYER_target}.7z
# Latest July 2020: http://downloads.sourceforge.net/project/mplayer-win32/MPlayer%20and%20MEncoder/r38188%2Bg6e1903938b/MPlayer-x86_64-r38188%2Bg6e1903938b.7z
# http://sourceforge.net/projects/mplayer-win32/files/MPlayer%20and%20MEncoder/r38188%2Bg6e1903938b/MPlayer-x86_64-r38188%2Bg6e1903938b.7z/download
!define MPLAYER_URL "http://sourceforge.net/projects/mplayer-win32/files/MPlayer%20and%20MEncoder/r38188%2Bg6e1903938b/MPlayer-x86_64-r38188%2Bg6e1903938b.7z/download?use_mirror=autoselect"

# Installer attributes
Unicode True
OutFile "..\${NAME}-${UMUI_VERSION}_user_setup.exe"
Caption "${NAME} ${VIProduct_Ver}"
InstallDir $PROGRAMFILES\${NAME}
CRCCheck on
XPStyle on
ShowInstDetails show
VIProductVersion "${VIProduct_Ver}"
VIAddVersionKey ProductName "${Name}"
VIAddVersionKey ProductVersion "${VERSION}"
VIAddVersionKey CompanyName "${COMPANY}"
VIAddVersionKey CompanyWebsite "${URL}"
VIAddVersionKey FileVersion "${VERSION}"
VIAddVersionKey FileDescription ""
VIAddVersionKey LegalCopyright ""
#InstallDirRegKey HKLM "${REGKEY}" Path
ShowUninstDetails show
# Vista+ XML manifest, does not affect older OSes
RequestExecutionLevel user

# MUI Symbol Definitions
!define MUI_ICON ${NAME}.ico
!define MUI_WELCOMEFINISHPAGE_BITMAP "installer_${NAME}.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "installer_${NAME}.bmp"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "SHCTX"
!define MUI_STARTMENUPAGE_REGISTRY_KEY ${REGKEY}
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME StartMenuGroup
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "${Name}"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall-colorful.ico"
!define MUI_UNFINISHPAGE_NOAUTOCLOSE
!define MUI_LICENSEPAGE_RADIOBUTTONS

!define MUI_FINISHPAGE_NOAUTOCLOSE

#!define MUI_FINISHPAGE_LINK "${URL}"
#!define MUI_FINISHPAGE_LINK_LOCATION "${URL}"

;--------------------------------
;Included files
!include Sections.nsh
!include UMUI.nsh
# LangFile.sh already included in UMUI file
#!include LangFile.nsh
!include WordFunc.nsh
!include FileFunc.nsh


;--------------------------------
;Interface Settings

  !define UMUI_SKIN "blue"

  !define UMUI_USE_INSTALLOPTIONSEX

  !define MUI_ABORTWARNING
  !define MUI_UNABORTWARNING

  !define UMUI_PAGEBGIMAGE
  !define UMUI_UNPAGEBGIMAGE

  !define UMUI_USE_ALTERNATE_PAGE ; For Welcome finish abort pages
  !define UMUI_USE_UNALTERNATE_PAGE

  !define MUI_COMPONENTSPAGE_SMALLDESC

  !define UMUI_DEFAULT_SHELLVARCONTEXT all

  !define UMUI_ENABLE_DESCRIPTION_TEXT

;--------------------------------
;Registry Settings

  !define UMUI_PARAMS_REGISTRY_ROOT HKCU
  !define UMUI_TEXT_SHELL_VAR_CONTEXT current
  !define UMUI_PARAMS_REGISTRY_KEY "${REGKEY}"

  !define UMUI_LANGUAGE_REGISTRY_VALUENAME "UMUI_InstallerLanguage"
  !define UMUI_SHELLVARCONTEXT_REGISTRY_VALUENAME "UMUI_ShellVarContext"

  !define UMUI_UNINSTALLPATH_REGISTRY_VALUENAME "UMUI_UninstallPath"
  !define UMUI_UNINSTALL_FULLPATH "$INSTDIR\Uninstall.exe"
  !define UMUI_INSTALLERFULLPATH_REGISTRY_VALUENAME "UMUI_InstallPath"

  !define UMUI_VERSION_REGISTRY_VALUENAME "UMUI_Version"
  !define UMUI_VERBUILD_REGISTRY_VALUENAME "UMUI_VerBuild"

  !define UMUI_PREUNINSTALL_FUNCTION preuninstall_function

  InstallDirRegKey ${UMUI_PARAMS_REGISTRY_ROOT} "${UMUI_PARAMS_REGISTRY_KEY}" ""

;--------------------------------
;Reserve Files

  !insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

# Variables
Var StartMenuGroup

;--------------------------------
;Pages

  !insertmacro UMUI_PAGE_MULTILANGUAGE

    !define UMUI_MAINTENANCEPAGE_MODIFY
    !define UMUI_MAINTENANCEPAGE_REPAIR
    !define UMUI_MAINTENANCEPAGE_REMOVE
    !define UMUI_MAINTENANCEPAGE_CONTINUE_SETUP
  !insertmacro UMUI_PAGE_MAINTENANCE

    !define UMUI_UPDATEPAGE_REMOVE
    !define UMUI_UPDATEPAGE_CONTINUE_SETUP
  !insertmacro UMUI_PAGE_UPDATE

    !define UMUI_WELCOMEPAGE_ALTERNATIVETEXT
  !insertmacro MUI_PAGE_WELCOME

    !define MUI_LICENSEPAGE_CHECKBOX
  !insertmacro MUI_PAGE_LICENSE "..\..\LICENSE"

    #!define UMUI_INFORMATIONPAGE_USE_RICHTEXTFORMAT
  !insertmacro UMUI_PAGE_INFORMATION "..\..\README"

    !define UMUI_SETUPTYPEPAGE_STANDARD "$(UMUI_TEXT_SETUPTYPE_STANDARD_TITLE)"
    !define UMUI_SETUPTYPEPAGE_DEFAULTCHOICE ${UMUI_STANDARD}
    !define UMUI_SETUPTYPEPAGE_REGISTRY_VALUENAME "UMUI_SetupType"
  !insertmacro UMUI_PAGE_SETUPTYPE

    !define UMUI_COMPONENTSPAGE_INSTTYPE_REGISTRY_VALUENAME "UMUI_InstType"
    !define UMUI_COMPONENTSPAGE_REGISTRY_VALUENAME "UMUI_Components"
  !insertmacro MUI_PAGE_COMPONENTS

  !insertmacro MUI_PAGE_DIRECTORY

    !define UMUI_ADDITIONALTASKS_REGISTRY_VALUENAME "UMUI_Tasks"
  !insertmacro UMUI_PAGE_ADDITIONALTASKS addtasks_function

  !insertmacro UMUI_PAGE_ALTERNATIVESTARTMENU Application $StartMenuGroup

    !define UMUI_CONFIRMPAGE_TEXTBOX confirm_function
  !insertmacro UMUI_PAGE_CONFIRM

  !insertmacro MUI_PAGE_INSTFILES

    !define MUI_FINISHPAGE_LINK "DPG4x Home Page"
    !define MUI_FINISHPAGE_LINK_LOCATION "${URL}"
  !insertmacro MUI_PAGE_FINISH

    !define UMUI_ABORTPAGE_LINK "DPG4x Home Page"
    !define UMUI_ABORTPAGE_LINK_LOCATION "${URL}"
  !insertmacro UMUI_PAGE_ABORT


  !insertmacro UMUI_UNPAGE_MULTILANGUAGE

    !define UMUI_MAINTENANCEPAGE_MODIFY
    !define UMUI_MAINTENANCEPAGE_REPAIR
    !define UMUI_MAINTENANCEPAGE_REMOVE
    !define UMUI_MAINTENANCEPAGE_CONTINUE_SETUP
  !insertmacro UMUI_UNPAGE_MAINTENANCE

  !insertmacro MUI_UNPAGE_WELCOME

  !insertmacro MUI_UNPAGE_CONFIRM

  !insertmacro MUI_UNPAGE_INSTFILES

    !define MUI_FINISHPAGE_LINK "DPG4X Home Page"
    !define MUI_FINISHPAGE_LINK_LOCATION "${URL}"
  !insertmacro MUI_UNPAGE_FINISH

    !define UMUI_ABORTPAGE_LINK "DPG4x Home Page"
    !define UMUI_ABORTPAGE_LINK_LOCATION "${URL}"
  !insertmacro UMUI_UNPAGE_ABORT

;--------------------------------
;Languages
!include nsis_translations\translations.nsh

;--------------------------------
;Installer Types

InstType "$(UMUI_TEXT_SETUPTYPE_STANDARD_TITLE)"

;--------------------------------
;Installer Sections

Section "Dpg4x core (required)" SECDpg4x

    SetDetailsPrint textonly
    DetailPrint "Installing DPG4x Core Files..."
    SetDetailsPrint listonly
	SetShellVarContext current

	SectionIn 1 2 RO

    SetOutPath $INSTDIR
    SetOverwrite on
    File ..\..\dist\dpg4x_main.exe
	# Doc to consider later
    #File /r ..\dist\doc
    # icons, translations included in exe file by pyinstaller
	#File /r ..\dist\i18n
    #File /r ..\dist\icons
    SetOutPath $INSTDIR\dependencies
    File /r ${DLLMSVC}
    File /r dependencies\README.txt
	File /r dependencies\download_mplayer.ps1
SectionEnd

!macro PowerShellExecFileMacro PSFile Arg0 Arg1
  !define PSExecID ${__LINE__}
  Push $R0
 
  nsExec::ExecToStack 'powershell -inputformat none -ExecutionPolicy RemoteSigned -File "${PSFile}" "${Arg0}" "${Arg1}"'
 
  Pop $R0 ;return value is first on stack
  ;script output is second on stack, leave on top of it
  IntCmp $R0 0 finish_${PSExecID}
  SetErrorLevel 2
 
finish_${PSExecID}:
  Exch ;now $R0 on top of stack, followed by script output
  Pop $R0
  !undef PSExecID
!macroend

Section "Download and install mplayer" SECMplayer
	SectionIn 1

    # Download and install mplayer
	# Mplayer download functions are based on, incl reusing code, the NSIS installer
    # in the SourceForge project: SMPlayer  (Written by redxii, thanks)
    retry_mplayer:

    DetailPrint $(MPLAYER_IS_DOWNLOADING)
	DetailPrint ${MPLAYER_URL}

	#NSISdl::download http://ladybug/dpg4x/MPlayer.7z   $INSTDIR\${MPLAYER7Z}
	#NSISdl::download ${MPLAYER_URL} $INSTDIR\${MPLAYER7Z}

	# sourceforge download works from a ps1 prompt:
	# $client = new-object System.Net.WebClient
    # $client.DownloadFile("http://sourceforge.net/projects/mplayer-win32/files/MPlayer%20and%20MEncoder/r38188%2Bg6e..., target)
    !insertmacro PowerShellExecFileMacro $INSTDIR\dependencies\download_mplayer.ps1 ${MPLAYER_URL} $INSTDIR\${MPLAYER7Z}
    #!insertmacro PowerShellExecFileMacro $INSTDIR\dependencies\download_mplayer.ps1 http://ladybug/dpg4x/MPlayer.7z $INSTDIR\${MPLAYER7Z}
	Pop $R0

    IfFileExists "$INSTDIR\${MPLAYER7Z}" mplayerDlSuccess
    DetailPrint $(MPLAYER_DL_FAILED)
	Goto checkInst

    mplayerDlSuccess:
      # DetailPrint "Extracting files..."
      SetOutPath $INSTDIR
      Nsis7z::Extract $INSTDIR/${MPLAYER7Z}

    checkInst:
	DetailPrint "$INSTDIR\${MPLAYER_target}\mplayer.exe"
    IfFileExists "$INSTDIR\${MPLAYER_target}\mplayer.exe" mplayerInstSuccess mplayerInstFailed
      mplayerInstSuccess:
        WriteRegDWORD SHCTX "${REGKEY}" Installed_MPlayer 0x1
		DetailPrint "Mplayer Installation OK"
        Goto done
      mplayerInstFailed:
        MessageBox MB_RETRYCANCEL|MB_ICONEXCLAMATION $(MPLAYER_DL_RETRY) /SD IDCANCEL IDRETRY retry_mplayer
        WriteRegDWORD SHCTX "${REGKEY}" Installed_MPlayer 0x0
        # Allow to continue without this and install mplayer manually later
        # Abort $(MPLAYER_INST_FAILED)
        MessageBox MB_OK  "$(MPLAYER_INST_FAILED)"
    done:
SectionEnd

Section "Install MS Visual C libraries" SECVisualClibs
	SectionIn 1

    # Silent install of visual C libraries:
    # If you would like to install the VC runtime packages in unattended mode (which will 
    # show a small progress bar but not require any user interaction), you can change the 
    # /qn switch below to /qb.  If you would like the progress bar to not show a cancel button, 
    # then you can change the /qn switch to /qb!
    ExecWait '"$INSTDIR\${DLLMSVC}" /q:a /c:"VCREDI~1.EXE /q:a /c:""msiexec /i vcredist.msi /qb!"" "'  
    WriteRegStr SHCTX "${REGKEY}\Components" Main 1
SectionEnd

Section -post SEC0001
    WriteRegStr SHCTX "${REGKEY}" Path $INSTDIR
    WriteRegStr SHCTX "${REGKEY}" Version "${VIProduct_Ver}"

    # Default Programs, Vista and later: (possibly more things to explore here...)
    # http://msdn.microsoft.com/en-us/library/cc144154%28v=vs.85%29.aspx
    WriteRegStr SHCTX  "${CLIENT_REGKEY}\Capabilities\FileAssociations" ".dpg" "DPG Video"
    WriteRegStr SHCTX  "${CLIENT_REGKEY}\Capabilities\FileAssociations" ".avi" "DPG Video"
    WriteRegStr SHCTX "${CLIENT_REGKEY}\Capabilities" "ApplicationDescription" $(APPLICATION_DESCRIPTION)
    WriteRegStr SHCTX "${CLIENT_REGKEY}\Capabilities" "ApplicationName" "${Name}"
    WriteRegStr SHCTX "Software\RegisteredApplications" "${Name}" "${CLIENT_REGKEY}\Capabilities"

    SetOutPath $INSTDIR
    WriteUninstaller $INSTDIR\uninstall.exe

	;create desktop shortcut
	!insertmacro UMUI_ADDITIONALTASKS_IF_CKECKED DESKTOP
	    CreateShortCut "$DESKTOP\${Name}.lnk" "$INSTDIR\${PROGRAM_FILE}" ""
    !insertmacro UMUI_ADDITIONALTASKS_ENDIF

    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    SetOutPath $SMPROGRAMS\$StartMenuGroup
    CreateShortCut "$SMPROGRAMS\$StartMenuGroup\${Name} ${VERSION}.lnk" "$INSTDIR\${PROGRAM_FILE}" "" "$INSTDIR\${PROGRAM_FILE}"
    WriteINIStr    "$SMPROGRAMS\$StartMenuGroup\$(WebLink).url" "InternetShortcut" "URL" "${URL}"
    !insertmacro MUI_STARTMENU_WRITE_END

	# From https://nsis.sourceforge.io/Add_uninstall_information_to_Add/Remove_Programs
	!define UNINST_KEY "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${Name}"
    WriteRegStr SHCTX "${UNINST_KEY}" DisplayName "${Name}"
    WriteRegStr SHCTX "${UNINST_KEY}" DisplayVersion "${UMUI_Version}"
    WriteRegStr SHCTX "${UNINST_KEY}" Publisher "${COMPANY}"
    WriteRegStr SHCTX "${UNINST_KEY}" URLInfoAbout "${URL}"
    WriteRegStr SHCTX "${UNINST_KEY}" "DisplayIcon" "$INSTDIR\uninstall.exe"
    WriteRegStr SHCTX "${UNINST_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
	WriteRegStr SHCTX "${UNINST_KEY}" \
                 "QuietUninstallString" "$INSTDIR\uninstall.exe /S"
    WriteRegDWORD SHCTX "${UNINST_KEY}" NoModify 1
    WriteRegDWORD SHCTX "${UNINST_KEY}" NoRepair 1

    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD SHCTX "${UNINST_KEY}" "EstimatedSize" "$0"

SectionEnd

# Uninstaller sections

!macro removeDpg4Xfiles
    # Delete directories recursively except for main directory
    # Do not recursively delete $INSTDIR
    RmDir /r $INSTDIR\dependencies    
    RmDir /r $INSTDIR\${MPLAYER_target}
    Delete $INSTDIR\*.exe
    Delete $INSTDIR\*.log    
    RmDir $INSTDIR
!macroend

!macro removeDpg4Xregistry
	SetShellVarContext current
    DeleteRegValue SHCTX "${REGKEY}\Components" Main

    DeleteRegValue SHCTX "${REGKEY}" StartMenuGroup
    DeleteRegKey /IfEmpty SHCTX "${REGKEY}\Components"
    DeleteRegKey /IfEmpty SHCTX "${REGKEY}"
    DeleteRegValue SHCTX "Software\RegisteredApplications" "${Name}"
    DeleteRegKey SHCTX "${REGKEY}"
    DeleteRegKey SHCTX "${CLIENT_REGKEY}"

	Delete "$DESKTOP\${Name}.lnk"

    DeleteRegKey SHCTX "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${Name}"
    Delete $INSTDIR\uninstall.exe

    Delete "$SMPROGRAMS\$StartMenuGroup\${Name} ${VERSION}.lnk"
    Delete "$SMPROGRAMS\$StartMenuGroup\$(WebLink).url" 
    RmDir $SMPROGRAMS\$StartMenuGroup
    RmDir $INSTDIR
    Push $R0
    StrCpy $R0 $StartMenuGroup 1
    StrCmp $R0 ">" no_smgroup
no_smgroup:
    Pop $R0
!macroend

Section Uninstall

    !insertmacro removeDpg4Xfiles
    !insertmacro removeDpg4Xregistry

SectionEnd

!insertmacro UMUI_DECLARECOMPONENTS_BEGIN
  !insertmacro UMUI_COMPONENT SECDpg4x
  !insertmacro UMUI_COMPONENT SECMplayer
  !insertmacro UMUI_COMPONENT SECVisualClibs
!insertmacro UMUI_DECLARECOMPONENTS_END

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDpg4x} "The core files required to use dpg4x (UI, dpg encoder)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SECMplayer} "Download and install mplayer and mencoder which converts video and audio streams"
  !insertmacro MUI_DESCRIPTION_TEXT ${SECVisualClibs} "Install Visual C redistributable libraries (vc_redist)"
!insertmacro MUI_FUNCTION_DESCRIPTION_END


Function .onGUIEnd
    # empty
FunctionEnd

Function .onInit
	!insertmacro UMUI_MULTILANG_GET
	; Change default InstallDir to C:\ProgramData on Windows Vista and more
	ClearErrors
    IfFileExists $INSTDIR endCheckVersion 0
      ReadRegStr $0 HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentVersion
      IfErrors endCheckVersion 0 ; If not WinNT
        IntCmp $0 6 0 endCheckVersion 0 ; If version >= 6
          SetShellVarContext current
          #StrCpy $INSTDIR "$APPDATA\${NAME}"
		  StrCpy $INSTDIR "$LocalAppData\Programs\${NAME}"
  endCheckVersion:

FunctionEnd

# Uninstaller functions
Function un.onInit
	!insertmacro UMUI_MULTILANG_GET
	SetShellVarContext current
    StrCpy $INSTDIR "$LocalAppData\Programs\${NAME}"
	# !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuGroup
FunctionEnd

;--------------------------------
; Pages functions

Function addtasks_function
  !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_LABEL "$(UMUI_TEXT_ADDITIONALTASKS_ADDITIONAL_ICONS)"
  !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_TASK DESKTOP 1 "$(UMUI_TEXT_ADDITIONALTASKS_CREATE_DESKTOP_ICON)"

  !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_LINE

  !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_LABEL "$(UMUI_TEXT_SHELL_VAR_CONTEXT)"

  !insertmacro UMUI_ADDITIONALTASKSPAGE_ADD_TASK_RADIO CURRENT 1 "$(UMUI_TEXT_SHELL_VAR_CONTEXT_ONLY_FOR_CURRENT_USER)"

FunctionEnd

!macro confirm_addline section

  SectionGetFlags ${Sec${section}} $1
  IntOp $1 $1 & ${SF_SELECTED}
  IntCmp $1 ${SF_SELECTED} 0 n${section} n${section}
    SectionGetText ${Sec${section}} $1
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "    - $1"
  n${section}:

!macroend


Function confirm_function
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "$(UMUI_TEXT_INSTCONFIRM_TEXTBOX_DESTINATION_LOCATION)"
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "      $INSTDIR"
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE ""
  
  ;Only if StartMenu Folder is selected
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "$(UMUI_TEXT_INSTCONFIRM_TEXTBOX_START_MENU_FOLDER)"
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "      $STARTMENU_FOLDER"

    ;ShellVarContext
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "$(UMUI_TEXT_SHELL_VAR_CONTEXT)"
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "      $(UMUI_TEXT_SHELL_VAR_CONTEXT_ONLY_FOR_CURRENT_USER)"
    !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE ""

  !insertmacro MUI_STARTMENU_WRITE_END

  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "$(UMUI_TEXT_INSTCONFIRM_TEXTBOX_COMPNENTS)"

  !insertmacro confirm_addline Dpg4x
  !insertmacro confirm_addline Mplayer
  !insertmacro confirm_addline VisualClibs
  
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE ""
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "$(UMUI_TEXT_ADDITIONALTASKS_TITLE):"
  ;Only if one at least of additional icon check is checked  
  !insertmacro UMUI_ADDITIONALTASKS_IF_CKECKED DESKTOP
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "      $(UMUI_TEXT_ADDITIONALTASKS_ADDITIONAL_ICONS)"
  !insertmacro UMUI_CONFIRMPAGE_TEXTBOX_ADDLINE "            $(UMUI_TEXT_ADDITIONALTASKS_CREATE_DESKTOP_ICON)"
  !insertmacro UMUI_ADDITIONALTASKS_ENDIF

FunctionEnd

Function preuninstall_function

  SetShellVarContext current
  IfFileExists $INSTDIR\${PROGRAM_FILE} dpg4x_installed
    MessageBox MB_YESNO "It does not appear that DPG4X is installed in the directory '$INSTDIR'.$\r$\nContinue anyway (not recommended)?" IDYES dpg4x_installed
    Abort "Install aborted by user"
  dpg4x_installed:

  # consider adding more here...
  !insertmacro removeDpg4Xfiles
  !insertmacro removeDpg4Xregistry
FunctionEnd