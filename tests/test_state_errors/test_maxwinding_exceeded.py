from DAVE import *


def model():
    s = Scene()
    # auto generated python code
    # By MS12H
    # Time: 2024-01-23 20:28:37 UTC

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
    s.new_point(name="Point", position=(0, 0, 0))

    # code for Point2
    s.new_point(name="Point2", position=(20, 0, 0))

    # code for Point3
    s.new_point(name="Point3", position=(10, 0, 5))

    # code for Circle
    c = s.new_circle(name="Circle", parent="Point3", axis=(0, 1, 0), radius=1)

    # code for Cable
    s.new_cable(
        name="Cable",
        endA="Point",
        endB="Point2",
        length=31.1355,
        EA=0.0,
        sheaves=["Circle"],
    )
    s["Cable"].reversed = (False, True, False)
    s["Cable"].max_winding_angles = [999, 200.0, 999]

    return s


def test_exceeded():
    s = model()
    assert s.warnings  # should be at least one error
    assert s.warnings[0][0] == s["Cable"]
