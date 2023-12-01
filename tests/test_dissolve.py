"""
Dissolving:
- Calling dissolve tries to unpack the scene as much as possible.
- The function returns True and if work was done
- The function returns False and a message if no work was done. The message specifies why no work was done and is for the user.

Dissolving a Frame or derived may need to alter its dependants:
- children need to be re-parented
- beams and springs need to have their end points repointed. This is only possible if the new parent is at the same global location and orientation as the old parent.

This is implemented on node-level using the try_swap method:

    if node.depends_on(self):
        node.try_swap(self, new)

Both "try-swap" and "dissolve" are implemented in all sub-classes of Node and called via super().
For frames, points, etc try-swap simply calls change_parent_to on the node. So implemented in HasParentXXX


"""
import pytest
from numpy.testing import assert_almost_equal, assert_allclose

from DAVE import *
from DAVE.nodes import HasContainer

def test_swap():
    s = Scene()
    f = s.new_frame('f')
    p = s.new_point('p', parent = f)
    f2 = s.new_frame('f2')
    assert p.try_swap(f, f2)

    assert p.parent == f2

    p.manager = "Managed"

    with pytest.raises(Exception):
        p.try_swap(f2, f)


def test_swap_maintain_global_position():
    s = Scene()
    f = s.new_frame('f')
    p = s.new_point('p', parent = f)
    f2 = s.new_frame('f2', position=(1,2,3), rotation=(10,20,90))
    assert p.try_swap(f, f2)
    assert p.parent == f2

    assert_almost_equal(p.global_position, (0,0,0))


def test_swap_circle():
    s = Scene()
    f = s.new_frame('f')
    p = s.new_point('p', parent=f)
    c = s.new_circle('c', parent=p, axis=(0,1,0))

    p2 = s.new_point('p2', parent=f)

    assert c.try_swap(p, p2)
    assert c.parent == p2

def test_swap_circle2():
    s = Scene()
    f = s.new_frame('f')
    p = s.new_point('p', parent=f)
    c = s.new_circle('c', parent=p, axis=(0,1,0))

    p2 = s.new_point('p2', parent=f, position = (0,0,1))

    assert c.try_swap(p, p2) == False  # can not swap because position is different
    assert c.parent == p

def test_dissolvesome_frame():
    s = Scene()
    f = s.new_frame('f')
    f2 = s.new_frame('f2', parent=f)
    p = s.new_point('p', parent=f2)

    c = s.new_circle('c', parent=p, axis=(0,1,0))

    done, why = f2.dissolve_some()
    assert done
    assert p.parent == f

def test_dissolve_frame():
    s = Scene()
    f = s.new_frame('f')
    f2 = s.new_frame('f2', parent=f)
    p = s.new_point('p', parent=f2)

    c = s.new_circle('c', parent=p, axis=(0,1,0))

    f2.dissolve()
    assert p.parent == f

    assert f2 not in s._nodes

def test_dissolve_rigidbody_zero_mass():
    s = Scene()
    rb = s.new_rigidbody('rb', mass=0)
    p = s.new_point('p', parent=rb)

    rb.dissolve()
    assert p.parent == None
    assert rb not in s._nodes

def test_dissolvesome_rigidbody_non_zero_mass():
    s = Scene()
    rb = s.new_rigidbody('rb', mass=10)
    p = s.new_point('p', parent=rb)

    rb.dissolve_some()

    assert p.parent == None
    assert rb in s._nodes

    assert getattr(rb, '_partially_dissolved', False) == False  # should not be marked as partially dissolved because it is not troublesome.


def test_dissolve_rigidbody_non_zero_mass():
    s = Scene()
    rb = s.new_rigidbody('rb', mass=10)
    p = s.new_point('p', parent=rb)

    with pytest.raises(Exception):
        rb.dissolve()


def test_dissolve_frame2():
    s = Scene()
    f = s.new_frame('f')
    f2 = s.new_frame('f2', parent=f, fixed = (True, True, True, True, True, False))
    p = s.new_point('p', parent=f2)

    c = s.new_circle('c', parent=p, axis=(0,1,0))

    done, why = f2.dissolve_some()
    assert why
    assert p.parent == f2
    assert not done

def test_dissolve_RB():
    s = Scene()
    f = s.new_frame('f')
    f2 = s.new_rigidbody('f2', parent=f)
    p = s.new_point('p', parent=f2)

    c = s.new_circle('c', parent=p, axis=(0,1,0))

    done, why = f2.dissolve_some()
    assert done
    assert p.parent == f


def test_dissolve_RB2():
    s = Scene()
    f = s.new_frame('f')
    f2 = s.new_rigidbody('f2', parent=f, mass=10)
    p = s.new_point('p', parent=f2)

    c = s.new_circle('c', parent=p, axis=(0,1,0))

    done, why = f2.dissolve_some()
    assert why
    assert p.parent == f
    assert done

def test_flatten():
    s = Scene()
    f = s.new_frame('f')
    f2 = s.new_frame('f2', parent=f)

    s.flatten()

    assert len(s._nodes) == 0

def test_flatten2():
    # f has dofs, but nothing is on f, so it can be removed
    s = Scene()
    f = s.new_frame('f', fixed=(True, True, True, True, True, False))
    f2 = s.new_frame('f2', parent=f)

    s.flatten()

    assert len(s._nodes) == 0

def test_dissolve_some_shackle():
    s = Scene()
    sh = s.new_shackle('sh', kind = "GP300")
    work_done, msg = sh.dissolve_some()
    assert work_done

def test_dissolve_shackle():
    s = Scene()
    sh = s.new_shackle('sh', kind = "GP300")
    sh.dissolve()

    assert isinstance(sh, RigidBody)
    assert not isinstance(sh, HasContainer)

    with pytest.raises(Exception):
        sh.dissolve() # still has mass

    sh.mass = 0
    sh.dissolve()

    assert sh not in s._nodes

def test_dissolve_component():
    s = Scene()
    c = s.new_component('c', path = 'res: default_component.dave')

    c.dissolve()  # first dissolve turn the component into a frame

    assert isinstance(c, Frame)
    assert not isinstance(c, Component)

    assert s['c/Frame'].parent == c

    assert c in s._nodes

    c.dissolve()   # second dissolve removes the frame
    assert c not in s._nodes

def test_dissolve_component_cheetah():
    s = Scene()
    c = s.new_component('c', path = 'res: cheetah.dave')

    c.dissolve()  # first dissolve turn the component into a frame
    c.dissolve()  # second dissolve removes the frame itself

def test_dissolve_component_cheetah():
    s = Scene()
    c = s.new_component('c', path = 'res: cheetah.dave')

    s.dissolve('c')

def gimme():
    s = Scene()

    # auto generated python code
    # By beneden
    # Time: 2023-05-19 11:47:34 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution

    def solved(number):
        return number

    # Environment settings
    s.g = 9.80665
    s.waterlevel = 0.0
    s.rho_air = 0.00126
    s.rho_water = 1.025
    s.wind_direction = 0.0
    s.wind_velocity = 0.0
    s.current_direction = 0.0
    s.current_velocity = 0.0

    # code for Frame
    s.new_frame(name='Frame',
                position=(0,
                          0,
                          0),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True))

    # code for Frame_1
    s.new_frame(name='Frame_1',
                position=(6.971,
                          6.688,
                          -0.567),
                rotation=(0,
                          0,
                          0),
                fixed=(True, True, True, True, True, True))

    # code for Component
    c = s.new_component(name='Component',
                        path=r'res: default_component.dave',
                        position=(0,
                                  15,
                                  0),
                        rotation=(0,
                                  0,
                                  0),
                        fixed=(True, True, True, True, True, True))



    # code for Point
    s.new_point(name='Point',
                parent='Frame_1',
                position=(0,
                          0,
                          0))

    # code for Point_1
    s.new_point(name='Point_1',
                parent='Frame',
                position=(0,
                          0,
                          0))

    # code for Con2d_Component/Frame_to_Frame
    s.new_connector2d(name='Con2d_Component/Frame_to_Frame',
                      nodeA='Frame',
                      nodeB='Component/Frame',
                      k_linear=0,
                      k_angular=0)

    # code for Circle
    s.new_circle(name='Circle',
                 parent='Point',
                 axis=(0, 1, 0),
                 radius=1)

    # code for Circle_1
    s.new_circle(name='Circle_1',
                 parent='Point_1',
                 axis=(0, 1, 0),
                 radius=1)

    # code for Point_2
    s.new_point(name='Point_2',
                parent='Component/Frame',
                position=(0,
                          0,
                          0))

    # code for Circle_2
    s.new_circle(name='Circle_2',
                 parent='Point_2',
                 axis=(0, 1, 0),
                 radius=1)

    # # Exporting Sling
    # # Create sling
    # sl = s.new_sling("Sling", length=20,
    #                  LeyeA=1.81051,
    #                  LeyeB=1.81051,
    #                  LspliceA=1.81051,
    #                  LspliceB=1.81051,
    #                  diameter=0.1,
    #                  EA=1,
    #                  mass=0.1,
    #                  endA="Circle_2",
    #                  endB="Circle",
    #                  sheaves=None)

    s.new_frame("Target_for_connector", position = (1,2,3))

    # code for Con6d_Sling/spliceB2_to_Component
    s.new_linear_connector_6d(name='Con6d_Sling/spliceB2_to_Component',
                              main='Target_for_connector',
                              secondary='Component/Frame',
                              stiffness=(0, 0, 0,
                                         0, 0, 0))

    return s

def test_scene_copy():
    s = gimme()
    s2 = s.copy()  # fails if dependancies are not correctly ordered

def test_testscene_flatten():

    s = gimme()
    s.flatten()

    assert s['Con6d_Sling/spliceB2_to_Component']


def test_testscene_dissolves():
    s = gimme()

    # DG(s)


    s6d =  s['Con6d_Sling/spliceB2_to_Component']

    com = s['Component']
    com.dissolve()

    assert com in s._nodes

    # with pytest.raises(Exception):
    com.dissolve()  # LC6D can not be relocated because frame is at a different location than None

    assert not isinstance(com, Component)

    with pytest.raises(Exception):
        s.dissolve('Frame')  # Same for Frame

    s.dissolve('Frame_1')

    s.flatten()

def test_testscene_flatten():
    s = gimme()

    f = s['Frame']
    refpos = f.global_position
    refrot = f.global_rotation

    assert 'Component' in s.node_names

    s.flatten()

    assert len(s._nodes) == 12

    assert 'Component' not in s.node_names


    # assert not isinstance(s['Component'], Component) # should be a frame now

    assert_allclose(s['Frame'].global_position, refpos)
    assert_allclose(s['Frame'].global_rotation, refrot)





def test_testscene_flatten_with_component_position_changed():
    s = gimme()
    s['Component'].position = (0,0,0)
    s['Component'].fixed_x = False

    s.flatten()
    assert not isinstance(s['Component'], Component) # should be a frame now and should still be here


def test_testscene_dissolves_with_component_position_changed_and_intermediate_frame_added():
    s = gimme()
    f3 = s.new_frame('f3', position=s['Component'].position)
    com = s['Component']
    com.parent = f3
    com.position = (0, 0, 0)

    com.dissolve()
    com.dissolve()
    #
    # from DAVE.gui import Gui
    # Gui(s)

    assert com not in s._nodes  # should be a frame now and should still be here

def test_dissolve_geometric_contact():
    s = Scene()
    sh1 = s.new_shackle('sh1')
    sh2 = s.new_shackle('sh2')

    gc = s.new_geometriccontact('gc', sh1.pin, sh2.bow)

    gc.dissolve()

    assert sh1.depends_on() == [s['gc/_axis_on_child']]
    s.sort_nodes_by_dependency()
    s.print_node_tree()

def test_flatten_geometric_contact():
    s = Scene()
    sh1 = s.new_shackle('sh1')
    sh2 = s.new_shackle('sh2')
    gc = s.new_geometriccontact('gc', sh1.pin, sh2.bow)

    s.flatten()

    s.print_node_tree(more=True)


def test_dissolve_rigidbodycontainer():
    """Dissolving an Node that derives from both Frame and Manager is always possible as the management can be voided.
    Dissolving
    """

    s = Scene()
    sh1 = s.new_shackle('sh1')
    sh1.fixed = False
    s.dissolve(sh1)

    s.print_node_tree()




