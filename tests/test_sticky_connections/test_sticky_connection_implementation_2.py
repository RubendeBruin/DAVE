import numpy as np
from numpy.testing import assert_allclose

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

    # make 5 points in the shape of a house
    p1 = s.new_point(name='p1', position=(0, 0, 0))
    p2 = s.new_point(name='p2', position=(0, 0, 5))
    p3 = s.new_point(name='p3', position=(2.5, 0, 7))
    p4 = s.new_point(name='p4', position=(5, 0, 5))
    p5 = s.new_point(name='p5', position=(5, 0, 0))

    connections = [p1, p2, p3, p4, p5, p1]

    c = s.new_cable(name='cable2', connections=connections, length=10, EA=12345)


    connections = ['p1', 'p2', 'p5', 'p1', 'p3', 'p4']
    reversed = [False, False, False, False, False, False]
    offsets = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_winding_angles = [999.0, 999.0, 999.0, 999.0, 999.0, 999.0]
    friction_type = [FrictionType.No, FrictionType.Force, FrictionType.Position, FrictionType.No]
    friction_force_factor = [None, 0.5, None, None]
    friction_point_cable = [None, None, 0.5, None]
    friction_point_connection = [None, None, None, None]

    s['cable2'].update_connections(connections=connections,
                                   reversed=reversed,
                                   offsets=offsets,
                                   max_winding_angles=max_winding_angles,
                                   friction_type=friction_type,
                                   friction_force_factor=friction_force_factor,
                                   friction_point_cable=friction_point_cable,
                                   friction_point_connection=friction_point_connection)

    s['cable2'].get_points_for_visual()

    # DG(s, autosave=False)




    #
    # s.update()
    #
    # print(c._vfCableNodes)
    #
    # points, f = c.get_points_and_tensions_for_visual()
    # points = np.array(points)
    #
    # # plot the first two coordinates for the points array using matplotlib
    # import matplotlib.pyplot as plt
    # plt.plot(points[:, 0], points[:, 2])
    # plt.show()
    # #
    # #
    # #
    # #
    # # DG(s, autosave=False)
