from DAVE import *

def test_cable_tension_data():

    s = Scene()
    p1 = s.new_point('p1', position = (0,0,0))
    p2 = s.new_point('p2', position = (10,0,0))

    c = s.new_cable('c', endA = p1, endB = p2, length = 8, EA = 12345)
    s.update()

    tension = c.tension

    end_tensions = c.segment_end_tensions
    print(end_tensions)

    positions, tensions = c._vfNode.get_drawing_data(3,8,True)

    for t in tensions:
        assert t == tension
