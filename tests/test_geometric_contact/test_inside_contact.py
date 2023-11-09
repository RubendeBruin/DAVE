from numpy.testing import assert_allclose
import pytest

from DAVE import *


def model_inside(swapped=False):
    s = Scene()

    # Exporting Fixed shackle
    # Create Shackle
    sh = s.new_shackle("Fixed shackle", kind="GP500")
    sh.position = (1.5194e-05, -2.25175e-22, 0.185)
    sh.rotation = (-127.279, 127.279, 0.000414929)

    # Exporting Connected Shackle
    # Create Shackle
    sh = s.new_shackle("Connected Shackle", kind="GP500")
    sh.position = (-0, -0, -0.9005)
    sh.rotation = (-0, -0, -0)

    if swapped:

        s.new_geometriccontact(name='Geometric_connection of Connected Shackle/bow on Fixed shackle/inside',
                               parent='Connected Shackle/bow',
                               child='Fixed shackle/inside',
                               inside=True,
                               rotation_on_parent=90,
                               child_rotation=90)

    else:

        s.new_geometriccontact(name='Geometric_connection of Connected Shackle/bow on Fixed shackle/inside',
                               child='Connected Shackle/bow',
                               parent='Fixed shackle/inside',
                               inside=True,
                               rotation_on_parent=90,
                               child_rotation=90)

    s['Fixed shackle/pin_point']._visible = False

    s['Fixed shackle/bow_point']._visible = False

    s['Fixed shackle/inside_circle_center']._visible = False

    s['Connected Shackle/pin_point']._visible = False

    s['Connected Shackle/bow_point']._visible = False

    s['Connected Shackle/inside_circle_center']._visible = False

    return s

def test_fix_inside_contact_1():
    s = model_inside()

    assert_allclose(s['Connected Shackle'].gz, -1.266)

    s.solve_statics()

    # s._check_and_fix_geometric_contact_orientations()

    assert_allclose(s['Connected Shackle'].gz,-1.4359999999587405)

# def test_fix_inside_contact_2():
#     s = model_inside(swapped=True)
#
#     assert_allclose(s['Connected Shackle'].gz, -1.266)
#
#     s.solve_statics()
#
#     # s._check_and_fix_geometric_contact_orientations()
#
#     assert_allclose(s['Connected Shackle'].gz,-1.4359999999587405)
#
#
# if __name__ == "__main__":
#     s = model_inside(swapped=True)
#
#     s.print_node_tree()
#
#     from DAVE.gui import Gui
#
#     Gui(s)
