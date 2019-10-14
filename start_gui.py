from DAVE.scene import *
from DAVE.gui import Gui

s = Scene()

from DAVE.example_scenes import *
grid(s,10)
Gui(s).show()