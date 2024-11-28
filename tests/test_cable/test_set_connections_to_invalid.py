import pytest

from DAVE import *

def basemodel(radius=1.2):
    s = Scene()

    # code for Point
    s.new_point(name="Point", position=(0.0, 0.0, 5.0))
    # code for point2
    s.new_point(name="point2", position=(0.0, 0.0, -5.0))
    # code for Circle
    s.new_circle(name="Circle", parent="Point", axis=(0.0, 1.0, 0.0), radius=radius)
    # code for Circle_1
    s.new_circle(name="Circle_1", parent="point2", axis=(0.0, 1.0, 0.0), radius=radius)

    cab = s.new_cable(
        "Cable",
        endA="Circle_1",
        endB="Circle_1",
        sheaves=["Circle"],
        length=2,
        diameter=0.3,
    )
    return s, cab

def test_reversed_error():
    s, cab = basemodel()
    with pytest.raises(ValueError):
        cab.reversed = None

def test_reversed_error2():
    s, cab = basemodel()
    assert cab.reversed == (False, False, False)
    with pytest.raises(ValueError):
        cab.reversed = [None]
    assert cab.reversed == (False, False, False)


def test_reversed_error3():
    s, cab = basemodel()
    assert cab.reversed == (False, False, False)
    with pytest.raises(AssertionError):
        cab.reversed = (False, False, False,False)
    assert cab.reversed == (False, False, False)

def test_reversed_auto_expand():
    s, cab = basemodel()
    assert cab.reversed == (False, False, False)

    cab.connections = ('Circle_1', 'Circle', 'Circle_1', 'Circle')

    assert cab.reversed == (False, False, False, False)



def test_reversed_auto_expand5():
    s, cab = basemodel()
    assert cab.reversed == (False, False, False)

    cab.connections = ('Circle_1', 'Circle', 'Circle_1', 'Circle', 'Circle_1')

    assert cab.reversed == (False, False, False, False, False)

# reapeat expand for offsets
def test_offsets_auto_expand():
    s, cab = basemodel()
    assert cab.offsets == (0, 0, 0)

    cab.connections = ('Circle_1', 'Circle', 'Circle_1', 'Circle')

    assert cab.offsets == (0, 0, 0, 0)

def test_offsets_auto_expand5():
    s, cab = basemodel()
    assert cab.offsets == (0, 0, 0)

    cab.connections = ('Circle_1', 'Circle', 'Circle_1', 'Circle', 'Circle_1')

    assert cab.offsets == (0, 0, 0, 0, 0)




# repeat sames tests for offsets
def test_offsets_error():
    s, cab = basemodel()
    with pytest.raises(ValueError):
        cab.offsets = None

def test_offsets_error2():
    s, cab = basemodel()
    assert cab.offsets == (0, 0, 0)
    with pytest.raises(AssertionError):
        cab.offsets = [None]
    assert cab.offsets == (0, 0, 0)



def test_invalid():
    s = Scene()
    # code for Point
    s.new_point(name='Point',
                position=(0,
                          0,
                          0))
    s.new_point(name='Point2')
    s.new_cable("Cable", endA="Point2", endB="Point", length=1)
    try:
        s['Cable'].connections = ('Point2', 'Point', 'Point')
        s['Cable'].reversed = (False, False, False)
    except ValueError:
        pass

    s2 = s.copy() # assert that no invalid code is generated



if __name__ == '__main__':
    s = Scene()
    # code for Point
    s.new_point(name='Point',
                position=(0,
                          0,
                          0))
    s.new_point(name='Point2')
    s.new_cable("Cable", endA="Point2", endB="Point", length=1)
    gui(s)