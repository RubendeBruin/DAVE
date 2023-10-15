"""Tests the core solver for a grommet around two points.

this used to cause an exception in the solver because of
taking the acos of a dot product where the dot product was 1.000000001 due to
rounding errors.
"""

from DAVE import *


def test_bug_acos_for_dot_product():
    s = Scene()
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

    # code for Body
    s.new_rigidbody(
        name="Body",
        mass=100,
        cog=(0, 0, 0),
        position=(
            solved(-2.117110379333387e-06),
            solved(-2.0119891269243955e-06),
            solved(-20.405334353799994),
        ),
        rotation=(solved(60.4788), solved(-37.3761), solved(23.1027)),
        fixed=(False, False, False, False, False, False),
    )

    # code for Hook
    s.new_point(name="Hook", position=(0, 0, 20))

    # code for LP1
    s.new_point(name="LP1", parent="Body", position=(10, 10, 5))

    # code for Visual
    s.new_visual(
        name="Visual",
        parent="Body",
        path=r"wirecube.obj",
        offset=(0, 0, 0),
        rotation=(0, 0, 0),
        scale=(10, 10, 5),
    )

    # code for sling_grommet0/_grommet
    s.new_cable(
        name="sling_grommet0/_grommet",
        endA="LP1",
        endB="LP1",
        length=50.4996,
        mass_per_length=0.008152,
        diameter=0.05,
        EA=79754.5654991329,
        sheaves=["Hook"],
    )
    s["sling_grommet0/_grommet"].friction = [None, 0.1]

    # Limits

    # Watches

    # Colors
    s.solve_statics()