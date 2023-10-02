from numpy.testing import assert_allclose

from DAVE import *

"""
A round-bar becomes in-active if it collides with one of the segment ends on either side
"""
def test_roundbar_active():
    s = Scene()
    s.new_point(name='p1',position = (-10,0,0))
    s.new_point(name='p2',position = (10,0,0))
    s.new_point(name='b', position = (9,0,0.5))
    s.new_circle(name='bar',parent='b',radius=1.2,axis=(0,1,0), roundbar=True)

    c = s.new_cable(connections=['p1','bar','p2'],name='cable',EA=1e6,length=20)

    s._save_coredump()

    c.update()

    assert(c.actual_length<20.1)