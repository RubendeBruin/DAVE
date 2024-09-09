import numpy as np
from numpy.testing import assert_allclose

from DAVE import *

def model():
    s = Scene()
    # auto generated python code
    # By MS12H
    # Time: 2024-09-04 17:40:11 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution

    def solved(number):
        return number


    # Environment settings
    s.g = 9.80665
    s.waterlevel = 0.0
    s.rho_air = 0.00126
    s.rho_water = 1.025
    s.wind_direction = 0.0
    s.wind_velocity = 0.0
    s.current_direction = 0.0
    s.current_velocity = 0.0



    # code for Barge
    s.new_rigidbody(name='Barge',
                    mass=1200,
                    cog=(0,
                         0,
                         0),
               position=(0,
                         0,
                         solved(0.8522238246788244)),
               rotation=(solved(0),
                         solved(0),
                         solved(0)),
               fixed =(True, True, False, False, False, False),
                    )

    # code for Barge2
    s.new_rigidbody(name='Barge2',
                    mass=1200,
                    cog=(0,
                         0,
                         0),
               position=(solved(0.0),
                         solved(0.0),
                         solved(7.852)),
               rotation=(solved(0),
                         solved(0),
                         solved(0)),
               fixed =(False, False, False, False, False, False),
                    )

    # code for Buoyancy
    mesh = s.new_buoyancy(name='Buoyancy',
              parent='Barge')
    mesh.trimesh.load_file(r'res: cube.obj', scale = (60.0,17.0,4.0), rotation = (0.0,0.0,0.0), offset = (0.0,0.0,0.0))

    # code for Support1
    s.new_frame(name='Support1',
               parent='Barge',
               position=(20,
                         5,
                         3),
               rotation=(0,
                         0,
                         0),
               fixed =(True, True, True, True, True, True),
                )

    # code for Support2
    s.new_frame(name='Support2',
               parent='Barge',
               position=(20,
                         -5,
                         3),
               rotation=(0,
                         0,
                         0),
               fixed =(True, True, True, True, True, True),
                )

    # code for Support3
    s.new_frame(name='Support3',
               parent='Barge',
               position=(-20,
                         -5,
                         3),
               rotation=(0,
                         0,
                         0),
               fixed =(True, True, True, True, True, True),
                )

    # code for Support4
    s.new_frame(name='Support4',
               parent='Barge',
               position=(-20,
                         5,
                         3),
               rotation=(0,
                         0,
                         0),
               fixed =(True, True, True, True, True, True),
                )

    # code for Point4
    s.new_point(name='Point4',
              parent='Barge2',
              position=(-20,
                        5,
                        -1.99978))

    # code for Point3
    s.new_point(name='Point3',
              parent='Barge2',
              position=(-20,
                        -5,
                        -1.99978))

    # code for Point2
    s.new_point(name='Point2',
              parent='Barge2',
              position=(20,
                        -5,
                        -1.99978))

    # code for Point
    s.new_point(name='Point',
              parent='Barge2',
              position=(20,
                        5,
                        -1.99978))

    # code for Buoyancy2
    mesh = s.new_buoyancy(name='Buoyancy2',
              parent='Barge2')
    mesh.trimesh.load_file(r'res: cube.obj', scale = (40.0,10.0,4.0), rotation = (0.0,0.0,0.0), offset = (0.0,0.0,0.0))

    # code for SP
    s.new_supportpoint(name='SP',
                frame='Support1',
                point='Point',
                kz=100000,
                delta_z=0.01,
                )

    # code for SP2
    s.new_supportpoint(name='SP2',
                frame='Support2',
                point='Point2',
                kz=100000,
                kx=0.5,
                ky=0.5,
                delta_z=0.01,
                )

    # code for SP3
    s.new_supportpoint(name='SP3',
                frame='Support3',
                point='Point3',
                kz=100000,
                kx=0.5,
                ky=0.5,
                delta_z=0.01,
                )

    # code for SP4
    s.new_supportpoint(name='SP4',
                frame='Support4',
                point='Point4',
                kz=100000,
                delta_z=0.01,
                )

    # Limits

    # Watches

    # Tags

    # - tags are added with 'try_add_tags' because the node may not exist anymore (eg changed components) wh

    # Colors
    return s

def test_solve():
    s = model()
    s.solve_statics()

def test_footprint():
    s = model()

    s.solve_statics()

    shearline = s['Barge'].give_load_shear_moment_diagram()
    shearline.plot_simple()

    x, Vz, My = shearline.give_shear_and_moment()

    assert_allclose(np.mean(Vz), 0, atol=1e-6)
    assert_allclose(np.max(Vz), 5884, atol=1)

    assert_allclose(Vz[0], 0, atol=1e-6)
    assert_allclose(Vz[-1], 0, atol=1e-6)

    assert_allclose(My[-1], 0, atol=1e-6)
    assert_allclose(My[-1], 0, atol=1e-6)

    assert_allclose(np.mean(My), -19644, atol=1)


if __name__ == '__main__':
    s = model()

    DG(s)