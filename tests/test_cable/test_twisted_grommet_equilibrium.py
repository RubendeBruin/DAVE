"""This model used to converge to an invalid solution.
There was a twist in the grommet that should not be there. The axes of the circles on top and on bottom of the grommet should align.

We test this for cable with and without weight.
"""
import math
from numpy.testing import assert_allclose

from DAVE import *

def test_nomass():
    s = Scene()

    # code for GrommetProtector/point2
    s.new_point(name='GrommetProtector/point2',
              position=(0,0,0))

    # code for Block
    blk = s.new_rigidbody(name='Block',
                    mass=0.36,
                    cog=(0,
                         0,
                         0.267333),
                    position=(0,0,-10),
                    rotation=(0,0,0),
                    fixed =True )

    # code for GrommetProtector/circle2
    s.new_circle(name='GrommetProtector/circle2',
                parent='GrommetProtector/point2',
                axis=(1, 1, 0),
                radius=0.122 )

    # code for 840 WB300 1/pin_point
    s.new_point(name='840 WB300 1/pin_point',
              parent='Block',
              position=(0,
                        0,
                        0))

    # code for 840 WB300 1/pin
    s.new_circle(name='840 WB300 1/pin',
                parent='840 WB300 1/pin_point',
                axis=(0, 1, 0),
                radius=0.067 )

    # code for system_1/Grommet/_grommet
    s.new_cable(name='system_1/Grommet/_grommet',
                endA='840 WB300 1/pin',
                endB='840 WB300 1/pin',
                length=13.2513,
                diameter=0.08,
                EA=437510.75930952904,
                sheaves = ['GrommetProtector/circle2'])
    s['system_1/Grommet/_grommet'].reversed = (True, False, False)

    s['GrommetProtector/point2']._visible = False

    s['840 WB300 1/pin_point']._visible = False

    assert_allclose(blk.uy, (0,1,0))

    blk.fixed = False

    s.solve_statics()
    a = 0.5 * math.sqrt(2)

    # DG(s)

    # Scene is not solved when initial condition is an equilibrium
    # even when that equilibrium is unstable and not the one we want.

    assert_allclose(blk.uy, (-a, -a, 0.0), atol=1e-2)

def test_with_mass():

    s = Scene()

    # code for GrommetProtector/point2
    s.new_point(name='GrommetProtector/point2',
                position=(0,0,0))

    # code for Block
    blk = s.new_rigidbody(name='Block',
                          mass=0.36,
                          cog=(0,
                               0,
                               0.267333),
                          position=(0,0,-10),
                          rotation=(0,0,0),
                          fixed =True )

    # code for GrommetProtector/circle2
    s.new_circle(name='GrommetProtector/circle2',
                 parent='GrommetProtector/point2',
                 axis=(1, 1, 0),
                 radius=0.122 )

    # code for 840 WB300 1/pin_point
    s.new_point(name='840 WB300 1/pin_point',
                parent='Block',
                position=(0,
                          0,
                          0))

    # code for 840 WB300 1/pin
    s.new_circle(name='840 WB300 1/pin',
                 parent='840 WB300 1/pin_point',
                 axis=(0, 1, 0),
                 radius=0.067 )

    # code for system_1/Grommet/_grommet
    s.new_cable(name='system_1/Grommet/_grommet',
                endA='840 WB300 1/pin',
                endB='840 WB300 1/pin',
                length=13.2513,
                mass = 1,
                diameter=0.08,
                EA=437510.75930952904,
                sheaves = ['GrommetProtector/circle2'])
    s['system_1/Grommet/_grommet'].reversed = (True, False, False)

    s['GrommetProtector/point2']._visible = False

    s['840 WB300 1/pin_point']._visible = False

    assert_allclose(blk.uy, (0,1,0))

    blk.fixed = False


    s.solve_statics()

    a = 0.5 * math.sqrt(2)
    assert_allclose(blk.uy, (-a, -a, 0.0), atol=1e-6)