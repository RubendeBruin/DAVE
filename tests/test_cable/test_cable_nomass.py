from numpy.testing import assert_allclose

from DAVE import *

def test_cable_force():
    s = Scene()
    p1 = s.new_point('p1', position=(0, 0, 0))
    p2 = s.new_point('p2', position=(10, 0, 0))
    c = s.new_cable('c', connections=['p1', 'p2'], EA=1000, length=2)

    s.update()

    stretch = (10 - 2) / 2
    expected = stretch * 1000
    assert_allclose(c.tension, expected, rtol=1e-6)
    assert_allclose(p1.force, expected, rtol=1e-6)
    assert_allclose(p1.force, expected, rtol=1e-6)
    assert_allclose(p1.applied_force, (expected, 0, 0), rtol=1e-6)
    assert_allclose(p2.applied_force, (-expected, 0, 0), rtol=1e-6)

def test_solve_pendulum():
    s = Scene()
    p1 = s.new_point('p1', position=(0, 0, 0))
    b = s.new_rigidbody('b', position=(0, 0, 0), fixed=False, mass=1)
    p2 = s.new_point('p2', position=(0, 0, 0), parent=b)
    c = s.new_cable('c', connections=['p1', 'p2'], EA=1000, length=2)

    s.solve_statics()

def test_solve_pendulum_with_cableweight():
    s = Scene()
    p1 = s.new_point('p1', position=(0, 0, 0))
    b = s.new_rigidbody('b', position=(0, 0, 0), fixed=False, mass=1)
    p2 = s.new_point('p2', position=(0, 0, 0), parent=b)
    c = s.new_cable('c', connections=['p1', 'p2'], EA=1000, length=2, mass=1)

    s.solve_statics()

    expected = 2 * s.g

    assert_allclose(p1.force, expected, rtol=1e-5)
    assert_allclose(c.tension, expected, rtol=1e-5)
    assert_allclose(p2.force, b.mass * s.g, rtol=1e-5)
