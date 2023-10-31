from DAVE import *
from numpy.testing import assert_allclose


def test_tilt():
    s = Scene()
    f = s.new_frame("f")
    f.rx = 30
    assert_allclose(f.tilt_x, 30)
    assert_allclose(f.heel, 30)


def test_tilt2():
    s = Scene()
    f = s.new_frame("f")
    f.rx = -30
    assert_allclose(f.tilt_x, -30)
    assert_allclose(f.heel, -30)


def test_tilt3():
    s = Scene()
    f = s.new_frame("f")
    f.ry = 30
    assert_allclose(f.tilt_y, 30)
    assert_allclose(f.trim, 30)


def test_tilt4():
    s = Scene()
    f = s.new_frame("f")
    f.ry = -30
    assert_allclose(f.tilt_y, -30)

    assert_allclose(f.trim, -30)
