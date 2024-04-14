import pytest

from DAVE import *

def model():
    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2024-04-14 15:06:00 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution

    def solved(number):
        return number

    # code for Frame
    s.new_frame(name='Frame',
                position=(3,
                          0,
                          0),
                rotation=(solved(0),
                          solved(0),
                          solved(0)),
                fixed=(True, True, True, False, False, False),
                )

    # code for Frame2
    s.new_frame(name='Frame2',
                parent='Frame',
                position=(3,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for Frame3
    s.new_frame(name='Frame3',
                parent='Frame2',
                position=(3,
                          0,
                          0),
                rotation=(solved(0),
                          0,
                          0),
                fixed=(True, True, True, False, True, True),
                )

    # code for Frame4
    s.new_frame(name='Frame4',
                parent='Frame3',
                position=(3,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for Frame5
    s.new_frame(name='Frame5',
                parent='Frame4',
                position=(3,
                          0,
                          0),
                rotation=(solved(0),
                          solved(0),
                          solved(0)),
                fixed=(True, True, True, False, False, False),
                )

    # code for Frame6
    s.new_frame(name='Frame6',
                parent='Frame5',
                position=(3,
                          0,
                          0),
                rotation=(solved(0),
                          solved(0),
                          solved(0)),
                fixed=(True, True, True, False, False, False),
                )

    # code for Frame7
    s.new_frame(name='Frame7',
                parent='Frame6',
                position=(3,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True),
                )

    # code for Body
    s.new_rigidbody(name='Body',
                    mass=4,
                    cog=(0,
                         0,
                         0),
                    parent='Frame7',
                    position=(3,
                              0,
                              0),
                    rotation=(0,
                              0,
                              0),
                    fixed=(True, True, True, True, True, True),
                    )


    return s

def test_copy_state():
    s = model()
    s2 = s.copy()

    assert s2.verify_equilibrium() == False

    s.solve_statics()
    s2.state = s.state

    s2.verify_equilibrium()


def test_set_invalid_state():
    s= model()

    with pytest.raises(ValueError):
        s.state = []


def test_set_invalid_state2():
    s = model()
    state = s.state
    s.clear()
    with pytest.raises(ValueError):
        s.state = state

