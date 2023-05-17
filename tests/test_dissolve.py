"""
Dissolving:
- Calling dissolve tries to unpack the scene as much as possible.
- The function returns True and if work was done
- The function returns False and a message if no work was done. The message specifies why no work was done and is for the user.

Dissolving a Frame or derived may need to alter its dependants:
- children need to be reparented
- beams and springs need to have their end points repointed. This is only possible if the new parent is at the same global location and orientation as the old parent.

Should this logic be implemented in Frame, Scene or in the spring elements themselves?

Implementing in the spring elements is the most future proof:
    if node.depends_on(self):
        node.try_swap(self, new)

Both "try-swap" and "dissolve" are implemented in all sub-classes of Node and called via super().
For frames, points, etc try-swap simply calls change_parent_to on the node. So implemented in HasParentXXX


"""
import pytest
from numpy.testing import assert_almost_equal

from DAVE import *

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

def test_dissolve_frame():
    s = Scene()
    f = s.new_frame('f')
    f2 = s.new_frame('f2', parent=f)
    p = s.new_point('p', parent=f2)

    c = s.new_circle('c', parent=p, axis=(0,1,0))

    done, why = f2.dissolve()
    assert done
    assert p.parent == f

def test_dissolve_frame2():
    s = Scene()
    f = s.new_frame('f')
    f2 = s.new_frame('f2', parent=f, fixed = (True, True, True, True, True, False))
    p = s.new_point('p', parent=f2)

    c = s.new_circle('c', parent=p, axis=(0,1,0))

    done, why = f2.dissolve()
    assert why
    assert p.parent == f2
    assert not done

def test_dissolve_RB():
    s = Scene()
    f = s.new_frame('f')
    f2 = s.new_rigidbody('f2', parent=f)
    p = s.new_point('p', parent=f2)

    c = s.new_circle('c', parent=p, axis=(0,1,0))

    done, why = f2.dissolve()
    assert done
    assert p.parent == f


def test_dissolve_RB2():
    s = Scene()
    f = s.new_frame('f')
    f2 = s.new_rigidbody('f2', parent=f, mass=10)
    p = s.new_point('p', parent=f2)

    c = s.new_circle('c', parent=p, axis=(0,1,0))

    done, why = f2.dissolve()
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

def test_dissolve_shackle():
    s = Scene()
    sh = s.new_shackle('sh', kind = "GP300")
    work_done, msg = sh.dissolve()
    assert work_done

====================================================================================
 Dissolve as it is implemented now should actually be called "Simplify"

Dissolving should simplify as much as possible and then delete the node if possible
=====================================================================================