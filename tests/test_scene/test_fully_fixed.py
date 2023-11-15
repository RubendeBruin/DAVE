# these are tests for the functions node_is_fully_fixed_to and node_is_fully_fixed

from DAVE import *

def test_fully_fixed():
    s = Scene()

    # code for Frame
    s.new_frame(
        name="Frame",
        position=(0, 0, 0),
        rotation=(0, 0, 0),
        fixed=(True, True, True, True, True, True),
    )

    # code for Point_2
    s.new_point(name="Point_2", position=(0, 0, -20))

    # code for Frame_1
    s.new_frame(
        name="Frame_1",
        parent="Frame",
        position=(0, 0, 0),
        rotation=(40, 0, 0),
        fixed=(True, True, True, False, True, True),
    )

    # code for Frame_2
    s.new_frame(
        name="Frame_2",
        parent="Frame",
        position=(0, 0, 0),
        rotation=(0, 10, 0),
        fixed=(True, True, True, True, True, True),
    )

    # code for Circle_2
    c = s.new_circle(name="Circle_2", parent="Point_2", axis=(0, 1, 0), radius=1)

    # code for Point
    s.new_point(name="Point", parent="Frame_1", position=(2, 0, -2))

    # code for Point_1
    s.new_point(name="Point_1", parent="Frame_2", position=(-1, 0, -2))

    # code for Circle
    c = s.new_circle(name="Circle", parent="Point", axis=(0, 1, 0), radius=1)

    # code for Circle_1
    c = s.new_circle(name="Circle_1", parent="Point_1", axis=(0, 1, 0), radius=1)

    c = s["Circle"]
    c_1 = s["Circle_1"]
    f = s["Frame"]

    assert not s.node_is_fully_fixed_to(c, f)
    assert s.node_is_fully_fixed_to(c_1, f)

    assert s.node_is_fully_fixed_to_world(c_1)
    assert not s.node_is_fully_fixed_to_world(c)
