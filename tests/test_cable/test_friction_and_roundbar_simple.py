from DAVE import *
from DAVE.gui.dock_system.dockwidget import guiEventType


def scene_1():
    s = Scene()
    s.new_point(name='p1',position = (-10,0,0))
    s.new_point(name='p2',position = (10,0,0))
    s.new_point(name='b', position = (0,0,2))
    s.new_circle(name='bar',parent='b',radius=1.2,axis=(0,1,0), roundbar=True)

    c = s.new_cable(connections=['p1','bar','p2'],name='cable',EA=1e6,length=20)

    c.friction = (0.1, )

    return s,c

def test_roundbar_active_1():
    s,c = scene_1()

    c.update()

    assert len(c.friction) == 1
    assert len(c.friction_forces) == 1
    assert c.friction_forces[0] > 0


def test_roundbar_inactive():
    s,c = scene_1()

    s['b'].gz = -2

    c.update()

    assert len(c.friction) == 1
    assert len(c.friction_forces) == 0







def test_example_scene_for_documentation():
    s = Scene()
    s.new_point(name='p1',position = (-10,0,0))
    s.new_point(name='p2',position = (10,0,0))
    s.new_point(name='b', position = (0,0,2))
    s.new_circle(name='bar',parent='b',radius=1.2,axis=(0,1,0), roundbar=True)

    c = s.new_cable(connections=['p1','bar','p2'],name='cable',EA=1e6,length=20)

    c.friction = (0.1, )

    s["cable"].watches["Friction forces"] = Watch(
        evaluate="self.friction_forces", condition="", decimals=2
    )

    s["cable"].watches["Mean segment tensions"] = Watch(
        evaluate="self.segment_mean_tensions", condition="", decimals=3
    )

    s["b"].position = (0.0, 0.0, -3.0)
    s["b"].watches["X-Force on bar (from Point)"] = Watch(
        evaluate="self.fx", condition="", decimals=3
    )

    from DAVE.gui import Gui
    g = Gui(s, block=False)
    g.run_code("s['b'].gz = -2", guiEventType.FULL_UPDATE)




