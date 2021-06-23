from DAVE import *
from DAVE.io.simplify import *
from numpy.testing import assert_allclose

def test_no_split():
    """Should not do anything"""
    s = Scene()
    s.new_point('A',position = (10,0,0))
    s.new_point('B',position = (-10,0,0))
    s.new_cable('cable','A','B',EA=123)

    names = [node.name for node in s._nodes]
    split_cables(s)
    names2 = [node.name for node in s._nodes]

    assert names == names2

def test_split():
    """Should not do anything"""
    s = Scene()
    s.new_point('A',position = (10,0,0))
    s.new_point('B',position = (-10,0,0))
    s.new_cable('cable','A','A',EA=123, sheaves = ['B'], length=6)

    names = [node.name for node in s._nodes]
    split_cables(s)
    # names2 = [node.name for node in s._nodes]
    #
    # assert names == names2
    assert_allclose(s['cable_part_1'].length, 3)
    assert_allclose(s['cable_part_2'].length, 3)

def test_split_sheave():
    """Should not do anything"""
    s = Scene()
    s.new_point('A',position = (10,0,0))
    s.new_point('B',position = (-10,0,0))
    s.new_circle('S','B',axis=(0,1,0), radius = 2)
    s.new_cable('cable','A','A',EA=123, sheaves = ['S'], length=6)

    names = [node.name for node in s._nodes]
    split_cables(s)
    # names2 = [node.name for node in s._nodes]
    #
    # assert names == names2
    assert_allclose(s['cable_part_1'].length, 3)
    assert_allclose(s['cable_part_2'].length, 3)
