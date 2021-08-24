import pytest

from DAVE import *
from DAVE.io.simplify import *
from numpy.testing import assert_allclose

from DAVE.gui import *

def test_tank_to_body():
    s = Scene()
    s.new_frame('main')
    t = s.new_tank('tank',parent='main')
    t.trimesh.load_obj('res: cube.obj', offset=(10,5,2))
    t.volume = 0.5
    t.density = 1.025

    # cube is 1x1x1 with the origin at the center

    tanks_to_bodies(s)

    b = s['tank']
    assert isinstance(b, RigidBody)

    assert_allclose(b.mass, 0.5 * 1.025)
    assert_allclose(b.global_position, (10,5,2-0.25))

def test_tank_to_body_empty():
    s = Scene()
    s.new_frame('main')
    t = s.new_tank('tank',parent='main')
    t.trimesh.load_obj('res: cube.obj', offset=(10,5,2))
    t.volume = 0
    t.density = 1.025

    tanks_to_bodies(s)

    # empty tank should have been deleted
    with pytest.raises(ValueError):
        s['tank']