from DAVE import *

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