from numpy.testing import assert_allclose
from DAVE import *



def convex_loop_180():
    s = Scene()

    # code for p1
    s.new_point(name="p1", position=(-10, 0, 0))

    # code for p2
    s.new_point(name="p2", position=(10, 0, 1))

    # code for p3
    s.new_point(name="p3", position=(0, 0, -1))

    # code for c_p1
    s.new_circle(name="c_p1", parent="p1", axis=(0, 1, 0), radius=1)

    # code for c
    c = s.new_cable(
        name="c",
        connections = ['c_p1','p2','p3','c_p1'],
        length=20,
        EA=1000.0,
        sheaves=["c_p2", "c_p3", "c_p4"],
    )

    return c,s

def test_convex_loop_180():
    c,s = convex_loop_180()

    A = 0.3
    c.friction = [A, -A , None]

    c.update()
    F1 = c.friction_forces

    c.friction = [None, -A , -A ]

    c.update()
    F2 = c.friction_forces

    assert_allclose(F1, F2, atol=1e-3)

def test_get_calculated_values():
    c,s  = convex_loop_180()

    A = 0.3
    c.friction = [A, -A , None]

    s.update()

    F = c.calculated_friction_factor
    assert_allclose(F, -A)

    c.friction = [None, -A , -A ]
    s.update()
    F = c.calculated_friction_factor
    assert_allclose(F, A)

    c.friction = [A, None, -A]
    s.update()
    F = c.calculated_friction_factor
    assert_allclose(F, -A)




