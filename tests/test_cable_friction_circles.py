from numpy.testing import assert_allclose

from DAVE import *

def test_friction_cable_over_circle():
    s = Scene()
    f = s.new_rigidbody('f', position=(0, 0, 0), fixed = (True, True, False, True, True, True), mass = 32)

    hook_point = s.new_point('hook_point', position=(0, 0, 0))
    hook = s.new_circle('hook',parent = hook_point, axis=(0,1,0), radius=0.1)

    s.new_point('p1', position=(-0.1, 0, 0), parent=f)
    s.new_point('p2', position=(0.1, 0, 0), parent=f)

    c = s.new_cable(connections = ['p1', 'hook', 'p2'], name='cable', EA = 122345, friction=[0.05], length=7)

    s.solve_statics()

    weight = f.mass * s.g

    assert_allclose(hook_point.fz, -weight, atol=1e-3)

    expected_friction =  weight * 0.05
    assert_allclose(c.friction_forces[0] + c.friction_forces[1], expected_friction, atol=1e-3)

    # positive friction increases the tension on side A of the connection
    section1 = 0.5*weight + 0.5*expected_friction
    assert_allclose(c.segment_forces[0], section1, atol=1e-3)

    section2 = 0.5*weight - 0.5*expected_friction
    assert_allclose(c.segment_forces[-1], section2, atol=1e-3)

def test_friction_cable_over_circle_opposite():
    s = Scene()
    f = s.new_rigidbody('f', position=(0, 0, 0), fixed = (True, True, False, True, True, True), mass = 32)

    hook_point = s.new_point('hook_point', position=(0, 0, 0))
    hook = s.new_circle('hook',parent = hook_point, axis=(0,1,0), radius=0.1)

    s.new_point('p1', position=(-0.1, 0, 0), parent=f)
    s.new_point('p2', position=(0.1, 0, 0), parent=f)

    c = s.new_cable(connections = ['p1', 'hook', 'p2'], name='cable', EA = 122345, friction=[-0.05], length=7)

    s.solve_statics()

    weight = f.mass * s.g

    assert_allclose(hook_point.fz, -weight, atol=1e-3)

    expected_friction =  -weight * 0.05
    assert_allclose(c.friction_forces[0] + c.friction_forces[1], expected_friction, atol=1e-3)

    # positive friction increases the tension on side A of the connection
    section1 = 0.5*weight + 0.5*expected_friction
    assert_allclose(c.segment_forces[0], section1, atol=1e-3)

    section2 = 0.5*weight - 0.5*expected_friction
    assert_allclose(c.segment_forces[-1], section2, atol=1e-3)
#
# def test_friction_cable_over_two_points_symmetric():
#     s = Scene()
#     f = s.new_rigidbody('f', position=(0, 0, -10), fixed = (True, True, False, True, True, True), mass = 32)
#
#     hook1 = s.new_point('hook1', position=(0, 0, 0))
#     hook2 = s.new_point('hook2', position=(1, 0, 0))
#     s.new_point('p1', position=(0, 0, 0), parent=f)
#     s.new_point('p2', position=(1, 0, 0), parent=f)
#
#     c = s.new_cable(connections = ['p1', 'hook1', 'hook2','p2'], name='cable', EA = 122345, friction=[0.05, -0.05], length=7)
#
#     s.update()
#
#     s.solve_statics()
#
#     weight = f.mass * s.g
#
#     segment_forces = c.segment_forces
#
#     # check total weight is supported
#     assert_allclose (segment_forces[0] + segment_forces[-1], weight, atol = 1e-3)
#
#     # check friction and section forces are symmetric
#     assert_allclose(c.segment_forces[0], c.segment_forces[-1], atol=1e-3)
#     assert_allclose(c.friction_forces[1], -c.friction_forces[0], atol=1e-3)
#
#     # check that friction is 5% of the normal force
#     # cables are under a 90 degree angle
#     # (45 degrees each)
#
#     N1 = segment_forces[0] * np.cos(np.pi/4)
#     N2 = segment_forces[1] * np.cos(np.pi/4)
#
#     expected_friction = 0.05 * (N1 + N2)
#
#     assert_allclose(c.friction_forces[0], expected_friction, atol=1e-3)
#
#
#
# def test_friction_grommet_over_points():
#     """Test friction in a grommet over two points
#
#                          hook : friction 5% of normal force
#                          |  |
#         segment[1]       |  | segment[0] : high tension
#            low tension   |  |
#                          |  |
#                           p1  : friction : solved
#
#
#     """
#     s = Scene()
#     hook = s.new_point('hook', position=(0, 0, 0))
#     s.new_point('p1', position=(0, 0, -10))
#
#     c = s.new_cable(connections=['p1', 'hook', 'p1'], name='cable', EA=122345, friction=[None, 0.05], length=7)
#
#     s.update()
#
#     normal_force = -hook.fz
#     mean_force = 0.5 * normal_force
#
#     # expected friction = weight * 0.05
#     expected_friction = normal_force * 0.05
#     assert_allclose(c.friction_forces[0], -expected_friction, atol=1e-3)
#     assert_allclose(c.friction_forces[1], expected_friction, atol=1e-3)
#
#     # positive friction increases the tension on side A of the connection
#     section1 = mean_force + 0.5 * expected_friction
#     assert_allclose(c.segment_forces[0], section1, atol=1e-3)
#
#     section2 =mean_force - 0.5 * expected_friction
#     assert_allclose(c.segment_forces[1], section2, atol=1e-3)
#
# def test_friction_grommet_over_points_solver():
#     s = Scene()
#     f = s.new_rigidbody('f', position=(0, 0, 0), fixed=(True, True, False, True, True, True), mass=32)
#
#     hook = s.new_point('hook', position=(0, 0, 0))
#     s.new_point('p1', position=(0, 0, 0), parent=f)
#
#     c = s.new_cable(connections=['p1', 'hook', 'p1'], name='cable', EA=122345, friction=[None, 0.05], length=7)
#
#     s.solve_statics()
#
#     weight = f.mass * s.g
#
#     assert_allclose(hook.fz, -weight, atol=1e-3)
#
#     # expected friction = weight * 0.05
#     expected_friction = weight * 0.05
#     assert_allclose(c.friction_forces[0], -expected_friction, atol=1e-3)
#     assert_allclose(c.friction_forces[1], expected_friction, atol=1e-3)
#
#     # positive friction increases the tension on side A of the connection
#     section1 = 0.5 * weight + 0.5 * expected_friction
#     assert_allclose(c.segment_forces[0], section1, atol=1e-3)
#
#     section2 = 0.5 * weight - 0.5 * expected_friction
#     assert_allclose(c.segment_forces[1], section2, atol=1e-3)
#
#     #
#
