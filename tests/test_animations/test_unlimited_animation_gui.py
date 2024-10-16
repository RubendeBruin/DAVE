import time

from PySide6.QtCore import QTimer

from DAVE import *

def test_unlimited_animation_gui(noclose=False):

    """Set-up a scene with a single DOF
    Start an animation using callbacks

    Run for 10 seconds, then stop the animation and close
    """

    s = Scene()

    f = s.new_frame('frame', fixed=True)
    f.fixed_ry = False

    # code for bar
    s.new_visual(name='bar',
                 parent='frame',
                 path=r'res: arrow.glb',
                 offset=(14, 0, 0),
                 rotation=(0, 180, 0),
                 scale=(1, 1, 1))

    g = DG(s, block = False, autosave=False)

    def time_activated(t: float, s: Scene):
        s['frame'].ry = 36*t

    g.animation_start_unlimited(callback_time_activated = time_activated, end_time=2)
    g._animation_speed = 10


    # make a single shot time that executes after 2 seconds (ok as speed is 10)
    def single_shot():
        g.animation_terminate()
        g.MainWindow.close()


    if not noclose:
        QTimer.singleShot(
            2*1000, single_shot
        )

    g.app.exec()  # start the app

if __name__ == '__main__':
    test_unlimited_animation_gui(noclose=True)