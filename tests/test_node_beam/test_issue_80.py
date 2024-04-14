"""3553 def moment_A(self):
"Moment on beam at node A (kNm, kNm, kNm) , axis system of node A""
-> 3555 return self._vfNode.moment_on_master
3556
3557 @Property

AttributeError: 'pyo3d.LinearBeam' object has no attribute 'moment_on_master'"""
import numpy as np
from numpy.testing import assert_allclose

from DAVE import *

def test_internal_forces_symmetric_model():
    """Both ends of the beam are supported vertically and rotationally.

    The weight of the beam is 1.4 kN/m.
    """

    s = Scene()


    # code for f1
    s.new_frame(name='f1',
               position=(0,
                         0,
                         0),
               rotation=(0,
                         0,
                         0),
               fixed =(True, True, True, True, True, True),
                )

    # code for f2
    s.new_frame(name='f2',
                position=(15,
                         0,
                         0),
               fixed =(False, False, True, True, True, True),
                )

    # code for beam beam
    beam = s.new_beam(name='beam',
                nodeA='f1',
                nodeB='f2',
                n_segments=20.0,
                tension_only=False,
                EIy =1000,
                EIz =1000,
                GIp =1000,
                EA =1e+06,
                mass =1.4,
                L =15) # L can possibly be omitted



    # Limits

    # Watches

    # Tags

    # Colors

    s.solve_statics()

    # DG(s)

    forces = beam.internal_forces
    moments = beam.internal_moments


    a = beam.moment_A
    b = beam.moment_B

    fa = beam.force_A
    fb = beam.force_B

    assert_allclose(a,[-c for c in b], atol=1e-5)
    assert_allclose(fa[0],-fb[0], atol=1e-5)
    assert_allclose(fa[1],fb[1], atol=1e-5)
    assert_allclose(fa[2],fb[2], atol=1e-5)

    fz = [f[2] for f in forces]
    my = [m[1] for m in moments]

    # import matplotlib.pyplot as plt
    # x = beam.X_nodes
    # plt.plot(x, fz, label='Fz')
    # plt.plot(x, my, label='My')
    # plt.legend()
    # plt.show()

    assert(fz[0] != fz[-1])
    assert(my[0] != my[-1])
    assert_allclose(fz[0] ,- fz[-1])
    assert_allclose(my[0] , my[-1], atol=1e-4)


def test_internal_forces_cantiliver():
    """Both ends of the beam are supported vertically and rotationally.

    The weight of the beam is 1 mT.
    """

    s = Scene()


    # code for f1
    s.new_frame(name='f1',
               fixed = True,
                )

    # code for f2
    s.new_frame(name='f2',
                position=(15,
                         0,
                         0),
               fixed = False)

    # code for beam beam
    beam = s.new_beam(name='beam',
                nodeA='f1',
                nodeB='f2',
                n_segments=20.0,
                tension_only=False,
                EIy =1000,
                EIz =1000,
                GIp =1000,
                EA =1e+06,
                mass =1,
                L =15) # L can possibly be omitted

    s.solve_statics()

    # Left end A is fixed
    # Right end B is free

    FA = beam.force_A
    assert_allclose(np.linalg.norm(FA), s.g * beam.mass, atol=1e-3)
    assert FA[2] < 0

    FB = beam.force_B
    assert_allclose(np.linalg.norm(FB), 0, atol=1e-3)

    MA = beam.moment_A
    assert_allclose(np.linalg.norm(MA), 0.5*beam.L * beam.mass * s.g, rtol = 0.1)  # this is only a rough estimate, the beam is not straight
    assert_allclose(MA[1], 0.5*beam.L * beam.mass * s.g, rtol = 0.1)  # this is only a rough estimate, the beam is not straight

def test_internal_forces_cantiliver_reversed():
    """Both ends of the beam are supported vertically and rotationally.

    The weight of the beam is 1 mT.
    """

    s = Scene()


    # code for f1
    s.new_frame(name='f1',
               fixed = False,
                )

    # code for f2
    s.new_frame(name='f2',
                position=(15,
                         0,
                         0),
               fixed = True)

    # code for beam beam
    beam = s.new_beam(name='beam',
                nodeA='f1',
                nodeB='f2',
                n_segments=20.0,
                tension_only=False,
                EIy =1000,
                EIz =1000,
                GIp =1000,
                EA =1e+06,
                mass =1,
                L =15) # L can possibly be omitted

    s.solve_statics()

    # Left end A is fixed
    # Right end B is free

    FB = beam.force_B
    assert_allclose(np.linalg.norm(FB), s.g * beam.mass, atol=1e-3)
    assert FB[2] < 0

    FA = beam.force_A
    assert_allclose(np.linalg.norm(FA), 0, atol=1e-3)

    MB = beam.moment_B
    assert_allclose(np.linalg.norm(MB), 0.5*beam.L * beam.mass * s.g, rtol = 0.1)  # this is only a rough estimate, the beam is not straight
    assert_allclose(MB[1], -0.5*beam.L * beam.mass * s.g, rtol = 0.1)  # this is only a rough estimate, the beam is not straight

