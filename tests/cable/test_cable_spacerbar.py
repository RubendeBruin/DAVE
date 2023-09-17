from DAVE import *

def test_cable_spacerbar_solve():

    s = Scene()

    def solved(number):
        return number


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
                    mass=100,
                    cog=(0,
                         0,
                         -4),
                    position=(solved(0.721553),
                              solved(0),
                              solved(-18.3971)),
                    rotation=(solved(0),
                              solved(63.5907),
                              solved(0)),
                    fixed =(False, False, False, False, False, False) )

    # code for SpacerBar
    s.new_rigidbody(name='SpacerBar',
                    mass=0.1,
                    cog=(0,
                         0,
                         0),
                    position=(solved(0.561889),
                              solved(0),
                              solved(-10.2291)),
                    rotation=(solved(0),
                              solved(76.3125),
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
    s['Cable_1'].max_winding_angle = [999, 999, 999]

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
    s['Load'].x = 0.7215525549071279
    s['Load'].y = 0.0
    s['Load'].z = -18.397125628175022
    s['Load'].rx = 0.0
    s['Load'].ry = 63.590699674611045
    s['Load'].rz = 0.0
    s['SpacerBar'].x = 0.5618892855223415
    s['SpacerBar'].y = 0.0
    s['SpacerBar'].z = -10.2290822276977
    s['SpacerBar'].rx = 0.0
    s['SpacerBar'].ry = 76.31253527054116
    s['SpacerBar'].rz = 0.0

    s.solve_statics()

    assert s.verify_equilibrium()
