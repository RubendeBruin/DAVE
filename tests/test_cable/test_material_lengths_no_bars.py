import numpy as np
from numpy.testing import assert_allclose

from DAVE import *

def test_pp_stretched():
    """10m material length stretched to 20m"""
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))

    c = s.new_cable(connections=['p1', 'p2'], name='cable', EA=1e6, length=10)
    s.update()
    print(c.material_lengths)

    expected = (10.0,)
    assert_allclose(c.material_lengths, expected, rtol=1e-6)

def test_cc_loop_stretched():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_circle(name='c1', parent='p1', radius=1.2, axis=(0, 1, 0))
    s.new_circle(name='c2', parent='p2', radius=1.2, axis=(0, 1, 0))

    c = s.new_cable(connections=['c1', 'c2', 'c1'], name='cable', EA=1e6, length=10)
    s.update()
    print(c.material_lengths_no_bars)

    total = sum(c.material_lengths_no_bars)
    assert_allclose(total, 10.0, rtol=1e-6)


def test_pp():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))

    c = s.new_cable(connections=['p1', 'p2'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.material_lengths)

    expected = (20.0,)
    assert_allclose(c.material_lengths, expected, rtol=1e-6)

def test_pp_no_bars():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))

    c = s.new_cable(connections=['p1', 'p2'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.material_lengths_no_bars)

    expected = (20.0,)
    assert_allclose(c.material_lengths_no_bars, expected, rtol=1e-6)

def test_pp_cat():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))

    c = s.new_cable(connections=['p1', 'p2'], name='cable', EA=1e6, length=30)
    s.update()
    expected = (30.0,)
    assert_allclose(c.material_lengths_no_bars, expected, rtol=1e-6)

def test_ppp_cat():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(0, 0, 0))
    s.new_point(name='p3', position=(10, 0, 0))

    c = s.new_cable(connections=['p1', 'p2','p3'], name='cable', EA=1e6, length=30)
    s.update()
    print(c.material_lengths_no_bars)

    expected = (15.0, 15.0)
    assert_allclose(c.material_lengths_no_bars, expected, rtol=1e-6)

def test_pp_EA0():
    s = Scene()
    p1 = s.new_point("p1", position=(0, 0, 0))
    p2 = s.new_point("p2", position=(1, 0, 10))
    c = s.new_cable("cable", p1, p2, EA=0, length=7)

    s.update()

    expected = (np.sqrt(101.0))
    assert_allclose(c.material_lengths_no_bars, expected, rtol=1e-6)



def test_pbp():

    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_point(name='b', position=(0, 0, 2))
    s.new_circle(name='bar', parent='b', radius=1.2, axis=(0, 1, 0), roundbar=True)

    c = s.new_cable(connections=['p1', 'bar', 'p2'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.material_lengths_no_bars)

    expected = (20,)
    assert_allclose(c.material_lengths_no_bars, expected, rtol=1e-6)

def test_pbp_loop():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_point(name='b', position=(0, 0, 2))
    s.new_circle(name='bar', parent='b', radius=1.2, axis=(0, 1, 0), roundbar=True)

    c = s.new_cable(connections=['p1', 'bar', 'p2', 'p1'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.material_lengths_no_bars)

    expected = [10.246566,  9.753434]
    assert_allclose(c.material_lengths_no_bars, expected, rtol=1e-6)

def test_cpc_loop_length_on_circle_bar_not_active():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_circle(name='c', parent='p2', radius=1.2, axis=(0, 1, 0))
    s.new_point(name='b', position=(0, 0, 2))
    s.new_circle(name='bar', parent='b', radius=1.2, axis=(0, 1, 0), roundbar=True)

    c = s.new_cable(connections=['c', 'bar', 'p1', 'c'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.material_lengths_no_bars)

    #           circle     free      free
    expected = (1.785504, 9.107248, 9.107248)

    assert len(c.material_lengths_no_bars) == 3
    assert_allclose(c.material_lengths_no_bars, expected, rtol=1e-6)
    assert sum(expected) == c.length
    assert expected[1] == expected[2]

    # DG(s)


def test_cpc_loop_length_on_circle_bar_active():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_circle(name='c', parent='p2', radius=1.2, axis=(0, 1, 0))
    s.new_point(name='b', position=(0, 0, -3))
    s.new_circle(name='bar', parent='b', radius=1.2, axis=(0, 1, 0), roundbar=True)

    c = s.new_cable(connections=['c', 'bar', 'p1', 'c'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.material_lengths_no_bars)

    expected = [1.548467, 9.599377, 8.852156]
    assert len(c.material_lengths_no_bars) == 3
    assert_allclose(c.material_lengths_no_bars, expected, rtol=1e-6)

def test_cc():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_circle(name='c1', parent='p1', radius=1.2, axis=(0, 1, 0))
    s.new_circle(name='c2', parent='p2', radius=1.2, axis=(0, 1, 0))

    c = s.new_cable(connections=['c1', 'c2'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.material_lengths_no_bars)

    expected = (20.0,)
    assert_allclose(c.material_lengths_no_bars, expected, rtol=1e-6)

def test_cc_loop():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_circle(name='c1', parent='p1', radius=1.2, axis=(0, 1, 0))
    s.new_circle(name='c2', parent='p2', radius=1.2, axis=(0, 1, 0))

    c = s.new_cable(connections=['c1', 'c2', 'c1'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.material_lengths_no_bars)

    expected = (1.586056, 8.413944, 1.586056, 8.413944)
    assert_allclose(c.material_lengths_no_bars, expected, rtol=1e-6)

def test_cbc_active():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_circle(name='c1', parent='p1', radius=1.2, axis=(0, 1, 0))
    s.new_circle(name='c2', parent='p2', radius=1.2, axis=(0, 1, 0))
    s.new_point(name='b', position=(0, 0, 2))
    s.new_circle(name='bar', parent='b', radius=1.2, axis=(0, 1, 0), roundbar=True)

    c = s.new_cable(connections=['c1', 'bar', 'c2'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.material_lengths_no_bars)

    expected = (20)
    assert_allclose(c.material_lengths_no_bars, expected, rtol=1e-6)

def test_ccc():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(0, 0, 1))
    s.new_point(name='p3', position=(10, 0, 0))
    s.new_circle(name='c1', parent='p1', radius=1.2, axis=(0, 1, 0))
    s.new_circle(name='c2', parent='p2', radius=1.2, axis=(0, 1, 0))
    s.new_circle(name='c3', parent='p3', radius=1.2, axis=(0, 1, 0))

    c = s.new_cable(connections=['c1', 'c2', 'c3'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.material_lengths_no_bars)

    expected = (9.882391, 0.235218, 9.882391)
    assert_allclose(c.material_lengths_no_bars, expected, atol=1e-6)

def test_ccc_loop():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(0, 0, 1))
    s.new_point(name='p3', position=(10, 0, 0))
    s.new_circle(name='c1', parent='p1', radius=1.2, axis=(0, 1, 0))
    s.new_circle(name='c2', parent='p2', radius=1.2, axis=(0, 1, 0))
    s.new_circle(name='c3', parent='p3', radius=1.2, axis=(0, 1, 0))

    c = s.new_cable(connections=['c1', 'c2', 'c3', 'c1'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.material_lengths_no_bars)

    expected = [1.532469, 4.219129, 0.100423, 4.219129, 1.532524, 8.396326]
    assert_allclose(c.material_lengths_no_bars, expected, atol=1e-6)

