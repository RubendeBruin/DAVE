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
    f = s.new_frame("Frame")
    s.new_point(name='Point2',
                parent = f,
                position=(0,
                          0,
                          0))

    # code for Point3
    s.new_point(name='Point3',
                position=(8.319,
                          0,
                          -0.088))

    # code for Circle
    c = s.new_circle(name='Circle',
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

    c : Cable = s['Cable']

    print(c.friction_forces)

    c.set_all_sticky()


    print(c.friction_forces)

    s['Point1'].x = 4

    s.update()
    print(c.friction_forces)

    f1 = s['Point1'].force
    f2 = s['Point3'].force

    friction = f2-f1
    print(friction)

    DG(s, autosave=False)
