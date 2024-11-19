import numpy as np
from numpy.testing import assert_allclose


from DAVE import *

def plot():
    s  = Scene()
    p1 = s.new_point(name='Point1', position=(0, 0, 0))

    c = s.new_circle(name='Circle', parent=p1, axis=(0, 1, 0), radius=5)

    #
    # for axis in [(0,0,1),(0,1,0),(1,0,0)]:
    #     c.axis = axis
    #     print(f"{axis} -> {c._local_y_axis} and {c._local_x_axis}")

    c.axis = (0,1,0)


    for angle in np.linspace(0, 360, num=9):
        theta = np.deg2rad(angle)
        p3 = c.point3_from_theta_and_r_local(theta=theta, r=5.0)
        s.new_point(f'Angle = {angle}', position=p3)

        check_theta = c.theta_from_point(p3)
        assert_allclose(theta, check_theta, atol=1e-6)

    s.new_force(name='Force', parent=p1, force=c.axis)

    return s

def test_directions_theta0_on_top():

    for axis in [(0,0,1),(0,1,0),(1,0,0),(1,1,0), (1,1,1), (1,0,1), (0,1,1),
                 (-1,0,0),(0,-1,0),(0,0,-1),(-1,-1,0), (-1,-1,-1), (-1,0,-1), (0,-1,-1),
                 (1,-1,0), (1,-1,-1), (1,0,-1), (1,1,-1), (1,1,0), (1,1,1), (1,0,1), (0,1,1),
                 (-1,1,0), (-1,1,1), (-1,0,1), (-1,-1,1), (-1,-1,0), (-1,-1,-1), (-1,0,-1), (0,-1,-1)]:

        s = Scene()
        p1 = s.new_point(name='Point1', position=(0, 0, 0))

        c = s.new_circle(name='Circle', parent=p1, axis=axis, radius=5)

        p0 =  c.point3_from_theta_and_r_local(theta=0, r=5.1)

        for angle in np.linspace(0, 360, num=30):
            theta = np.deg2rad(angle)
            p3 = c.point3_from_theta_and_r_local(theta=theta, r=5.0)

            assert p0[2] >= p3[2]

            check_theta = c.theta_from_point(p3)
            assert_allclose(theta, check_theta, atol=1e-6)




if __name__ == '__main__':
    s = plot()
    DG(s)




    DG(s, autosave=False)