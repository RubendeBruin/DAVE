import numpy as np
from DAVE import *

def test_rb_adjusting_mean_tensions():
    """This was an issue in the development core material length / taut length setting."""
    s = Scene()

    # code for LiftingBeam
    s.new_frame(name='LiftingBeam',
               position=(0.00539403,
                         -0.0949733,
                         29.2208),
               rotation=(8.49347,
                         -0.0687616,
                         0.0083755),
               fixed =(True, True, True, True, True, True),
                )

    # code for system2/Shackle1/pin_point
    s.new_point(name='system2/Shackle1/pin_point',
              position=(2.11346,
                        1.02405,
                        24.432))

    # code for system2/Shackle1/bow_point
    s.new_point(name='system2/Shackle1/bow_point',
              position=(2.14664,
                        0.946101,
                        25.0644))

    # code for system2/Shackle1/inside_circle_center
    s.new_point(name='system2/Shackle1/inside_circle_center',
              position=(2.13598,
                        0.971148,
                        24.8612))

    # code for system2/Shackle2/pin_point
    s.new_point(name='system2/Shackle2/pin_point',
              position=(2.12344,
                        -2.05246,
                        23.2903))

    # code for system2/Shackle2/bow_point
    s.new_point(name='system2/Shackle2/bow_point',
              position=(2.1228,
                        -1.91775,
                        23.9139))

    # code for system2/Shackle2/inside_circle_center
    s.new_point(name='system2/Shackle2/inside_circle_center',
              position=(2.123,
                        -1.96103,
                        23.7135))

    # code for LiftingBeam/WGT/EQ_main_steel
    s.new_rigidbody(name='LiftingBeam/WGT/EQ_main_steel',
                    mass=12,
                    cog=(0,
                         0,
                         0),
                    parent='LiftingBeam',
               position=(0,
                         0,
                         0),
               rotation=(0,
                         0,
                         0),
               inertia_radii = (1.0, 1.0, 1.0),
               fixed =(True, True, True, True, True, True),
                    )
    s['LiftingBeam/WGT/EQ_main_steel'].footprint = ((-6.5, 0.0, 0.0), (6.5, 0.0, 0.0), (6.5, 0.0, 0.0), (-6.5, 0.0, 0.0))

    # code for LiftingBeam/RoundBar/BottomLeft
    s.new_point(name='LiftingBeam/RoundBar/BottomLeft',
              parent='LiftingBeam',
              position=(0,
                        0.34,
                        -0.475))

    # code for LiftingBeam/RoundBar/BottomRight
    s.new_point(name='LiftingBeam/RoundBar/BottomRight',
              parent='LiftingBeam',
              position=(0,
                        -0.34,
                        -0.475))

    # code for GrommetProtector/point1
    s.new_point(name='GrommetProtector/point1',
              parent='LiftingBeam',
              position=(2.112,
                        0.34,
                        0.475))

    # code for GrommetProtector/point2
    s.new_point(name='GrommetProtector/point2',
              parent='LiftingBeam',
              position=(2.112,
                        -0.34,
                        0.475))

    # code for system2/Shackle1/bow
    c = s.new_circle(name='system2/Shackle1/bow',
                parent='system2/Shackle1/bow_point',
                axis=(0, 1, 0),
                radius=0.06 )

    # code for system2/Shackle2/bow
    c = s.new_circle(name='system2/Shackle2/bow',
                parent='system2/Shackle2/bow_point',
                axis=(0, 1, 0),
                radius=0.06 )

    # code for LiftingBeam/RoundBar/BottomLeft/BottomLeft
    c = s.new_circle(name='LiftingBeam/RoundBar/BottomLeft/BottomLeft',
                parent='LiftingBeam/RoundBar/BottomLeft',
                axis=(1, 0, 0),
                roundbar=True,
                radius=0.125 )
    c.draw_start = -6.5
    c.draw_stop = 6.5

    # code for LiftingBeam/RoundBar/BottomRight/BottomRight
    c = s.new_circle(name='LiftingBeam/RoundBar/BottomRight/BottomRight',
                parent='LiftingBeam/RoundBar/BottomRight',
                axis=(1, 0, 0),
                roundbar=True,
                radius=0.125 )
    c.draw_start = -6.5
    c.draw_stop = 6.5

    # code for GrommetProtector/GrommetProtector_circle1
    c = s.new_circle(name='GrommetProtector/GrommetProtector_circle1',
                parent='GrommetProtector/point1',
                axis=(1, 0, 0),
                radius=0.125 )

    # code for GrommetProtector/GrommetProtector_circle2
    c = s.new_circle(name='GrommetProtector/GrommetProtector_circle2',
                parent='GrommetProtector/point2',
                axis=(1, 0, 0),
                radius=0.125 )

    # code for system2/Grommet1/_grommet
    s.new_cable(name='system2/Grommet1/_grommet',
                endA='system2/Shackle1/bow',
                endB='system2/Shackle1/bow',
                length=24.3393,
                mass_per_length=0.0489008,
                diameter=0.108,
                EA=797363.3588416165,
                sheaves = ['LiftingBeam/RoundBar/BottomLeft/BottomLeft',
                           'GrommetProtector/GrommetProtector_circle1',
                           'GrommetProtector/GrommetProtector_circle2',
                           'LiftingBeam/RoundBar/BottomRight/BottomRight',
                           'system2/Shackle2/bow',
                           'LiftingBeam/RoundBar/BottomRight/BottomRight',
                           'GrommetProtector/GrommetProtector_circle2',
                           'GrommetProtector/GrommetProtector_circle1',
                           'LiftingBeam/RoundBar/BottomLeft/BottomLeft'])
    s['system2/Grommet1/_grommet'].reversed = (True, False, False, False, False, True, True, True, True, True, False)

    s.update()

    cable = s['system2/Grommet1/_grommet']

    d = np.diff(s['system2/Grommet1/_grommet'].segment_mean_tensions)
    max_step = np.max(np.abs(d))
    print(max_step)
    assert max_step < 1
