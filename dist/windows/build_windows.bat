@ECHO off
REM This file build an installer file for Windows, to be run from the windows directory
REM Please install everything listed in README_dpg4x_win.txt before running this file
cd /d %~dp0\..\..
REM This requires a local Python environment with all PIP deps installed
.\dpg4x-python\Scripts\pyinstaller --onefile -w --icon .\dist\windows\dpg4x.ico --clean --paths C:\Users\Tomas_2\AppData\Local\Programs\Python\Python38  --add-data ".\dpg4x\icons;dpg4x\icons" --add-data ".\dpg4x\i18n;dpg4x\i18n"  .\dpg4x_main.py
REM This requires http://ultramodernui.sourceforge.net/
"C:\ProgramData\NSIS\makensis.exe"  .\dist\windows\dpg4x.nsi
 echo "Successfully built new installer" 