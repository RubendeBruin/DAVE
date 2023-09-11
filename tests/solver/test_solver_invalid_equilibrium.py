from DAVE import *

def test_solver_accepts_invalid_static_equilibrium():

    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2023-08-29 20:31:12 UTC

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



    # code for Frame
    s.new_frame(name='Frame',
               position=(0,
                         0,
                         0),
               rotation=(0,
                         0,
                         0),
               fixed =(True, True, True, True, True, True) )

    # code for Load
    s.new_rigidbody(name='Load',
                    mass=2,
                    cog=(1,
                         0,
                         -4),
                    position=(solved(1.70637),
                              solved(0),
                              solved(-11.3306)),
                    rotation=(solved(0),
                              solved(39.4764),
                              solved(0)),
                    fixed =(False, False, False, False, False, False) )

    # code for SpacerBar
    s.new_rigidbody(name='SpacerBar',
                    mass=0.1,
                    cog=(0,
                         0,
                         0),
                    position=(solved(1.29562),
                              solved(0),
                              solved(-9.62734)),
                    rotation=(solved(0),
                              solved(43.1292),
                              solved(0)),
                    fixed =(False, False, False, False, False, False) )

    # code for Point_1
    s.new_point(name='Point_1',
              parent='Frame',
              position=(0,
                        0,
                        0))

    # code for Point_2
    s.new_point(name='Point_2',
              parent='Load',
              position=(-7,
                        0,
                        0))

    # code for Point_3
    s.new_point(name='Point_3',
              parent='Load',
              position=(7,
                        0,
                        0))

    # code for Point
    s.new_point(name='Point',
              parent='SpacerBar',
              position=(5,
                        0,
                        0))

    # code for Point_4
    s.new_point(name='Point_4',
              parent='SpacerBar',
              position=(-5,
                        0,
                        0))

    # code for Cable_1
    s.new_cable(name='Cable_1',
                endA='Point_4',
                endB='Point',
                length=20.5913,
                EA=100000.0,
                sheaves = ['Point_1'])
    s['Cable_1'].max_winding_angles = [999, 999, 999]

    # code for Circle
    s.new_circle(name='Circle',
                parent='Point_1',
                axis=(0, 1, 0),
                radius=1 )

    # code for Circle_1
    s.new_circle(name='Circle_1',
                parent='Point',
                axis=(0, 1, 0),
                radius=1 )

    # code for Circle_2
    s.new_circle(name='Circle_2',
                parent='Point_4',
                axis=(0, 1, 0),
                radius=1 )

    # code for Cable
    s.new_cable(name='Cable',
                endA='Point_3',
                endB='Point_2',
                length=40,
                EA=103000.0,
                sheaves = ['Circle_1',
                           'Circle',
                           'Circle_2']),
    s['Cable'].reversed = (False, True, True, True, False)
    s['Cable'].max_winding_angles = [0, 200, 0, 200, 0]

    # Limits

    # Watches

    # Tags

    # Colors

    # Solved state of managed DOFs nodes
    s['Load'].x = 1.706372333543476
    s['Load'].y = 0.0
    s['Load'].z = -11.330563092875934
    s['Load'].rx = 0.0
    s['Load'].ry = 39.47637504436986
    s['Load'].rz = 0.0
    s['SpacerBar'].x = 1.2956182162699852
    s['SpacerBar'].y = 0.0
    s['SpacerBar'].z = -9.627340391815187
    s['SpacerBar'].rx = 0.0
    s['SpacerBar'].ry = 43.129235679302695
    s['SpacerBar'].rz = 0.0

    s.solve_statics()

    s.update()

    assert s.verify_equilibrium()  # Make sure that we're at (an) equilibrium
