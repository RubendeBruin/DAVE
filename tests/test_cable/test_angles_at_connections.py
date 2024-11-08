"""Angles at connections gives the angle change at each connection.
including the first and last"""
from cmath import isnan

from numpy.testing import assert_allclose

from DAVE import *
def test_p3_line():
    s = Scene()
    s.new_point("p1", position=(-1, 0, 0))
    s.new_point("p2", position=(0, 0, 0))
    s.new_point("p3", position=(0, 0, -1))

    c = s.new_cable("cable", connections=["p1", "p2", "p3"], EA = 1000, length=2)

    s._save_coredump()

    assert_allclose(c.angles_at_connections, [0, 90, 0])

def test_p3_loop():
    s = Scene()
    s.new_point("p1", position=(-1, 0, 0))
    s.new_point("p2", position=(0, 0, 0))
    s.new_point("p3", position=(0, 0, -1))

    c = s.new_cable("cable", connections=["p1", "p2", "p3", "p1"], EA = 1000, length=2)

    s._save_coredump()

    assert_allclose(c.angles_at_connections, [90+45, 90, 90+45, 90+45])

def test_c3_line():
    s = Scene()
    s.new_point("p1", position=(-1, 0, 0))
    s.new_point("p2", position=(0, 0, 0))
    s.new_point("p3", position=(0, 0, -1))

    c1 = s.new_circle("c1", parent="p1", axis=(0, 1, 0), radius=0.1)
    c2 = s.new_circle("c2", parent="p2", axis=(0, 1, 0), radius=0.1)
    c3 = s.new_circle("c3", parent="p3", axis=(0, 1, 0), radius=0.1)

    c = s.new_cable("cable", connections=["c1", "c2", "c3"], EA = 1000, length=2)

    assert_allclose(c.angles_at_connections, [0, 90, 0], atol=0.1)

def test_c3_loop():
    s = Scene()
    s.new_point("p1", position=(-1, 0, 0))
    s.new_point("p2", position=(0, 0, 0))
    s.new_point("p3", position=(0, 0, -1))

    c1 = s.new_circle("c1", parent="p1", axis=(0, 1, 0), radius=0.1)
    c2 = s.new_circle("c2", parent="p2", axis=(0, 1, 0), radius=0.1)
    c3 = s.new_circle("c3", parent="p3", axis=(0, 1, 0), radius=0.1)


    c = s.new_cable("cable", connections=["c1", "c2", "c3", "c1"], EA = 1000, length=2)

    assert_allclose(c.angles_at_connections, [90+45, 90, 90+45, 90+45], atol=0.1)

def test_bar_active_line():
    s=Scene()
    s.new_point(name="p1", position=(-10, 0, 0))
    s.new_point(name="p2", position=(10, 0, 0))
    s.new_point(name="b", position=(0, 0, 2))
    s.new_circle(name="bar", parent="b", radius=1.2, axis=(0, 1, 0), roundbar=True)

    c = s.new_cable(connections=["p1", "bar", "p2"], name="cable", EA=1e6, length=20)

    assert_allclose(c.angles_at_connections, [0,36.135129,0], atol=0.1)

def test_bar_inactive_line():
    s = Scene()
    s.new_point(name="p1", position=(-10, 0, 0))
    s.new_point(name="p2", position=(10, 0, 0))
    s.new_point(name="b", position=(0, 0, -2))
    s.new_circle(name="bar", parent="b", radius=1.2, axis=(0, 1, 0), roundbar=True)

    c = s.new_cable(connections=["p1", "bar", "p2"], name="cable", EA=1e6, length=20)

    assert_allclose(c.angles_at_connections, [0, -1, 0], atol=0.1)

    assert c.angles_at_connections[1] < 0

def test_bar_active_loop():
    s = Scene()
    s.new_point(name="p1", position=(-10, 0, 0))
    s.new_point(name="p2", position=(10, 0, 0))
    s.new_point(name="b", position=(0, 0, 2))
    s.new_circle(name="bar", parent="b", radius=1.2, axis=(0, 1, 0), roundbar=True)
    
    c = s.new_cable(connections=["p1", "bar", "p2"], name="cable", EA=1e6, length=20)
    
    assert_allclose(c.angles_at_connections, [0, 36.135129, 0], atol=0.1)


def test_circles_and_point():
    s = Scene()

    # code for Point
    s.new_point(name='Point',
                position=(0,
                          0,
                          0))

    # code for Point2
    s.new_point(name='Point2',
                position=(2,
                          0,
                          5))

    s.new_point('P3', position=(4, 0, 3))

    # code for Circle
    c = s.new_circle(name='Bottom',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Circle2
    c = s.new_circle(name='Top',
                     parent='Point2',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Loop
    s.new_cable(name='Loop',
                endA='Top',
                endB='Bottom',
                length=16.2832,
                diameter=0.5,
                EA=12345.0,
                sheaves=['P3'])

    loop = s['Loop']
    s.update()

    angles = loop.angles_at_connections

    expected = [ 0.      , 57.424753,  0.     ]
    assert_allclose(angles, expected)

def test_loop_with_circle_and_points():
    s = Scene()

    # code for Point
    s.new_point(name='Point',
                position=(0,
                          0,
                          0))

    # code for Point2
    s.new_point(name='Point2',
                position=(2,
                          0,
                          5))

    s.new_point('P3', position=(4, 0, 3))

    # code for Circle
    c = s.new_circle(name='Bottom',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Circle2
    c = s.new_circle(name='Top',
                     parent='Point2',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Loop
    s.new_cable(name='Loop',
                endA='Top',
                endB='Top',
                length=16.2832,
                diameter=0.5,
                EA=12345.0,
                sheaves=['P3','Bottom'])

    s.update()

    loop = s['Loop']
    angles = loop.angles_at_connections

    for a in angles:
        assert not isnan(a)





