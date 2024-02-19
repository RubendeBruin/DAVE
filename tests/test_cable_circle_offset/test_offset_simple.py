from numpy.testing import assert_allclose
from DAVE import *

"""Models the same situation twice : simple cable

Once using separate sheaves
and a second time using a single sheave and offsets on the cable

both should give the same results for the cable and the visualisation

"""

def model():
    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2024-02-14 09:41:22 UTC

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
                position=(0,
                          0,
                          0))

    # code for Point2
    s.new_point(name='Point2',
                position=(10.144,
                          0,
                          -1.591))

    # code for Point3
    s.new_point(name='Point3',
                position=(3.467,
                          0,
                          2.024))

    # code for Point4
    s.new_point(name='Point4',
                position=(3.467,
                          -0.25,
                          2.024))

    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='Point3',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Circle_offset
    c = s.new_circle(name='Circle_offset',
                     parent='Point4',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Cable_offsets
    s.new_cable(name='Cable_offsets',
                endA='Point',
                endB='Point2',
                length=14,
                diameter=0.5,
                EA=100.0,
                sheaves=['Circle'])
    s['Cable_offsets'].offsets = [0, 1, 0]

    # code for Cable_original
    s.new_cable(name='Cable_original',
                endA='Point',
                endB='Point2',
                length=14,
                diameter=0.5,
                EA=100.0,
                sheaves=['Circle_offset'])



    return s

def test_same_results():

    s = model()

    c1 = s['Cable_offsets']
    c2 = s['Cable_original']

    # both cables should effectively be the same
    s.update()

    assert_allclose(c1.length, c2.length)
    assert_allclose(c1.diameter, c2.diameter)
    assert_allclose(c1.EA, c2.EA)
    assert_allclose(c1.tension, c2.tension)
    assert_allclose(c1.stretch, c2.stretch)

    assert_allclose(c1.get_points_for_visual(), c2.get_points_for_visual())


def test_same_results_copy():

    s = model()
    s = s.copy()

    c1 = s['Cable_offsets']
    c2 = s['Cable_original']

    # both cables should effectively be the same
    s.update()

    assert_allclose(c1.length, c2.length)
    assert_allclose(c1.diameter, c2.diameter)
    assert_allclose(c1.EA, c2.EA)
    assert_allclose(c1.tension, c2.tension)
    assert_allclose(c1.stretch, c2.stretch)

    assert_allclose(c1.get_points_for_visual(), c2.get_points_for_visual())