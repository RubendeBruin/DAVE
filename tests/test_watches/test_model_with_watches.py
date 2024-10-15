from DAVE import *

def test_watches():

    s = Scene()
    p = s.new_point('Point')
    s.try_add_watch('Point', 'x')
    s.try_add_watch(p, 'x')
    s.try_add_watch('does not exist', 'x')
    s.try_add_watch('Point', 'does not exist')

    nodes, props, values, docs = s.evaluate_watches()

    assert len(props) == 1
    assert props[0] == 'x'
    assert values[0] == 0
    assert docs[0].units == '[m]'

    s2 = s.copy()

    s.try_delete_watch('Point', 'x')

    nodes, props, values, units = s.evaluate_watches()
    assert len(props) == 0


    nodes, props, values, docs = s2.evaluate_watches()

    assert len(props) == 1
    assert props[0] == 'x'
    assert values[0] == 0
    assert docs[0].units == '[m]'

    s2.delete('Point')
    nodes, props, values, units = s2.evaluate_watches()
    assert len(props) == 0

def test_watches_only_single_numeric():
    s = Scene()
    p = s.new_point('Point')
    s.try_add_watch('Point', 'applied_force')
    s.try_add_watch('Point', 'x')

    nodes, props, values, units = s.evaluate_watches()
    assert len(props) == 1

