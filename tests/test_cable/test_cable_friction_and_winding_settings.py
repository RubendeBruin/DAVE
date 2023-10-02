from numpy.testing import assert_allclose

from DAVE import Scene, Watch


def cable():
    s = Scene()
    f = s.new_rigidbody(
        "f", position=(0, 0, -10), fixed=(True, True, False, True, True, True), mass=32
    )
    
    hook1 = s.new_point("hook1", position=(0, 0, 0))
    hook2 = s.new_point("hook2", position=(1, 0, 0))
    s.new_point("p1", position=(0, 0, 0), parent=f)
    s.new_point("p2", position=(1, 0, 0), parent=f)
    
    c = s.new_cable(
        connections=["p1", "hook1", "hook2", "p2"],
        name="cable",
        EA=122345,
        length=7,
    )

    return c

def loop():
    c=  cable()
    c.connections = ["p1", "hook1", "hook2", "p2", "p1"]
    return c

def cable_with_circle():
    s = Scene()

    s.new_point("p1", position=(-1, 0, 0))
    s.new_point("p2", position=(1, 0, 0))
    s.new_point("p3", position=(0, 0, 4))
    s.new_circle("c1", radius=1, parent="p3", axis=(0,1,0))
    s.new_cable("cable", connections=["p1", "c1", "p2"], EA = 1000, length=9)

    return s["cable"]


def test_cable_default_winding_settings():
    c = cable()
    assert c.max_winding_angles == (999, 999,999,999)

def test_cable_default_winding_settings_friction():
    """assert that setting the friction does not change the winding settings"""
    c = cable()
    c.friction = (0.1, -0.1)
    assert c.max_winding_angles == (999, 999,999,999)

def test_modify_create_loop_by_adding_a_point():
    c = cable()
    s = c._scene

    c.friction = (0.1, -0.1)
    s.solve_statics()
    c.connections = ['p1', 'hook1', 'hook2', 'p2', 'p1']
    s.solve_statics()  #<-- should not crash

    assert c.max_winding_angles == (999, 999,999,999,999)
    assert c.friction == (None, 0.1, -0.1, 0)


def test_modify_create_loop_by_changing_a_point():
    c = cable()
    s = c._scene

    c.friction = (0.1, -0.1)
    s.solve_statics()
    c.connections = ['p1', 'hook1', 'hook2', 'p1']
    s.solve_statics()  #<-- should not crash

    assert c.max_winding_angles == (999, 999,999,999)
    assert c.friction == (None, 0.1, -0.1)

def test_break_loop_by_removing_a_point():
    c = loop()
    s = c._scene

    c.friction = (None, 0.1, -0.1, 0)

    s.solve_statics()
    c.connections = ['p1', 'hook1', 'hook2', 'p2']
    s.solve_statics()  #<-- should not crash

    assert c.max_winding_angles == (999, 999,999,999)
    assert c.friction == (0.1, -0.1)

def test_break_loop_by_changing_a_point():
    c = loop()
    s = c._scene
    
    c.friction = (None, 0.1, -0.1, 0)
    
    s.solve_statics()
    c.connections = ["p1", "hook1", "hook2", "p2", "hook1"]
    s.solve_statics()  # <-- should not crash
    
    assert c.max_winding_angles == (999, 999, 999, 999, 999)
    assert c.friction == (0.1, -0.1,0)

def test_revesed():
    c  = cable_with_circle()
    c.friction = (0.1, )
    c.update()
    tensions = c.segment_mean_tensions
    assert tensions[0] > tensions[1]  # friction from A to B

    assert c.reversed[1] == False
    c.reversed = (False, True, False)

    c.update()

    tensions = c.segment_mean_tensions
    assert tensions[0] > tensions[1]  # friction still from A to B

def test_resuls():
    c= cable_with_circle()

    assert len(c.friction) == 1
    assert len(c.friction_forces) == 1
    assert len(c.segment_mean_tensions) == 2
    assert len(c.segment_end_tensions) == 2

    for c in c.segment_end_tensions:
        assert len(c) == 2

def test_resuls_loop():
    c= cable_with_circle()
    c.connections = ["p1", "c1", "p2", "p1"]

    assert c._isloop

    assert len(c.friction) == 3
    assert len(c.friction_forces) == 3
    assert len(c.segment_mean_tensions) == 3
    assert len(c.segment_end_tensions) == 3

    for _ in c.segment_end_tensions:
        assert len(_) == 2

    import vedo

    points, tensions = c.get_points_and_tensions_for_visual()
    #
    # colors = vedo.color_map(tensions, 'viridis', vmin = min(tensions), vmax = max(tensions))
    # t = vedo.Tube(points, c=colors)
    # t.show()

if __name__ == '__main__':


    from DAVE.gui import Gui
    c = cable_with_circle()
    s = c._scene

    s["cable"].watches["Mean segment tensions"] = Watch(
        evaluate=r"'\n'.join([str(round(c)) for c in self.segment_mean_tensions])", condition="", decimals=1
    )

    Gui(s)
