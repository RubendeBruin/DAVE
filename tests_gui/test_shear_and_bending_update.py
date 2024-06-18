from DAVE import *
from DAVE.gui import Gui

s = Scene()
s.import_scene("res: cheetah with crane.dave", containerize=False, prefix="")
g = Gui(s, autosave_enabled=False, block=False)
g.activate_dockgroup("Shear and Bending")
g.app.exec()