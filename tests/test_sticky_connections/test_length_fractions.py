from numpy import rad2deg

from DAVE import *
from numpy.testing import assert_allclose

def test_length_fractions_on_sticky_2p_loop():

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

    s['Loop'].sticky = [(0, 1.6),(0.5, 4.5), None]
    loop.friction_point_cable = (0, 0.5)
    loop.friction_point_connection = (rad2deg(1.6), rad2deg(4.5))
    loop.friction_type = FrictionType.Position

    # DG(s)

    lengths = s['Loop']._get_partial_cable_length_fractions()

    assert_allclose(lengths, [0.5, 0.5])

    s['Loop'].sticky = [(0.2, (0, 0, 6.00001)), (0.7, (0, 0, -1.0001)), None]
    loop.friction_point_cable = (0.2, 0.7)

    lengths = s['Loop']._get_partial_cable_length_fractions()

    assert_allclose(lengths, [0.5, 0.5])

    loop.friction_point_cable = (0.2, 0.6)

    lengths = s['Loop']._get_partial_cable_length_fractions()

    assert_allclose(lengths, [0.4, 0.6])
