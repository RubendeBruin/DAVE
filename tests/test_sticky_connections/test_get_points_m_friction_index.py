from DAVE import *
from DAVE.visual_helpers.constants import RESOLUTION_CABLE_OVER_CIRCLE

"""
    s['cable2'].get_points_for_visual()
  File "C:\data\DAVE\public\DAVE\src\DAVE\nds\cable.py", line 913, in get_points_for_visual
    pts, _ = cableNode.get_drawing_data(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
DAVEcore.DAVECore_runtime: m_unknown_friction_index not found in active connections cable2
"""

def test_get_points_explicit_no_loop_sticky_segments():

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
    friction_type = [FrictionType.No, FrictionType.Force, FrictionType.Pinned, FrictionType.No]
    friction_force_factor = [None, 0.5, None, None]
    pin_position_cable = [None, None, 0.5, None]
    pin_position_circle = [None, None, None, None]

    s['cable2'].update_connections(connections=connections,
                                   reversed=reversed,
                                   offsets=offsets,
                                   max_winding_angles=max_winding_angles,
                                   friction_type=friction_type,
                                   friction_force_factor=friction_force_factor,
                                   pin_position_cable=pin_position_cable,
                                   pin_position_circle=pin_position_circle)

    # one position and one force
    # but not a loop
    # so correct that there is no m_unknown_friction_index

    # the error is in the first segment
    # which happens to start and end with the same point
    # so the solver must be told explicitly that this is not a loop

    c = s['cable2']

    rsag = 100

    c._vfCableNodes[0].get_drawing_data(
        rsag, RESOLUTION_CABLE_OVER_CIRCLE, False
    )

    s['cable2'].get_points_for_visual()


