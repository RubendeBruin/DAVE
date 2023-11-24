import logging

import pytest

from DAVE.scene import Scene
from DAVE.nodes import *
from DAVE.settings import DAVE_ADDITIONAL_RUNTIME_MODULES


def test_parents():

    s = Scene()

    f = s.new_frame('f')


    f2 = s.new_frame('f2', parent = f)
    f3 = s.new_frame('f3'
                     , parent = f2)

    print(f3.parent.name)

    p = Point(s,'p')

    assert f._vfNode.parent is None  # <--  shoud be None
    assert f.parent is None

    p.parent = f
    assert p.parent == f

    with pytest.raises(ValueError):
        f.parent = f3  # <-- should fail

    with pytest.raises(ValueError):
        f.parent = f2  # <-- should fail

    s.print_node_tree()

def test_parent_on_all_node_types():

    node_types = [Frame, Point, RigidBody]

    s = Scene()
    f = s.new_frame('f')

    for node_type in node_types:
        d = node_type(s, str(node_type))
        d.parent = f
        assert d.parent == f

    s.print_node_tree()

def test_frame():
    s = Scene()
    f = s.new_frame('f')

    f.name = "renamed"
    assert f.name == "renamed"

    # assert that the pointmasses have been renamed as well
    assert "renamed" in f._pointmasses[0].name

def test_rigidbody_names():
    s = Scene()
    f = s.new_rigidbody('f')

    f.name = "renamed"
    assert f.name == "renamed"

    # assert that the pointmasses have been renamed as well
    for pm in f._pointmasses:
        assert "renamed" in pm.name

    assert "renamed" in f._vfNode.name
    assert "renamed" in f._vfPoi.name
    assert "renamed" in f._vfForce.name


def test_circle():
    s = Scene()
    f = s.new_frame('f')
    p = s.new_point('p', parent = f)
    c = s.new_circle('c', parent = p, axis=(0,1,0), radius=1)

def test_rigidbody_footprint_and_cog():

    s = Scene()
    f = s.new_frame('f')

    rb = RigidBody(s, 'rb')

    rb.parent = f

    assert rb._vfForce.parent == rb._vfPoi.name
    assert rb._vfPoi.parent == rb._vfNode.name
    assert rb._vfPoi.parent == rb.name

def test_cable():
    s = Scene()
    p = s.new_point('p')
    rb = s.new_rigidbody('rb', mass = 5, position = (0,0,-5))

    p2 = s.new_point('p2', parent=rb)

    c = s.new_cable('cable',endA = p, endB = p2)

    assert c.connections[0] == p
    assert c.connections[1] == p2

def test_force():
    s = Scene()
    f = s.new_frame('f')
    p = s.new_point('p', parent = f)
    f = s.new_force('force', parent = p, force = (0,0,1))

    assert f.parent == p

    with pytest.raises(Exception):
        f.parent = None


def test_wind():
    s = Scene()
    f = s.new_frame('f')
    p = s.new_point('p', parent = f)
    f = s.new_windarea('wind', parent = p)

    assert f.parent == p

    with pytest.raises(Exception):
        f.parent = None

def test_contactmesh():
    s = Scene()
    c= s.new_contactmesh('c')
    c.change_parent_to(s.new_frame('f'))

    assert c.parent.name == 'f'

def test_contactball():
    s = Scene()
    f = s.new_frame('f')
    p = s.new_point('p', parent = f)
    f = s.new_contactball('ball', parent = p)
    c = s.new_contactmesh('c')

    f.meshes = (c, )

    assert f.parent == p
    assert c in f.depends_on()

    with pytest.raises(Exception):
        f.parent = None

    assert p in f.depends_on()

def test_spmt():
    s = Scene()
    f = s.new_frame('f')
    spmt = s.new_spmt('spmt', parent = f)
    c = s.new_contactmesh('c')

    spmt.meshes = (c, )

    assert spmt.parent == f
    assert c in spmt.depends_on()

    with pytest.raises(Exception):
        spmt.parent = None

    assert f in spmt.depends_on()

def test_hydspring():
    s = Scene()
    f = s.new_frame('f')

    h = s.new_hydspring("linear", "f", (1,2,3), 1,2,3,4,5,6,7)

    with pytest.raises(Exception):
        h.change_parent_to(None)

def test_c2d():
    s = Scene()
    f1 = s.new_frame('f1')
    f2 = s.new_frame('f2')

    c2d = s.new_connector2d('c2d', nodeA = f1, nodeB = f2)

    assert f1 in c2d.depends_on()
    assert f2 in c2d.depends_on()

    c2d.nodeB = f1
    c2d.nodeA = f2

    assert f1 in c2d.depends_on()
    assert f2 in c2d.depends_on()

    assert f1 == c2d.nodeB
    assert f2 == c2d.nodeA


def test_beam():
    s = Scene()
    f1 = s.new_frame('f1')
    f2 = s.new_frame('f2', position = (10,0,0))

    c2d = s.new_connector2d('c2d', nodeA = f1, nodeB = f2)

    assert f1 in c2d.depends_on()
    assert f2 in c2d.depends_on()

    c2d.nodeB = f1
    c2d.nodeA = f2

    assert f1 in c2d.depends_on()
    assert f2 in c2d.depends_on()

    assert f1 == c2d.nodeB
    assert f2 == c2d.nodeA

def test_c6d():
    s = Scene()
    f1 = s.new_frame('f1')
    f2 = s.new_frame('f2')

    c2d = s.new_linear_connector_6d('c2d', secondary = f1, main = f2)

    assert f1 in c2d.depends_on()
    assert f2 in c2d.depends_on()

    c2d.main = f1
    c2d.secondary = f2

    assert f1 in c2d.depends_on()
    assert f2 in c2d.depends_on()

    assert f1 == c2d.main
    assert f2 == c2d.secondary

def test_buoyancy():
    s = Scene()
    f = s.new_frame('f')
    b = s.new_buoyancy('b', parent = f)

    with pytest.raises(Exception):
        b.parent = None

    assert f in b.depends_on()

def test_tank():
    s = Scene()
    f = s.new_frame('f')
    f2 = s.new_frame('f2', position = (5,7,9), rotation=(30, 40, 70))
    b = s.new_tank('b', parent = f, )

    with pytest.raises(Exception):
        b.parent = None

    assert f in b.depends_on()

def test_geometric_contact():
    s = Scene()
    f1 = s.new_frame('f1')
    p1 = s.new_point('p1', parent = f1)
    c1 = s.new_circle('c1', parent = p1, radius = 1, axis = (0,1,0))

    f2 = s.new_frame('f2')
    p2 = s.new_point('p2', parent = f2)
    c2 = s.new_circle('c2', parent = p2, radius = 0.5, axis = (0,1,0))

    g = s.new_geometriccontact('g', parent=c1, child = c2)

    g.name = "renamed"

    _ = s["renamed/_axis_on_child"]  # raises error if name not found

    s.print_node_tree()
#
# def test_sling():
#     s = Scene()
#     f1 = s.new_frame('f1')
#     p1 = s.new_point('p1', parent = f1)
#     c1 = s.new_circle('c1', parent = p1, radius = 1, axis = (0,1,0))
#
#     f2 = s.new_frame('f2', position = (10,0,0))
#     p2 = s.new_point('p2', parent = f2)
#     c2 = s.new_circle('c2', parent = p2, radius = 0.5, axis = (0,1,0))
#
#     sl = s.new_sling('sling', endA=c1, endB=c2)
#
#     sl.name = "renamed"
#     s.print_node_tree()
#
#     _ = s["renamed/main_part"] # check renamed node
#
#     assert sl.name == "renamed"
#
# def test_shackle():
#     s = Scene()
#     sh = s.new_shackle('shackle', kind = "GP800")
#
#     sh.name = "renamed"
#     assert sh.name == "renamed"
#
#     _ = s["renamed/bow"] # check renamed node
#
#     sh.depends_on()
#
#     s.sort_nodes_by_parent()
#
#     s.print_node_tree()

def test_component():
    s = Scene()
    c = s.new_component('c')

    c.name = "renamed"

    assert isinstance(s['renamed/Frame'], Frame) # check renamed node

def test_import():
    s = Scene()
    s.import_scene("res: cheetah with crane.dave", containerize=False, prefix="")