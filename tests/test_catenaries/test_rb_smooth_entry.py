from numpy.testing import assert_almost_equal

"""Tests the smooth entry of a roundbar into a complex loop of a cable

test 1:

roundbar is under an angle
cable is a loop
cable has zero diameter

test 2:

cable has a zero segment between two point
cable has a diameter

"""

from DAVE import *
from DAVE_timeline import *

def test_smooth_taut_entry_points_test1():
    s = Scene()

    # code for Point
    s.new_point(name='Point',
                position=(-2,
                          0,
                          3))

    # code for Point2
    s.new_point(name='Point2',
                position=(10,
                          0,
                          0))

    # code for Point3
    s.new_point(name='Point3',
                position=(2,
                          -2,
                          6.74))

    # code for Point4
    s.new_point(name='Point4',
                position=(0,
                          0,
                          0))

    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='Point3',
                     axis=(0.57735, 0.57735, -0.57735),
                     roundbar=True,
                     radius=1)
    c.draw_stop = 32.0

    # code for Circle2
    c = s.new_circle(name='Circle2',
                     parent='Point4',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Cable
    s.new_cable(name='Cable',
                endA='Circle2',
                endB='Circle2',
                length=40,
                mass_per_length=0.0714286,
                EA=100000.0,
                sheaves=['Point',
                         'Circle',
                         'Point2'])


    import numpy as np

    zs = np.linspace(13,14.80,1000)
    fzs = []

    for z in zs:
        s['Point3'].z = z
        s.update()

        fzs.append(s['Point3'].fz)

    maxabsdiff = np.max(np.abs(np.diff(fzs)))

    assert_almost_equal(maxabsdiff, 0.0111714590881462071, 3)

def test_smooth_taut_entry_points_test1():
    s = Scene()

    # code for Point
    s.new_point(name='Point',
                position=(-2,
                          0,
                          3))

    # code for Point2
    s.new_point(name='Point2',
                position=(2,
                          0,
                          3))

    # code for Point3
    s.new_point(name='Point3',
                position=(0,
                          0,
                          -3))

    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='Point3',
                     axis=(0,1,0),
                     roundbar=True,
                     radius=0.5)

    # code for Cable
    s.new_cable(name='Cable',
                connections=['Point','Circle','Point2'],
                length=5,
                diameter=0.1,
                mass_per_length=0.0714286,
                EA=100000.0)

    # DG(s)

    import numpy as np

    zs = np.linspace(4,2,1000)
    fzs = []

    for z in zs:
        s['Point3'].z = z
        s.update()

        fzs.append(s['Point3'].fz)

    #
    #
    # import matplotlib.pyplot as plt
    # plt.plot(zs, fzs)
    # plt.show()

    dxdy = np.abs(np.diff(fzs)) # first derivative
    d2xdy2 = np.abs(np.diff(dxdy)) # second derivative

    maxabsdiff2 = np.max(d2xdy2)
    print(maxabsdiff2)

    assert_almost_equal(maxabsdiff2, 33.1473562541336, 3)
