import pytest
from numpy.testing import assert_allclose

from DAVE import *
from DAVE.nds.measurement import MeasurementDirection


def model():
    s = Scene()

    f1 = s.new_frame('f1')
    f2 = s.new_frame('f2', position = (10,10,10))

    m = Measurement(s, 'm1')
    m.kind = MeasurementType.Angle
    m.point1 = f1
    m.point2 = f2

    s = s.copy()
    m = s['m1']

    return s,m

def test_angle_total():
    s,m = model()

    s['f2'].position = (10,0,10)

    m.direction = MeasurementDirection.X
    assert_allclose(m.value,45)

    m.direction = MeasurementDirection.Y
    assert_allclose(m.value,0)

    m.direction = MeasurementDirection.Z
    assert_allclose(m.value,45)

    m.direction = MeasurementDirection.negative_X
    assert_allclose(m.value,135)

def test_parallel():
    s, m = model()
    m.kind = MeasurementType.Angle
    m.direction = MeasurementDirection.XY

    s['f2'].position = (0,0,10)

    assert m.value == 0

if __name__ == '__main__':
    s,m = model()
    m.kind = MeasurementType.Angle
    m.direction = MeasurementDirection.XY
    m.reference = s['f1']
    DG(s)