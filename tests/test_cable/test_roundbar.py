import math
from numpy.testing import assert_allclose

from DAVE import *

"""
A round-bar is active when its edge passes at the positive side of the cable.
The positive side is the cross-product of the cable segement direction and the bar axis.
The positive side may be reversed by setting the roundbar's 'reversed' property to True.

In test 1:
the segment direction is (1,0,0) and the bar axis is (0,1,0).
The positive side is (0,0,1).

as b is on the positive side of the cable, the bar is active.
This can be checked by looking at the cable's actual_length. That should be "much" more than 20.

Test 2 tests the same but then with the bar axis reversed (0,-1,0).

Tests 1_reversed and 2_reversed check the same, but with the reversed property set to True (in the connection).

"""
def test_roundbar_active_1():
    s = Scene()
    s.new_point(name='p1',position = (-10,0,0))
    s.new_point(name='p2',position = (10,0,0))
    s.new_point(name='b', position = (0,0,2))
    s.new_circle(name='bar',parent='b',radius=1.2,axis=(0,1,0), roundbar=True)

    c = s.new_cable(connections=['p1','bar','p2'],name='cable',EA=1e6,length=20)

    c.update()

    assert(c.actual_length>20.1)

def test_roundbar_active_1_reversed():
    s = Scene()
    s.new_point(name='p1',position = (-10,0,0))
    s.new_point(name='p2',position = (10,0,0))
    s.new_point(name='b', position = (0,0,2))
    s.new_circle(name='bar',parent='b',radius=1.2,axis=(0,1,0), roundbar=True)

    c = s.new_cable(connections=['p1','bar','p2'],name='cable',EA=1e6,length=20)
    c.reversed = [False, True, False]
    c.update()

    assert(c.actual_length<20.1)

def test_roundbar_active_2():
    s = Scene()
    s.new_point(name='p1',position = (0,-10,0))
    s.new_point(name='p2',position = (0,10,0))
    s.new_point(name='b', position = (0,0,2))
    s.new_circle(name='bar',parent='b',radius=1.2,axis=(-1,0,0), roundbar=True)

    c = s.new_cable(connections=['p1','bar','p2'],name='cable',EA=1e6,length=20)

    c.update()

    assert(c.actual_length>20.1)

def test_roundbar_active_2_reversed():
    s = Scene()
    s.new_point(name='p1', position=(0, -10, 0))
    s.new_point(name='p2', position=(0, 10, 0))
    s.new_point(name='b', position=(0, 0, 2))
    s.new_circle(name='bar', parent='b', radius=1.2, axis=(-1, 0, 0), roundbar=True)

    c = s.new_cable(connections=['p1','bar','p2'],name='cable',EA=1e6,length=20)
    c.reversed = [False, True, False]
    c.update()

    assert(c.actual_length<20.1)




def test_calc_equilibrium_and_cable_length():
    """Checks if an equilibrium can be found for this 1d system, and then
    checks if the final cable length (as drawn) is correct.

    """
    s = Scene()
    s.new_point(name='p1',
              position=(0,
                        0,
                        4))
    s.new_point(name='p2',
              position=(10,
                        2,
                        2))
    body = s.new_rigidbody(name='body',mass=1, fixed=True)
    body.fixed_z = False
    body.x = 4

    s.new_point('pbody', parent=body)
    c = s.new_circle('c1', parent='pbody', radius=1, axis=(0, 1, 0))
    c.is_roundbar = True

    c = s.new_cable(connections=['p1', 'c1', 'p2'], name='cable', EA=1e6, length=20, reversed = (False, True, False))

    s.solve_statics()

    pts, _ = c.get_points_and_tensions_for_visual()

    p = pts[0]
    L = 0
    for p2 in pts[1:]:
        L += math.sqrt((p2[0] - p[0])**2 + (p2[1] - p[1])**2 + (p2[2] - p[2])**2)
        p = p2

    assert_allclose(L, 20, rtol=1e-3)


def test_roundbar_and_circles_mixed():
    s = Scene()

    # code for Frame
    s.new_frame(name='Frame',
                position=(7,
                          -3,
                          -12))

    # code for Point1
    s.new_point(name='Point1',
                position=(0,
                          0,
                          9))

    # code for Point2
    s.new_point(name='Point2',
                position=(7.414,
                          4.583,
                          -8.943))

    s.new_point(name='OtherPoint',
                position=(0,
                          1,
                          -10))

    # code for Point
    s.new_point(name='Point',
                parent='Frame',
                position=(0,
                          0,
                          9))

    # code for Point
    s.new_point(name='PointBar',
                parent='Frame',
                position=(0,
                          0,
                          0))

    # code for Visual
    s.new_visual(name='Visual',
                 parent='Frame',
                 path=r'res: cylinder 1x1x1.obj',
                 offset=(0, 13, 0),
                 rotation=(90, 0, 0),
                 scale=(2.4, 2.4, 22))

    # code for Circle
    circle = s.new_circle(name='Circle',
                          parent='Point',
                          axis=(0, 1, 0),
                          radius=1.2)

    # code for Circle
    bar = s.new_circle(name='Bar',
                       parent='PointBar',
                       axis=(0, -1, 0),
                       radius=1.2,
                       roundbar=True)

    # code for Circle
    circle = s.new_circle(name='Circle2',
                          parent='OtherPoint',
                          axis=(0, 1, 0),
                          radius=1.2)

    # code for Cable
    c = s.new_cable(name='Cable',
                    endA='Point1',
                    endB='Point2',
                    length=20,
                    mass_per_length=0.25,
                    diameter=0.3,
                    EA=1000.0,
                    sheaves=['Circle2', 'Bar', 'Circle'])

    c.update()

    pts, _ = c.get_points_and_tensions_for_visual()

    p = pts[0]
    L = 0
    for p2 in pts[1:]:
        L += math.sqrt((p2[0] - p[0]) ** 2 + (p2[1] - p[1]) ** 2 + (p2[2] - p[2]) ** 2)
        p = p2

    assert_allclose(L, 59.829521, rtol=1e-3)

def test_compare_bar_and_circle():
    """Compares the results of a bar and a circle with the same radius"""

    s = Scene()
    s.new_point(name='p1',position = (0,-1,0))
    s.new_point(name='p2',position = (0,1,0))

    b = s.new_rigidbody(name='body',mass=1, fixed=True)
    b.fixed_z = False

    s.new_point('pbody', parent=b)
    c = s.new_circle(name='c1', parent='pbody', radius=1, axis=(1, 0,0))

    assert c.is_roundbar == False

    c.is_roundbar = True

    c = s.new_cable(connections=['p1', 'c1', 'p2'], name='cable', EA=1e6, length=20)

    s.solve_statics()

    z_bar = b.gz
    c.is_roundbar = False
    b.gz = 3 # set to a different value to enforce solving again


    s.solve_statics()

    z_circle = b.gz

    assert_allclose(z_bar, z_circle, rtol=1e-6)

def test_get_drawing_points_without_crashing():
    s = Scene()

    # code for Frame
    s.new_frame(
        name="Frame",
        position=(-0.46, 1.039, 7.825),
        rotation=(0, 0, 0),
        fixed=(True, True, True, True, True, True),
    )
    
    # code for Frame_1
    s.new_frame(
        name="Frame_1",
        position=(0, 0, 0),
        rotation=(0, 0, 0),
        fixed=(True, True, True, True, True, True),
    )
    
    # code for Point
    s.new_point(name="Point", parent="Frame", position=(0, 0, 0))
    
    # code for Point_1
    s.new_point(name="Point_1", parent="Frame_1", position=(0, -1, -4))
    
    # code for Point_2
    s.new_point(name="Point_2", parent="Frame_1", position=(2, 0, 0))
    
    # code for Circle
    s.new_circle(name="Circle", parent="Point", axis=(0, 1, 0), radius=1)
    
    # code for Circle_1
    s.new_circle(name="Circle_1", parent="Point_1", axis=(0, 1, 0), radius=1)
    
    # code for RB
    s.new_circle(name="RB", parent="Point_2", axis=(0, 1, 0), roundbar=True, radius=1)
    
    # code for sling_grommet/_grommet
    c =s.new_cable(
        name="sling_grommet/_grommet",
        endA="Circle",
        endB="Circle",
        length=20.421,
        mass_per_length=0.002038,
        diameter=0.025,
        EA=19938.641374783227,
        sheaves=["Circle_1", "RB"],
    )
    s["sling_grommet/_grommet"].max_winding_angles = [999, 999, 999, 999]

    # This model crashed in the GUI when rotating Frame_1 over ry
    rys = [0, -10, -20, -30, -40, -50, -60, -70, -80, -90, -80 , -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70 , 80, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]

    for ry in rys:
        s["Frame_1"].ry = ry
        print(ry)
        c.get_points_and_tensions_for_visual()

    assert True, "No crash"