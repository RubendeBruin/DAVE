"""Max sidelead exceeded"""

from DAVE import *

def test_cable_201():

    s = Scene()


    # code for Point
    s.new_point(name='Point',
              position=(2,
                        0,
                        0))

    # code for Point2
    s.new_point(name='Point2',
              position=(0,
                        6,
                        0))

    # code for Circle
    c = s.new_circle(name='Circle',
                parent='Point',
                axis=(0, 1, 0),
                radius=1 )

    # code for Cable
    cable = s.new_cable(name='Cable',
                endA='Point2',
                endB='Point2',
                length=6.08276,
                EA=0.0,
                sheaves = ['Circle'])

    s.update()

    found = False
    for w in cable.warnings:
        found = found or '201' in w

    assert found




# DG(s)