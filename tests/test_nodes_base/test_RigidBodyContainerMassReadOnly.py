import pytest
from numpy.testing import assert_allclose

from DAVE import Scene, RigidBodyContainerMassReadOnly


def test_issue_readonly_protection_doc():
    s = Scene()
    sh = RigidBodyContainerMassReadOnly(s, name="RB")
    props = s.give_properties_for_node(sh, settable=True)

    # Check that the properties are not settable
    protected_attrs = [
        "mass",
        "inertia",
        "cogx",
        "cogy",
        "cogz",
        "cog",
        "inertia_radii",
        "inertia_position",
    ]

    for attr in protected_attrs:
        assert attr not in props


def test_issue_readonly_protection():
    s = Scene()
    sh = RigidBodyContainerMassReadOnly(s, name="RB")

    # Check that the properties are not settable
    protected_attrs = [
        "mass",
        "inertia",
        "cogx",
        "cogy",
        "cogz",
        "cog",
        "inertia_radii",
        "inertia_position",
    ]

    for attr in protected_attrs:
        with pytest.raises(AttributeError):
            setattr(sh, attr, 0.01)

def test_mass_setters_workaround_for_derived_classes():
    s = Scene()
    sh = RigidBodyContainerMassReadOnly(s, name="Shackle")

    # Check that the properties are not settable
    protected_attrs = [
        "mass",
        "inertia",
        "cogx",
        "cogy",
        "cogz",
        "cog",
        "inertia_radii",
        "inertia_position",
    ]

    # single props
    sh._set_mass(1)
    assert sh.mass == 1

    sh._set_inertia(2)
    assert sh.inertia == 2

    sh._set_cog_x(1)
    assert sh.cogx == 1

    sh._set_cog_y(2)
    assert sh.cogy == 2

    sh._set_cog_z(3)
    assert sh.cogz == 3

    assert sh.cog == (1,2,3)



    # vector props
    sh._set_cog((1,2,3))
    assert_allclose(sh.cog, (1,2,3))
    assert_allclose(sh.inertia_position , (1,2,3))

    sh._set_inertia_radii((1,2,2.1))
    assert_allclose(sh.inertia_radii , (1,2,2.1))
    assert_allclose(sh.inertia_position, (1, 2, 3))

