from numpy.testing import assert_allclose

from DAVE import *

def test_friction_cable_over_point():
    s = Scene()
    f = s.new_rigidbody('f', position=(0, 0, 0), fixed = (True, True, False, True, True, True), mass = 32)

    hook = s.new_point('hook', position=(0, 0, 0))
    s.new_point('p1', position=(0, 0, 0), parent=f)
    s.new_point('p2', position=(0, 0, 0), parent=f)

    c = s.new_cable(connections = ['p1', 'hook', 'p2'], name='cable', EA = 122345, friction=[0.1], length=7)

    s.solve_statics()

    weight = f.mass * s.g

    assert_allclose(hook.fz, -weight, rtol=1e-6)
    #
    expected_friction =  weight * 0.1
    assert_allclose(c.friction_forces[0], expected_friction, rtol=1e-6)

    # positive friction increases the tension on side A of the connection
    section1 = 0.5*weight + 0.5*expected_friction
    assert_allclose(c.segment_mean_tensions[0], section1, rtol=1e-6)

    section2 = 0.5*weight - 0.5*expected_friction
    assert_allclose(c.segment_mean_tensions[1], section2, rtol=1e-6)

def test_friction_cable_over_point_opposite():
    s = Scene()
    f = s.new_rigidbody('f', position=(0, 0, 0), fixed = (True, True, False, True, True, True), mass = 32)

    hook = s.new_point('hook', position=(0, 0, 0))
    s.new_point('p1', position=(0, 0, 0), parent=f)
    s.new_point('p2', position=(0, 0, 0), parent=f)

    c = s.new_cable(connections = ['p1', 'hook', 'p2'], name='cable', EA = 122345, friction=[-0.05], length=7)

    s.solve_statics()

    weight = f.mass * s.g

    assert_allclose(hook.fz, -weight, atol=1e-3)

    expected_friction =  weight * 0.05
    assert_allclose(c.friction_forces[0], -expected_friction, atol=1e-3)

    # positive friction increases the tension on side A of the connection
    section1 = 0.5*weight - 0.5*expected_friction
    assert_allclose(c.segment_mean_tensions[0], section1, atol=1e-3)

    section2 = 0.5*weight + 0.5*expected_friction
    assert_allclose(c.segment_mean_tensions[1], section2, atol=1e-3)

def test_friction_cable_over_two_points_symmetric():
    s = Scene()
    f = s.new_rigidbody('f', position=(0, 0, -10), fixed = (True, True, False, True, True, True), mass = 32)

    hook1 = s.new_point('hook1', position=(0, 0, 0))
    hook2 = s.new_point('hook2', position=(1, 0, 0))
    s.new_point('p1', position=(0, 0, 0), parent=f)
    s.new_point('p2', position=(1, 0, 0), parent=f)

    c = s.new_cable(connections = ['p1', 'hook1', 'hook2','p2'], name='cable', EA = 122345, friction=[0.05, -0.05], length=7)

    s.solve_statics()
    weight = f.mass * s.g

    segment_mean_tensions = c.segment_mean_tensions

    # check total weight is supported
    assert_allclose(segment_mean_tensions[0] + segment_mean_tensions[-1], weight, atol=1e-3)

    # check friction and section forces are symmetric
    assert_allclose(c.segment_mean_tensions[0], c.segment_mean_tensions[-1], atol=1e-2)
    assert_allclose(c.friction_forces[1], -c.friction_forces[0], atol=1e-2)


def test_friction_cable_over_multiple_points():
    s = Scene()
    f = s.new_rigidbody('f', position=(0, 0, -10), fixed = (True, True, False, True, True, True), mass = 32)

    hook1 = s.new_point('hook1', position=(0, 0, 0))
    hook2 = s.new_point('hook2', position=(0.3, 0, 0.5))
    hook3 = s.new_point('hook3', position=(0.6, 0, 0.4))
    hook4 = s.new_point('hook4', position=(1, 0, 0))
    s.new_point('p1', position=(0, 0, 0), parent=f)
    s.new_point('p2', position=(1, 0, 0), parent=f)


    c = s.new_cable(connections = ['p1', 'hook1', 'hook2','hook3','hook4','p2'], name='cable', EA = 122345, friction=[0.1,0.1,0.1,0.1], length=7)

    s.solve_statics()
    weight = f.mass * s.g

    segment_mean_tensions = c.segment_mean_tensions

    # check total weight is supported
    assert_allclose(segment_mean_tensions[0] + segment_mean_tensions[-1], weight, atol=1e-3)

    # check final 45/55 distribution
    assert_allclose(c.segment_mean_tensions[0] / c.segment_mean_tensions[-1], 55/45, atol=1e-6)


def test_friction_grommet_over_points():
    """Test friction in a grommet over two points

                         hook : friction 5% of normal force
                         |  |
        segment[1]       |  | segment[0] : high tension
           low tension   |  |
                         |  |
                          p1  : friction : solved


    """
    s = Scene()
    hook = s.new_point('hook', position=(0, 0, 0))
    s.new_point('p1', position=(0, 0, -10))

    c = s.new_cable(connections=['p1', 'hook', 'p1'], name='cable', EA=122345, friction=[None, 0.05], length=7)

    s.update()

    normal_force = -hook.fz
    mean_force = 0.5 * normal_force

    # expected friction = weight * 0.05
    expected_friction = normal_force * 0.05
    assert_allclose(c.friction_forces[0], -expected_friction, atol=1e-3)
    assert_allclose(c.friction_forces[1], expected_friction, atol=1e-3)

    # positive friction increases the tension on side A of the connection
    section1 = mean_force + 0.5 * expected_friction
    assert_allclose(c.segment_mean_tensions[0], section1, atol=1e-3)

    section2 =mean_force - 0.5 * expected_friction
    assert_allclose(c.segment_mean_tensions[1], section2, atol=1e-3)

def test_friction_grommet_over_points_solver():
    s = Scene()
    f = s.new_rigidbody('f', position=(0, 0, 0), fixed=(True, True, False, True, True, True), mass=32)

    hook = s.new_point('hook', position=(0, 0, 0))
    s.new_point('p1', position=(0, 0, 0), parent=f)

    c = s.new_cable(connections=['p1', 'hook', 'p1'], name='cable', EA=122345, friction=[None, 0.05], length=7)

    s.solve_statics()

    weight = f.mass * s.g

    assert_allclose(hook.fz, -weight, atol=1e-3)

    # expected friction = weight * 0.05
    expected_friction = weight * 0.05
    assert_allclose(c.friction_forces[0], -expected_friction, atol=1e-3)
    assert_allclose(c.friction_forces[1], expected_friction, atol=1e-3)

    # positive friction increases the tension on side A of the connection
    section1 = 0.5 * weight + 0.5 * expected_friction
    assert_allclose(c.segment_mean_tensions[0], section1, atol=1e-3)

    section2 = 0.5 * weight - 0.5 * expected_friction
    assert_allclose(c.segment_mean_tensions[1], section2, atol=1e-3)

    #

