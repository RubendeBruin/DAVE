"""Catenaries in DAVE can be modelled in two ways:

1. As Cable
2. As Beam without bending stiffness

The tests in this file compare the results of both methods and verifies that they are the same. There is a slight
tolerance as the "beam" method is not exact while the cable method is.
"""

import numpy as np
from numpy.testing import assert_allclose

from DAVE import *



def give_beam_and_cable_scene(L=18, EA=1e6, mass=0.1):

    s = Scene()
    # code for Frame
    s.new_frame(name='Frame',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True))

    # code for Frame2
    s.new_frame(name='Frame2',
                position=(6,
                          2,
                          4),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True))

    # code for Beam1
    s.new_frame(name='Beam1',
                parent='Frame',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True))

    # code for Point1
    s.new_point(name='Point1',
                parent='Frame',
                position=(0,
                          0.3,
                          0))

    # code for Beam2
    s.new_frame(name='Beam2',
                parent='Frame2',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True))

    # code for Point2
    s.new_point(name='Point2',
                parent='Frame2',
                position=(0,
                          0.3,
                          0))

    # code for Cable
    s.new_cable(name='Cable',
                endA='Point1',
                endB='Point2',
                length=L,
                mass_per_length=mass/L,
                EA=EA)

    # code for beam Beam
    s.new_beam(name='Beam',
               nodeA='Beam1',
               nodeB='Beam2',
               n_segments=20.0,
               tension_only=True,
               EIy=0,
               EIz=0,
               GIp=0,
               EA=EA,
               mass=mass,
               L=L)  # L can possibly be omitted

    return s

def assertS(s):
    assert_allclose(s['Beam1'].applied_force[:3], s['Point1'].applied_force, rtol = 1e-4, atol = 1e-2)
    assert_allclose(s['Beam2'].applied_force[:3], s['Point2'].applied_force, rtol = 1e-4, atol = 1e-2)

def plot_initial_estimate(s):

    beam = s['Beam']
    bp = beam.global_positions
    cp = s['Cable']
    pos, ten = cp._vfNode.get_drawing_data(int(beam.n_segments+1), 2,False)

    bx = [p[0] for p in bp]
    bz = [p[2] for p in bp]
    cx = [p[0] for p in pos]
    cz = [p[2] for p in pos]

    import matplotlib.pyplot as plt

    plt.plot(bx, bz, 'o-')
    plt.plot(cx, cz, '*-')

    s.solve_statics()
    bp = beam.global_positions
    bx = [p[0] for p in bp]
    bz = [p[2] for p in bp]
    plt.plot(bx, bz, '+')

    plt.show()


def test_elastic_catenary_estimations_slack():

    s = give_beam_and_cable_scene(L=18, EA=1e6, mass=0.1)

    s.solve_statics()
    assertS(s)

def test_elastic_catenary_estimations_taut():

    s = give_beam_and_cable_scene(L=18, EA=1e6, mass=0.1)
    s['Frame2'].x = 20
    s.solve_statics()
    assertS(s)

def test_elastic_catenary_estimations_various():

    doplot = False
    variations = [(18, 1e6, 1),
                  (17, 1e5, 2),
                  (17.5, 1e4, 3),
                  (18, 1e3, 4),
                  (16.5, 1e2, 5),
                  (16, 1e2, 5),
                  (15.5, 1e2, 5),
                  (15, 1e2, 5),
                  ]

    if doplot:
        import matplotlib.pyplot as plt

    for (L, EA, mass) in variations:
        s = give_beam_and_cable_scene(L=L, EA=EA, mass=mass)
        s['Frame2'].x = 20

        s.solve_statics()
        assertS(s)

        if doplot:
            bp = s['Beam'].global_positions
            bx = [p[0] for p in bp]
            bz = [p[2] for p in bp]
            plt.plot(bx, bz)

    if doplot:
        plt.show()


def compare(p1, p2, c):
    L = c.length
    EA = c.EA
    dist = np.linalg.norm(np.array(p2.position) - p1.position)
    s = c._scene

    elastic_tension = EA * (dist - L) / L

    dH = p2.x - p1.x
    dV = p2.z - p1.z

    # estimate_taut_catenary(double weight, double dH, double dV, double EA, double tension);
    Fh, Fv1, Fv2 = estimate_taut_catenary(c.mass, c._scene.g, dH, dV, EA, elastic_tension)

    return elastic_tension, Fh, Fv1, Fv2, p1.fx, p1.fz, p2.fz


# s = Scene()
# p1 = s.new_point('p1', position=(0, 0, 0))
# p2 = s.new_point('p2', position=(1, 0, 11))
#
# c = s.new_cable(connections=['p1', 'p2'], name='cable', EA=1000000, mass=1, length=10)
# s.update()
# # weight_fraction, Fh, Fv1, Fv2, fx, fy1, fy2 = compare(p1, p2, c)
# #
# # print(weight_fraction)
# # print(Fh-fx)
# # print(Fv1-fy1)
# # print(Fv2-fy2)
#
# L = c.length
# EA = c.EA
# dist = np.linalg.norm(np.array(p2.position) - p1.position)
# weight = c.mass * s.g
#
# elastic_tension = EA * (dist - L) / L
#
# print(elastic_tension)
# print(c.tension)
#
# dH = p2.x - p1.x
# dV = p2.z - p1.z
#
# # estimate_taut_catenary(double weight, double dH, double dV, double EA, double tension);
# Fh, Fv1, Fv2 = estimate_taut_catenary(1, s.g, dH, dV, EA, elastic_tension)
#
# print(Fh)
# print(p1.fx)
#
#
# import matplotlib.pyplot as plt
# fig = plt.figure(figsize=(10, 5))
# ax_main = ax1 = plt.subplot2grid(shape=(2, 4), loc=(0, 0), colspan=2, rowspan=2)
# ax1 = plt.subplot2grid(shape=(2, 4), loc=(0, 2))
# ax2 = plt.subplot2grid(shape=(2, 4), loc=(0, 3))
# ax3 = plt.subplot2grid(shape=(2, 4), loc=(1, 2))
# ax1.set_title('dFH1')
# ax2.set_title('dFV1')
# ax3.set_title('dFH2')
#
#
# # tension due to stretch
#
# for i in range(1000):
#
#     dx = 1*np.sin(i/10)
#     dy = 1*np.sin(i/13)
#
#     p2.x = 1 + dx
#     p2.z = 10 + dy
#
#     s.update()
#
#     if c.stretch > -0.01:
#
#         weight_fraction, Fh, Fv1, Fv2, fx, fy1, fy2 = compare(p1, p2, c)
#
#         points = c.get_points_for_visual()
#         x = [p[0] for p in points]
#         y = [p[2] for p in points]
#         ax_main.plot(x,y)
#
#         ax1.plot(weight_fraction, Fv1-fy1, 'r*')
#         ax2.plot(weight_fraction, Fv2 - fy2, 'r*')
#         ax3.plot(weight_fraction, Fh-fx, 'r*')
#         # ax4.plot(weight_fraction, dFV2, 'r*')
#
# plt.show()

if __name__ == '__main__':
    from DAVE.gui import Gui
    s = give_beam_and_cable_scene(L=18, EA=1e6, mass=0.1)
    Gui(s)