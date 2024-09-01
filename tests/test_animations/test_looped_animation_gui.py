import time

from PySide6.QtCore import QTimer

from DAVE import *

def test_looped_animation_gui():

    """Set-up a scene with a single DOF
    Start an animation using callbacks

    Run for 10 seconds, then stop the animation and close
    """

    s = Scene()

    s.import_scene('res: pendulum.dave')
    g = DG(s, block = False, autosave=False, workspace="Modeshapes")

    def start_animation():
        dock = g.guiWidgets["Mode-shapes"]
        dock.ui.btnCalc.click()

    QTimer.singleShot(1, start_animation)

    # make a single shot time that executes after 10 seconds
    def single_shot():
        g.animation_terminate()
        g.MainWindow.close()


    QTimer.singleShot(
        10*1000, single_shot
    )

    g.app.exec()  # start the app
