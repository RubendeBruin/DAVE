"""Helper functions and classes for nodes"""
import functools
from dataclasses import dataclass


def node_setter_manageable(func):
    @functools.wraps(func)
    def wrapper_decorator(self, *args, **kwargs):
        self._verify_change_allowed()
        value = func(self, *args, **kwargs)
        return value

    return wrapper_decorator


# Wrapper (decorator) observed nodes
def node_setter_observable(func):
    @functools.wraps(func)
    def wrapper_decorator(self, *args, **kwargs):
        value = func(self, *args, **kwargs)
        # Do something after
        self._notify_observers()

        return value

    return wrapper_decorator


class ClaimManagement:
    """Helper class for doing:

    with ClaimManagement(scene, manager):
        change nodes that belong to manager

    """

    def __init__(self, scene, manager):
        from ..scene import Scene

        assert isinstance(scene, Scene)
        if manager is not None:
            from ..nodes import Manager
            assert isinstance(manager, Manager)
        self.scene = scene
        self.manager = manager

    def __enter__(self):
        self._old_manager = self.scene.current_manager
        self.scene.current_manager = self.manager

    def __exit__(self, *args, **kwargs):
        self.scene.current_manager = self._old_manager


def valid_node_weakref(wr):
    """Helper function to check if weakrefs to nodes are valid (this is not guaranteed by weakref).
    Returns true if a weakref to a node still exists and points to a valid node"""

    node = wr()
    if node is None:
        return False
    return node.is_valid


@dataclass
class Watch:
    """Watches on nodes

    a watch is part of a node
    it is stored in a dictionary where the key is the description of the watch
    """

    evaluate: str = "self.name"
    decimals: int = 3
    condition: str = ""  # Empty evaluates to True
