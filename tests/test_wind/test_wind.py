import numpy as np

from DAVE import *
from numpy.testing import assert_allclose
from pytest import raises


def test_wind_plane():
    s = Scene()
    f = s.new_frame("frame")
    p = s.new_point("point", parent=f)
    w = s.new_windarea(
        "wind_area",
        parent=p,
        A=100,
        areakind=AreaKind.PLANE,
        Cd=1.2,
        direction=(1, 0, 0),
    )

    s.wind_direction = 0
    s.wind_velocity = 10

    s.update()

    assert s.wind_velocity == 10
    assert_allclose(w.force, (0.5 * s.rho_air * 100 * 1.2 * 10 * 10, 0, 0))


def test_wind_plane_perpendicular_means_no_force():
    s = Scene()
    f = s.new_frame("frame")
    p = s.new_point("point", parent=f)
    w = s.new_windarea(
        "wind_area",
        parent=p,
        A=100,
        areakind=AreaKind.PLANE,
        Cd=1.2,
        direction=(1, 0, 0),
    )

    s.wind_direction = 90
    s.wind_velocity = 10

    s.update()

    assert s.wind_velocity == 10
    assert_allclose(w.force, 0, atol=1e-6)

    s.wind_direction = 270
    s.update()
    assert_allclose(w.force, 0, atol=1e-6)

    s.wind_direction = 180
    s.update()
    assert w.force[0] < -1  # just to check that we're not getting false negatives




def test_wind_plane_rot90():
    s = Scene()
    f = s.new_frame("frame")
    p = s.new_point("point", parent=f)
    w = s.new_windarea(
        "wind_area",
        parent=p,
        A=100,
        areakind=AreaKind.PLANE,
        Cd=1.2,
        direction=(1, 0, 0),
    )

    s.wind_direction = 90
    s.wind_velocity = 10

    w.direction = (0,1,0)

    s.update()

    assert s.wind_velocity == 10
    assert_allclose(w.force, (0, 0.5 * s.rho_air * 100 * 1.2 * 10 * 10, 0), atol=1e-7)


def test_wind_cylinder():
    s = Scene()
    f = s.new_frame("frame")
    p = s.new_point("point", parent=f)
    w = s.new_windarea(
        "wind_area",
        parent=p,
        A=100,
        areakind=AreaKind.CYLINDER,
        Cd=1.2,
        direction=(0, 0, 1),
    )

    s.wind_direction = 10
    s.wind_velocity = 10

    s.update()

    assert s.wind_velocity == 10

    f = 0.5 * s.rho_air * 100 * 1.2 * 10 * 10

    assert_allclose(
        w.force, (np.cos(np.deg2rad(10)) * f, np.sin(np.deg2rad(10)) * f, 0)
    )

def test_wind_invalid_type():
    s = Scene()
    f = s.new_frame("frame")
    p = s.new_point("point", parent=f)
    w = s.new_windarea(
        "wind_area",
        parent=p,
        A=100,
        areakind=AreaKind.CYLINDER,
        Cd=1.2,
        direction=(0, 0, 1),
    )

    with raises(ValueError):
        w.areakind = 4

def test_wind_invalid_direction():
    s = Scene()
    f = s.new_frame("frame")
    p = s.new_point("point", parent=f)
    w = s.new_windarea(
        "wind_area",
        parent=p,
        A=100,
        areakind=AreaKind.CYLINDER,
        Cd=1.2,
        direction=(0, 0, 1),
    )

    with raises(AssertionError):
        w.direction = (1,2,3,4)

def test_wind_on_beam():
    s = Scene()
    bar = s.new_rigidbody("bar", fixed = (True,True,True,False,False,False), cog = (0,0,10), mass=10)
    wind_point = s.new_point("point",parent=bar, position = (0,0,20))
    w = s.new_windarea(
        "wind_area",
        parent=wind_point,
        A=100,
        areakind=AreaKind.PLANE,
        Cd=1.2,
        direction=(1, 0, 0),
    )

    s.wind_direction = 37
    s.wind_velocity = 10
    s.solve_statics()

    # from DAVE.gui import Gui
    #
    # Gui(s)

def test_wind_on_beam_1dof():
    s = Scene()
    bar = s.new_rigidbody("bar", fixed = (True,True,True,True,False,True), cog = (0,0,10), mass=10)
    wind_point = s.new_point("point",parent=bar, position = (0,0,20))
    w = s.new_windarea(
        "wind_area",
        parent=wind_point,
        A=100,
        areakind=AreaKind.PLANE,
        Cd=1.2,
        direction=(1, 0, 0),
    )

    s.wind_direction = 37
    s.wind_velocity = 10
    s.solve_statics()

def test_wind_on_beam_cylinder():
    s = Scene()
    bar = s.new_rigidbody("bar", fixed = (True,True,True,False,False,False), cog = (0,0,10), mass=10)
    wind_point = s.new_point("point",parent=bar, position = (0,0,20))
    w = s.new_windarea(
        "wind_area",
        parent=wind_point,
        A=100,
        areakind=AreaKind.CYLINDER,
        Cd=1.2,
        direction=(0, 0, 1),
    )

    s.wind_direction = 25
    s.wind_velocity = 10
    s.solve_statics()

def test_wind_45deg_cylinder():
    s = Scene()
    bar = s.new_frame('frame',rotation=(60,0,0))
    wind_point = s.new_point("point", parent=bar, position=(0, 0, 20))
    w = s.new_windarea(
        "wind_area",
        parent=wind_point,
        A=100,
        areakind=AreaKind.CYLINDER,
        Cd=1.2,
        direction=(0, 0, 1),
    )

    s.wind_direction = 0
    s.wind_velocity = 10

    f = 0.5 * s.rho_air * 100 * 1.2 * 10 * 10
    print(f)

    s.update()
    assert_allclose(w.force, (f,0,0))

    # with a wind-direction of 90, we see the plane under a 60 degree angle

    s.wind_direction = 90
    s.update()
    import math
    assert_allclose(w.force, (0, f * np.cos(np.deg2rad(60)), 0), atol=1e-6)

    # and same for -90


    s.wind_direction = -90
    s.update()
    import math
    assert_allclose(w.force, (0, -f * np.cos(np.deg2rad(60)), 0), atol=1e-6)

def test_wind_scene_copy():
    s = Scene()
    s.wind_direction = 37
    s.wind_velocity = 10

    s2 = Scene(copy_from=s)
    assert s2.wind_direction == 37
    assert s2.wind_velocity == 10


def test_wind_on_beam_to_code_and_back():
    s = Scene()
    bar = s.new_rigidbody("bar", fixed = (True,True,True,True,False,True), cog = (0,0,10), mass=10)
    wind_point = s.new_point("point",parent=bar, position = (0,0,20))
    w = s.new_windarea(
        "wind_area",
        parent=wind_point,
        A=100,
        areakind=AreaKind.PLANE,
        Cd=1.2,
        direction=(1, 0, 0),
    )

    s.wind_direction = 37
    s.wind_velocity = 10

    c = s.give_python_code()

    s2 = Scene(copy_from = s)
    #
    s2.solve_statics()
    s.solve_statics()
    #
    assert_allclose(s['point'].global_position, s2['point'].global_position)




