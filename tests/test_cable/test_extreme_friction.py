"""Bugreport Freek

This crashes the core
"""
import pytest

from DAVE import *
def model_extreme_friction():

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
    s.new_rigidbody(name='Body',
                    mass=10,
                    cog=(1,
                         0,
                         0),
                    position=(solved(0.5),
                              solved(0.0),
                              solved(7.351)),
                    rotation=(solved(0),
                              solved(90),
                              solved(0)),
                    fixed=(False, False, False, False, False, False),
                    )

    # code for Hook1
    s.new_point(name='Hook1',
                position=(0,
                          0,
                          10))

    # code for Hook2
    s.new_point(name='Hook2',
                position=(5,
                          0,
                          10))

    # code for Liftpoint
    s.new_point(name='Liftpoint',
                parent='Body',
                position=(0,
                          0,
                          0))

    # code for Visual
    s.new_visual(name='Visual',
                 parent='Body',
                 path=r'res: cube_with_bevel.obj',
                 offset=(1, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(1, 1, 1))

    # code for Cable
    s.new_cable(name='Cable',
                endA='Hook1',
                endB='Hook2',
                length=10,
                EA=1000.0,
                sheaves=['Liftpoint'])
    s['Cable'].friction = [50.0]

    s.solver_settings.timeout_s = 3 # enough to check that it does not crash fatally

    # s.solver_settings.do_local_descent = True
    # s.solver_settings.do_local_descent = True
    # s.solver_settings.do_global_descent = False

    return s

def test_extreme_friction():
    assert False # test disables - hard crashes
    s = model_extreme_friction()
    s.solve_statics()

@pytest.mark.skip(reason="This test is interactive")
def test_extreme_friction_GUI_PressSolveToCrashTheGui():
    s = model_extreme_friction()
    DG(s)  # <--- press solve to crash the gui


if __name__ == '__main__':
    s = test_extreme_friction()

