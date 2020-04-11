#from setuptools import setup
from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == "win32":
    base = "Win32GUI"    

executables = [Executable("SnapSort\__main__.py", base=base)]

packages=["SnapSort"]

try:
    from pyqt_distutils.build_ui import build_ui
    cmdclass = {"build_ui": build_ui}
except ImportError:
    cmdclass = {}

options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name="SnapSort",
    version="0.1",
    packages = packages,
    options = options,
    executables = executables,
#    cmdclass = cmdclass
)