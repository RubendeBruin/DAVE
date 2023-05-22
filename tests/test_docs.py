from DAVE import *

def test_point_parent():
    s = Scene()
    p = s.new_point('p')

    assert s.give_documentation(p,'parent')