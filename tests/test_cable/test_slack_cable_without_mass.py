import numpy as np

from DAVE import *

def test_zero_tension_for_slack_cabble_without_mass():
    s = Scene()
    p = s.new_point(name='Point1', position=(0, 0, 0))
    p2 = s.new_point(name='Point2', position=(10, 0, 5))

    c = s.new_cable(name='Cable', endA=p, endB=p2, length=30, diameter=0.5, EA=12345.0)

    pts, tensions = c.get_points_and_tensions_for_visual()

    assert np.max(tensions) < 1e-6
    assert len(tensions) > 3
