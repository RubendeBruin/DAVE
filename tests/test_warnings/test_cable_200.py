"""Maximum winding angle exceeded"""

from DAVE import *

def test_cable_200():
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
                        10))

    # code for Point3
    s.new_point(name='Point3',
              position=(2,
                        0,
                        5))

    # code for Circle
    c = s.new_circle(name='Circle',
                parent='Point3',
                axis=(0, 1, 0),
                radius=1 )

    # code for Cable
    cable = s.new_cable(name='Cable',
                endA='Point',
                endB='Point2',
                length=10.2007,
                EA=0.0,
                sheaves = ['Circle'])


    s.update()

    cable.max_winding_angles = [999, 220.0, 999]

    s.update()

    found = False
    for w in cable.warnings:
        found = found or '200' in w

    assert found

