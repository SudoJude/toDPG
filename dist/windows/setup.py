import glob,os
import py2exe

top_directory = "dpg4x"
icon_files=[(os.path.join(top_directory, 'icons'), glob.glob(os.path.join('icons', '*.png')))]
i18n_files=[(os.path.join(top_directory, os.path.dirname(f)), [f]) for f in glob.glob(os.path.join('i18n', '*', 'LC_MESSAGES', 'dpg4x.mo'))]
doc_files = [(os.path.join(top_directory, 'doc'), ['COPYING', 'CREDITS', 'INSTALL', 'INSTALL.win', 'README', 'ChangeLog'])]

# Python is compiled with Visual C. This requires libraries for standalone Py2exe programs
# Handle Visual C libraries in the NSIS installer

from distutils.core import setup
setup(name='dpg4x',
      version='3.0',
      license='GPLv3',
      url='http://sourceforge.net/projects/dpg4x',
      description='GUI to encode files into the DPG video format',
      py_modules=[f.replace(".py","") for f in glob.glob(os.path.join(top_directory, "*.py"))],
      packages=[os.path.join(top_directory, 'moreControls')],
      data_files= icon_files + i18n_files + doc_files,
      # Needed to be able to use win32api on Windows XP
      options = {"py2exe":{"dll_excludes":[ "powrprof.dll" ]}},
      # Used by py2exe to create a wrapper exe files
#      windows = [
#        {
#            "script": os.path.join(top_directory, "Dpg4x.py"),    ### Wx Python script    
#            "icon_resources": [(0, "dist/windows/dpg4x.ico")]     ### Icon to embed into the PE file.
#        }],
# Testing a basic case from googling... -> no lnger mainained -> give up on py2exe
      console = [os.path.join(top_directory, "Dpg4x.py")]   ### cmdline Python script    
#      console = [
#        {
#            "script": os.path.join(top_directory, "Dpg4x.py"),   ### cmdline Python script    
#            "dest_base": "Dpg4xConsole"                          ### based on same src as above
#        }
#       ]
      )
