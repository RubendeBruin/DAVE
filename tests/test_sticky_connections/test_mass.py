import numpy as np
from numpy.testing import assert_allclose

"""This test creates core cable segments with length of 0. This test passes only of the core handles that case correctly"""

from DAVE import *

if __name__ == '__main__':
    s = Scene()
    # code for Point1
    s.new_point(name='Point1',
                position=(3.245,
                          0,
                          -11.726))

    # code for Point2
    s.new_point(name='Point2',
                position=(0,
                          0,
                          0))

    # code for Point3
    s.new_point(name='Point3',
                position=(8.319,
                          0,
                          -0.088))

    # code for Circle
    s.new_circle(name='Circle',
                 parent='Point2',
                 axis=(0, 1, 0),
                 radius=1)

    # code for Cable
    s.new_cable(name='Cable',
                endA='Point1',
                endB='Point3',
                length=20,
                diameter=0.5,
                EA=12345.0,
                sheaves=['Circle'])

    s['Cable'].max_winding_angles = [0, 181, 0]

    c: Cable = s['Cable']

    c.set_sticky_data_from_current_geometry()
    c.friction_type = FrictionType.Position

    c.mass = 0.1

    s.update()
