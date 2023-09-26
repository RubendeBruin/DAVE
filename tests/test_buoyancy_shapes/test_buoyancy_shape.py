from numpy.testing import assert_allclose

from DAVE import *

def box_model():
    s = Scene()

    body = s.new_rigidbody("Box", mass=0)
    b = s.new_buoyancy("shape", parent=body)
    b.trimesh.load_obj("res: cube.obj", scale=(100, 10, 4))

    return s,b, body

def test_cob_initial():
    s,b, body = box_model()
    s.solve_statics()
    s.verify_equilibrium()

    assert_allclose(b.cob,(0,0,-1))
    assert_allclose(body.connection_force_z, 100 * 10 * 2 * s.g * s.rho_water)

def test_cob_movement_z():
    s,b, body = box_model()
    s.update()
    assert_allclose(b.cob,(0,0,-1))

    body.position = (0,0,-1)
    s.update()
    assert_allclose(b.cob,(0,0,-1.5))
    assert_allclose(body.connection_force_z, 100*10*3*s.g*s.rho_water)

def test_cob_movement_xy():
    s,b, body = box_model()
    s.update()
    assert_allclose(b.cob,(0,0,-1))

    body.position = (10,2,0)
    s.update()
    assert_allclose(b.cob,(10,2,-1))

def test_cob_movement_trim():
    s,b, body = box_model()
    s.update()
    assert_allclose(b.cob,(0,0,-1))

    body.rotation = (0,1,0)  # trim by 1 degree
    s.update()
    assert_allclose(b.cob,(7.256,0,-1.063), atol=1e-3)

    body.rotation = (0,0,0)
    s.update()
    assert_allclose(body.connection_moment_y,0)

def test_cob_movement_heel():
    s,b, body = box_model()
    s.update()
    assert_allclose(b.cob,(0,0,-1))

    body.rotation = (1,0,0)  # heel by 1 degree
    s.update()
    assert_allclose(b.cob,(0,-5.527703e-02,-1.0005), atol=1e-3)
    assert_allclose(body.connection_moment_x,-1111.269129)

    body.rotation = (0,0,0)
    s.update()
    assert_allclose(body.connection_moment_x,0)


