from DAVE import *

def test_cat_shape_visual():
    s = Scene()
    s.new_point(name="p1", position=(-10, 0, 0))
    s.new_point(name="p2", position=(10, 0, 0))
    s.new_cable(name="cable", connections=["p1", "p2"], EA=0, length=20)

    from DAVE.gui import Gui
    Gui(s, block=False)