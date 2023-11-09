from numpy.testing import assert_allclose
import numpy as np
from DAVE import *


def test_circle_colliding_with_point():
    """This is gracefully handled when the point is not on the centerline of the circle"""
    s = Scene()
    s.new_point(name='p1',position = (-10,0,0))
    s.new_point(name='p2',position = (10,0,0))
    s.new_point(name='b', position = (9,0,0.5))
    s.new_circle(name='circle',parent='b',radius=1.2,axis=(0,1,0), roundbar=False)

    c = s.new_cable(connections=['p1','circle','p2'],name='cable',EA=1e6,length=20)

    c.update()
    s.update()

    assert c.actual_length > 20
    assert c.actual_length < 22

    assert not np.isnan(np.linalg.norm(s["p1"].applied_force_and_moment_global))
    assert not np.isnan(np.linalg.norm(s["p2"].applied_force_and_moment_global))

def test_circle_center_colliding_with_point():
    """This is gracefully handled when the point is not on the centerline of the circle"""
    s = Scene()
    s.new_point(name='p1',position = (-10,0,0))
    s.new_point(name='p2',position = (10,0,0))
    s.new_point(name='b', position = (10,0,0))
    s.new_circle(name='circle',parent='b',radius=1.2,axis=(0,1,0), roundbar=False)

    c = s.new_cable(connections=['p1','circle','p2'],name='cable',EA=1e6,length=20)

    c.update()

    assert c.actual_length > 20
    assert c.actual_length < 22

    s.update()

    assert not np.isnan(np.linalg.norm(s["p1"].applied_force_and_moment_global))
    assert not np.isnan(np.linalg.norm(s["p2"].applied_force_and_moment_global))

def test_two_circles_at_same_position():
    s = Scene()
    s.new_point(name='p1',position = (-10,0,0))
    s.new_point(name='p2',position = (10,0,0))

    s.new_point(name='b', position = (0,0,0))
    s.new_circle(name='circle',parent='b',radius=1.2,axis=(0,1,0), roundbar=False)
    s.new_circle(name='circle2',parent='b',radius=1.2,axis=(0,1,0), roundbar=False)


    c = s.new_cable(connections=['p1','circle', 'circle2','p2'],name='cable',EA=1e6,length=20)

    c.update()

    assert c.actual_length > 20
    assert c.actual_length < 30

    s.update()

    assert not np.isnan(np.linalg.norm(s["p1"].applied_force_and_moment_global))
    assert not np.isnan(np.linalg.norm(s["p2"].applied_force_and_moment_global))

def test_two_circles_at_same_position_different_axis():
    s = Scene()
    s.new_point(name='p1',position = (-10,0,0))
    s.new_point(name='p2',position = (10,0,0))

    s.new_point(name='b', position = (0,0,0))
    s.new_circle(name='circle',parent='b',radius=1.2,axis=(0,1,0), roundbar=False)
    s.new_circle(name='circle2',parent='b',radius=1.2,axis=(1,0,0), roundbar=False)

    c = s.new_cable(connections=['p1','circle', 'circle2','p2'],name='cable',EA=1e6,length=20)

    c.update()

    assert c.actual_length > 20
    assert c.actual_length < 30

    s.update()

    assert not np.isnan(np.linalg.norm(s['p1'].applied_force_and_moment_global))
    assert not np.isnan(np.linalg.norm(s['p2'].applied_force_and_moment_global))



