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
    m.reference = MeasurementDirection.X
    assert m.value == 10

def test_projected_distance_flip():
    s,m = model()
    m.reference = MeasurementDirection.X
    m.update_positive_direction_guide(invert=True)
    assert m.value == -10

def test_projected_distance_negative():
    s,m = model()
    m.reference = MeasurementDirection.X # this sets the positive direction
    s['f2'].x = -10
    assert m.value == -10

def test_projected_distance_negative_reset():
    s,m = model()
    m.reference = MeasurementDirection.X # this sets the positive direction
    s['f2'].x = -10
    m.update_positive_direction_guide(invert=False)
    assert m.value == 10

def test_projected_distance_reference():
    s,m = model()
    m.reference = MeasurementDirection.X
    m._reference_frame = s['f1']
    assert m.value == 10


