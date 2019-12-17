import sys
sys.path.append(r'c:\data\dave\public\dave\src')
sys.path.append(r'C:\data\vf\pyo3d\x64\Release')

from DAVE.gui2.main import Gui
from DAVE.scene import *


s = Scene()
Gui(s)
