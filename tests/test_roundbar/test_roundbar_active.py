"""See also: tests/test_cable/test_roundbar.py

But now with a cable diameter
"""
from numpy.testing import assert_allclose

from DAVE import *

def test_roundbar_active_wire_diameter():
    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2023-12-06 18:31:35 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution

    def solved(number):
        return number

    # Environment settings
    s.g = 9.80665
    s.waterlevel = 0.0
    s.rho_air = 0.00126
    s.rho_water = 1.025
    s.wind_direction = 0.0
    s.wind_velocity = 0.0
    s.current_direction = 0.0
    s.current_velocity = 0.0

    # code for p1
    s.new_point(name='p1',
                position=(-10,
                          0,
                          0))

    # code for p2
    s.new_point(name='p2',
                position=(10,
                          0,
                          0))

    # code for b
    s.new_point(name='b',
                position=(0,
                          0,
                          -1.5))

    # code for bar
    c = s.new_circle(name='bar',
                     parent='b',
                     axis=(0, 1, 0),
                     roundbar=True,
                     radius=1.2)
    c.draw_start = -6.0
    c.draw_stop = 8.0

    # code for cable
    s.new_cable(name='cable',
                endA='p1',
                endB='p2',
                length=20,
                diameter=2,
                EA=1000000.0,
                sheaves=['bar'])

    # code for cable2
    s.new_cable(name='cable2',
                endA='p1',
                endB='p2',
                length=20,
                diameter=0.1,
                EA=1000000.0,
                sheaves=['bar'])

    s.update()

    thick_cable = s['cable']
    thin_cable = s['cable2']

    assert(thick_cable.actual_length>20.04)
    assert_allclose(thin_cable.actual_length,20)
