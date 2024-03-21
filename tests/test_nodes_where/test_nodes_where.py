from DAVE import *

def model1():
    s = Scene()
    p = s.new_point(name="Point", position=(0, 0, 0))
    p2 = s.new_point(name="anchor_point", position=(4, 3, 0))
    c = s.new_cable(name="Cable", connections = ["Point","anchor_point"], EA = 1000)

    circle = s.new_circle(name="Circle", parent="anchor_point", axis=(1, 0, 0), radius=1)

    c2 = s.new_cable(name="Cable2", connections = ["Point","Circle","Point"], EA = 1000)

    return s

def model2():
    s = Scene()
    f1 = s.new_frame(name="Frame1", position=(0, 0, 0))
    f2 = s.new_frame(name="Frame2", position=(4, 3, 0))

    con = s.new_connector2d(name="Connector", nodeA = "Frame1", nodeB = "Frame2")
    return s


def test_core_connected_cable():
    s = model1()

    nodes = s.nodes_where(kind = Cable, core_connected_to = s['Point'])

    assert len(nodes) == 2

    assert len(s.nodes_where(core_connected_to = s['anchor_point'])) == 3  # two cables, one circle

def test_core_connected_spring():
    s = model2()

    nodes = s.nodes_where(core_connected_to = s['Frame1'])

    assert len(nodes) == 1
    assert nodes[0].name == "Connector"

def test_name():
    s = model2()
    assert len(s.nodes_where(name = "Fra*")) == 2

def test_fixed_to_no():
    s = model2()
    assert len(s.nodes_where(fixed_to = s['Frame1'])) == 0

def test_fixed_to():
    s = model1()
    assert len(s.nodes_where(fixed_to = s['anchor_point'])) == 1


