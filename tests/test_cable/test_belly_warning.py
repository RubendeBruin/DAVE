"""If a cable has more than one belly, a warning should be raised"""

from DAVE import *

def haswarning(cable):
    for w in cable.warnings:
        if 'belly' in w.lower():
            return True
    return False

def test_belly_warning_2p_nowarn():
    s = Scene()
    s.new_point('p1')
    s.new_point('p2', position = (10,0,0))
    cab = s.new_cable('c1', connections = ['p1', 'p2'], length = 12, mass_per_length=0.1, EA=10000)

    s.update()

    assert not haswarning(cab)


def test_belly_warning_2p_nowarn_dia():
    s = Scene()
    s.new_point('p1')
    s.new_point('p2', position = (10,0,0))
    cab = s.new_cable('c1', connections = ['p1', 'p2'], length = 12, mass_per_length=0.1, diameter=0.1,  EA=10000)

    s.update()

    s._save_coredump()

    assert not haswarning(cab)


def test_belly_warning_3p_warn():
    s = Scene()
    s.new_point('p1')
    s.new_point('p2', position=(10, 0, 0))
    s.new_point('p3', position=(5, 0, 0))
    cab = s.new_cable('c1', connections=['p1', 'p3', 'p2'], length=12, mass_per_length=0.1, EA=10000)

    s.update()

    assert haswarning(cab)

    cab.length = 8
    s.update()

    assert not haswarning(cab)

def test_belly_warning_3c_warn():
    s = Scene()
    s.new_point('p1')
    s.new_point('p2', position=(10, 0, 0))
    s.new_point('p3', position=(5, 0, 0))

    # create circles at the points
    s.new_circle('c1', parent='p1', radius=0.1, axis = (0,1,0))
    s.new_circle('c2', parent='p2', radius=0.1, axis = (0,1,0))
    s.new_circle('c3', parent='p3', radius=0.1, axis = (0,1,0))


    cab = s.new_cable('cable', connections=['c1', 'c3', 'c2'], length=12, mass_per_length=0.1, EA=10000)

    s.update()

    assert haswarning(cab)

    cab.length = 8
    s.update()

    assert not haswarning(cab)

def test_belly_warning_3cLoop_warn():
    s = Scene()
    s.new_point('p1')
    s.new_point('p2', position=(10, 0, 0))
    s.new_point('p3', position=(5, 0, 0))

    # create circles at the points
    s.new_circle('c1', parent='p1', radius=0.1, axis = (0,1,0))
    s.new_circle('c2', parent='p2', radius=0.1, axis = (0,1,0))
    s.new_circle('c3', parent='p3', radius=0.1, axis = (0,1,0))


    cab = s.new_cable('cable', connections=['c1', 'c3', 'c2', 'c1'], length=30, mass_per_length=0.1, EA=10000)

    s.update()

    assert haswarning(cab)

    cab.length = 8
    s.update()

    assert not haswarning(cab)

    DG(s)
