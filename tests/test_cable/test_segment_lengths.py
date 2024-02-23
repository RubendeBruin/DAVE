from numpy.testing import assert_allclose

from DAVE import *


def test_pbp():

    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_point(name='b', position=(0, 0, 2))
    s.new_circle(name='bar', parent='b', radius=1.2, axis=(0, 1, 0), roundbar=True)

    c = s.new_cable(connections=['p1', 'bar', 'p2'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.segment_lengths)

    expected = (0.0, 9.639805163278426, 0.7203896734431466, 9.639805163278426)
    assert_allclose(c.segment_lengths, expected, rtol=1e-6)

def test_pbp_loop():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_point(name='b', position=(0, 0, 2))
    s.new_circle(name='bar', parent='b', radius=1.2, axis=(0, 1, 0), roundbar=True)

    c = s.new_cable(connections=['p1', 'bar', 'p2', 'p1'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.segment_lengths)

    expected = (0.0, 4.938744756838719, 0.3690759991862853, 4.938744756838719, 9.753434487136277)
    assert_allclose(c.segment_lengths, expected, rtol=1e-6)

def test_cpc_loop_length_on_circle():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_circle(name='c', parent='p2', radius=1.2, axis=(0, 1, 0))
    s.new_point(name='b', position=(0, 0, 2))
    s.new_circle(name='bar', parent='b', radius=1.2, axis=(0, 1, 0), roundbar=True)

    c = s.new_cable(connections=['c', 'bar', 'p1', 'c'], name='cable', EA=1e6, length=20)
    s.update()
    print(c.segment_lengths)

    expected = (1.785504, 9.107248, 9.107248)
    assert_allclose(c.segment_lengths, expected, rtol=1e-6)


def test_cpcbc_loop():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(10, 0, 0))
    s.new_circle(name='c', parent='p2', radius=1.2, axis=(0, 1, 0))
    s.new_point(name='b', position=(0, 0, -3))
    s.new_circle(name='bar', parent='b', radius=1.2, axis=(0, 1, 0), roundbar=True)

    c = s.new_cable(connections=['c', 'bar', 'p1', 'c'], name='cable', EA=1e6, length=20)
    s.update()

    expected = (1.548467, 4.629301, 0.371455, 4.598621, 8.852156)
    assert_allclose(c.segment_lengths, expected, rtol=1e-5)

