import numpy as np
from numpy.testing import assert_allclose

from DAVE import *

def make_wheel_model():
    s = Scene()

    wheel = s.new_frame('wheel')
    point = s.new_point('point', position = (5,0,0), parent=wheel)

    m1 = Measurement(s, 'm1')
    m1.point1 = wheel
    m1.point2 = point
    m1.kind = MeasurementType.Distance

    m2 = Measurement(s, 'm2')
    m2.point1 = wheel
    m2.point2 = point
    m2.reference = MeasurementDirection.XY
    m2.kind = MeasurementType.Angle

    return s, wheel, m1, m2

def test_angle_inv():
    s, wheel, m1, m2 = make_wheel_model()

    # m2.update_user_sign_reference(invert=True)
    m2.flip_angle_direction = True

    for a in np.linspace(-360, 800, 1000):
        wheel.ry = a
        val = m2.value

        difference = np.mod(wheel.ry - val, 360)
        if difference > 360-1e-6:
            difference -= 360

        assert_allclose(difference, 0, atol=1e-6)

def test_angle():
    s, wheel, m1, m2 = make_wheel_model()

    # m2.update_user_sign_reference(invert=True)
    m2.flip_angle_direction = False

    for a in np.linspace(-360, 800, 1000):
        wheel.ry = a
        val = -m2.value

        difference = np.mod(wheel.ry - val, 360)
        if difference > 360-1e-6:
            difference -= 360

        assert_allclose(difference, 0, atol=1e-6)


if __name__ == '__main__':
    s, wheel, m1, m2 = make_wheel_model()

    print('Distance:', m1.value)
    print('Angle:', m2.value)

    DG(s)