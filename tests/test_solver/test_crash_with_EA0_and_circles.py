from DAVE import *


def model():
    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2023-12-18 09:35:37 UTC

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

    # code for upper_frame
    s.new_frame(name='upper_frame',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for lower_frame
    s.new_frame(name='lower_frame',
                position=(0,
                          0,
                          solved(-50.0)),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, False, True, True, True),
                )

    # code for pu0
    s.new_point(name='pu0',
                parent='upper_frame',
                position=(0,
                          0,
                          0))

    # code for force_point
    s.new_point(name='force_point',
                parent='lower_frame',
                position=(0,
                          0,
                          0))

    # code for pl0
    s.new_point(name='pl0',
                parent='lower_frame',
                position=(0,
                          0,
                          0))

    # code for Circle2
    c = s.new_circle(name='Circle2',
                     parent='pu0',
                     axis=(0, 1, 0),
                     radius=1)

    # code for force
    s.new_force(name='force',
                parent='force_point',
                force=(0, 0, -10000),
                moment=(0, 0, 0))

    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='pl0',
                     axis=(1, 0, 0),
                     radius=1)

    # code for Grommet1/_grommet
    s.new_cable(name='Grommet1/_grommet',
                endA='Circle2',
                endB='Circle2',
                length=40.0628,
                mass_per_length=0.00167698,
                diameter=0.02,
                EA=0.0,
                sheaves=['Circle'])
    s['Grommet1/_grommet'].reversed = (True, True, False)

    return s

def test_proper_message():
    """Needs build >= 2023-12-18"""
    s = model()
    try:
        s.solve_statics()
    except Exception as M:
        assert "Cable with mass needs to have a EA > 0 for Grommet1/_grommet" in str(M), "Unexpected error message"

