"""Issue 144"""

import pytest
from DAVE import *

def model():
    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2023-11-29 21:43:30 UTC

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

    # code for Point
    s.new_point(name='Point',
                position=(-2.646,
                          -0.478,
                          4.336))

    # code for Point2
    s.new_point(name='Point2',
                position=(4.763,
                          -0.416,
                          0.871))

    # code for gg
    s.new_point(name='gg',
                position=(8.082,
                          4.803,
                          5.227))

    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Circle2
    c = s.new_circle(name='Circle2',
                     parent='Point2',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Circle3
    c = s.new_circle(name='Circle3',
                     parent='gg',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Cable
    s.new_cable(name='Cable',
                endA='Circle3',
                endB='Circle3',
                length=26.3797,
                EA=0.0,
                sheaves=['Circle',
                         'Circle2',
                         'Circle',
                         'Circle2'])

    return s

def test():
    s = model()

    with pytest.raises(ValueError):
        s['Circle3'].is_roundbar = True

    # s.update()  #<-- fatal crash if previous is executed
