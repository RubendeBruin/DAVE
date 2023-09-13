from numpy.testing import assert_allclose

from DAVE import *

"""
Test corresponds to 

Worked example: Friction on a doubled grommet
==============================================

"""

def test_friction_on_double_grommet_documentation():
    s = Scene()
    s.new_point("upper1", position=(-1, 0, 10))
    s.new_point("upper2", position=(1, 0, 10))

    b = s.new_rigidbody("load", mass = 100/s.g, cog = (0,0,-1), rotation=(0,0,-90))
    b.fixed_z = False
    s.new_point("lower1", position=(-1, 0, 0), parent = b)
    s.new_point("lower2", position=(1, 0, 0), parent = b)

    for p in s.nodes_of_type(Point):
        s.new_circle(f"c_{p.name}", parent=p, radius=1, axis=(1, 0, 0))

    # code for Cable
    grommet = s.new_cable(name='Cable',
                connections=['c_upper1',
                             'c_lower1',
                             'c_upper2',
                             'c_lower2',
                             'c_upper1',
                             ],
                length=40,
                EA=3000.0,
                )
    grommet.reversed = (True, False, False, True, False)

    grommet = s['Cable'] # alias
    s['Cable'].friction = [-0.1, 0.1, 0.1, None]

    s.solve_statics()
    print(4*grommet.tension)


    print(s['Cable'].friction)

    tensions = grommet.segment_mean_tensions
    print(tensions)

    import numpy as np
    print(np.sum(tensions))

    highest_tension = max(tensions)
    print(highest_tension)

    print(grommet.tension)

    assert_allclose(grommet.tension, 30.25, atol = 0.001)

