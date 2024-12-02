import pytest
from numpy.testing import assert_allclose

from DAVE import *

def loop5():
    s = Scene()

    # make 5 points in the shape of a house
    p1 = s.new_point(name='p1', position=(0, 0, 0))
    p2 = s.new_point(name='p2', position=(0, 0, 5))
    p3 = s.new_point(name='p3', position=(2.5, 0, 7))
    p4 = s.new_point(name='p4', position=(5, 0, 5))
    p5 = s.new_point(name='p5', position=(5, 0, 0))

    connections = [p1, p2, p3, p4, p5, p1]

    c = s.new_cable(name='cable', connections=connections, length = 10, EA = 12345)

    return s, c, connections[:5]

def test_2f():
    """Test with two forces, of which one is None"""

    s, c, points = loop5()
    c.friction_factor = [None, 0.0, 0.0, 0.0, 0.5]

    with pytest.raises(ValueError):
        c.friction_type = [FrictionType.Force, FrictionType.No, FrictionType.No, FrictionType.No,
                           FrictionType.Force]

    # print(c.friction_forces)
    #
    # assert_allclose(c.friction_forces, (-6767.464008214147, 0, 0.0, 0, 6767.464008214147), atol = 1e-6)

def test_2f_bugus_friction_def():
    """Test with two forces, of which one is None"""

    s, c, points = loop5()
    c.friction_force_factor = [None, -2.0, 3.0, None, 0.5]
    c.pin_position_cable = [0, 1,2,3,4]  # only the first point matters
    c.friction_type = [FrictionType.Pinned, FrictionType.No, FrictionType.No, FrictionType.No,
                       FrictionType.Force]

    assert_allclose(c.friction_forces, (-6767.464008214147, 0, 0.0, 0, 6767.464008214147), atol = 1e-6)

def test_1f_1p():
    """Test with one force, one position"""

    s, c, points = loop5()
    c.friction_force_factor = [None, -2.0, 3.0, None, 0.5]
    c.pin_position_cable = [0, 1,2,3,4]  # only the first point matters
    c.friction_type = [FrictionType.Pinned, FrictionType.No, FrictionType.No, FrictionType.No,
                       FrictionType.Force]

    assert_allclose(c.friction_forces, (-6767.464008214147, 0, 0.0, 0, 6767.464008214147), atol = 1e-6)

    s2 = s.copy()
    c2 = s2['cable']
    assert_allclose(c2.friction_forces, (-6767.464008214147, 0, 0.0, 0, 6767.464008214147), atol = 1e-6)




def test_2p_1f():
    """Test with one force, one position"""

    s, c, points = loop5()
    c.friction_force_factor = [None, -2.0, 3.0, None, 0.5]
    c.pin_position_cable = [0, 0.3,2,3,4]  # only the first two points matter
    c.friction_type = [FrictionType.Pinned, FrictionType.Pinned, FrictionType.No, FrictionType.No,
                       FrictionType.Force]

    s.update()

    assert c._get_core_cable_indices() == [[0, 1], [1, 2, 3, 4, 0]]
    assert len(c._vfCableNodes) == 2
    assert c._vfCableNodes[1].friction_factors == [0.0, 0.0, 0.5]
    assert c._vfCableNodes[1].Length == 7
    assert c._vfCableNodes[1].stretch > 0
    assert c._vfCableNodes[1].tension > 0

    print(c._vfCableNodes[1].friction_forces)
    assert_allclose(c._vfCableNodes[1].friction_forces, [0.0, 0.0, 8316.295530035875], atol = 1e-6)

    assert len(c.friction_forces) == 5
    print(c.friction_forces)
    assert_allclose(c.friction_forces, [-3130.270959407646, 11446.566489443281, 0.0, 3.637978807091713e-12, 8316.295530035632], atol = 1e-6)

    s2 = s.copy()
    c2 = s2['cable']
    assert_allclose(c2.friction_forces, [-3130.270959407646, 11446.566489443281, 0.0, 3.637978807091713e-12, 8316.295530035632], atol = 1e-6)

def test_invalid_setting():
    """Impossible because it defines friction at a single location on a loop"""
    s, c, points = loop5()

    c.update()

    s['cable'].friction = [None, -2.0, 3.0, None, 0.5]
    s['cable'].pin_position_cable = [0.0, 0.3, 2.0, 3.0, 4.0]
    s['cable'].pin_position_circle = [None, None, None, None, None]

    with pytest.raises(ValueError):
        s['cable'].friction_type = [FrictionType.No, FrictionType.No, FrictionType.No, FrictionType.No, FrictionType.Force]



def test_invalid_setting_detect():
    """Impossible because it defines friction at a single location on a loop"""
    s, c, points = loop5()

    c.update()

    friction_force = [None, -2.0, 3.0, None, 0.5]
    pin_position_cable = [0.0, 0.3, 2.0, 3.0, 4.0]
    pin_position_circle = [None, None, None, None, None]
    friction_type = [FrictionType.No, FrictionType.No, FrictionType.No, FrictionType.No, FrictionType.Force]

    errors = c._check_friction_vectors(friction_force_factor= friction_force,
                                       pin_position_cable= pin_position_cable,
                                       pin_position_circle= pin_position_circle,
                                       friction_type= friction_type)
    print(errors)




if __name__ == '__main__':
    s, c, points = loop5()
    test_2p_1f()
    # test_make_invalid_by_deleting_connection()
