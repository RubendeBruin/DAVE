from DAVE import *

def test_change_connections():
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
    #
    # print(c.friction_forces)

    c.set_sticky_data_from_current_geometry()
    c.friction_type = FrictionType.Position
    #
    # s.update()
    # print(c.friction_forces)
    # assert_allclose(c.friction_forces, (0,), atol=1e-9)
    #
    # s['Point1'].x = 4
    #
    # s.update()
    # print(c.friction_forces)
    #
    # f1 = s['Point1'].force
    # f2 = s['Point3'].force
    #
    # friction = f1 - f2
    #
    # # print(friction)
    # # print(c.friction_forces)
    # #
    # # assert_allclose(friction, c.friction_forces)
    # #
    # #
    # # print(c.friction_forces)
    #
    # s['Point1'].x = 4
    #
    # s.update()
    # print(c.friction_forces)
    #
    # f1 = s['Point1'].force
    # f2 = s['Point3'].force
    #
    # friction = f2-f1
    # print(friction)

    s.new_frame(name='Frame')
    s['Point2'].change_parent_to(s['Frame'])
    s['Frame'].rotation = (0.0, -5.0, 0.0)

    # range = np.linspace(-40, 45, num = 100)
    #
    # for y in range:
    #     s['Frame'].rotation = (0.0, y, 0.0)
    #     s.update()
    #     print(s['Cable'].friction_forces)

    data = c.get_annotation_data()
    print(data)

    s['Cable'].connections = ('Point1', 'Circle', 'Point1', 'Point3')

    s['Cable'].friction = [0.0, 0.0]
    s['Cable'].friction_point_cable = [0.584, 0.6]
    s['Cable'].friction_point_connection = [38.9, None]
    s['Cable'].friction_type = [FrictionType.Position, FrictionType.Position]

    s['Cable'].connections = ('Point1', 'Circle', 'Point1')

if __name__ == '__main__':
    test_change_connections()