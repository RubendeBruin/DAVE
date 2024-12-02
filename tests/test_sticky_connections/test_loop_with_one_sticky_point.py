"""A loop with one sticky point (Position) is not stick because the cable is uniform.
"""

import pytest
from DAVE import *

def loop3():
    s = Scene()

    # make 5 points in the shape of a house
    p1 = s.new_point(name='p1', position=(0, 0, 0))
    p2 = s.new_point(name='p2', position=(0, 0, 5))
    p3 = s.new_point(name='p3', position=(2.5, 0, 7))

    connections = [p1, p2, p3, p1]

    c = s.new_cable(name='cable', connections=connections, length = 5, EA = 12345)

    return s, c, connections[:-1]

def test_one_sticky_is_not_sticky():
    s, c, points = loop3()

    # this is valid
    c.friction_type = [FrictionType.No, FrictionType.Pinned, FrictionType.No]

    # this is not valid
    with pytest.raises(ValueError):
        c.friction_type = [FrictionType.No, FrictionType.Pinned, FrictionType.Pinned]




