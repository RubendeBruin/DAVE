"""These are the abstract classes for DAVE nodes

Node:
    - Master class for all nodes
    - Has name as abstract requirement

"""
import fnmatch
import logging
import warnings
from abc import ABC, abstractmethod

import numpy as np

from .helpers import *


class DAVENodeBase:
    """Shall be the ultimate base class for nodes as well as anything mixed into nodes.

    - Implements "black holes" for all methods that are to be implemented with super()

    - The constructor really does nothing except making sure that object is not called with arguments
      This is an unfortunate workaround for super().

    - _on_name_changed: called after the name has changed
    - dissolve
    - try_swap

    """

    def __init__(self, *args, **kwargs):
        pass

    def _on_name_changed(self):
        """Called when the name of the node has changed
        !! When implementing this method, call super()._on_name_changed() in the implementation !!
        """
        pass  # black hole because super does not have this method

    def dissolve_some(self) -> tuple[bool, str]:
        """Dissolves the node into its children. Returns True if work was done, False otherwise"""
        return False, ""

    def try_swap(self, old: "Node", new: "Node") -> bool:
        """Tries to swap old for new. Returns True if work was done, False otherwise"""
        return False


class Node(DAVENodeBase, ABC):
    """ABSTRACT CLASS - Properties defined here are applicable to all derived classes
    Master class for all nodes"""

    def __init__(self, scene: "Scene", name: str or None = None):
        logging.info("Node.__init__")

        # Checks
        if hasattr(self, "_scene"):
            raise ValueError("_scene already exists, error in MRO?")

        self._scene: "Scene" = scene
        """reference to the scene that the node lives is"""

        self._manager: Node or None = None
        """Reference to a node that controls this node"""

        self.observers = list()
        """List of nodes observing this node."""

        self._visible: bool = True
        """Determines if the visual for of this node (if any) should be visible"""

        self._color: tuple or None = None
        """Holds the RGB (int) colors for the node or None for default color"""

        self.limits = dict()
        """Defines the limits of the nodes properties for calculating a UC, key is the property name, value is the limit."""

        self.watches: dict[str, Watch] = dict()
        """Defines the watches of the node, there are of type Watch"""

        self._valid = True
        """Turns False if the node in removed from a scene. This is a work-around for weakrefs"""

        self._tags = set()

        scene.add_node(self)  # adds the node to the scene

        # some custom properties for gui interaction
        self._no_name_editor = False

        super().__init__(scene=scene, name=name)

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the node [str]"""
        pass

    @name.setter
    @abstractmethod
    def name(self, val):
        self._on_name_changed()

    @property
    def warnings(self) -> list[str]:
        """Returns a list of warnings for this node, defaults to empty list"""
        return []

    @property
    def label(self) -> str:
        """Label of the node, used for display purposes [str]"""
        if self._valid:
            if "/" in self.name:
                return self.name.split("/")[-1]
            else:
                return self.name
        else:
            return "THIS NODE HAS BEEN DELETED"

    def __repr__(self):
        if self.is_valid:
            return f"{self.name} <{self.__class__.__name__}>"
        else:
            return "THIS NODE HAS BEEN DELETED"

    def __str__(self):
        return self.name

    def dissolve(self):
        """Dissolves the node, raises an exception if not possible."""
        raise Exception(f"Dissolve not implemented for node {self.__repr__()}")

    @property
    def color(self) -> tuple or None:
        """The color (r,g,b) of the node - use None for default"""
        return self._color

    @color.setter
    def color(self, value):
        if value is not None:
            assert len(value) == 3, "Color should be something like (r,g,b)"
        self._color = value

    @property
    def class_name(self) -> str:
        """Name of the python class, used for looking up documentation [str]
        #NOGUI"""
        return self.__class__.__name__

    @abstractmethod
    def depends_on(self) -> list:
        """Returns a list of nodes that need to be present for this node to exist"""
        raise ValueError(
            f"Derived class should implement this method, but {type(self)} does not"
        )

    def give_python_code(self):
        """Returns the python code that can be executed to re-create this node"""
        return "# No python code generated for element {}".format(self.name)

    @property
    def visible(self) -> bool:
        """Determines if this node is visible in the viewport [bool]"""
        if self.manager:
            return self.manager.visible and self._visible
        return self._visible

    @visible.setter
    @node_setter_manageable
    @node_setter_observable
    def visible(self, value):
        self._visible = value

    @property
    def manager(self) -> "Manager" or None:
        """If this node is managed then this is a reference to the node that manages this node. Otherwise None [Manager]
        #NOGUI"""
        return self._manager

    @manager.setter
    @node_setter_manageable
    @node_setter_observable
    def manager(self, value):
        self._manager = value
        pass

    def _verify_change_allowed(self):
        """Changing the state of a node is only allowed if either:
        1. the node is not manages (node._manager is None)
        2. the manager of the node is identical to scene.current_manager
        """
        if self._scene._godmode:  # pylint: disable=some-message,another-one
            return True

        if self._manager is not None:
            if self._manager != self._scene.current_manager:
                if self._scene.current_manager is None:
                    name = None
                else:
                    name = self._scene.current_manager.name
                raise Exception(
                    f"Node {self.name} may not be changed because it is managed by {self._manager.name} and the current manager of the scene is {name}"
                )

    @abstractmethod
    def _delete_vfc(self):
        """Removes any internally created core objects"""
        # TODO: refactor to _delete or something like that, not specific to vfc

        pass

    def update(self):
        """Performs internal updates relevant for physics. Called before solving statics or getting results such as
        forces or inertia"""
        pass

    def _notify_observers(self):
        for obs in self.observers:
            obs.on_observed_node_changed(self)

    def on_observed_node_changed(self, changed_node):
        """ """
        pass

    # Note: this is a property such that it shows up in the derived properties
    # this is inconsistent with scene.UC() which is a method
    @property
    def UC(self) -> float or None:
        """Returns the governing UC of the node, returns None is no limits are defined [-]

        See Also: give_UC, UC_governing_details
        """
        if not self.limits:
            return None

        gov_uc = -1

        props = [
            *self.limits.keys()
        ]  # Note: if a limit on UC itself was defined then this will be deleted during this loop
        for propname in props:
            uc = self.give_UC(propname)
            if uc is not None:
                gov_uc = max(gov_uc, uc)

        if gov_uc > -1:
            return gov_uc
        else:
            return None

    @property
    def UC_governing_details(self) -> tuple:
        """Returns the details of the governing UC for this node [-, name, limit value, actual value]:
        0: UC,
        1: property-name,
        2: property-limits
        3: property value

        Returns (None, None, None, None) if no limits are supplied
        """

        if not self.limits:
            return None, None, None, None

        gov_uc = 0
        gov_prop = ""
        gov_limits = ()
        gov_value = None

        for propname, limits in self.limits.items():
            uc = self.give_UC(propname)
            if uc > gov_uc:
                gov_uc = max(gov_uc, uc)
                gov_prop = propname
                gov_limits = limits
                gov_value = getattr(self, propname)

        return gov_uc, gov_prop, gov_limits, gov_value

    def give_UC(self, prop_name=None):
        """Returns the UC for the provided property name.

        See Also: UC (property)
        """

        if prop_name not in self.limits:
            return None

        if prop_name == "UC":
            warnings.warn(
                f'Limit defined on "UC" on node {self.name}. Can not calculate the UC for UC as that would result in infinite recursion. Deleting this limit'
            )
            del self.limits["UC"]
            return None

        limits = self.limits[prop_name]

        if isinstance(limits, (float, int)):
            if limits <= 0:
                return 0

        value = getattr(self, prop_name, None)
        if value is None:
            raise ValueError(
                f"Error evaluating limits: No property named {prop_name} on node {self.name}"
            )

        assert isinstance(
            value, (int, float)
        ), f"property named {prop_name} on node {self.name} is not a single number, it is: {str(value)}"

        if isinstance(limits, (int, float)):  # single number
            uc = abs(value) / limits
        else:
            midpoint = (limits[1] + limits[0]) / 2
            delta = abs(limits[1] - limits[0]) / 2
            uc = abs(value - midpoint) / delta

        return uc

    def invalidate(self):
        self._valid = False

    @property
    def is_valid(self) -> bool:
        """Returns True if the node is still present in the scene and/or connected to the core.
        Use this to verify that references to nodes that may have been deleted from the scene in the mean-time are
        still valid.
        #NOGUI
        """
        return self._valid

    @property
    def node_errors(self) -> list[str]:
        """Returns a list of models structure errors that are relevant for this node
        #NOGUI"""

        return []

    def add_tag(self, value: str):
        """Adds the provided tag to the tags"""
        assert isinstance(
            value, str
        ), f"Tags needs to be strings (text)but {value} is not a string"
        self._tags.add(value)

    def add_tags(self, tags):
        for tag in tags:
            assert isinstance(
                tag, str
            ), f"Tags needs to be strings (text), but {tag} is not a string"

        for tag in tags:
            self.add_tag(tag)

    def has_tag(self, tag: str):
        """Returns true if node has the given tag - tag can be a tag selection expression"""
        if tag in self._tags:  # simple first quick check
            return True

        req_tags = [_.strip() for _ in tag.split(",")]

        for tag in self._tags:
            matching = [fnmatch.fnmatch(tag, fltr) for fltr in req_tags]

            if any(matching):
                return True

        return False

    @property
    def tags(self) -> tuple:
        """All tags of this node (tuple of str)"""
        return tuple(self._tags)

    def delete_tag(self, value: str):
        self._tags.remove(value)

    # watches
    def run_watches(self) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
        """Executes all watches on this node and returns the execution result as
        active = list[tuple[str, values]]
        hidden = list[tuple[str, values]]

        watches of which the condition evaluates to False are excluded
        numerical results are rounded to "decimals" if >= 0
        """
        r = []
        hidden = []

        for desc, w in self.watches.items():
            try:
                value = eval(w.evaluate, {"np": np}, {"s": self._scene, "self": self})
            except Exception as M:
                value = f"ERROR: {w.evaluate} -> {str(M)}"

            if w.condition:
                condition = eval(
                    w.condition,
                    {"np": np},
                    {"s": self._scene, "self": self, "value": value},
                )
            else:
                condition = True

            # convert nd arrays to tuples for easier comparison later
            if isinstance(value, np.ndarray):
                value = tuple(value)

            if condition:
                if w.decimals >= 0:
                    if isinstance(value, float):
                        value = round(value, w.decimals)

                r.append((desc, value))

            else:
                hidden.append((desc, value))

        return r, hidden


class NodeCoreConnected(Node):
    def __init__(self, scene, name):
        logging.info("NodeCoreConnected.__init__")
        assert hasattr(
            self, "_vfNode"
        ), "_vfNode must be assigned BEFORE calling super()__init__"
        super().__init__(scene=scene, name=name)

    @property
    def name(self) -> str:
        """Name of the node (str), must be unique"""
        if self._vfNode is None:  # node has been deleted
            return None
        return self._vfNode.name

    @property
    def warnings(self) -> list[str]:
        """Returns a list of warnings for this node, if any"""
        return self._vfNode.warnings

    @name.setter
    @node_setter_manageable
    @node_setter_observable
    def name(self, name):
        if self._vfNode is None:
            raise ValueError(f"No connection to core - can not set name {name}")

        if not name == self._vfNode.name:
            self._scene._verify_name_available(name)
            self._vfNode.name = name

        self._on_name_changed()

    def _delete_vfc(self):
        name = self._vfNode.name
        self._vfNode = None  # this node will become invalid.
        self._scene._vfc.delete(name)
        self.invalidate()


class NodePurePython(Node):
    def __init__(self, scene, name):
        self._name = name
        super().__init__(scene=scene, name=name)

    @property
    def name(self) -> str:
        """Name of the node (str), must be unique [str]"""
        return self._name

    def depends_on(self) -> list:
        """Returns a list of nodes that need to be present for this node to exist"""
        return []  # no dependencies by default

    @name.setter
    @node_setter_manageable
    @node_setter_observable
    def name(self, name):
        self._name = name

        self._on_name_changed()

    def _delete_vfc(self):
        pass  # nothing to delete
