from DAVE import *
from numpy.testing import assert_allclose

"""
Tests the weight of a cable indirectly.
A cable is attached to a frame. After solving the connection force of the frame to the world is checked.

This checks both the cable weight and the cog position

The reference CoG position is estimated to be at the center of the endpoints. This is accurate for
a straight cable, but not for catenary. For the tests with a catenary the cog position is therefore validated
with a higher tolerance.

"""

def run_test_cable_weight_single(x1=0., x2=10., L = 10., EA= 1., mass=1., ry=0., rotation = None, ftol=1e-5, mtol=1e-5, loop=False  ):
    s = Scene()
    f = s.new_frame('frame')
    p1 = s.new_point('p1', f, position=(x1, 0, 0))
    p2 = s.new_point('p2', f, position=(x2, 0, 0))
    cog_estimation = s.new_point('cog_estimation', f, position=(0.5 * (x1 + x2), 0, 0))

    if loop:
        c1 = s.new_circle('c1',p1, radius = 1, axis=(0,1,0))
        c2 = s.new_circle('c2',p2, radius = 1, axis=(0,1,0))

        w = s.new_cable('wire',c1,c1, sheaves = [c2], length = L, EA=EA, mass=mass)
    else:
        w = s.new_cable('wire', connections=[p1, p2], length=L, EA=EA, mass=mass)

    f.ry = ry

    if rotation:
        f.rotation = rotation

    s._save_coredump()

    s.update()
    assert_allclose(f.applied_force[2], -mass * s.g, atol=ftol)

    # calculate the expected moment, assuming the CoG is in the center of the endpoints
    moment = cog_estimation.gx * mass * s.g

    assert_allclose(f.applied_force[4], moment, atol=mtol)




def test_cable_weight_default():
    run_test_cable_weight_single()

def test_cable_weight_taut():
    for angle in range(-180,180,2):
        run_test_cable_weight_single(ry=angle, EA=1e6, L=9, mtol=1e-2)

def test_cable_weight_taut_3d(angles):
    for angle in angles:
        run_test_cable_weight_single(rotation=angle, EA=1e6, L=9, mtol=1e-2)

def test_cable_weight_supertaut():
    for angle in range(-180,180,2):
        run_test_cable_weight_single(ry=angle, EA=1e6, L=9, mtol=1e-2)

def test_cable_weight_supertaut_3d(angles):
    for angle in angles:
        run_test_cable_weight_single(rotation=angle, EA=1e6, L=9, mtol=1e-2)

def test_cable_weight_normal():
    for angle in range(-180,180,2):
        print(angle)
        run_test_cable_weight_single(ry=angle, EA=1e4, L=10, mtol=2)

def test_cable_weight_normal_3d(angles):
    for angle in angles:
        run_test_cable_weight_single(rotation=angle, EA=1e4, L=10, mtol=2)

def test_cable_weight_normal_3d(angles):
    for angle in angles:
        run_test_cable_weight_single(rotation=angle, EA=1e4, L=10, mtol=2)

def test_cable_weight_slack():
    for angle in range(-180,180,2):
        run_test_cable_weight_single(ry=angle, EA=1e4, L=15, mtol=10)

def test_cable_weight_slack_3d(angles):
    for angle in angles:
        run_test_cable_weight_single(rotation=angle, EA=1e4, L=15, mtol=10)


def test_wire_between_points_zero_width():
    """Check if the weight of single cable is calculated correctly.
    """
    s = Scene()
    f = s.new_frame('frame')
    p1 = s.new_point('p1',f, position = (10,0,0))
    p2 = s.new_point('p2',f, position = (10,0,1))

    w = s.new_cable('wire',connections=[p1,p2], length = 10, EA=1)
    w.mass_per_length = 1

    dc = s._vfc
    dc.state_prepare()

    s.solve_statics()

    assert_allclose(f.applied_force[2], -w.length * w.mass_per_length * s.g)
    assert_allclose(f.applied_force[4], 10*w.length * w.mass_per_length * s.g)

def test_wire_loop_horizontal():
    """Check if the weight of a looped cable is calculated correctly.
    """

    run_test_cable_weight_single(loop=True, ftol=1e-5, mtol=1e-3)

def test_wire_loop_angles(angles):
    """Check if the weight of a looped cable is calculated correctly.
    """

    for angle in range(-180,180,2):
        print(angle)
        run_test_cable_weight_single(ry=angle, mtol=2)

    for angle in angles:
        run_test_cable_weight_single(rotation=angle, mtol=2)


def test_wire_loop_angles_3d(angles):
    """Check if the weight of a looped cable is calculated correctly.
    """


    for angle in angles:
        run_test_cable_weight_single(loop=True, ftol=1e-5, mtol=3, rotation=angle)

    for angle in angles:
        run_test_cable_weight_single(loop=False, ftol=1e-5, mtol=2, rotation=angle)