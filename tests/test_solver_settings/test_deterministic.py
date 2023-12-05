from DAVE import *

"""
This is a model with chaotic solving process. It is used to test the determinism of the solver.
"""

def model():
    s = Scene()
    # auto generated python code
    # By MS12H
    # Time: 2023-12-05 15:37:05 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution

    def solved(number):
        return number

    # code for LB
    s.new_frame(name='LB',
               position=(solved(31.17377034726446),
                         solved(0.3781409260575409),
                         solved(-4.11047247536619)),
               rotation=(solved(2.25716),
                         solved(-1.99028),
                         solved(89.9798)),
               fixed =(False, False, False, False, False, False),
                )

    # code for Block-900ton
    s.new_frame(name='Block-900ton',
               fixed =(False, False, False, False, False, False),
                )

    # code for Point
    s.new_point(name='Point',
              position=(31.1749,
                        -0.49,
                        23.8556))

    # code for Point2
    s.new_point(name='Point2',
              position=(31.1749,
                        0.49,
                        23.8556))

    # code for Point3
    s.new_point(name='Point3',
              position=(30.4969,
                        0,
                        24.03))

    # code for remain1
    s.new_point(name='remain1',
              position=(31.1749,
                        0,
                        23.8556))

    # code for _spliceA1
    s.new_rigidbody(name='_spliceA1',
                    mass=0.0923295,
                    cog=(0,
                         0,
                         0),
               position=(solved(32.00779559164631),
                         solved(5.12446371054534),
                         solved(-3.572572134044817)),
               rotation=(0,
                         0,
                         0),
               fixed =(False, False, False, True, True, True),
                    )

    # code for _spliceA2
    s.new_rigidbody(name='_spliceA2',
                    mass=0.0923295,
                    cog=(0,
                         0,
                         0),
               position=(solved(31.95636560049846),
                         solved(4.74280670590451),
                         solved(-2.987599171943672)),
               rotation=(0,
                         0,
                         0),
               fixed =(False, False, False, True, True, True),
                    )

    # code for _spliceB1
    s.new_rigidbody(name='_spliceB1',
                    mass=0.0923295,
                    cog=(0,
                         0,
                         0),
               position=(solved(30.34015496835495),
                         solved(5.124183557192731),
                         solved(-3.567551404372347)),
               rotation=(0,
                         0,
                         180),
               fixed =(False, False, False, True, True, True),
                    )

    # code for _spliceB2
    s.new_rigidbody(name='_spliceB2',
                    mass=0.0923295,
                    cog=(0,
                         0,
                         0),
               position=(solved(30.39304462193616),
                         solved(4.742360070049417),
                         solved(-2.982817285303805)),
               rotation=(0,
                         0,
                         180),
               fixed =(False, False, False, True, True, True),
                    )

    # code for EQ_main_steel
    s.new_rigidbody(name='EQ_main_steel',
                    mass=42.7,
                    cog=(-0.419,
                         0,
                         0),
                    parent='LB',
               position=(0,
                         0,
                         0),
               rotation=(0,
                         0,
                         0),
               inertia_radii = (1.0, 1.0, 1.0),
               fixed =(True, True, True, True, True, True),
                    )
    s['EQ_main_steel'].footprint = ((-6.7, 0.0, 0.0), (6.9, 0.0, 0.0), (6.9, 0.0, 0.0), (-6.7, 0.0, 0.0))

    # code for BottomLeft
    s.new_point(name='BottomLeft',
              parent='LB',
              position=(0,
                        0.68,
                        -1.48))

    # code for BottomRight
    s.new_point(name='BottomRight',
              parent='LB',
              position=(0,
                        -0.68,
                        -1.48))

    # code for TopLeft
    s.new_point(name='TopLeft',
              parent='LB',
              position=(0,
                        0.68,
                        1.48))

    # code for TopRight
    s.new_point(name='TopRight',
              parent='LB',
              position=(0,
                        -0.68,
                        1.48))

    # code for A Lower 1_frame
    s.new_rigidbody(name='A Lower 1_frame',
                    mass=2.3,
                    cog=(0,
                         0,
                         0),
                    parent='LB',
               position=(-5.25,
                         0,
                         -0.5),
               rotation=(0,
                         0,
                         0),
               fixed =(True, True, True, True, True, True),
                    )

    # code for A Lower 6_frame
    s.new_rigidbody(name='A Lower 6_frame',
                    mass=2.3,
                    cog=(0,
                         0,
                         0),
                    parent='LB',
               position=(5.25,
                         0,
                         -0.5),
               rotation=(0,
                         0,
                         0),
               fixed =(True, True, True, True, True, True),
                    )

    # code for A Lower 1_point_left
    s.new_point(name='A Lower 1_point_left',
              parent='LB',
              position=(-5.25,
                        0.8975,
                        -0.5))

    # code for A Lower 1_point_right
    s.new_point(name='A Lower 1_point_right',
              parent='LB',
              position=(-5.25,
                        -0.8975,
                        -0.5))

    # code for A Lower 6_point_left
    s.new_point(name='A Lower 6_point_left',
              parent='LB',
              position=(5.25,
                        0.8975,
                        -0.5))

    # code for A Lower 6_point_right
    s.new_point(name='A Lower 6_point_right',
              parent='LB',
              position=(5.25,
                        -0.8975,
                        -0.5))

    # code for wt
    s.new_rigidbody(name='wt',
                    mass=36.4,
                    cog=(0,
                         0,
                         0),
                    parent='Block-900ton',
               position=(0,
                         0,
                         0),
               rotation=(0,
                         0,
                         0),
               fixed =(True, True, True, True, True, True),
                    )

    # code for sr
    s.new_point(name='sr',
              parent='Block-900ton',
              position=(0.492,
                        0,
                        1.29))

    # code for sl
    s.new_point(name='sl',
              parent='Block-900ton',
              position=(-0.492,
                        0,
                        1.29))

    # code for hinge_joint
    s.new_frame(name='hinge_joint',
               parent='Block-900ton',
               position=(0,
                         0,
                         0),
               rotation=(solved(0.0116648),
                         0,
                         0),
               fixed =(True, True, True, False, True, True),
                )

    # code for Crane-tip-left-circle
    c = s.new_circle(name='Crane-tip-left-circle',
                parent='Point',
                axis=(0, 1, 0),
                radius=0.49 )

    # code for Crane-tip-right-circle
    c = s.new_circle(name='Crane-tip-right-circle',
                parent='Point2',
                axis=(0, 1, 0),
                radius=0.49 )

    # code for _spliceA1p
    s.new_point(name='_spliceA1p',
              parent='_spliceA1',
              position=(0,
                        0,
                        0))

    # code for _spliceA2p
    s.new_point(name='_spliceA2p',
              parent='_spliceA2',
              position=(0,
                        0,
                        0))

    # code for _spliceB1p
    s.new_point(name='_spliceB1p',
              parent='_spliceB1',
              position=(0,
                        0,
                        0))

    # code for _spliceB2p
    s.new_point(name='_spliceB2p',
              parent='_spliceB2',
              position=(0,
                        0,
                        0))

    # code for _spliceA
    s.new_cable(name='_spliceA',
                endA='_spliceA1p',
                endB='_spliceA2p',
                length=0.7,
                diameter=0.12,
                EA=246100)

    # code for _spliceB
    s.new_cable(name='_spliceB',
                endA='_spliceB1p',
                endB='_spliceB2p',
                length=0.7,
                diameter=0.12,
                EA=246100)

    # code for LBM
    c = s.new_circle(name='LBM',
                parent='BottomLeft',
                axis=(1, 0, 0),
                roundbar=True,
                radius=0.02 )
    c.draw_start = -6.7
    c.draw_stop = 6.7

    # code for LBR
    c = s.new_circle(name='LBR',
                parent='BottomRight',
                axis=(1, 0, 0),
                roundbar=True,
                radius=0.02 )
    c.draw_start = -6.7
    c.draw_stop = 6.7

    # code for LBTL
    c = s.new_circle(name='LBTL',
                parent='TopLeft',
                axis=(1, 0, 0),
                roundbar=True,
                radius=0.02 )
    c.draw_start = -6.7
    c.draw_stop = 6.7

    # code for LBTR
    c = s.new_circle(name='LBTR',
                parent='TopRight',
                axis=(1, 0, 0),
                roundbar=True,
                radius=0.02 )
    c.draw_start = -6.7
    c.draw_stop = 6.7

    # code for A Lower 1_Left
    c = s.new_circle(name='A Lower 1_Left',
                parent='A Lower 1_point_left',
                axis=(0, 1, 0),
                radius=0.2795 )

    # code for A Lower 1_Right
    c = s.new_circle(name='A Lower 1_Right',
                parent='A Lower 1_point_right',
                axis=(0, -1, 0),
                radius=0.2795 )

    # code for A Lower 6_Left
    c = s.new_circle(name='A Lower 6_Left',
                parent='A Lower 6_point_left',
                axis=(0, 1, 0),
                radius=0.2795 )

    # code for A Lower 6_Right
    c = s.new_circle(name='A Lower 6_Right',
                parent='A Lower 6_point_right',
                axis=(0, -1, 0),
                radius=0.2795 )

    # code for HT-sheaves-right-circle
    c = s.new_circle(name='HT-sheaves-right-circle',
                parent='sr',
                axis=(1, 0, 0),
                radius=0.64 )

    # code for HT-sheaves-left-circle
    c = s.new_circle(name='HT-sheaves-left-circle',
                parent='sl',
                axis=(1, 0, 0),
                radius=0.64 )

    # code for Hook-eye
    s.new_point(name='Hook-eye',
              parent='hinge_joint',
              position=(0,
                        4.23516e-22,
                        -1.737))

    # code for HT-horn-right-hinge
    s.new_frame(name='HT-horn-right-hinge',
               parent='hinge_joint',
               position=(0.413,
                         1.30414e-16,
                         -1.29),
               rotation=(0,
                         solved(-28.2804),
                         0),
               fixed =(True, True, True, True, False, True),
                )

    # code for HT-horn-left-hinge
    s.new_frame(name='HT-horn-left-hinge',
               parent='hinge_joint',
               position=(-0.413,
                         -1.50239e-16,
                         -1.29),
               rotation=(0,
                         solved(32.2513),
                         0),
               fixed =(True, True, True, True, False, True),
                )

    # code for _eyeA
    s.new_cable(name='_eyeA',
                endA='_spliceA1p',
                endB='_spliceA1p',
                length=2.97487,
                diameter=0.06,
                EA=246099.80211161007,
                sheaves = ['A Lower 6_Right'])

    # code for _eyeB
    s.new_cable(name='_eyeB',
                endA='_spliceB1p',
                endB='_spliceB1p',
                length=2.97487,
                diameter=0.06,
                EA=246099.80211161007,
                sheaves = ['A Lower 6_Left'])

    # code for crane-wire
    s.new_cable(name='crane-wire',
                endA='Crane-tip-left-circle',
                endB='Crane-tip-right-circle',
                length=78,
                diameter=0.05,
                EA=526216.0,
                sheaves = ['HT-sheaves-right-circle',
                           'Crane-tip-left-circle',
                           'Point3',
                           'Crane-tip-right-circle',
                           'HT-sheaves-left-circle'])
    s['crane-wire'].reversed = (True, False, True, False, False, True, False)
    s['crane-wire'].max_winding_angles = [999, 999, 360.0, 999, 999, 999, 999]

    # code for Hook-eye-circle
    c = s.new_circle(name='Hook-eye-circle',
                parent='Hook-eye',
                axis=(0, 1, 0),
                radius=0.128 )

    # code for HT-horn-right
    s.new_point(name='HT-horn-right',
              parent='HT-horn-right-hinge',
              position=(0,
                        0,
                        -0.412))

    # code for HT-horn-left
    s.new_point(name='HT-horn-left',
              parent='HT-horn-left-hinge',
              position=(0,
                        0,
                        -0.412))

    # code for HT-horn-right-circle
    c = s.new_circle(name='HT-horn-right-circle',
                parent='HT-horn-right',
                axis=(1, 0, 0),
                radius=0.187 )

    # code for HT-horn-left-circle
    c = s.new_circle(name='HT-horn-left-circle',
                parent='HT-horn-left',
                axis=(1, 0, 0),
                radius=0.187 )

    # code for _main_part
    s.new_cable(name='_main_part',
                endA='_spliceA2p',
                endB='_spliceB2p',
                length=15.72,
                diameter=0.06,
                EA=246099.80211161007,
                sheaves = ['LBTR',
                           'HT-horn-left-circle',
                           'LBTL'])
    s['_main_part'].reversed = (False, True, False, True, False)

    # code for _grommet
    s.new_cable(name='_grommet',
                endA='A Lower 1_Left',
                endB='A Lower 1_Left',
                length=40.1885,
                mass_per_length=0.0150928,
                diameter=0.06,
                EA=246099.80211161007,
                sheaves = ['LBTL',
                           'HT-horn-right-circle',
                           'LBTR',
                           'A Lower 1_Right',
                           'LBTR',
                           'HT-horn-right-circle',
                           'LBTL'])
    s['_grommet'].reversed = (False, False, True, False, False, True, False, True, True)

    return s

def model_linear_eq():
    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2023-12-05 16:25:12 UTC

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

    # code for LB
    s.new_frame(name='LB',
                position=(solved(31.198512919790726),
                          solved(0.27761980590534424),
                          solved(-3.643112233596083)),
                rotation=(solved(2.25716),
                          solved(-1.99028),
                          solved(89.9798)),
                fixed=(False, False, False, False, False, False),
                )

    # code for Block-900ton
    s.new_frame(name='Block-900ton',
                position=(solved(31.174899999999955),
                          solved(1.3845342134233518e-12),
                          solved(4.967236458021962)),
                rotation=(solved(0),
                          solved(0),
                          solved(0)),
                fixed=(False, False, False, False, False, False),
                )

    # code for Point
    s.new_point(name='Point',
                position=(31.1749,
                          -0.49,
                          23.8556))

    # code for Point2
    s.new_point(name='Point2',
                position=(31.1749,
                          0.49,
                          23.8556))

    # code for Point3
    s.new_point(name='Point3',
                position=(30.4969,
                          0,
                          24.03))

    # code for remain1
    s.new_point(name='remain1',
                position=(31.1749,
                          0,
                          23.8556))

    # code for _spliceA1
    s.new_rigidbody(name='_spliceA1',
                    mass=0.0923295,
                    cog=(0,
                         0,
                         0),
                    position=(solved(32.03452165718621),
                              solved(4.985301593164861),
                              solved(-3.1318128814357045)),
                    rotation=(0,
                              0,
                              0),
                    fixed=(False, False, False, True, True, True),
                    )

    # code for _spliceA2
    s.new_rigidbody(name='_spliceA2',
                    mass=0.0923295,
                    cog=(0,
                         0,
                         0),
                    position=(solved(31.984691108473193),
                              solved(4.575077780781426),
                              solved(-2.5663242638736405)),
                    rotation=(0,
                              0,
                              0),
                    fixed=(False, False, False, True, True, True),
                    )

    # code for _spliceB1
    s.new_rigidbody(name='_spliceB1',
                    mass=0.0923295,
                    cog=(0,
                         0,
                         0),
                    position=(solved(30.315808759443232),
                              solved(4.9444132249269535),
                              solved(-3.155461857107005)),
                    rotation=(0,
                              0,
                              180),
                    fixed=(False, False, False, True, True, True),
                    )

    # code for _spliceB2
    s.new_rigidbody(name='_spliceB2',
                    mass=0.0923295,
                    cog=(0,
                         0,
                         0),
                    position=(solved(30.328510415172772),
                              solved(4.504079076079752),
                              solved(-2.6109541443707864)),
                    rotation=(0,
                              0,
                              180),
                    fixed=(False, False, False, True, True, True),
                    )

    # code for EQ_main_steel
    s.new_rigidbody(name='EQ_main_steel',
                    mass=42.7,
                    cog=(-0.419,
                         0,
                         0),
                    parent='LB',
                    position=(0,
                              0,
                              0),
                    rotation=(0,
                              0,
                              0),
                    inertia_radii=(1.0, 1.0, 1.0),
                    fixed=(True, True, True, True, True, True),
                    )
    s['EQ_main_steel'].footprint = ((-6.7, 0.0, 0.0), (6.9, 0.0, 0.0), (6.9, 0.0, 0.0), (-6.7, 0.0, 0.0))

    # code for BottomLeft
    s.new_point(name='BottomLeft',
                parent='LB',
                position=(0,
                          0.68,
                          -1.48))

    # code for BottomRight
    s.new_point(name='BottomRight',
                parent='LB',
                position=(0,
                          -0.68,
                          -1.48))

    # code for TopLeft
    s.new_point(name='TopLeft',
                parent='LB',
                position=(0,
                          0.68,
                          1.48))

    # code for TopRight
    s.new_point(name='TopRight',
                parent='LB',
                position=(0,
                          -0.68,
                          1.48))

    # code for A Lower 1_frame
    s.new_rigidbody(name='A Lower 1_frame',
                    mass=2.3,
                    cog=(0,
                         0,
                         0),
                    parent='LB',
                    position=(-5.25,
                              0,
                              -0.5),
                    rotation=(0,
                              0,
                              0),
                    fixed=(True, True, True, True, True, True),
                    )

    # code for A Lower 6_frame
    s.new_rigidbody(name='A Lower 6_frame',
                    mass=2.3,
                    cog=(0,
                         0,
                         0),
                    parent='LB',
                    position=(5.25,
                              0,
                              -0.5),
                    rotation=(0,
                              0,
                              0),
                    fixed=(True, True, True, True, True, True),
                    )

    # code for A Lower 1_point_left
    s.new_point(name='A Lower 1_point_left',
                parent='LB',
                position=(-5.25,
                          0.8975,
                          -0.5))

    # code for A Lower 1_point_right
    s.new_point(name='A Lower 1_point_right',
                parent='LB',
                position=(-5.25,
                          -0.8975,
                          -0.5))

    # code for A Lower 6_point_left
    s.new_point(name='A Lower 6_point_left',
                parent='LB',
                position=(5.25,
                          0.8975,
                          -0.5))

    # code for A Lower 6_point_right
    s.new_point(name='A Lower 6_point_right',
                parent='LB',
                position=(5.25,
                          -0.8975,
                          -0.5))

    # code for wt
    s.new_rigidbody(name='wt',
                    mass=36.4,
                    cog=(0,
                         0,
                         0),
                    parent='Block-900ton',
                    position=(0,
                              0,
                              0),
                    rotation=(0,
                              0,
                              0),
                    fixed=(True, True, True, True, True, True),
                    )

    # code for sr
    s.new_point(name='sr',
                parent='Block-900ton',
                position=(0.492,
                          0,
                          1.29))

    # code for sl
    s.new_point(name='sl',
                parent='Block-900ton',
                position=(-0.492,
                          0,
                          1.29))

    # code for hinge_joint
    s.new_frame(name='hinge_joint',
                parent='Block-900ton',
                position=(0,
                          0,
                          0),
                rotation=(solved(0.0116648),
                          0,
                          0),
                fixed=(True, True, True, False, True, True),
                )

    # code for Crane-tip-left-circle
    c = s.new_circle(name='Crane-tip-left-circle',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=0.49)

    # code for Crane-tip-right-circle
    c = s.new_circle(name='Crane-tip-right-circle',
                     parent='Point2',
                     axis=(0, 1, 0),
                     radius=0.49)

    # code for _spliceA1p
    s.new_point(name='_spliceA1p',
                parent='_spliceA1',
                position=(0,
                          0,
                          0))

    # code for _spliceA2p
    s.new_point(name='_spliceA2p',
                parent='_spliceA2',
                position=(0,
                          0,
                          0))

    # code for _spliceB1p
    s.new_point(name='_spliceB1p',
                parent='_spliceB1',
                position=(0,
                          0,
                          0))

    # code for _spliceB2p
    s.new_point(name='_spliceB2p',
                parent='_spliceB2',
                position=(0,
                          0,
                          0))

    # code for _spliceA
    s.new_cable(name='_spliceA',
                endA='_spliceA1p',
                endB='_spliceA2p',
                length=0.7,
                diameter=0.12,
                EA=246100)

    # code for _spliceB
    s.new_cable(name='_spliceB',
                endA='_spliceB1p',
                endB='_spliceB2p',
                length=0.7,
                diameter=0.12,
                EA=246100)

    # code for LBM
    c = s.new_circle(name='LBM',
                     parent='BottomLeft',
                     axis=(1, 0, 0),
                     roundbar=True,
                     radius=0.02)
    c.draw_start = -6.7
    c.draw_stop = 6.7

    # code for LBR
    c = s.new_circle(name='LBR',
                     parent='BottomRight',
                     axis=(1, 0, 0),
                     roundbar=True,
                     radius=0.02)
    c.draw_start = -6.7
    c.draw_stop = 6.7

    # code for LBTL
    c = s.new_circle(name='LBTL',
                     parent='TopLeft',
                     axis=(1, 0, 0),
                     roundbar=True,
                     radius=0.02)
    c.draw_start = -6.7
    c.draw_stop = 6.7

    # code for LBTR
    c = s.new_circle(name='LBTR',
                     parent='TopRight',
                     axis=(1, 0, 0),
                     roundbar=True,
                     radius=0.02)
    c.draw_start = -6.7
    c.draw_stop = 6.7

    # code for A Lower 1_Left
    c = s.new_circle(name='A Lower 1_Left',
                     parent='A Lower 1_point_left',
                     axis=(0, 1, 0),
                     radius=0.2795)

    # code for A Lower 1_Right
    c = s.new_circle(name='A Lower 1_Right',
                     parent='A Lower 1_point_right',
                     axis=(0, -1, 0),
                     radius=0.2795)

    # code for A Lower 6_Left
    c = s.new_circle(name='A Lower 6_Left',
                     parent='A Lower 6_point_left',
                     axis=(0, 1, 0),
                     radius=0.2795)

    # code for A Lower 6_Right
    c = s.new_circle(name='A Lower 6_Right',
                     parent='A Lower 6_point_right',
                     axis=(0, -1, 0),
                     radius=0.2795)

    # code for HT-sheaves-right-circle
    c = s.new_circle(name='HT-sheaves-right-circle',
                     parent='sr',
                     axis=(1, 0, 0),
                     radius=0.64)

    # code for HT-sheaves-left-circle
    c = s.new_circle(name='HT-sheaves-left-circle',
                     parent='sl',
                     axis=(1, 0, 0),
                     radius=0.64)

    # code for Hook-eye
    s.new_point(name='Hook-eye',
                parent='hinge_joint',
                position=(0,
                          4.23516e-22,
                          -1.737))

    # code for HT-horn-right-hinge
    s.new_frame(name='HT-horn-right-hinge',
                parent='hinge_joint',
                position=(0.413,
                          1.30414e-16,
                          -1.29),
                rotation=(0,
                          solved(-28.2804),
                          0),
                fixed=(True, True, True, True, False, True),
                )

    # code for HT-horn-left-hinge
    s.new_frame(name='HT-horn-left-hinge',
                parent='hinge_joint',
                position=(-0.413,
                          -1.50239e-16,
                          -1.29),
                rotation=(0,
                          solved(32.2513),
                          0),
                fixed=(True, True, True, True, False, True),
                )

    # code for _eyeA
    s.new_cable(name='_eyeA',
                endA='_spliceA1p',
                endB='_spliceA1p',
                length=2.97487,
                diameter=0.06,
                EA=246099.80211161007,
                sheaves=['A Lower 6_Right'])

    # code for _eyeB
    s.new_cable(name='_eyeB',
                endA='_spliceB1p',
                endB='_spliceB1p',
                length=2.97487,
                diameter=0.06,
                EA=246099.80211161007,
                sheaves=['A Lower 6_Left'])

    # code for crane-wire
    s.new_cable(name='crane-wire',
                endA='Crane-tip-left-circle',
                endB='Crane-tip-right-circle',
                length=78,
                diameter=0.05,
                EA=526216.0,
                sheaves=['HT-sheaves-right-circle',
                         'Crane-tip-left-circle',
                         'Point3',
                         'Crane-tip-right-circle',
                         'HT-sheaves-left-circle'])
    s['crane-wire'].reversed = (True, False, True, False, False, True, False)
    s['crane-wire'].max_winding_angles = [999, 999, 360.0, 999, 999, 999, 999]

    # code for Hook-eye-circle
    c = s.new_circle(name='Hook-eye-circle',
                     parent='Hook-eye',
                     axis=(0, 1, 0),
                     radius=0.128)

    # code for HT-horn-right
    s.new_point(name='HT-horn-right',
                parent='HT-horn-right-hinge',
                position=(0,
                          0,
                          -0.412))

    # code for HT-horn-left
    s.new_point(name='HT-horn-left',
                parent='HT-horn-left-hinge',
                position=(0,
                          0,
                          -0.412))

    # code for HT-horn-right-circle
    c = s.new_circle(name='HT-horn-right-circle',
                     parent='HT-horn-right',
                     axis=(1, 0, 0),
                     radius=0.187)

    # code for HT-horn-left-circle
    c = s.new_circle(name='HT-horn-left-circle',
                     parent='HT-horn-left',
                     axis=(1, 0, 0),
                     radius=0.187)

    # code for _main_part
    s.new_cable(name='_main_part',
                endA='_spliceA2p',
                endB='_spliceB2p',
                length=15.72,
                diameter=0.06,
                EA=246099.80211161007,
                sheaves=['LBTR',
                         'HT-horn-left-circle',
                         'LBTL'])
    s['_main_part'].reversed = (False, True, False, True, False)

    # code for _grommet
    s.new_cable(name='_grommet',
                endA='A Lower 1_Left',
                endB='A Lower 1_Left',
                length=40.1885,
                mass_per_length=0.0150928,
                diameter=0.06,
                EA=246099.80211161007,
                sheaves=['LBTL',
                         'HT-horn-right-circle',
                         'LBTR',
                         'A Lower 1_Right',
                         'LBTR',
                         'HT-horn-right-circle',
                         'LBTL'])
    s['_grommet'].reversed = (False, False, True, False, False, True, False, True, True)

    return s


if __name__ == '__main__':

    s = model_linear_eq()

    s.solver_settings.tolerance_during_linear_phase = 1
    s.solver_settings.do_linear_first = True

    s.solver_settings.do_local_descent = True
    s.solver_settings.do_newton = True
    s.solver_settings.do_global_descent = True
    s.solver_settings.do_deterministic = False

    s.solver_settings.deterministic_global_steps = 250
    s.solver_settings.deterministic_local_steps = 50
    s.solver_settings.max_newton_iterations = 20

    DG(s, bare=True)
    # s.solve_statics()

