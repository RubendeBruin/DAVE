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
    friction_type = [FrictionType.No, FrictionType.No, FrictionType.Pinned, FrictionType.No, FrictionType.Force]
    friction_force_factor = [None, None, None, None, 0.5]
    pin_position_cable = [None, None, 0.0, None, None]
    pin_position_circle = [None, None, None, None, None]

    s['cable'].update_connections(connections=connections,
                                  reversed=reversed,
                                  offsets=offsets,
                                  max_winding_angles=max_winding_angles,
                                  friction_type=friction_type,
                                  friction_force_factor=friction_force_factor,
                                  pin_position_cable=pin_position_cable,
                                  pin_position_circle=pin_position_circle)

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
    friction_type = [FrictionType.No, FrictionType.No, FrictionType.Pinned, FrictionType.No, FrictionType.Pinned]
    friction_force_factor = [None, None, None, None, None]
    pin_position_cable = [None, None, 0.1, None, 0.4]
    pin_position_circle = [None, None, None, None, None]

    s['cable'].update_connections(connections=connections,
                                  reversed=reversed,
                                  offsets=offsets,
                                  max_winding_angles=max_winding_angles,
                                  friction_type=friction_type,
                                  friction_force_factor=friction_force_factor,
                                  pin_position_cable=pin_position_cable,
                                  pin_position_circle=pin_position_circle)

    forces = s['cable'].friction_forces

    f = 7343.414465
    assert_allclose(forces, (0, 0, f, 0, -f), atol=1)

    # DG(s)

def test_evaporated_sling():
    s  = Scene()

    # Environment settings
    s.g = 9.80665
    s.waterlevel = 0.0
    s.rho_air = 0.00126
    s.rho_water = 1.025
    s.wind_direction = 0.0
    s.wind_velocity = 0.0
    s.current_direction = 0.0
    s.current_velocity = 0.0

    # code for Point1
    s.new_point(name='Point1',
                position=(-10,
                          0,
                          0))

    # code for Point2
    s.new_point(name='Point2',
                position=(0,
                          0,
                          10))

    # code for Point3
    s.new_point(name='Point3',
                position=(10,
                          0,
                          0))

    # code for Point
    s.new_point(name='Point',
                position=(0,
                          0,
                          0))

    # code for Point2_copy_to_avoid_loop
    s.new_point(name='Point2_copy_to_avoid_loop',
                position=(0,
                          0,
                          10))

    # code for Circle1
    c = s.new_circle(name='Circle1',
                     parent='Point1',
                     axis=(0, 1, 0),
                     radius=0.1)

    # code for Circle2
    c = s.new_circle(name='Circle2',
                     parent='Point2',
                     axis=(0, 1, 0),
                     radius=0.1)

    # code for Circle3
    c = s.new_circle(name='Circle3',
                     parent='Point3',
                     axis=(0, 1, 0),
                     radius=0.1)

    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for sling_grommet/_main
    s.new_cable(name='sling_grommet/_main',
                endA='Point2',
                endB='Point2_copy_to_avoid_loop',
                length=54.6706,
                mass_per_length=0.189376,
                diameter=0.2,
                EA=2867601.7795859096,
                sheaves=['Circle1',
                         'Circle',
                         'Circle3'])
    s['sling_grommet/_main'].reversed = (False, True, False, False, False)
    # friction, first set values, then enable
    s['sling_grommet/_main'].friction_force_factor = [None, 0.5, None]
    s['sling_grommet/_main'].pin_position_cable = [0.2, None, None]
    s['sling_grommet/_main'].pin_position_circle = [0.0, None, None]
    s['sling_grommet/_main'].friction_type = [FrictionType.Pinned, FrictionType.Force, FrictionType.No]

    c : Cable = s['sling_grommet/_main']
    print(c.friction_forces)

    # s._save_coredump()

    # First friction force should be high, approximately the tension

    assert_allclose(c.friction_forces[0],-1130063,atol = 1000)

    c.get_points_and_tensions_for_visual()

    return s



if __name__ == '__main__':
    s = test_evaporated_sling()
    DG(s)
    # test_2p()
