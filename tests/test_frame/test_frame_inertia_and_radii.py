from DAVE import *
from numpy.testing import assert_allclose

def test_ineria_and_radii():
    s = Scene()
    f = s.new_frame('f',inertia=100, inertia_radii=[1,2,2.1])

    s2 = s.copy()

    assert s['f'].inertia == 100
    assert_allclose(s['f'].inertia_radii, (1,2,2.1))
    assert s2['f'].inertia == 100
    assert_allclose(s2['f'].inertia_radii, (1,2,2.1))
