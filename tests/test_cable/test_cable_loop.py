import numpy as np
from numpy.testing import assert_allclose

from DAVE import *
import math

def basemodel(radius = 1.2):
    s = Scene()

    
    # code for Point
    s.new_point(name="Point", position=(0.0, 0.0, 5.0))
    # code for point2
    s.new_point(name="point2", position=(0.0, 0.0, -5.0))
    # code for Circle
    s.new_circle(name="Circle", parent="Point", axis=(0.0, 1.0, 0.0), radius=radius)
    # code for Circle_1
    s.new_circle(name="Circle_1", parent="point2", axis=(0.0, 1.0, 0.0), radius=radius)
    
    cab = s.new_cable(
        "Cable",
        endA="Circle_1",
        endB="Circle_1",
        sheaves=["Circle"],
        length=2,
        diameter=0.3,
    )
    return s

def test_simple_loop():

    radius = 1.2
    s = basemodel(radius=radius)

    cab = s["Cable"]

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

def test_loop_twist():
    s = basemodel(radius=1)
    circle2 = s['Circle_1']
    circle2.axis = (1,0,0) # rotated 90 degrees


    cab : Cable = s["Cable"]
    cab.EA = 1000
    cab.update()
    cab.set_length_for_tension(1000)

    s.update()

    assert_allclose(cab.tension,1000, atol=1e-3)

    # the vertical distance between the circle axis is 10m
    # the diameter of the wire is 0.3m
    # the radius of the circle is 1.0m
    # so the distance between the endpoint of the straight cable section and the vertical axis is 1.15m

    d = 1.15

    # the angle between the circles is 90 degrees

    # the horizontal distance between the cable enddpoints is
    dh = math.sqrt(2*d**2)

    # the length of the straight section is
    L = 9.9 # m  <== approximation, should be slightly less than 10
    Ls = math.sqrt(d**2 + d**2 + L**2)

    # the component of the force in "moment" direction is
    Fm = cab.tension * d / Ls

    print(Fm)

    Mz = Fm * d

    # and we have two cable sections
    Mz *= 2

    assert_allclose(s['point2'].applied_moment[2], Mz, rtol=1e-2)
    assert_allclose(s['Point'].applied_moment[2], -Mz, rtol=1e-2)



