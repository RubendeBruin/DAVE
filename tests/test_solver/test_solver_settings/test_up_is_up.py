from DAVE import *

def model():
    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2023-12-15 09:35:30 UTC

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


    # code for Body
    s.new_rigidbody(name='Body',
                    mass=10,
                    cog=(0.20,
                         0.20,
                         3),
                    position=(solved(0.0),
                              solved(0.0),
                              solved(0.0)),
                    rotation=(solved(0),
                              solved(0),
                              solved(0)),
                    fixed=(False, False, False, False, False, False),
                    )

    # code for LP
    s.new_point(name='LP',
                position=(0,
                          0,
                          14))

    # code for Point
    s.new_point(name='Point',
                parent='Body',
                position=(0,
                          0,
                          0))

    # code for Point2
    s.new_point(name='Point2',
                parent='Body',
                position=(0,
                          1,
                          0))

    # code for Point3
    s.new_point(name='Point3',
                parent='Body',
                position=(1,
                          0,
                          0))

    # code for Cable
    s.new_cable(name='Cable',
                endA='LP',
                endB='Point',
                length=10,
                EA=1e+07)

    # code for Cable2
    s.new_cable(name='Cable2',
                endA='LP',
                endB='Point2',
                length=10,
                EA=1e+07)

    # code for Cable3
    s.new_cable(name='Cable3',
                endA='LP',
                endB='Point3',
                length=10,
                EA=1e+07)

    s.solver_settings.do_deterministic = True
    s.solver_settings.do_linear_first = True
    s.solver_settings.tolerance_during_linear_phase = 1e-4
    s.solver_settings.mobility = 20

    return s

def test_no_flip_with_up_is_up():
    s = model()

    s.solver_settings.up_is_up_factor = 1.0

    s.solve_statics()

    glob_up = s['Body'].to_glob_direction((0,0,1))
    assert glob_up[2] > 0

def test_no_flip_with_up_is_up_extreme():
    s = model()
    s.solver_settings.up_is_up_factor = 10

    s.solve_statics()

    glob_up = s['Body'].to_glob_direction((0,0,1))
    assert glob_up[2] > 0


def test_flip_without_up_is_up():
    s = model()
    s.solver_settings.up_is_up_factor = 0.0

    s.solve_statics()

    glob_up = s['Body'].to_glob_direction((0, 0, 1))
    assert glob_up[2] < 0

