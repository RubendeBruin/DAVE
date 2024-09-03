import DAVEcore as dc
from DAVE import Scene, SupportPoint


def test_basic_creation():
    s = Scene()
    sp = dc.SupportPoint()  # leaks memory, just to check it doens't crash

    sp2 = s._vfc.new_supportpoint("first")

    assert type(sp) == type(sp2)

def test_node_creation():
    s = Scene()
    sp = SupportPoint(s, "new point")




