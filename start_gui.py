from DAVE.scene import *
from DAVE.gui import Gui

s = Scene()

from DAVE.example_scenes import *
octopus(s)
Gui(s).show()