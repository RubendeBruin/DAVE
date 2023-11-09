import numpy as np
from numpy.testing import assert_allclose
import math

from DAVE import *

def test_friction_cable_over_circle():
    s = Scene()
    f = s.new_rigidbody('f', position=(0, 0, 0), fixed = (True, True, False, True, True, True), mass = 32)

    hook_point = s.new_point('hook_point', position=(0, 0, 0))
    hook = s.new_circle('hook',parent = hook_point, axis=(0,1,0), radius=0.4)

    s.new_point('p1', position=(-0.5, 0, 0), parent=f)
    s.new_point('p2', position=(0.5, 0, 0), parent=f)

    c = s.new_cable(connections = ['p1', 'hook', 'p2'], name='cable', EA = 122345, friction=[0.1], length=7, diameter=0.2)

    s.solve_statics()

    weight = f.mass * s.g

    assert_allclose(hook_point.fz, -weight, atol=1e-6)

    expected_friction =  weight * 0.1
    assert_allclose(c.friction_forces[0] ,expected_friction, atol=1e-6)

    # positive friction increases the tension on side A of the connection
    section1 = 0.5*weight + 0.5*expected_friction
    assert_allclose(c.segment_mean_tensions[0], section1, atol=1e-6)

    section2 = 0.5*weight - 0.5*expected_friction
    assert_allclose(c.segment_mean_tensions[-1], section2, atol=1e-6)


def test_friction_cable_over_circle_opposite():
    s = Scene()
    f = s.new_rigidbody('f', position=(0, 0, 0), fixed = (True, True, False, True, True, True), mass = 32)

    hook_point = s.new_point('hook_point', position=(0, 0, 0))
    hook = s.new_circle('hook',parent = hook_point, axis=(0,1,0), radius=0.1)

    s.new_point('p1', position=(-0.1, 0, 0), parent=f)
    s.new_point('p2', position=(0.1, 0, 0), parent=f)

    c = s.new_cable(connections = ['p1', 'hook', 'p2'], name='cable', EA = 122345, friction=[-0.1], length=7)

    s.solve_statics()

    weight = f.mass * s.g

    assert_allclose(hook_point.fz, -weight, atol=1e-3)

    expected_friction =  -weight * 0.1
    assert_allclose(c.friction_forces[0], expected_friction, atol=1e-3)

    # positive friction increases the tension on side A of the connection
    section1 = 0.5*weight + 0.5*expected_friction
    assert_allclose(c.segment_mean_tensions[0], section1, atol=1e-3)

    section2 = 0.5*weight - 0.5*expected_friction
    assert_allclose(c.segment_mean_tensions[-1], section2, atol=1e-3)
#
def test_friction_cable_over_two_circles_symmetric():
    s = Scene()
    f = s.new_rigidbody('f', position=(0, 0, -10), fixed = (True, True, False, True, True, True), mass = 32)

    hook1 = s.new_point('hook1', position=(0, 0, 0))
    hook2 = s.new_point('hook2', position=(1, 0, 0))

    hs1 = s.new_circle('hs1',parent = hook1, axis=(0,1,0), radius=0.1)
    hs2 = s.new_circle('hs2',parent = hook2, axis=(0,1,0), radius=0.1)

    s.new_point('p1', position=(-0.1, 0, 0), parent=f)
    s.new_point('p2', position=(1.1, 0, 0), parent=f)

    c = s.new_cable(connections = ['p1', 'hs1', 'hs2','p2'], name='cable', EA = 122345, friction=[0.05, -0.05], length=7)

    s.solve_statics()
    weight = f.mass * s.g

    segment_mean_tensions = c.segment_mean_tensions

    # check total weight is supported
    assert_allclose (segment_mean_tensions[0] + segment_mean_tensions[-1], weight, atol = 1e-3)

    # check friction and section forces are symmetric
    assert_allclose(c.segment_mean_tensions[0], c.segment_mean_tensions[-1], atol=1e-2)
    assert_allclose(c.friction_forces[1], -c.friction_forces[0], atol=1e-2)



def test_friction_cable_over_two_circles_none_symmetric():
    s = Scene()

    # code for Frame
    s.new_frame(name='Frame',
                position=(-4,0,0))

    # code for f
    s.new_rigidbody(name='f',
                    mass=32,
                    cog=(0,
                         0,
                         0),
                    parent='Frame',
                    fixed=(True, False, False, True, True, True))

    # code for hook2
    s.new_point(name='hook2',
                parent='Frame',
                position=(0.5,
                          0,
                          3))

    # code for hook1
    s.new_point(name='hook1',
                parent='Frame',
                position=(-0.5,
                          0,
                          3))

    # code for p1
    s.new_point(name='p1',
                parent='f',
                position=(-1,
                          0,
                          0))

    # code for p2
    s.new_point(name='p2',
                parent='f',
                position=(1,
                          0,
                          0))

    # code for hs2
    s.new_circle(name='hs2',
                 parent='hook2',
                 axis=(0, 1, 0),
                 radius=0.4)

    # code for hs1
    s.new_circle(name='hs1',
                 parent='hook1',
                 axis=(0, 1, 0),
                 radius=0.4)

    # code for cable
    c = s.new_cable(name='cable',
                endA='p1',
                endB='p2',
                length=7,
                diameter=0.2,
                EA=122345.0,
                sheaves=['hs1',
                         'hs2'])

    c.friction = (0.1, 0.1)

    s.solve_statics()

    # assert_allclose(c.friction_forces[0], c.friction_forces[1], atol=1e-3)
    assert_allclose(c.segment_mean_tensions[0] / c.segment_mean_tensions[-1], 55/45, atol=1e-6)







def test_friction_cable_over_three_circles():
    s = Scene()

    # code for Frame
    s.new_frame(name='Frame',
                position=(-4,0,0))

    # code for f
    s.new_rigidbody(name='f',
                    mass=32,
                    cog=(0,
                         0,
                         0),
                    parent='Frame',
                    fixed=(True, False, False, True, True, True))

    # code for hook3
    s.new_point(name='hook3',
                parent='Frame',
                position=(0.2,
                          0,
                          5))

    # code for hook2
    s.new_point(name='hook2',
                parent='Frame',
                position=(0.5,
                          0,
                          3))

    # code for hook1
    s.new_point(name='hook1',
                parent='Frame',
                position=(-0.5,
                          0,
                          3))

    # code for p1
    s.new_point(name='p1',
                parent='f',
                position=(-1,
                          0,
                          0))

    # code for p2
    s.new_point(name='p2',
                parent='f',
                position=(1,
                          0,
                          0))


    # code for hs3
    s.new_circle(name='hs3',
                 parent='hook3',
                 axis=(0, 1, 0),
                 radius=0.2)

    # code for hs2
    s.new_circle(name='hs2',
                 parent='hook2',
                 axis=(0, 1, 0),
                 radius=0.4)

    # code for hs1
    s.new_circle(name='hs1',
                 parent='hook1',
                 axis=(0, 1, 0),
                 radius=0.4)

    # code for cable
    c = s.new_cable(name='cable',
                endA='p1',
                endB='p2',
                length=7,
                diameter=0.2,
                EA=122345.0,
                sheaves=['hs1',
                         'hs3',
                         'hs2'])

    c.friction = (0.1, 0.1,0.1)

    s.solve_statics()

    # assert_allclose(c.friction_forces[0], c.friction_forces[1], atol=1e-3)
    assert_allclose(c.segment_mean_tensions[0] / c.segment_mean_tensions[-1], 55/45, atol=1e-3)

def test_friction_grommet_over_circles():
    """Test friction in a grommet over two points

                         hook : friction 5% of normal force
                         |  |
        segment[1]       |  | segment[0] : high tension
           low tension   |  |
                         |  |
                          p1  : friction : solved


    """
    s = Scene()
    hook_point = s.new_point('hook_point', position=(0, 0, 0))
    hook = s.new_circle('hook', parent=hook_point, axis=(0, 1, 0), radius=0.1)
    s.new_point('p1_point', position=(0, 0, -10))
    p1 = s.new_circle('p1', parent='p1_point', axis=(0, 1, 0), radius=0.1)

    c = s.new_cable(connections=['p1', 'hook', 'p1'], name='cable', EA=122345, friction=[None, 0.05], length=7)

    # s._save_coredump()

    s.update()

    normal_force = -hook_point.fz
    mean_force = 0.5 * normal_force

    # check mean force
    assert_allclose(np.mean(c.segment_mean_tensions), mean_force, atol=1e-6)

    # expected friction = weight * 0.05
    expected_friction = normal_force * 0.05
    assert_allclose(c.friction_forces[0], -expected_friction, rtol=1e-6)
    assert_allclose(c.friction_forces[1], expected_friction, rtol=1e-6)

    # positive friction increases the tension on side A of the connection
    section1 = mean_force + 0.5 * expected_friction
    assert_allclose(c.segment_mean_tensions[0], section1, atol=1e-3)

    section2 =mean_force - 0.5 * expected_friction
    assert_allclose(c.segment_mean_tensions[1], section2, atol=1e-3)

def test_friction_grommet_over_circles_higher_friction():
    """Test friction in a grommet over two points

                         hook : friction 5% of normal force
                         |  |
        segment[1]       |  | segment[0] : high tension
           low tension   |  |
                         |  |
                          p1  : friction : solved


    """
    s = Scene()
    hook_point = s.new_point('hook_point', position=(0, 0, 0))
    hook = s.new_circle('hook', parent=hook_point, axis=(0, 1, 0), radius=0.1)
    s.new_point('p1_point', position=(0, 0, -10))
    p1 = s.new_circle('p1', parent='p1_point', axis=(0, 1, 0), radius=0.1)

    c = s.new_cable(connections=['p1', 'hook', 'p1'], name='cable', EA=122345, friction=[None, 0.5], length=7)

    s.update()

    normal_force = -hook_point.fz
    mean_force = 0.5 * normal_force

    # check mean force
    assert_allclose(np.mean(c.segment_mean_tensions), mean_force, atol=1e-6)

    # expected friction = weight * 0.05
    expected_friction = normal_force * 0.5
    assert_allclose(c.friction_forces[0], -expected_friction, rtol=1e-6)
    assert_allclose(c.friction_forces[1], expected_friction, rtol=1e-6)

    # positive friction increases the tension on side A of the connection
    section1 = mean_force + 0.5 * expected_friction
    assert_allclose(c.segment_mean_tensions[0], section1, rtol=1e-6)

    section2 =mean_force - 0.5 * expected_friction
    assert_allclose(c.segment_mean_tensions[1], section2, rtol=1e-6)


def test_demo_90deg():
    s = Scene()
    mass = 100
    # code for f

    s.new_rigidbody(name='f',
                    mass=mass,
                    fixed=(True, True, False, True, True, True))

    # code for hook1
    s.new_point(name='hook1',
                position=(0,
                          0,
                          0))

    # code for p2
    s.new_point(name='p2',
                position=(6,
                          0,
                          1))

    # code for p1
    s.new_point(name='p1',
                parent='f',
                position=(-1,
                          0,
                          0))

    # code for hs1
    s.new_circle(name='hs1',
                 parent='hook1',
                 axis=(0, 1, 0),
                 radius=0.95)

    # code for cable
    c = s.new_cable(name='cable',
                endA='p1',
                endB='p2',
                length=20,
                diameter=0.1,
                EA=122345.0,
                sheaves=['hs1'])

    # 90 degrees
    s.solve_statics()

    c.friction = [0.1]

    s.solve_statics()

    factor = ((1-0.1)/(1+0.1))**(90/180)


    tensions = c.segment_mean_tensions
    assert_allclose(tensions[0], s.g*mass, atol=1e-5)
    assert_allclose(tensions[1], s.g*mass * factor, atol=1e-5)

def test_demo_270deg():
    s = Scene()
    mass = 100
    # code for f

    s.new_rigidbody(name='f',
                    mass=mass,
                    fixed=False)

    # code for hook1
    s.new_point(name='hook1',
                position=(0,
                          0,
                          0))

    # code for p2
    s.new_point(name='p2',
                position=(6,
                          0,
                          -1))

    # code for p1
    s.new_point(name='p1',
                parent='f',
                position=(-1,
                          0,
                          0))

    # code for hs1
    s.new_circle(name='hs1',
                 parent='hook1',
                 axis=(0, -1, 0),
                 radius=0.95)

    # code for cable
    c = s.new_cable(name='cable',
                endA='p1',
                endB='p2',
                length=20,
                diameter=0.1,
                EA=122345.0,
                sheaves=['hs1'])

    # 270 degrees
    c.friction = [0.1]

    s.solve_statics()

    factor = ((1 - 0.1) / (1 + 0.1)) ** (270 / 180)

    tensions = c.segment_mean_tensions
    assert_allclose(tensions[0], s.g * mass, atol=1e-5)
    assert_allclose(tensions[1], s.g * mass * factor, atol=1e-5)


def test_friction_over_three_circle_loop():
    """Equal sides:

            c2

        c1      c3


    Returns:

    """

    s = Scene()
    p1 = s.new_point("p1", position=(-10, 0, 0))
    p3 = s.new_point("p2", position=(0, 0, math.sqrt(20**2 - 10**2)))
    p2 = s.new_point("p3", position=(10, 0, 0))

    c1 = s.new_circle("c1", radius=1, parent="p1", axis=(0,1,0))
    c2 = s.new_circle("c2", radius=1, parent="p2", axis=(0,1,0))
    c3 = s.new_circle("c3", radius=1, parent="p3", axis=(0,1,0))

    c = s.new_cable(
        connections=["c1", "c2", "c3", "c1"],
        name="cable",
        EA=122345,
        friction=[0.1, None, 0.1],
        length=20,
        diameter=0.4
    )

    s._save_coredump()

    expected = [254963.727468, 333184.395387, 291461.721985]
    assert_allclose(c.segment_mean_tensions, expected, atol=1e-6)
