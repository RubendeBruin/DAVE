from DAVE import *

def model():

    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2024-05-02 10:28:47 UTC

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

    # code for Frame
    s.new_frame(name='Frame',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for Frame_1
    s.new_frame(name='Frame_1',
                parent='Frame',
                position=(0,
                          0,
                          0),
                rotation=(solved(25),
                          0,
                          0),
                fixed=(True, True, True, False, True, True),
                )

    # code for Frame_2
    s.new_frame(name='Frame_2',
                parent='Frame',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          10,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for Point
    s.new_point(name='Point',
                parent='Frame_1',
                position=(2,
                          0,
                          -2))

    # code for Point_1
    s.new_point(name='Point_1',
                parent='Frame_2',
                position=(-1,
                          0,
                          -2))

    # code for Circle
    c = s.new_circle(name='Circle',
                     parent='Point',
                     axis=(0, 1, 0),
                     radius=1)

    # code for Circle_1
    c = s.new_circle(name='Circle_1',
                     parent='Point_1',
                     axis=(0, 1, 0),
                     radius=1)

    return s

def test_change_parent_Frame():
    s = model()
    s.delete('Frame_2')  # clean up

    # Frame is the parent of Frame_1
    # Frame_1 has the rotational x dof free
    # but Frame has zero rotation
    # So it should not be an issue

    s['Frame_1'].change_parent_to(None)


def test_dissolve_Frame():
    s = model()
    s.delete('Frame_2')  # clean up

    # Frame is the parent of Frame_1
    # Frame_1 has the rotational x dof free
    # but Frame has zero rotation
    # So it should not be an issue

    s.dissolve('Frame')

def test_change_parent_of_circle():
    s = model()
    s['Circle_1'].change_parent_to(s['Point'])



if __name__ == '__main__':
    s = model()
    DG(s)

