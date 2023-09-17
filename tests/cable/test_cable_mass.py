from numpy.testing import assert_allclose

from DAVE import *

def test_wide_hammock_with_mass():

    s = Scene()
    p1 = s.new_point(name='p1', position=(0, -2, 0))
    p2 = s.new_point(name='p2', position=(0, 2, 0))
    b = s.new_rigidbody(name='body', mass=1, fixed=True)
    b.fixed_z = False
    s.new_point('pbody', parent=b)
    c = s.new_circle(name='c1', parent='pbody', radius=1, axis=(1, 0, 0))
    c = s.new_cable(connections=['p1', 'c1', 'p2'], name='cable', EA=1e6, length=20, mass=10)

    s.solve_statics()

    assert_allclose(p1.fz, p2.fz, atol=1e-6)
    assert_allclose(p1.fz + p2.fz, -11 * s.g, atol=1e-4)

    s._save_coredump()

    # s.update()

    _, tensions = c.get_points_and_tensions_for_visual()  # should not modify the forces!

    for i in range(int(len(tensions) / 2)):
        assert_allclose(tensions[i], tensions[-(i+1)], atol=1e-6)

    # from DAVE.gui import Gui
    # Gui(s)

    assert_allclose(p1.fz, p2.fz, atol=1e-6)
    assert_allclose(p1.fz + p2.fz, -11 * s.g, atol=1e-4)

def test_straight_hammock_with_mass():

    s = Scene()
    p1 = s.new_point(name='p1', position=(0, -1, 0))
    p2 = s.new_point(name='p2', position=(0, 1, 0))
    b = s.new_rigidbody(name='body', mass=1, fixed=True)
    b.fixed_z = False
    s.new_point('pbody', parent=b)
    c = s.new_circle(name='c1', parent='pbody', radius=1, axis=(1, 0, 0))
    c = s.new_cable(connections=['p1', 'c1', 'p2'], name='cable', EA=1e6, length=20, mass=10)

    s.solve_statics()

    _, tensions = c.get_points_and_tensions_for_visual()

    for i in range(int(len(tensions) / 2)):
        assert_allclose(tensions[i], tensions[-(i+1)], atol=1e-6)

    assert_allclose(p1.fz, p2.fz, atol=1e-6)
    assert_allclose(p1.fz + p2.fz, -11*s.g, atol=1e-4)