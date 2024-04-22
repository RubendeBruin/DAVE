import pytest
from numpy.testing import assert_allclose

from DAVE import *

def model():
    s = Scene()
    f1 = s.new_frame('f1', rotation=(0, 0, 30))
    f2 = s.new_frame('f2', parent=f1, fixed="TFTTTT")
    f3 = s.new_frame('f3', parent=f2, fixed=True)

    return s,f1,f2,f3

def test_dissolve_dofs_i125():
    s, f1, f2, f3 = model()

    with pytest.raises(ValueError):  # Node f2 has degrees of freedom and can therefore not be dissolved
        s.dissolve(f2)

def test_dissolve_f1_issue125():
    s, f1, f2, f3 = model()

    # dissolving f1 would change the orientation of the degree of freedom of f2
    # so this is not allowed

    with pytest.raises(ValueError):
        s.dissolve(f1)


def test_change_parent_to():
    s, f1, f2, f3 = model()


    with pytest.raises(ValueError):
        f2.change_parent_to(None)



def test_dissolve_f1_issue125_Fixed():
    s, f1, f2, f3 = model()

    f2.fixed = [False, False, False, True, True, True]

    o1 = f3.global_rotation

    s.dissolve(f1) # no problem

    assert_allclose(f3.global_rotation, o1)

