import pytest
from DAVE.nds.base import NodeSingleton, RigidBodyContainer, RigidBodyContainerMassReadOnly
from DAVE import Scene, RigidBody

def test_node_singleton_initialization():
    scene = Scene()
    node = NodeSingleton(scene, "singleton_node")
    assert node.name == "singleton_node"
    assert node._scene == scene

def test_node_singleton_overwrite_existing():
    scene = Scene()
    existing_node = NodeSingleton(scene, "singleton_node")
    scene._nodes.append(existing_node)
    new_node = NodeSingleton(scene, "singleton_node")
    assert new_node.name == "singleton_node"
    assert new_node._scene == scene
    assert existing_node not in scene._nodes

def test_node_singleton_name_conflict():
    scene = Scene()
    NodeSingleton(scene, "singleton_node")
    NodeSingleton(scene, "singleton_node")

    assert len(scene._nodes) == 1

def test_rigid_body_container_initialization():
    scene = Scene()
    node = RigidBodyContainer(scene, "rigid_body_container")
    assert node.name == "rigid_body_container"
    assert node._scene == scene

def test_rigid_body_container_dissolve():
    scene = Scene()
    node = RigidBodyContainer(scene, "rigid_body_container")
    node.dissolve()
    assert isinstance(node, RigidBody)

def test_rigid_body_container_mass_read_only_properties():
    scene = Scene()
    node = RigidBodyContainerMassReadOnly(scene, "rigid_body_container_mass_read_only")
    assert node.mass is not None
    assert node.inertia is not None
    assert node.cogx is not None
    assert node.cogy is not None
    assert node.cogz is not None
    assert node.cog is not None
    assert node.inertia_radii is not None
    assert node.inertia_position is not None

def test_rigid_body_container_mass_read_only_setter():
    scene = Scene()
    node = RigidBodyContainerMassReadOnly(scene, "rigid_body_container_mass_read_only")
    with pytest.raises(AttributeError):
        node.mass = 10
    with pytest.raises(AttributeError):
        node.inertia = 10
    with pytest.raises(AttributeError):
        node.cogx = 10
    with pytest.raises(AttributeError):
        node.cogy = 10
    with pytest.raises(AttributeError):
        node.cogz = 10
    with pytest.raises(AttributeError):
        node.cog = (10, 10, 10)
    with pytest.raises(AttributeError):
        node.inertia_radii = (10, 10, 10)
    with pytest.raises(AttributeError):
        node.inertia_position = (10, 10, 10)

