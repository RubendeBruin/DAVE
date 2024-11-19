from numpy.testing import assert_allclose

from DAVE import *

def mixed_model():
    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2024-11-19 08:06:40 UTC

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

    # code for pCircle
    s.new_point(name='pCircle',
                position=(0,
                          0,
                          0))

    # code for p2
    s.new_point(name='p2',
                position=(0,
                          0,
                          5))

    # code for p3
    s.new_point(name='p3',
                position=(2.5,
                          0,
                          7))

    # code for p4
    s.new_point(name='p4',
                position=(5,
                          0,
                          5))

    # code for p5
    s.new_point(name='p5',
                position=(5,
                          0,
                          0))

    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='pCircle',
                     axis=(0, 1, 0),
                     radius=1)

    # code for cable
    s.new_cable(name='cable',
                endA='p2',
                endB='p2',
                length=10,
                EA=12345,
                sheaves=['Circle',
                         'p5',
                         'p4',
                         'p3'])
    s['cable'].reversed = (False, True, False, False, False, False)
    s['cable'].max_winding_angles = [999.0, 0.0, 999.0, 999.0, 999.0, 0]

    return s

def test_p1f2_test_zero_diameter_cable_points():
    s = mixed_model()

    connections = ['p2', 'Circle', 'p5', 'p4', 'p3', 'p2']
    reversed = [False, True, False, False, False, False]
    offsets = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_winding_angles = [999.0, 0.0, 999.0, 999.0, 999.0, 0.0]
    friction_type = [FrictionType.No, FrictionType.No, FrictionType.Position, FrictionType.No, FrictionType.Force]
    friction_force_factor = [None, None, None, None, 0.5]
    friction_point_cable = [None, None, 0.0, None, None]
    friction_point_connection = [None, None, None, None, None]

    s['cable'].update_connections(connections=connections,
                                  reversed=reversed,
                                  offsets=offsets,
                                  max_winding_angles=max_winding_angles,
                                  friction_type=friction_type,
                                  friction_force_factor=friction_force_factor,
                                  friction_point_cable=friction_point_cable,
                                  friction_point_connection=friction_point_connection)

    forces = s['cable'].friction_forces
    assert_allclose(forces, (0, 0, -8333, 0, 8333), atol=1)

    midpoints = s['cable']._get_cable_points_at_mid_of_connections()

def test_2p():
    """Tests that friction forces are returned at the right indices when a segmented cable does not start at connection 0"""
    s = mixed_model()

    connections = ['p2', 'Circle', 'p5', 'p4', 'p3', 'p2']
    reversed = [False, True, False, False, False, False]
    offsets = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_winding_angles = [999.0, 0.0, 999.0, 999.0, 999.0, 0.0]
    friction_type = [FrictionType.No, FrictionType.No, FrictionType.Position, FrictionType.No, FrictionType.Position]
    friction_force_factor = [None, None, None, None, None]
    friction_point_cable = [None, None, 0.1, None, 0.4]
    friction_point_connection = [None, None, None, None, None]

    s['cable'].update_connections(connections=connections,
                                  reversed=reversed,
                                  offsets=offsets,
                                  max_winding_angles=max_winding_angles,
                                  friction_type=friction_type,
                                  friction_force_factor=friction_force_factor,
                                  friction_point_cable=friction_point_cable,
                                  friction_point_connection=friction_point_connection)

    forces = s['cable'].friction_forces

    f = 7343.414465
    assert_allclose(forces, (0, 0, f, 0, -f), atol=1)

    # DG(s)


if __name__ == '__main__':
    s = mixed_model()
    DG(s)
    # test_2p()
