from DAVE import *
from DAVE.nds.measurement import MeasurementDirection


def model():
    s = Scene()

    f1 = s.new_frame('f1')
    f2 = s.new_frame('f2', position = (10,10,10))

    m = Measurement(s, 'm1')
    m.point1 = f1
    m.point2 = f2

    s = s.copy()
    m = s['m1']

    return s,m

def test_total_distance():
    s,m = model()
    assert m.value == 17.320508075688775

def test_projected_distance():
    s,m = model()
    m.direction = MeasurementDirection.X
    assert m.value == 10

def test_projected_distance_negative():
    s,m = model()
    m.direction = MeasurementDirection.negative_X
    assert m.value == -10

def test_projected_distance_reference():
    s,m = model()
    m.direction = MeasurementDirection.X
    m.reference = s['f1']
    assert m.value == 10


