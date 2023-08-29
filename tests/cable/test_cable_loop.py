import numpy as np
from numpy.testing import assert_allclose

from DAVE import *

def test_simple_loop():
    s = Scene()

    radius = 1.2

    # code for Point
    s.new_point(name='Point',
              position=(0.0,
                        0.0,
                        5.0))
    # code for point2
    s.new_point(name='point2',
              position=(0.0,
                        0.0,
                        -5.0))
    # code for Circle
    s.new_circle(name='Circle',
                parent='Point',
                axis=(0.0, 1.0, 0.0),
                radius=radius)
    # code for Circle_1
    s.new_circle(name='Circle_1',
                parent='point2',
                axis=(0.0, 1.0, 0.0),
                radius=radius )

    cab = s.new_cable('Cable', endA = 'Circle_1', endB= 'Circle_1',sheaves=['Circle'], length=2, diameter=0.3)

    # print(s._vfc.to_string())
    #
    s.solve_statics()
    #
    actual = cab.length + cab.stretch

    r = radius + (cab.diameter/2)

    expected = 2 * 10 + 2 * np.pi * r

    assert_allclose(actual, expected)

def test_table_loop_solve():
    s = Scene()

    # code for point2
    s.new_point(name='point2',
                position=(0.0,
                          0.0,
                          1.0))
    # code for point2_1
    s.new_point(name='point2_1',
                position=(-5.0,
                          -2.0,
                          1.0))
    # code for Body
    s.new_rigidbody(name='Body',
                    mass=2.0,
                    cog=(0.0,
                         0.0,
                         0.0),

                    fixed=(False, False, False, False, False, False))
    # code for Point
    s.new_point(name='Point',
                parent='Body',
                position=(0.0,
                          0.0,
                          2.0))
    # code for Circle_1
    s.new_circle(name='Circle_1',
                 parent='point2',
                 axis=(0.0, 1.0, 0.0),
                 radius=1.0)
    # code for Circle_1_1
    s.new_circle(name='Circle_1_1',
                 parent='point2_1',
                 axis=(0.0, -1.0, 0.0),
                 radius=1.0)
    # code for Circle
    s.new_circle(name='Circle',
                 parent='Point',
                 axis=(0.0, 1.0, 0.0),
                 radius=1.0)
    # code for Cable
    s.new_cable(name='Cable',
                endA='Circle_1',
                endB='Circle_1',
                length=22.0,
                EA=100.0,
                sheaves=['Circle_1_1',
                         'Circle'])
    s.solve_statics()