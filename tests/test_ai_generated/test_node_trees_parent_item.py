import pytest
from DAVE import GeometricContact
from DAVE.helpers.node_trees import give_parent_item

def test_node_tree_parent_item():

    class MockNode:
        def __init__(self, name, parent=None, manager=None):
            self.name = name
            self.parent = parent
            self.manager = manager

    class MockGeometricContact:
        def __init__(self, name):
            self.name = name

        def creates(self, node):
            return False

    parent_item_is_root = give_parent_item(MockNode("root"), {})
    assert parent_item_is_root is None

    parent_item_with_parent = give_parent_item(MockNode("child", parent=MockNode("parent")), {"parent": "parent_item"})
    assert parent_item_with_parent == "parent_item"

    parent_item_with_manager = give_parent_item(MockNode("child", manager=MockNode("manager")), {"manager": "manager_item"})
    assert parent_item_with_manager == "manager_item"

    parent_item_with_geometric_contact = give_parent_item(MockNode("child", parent=MockNode("parent", manager=MockGeometricContact("gc"))), {"gc": "gc_item"})
    assert parent_item_with_geometric_contact == "gc_item"

    parent_item_with_hidden_nodes = give_parent_item(MockNode("child", parent=MockNode("hidden", parent=MockNode("parent"))), {"parent": "parent_item"})
    assert parent_item_with_hidden_nodes == "parent_item"

    parent_item_no_parent_no_manager = give_parent_item(MockNode("child"), {})
    assert parent_item_no_parent_no_manager is None