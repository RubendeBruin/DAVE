"""Overriding the `is_property_change_allowed` method in a manager class enables a finer control
of permitted changes to properties of nodes in the manager.

This is used in GeometricContact for example to prevent position, rotation, parent and name changes
in the managed connected frame. All other changes are allowed.
"""
import pytest

from DAVE import *

def model():
    s = Scene()

    s.new_frame(name='Frame')
    point = s.new_point(name='Point', parent='Frame')
    s.new_circle(name='Circle', parent=point, axis=(0, 1, 0), radius=1)
    s.new_rigidbody(name='Body')
    point = s.new_point(name='Point2', parent='Body')
    s.new_circle(name='Circle2', parent=point, axis=(0, 1, 0), radius=1)

    s['Circle2'].radius = 0.4

    s['Body'].mass = 2.0

    s['Body'].cog = (0.0, 0.0, 3.0)
    s.new_geometriccontact('Geometric_connection of Circle2 on Circle', 'Circle2', 'Circle')

    s['Geometric_connection of Circle2 on Circle'].inside = True

    s.solve_statics()

    return s

def test_mass_change_allowed():
    s = model()
    s['Geometric_connection of Circle2 on Circle/Body'].mass = 3.0
    assert s['Geometric_connection of Circle2 on Circle/Body'].mass == 3.0

def test_name_change_not_allowed():
    s = model()
    node = s['Geometric_connection of Circle2 on Circle/Body']
    with pytest.raises(ValueError):
        node.name = 'NewName'

def test_position_change_not_allowed():
    s = model()
    node = s['Geometric_connection of Circle2 on Circle/Body']
    with pytest.raises(ValueError):
        node.position = (1,2,3)


def test_mass_change_not_allowed_when_in_component(tmp_path):
    s = model()
    component_path = tmp_path / 'component.dave'
    s.save_scene(str(component_path))

    s2 = Scene()
    s2.new_component(name='Component', path=str(component_path))

    s2.print_node_tree()

    node = s2['Component/Geometric_connection of Circle2 on Circle/Body']

    with pytest.raises(ValueError):
        node.mass = 3.0


if __name__ == '__main__':
    s = model()
    DG(s)
    s.print_node_tree()
