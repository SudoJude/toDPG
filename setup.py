import glob,os
from setuptools import setup, find_packages

target_directory = os.path.join('share', 'dpg4x')
top_directory = 'dpg4x'
icon_files=[(os.path.join(target_directory, 'icons'), glob.glob(os.path.join(top_directory, 'icons', '*.png')))]
i18n_files=[(os.path.join('share', os.path.dirname(f)), [f]) for f in glob.glob(os.path.join(top_directory, 'i18n', '*', 'LC_MESSAGES', 'dpg4x.mo'))]
doc_files = [(os.path.join(target_directory, 'doc'), ['LICENSE', 'CREDITS', 'INSTALL', 'INSTALL.win', 'README', 'ChangeLog'])]
dist_files = [(os.path.join(target_directory, 'dist', 'pkg_common'), glob.glob(os.path.join('dist', 'pkg_common', '*')))]

from distutils.core import setup
setup(name='dpg4x',
      version='3.0',
      license='GPLv3',
      url='http://sourceforge.net/projects/dpg4x',
      description='GUI to encode files into the DPG video format',
      author='d0malaga, mpdavig, xukosky @sourceforge',
      author_email='<d0malaga@users.sourceforge.net>',
      maintainer='Tomas Aronsson ',
      maintainer_email='<d0malaga@users.sourceforge.net>',
      py_modules=['dpg4x_main'],
      # py_modules=[f.replace(".py","") for f in glob.glob("*.py")],
      packages=['dpg4x','dpg4x.moreControls'],
      # packages=find_packages()
      data_files= icon_files + i18n_files + doc_files + dist_files,
      entry_points={
          "console_scripts": [
              "dpg4x_cmd = dpg4x_main:main"
          ],
          "gui_scripts": [
              "dpg4x = dpg4x_main:main"
          ]
      },
      # TBD: different for Ubuntu, Fedora, Windows... and some non python deps too
      install_requires=["wxPython > 4.0",
                        "pywin32 >= 1.0;platform_system=='Windows'"]
)
