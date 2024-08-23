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

def test_angle_total_X():
    s,m = model()

    s['f2'].position = (10,0,10)

    m.reference = MeasurementDirection.X
    assert_allclose(m.value,45)

def test_angle_total_X_flipped():
    s,m = model()

    s['f2'].position = (10,0,10)

    m.reference = MeasurementDirection.X
    m.update_positive_direction_guide(invert=True)
    assert_allclose(m.value,135)


def test_angle_total_X_downwards():
    s,m = model()

    m.reference = MeasurementDirection.X
    s['f2'].position = (10,0,-10)

    assert_allclose(m.value,45) # note: no orientation is defined for a vector, so the angle is the same

def test_angle_total_XY():
    s,m = model()

    s['f2'].position = (10,0,10)

    m.reference = MeasurementDirection.XY
    assert_allclose(m.value,45)

def test_angle_total_XY_downwards():
    s,m = model()

    m.reference = MeasurementDirection.XY
    s['f2'].position = (10,0,-10)

    assert_allclose(m.value,-45) # note: no orientation is defined for a vector, so the angle is the same



def test_angle_total_Y():
    s, m = model()

    s['f2'].position = (10, 0, 10)

    m.reference = MeasurementDirection.Y
    assert_allclose(m.value,90)

def test_angle_total_Z():
    s, m = model()

    s['f2'].position = (10, 0, 10)

    m.reference = MeasurementDirection.Z
    assert_allclose(m.value,45)


def test_parallel():
    s, m = model()
    m.kind = MeasurementType.Angle
    m.reference = MeasurementDirection.XY

    s['f2'].position = (0,0,10)

    assert m.value == 90

if __name__ == '__main__':
    s,m = model()
    m.kind = MeasurementType.Angle
    m._reference_frame = s['f1']
    m.reference = MeasurementDirection.XY
    DG(s)