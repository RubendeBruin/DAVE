from PySide6 import QtWidgets, QtCore

from DAVE import *
from DAVE.gui import Gui
from DAVE.gui.dock_system.dockwidget import guiEventType


if __name__ == '__main__':

    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2024-02-19 15:04:06 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution

    def solved(number):
        return number

    # Environment settings
    s.g = 9.80665
    s.waterlevel = 0.0
    s.rho_air = 0.00126
    s.rho_water = 1.025
    s.wind_direction = 0.0
    s.wind_velocity = 0.0
    s.current_direction = 0.0
    s.current_velocity = 0.0

    # code for Point1
    s.new_point(name='Point1',
                position=(-10,
                          0,
                          0))

    # code for Point2
    s.new_point(name='Point2',
                position=(0,
                          0,
                          10))

    # code for Point3
    s.new_point(name='Point3',
                position=(10,
                          0,
                          0))

    # code for Circle1
    c = s.new_circle(name='Circle1',
                     parent='Point1',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Circle2
    c = s.new_circle(name='Circle2',
                     parent='Point2',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Circle3
    c = s.new_circle(name='Circle3',
                     parent='Point3',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Cable
    s.new_cable(name='Cable',
                endA='Circle1',
                endB='Circle1',
                length=29.8549,
                EA=0.0,
                sheaves=['Circle2',
                         'Circle3'])
    s['Cable'].reversed = (True, True, True, True)
    s['Cable'].friction = [0.1, 0.0, None]

    g = Gui(scene=s, block=False)
    app = g.app
    g.guiSelectNode("Cable", execute_now=False)


    for i in range(200):

        g.run_code("s['Cable'].reversed = [True, True, False, True]", guiEventType.FULL_UPDATE)
        g.app.processEvents()
        g.run_code("s['Cable'].reversed = [False, False, False, True]", guiEventType.FULL_UPDATE)
        g.app.processEvents()

    g.app.exec()

