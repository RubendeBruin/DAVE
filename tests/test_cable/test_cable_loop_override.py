"""In some very specific cases we need to have a cable that starts and ends at the same point, but is not a loop

Most notably when using the mean sling model from the rigging package.
"""

from DAVE import *

def test_cable_loop_override():
    s = Scene()
    p1 = s.new_point(name="p1", position=(0, 0, 0))
    p2 = s.new_point(name="p2", position=(1, 0, 0))
    cab = s.new_cable(name="cable", connections = [p1,p2,p1])

    assert cab._isloop

    cab._set_no_loop()

    assert not cab._isloop

    s2 = s.copy()
    cab2 = s2["cable"]
    assert not cab2._isloop

def test_compare_with_normal_nonloop2p():
    s = Scene()
    p1 = s.new_point(name="p1", position=(0, 0, 0))
    p2 = s.new_point(name="p2", position=(1, 0, 0))
    p1copy = s.new_point(name="p1copy", position=(0, 0, 0))

    cab_explicit = s.new_cable(name="cable", connections=[p1, p2, p1])
    cab_normal = s.new_cable(name="cable_normal", connections=[p1, p2, p1copy])

    cab_explicit._set_no_loop()

    s.update()

    # all properties of the two cables should now be exactly the same, except for the endpoint
    assert cab_explicit._isloop == cab_normal._isloop

    # loop over all properties

    for key, value in cab_explicit.__dict__.items():
        if key in ("endB", "_pois","_vfNode"):
            continue

        print("comparing", key, value, ' =?= ' , getattr(cab_normal, key))

        assert value == getattr(cab_normal, key)

def test_compare_with_normal_nonloop3p():
    s = Scene()
    p1 = s.new_point(name="p1", position=(0, 0, 0))
    p2 = s.new_point(name="p2", position=(1, 0, 0))
    p3 = s.new_point(name="p3", position=(1, 1, 0))
    c3 = s.new_circle(name="c3", parent=p1, axis=(0, 1, 0), radius=0.1)
    p1copy = s.new_point(name="p1copy", position=(0, 0, 0))

    cab_explicit = s.new_cable(name="cable", connections=[p1, p2, c3, p1])
    cab_normal = s.new_cable(name="cable_normal", connections=[p1, p2, c3, p1copy])

    cab_explicit._set_no_loop()

    s.update()

    # all properties of the two cables should now be exactly the same, except for the endpoint
    assert cab_explicit._isloop == cab_normal._isloop

    # loop over all properties

    for key, value in cab_explicit.__dict__.items():
        if key in ("endB", "_pois","_vfNode"):
            continue

        print("comparing", key, value, ' =?= ' , getattr(cab_normal, key))

        assert value == getattr(cab_normal, key)