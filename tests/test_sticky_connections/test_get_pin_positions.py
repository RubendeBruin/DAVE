from numpy.testing import assert_allclose
from DAVE import *


def model():
    """Circle - Point - Circle ; not a loop"""
    s = Scene()

    # code for Point
    s.new_point(name='Point',
                position=(0,
                          0,
                          0))

    # code for Point2
    s.new_point(name='Point2',
                position=(0,
                          0,
                          5))

    # code for Point3
    s.new_point(name='Point3',
                position=(4.932,
                          -0.319,
                          3.867))

    # code for Bottom
    c = s.new_circle(name='Bottom',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Top
    c = s.new_circle(name='Top',
                     parent='Point2',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Cable
    s.new_cable(name='Cable',
                endA='Top',
                endB='Bottom',
                length=16.2832,
                diameter=0.5,
                EA=12345.0,
                sheaves=['Point3'])
    # friction, first set values, then enable
    s['Cable'].friction_point_cable = [0.34484533331770295]
    s['Cable'].friction_type = [FrictionType.Position]

    return s, s['Cable']

def model_loop():
    s, c = model()

    connections = ['Top', 'Point3', 'Bottom', 'Top']
    friction_type = [FrictionType.No, FrictionType.Position, FrictionType.No]
    friction_force_factor = [None, 0, None]
    friction_point_cable = [None, 0.34484533331770295, None]
    friction_point_connection = [None, None, None]

    s['Cable'].update_connections(connections=connections,
                                  friction_type=friction_type,
                                  friction_force_factor=friction_force_factor,
                                  friction_point_cable=friction_point_cable,
                                  friction_point_connection=friction_point_connection)

    return s, c



def test_get_pin_positions():
    s, c = model()
    c : Cable
    poss = c._get_cable_points_at_mid_of_connections()

    assert_allclose(poss, [(0.5721208030438902, 0.0, 6.111385525695028), (4.932, -0.319, 3.867), (0.9519720514049897, 0.0, -0.8100921017660744)])

    print(poss)
    a, b = c.get_zero_friction_sticky_data_from_current_geometry()
    assert len(a) == len(poss)
    
    c.set_zero_friction_sticky_data_from_current_geometry()

def test_model_doubled_grommet():
    s = Scene()

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

    # code for Point
    s.new_point(name='Point',
                position=(0,
                          0,
                          20))

    # code for Point2
    s.new_point(name='Point2',
                position=(5,
                          0,
                          20))

    # code for Body
    s.new_rigidbody(name='Body',
                    mass=100,
                    cog=(0,
                         0,
                         0),
                    position=(solved(2.1257472076260933),
                              solved(-5.807896144685365e-11),
                              solved(10.424743064624456)),
                    rotation=(solved(-1.25341e-09),
                              solved(1.23339),
                              solved(1.47134e-09)),
                    fixed=(False, False, False, False, False, False),
                    )


    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=0.2)

    # code for Circle3
    c = s.new_circle(name='Circle3',
                     parent='Point2',
                     axis=(0, 1, 0),
                     radius=0.3)

    # code for Point3
    s.new_point(name='Point3',
                parent='Body',
                position=(1,
                          0,
                          3))

    # code for LiftPoint
    s.new_rigidbody(name='LiftPoint',
                    mass=-0,
                    cog=(0,
                         0,
                         0),
                    parent='Body',
                    position=(-10,
                              0,
                              0),
                    rotation=(0,
                              0,
                              0),
                    fixed=(True, True, True, True, True, True),
                    )
    s['LiftPoint'].footprint = ((0.0, 0.0, 0.0), (0.5, 0.0, 0.0))

    # code for LiftPoint2
    s.new_rigidbody(name='LiftPoint2',
                    mass=-0,
                    cog=(0,
                         0,
                         0),
                    parent='Body',
                    position=(10,
                              0,
                              0),
                    rotation=(0,
                              0,
                              180),
                    fixed=(True, True, True, True, True, True),
                    )
    s['LiftPoint2'].footprint = ((0.0, 0.0, 0.0), (0.5, 0.0, 0.0))

    # code for Circle2
    c = s.new_circle(name='Circle2',
                     parent='Point3',
                     axis=(0, 1, 0),
                     radius=1)

    # code for LiftPoint/point
    s.new_point(name='LiftPoint/point',
                parent='LiftPoint',
                position=(0.5,
                          0,
                          0.3))

    # code for LiftPoint/visual
    s.new_visual(name='LiftPoint/visual',
                 parent='LiftPoint',
                 path=r'res: cube.obj',
                 offset=(0.35, 0, 0.25),
                 rotation=(0, 0, 0),
                 scale=(0.7, 0.01, 0.5))

    # code for system/GC2/_axis_on_parent
    s.new_frame(name='system/GC2/_axis_on_parent',
                parent='LiftPoint',
                position=(0.5,
                          0,
                          0.3),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for LiftPoint2/point
    s.new_point(name='LiftPoint2/point',
                parent='LiftPoint2',
                position=(0.5,
                          0,
                          0.3))

    # code for LiftPoint2/visual
    s.new_visual(name='LiftPoint2/visual',
                 parent='LiftPoint2',
                 path=r'res: cube.obj',
                 offset=(0.35, 0, 0.25),
                 rotation=(0, 0, 0),
                 scale=(0.7, 0.01, 0.5))

    # code for system/GC1/_axis_on_parent
    s.new_frame(name='system/GC1/_axis_on_parent',
                parent='LiftPoint2',
                position=(0.5,
                          0,
                          0.3),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for LiftPoint/circle
    c = s.new_circle(name='LiftPoint/circle',
                     parent='LiftPoint/point',
                     axis=(0, 1, 0),
                     radius=0.05)

    # code for system/GC2/_pin_hole_connection
    s.new_frame(name='system/GC2/_pin_hole_connection',
                parent='system/GC2/_axis_on_parent',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          solved(-53.1345),
                          0),
                fixed=(True, True, True, True, False, True),
                )

    # code for LiftPoint2/circle
    c = s.new_circle(name='LiftPoint2/circle',
                     parent='LiftPoint2/point',
                     axis=(0, 1, 0),
                     radius=0.05)

    # code for system/GC1/_pin_hole_connection
    s.new_frame(name='system/GC1/_pin_hole_connection',
                parent='system/GC1/_axis_on_parent',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          solved(-55.2685),
                          0),
                fixed=(True, True, True, True, False, True),
                )

    # code for system/GC2/_connection_axial_rotation
    s.new_frame(name='system/GC2/_connection_axial_rotation',
                parent='system/GC2/_pin_hole_connection',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for system/GC1/_connection_axial_rotation
    s.new_frame(name='system/GC1/_connection_axial_rotation',
                parent='system/GC1/_pin_hole_connection',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for system/GC2/_axis_on_child
    s.new_frame(name='system/GC2/_axis_on_child',
                parent='system/GC2/_connection_axial_rotation',
                position=(0.0025,
                          0,
                          0),
                rotation=(0,
                          90,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for system/GC1/_axis_on_child
    s.new_frame(name='system/GC1/_axis_on_child',
                parent='system/GC1/_connection_axial_rotation',
                position=(0.0025,
                          0,
                          0),
                rotation=(0,
                          90,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for system/Shackle2
    s.new_rigidbody(name='system/Shackle2',
                    mass=0.11,
                    cog=(0,
                         0,
                         0.180833),
                    parent='system/GC2/_axis_on_child',
                    position=(-0,
                              -0,
                              -0),
                    rotation=(-0,
                              -0,
                              -0),
                    inertia_radii=(0.3644461551450365, 0.2987996820614105, 0.21920823433438807),
                    fixed=(True, True, True, True, True, True),
                    )

    # code for system/Shackle1
    s.new_rigidbody(name='system/Shackle1',
                    mass=0.11,
                    cog=(0,
                         0,
                         0.180833),
                    parent='system/GC1/_axis_on_child',
                    position=(0,
                              -0,
                              -0),
                    rotation=(-0,
                              -0,
                              -0),
                    inertia_radii=(0.3644461551450365, 0.2987996820614105, 0.21920823433438807),
                    fixed=(True, True, True, True, True, True),
                    )

    # code for system/Shackle2/pin_point
    s.new_point(name='system/Shackle2/pin_point',
                parent='system/Shackle2',
                position=(0,
                          0,
                          0))

    # code for system/Shackle2/bow_point
    s.new_point(name='system/Shackle2/bow_point',
                parent='system/Shackle2',
                position=(0,
                          0,
                          0.495))

    # code for system/Shackle2/inside_circle_center
    s.new_point(name='system/Shackle2/inside_circle_center',
                parent='system/Shackle2',
                position=(0,
                          0,
                          0.3285))

    # code for system/Shackle2/visual
    s.new_visual(name='system/Shackle2/visual',
                 parent='system/Shackle2',
                 path=r'res: shackle_gp800.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(0.530547, 0.530547, 0.530547))

    # code for system/Shackle1/pin_point
    s.new_point(name='system/Shackle1/pin_point',
                parent='system/Shackle1',
                position=(0,
                          0,
                          0))

    # code for system/Shackle1/bow_point
    s.new_point(name='system/Shackle1/bow_point',
                parent='system/Shackle1',
                position=(0,
                          0,
                          0.495))

    # code for system/Shackle1/inside_circle_center
    s.new_point(name='system/Shackle1/inside_circle_center',
                parent='system/Shackle1',
                position=(0,
                          0,
                          0.3285))

    # code for system/Shackle1/visual
    s.new_visual(name='system/Shackle1/visual',
                 parent='system/Shackle1',
                 path=r'res: shackle_gp800.obj',
                 offset=(0, 0, 0),
                 rotation=(0, 0, 0),
                 scale=(0.530547, 0.530547, 0.530547))

    # code for system/Shackle2/pin
    c = s.new_circle(name='system/Shackle2/pin',
                     parent='system/Shackle2/pin_point',
                     axis=(0, 1, 0),
                     radius=0.0475)

    # code for system/Shackle2/bow
    c = s.new_circle(name='system/Shackle2/bow',
                     parent='system/Shackle2/bow_point',
                     axis=(0, 1, 0),
                     radius=0.0475)

    # code for system/Shackle2/inside
    c = s.new_circle(name='system/Shackle2/inside',
                     parent='system/Shackle2/inside_circle_center',
                     axis=(1, 0, 0),
                     radius=0.119)

    # code for system/Shackle1/pin
    c = s.new_circle(name='system/Shackle1/pin',
                     parent='system/Shackle1/pin_point',
                     axis=(0, 1, 0),
                     radius=0.0475)

    # code for system/Shackle1/bow
    c = s.new_circle(name='system/Shackle1/bow',
                     parent='system/Shackle1/bow_point',
                     axis=(0, 1, 0),
                     radius=0.0475)

    # code for system/Shackle1/inside
    c = s.new_circle(name='system/Shackle1/inside',
                     parent='system/Shackle1/inside_circle_center',
                     axis=(1, 0, 0),
                     radius=0.119)

    # code for system/Sling1/_grommet
    s.new_cable(name='system/Sling1/_grommet',
                endA='system/Shackle2/bow',
                endB='system/Shackle2/bow',
                length=80.2513,
                mass_per_length=0.0268317,
                diameter=0.08,
                EA=437510.75930952904,
                sheaves=['Circle',
                         'Circle2',
                         'Circle3',
                         'system/Shackle1/bow',
                         'Circle3',
                         'Circle2',
                         'Circle'])
    s['system/Sling1/_grommet'].reversed = (False, False, True, False, False, True, False, True, True)
    # friction, first set values, then enable
    s['system/Sling1/_grommet'].friction_force_factor = [None, None, 0.0, None, None, None, -0.0, None]
    s['system/Sling1/_grommet'].friction_point_cable = [None, None, None, None, None, None, None, None]
    s['system/Sling1/_grommet'].friction_type = [FrictionType.Position, FrictionType.No, FrictionType.Force,
                                                 FrictionType.No, FrictionType.No, FrictionType.No, FrictionType.Force,
                                                 FrictionType.No]

    cable = s['system/Sling1/_grommet']

    poss = cable._get_cable_points_at_mid_of_connections()

    assert len(poss) == len(cable.connections)
    assert poss[-1] == poss[0]






def test_model_loop_with_returns_and_point_as_start_and_end():

    s, c = model_loop()

    connections = ['Point3', 'Top', 'Bottom', 'Point3', 'Top', 'Point3']
    reversed = [False, False, False, False, False, False]
    offsets = [0, 0, 0, 0, 0, 0]
    max_winding_angles = [999, 999, 999, 999, 999, 999]
    friction_type = [FrictionType.No, FrictionType.No, FrictionType.No, FrictionType.No, FrictionType.No]
    friction_force_factor = [None, None, None, None, None]
    friction_point_cable = [None, None, None, None, None]
    friction_point_connection = [None, None, None, None, None]

    c.update_connections(connections=connections,
                                  reversed=reversed,
                                  offsets=offsets,
                                  max_winding_angles=max_winding_angles,
                                  friction_type=friction_type,
                                  friction_force_factor=friction_force_factor,
                                  friction_point_cable=friction_point_cable,
                                  friction_point_connection=friction_point_connection)

    c: Cable
    poss = c._get_cable_points_at_mid_of_connections()
    a, b = c.get_zero_friction_sticky_data_from_current_geometry()
    assert len(a) == len(poss)


def test_model_with_roundbar():
    s = Scene()

    # code for Point
    s.new_point(name='Point',
                position=(0,
                          0,
                          0))

    # code for Point2
    s.new_point(name='Point2',
                position=(0,
                          0,
                          5))

    # code for Point3
    s.new_point(name='Point3',
                position=(4.932,
                          -0.319,
                          3.867))

    # code for Bottom
    c = s.new_circle(name='Bottom',
                     parent='Point',
                     axis=(0, 1, 0),
                     roundbar=True,
                     radius=1)

    # code for Top
    c = s.new_circle(name='Top',
                     parent='Point2',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Cable
    s.new_cable(name='Cable',
                endA='Top',
                endB='Top',
                length=15,
                diameter=0.5,
                EA=12345.0,
                sheaves=['Bottom',
                         'Point3'])
    s['Cable'].reversed = (True, True, False, False)
    # friction, first set values, then enable
    s['Cable'].friction_force_factor = [None, 0.0, None]
    s['Cable'].friction_point_cable = [None, None, None]
    s['Cable'].friction_type = [FrictionType.No, FrictionType.Force, FrictionType.Position]

    cable : Cable = s['Cable']
    cable.get_zero_friction_sticky_data_from_current_geometry()

    DG(s)

if __name__ == '__main__':
    test_model_with_roundbar()