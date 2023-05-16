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
