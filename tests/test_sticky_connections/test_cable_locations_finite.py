import pytest

from DAVE import *

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

    s.new_point(name='Point4',
                position=(8.319,
                          0,
                          20))


    # code for Cable
    c = s.new_cable(name='Cable',
                endA='Point1',
                endB='Point4',
                length=20,
                diameter=0.5,
                EA=12345.0,
                sheaves=['Point2','Point3'])


    c.pin_position_cable = (0.3, 0.3)

    with pytest.raises(ValueError):
        c.friction_type = FrictionType.Pinned # <-- should raise an error because the points on the cable are not > previous

    s.update()

if __name__ == '__main__':
    test_friction_ppp()
