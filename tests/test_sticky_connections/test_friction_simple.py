from imapclient.version import maintainer
from numpy.testing import assert_allclose
from DAVE import *

"""Single point/circle between two other points.
Cable is made sticky
Then one of the two end-points is moved.
Friction is then cheched against the forces at the endpoints"""


def test_friction_pcp():
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

    print(c.friction_forces)

    c.set_all_sticky()

    print(c.friction_forces)

    s['Point1'].x = 4

    s.update()
    print(c.friction_forces)

    f1 = s['Point1'].force
    f2 = s['Point3'].force

    friction = f1 - f2

    print(friction)
    print(c.friction_forces)

    assert_allclose(friction, c.friction_forces)


def test_friction_ppp():
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


    # code for Cable
    s.new_cable(name='Cable',
                endA='Point1',
                endB='Point3',
                length=20,
                diameter=0.5,
                EA=12345.0,
                sheaves=['Point2'])

    c: Cable = s['Cable']
    c.set_all_sticky()

    s['Point1'].x = 4

    s.update()

    f1 = s['Point1'].force
    f2 = s['Point3'].force
    friction = f1 - f2

    assert_allclose(friction, c.friction_forces)
    assert_allclose(friction, 231.51169218139086)
    assert abs(friction) > 1

def test_cc_loop():
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

    # code for Circle
    c = s.new_circle(name='Bottom',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Circle2
    c = s.new_circle(name='Top',
                     parent='Point2',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Loop
    loop = s.new_cable(name='Loop',
                endA='Top',
                endB='Top',
                length=16.2832,
                diameter=0.5,
                EA=12345.0,
                sheaves=['Bottom'])



    loop.sticky = [(0, 1.6), (0.5, 4.5), None]

    expected = (-915.8093337200321, 915.8093337200321)
    assert_allclose(loop.friction_forces, expected)

    # change points fixed to the circle, but same difference

    loop.sticky = [(0.25, 1.6), (0.25 + 0.5, 4.5), None]

    s.update()

    expected = (-915.8093337200321, 915.8093337200321)
    assert_allclose(loop.friction_forces, expected)

    friction = loop.friction_forces
    print(friction)

    loop.get_annotation_data()

    return s


def test_pp_loop():
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


    # code for Loop
    loop = s.new_cable(name='Loop',
                endA='Point2',
                endB='Point2',
                length=9,
                diameter=0.5,
                EA=12345.0,
                sheaves=['Point'])



    loop.sticky = [0, 0.5, None]

    expected = (0,0)
    assert_allclose(loop.friction_forces, expected)

    loop.sticky = [0, 0.6, None]

    s.update()
    print(loop.friction_forces)
    # expected = (0,0)
    # assert_allclose(loop.friction_forces, expected)
    loop.friction_forces

    # loop.sticky = [0, 0.7, None]

if __name__ == '__main__':
    s = test_cc_loop()
    DG(s, autosave=False)




