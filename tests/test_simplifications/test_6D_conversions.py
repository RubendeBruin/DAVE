import numpy as np
from numpy.testing import assert_allclose

from DAVE import *
from DAVE.io.simplify import connector6D_to_cables


def model():
    s = Scene()
    s.new_frame("global", fixed=True)
    s.new_rigidbody("connected", fixed = False, mass=1, cog = (0.1,0,0))

    s.new_linear_connector_6d("connector", main = "global", secondary = "connected",
                              stiffness = (0,0,10,10,10,0))

    return s

def do_check(s):
    s.solve_statics()

    P1 = s["connected"].position
    R1 = s["connected"].rotation

    from DAVE.io.simplify import connector6D_to_cables
    connector6D_to_cables(s, s["connector"], L=10)

    # DG(s)

    s.solve_statics()

    P2 = s["connected"].position
    R2 = s["connected"].rotation

    assert_allclose(P1, P2, atol=1e-1)

    print('-------------------')
    print("TRANSLATION OK")
    print('-------------------')

    assert_allclose(R1, R2, atol=1e-1)


def test_kz():
    s = model()
    s["connected"].mass = 1
    s["connected"].cog =  (0.1,0,0)
    s["connector"].stiffness = (0,0,10,10,10,0)

    s.solve_statics()

    # expected position in base-case
    assert_allclose(s["connected"].gz, -1*s.g / 10,atol=1e-5)  # check base-case

    # expected rotation in base-case
    moment = 1 * s.g * 0.1  # kN*m / rad

    angle_rad = moment / 10  # rad
    angle_deg = angle_rad * 180 / np.pi  # deg

    assert_allclose(s["connected"].rotation[1], angle_deg, atol=1e-1)  # check base-case

    print("SELF-CHECK OK")

    do_check(s)

def test_pure_moment():
    s = model()
    s["connected"].mass = 0
    s["connector"].stiffness = (0,0,10,10,10,0)

    s.new_point("Point", parent="connected")
    s.new_force("Force",parent="Point", moment=(0,1,0))

    do_check(s)


def test_kxkymz():
    s = model()
    s["connected"].mass = 0
    s["connector"].stiffness = [10,10,0,0,0,10]
    do_check(s)

def test_all():
    s = model()
    s["connected"].mass = 0.1 # use a lower mass to avoid non-linearities
    s["connector"].stiffness = [10,20,10,40,50,60]
    do_check(s)


def test_differently():
    s = model()

    s["connector"].stiffness = (0, 0, 133.3, 0, 13333, 0)
    s["connected"].mass = 0

    connector6D_to_cables(s, s["connector"], L=50)

    con = s['connected']
    con.fixed = (True, True, True, True, True, True)

    con.z = -1
    s.update()
    fz = con.connection_force_z

    assert_allclose(fz, 133.3,rtol=1e-6)

    con.z = 0

    r = 1
    s['connected'].ry = -r
    s.update()
    m = con.connection_moment_y

    ky = m / np.deg2rad(r)

    print(f"ky = {ky}")
    assert_allclose(13333, ky, rtol=1e-3)

