from DAVE import *

def test_sheaved_catenary():

    s = Scene()
    f = s.new_frame('global')

    p1 = s.new_point('p1', position=(-10, 0, 0), parent=f)
    s.new_point('p2', position=(1, 2, 0), parent=f)
    s.new_point('p3', position=(4, 4, 0), parent=f)

    s.new_cable(connections=['p1', 'p2', 'p3'], name='cable', EA=122345, mass = 1000, length=30)
    #
    # s['cable']._vfNode._set_shifts([0, -3, 0])
    # s.update()
    # print(p1.force)
    # print(s['cable'].friction_forces)
    #
    # s['cable']._vfNode._set_shifts([0, 3, 0])
    # s.update()
    #
    #
    #
    # print(p1.force)
    # print(s['cable'].friction_forces)
    #
    # import numpy as np
    #
    # xx = np.linspace(-0.1, 0.1, 100)
    # yy= []
    # for x in xx:
    #     s['cable']._vfNode._set_shifts([0, x, 0])
    #     s.update()
    #     yy.append(s['cable'].friction_forces[0])
    #
    # # plot xx vs yy
    # import matplotlib.pyplot as plt
    # plt.plot(xx, yy)
    # plt.show()
    #
    # #
    # # s._save_coredump()
    # #
    from DAVE.gui import Gui
    Gui(s)


    s.solve_statics()

    print(f"DOFS = {s._vfc.get_dofs()}")

if __name__ == '__main__':
    test_sheaved_catenary()