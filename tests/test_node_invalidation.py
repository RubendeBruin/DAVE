import pytest

from DAVE import *

def test_node_invalidation():
    s = Scene()
    t1 = s.new_point('test')
    assert t1 == s['test']

    assert t1.is_valid

    s.delete('test')

    assert t1.is_valid == False

    t2 = s.new_point('test')
    assert t2 == s['test']

def test_node_invalidation_child():
    s = Scene()
    t1 = s.new_point('test')
    f = s.new_frame('frame')
    t1.parent = f
    assert t1 == s['test']

    assert t1.is_valid

    s.delete('frame')

    assert t1.is_valid == False

    t2 = s.new_point('test')
    assert t2 == s['test']

def test_node_invalidation_and_lookup():

    names = [f'frame{i}' for i in range(100)]

    s = Scene()
    nodes =dict()

    for name in names:
        nodes[name] = s.new_frame(name)

    for name in names:
        assert nodes[name] == s[name]

    to_be_deleted = [f'frame{i+20}' for i in range(30)]

    for dname in to_be_deleted:
        s.delete(dname)

        for name in names:
            if name not in to_be_deleted:
                assert nodes[name] == s[name]

    for dname in to_be_deleted:
        with pytest.raises(ValueError):
            assert s.node_by_name(dname, silent=True)
