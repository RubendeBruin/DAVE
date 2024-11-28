from imapclient.version import maintainer
from xarray.testing import assert_allclose

from DAVE import *


def model():
    s = Scene()
    point1 = s.new_point(name='Point1')
    point2 = s.new_point(name='Point2', position = (10,0,0))
    point3 = s.new_point(name='Point3', position = (20,0,0))
    point4 = s.new_point(name='Point4', position = (10,0,10))
    point5 = s.new_point(name='Point5', position = (0,0,10))

    return s, (point1, point2, point3, point4, point5)

def test_example_case_1():
    """
    Examples of the mapping for a loop

        API Definition      CoreCable1       CoreCable2

        Connection #        indeces[0]       indices[1]
        0    pointA
        1   sticky             1
        2                      2
        3                      3
        4   sticky             4                 4
        5    pointA                              5  <-- do not include, same a 0
                                                 0
                                                 1




    """

    s, points = model()
    c = s.new_cable(name='Cable',connections = [points[0], points[1], points[2], points[3], points[4], points[0]])

    c.set_zero_friction_sticky_data_from_current_geometry()

    c.friction_type = [FrictionType.No,
                       FrictionType.Position,
                       FrictionType.No,
                       FrictionType.No,
                       FrictionType.Position]

    indices = c._get_core_cable_indices()
    print(indices)

    assert indices ==  [[1,2,3,4], [4,0,1]]

def test_example_case_2():
    """
        API Definition      CoreCable1       CoreCable2

        Connection #        indeces[0]       indices[1]
        0   sticky             0
        1                      1
        2                      2
        3                      3
        4   sticky             4                 4
        5   pointA                               0

    """

    s, points = model()
    c = s.new_cable(name='Cable',connections = [points[0], points[1], points[2], points[3], points[4], points[0]])

    c.set_zero_friction_sticky_data_from_current_geometry()

    c.friction_type = [FrictionType.Position,  # 0
                       FrictionType.No,        # 1
                       FrictionType.No,        # 2
                       FrictionType.No,        # 3
                       FrictionType.Position]  # 4

    indices = c._get_core_cable_indices()
    print(indices)

    assert indices ==  [[0,1,2,3,4], [4,0]]


if __name__ == '__main__':
    test_example_case_1()
    test_example_case_2()
