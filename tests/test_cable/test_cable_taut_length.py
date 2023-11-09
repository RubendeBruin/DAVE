from numpy.testing import assert_allclose
from DAVE import *
import math
import numpy as np

def test_cable_length_points():
    """Tests the taut length of a grommet"""

    s = Scene()

    d = 1

    p1 = s.new_point('p1', position=(0, 0, 0))
    p2 = s.new_point('p2', position=(10, 0, 0))
    p3 = s.new_point('p3', position=(10, 0, 10))

    c = s.new_cable('c', connections=['p1', 'p2', 'p3'], EA=10, length=0.1, diameter=d)

    expected_length = 20
    assert_allclose(c.actual_length, expected_length, rtol=1e-6)

def test_cable_loop_length_points():
    """Tests the taut length of a grommet"""

    s = Scene()

    d = 0.5

    f1 = s.new_frame('f1', position=(-1, 2, 0.23451), rotation=(10,6,20))  # under a weird rotation and position

    p1 = s.new_point('p1', parent=f1, position=(0, 0, 0))
    p2 = s.new_point('p2', parent=f1, position=(10, 0, 0))

    c = s.new_cable('c', connections=['p1', 'p2', 'p1'], EA=10, length=0.1, diameter=d)

    expected_length = 20
    assert_allclose(c.actual_length, expected_length, rtol=1e-6)


def test_cable_loop_length_circles():
    """Tests the taut length of a grommet"""

    s = Scene()

    r = 1
    d = 0.5

    f1 = s.new_frame('f1', position=(-1, 2, 0.23451), rotation=(10,6,20))  # under a weird rotation and position

    p1 = s.new_point('p1', parent=f1, position=(0, 0, 0))
    p2 = s.new_point('p2', parent=f1, position=(10, 0, 0))

    c1 = s.new_circle('c1', p1, axis=(0, 1, 0), radius=r)
    c2 = s.new_circle('c2', p2, axis=(0, 1, 0), radius=r)

    c = s.new_cable('c', connections=['c1', 'c2', 'c1'], EA=10, length=0.1, diameter=d)

    expected_length = 2 * math.pi * (r + d/2) + 20
    assert_allclose(c.actual_length, expected_length, rtol=1e-6)

    # check the drawing length
    points, tensions = c.get_points_and_tensions_for_visual()

    pd = np.array(points)
    d = np.diff(pd, axis=0)
    length = np.linalg.norm(d, axis=1).sum()

    assert_allclose(length, expected_length, atol=0.1)


def test_cable_loop_drawing_length_taut():
    """Tests the slack length of a grommet"""

    s = Scene()

    r = 1
    d = 0.5

    f1 = s.new_frame('f1')

    p1 = s.new_point('p1', parent=f1, position=(0, 0, 0))
    p2 = s.new_point('p2', parent=f1, position=(10, 0, 0))

    c1 = s.new_circle('c1', p1, axis=(0, 1, 0), radius=r)
    c2 = s.new_circle('c2', p2, axis=(0, 1, 0), radius=r)

    c = s.new_cable('c', connections=['c1', 'c2', 'c1'], EA=10000000, length=20, diameter=d)
    #

    points, tensions = c._vfNode.get_drawing_data(300, 300,
                                                     False)

    # x = [p[0] for p in points]
    # y = [p[2] for p in points]
    #
    # import matplotlib.pyplot as plt
    # plt.plot(x, y)
    # plt.axis('equal')
    # plt.show()

    #
    pd = np.array(points)
    d = np.diff(pd, axis=0)
    length = np.linalg.norm(d, axis=1).sum()
    #

    expected = 2*10 + 2*math.pi*(r + c.diameter/2)

    assert_allclose(length, expected, atol = 0.001)

def test_cable_loop_drawing_length_slack():
    """Tests the slack length of a grommet"""

    s = Scene()

    r = 1
    d = 0.5

    f1 = s.new_frame('f1')

    p1 = s.new_point('p1', parent=f1, position=(0, 0, 0))
    p2 = s.new_point('p2', parent=f1, position=(10, 0, 0))

    c1 = s.new_circle('c1', p1, axis=(0, 1, 0), radius=r)
    c2 = s.new_circle('c2', p2, axis=(0, 1, 0), radius=r)

    c = s.new_cable('c', connections=['c1', 'c2', 'c1'], EA=10000000, length=30, diameter=d)
    #

    s._save_coredump()

    # lenght on sheaves
    LOS = 2 * math.pi * (r + c.diameter / 2)
    print(f"Expected material length on sheave = {LOS / 2}")
    expected = 30 -2 * math.pi * (r + c.diameter / 2)
    print(f"Expected material length = {expected/2}")

    points, tensions = c._vfNode.get_drawing_data(300, 300,
                                                     False)

    # x = [p[0] for p in points]
    # y = [p[2] for p in points]
    #
    # import matplotlib.pyplot as plt
    # plt.plot(x, y)
    # plt.axis('equal')
    # plt.show()

    #
    pd = np.array(points)
    d = np.diff(pd, axis=0)
    length = np.linalg.norm(d, axis=1).sum()
    #

    expected = 30

    assert_allclose(length, expected, atol = 0.001)


def test_cable_loop_drawing_length_slack_angled():
    """Tests the slack length of a grommet"""

    s = Scene()

    r = 1
    d = 0.5

    f1 = s.new_frame('f1', position=(-1, 2, 0.23451), rotation=(10, 6, 20))  # under a weird rotation and position

    p1 = s.new_point('p1', parent=f1, position=(0, 0, 0))
    p2 = s.new_point('p2', parent=f1, position=(10, 0, 0))

    c1 = s.new_circle('c1', p1, axis=(0, 1, 0), radius=r)
    c2 = s.new_circle('c2', p2, axis=(0, 1, 0), radius=r)

    c = s.new_cable('c', connections=['c1', 'c2', 'c1'], EA=10000000, length=30, diameter=d)
    #

    points, tensions = c.get_points_and_tensions_for_visual()
    #
    pd = np.array(points)
    d = np.diff(pd, axis=0)
    length = np.linalg.norm(d, axis=1).sum()
    #
    assert_allclose(length, 30, atol=0.1)