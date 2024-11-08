from numpy.testing import assert_allclose

from DAVE import *

def test_location_midpoints():

    s = Scene()

    # code for Point
    s.new_point(name='Point',
                position=(0,
                          0,
                          0))

    # code for Point2
    s.new_point(name='Point2',
                position=(2,
                          0,
                          5))

    s.new_point('P3', position=(4, 0, 3))

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
    s.new_cable(name='Loop',
                endA='Top',
                endB='Top',
                length=16.2832,
                diameter=0.5,
                EA=12345.0,
                sheaves=['P3','Bottom'])

    locations = s['Loop']._get_cable_points_at_mid_of_connections()

    print(locations)

    expected = [(2.033036843354133, 0.0, 6.249563350527373), (4.0, 0.0, 3.0), (-0.6292839600817925, 0.0, -1.0800470811884901), (2.033036843354133, 0.0, 6.249563350527373)]

    assert_allclose(locations, expected)


