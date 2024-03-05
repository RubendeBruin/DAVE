import time

from PySide6 import QtWidgets

from DAVE import *
from DAVE.gui import Gui
from DAVE.gui.dock_system.dockwidget import guiEventType
from DAVE.gui.settings import DOCK_GROUPS

s = Scene()
g = Gui(s, block = False)
app : QtWidgets.QApplication = g.app

g.run_code('s.new_point(name="Point1", position=(-10, 0, 0))', guiEventType.MODEL_STRUCTURE_CHANGED)
g.run_code('s.new_point(name="Point2", position=(0, 0, 10))', guiEventType.MODEL_STRUCTURE_CHANGED)
g.run_code('s.new_point(name="Point3", position=(10, 0, 0))', guiEventType.MODEL_STRUCTURE_CHANGED)

app.processEvents()

g.guiSelectNode("Point1", execute_now=False)

app.processEvents()

app.focusWindow()

def cycle_dockgroups():

    current = g._active_dockgroup.ID

    for dg in DOCK_GROUPS:
        if dg.ID == current:
            continue

        # if dg.ID == "Ballast":
        #     continue

        print('Activating dockgroup', dg.ID,dg.description)

        g.activate_dockgroup(dg.ID)
        time.sleep(0.5)
        app.processEvents()



    g.activate_dockgroup(current)
    app.processEvents()


cycle_dockgroups()

app.exec()