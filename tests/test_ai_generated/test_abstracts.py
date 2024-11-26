import pytest
from DAVE.nds.abstracts import NodePurePython, NodeCoreConnected, DAVENodeBase

class MockScene:

    def __init__(self):
        self._godmode = False

    def add_node(self, node):
        pass

    def _verify_name_available(self, name):
        pass

def test_node_pure_python_initialization():
    scene = MockScene()
    node = NodePurePython(scene, "test_node")
    assert node.name == "test_node"
    assert node._scene == scene

def test_node_pure_python_name_setter():
    scene = MockScene()
    node = NodePurePython(scene, "test_node")
    node.name = "new_name"
    assert node.name == "new_name"


def test_dave_node_base_dissolve_some():
    node = DAVENodeBase()
    result = node.dissolve_some()
    assert result == (False, "")

def test_dave_node_base_try_swap():
    node = DAVENodeBase()
    result = node.try_swap(None, None)
    assert result == False

