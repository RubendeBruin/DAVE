from numpy.testing import assert_allclose

from DAVE import *

if __name__ == '__main__':


    s = Scene()

    # code for Point
    s.new_point(name='Point',
                position=(0,
                          0,
                          0))

    # code for Point2
    s.new_point(name='Point2',
                position=(2,
                          0,
                          5))

    s.new_point('P3', position=(4, 0, 3))

    # code for Circle
    c = s.new_circle(name='Bottom',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Circle2
    c = s.new_circle(name='Top',
                     parent='Point2',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Loop
    s.new_cable(name='Loop',
                endA='Top',
                endB='Top',
                length=16.2832,
                diameter=0.5,
                EA=12345.0,
                sheaves=['P3','Bottom'])



    loop :Cable = s['Loop']

    locations = loop._get_cable_points_at_mid_of_connections()

    print(locations)

    theta1 = loop.connections[0].theta_from_point(locations[0])
    theta2 = loop.connections[2].theta_from_point(locations[2])

    P1 = loop.connections[0].point3_from_theta_and_r_local(theta1, r=2)
    P2 = loop.connections[2].point3_from_theta_and_r_local(theta2, r=2)

    s.new_point('P1', position=P1)
    s.new_point('P2', position=P2)

    s.update()

    print(f"Angles at connection = {loop._vfNode.angles_at_connections}")
    print(f"Angles at connection = {loop.angles_at_connections}")

    loop.connected_bars_active

    s['Loop'].connections = ('Top', 'P3', 'Top')

    s['Bottom'].is_roundbar = True
    s['Loop'].connections = ('Top', 'Bottom', 'P3', 'Top')

    print(loop.connected_bars_active)

    print(loop.material_lengths_no_bars)

    loop.reversed = [False, True, False, False]

    print(loop.material_lengths_no_bars)

    exit(0)

    # loop.set_all_sticky()



    loop.diameter = 0.3

    # print(loop.segment_lengths)

    # s._save_coredump()

    # DG(s, autosave=False)


    #
    # # plot x and y coordinates of the locations using matplotlib
    # import matplotlib.pyplot as plt
    #
    # x = [loc[0] for loc in locations]
    # y = [loc[2] for loc in locations]
    #
    # plt.plot(x, y, 'ro')
    #
    # # add numbers
    # for i, txt in enumerate(locations):
    #     plt.annotate(f"{i}", (x[i], y[i]))
    #
    # plt.axis('equal')
    # plt.show()
    #



    # s.delete('Loop')

    DG(s, autosave=False)