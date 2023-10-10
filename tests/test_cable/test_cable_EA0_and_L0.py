"""L may be 0 if EA = 0"""
import pytest

from DAVE import *

def test_L0_EA0():
    s = Scene()
    s.new_point(name="p1", position=(-10, 0, 0))
    s.new_point(name="p2", position=(10, 0, 0))
    c = s.new_cable(name="cable", connections=["p1", "p2"], EA=1e6, length=20)

    c.EA = 0
    c.length = 0

    s._save_coredump()

    s.update()

def test_Llt0_EA0():
    s = Scene()
    s.new_point(name="p1", position=(-10, 0, 0))
    s.new_point(name="p2", position=(10, 0, 0))
    c = s.new_cable(name="cable", connections=["p1", "p2"], EA=0, length=0)

    with pytest.raises(ValueError):
        c.length = -1

def test_Llt0_EA0_make():
    s = Scene()
    s.new_point(name="p1", position=(-10, 0, 0))
    s.new_point(name="p2", position=(10, 0, 0))

    with pytest.raises(ValueError):
        c = s.new_cable(name="cable", connections=["p1", "p2"], EA=0, length=-1)

def test_L0_EA1():
    s = Scene()
    s.new_point(name="p1", position=(-10, 0, 0))
    s.new_point(name="p2", position=(10, 0, 0))
    c = s.new_cable(name="cable", connections=["p1", "p2"], EA=1e6, length=20)

    c.EA = 1

    with pytest.raises(ValueError):
        c.length = 0

def test_L0_EA_set_EA():
    s = Scene()
    s.new_point(name="p1", position=(-10, 0, 0))
    s.new_point(name="p2", position=(10, 0, 0))
    c = s.new_cable(name="cable", connections=["p1", "p2"], EA=0, length=0)

    with pytest.raises(ValueError):
        c.EA = 1

