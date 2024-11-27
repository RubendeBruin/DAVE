from numpy.testing import assert_allclose

from DAVE import *

def model():
    s = Scene()

    # Environment settings
    s.g = 9.80665
    s.waterlevel = 0.0
    s.rho_air = 0.00126
    s.rho_water = 1.025
    s.wind_direction = 0.0
    s.wind_velocity = 0.0
    s.current_direction = 0.0
    s.current_velocity = 0.0

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

    # code for Point3
    s.new_point(name='Point3',
                position=(4.932,
                          -0.319,
                          3.867))

    # code for Bottom
    c = s.new_circle(name='Bottom',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Top
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
                sheaves=['Point3',
                         'Bottom'])
    # friction, first set values, then enable
    s['Loop'].friction_point_cable = [0.059024212918091915, 0.34484533331770295, 0.6989516860188825]
    s['Loop'].friction_point_connection = [328.61902993549796, None, 200.19826133364919]
    s['Loop'].friction_type = [FrictionType.Position, FrictionType.Position, FrictionType.Position]

    return s, s['Loop']

def test_sticky_pins_locations():
    s, c = model()
    c.diameter = 0
    p1, p2 = c.get_sticky_positions_and_directions(min_dia=0.5)

    assert_allclose(p1, [[-0.781089,  0.      ,  6.280586],
       [ 4.932   , -0.319   ,  3.867   ],
       [-0.517905,  0.      , -1.407755]], atol=1e-5)
    assert_allclose(p2, [[-1.171634,  0.      ,  6.920879],
       [ 5.653352, -0.365657,  4.066937],
       [-0.776857,  0.      , -2.111633]], atol = 1e-5)

if __name__ == '__main__':
    s, c = model()
    DG(s, autosave=False)