"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""
import graphlib
import itertools
import logging
import string
import warnings
import weakref
import datetime
from copy import deepcopy
from graphlib import TopologicalSorter
from os.path import isdir, isfile
from os import mkdir
from pathlib import Path
from random import choice
from shutil import copy, copyfile
import re
import tempfile

from time import sleep
from typing import Tuple, List
import functools

import DAVEcore as DC

from DAVE.settings import (
    SolverSettings,
    RESOURCE_PATH,
    NodePropertyInfo,
    MANAGED_NODE_IDENTIFIER,
    DAVE_NODEPROP_INFO,
)

from .exceptions import ModelInvalidException
from DAVE import settings
from DAVE import gui_globals
from .helpers.code_error_extract import get_code_error

from .resource_provider import DaveResourceProvider
from .helpers.string_functions import increment_string_end
from .nds.mixins import Manager

from .tools import *
from .nodes import *

# from .nodes import _Area

# we are wrapping all methods of DAVEcore such that:
# - it is more user-friendly
# - code-completion is more robust
# - we can do some additional checks. DAVEcore is written for speed, not robustness.
# - DAVEcore is not a hard dependency
#
# notes and choices:
# - properties are returned as tuple to make sure they are not editable.
#    --> node.position[2] = 5 is not allowed


class Scene:
    """
    A Scene is the main component of DAVE.

    It provides a world to place nodes (elements) in.
    It interfaces with DAVEcore for all calculations.

    By convention a Scene element is created with the name s, but create as many scenes as you want.

    Examples:

        s = Scene()
        s.new_frame('my_axis', position = (0,0,1))

        a = Scene() # another world
        a.new_point('a point')


    """

    def __init__(
        self,
        filename=None,
        copy_from=None,
        code=None,
        resource_provider: DaveResourceProvider or None = None,
    ):
        """Creates a new Scene

        Args:
            filename: (str or Path) Insert contents from this file into the newly created scene
            copy_from:  (Scene) Copy nodes from this other scene into the newly created scene
        """

        count = 0
        if filename:
            count += 1
        if copy_from:
            count += 1
        if code:
            count += 1
        if count > 1:
            raise ValueError(
                "Only one of the named arguments (filename OR copy_from OR code) can be used"
            )

        self.verbose = True
        """Report actions using print()"""

        self._vfc = DC.Scene()
        """_vfc : DAVE Core, where the actual magic happens"""

        self._nodes = []
        """Contains a list of all nodes in the scene"""

        self._node_dict = {}
        """Temporary dict of nodes and names - for internal use only"""

        self.resource_provider = resource_provider or DaveResourceProvider()
        """Resource provider for this scene, will be passed as ref to all implicitly created scenes (components etc)"""

        self._resource_logger = None
        """Logger injection point for resource capturing"""

        self._savepoint = None
        """Python code to re-create the scene, see savepoint_make()"""

        self.current_manager = None
        """Setting this to an instance of a Manager allows nodes with that manager to be changed"""

        self._godmode = False
        """Icarus warning, wear proper PPE"""

        self._export_code_with_solved_function = True
        """Wrap solved values in 'solved' function when exporting python code"""

        self.reports = []
        """List of reports"""

        self.t: "TimeLine" or None = None
        """Optional timeline"""

        self.gui_solve_func = None
        """Optional reference to function to use instead of solve_statics - used by the Gui to give user control of solving
        Function is called with self as argument"""

        self.solve_activity_desc = "Solving static equilibrium"
        """This string may be used for feedback to user - read by Gui"""

        self.solver_settings = SolverSettings()
        """Settings for the solver"""

        if filename is not None:
            self.load_scene(filename)

        if copy_from is not None:
            self.import_scene(copy_from, containerize=False, settings=True)

        if code is not None:
            self.run_code(code)

    @property
    def resources_paths(self):
        raise NotImplementedError("Use resource_provider.resources_paths instead")

    @resources_paths.setter
    def resources_paths(self, value):
        raise NotImplementedError("Use resource_provider.resources_paths instead")

    def add_resources_paths(self, path: Path or str):
        if isinstance(path, str):
            path = Path(path)
        self.resource_provider.addPath(path)

    @property
    def current_directory(self):
        return self.resource_provider.cd

    @current_directory.setter
    def current_directory(self, value: str or Path):
        if isinstance(value, str):
            value = Path(value)
        self.resource_provider.cd = value

    def clear(self):
        """Deletes all nodes - leaves settings and reports in place"""

        # manually remove all references to the core
        # this avoids dangling pointers in copies of nodes
        for node in self._nodes:
            node.invalidate()
            node._delete_vfc()

        self._nodes = []
        del self._vfc

        # clear reports
        self._validate_reports()

        self.reports.clear()

        self.t = None  # reset timelines (if any)

        self._vfc = DC.Scene()

        # reset solver settings to default values
        self.solver_settings = SolverSettings()

    # =========== settings =============

    @property
    def g(self):
        """Gravity in kg*m/s2"""
        return self._vfc.g

    @g.setter
    def g(self, value):
        assert1f(value)

        old_godmode = (
            self._godmode
        )  # we also need to change the "mass" of managed nodes.
        self._godmode = True

        # first store the old masses
        rbs = self.nodes_of_type(RigidBody)
        for n in rbs:
            n._temp_mass = n.mass  # temporary property

        # then update gravity, this changes the mass as the mass is stored as a force on the cog
        self._vfc.g = value

        # now re-apply the old masses
        for n in rbs:
            n.mass = n._temp_mass

        self._godmode = old_godmode

    @property
    def rho_water(self):
        """Density of water [mT/m3]"""
        return self._vfc.rho_water

    @rho_water.setter
    def rho_water(self, value):
        assert1f_positive_or_zero(value)
        self._vfc.rho_water = value

    @property
    def rho_air(self):
        """Density of air [mT/m3]"""
        return self._vfc.rho_air

    @rho_air.setter
    def rho_air(self, value):
        assert1f_positive_or_zero(value)
        self._vfc.rho_air = value

    @property
    def waterlevel(self):
        """Elevation of the waterplane (global) [m]"""
        return self._vfc.waterlevel

    @waterlevel.setter
    def waterlevel(self, value):
        assert1f(value)
        if value != self._vfc.waterlevel:
            raise ValueError("Waterlevels other than 0 are not supported yet")
        self._vfc.waterlevel = value

    @property
    def nFootprintSlices(self):
        """Number of slices used in buoyancy discretization when calculating bending moments"""
        return self._vfc.nFootprintSlices

    @nFootprintSlices.setter
    def nFootprintSlices(self, value):
        assert isinstance(value, int), "needs to be integer"
        self._vfc.nFootprintSlices = value

    @property
    def roundbar_entry_ease_in_distance_m(self):
        """Distance over which the roundbar entry is eased in"""
        return self._vfc.roundbar_entry_ease_in_distance_m

    @roundbar_entry_ease_in_distance_m.setter
    def roundbar_entry_ease_in_distance_m(self, value):
        assert1f_positive_or_zero(value)
        self._vfc.roundbar_entry_ease_in_distance_m = value

    @property
    def wind_direction(self):
        return np.mod(np.rad2deg(self._vfc.wind_direction), 360)

    @wind_direction.setter
    def wind_direction(self, value):
        assert1f(value, "wind direction")
        self._vfc.wind_direction = np.deg2rad(value)

    @property
    def current_direction(self):
        return np.mod(np.rad2deg(self._vfc.current_direction), 360)

    @current_direction.setter
    def current_direction(self, value):
        assert1f(value, "current direction")
        self._vfc.current_direction = np.deg2rad(value)

    @property
    def wind_velocity(self):
        return self._vfc.wind_velocity

    @wind_velocity.setter
    def wind_velocity(self, value):
        assert1f_positive_or_zero(value, "wind velocity")
        self._vfc.wind_velocity = value

    @property
    def current_velocity(self):
        return self._vfc.current_velocity

    @current_velocity.setter
    def current_velocity(self, value):
        assert1f_positive_or_zero(value, "current velocity")
        self._vfc.current_velocity = value

    # =========== private functions =============

    def _print_cpp(self):
        print(self._vfc.to_string())

    def _save_coredump(self, filename=r"c:\data\test.txt"):
        with open(filename, "w") as f:
            f.write(self._vfc.to_string())
        print('Saved coredump to "{}"'.format(filename))

    def _print(self, what):
        if self.verbose:
            print(what)

    def _verify_name_available(self, name):
        """Throws an error if a node with name 'name' already exists"""
        if name == "":
            raise Exception("Name can not be empty")

        names = [n.name for n in self._nodes]
        names.extend(self._vfc.names)
        if name in names:
            raise Exception(
                "The name '{}' is already in use. Pick a unique name".format(name)
            )

    def _node_from_node_or_str_or_None(self, node):
        if node is None:
            return None
        return self._node_from_node_or_str(node)

    def _node_from_node_or_str(self, node):
        """If node is a string, then returns the node with that name,
        if node is a node, then returns that node

        Raises:
            ValueError if a string is passed with an non-existing node
        """

        if isinstance(node, Node):
            return node
        if isinstance(node, str):
            return self[node]
        raise ValueError(
            "Node should be a Node or a string, not a {}".format(type(node))
        )

    def _node_from_node(self, node, reqtype):
        """Gets a node from the specified type

        Returns None if node is None
        Returns node if node is already a reqtype type node
        Else returns the axis with the given name

        Raises Exception if a node with name is not found"""

        if node is None:
            return None

        # node is a string then get the node with this name
        if type(node) == str:
            # use prefix if any
            node = self[node]

        reqtype = make_iterable(reqtype)

        for r in reqtype:
            if isinstance(node, r):
                return node

        if issubclass(type(node), Node):
            raise Exception(
                "Element with name {} can not be used , it should be a {} or derived type but is a {}.".format(
                    node.name, reqtype, type(node)
                )
            )

        raise Exception("This is not an acceptable input argument {}".format(node))

    def _parent_from_node(self, node):
        """Returns None if node is None
        Returns node if node is an axis type node
        Else returns the axis with the given name

        Raises Exception if a node with name is not found"""

        return self._node_from_node(node, Frame)

    def _poi_from_node(self, node):
        """Returns None if node is None
        Returns node if node is an poi type node
        Else returns the poi with the given name

        Raises Exception if anything is not ok"""

        return self._node_from_node(node, Point)

    def _poi_or_sheave_from_node(self, node):
        """Returns None if node is None
        Returns node if node is an poi type node
        Else returns the poi with the given name

        Raises Exception if anything is not ok"""

        return self._node_from_node(node, [Point, Circle])

    def _sheave_from_node(self, node):
        """Returns None if node is None
        Returns node if node is an poi type node
        Else returns the poi with the given name

        Raises Exception if anything is not ok"""

        return self._node_from_node(node, Circle)

    def _geometry_changed(self):
        """Notify the scene that the geometry has changed and that the global transforms are invalid"""
        self._vfc.geometry_changed()

    def _fix_vessel_heel_trim(self):
        """Fixes the heel and trim of each node that has a buoyancy or linear hydrostatics node attached.

        Returns:
            Dictionary with original fixed properties as dict({'node name',fixed[6]}) which can be passed to _restore_original_fixes
        """
        remember_godmode = self._godmode
        self._godmode = True

        vessel_indicators = [
            *self.nodes_of_type(Buoyancy),
            *self.nodes_of_type(HydSpring),
        ]
        r = dict()

        for node in vessel_indicators:
            parent = node.parent  # axis

            if parent.fixed[3] and parent.fixed[4]:
                continue  # already fixed

            r[parent.name] = parent.fixed  # store original fixes
            fixed = [*parent.fixed]
            fixed[3] = True
            fixed[4] = True

            # if fixed[3] and fixed[4] are non-zero, then yaw has to be fixed as well.
            # The solver does not support it when an angular dof is free, but one of the fixed
            # angular dofs is non-zero

            fixed[5] = True

            parent.fixed = fixed

        self._godmode = remember_godmode

        return r

    def _restore_original_fixes(self, original_fixes):
        """Restores the fixes as in original_fixes

        See also: _fix_vessel_heel_trim

        Args:
            original_fixes: dict with {'node name',fixes[6] }

        Returns:
            None

        """
        if original_fixes is None:
            return

        remember_godmode = self._godmode
        self._godmode = True

        for name in original_fixes.keys():
            self.node_by_name(name).fixed = original_fixes[name]

        self._godmode = remember_godmode

    def _check_and_fix_geometric_contact_orientations(self) -> Tuple[bool, list]:
        """A Geometric pin on pin contact may end up with tension in the contact. Fix that by moving the child pin to the other side of the parent pin

        Returns:
            True if anything was changed; False otherwise
        """

        changed = False
        messages = []
        for n in self.nodes_of_type(GeometricContact):
            if n.fixed_to_parent or n.child_fixed:  # can not change side if fixed
                continue

            if n.inside:
                # inside contact
                # the rod connecting the two pins needs to be under tension if the child circle is smaller than the parent circle (the usual case)
                # if the child circle is larger than the parent circle, then the rod needs to be under compression

                # the tension in the rod can be obtained from the connection force of the child of the rod the axis_in_child
                # the x-component of this force should be positive

                if n._axis_on_child.connection_force_x < 0:
                    messages.append(
                        f"Changing side of inside connection {n.name} because it is on the wrong side"
                    )  #  due to compression in connection")
                    n.change_side()
                    changed = True

                if n._parent_circle.radius < n._child_circle.radius:
                    warnings.warn(
                        "Parent circle is smaller than child circle, this is allowed but may lead to unexpected results if this is not what you intended to do"
                    )

            else:  # outside contact
                # connection force of the child is the
                # force applied on the connecting rod
                # in the axis system of the rod
                if n._axis_on_child.connection_force_x > 0:
                    messages.append(
                        f"Changing side of outside connection {n.name} because it is on the wrong side"
                    )  # due to tension in connection")
                    n.change_side()
                    changed = True

        return (changed, messages)

    # ======== resources =========

    def is_valid_resource_path(self, url) -> bool:
        """Returns True if url is a valid resource path"""
        try:
            self.get_resource_path(url, no_gui=True)
            return True
        except FileNotFoundError:
            return False

    def get_resource_path(self, url: str, no_gui=False) -> Path:
        """Resolves the path on disk for resource url.
        Urls statring with res: result in a file from the resources system.
        Urls statring with cd: result in a file from the current directory.

        Looks for a file with "name" in the specified resource-paths of the resource provider and returns the full path to the the first one
        that is found.
        If name is a full path to an existing file, then that is returned.

        If the file is not found, but a Qt Application is present, then a dialog will be shown asking the user to locate the file. Except if no_gui is True, then a FileNotFoundError is raised.


        Returns:
            Full Path to resource : Path

        Raises:
            FileExistsError if resource is not found

        """
        if isinstance(url, Path):
            url = str(url)

        return self.resource_provider.get_resource_path(url, no_gui=no_gui)

    def get_used_resources(self):
        """Returns a list of all resources used in the scene"""

        copy_of_resource_provider = deepcopy(self.resource_provider)
        copy_of_resource_provider.clearLog()
        s2 = Scene(resource_provider=copy_of_resource_provider)
        s2.import_scene(self)
        return s2.resource_provider.getLog()

    def get_resource_list(
        self, extension, include_subdirs=False, include_current_dir=True
    ):
        """Returns a list of all resources (strings) with given extension in any of the resource-paths

        extension: (str) extension to look for, for example 'dave' or '.dave'
        include_subdirs : do a recursive search
        include_current_dir : return 'cd:' based resources as well

        """
        return self.resource_provider.get_resource_list(
            extension, include_subdirs, include_current_dir
        )

    # ======== element functions =========

    @property
    def unmanaged_nodes(self):
        """Returns a tuple containing references to all nodes that do not have a manager"""
        nodes = [node for node in self._nodes if node.manager is None]
        return tuple(nodes)

    @property
    def managed_nodes(self):
        """Returns a tuple containing references to all nodes that do have a manager"""
        nodes = [node for node in self._nodes if node.manager is not None]
        return tuple(nodes)

    def give_properties_for_node(
        self, node, settable=None, single_settable=None, single_numeric=None
    ) -> tuple[str]:
        """Returns a tuple containing all property-names for the given node optionally matching the given criteria.

        Args:
            node: Node for which to get the properties
            settable: [None], set to True or False to filter, None to ignore
            single_settable: [None], set to True or False to filter, None to ignore
            single_numeric: [None], set to True or False to filter, None to ignore

        Returns: tuple of strings"""

        # get docs for type of Node and all classes it inherits from
        anchestors = type(node).mro()
        props = []

        ignore_all = (
            (settable is None)
            and (single_settable is None)
            and (single_numeric is None)
        )

        for anchestor in reversed(anchestors):
            if anchestor in DAVE_NODEPROP_INFO:
                if ignore_all:
                    props.extend(DAVE_NODEPROP_INFO[anchestor].keys())
                else:
                    for key, value in DAVE_NODEPROP_INFO[anchestor].items():
                        if (
                            ((value.is_settable == settable) or (settable is None))
                            and (
                                (value.is_single_settable == single_settable)
                                or (single_settable is None)
                            )
                            and (
                                (value.is_single_numeric == single_numeric)
                                or (single_numeric is None)
                            )
                        ):
                            props.append(key)

        # remove duplicates
        props = list(set(props))  # filter out doubles
        props.sort()

        return tuple(props)

    def give_documentation(self, node: "Node", property_name: str) -> NodePropertyInfo:
        """Returns info about property_name of node node. Returns None if no documentation is found"""

        # get docs for type of Node and all classes it inherits from
        anchestors = type(node).mro()

        # strip [] from property_name
        if "[" in property_name:
            property_name = re.sub(r"\[.*?\]", "", property_name)

        docs = None

        for anchestor in reversed(anchestors):
            if anchestor in DAVE_NODEPROP_INFO:
                info = DAVE_NODEPROP_INFO[anchestor]
                if property_name in info:
                    docs = info[property_name]

        return docs

    def node_by_name(self, node_name, silent=False):
        """Returns a node with the given name. Raises an error if no node is found."""

        # For faster lookup we keep a dict with node names as keys and node indices as values
        # (Keeping the index instead of the node itself assures that the node in indeed in the _nodes list
        # if not then a node with the same name may be returned by accident)
        #
        # This has a good chance of quickly returning the node
        # to verify that it is indeed the correct node we check the name
        #
        # There is nothing keeping the dict in sync with _nodes, so we rebuild it
        # when we can not find the node that we're looking for.

        # the quick way
        if node_name in self._node_dict:
            index = self._node_dict[node_name]
            if index < len(self._nodes):
                node = self._nodes[index]
                if node.name == node_name:
                    return node

        assert isinstance(
            node_name, str
        ), f"Node name should be a string, but is a {type(node_name)}"

        # rebuild nodes dict

        self._node_dict = {node.name: index for index, node in enumerate(self._nodes)}
        if node_name in self._node_dict:
            return self._nodes[self._node_dict[node_name]]  # return directly

        # work-around for renames
        # TODO: remove this when renames are implemented (May 2023) - Removing this break models created before May 2023
        #
        # Renames are _ to /
        #            >>> to /

        # See if we get a single match when we just ignore _ / and >>>

        search_for = node_name.replace("_", "^").replace(">>>", "^").replace("/", "^")
        options = [
            t.replace("_", "^").replace(">>>", "^").replace("/", "^")
            for t in self.node_names
        ]

        if search_for in options:
            if options.count(search_for) == 1:
                index = options.index(search_for)
                N = self._nodes[index]

                warnings.warn(
                    f"Selecting node {node_name} based on fuzzy-match {N.name}. If you are not importing an old file then please use the correct the name in the future."
                )

                return N

            else:
                # multiple matches
                warnings.warn(
                    f"Selecting node {node_name} based on fuzzy-match {N.name}. If you are not importing an old file then please use the correct the name in the future."
                )

        # end work-around

        if not silent:
            self.print_node_tree()

        # See if we can give a good hint using fuzzy

        choices = [node.name for node in self._nodes]
        suggestion = MostLikelyMatch(node_name, choices)

        # do we have a gui and does it allow for us to ask?
        if gui_globals.do_ask_user_for_unavailable_nodenames:
            try:
                from PySide6.QtWidgets import QApplication

                if QApplication.instance() is not None:
                    from PySide6.QtWidgets import QMessageBox

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Question)
                    msg.setText(
                        f'Node with name "{node_name}" not found. Did you mean: "{suggestion}"?'
                    )
                    msg.setWindowTitle("DAVE")
                    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    if msg.exec() == QMessageBox.Yes:
                        return self.node_by_name(suggestion)

            except ImportError:
                pass

        raise ValueError(
            'No node with name "{}". Did you mean: "{}"? \nAvailable names printed above.'.format(
                node_name, suggestion
            )
        )

    def __getitem__(self, node_name):
        """Returns a node with name"""
        return self.node_by_name(node_name)

    def nodes_of_type(self, node_class):
        """Returns all nodes of the specified or derived type

        Examples:
            pois = scene.nodes_of_type(DAVE.Poi)
            axis_and_bodies = scene.nodes_of_type(DAVE.Axis)
        """
        r = list()
        for n in self._nodes:
            if isinstance(n, node_class):
                r.append(n)
        return r

    def assert_unique_names(self):
        """Asserts that all names are unique"""
        names = [n.name for n in self._nodes]
        unique_names = set(names)

        if len(unique_names) != len(names):
            previous_name = ""
            names.sort()
            duplicates = ""
            for name in names:
                if name == previous_name:
                    print(f"Duplicate: {name}")
                    duplicates += name + " "

                    for n in self._nodes:
                        if n.name == name:
                            print(n)

                previous_name = name
            raise ValueError(f"Duplicate names exist: " + duplicates)

    def assert_no_external_managers(self):
        """Asserts that the managers of all nodes are also present in the Scene"""
        check = [
            node for node in self._nodes if node.manager not in (*self._nodes, None)
        ]
        if check:
            for c in check:
                print(f'Node: "{c.name}" has missing manager: "{c.manager}"')
            raise ValueError(
                "Some of the nodes in this scene are managed by a manager who itself is not part of the scene"
            )

    def sort_nodes_by_parent(self):
        """Sorts the nodes such that the parent of this node (if any) occurs earlier in the list.

        See Also:
            sort_nodes_by_dependency
        """

        self.assert_unique_names()
        self.assert_no_external_managers()

        graph = dict()
        for node in self._nodes:
            deps = []

            if isinstance(node, HasParent):
                if node.parent is not None:
                    deps.append(node.parent)

            if node.manager is not None:
                deps.append(node.manager)

            graph[node] = deps

        try:
            ts = TopologicalSorter(graph)
        except graphlib.CycleError as M:
            raise Exception(
                f"Could not sort nodes by parent, circular references exist: {str(M)}"
            )

        self._nodes = list(ts.static_order())

    def get_created_by_dict(self) -> dict:
        """Returns a dictionary containing the nodes created by each manager.
        Keys are the manager nodes
        Values are lists of nodes created by that manager

        Raises and exception if a node is created by multiple managers

        See Also: get_implicitly_created_nodes
        """

        creates = dict()
        for node in self._nodes:
            if isinstance(node, Manager):
                c = []
                for n in self._nodes:
                    if node.creates(n):
                        c.append(n)

                        # check if not already created by another manager
                        for k, v in creates.items():
                            for vnode in v:
                                if vnode == n:
                                    raise Exception(
                                        f"Node {n} is already created by {k} , can not be created by {node} as well"
                                    )

                if c:
                    # print(f"Manager {node.name} creates:")
                    # for n in c:
                    #     print(f"  {n.name}")
                    creates[node] = c

        return creates

    def get_implicitly_created_nodes(self):
        """Returns a list of nodes that are created by a manager.

        See Also: get_created_by_dict
        """
        r = []
        for val in self.get_created_by_dict().values():
            r.extend(val)

        return r

    def sort_nodes_by_dependency(self):
        """Sorts the nodes such that a nodes creation only depends on nodes earlier in the list.

        This sorting is used for node creation order

        See Also:
            sort_nodes_by_parent
        """

        self.assert_unique_names()

        exported = []
        to_be_exported = self._nodes.copy()
        counter = 0

        originally_present = tuple(to_be_exported)  # for check

        # Some of the nodes are created by another node in this list.
        # Remove those nodes from the to_be_exported list and add
        # them to exported when the node that creates them is exported

        # create a dict "creates" that contains the nodes that are created by a manager as values of the manager as key.

        creates = self.get_created_by_dict()

        for v in creates.values():
            for node in v:
                to_be_exported.remove(node)

        # Move from the to_be_exported list to the exported list when all dependencies are exported

        while to_be_exported:
            counter += 1
            if counter > len(self._nodes):
                print("Error when exporting, could not resolve dependencies:")

                for node in to_be_exported:
                    print(f"Node : {node.name}")
                    for d in node.depends_on():
                        print(f"  depends on: {d.name}")
                    if node._manager:
                        print(f"   managed by: {node._manager.name}")
                    if node in node.depends_on():
                        raise Exception(
                            f"Node {node.name} depends on itself - that is not possible"
                        )

                raise Exception(
                    "Could not sort nodes by dependency, circular references exist?"
                )

            can_be_exported = []

            for node in to_be_exported:
                if all(el in exported for el in node.depends_on()):
                    can_be_exported.append(node)

            # remove exported nodes from
            for n in can_be_exported:
                to_be_exported.remove(n)

            # check for nodes that are created by the can_be_exported nodes
            #   and then recursively check on the nodes created by those nodes as well

            def expand_by_using_creates(node):
                nodes = [node]
                if node in creates:
                    for created_node in creates[node]:
                        nodes.extend(expand_by_using_creates(created_node))
                return nodes

            for node in can_be_exported:
                exported.extend(expand_by_using_creates(node))

        # self-check
        for n in originally_present:
            assert n in exported, f"Node {n.name} got lost during the sorting process"

        self._nodes = exported  # set the sorted list

    def assert_name_available(self, name):
        """Raises an error is name is not available"""
        assert self.name_available(name), f"Name {name} is already in use"

    @property
    def node_names(self) -> tuple:
        """Returns a tuple of all node names"""
        return tuple([n.name for n in self._nodes])

    def name_available(self, name):
        """Returns True if the name is still available. See Also: node_exists"""
        names = [n.name for n in self._nodes]
        names.extend(self._vfc.names)
        return not (name in names)

    def node_exists(self, name_or_node):
        """Returns True if a node with this name exists. See Also: name_available"""
        if isinstance(name_or_node, Node):
            return name_or_node in self._nodes
        else:
            return not self.name_available(name_or_node)

    def add_node(self, node):
        """Adds a node to the scene"""
        # called by base constructor, name property may not be set yet hence supplied separately
        assert node.name not in [
            node.name for node in self._nodes
        ], f"Node with name {node.name} already exists in the scene"
        self._nodes.append(node)

    def available_name_like(self, like, _additional_names=()):
        """Returns an available name like the one given, for example Axis23

        Args
            _additional_names [()] : if provided then the name shall not be one of these either
        """

        if self.name_available(like):
            if like not in _additional_names:
                return like

        name = like
        while True:
            if self.name_available(name):
                if name not in _additional_names:
                    return name
            name = increment_string_end(name)

    def node_A_core_depends_on_B_core(self, A, B):
        """Returns True if the node core of node A depends on the core node of node B"""

        A = self._node_from_node_or_str(A)
        B = self._node_from_node_or_str(B)

        if not isinstance(A, NodeCoreConnected):
            raise ValueError(
                f"{A.name} is not connected to a core node. Dependencies can not be traced using this function"
            )
        if not isinstance(B, NodeCoreConnected):
            raise ValueError(
                f"{B.name} is not connected to a core node. Dependencies can not be traced using this function"
            )

        return self._vfc.element_A_depends_on_B(A._vfNode.name, B._vfNode.name)

    def nodes_managed_by(self, manager: Manager, recursive=False) -> list:
        """Returns a list of nodes managed by manager"""
        if recursive:
            nodes = self.nodes_managed_by(manager, recursive=False)

            for node in tuple(nodes):
                if isinstance(node, Manager):
                    nodes.extend([*self.nodes_managed_by(node, recursive=True)])

            return nodes

        else:
            return [node for node in self._nodes if node.manager == manager]

    def nodes_depending_on(self, node, recursive=True) -> list[str]:
        """Returns a list of nodes that physically depend on node. Only direct dependants are obtained if recursive is False.
        This function should be used to determine if a node can be created, deleted, exported.

        For making node-trees please use nodes_with_parent instead.

        Args:
            node_name : Node or node-name

        Returns:
            list of names [str]

        See Also: nodes_with_parent
        """

        if isinstance(node, Node):
            node_name = node.name
        else:
            node_name = node

        # check the node type
        _node = self[node_name]
        if not isinstance(_node, NodeCoreConnected):
            r = []
        else:
            if recursive:
                names = self._vfc.elements_depending_on(node_name)
            else:
                names = self._vfc.elements_depending_directly_on(node_name)

            # filter to only the nodes that are in the scene (remove pointmasses etc)
            nodes_names_in_scene = self.node_names
            r = [n for n in names if n in nodes_names_in_scene]

        # check all other nodes in the scene
        #
        # Up till now we've covered all core-connected nodes
        # Now we need to check if there are any other nodes that depend on any of these nodes
        #
        # This is only a single pass as there are no nodes depending on a node that is not core-connected

        dependants_and_self = r.copy()
        dependants_and_self.append(node_name)

        for n in self._nodes:
            try:
                nodes = n.depends_on()
            except Exception as E:
                raise Exception(
                    f"Error when checking dependencies of node {n.name} of type {type(n)}"
                    + ":"
                    + str(E)
                )
            nodes_names = [node.name for node in nodes]

            for pre in nodes_names:
                if pre in dependants_and_self:
                    r.append(n.name)

        return r

    def node_is_fully_fixed_to(self, node, other_node) -> bool:
        """Returns true if this node will never move relative to other_node.
        Raises a ValueError if node is not connected to other_node"""

        if node == other_node:
            return True

        if node is None:
            raise ValueError(f"Node {node} is not connected to {other_node.name}")

        if not hasattr(node, "parent"):
            raise ValueError(
                f"Node {node} is not connected to anything (no parent property)"
            )

        if isinstance(node, Frame):
            if not all(node.fixed):
                return False

        return self.node_is_fully_fixed_to(
            node.parent,
            other_node,
        )  # recursive call on parent. Parent None returns True

    def node_is_fully_fixed_to_world(self, node) -> bool:
        """Returns true if this node will never move"""
        return self.node_is_fully_fixed_to(node, None)

    def common_ancestor_of_nodes(
        self, nodes: List[Node], required_type=None
    ) -> Node or None:
        """Finds a nearest ancestor (parent) that is common to all of the nodes.

        If required type is specified then the common anchestor needs to be in instance of that type.

        frame [Frame]
         |-> frame2 [Frame]
         |    |-> point [Point]
         |    |    |-> circle [Circle]
         |    |    |-> circle2 [Circle]
         |    |-> point2 [Point]
        frame3 [Frame]

        for example the common parent of point2 and circle is frame2.
        the common parent of circle and circle2 is point
        the common parent of circle2 and frame3 is None

        Args:
            nodes: list of nodes

        Returns:
            Node or None
        """
        parents_of_node = []

        for node in nodes:
            parents = []
            parent = getattr(node, "parent", None)
            while parent is not None:
                parents.append(parent)
                parent = getattr(parent, "parent", None)

            parents_of_node.append(parents)

        # remove any non-required types for the database
        if required_type is not None:
            parents_of_node = [
                [p for p in parents if isinstance(p, required_type)]
                for parents in parents_of_node
            ]

        # Now find the first entry that is common in all of the lists of parent_of_node - maintain the order
        common = parents_of_node[0]
        for parents in parents_of_node[1:]:
            common = [c for c in common if c in parents]

        if common:
            return common[0]
        else:
            return None

    def nodes_with_parent(self, node, recursive=False):
        """Returns a list of nodes that have given node as a parent. Good for making trees.
        For checking physical connections use nodes_depending_on instead.

        Args:
            node : Node or node-name
            recursive : look for grand-parents as well. This means a whole branch of the node-tree is returned.

        Returns:
            list of nodes

        See Also: nodes_depending_on
        """

        if isinstance(node, str):
            node = self[node]

        r = []

        for n in self._nodes:
            try:
                parent = n.parent
            except AttributeError:
                continue

            if parent == node:
                r.append(n)

        if recursive:
            more = []
            for n in r:
                more.extend(self.nodes_with_parent(n, recursive=True))
            r.extend(more)

        return r

    def nodes_with_dependencies_in_and_satifsfied_by(self, nodes):
        """Returns a list of all nodes that have dependencies and whose dependencies that are all within 'nodes'

        Often used in combination with nodes_with_parent, for example to find cables that fall within a branch of the
        node-tree.
        """

        r = []

        for node in self._nodes:
            deps = node.depends_on()
            if not deps:
                continue  # skip nodes without dependencies

            satisfied = True
            for dep in node.depends_on():
                if dep not in nodes:
                    satisfied = False
                    break

            if satisfied:
                r.append(node)

        return r

    def nodes_tagged(self, tag):
        """Returns all nodes that have the given tag or where the tag satisfies the tag-filter. Tag = None or '' returns all nodes"""

        if tag:
            return tuple([node for node in self._nodes if node.has_tag(tag)])
        else:
            return tuple(self._nodes)

    def nodes_tag_and_type(self, tag, type):
        """Returns all nodes of type 'type' with tag 'tag'"""

        set1 = self.nodes_tagged(tag)
        set2 = self.nodes_of_type(type)

        intersect = set(set1).intersection(set(set2))

        return tuple(intersect)

    def delete_tag(self, tag):
        """Removes the given tag from all nodes"""
        for node in self._nodes:
            if tag in node._tags:
                node.delete_tag(tag)

    @property
    def tags(self) -> tuple:
        """All tags in the scene"""
        tgs = set()
        for node in self._nodes:
            for tag in node.tags:
                tgs.add(tag)
        return tuple(tgs)

    def _unmanage_and_delete(self, nodes):
        """Un-manages as collection of nodes and then deletes them"""
        for node in nodes:
            node._manager = None
        for node in nodes:
            if node in self._nodes:
                self.delete(node)

    def delete(self, node):
        """Deletes the given node from the scene as well as all nodes depending on it.

        Depending nodes are nodes that are physically connected to the deleted node or are observing the node.

        About managed nodes:
        - deleting a managed node will delete its manager
        - deleting a manger will
            - release management of all nodes managed by that manager
            - delete all the nodes created by that manager

        See Also:
            dissolve
        """

        if isinstance(node, str):
            node = self[node]

        if node not in self._nodes:
            raise ValueError(
                "Can not delete node because it is not a node of this scene"
            )

        if node._manager:  # managed node, delete its manager
            self.delete(node._manager)

            # after deleting the manager, the node itself may still be here but now un-managed
            if node in self._nodes:
                self.delete(node)
            return

        if isinstance(node, Manager):
            if not getattr(
                node, "_dissolved", False
            ):  # work-around for skipping removal of created nodes when dissolving
                node.delete()  # deletes all created nodes, releases management

        depending_nodes = self.nodes_depending_on(node)
        depending_nodes.extend([n.name for n in node.observers])

        # Referenced nodes
        # Some node-types can reference to a node (so depend on it) but do not have a hard-dependancy.
        # - tanks in a ballast-system
        # - contact-meshes in a contact-ball
        # Treat these references differently

        for dep in [*depending_nodes]:
            dep_node = self[dep]

            if isinstance(dep_node, BallastSystem):
                if node in dep_node.tanks:
                    dep_node.tanks.remove(node)
                    depending_nodes.remove(dep)

            elif isinstance(dep_node, ContactBall):
                if node in dep_node.meshes:
                    meshes = list(dep_node.meshes)  # returns tuple
                    meshes.remove(node)  # re-init with new list
                    dep_node.meshes = meshes
                    depending_nodes.remove(dep)

        # First delete the dependencies
        for d in depending_nodes:
            if not self.name_available(d):  # element is still here
                self.delete(d)

        # then remove the vtk node itself
        # self._print('removing vfc node')
        node.invalidate()
        node._delete_vfc()
        self._nodes.remove(node)

        # validate reports
        self._validate_reports()

        # validate timelines
        self._validate_timelines()

    def dissolve(self, node):
        """Calls node.dissolve()"""

        node = self._node_from_node_or_str(node)
        node.dissolve()

    def delete_empty_frames_and_bodies(self):
        """Deletes all empty frames and rigid bodies with zero mass"""

        for node in self._nodes:
            if isinstance(node, RigidBody):
                if node.mass == 0:
                    if len(self.nodes_depending_on(node)) == 0:
                        self.delete(node)
                        return True
            elif isinstance(node, Frame):
                if len(self.nodes_depending_on(node)) == 0:
                    self.delete(node)
                    return True

        return False

    def flatten(self, root_node=None, exclude_known_types=False):
        """Performs a recursive dissolve on Frames (not rigid bodies). If root_node is None (default) then the whole model is flattened"""

        from .nodes import Component, GeometricContact

        known_types = (Component, GeometricContact)

        dissolved_node_name = None
        dissolved_node_names = []

        while True:
            if dissolved_node_name is not None:
                dissolved_node_names.append(dissolved_node_name)

            work_done = False

            if root_node is None:
                nodes = (*self._nodes,)
            else:
                nodes = self.nodes_depending_on(root_node)

            if exclude_known_types:
                nodes = [n for n in nodes if not isinstance(n, known_types)]

            for node in nodes:
                work_done, reason = node.dissolve_some()

                if work_done:
                    print(f"reason: {reason}")
                    break

            if not work_done:
                for node in nodes:
                    try:
                        nodename = node.name
                        node.dissolve()
                        print(f"Dissolved: {nodename}")
                        work_done = True
                    except:
                        pass

            if not work_done:
                break

        if root_node is not None:
            try:
                self.dissolve(root_node)
            except:
                pass

        return dissolved_node_names

    # # TODO: can be deleted?
    # def savepoint_make(self):
    #     """Makes a safepoint if non is present"""
    #     if self._savepoint is None:
    #         self._savepoint = self.give_python_code()
    #
    # # TODO: can be deleted?
    # def savepoint_restore(self):
    #     if self._savepoint is not None:
    #         self.clear()
    #         self.run_code(self._savepoint)
    #         self._savepoint = None
    #         return True
    #     else:
    #         return False

    def create_standalone_copy(
        self, target_dir, filename, include_visuals=True, flatten=False
    ):
        """Creates a stand-alone copy in .zip format
        Returns:
        filename, log of actions"""

        log = []
        success = False

        # create target dir
        if not isdir(target_dir):
            mkdir(target_dir)
            log.append("Created {}".format(target_dir))

        # Use a temporary directory to collect the resources
        with tempfile.TemporaryDirectory() as tmp_dir:
            used_resources = self.get_used_resources()

            s = self.copy(quick=True)
            if flatten:
                s.flatten(exclude_known_types=True)
                log.append("Flattened")

            # cube.obj is sometimes used as default visual, so copy it
            # same for default_component

            additional_files = (
                "shackle_gp800.obj",
                "cube.obj",
                "default_component.dave",
            )

            # create a mapping of used resources to
            counter = 0
            mapping = dict()
            for url, file in used_resources:
                if url in mapping:
                    continue

                if not include_visuals:
                    # Map all .obj files to the default cube
                    if Path(file).suffix == ".obj":
                        file = self.get_resource_path("res: cube.obj")

                # make a target name
                target_name = f"res_{counter}" + Path(file).suffix
                target_file = Path(tmp_dir) / target_name

                # copy
                copyfile(file, target_file)
                log.append(f"Copied {url} as  {target_file}")

                mapping[url] = target_name

                counter += 1

            for file in additional_files:
                copyfile(
                    self.get_resource_path(f"res: {file}"), str(Path(tmp_dir) / file)
                )

            # create export code for mapping
            code = "## This is a DAVE PACKAGE file - set package_folder to the folder containing this file before executing this code\n\n"
            code += f"mapping = {mapping}"
            code += "\ns.resource_provider.install_mapping(package_folder, mapping)"
            code += s.give_python_code()

            exported_DAVE_file = Path(tmp_dir) / (filename + ".dave")
            with open(exported_DAVE_file, "w") as f:
                f.write(code)

            log.append(f"Created DAVE file {exported_DAVE_file}")

            # Perform a self-check
            try:
                log.append("Self-check")
                t = Scene()
                t.load_package(exported_DAVE_file)
                log.append("Self-check completed without errors")
                success = True
            except Exception as E:
                log.append(f"Self check FAILED with error {str(E)}")

            try:
                log.append("Creating zip-file")
                zip_filename = Path(target_dir) / filename

                from shutil import make_archive

                make_archive(zip_filename, format="zip", root_dir=tmp_dir)

                log.append(f"Created zipfile {zip_filename}.zip")
            except Exception as E:
                log.append(f"Creating zipfile FAILED with error {str(E)}")
            #
        return Path(str(zip_filename) + ".zip"), log

    def load_package(self, filename: str or Path):
        """Loads a DAVE self-contained package file"""
        filename = Path(filename)
        path = filename.parent
        package_folder = str(path)
        code = filename.read_text()
        self.run_code(code, package_folder=package_folder)

    # ========= Limits ===========

    def UC(self, tags=None):
        """Returns the highest UC in the scene

        Optional argument tags limits the evaluated nodes to nodes with the given tag(s)
        """
        gov = 0

        for node in self.nodes_tagged(tags):  # None --> all nodes
            uc = node.UC
            if uc is not None:
                gov = max(gov, uc)
        return gov

    def UC_governing_details(self, tags=None):
        """Returns tuple with:
        0: governing UC,
        1: node-name in which this UC occurs
        2: property name
        3: limits
        4: value

        Optional argument tags limits the evaluated nodes to nodes with the given tag(s)
        """

        gov_node = None
        gov_prop = ""
        gov_limits = ()
        gov_value = None
        gov = 0
        for node in self.nodes_tagged(tags):
            uc, prop_name, limits, value = node.UC_governing_details
            if uc is not None:
                if uc > gov:
                    gov = uc
                    gov_node = node.name
                    gov_value = value
                    gov_prop = prop_name
                    gov_limits = limits

        if gov_node is None:
            return None, None, None, None
        else:
            return gov, gov_node, gov_prop, gov_limits, gov_value

    # ========= The most important functions ========

    @property
    def warnings(self) -> list[tuple[Node, str]]:
        """Returns a list of nodes that have an invalid or questionable state in the current state"""

        ers = []
        for node in self._nodes:
            for msg in node.warnings:
                ers.append((node, msg))
        return ers

    @property
    def node_errors(self) -> list[tuple[Node, str]]:
        """Returns a list of nodes with an error in the current model"""
        ers = []
        for node in self._nodes:
            for msg in node.node_errors:
                ers.append((node, msg))

        return ers

    def update(self):
        """Updates the interface between the nodes and the core. This includes the re-calculation of all forces,
        buoyancy positions, ballast-system cogs etc.
        """
        for n in self._nodes:
            n.update()
        self._vfc.state_update()

    def _solve_statics_with_optional_control(
        self,
        feedback_func=None,
        do_terminate_func=None,
    ):
        """Solves statics with a time-out and feedback/terminate functions.

        Solver settings are taken from self.solver_settings
        If user terminates then settings.SOLVER_TERMINATED_SCENE is set to this scene

        Options for feedback to user and termination control during solving:

        feedback_func     : func(str)
        do_terminate_func : func() -> bool
        """

        self.update()  # <-- needed to get the correct initial state including number of DOFs

        if self._vfc.n_dofs() == 0:  # check for the trivial case
            return True

        # Two quick helper functions for running in controlled mode
        def give_feedback(txt):
            if feedback_func is not None:
                feedback_func(txt)

        def should_terminate():
            if do_terminate_func is not None:
                return do_terminate_func()
            else:
                return False

        start_time = datetime.datetime.now()

        while True:  # only stop when we are completely happy or when the user cancels
            if not self.verify_equilibrium():  # does update
                # Scene is not in equilibrium
                # construct a background solver
                # start it
                # wait till it completes or it is cancelled

                BackgroundSolver = DC.BackgroundSolver(self._vfc)

                self.solver_settings.apply(BackgroundSolver)
                print(self.solver_settings)

                started = BackgroundSolver.Start()

                sleep_time = 0.001  # start with a millisecond

                if started:
                    while BackgroundSolver.Running:
                        if should_terminate():
                            BackgroundSolver.Stop()
                            settings.SOLVER_TERMINATED_SCENE = self
                            return False

                        # check if time has passed
                        time_diff = datetime.datetime.now() - start_time
                        secs = time_diff.total_seconds()
                        if (
                            self.solver_settings.timeout_s >= 0
                            and secs > self.solver_settings.timeout_s
                        ):
                            BackgroundSolver.Stop()

                            raise ValueError(
                                f"Solver maximum time of {self.solver_settings.timeout_s} exceeded - set terminate_after_s to change the allowed time for the solver."
                            )

                        sleep(sleep_time)  # sleep for a millisecond
                        sleep_time *= 1.1  # increase sleep time
                        sleep_time = min(sleep_time, 0.1)  # but not more than 100ms

                    # Background solver is done and
                    info = f"Converged within tolerance of {BackgroundSolver.tolerance} with E : {BackgroundSolver.Enorm:.6e}(norm) / {BackgroundSolver.Emaxabs:.6e}(max-abs) in {BackgroundSolver.Emaxabs_where}"

                    give_feedback(info)
                    logging.info(info)

                BackgroundSolver.CopyStateTo(self._vfc)

                self.update()

                assert (
                    self.verify_equilibrium()
                ), "Solver self-check failed: Equilibrium not reached after solving"

            else:
                pass  # already in equilibrium

            # check is geometric contacts are satisfied
            work_done, messages = self._check_and_fix_geometric_contact_orientations()

            if not work_done:  # contacts are satisfied
                return True  # <--- This is the exit

            # exit if time has passed
            time_diff = datetime.datetime.now() - start_time
            secs = time_diff.total_seconds()
            if (
                self.solver_settings.timeout_s >= 0
                and secs > self.solver_settings.timeout_s
            ):
                raise ValueError(
                    f"Solver maximum time of {self.solver_settings.timeout_s}s exceeded, solver converged but geometric contacts not satisfied - set terminate_after_s to change the allowed time for the solver."
                )

            give_feedback(
                "Geometric contacts not satisfied, correcting and trying again"
            )
            logging.info(
                "Geometric contacts not satisfied, correcting and trying again"
            )

            for m in messages:
                give_feedback(m)
                logging.info(m)

    def solve_statics(self):
        """Solves statics


        Returns:
            bool: True if successful, False otherwise.

        """

        if self.gui_solve_func is not None:
            return self.gui_solve_func(self, called_by_user=False)
        else:
            return self._solve_statics_with_optional_control()

    def verify_equilibrium(self, tol=None):
        """Checks if the current state is an equilibrium

        Returns:
            bool: True if successful, False if not an equilibrium.

        """
        if tol is None:
            tol = self.solver_settings.tolerance

        self.update()
        return self._vfc.Emaxabs < tol

    def obfuscate_names(self):
        """Will rename all nodes to random names"""

        nnames = list(self.node_names)
        for node in self._nodes:
            letters = string.ascii_letters
            while True:
                random_string = "".join(choice(letters) for i in range(10))
                if random_string not in nnames:
                    break

            node.name = random_string
            nnames.append(random_string)

    def export_points_to_csv(self, filename):
        """Writes a list of points and their 3d locations to a csv file"""
        with open(filename, "w") as f:
            f.write("name,x,y,z\n")
            for node in self.nodes_of_type(Point):
                f.write(f"{node.name},{node.gx},{node.gy},{node.gz}\n")
        print(f"Exported points to {filename}")

    # ====== goal seek ========

    def goal_seek(
        self, evaluate, target, change, bracket=None, tol=1e-3, tol_out=0.1, delta=0.001
    ):
        """goal_seek

        Goal seek is the classic goal-seek. It changes a single property of a single node in order to get
        some property of some node to a specified value. Just like excel.

        Args:
            evaluate : code to be evaluated to yield the value that is solved for. Eg: s['poi'].fx Scene is abbiviated as "s"
            target (number):       target value for that property
            change (string, tuple) value to be adjused. If string this is executed as change = number. If tuple then this is
                                   is done for each string in the tuple
            range(optional)  : specify the possible search-interval
            delta(optional)  : initial step-size on input

            tol : tolerance on changed variable
            tol_out : tolerance on evaluated variable

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            Change the y-position of the cog of a rigid body ('Barge')  in order to obtain zero roll (heel)
            >>> s.goal_seek("s['Barge'].heel",0,'s["Barge"].cogy')

        """
        s = self

        # check that the attributes exist and are single numbers
        test = eval(evaluate)

        try:
            float(test)
        except:
            raise ValueError("Evaluation of {} does not result in a float")

        self._print(
            "Attempting to evaluate {} to {} (now {})".format(evaluate, target, test)
        )

        if isinstance(change, str):
            change = (change,)  # make tuple

        if not isinstance(change, (tuple, list)):
            raise ValueError(
                "Variable to be changed shall be a tuple (of strings) or string"
            )

        initial = eval(change[0])

        self._print(f"By changing the value of {change} (now {initial})")

        def set_and_get(x):
            s = self

            for c in change:
                code = f"{c} = {x}"
                try:
                    exec(code)
                except Exception as E:
                    raise ValueError(
                        f"Error when running [{code}]. The error was:\n {str(E)}"
                    )

            self.solve_statics()
            result = eval(evaluate)
            print("setting {} results in {}".format(x, result))
            return result - target

        from scipy.optimize import root_scalar

        x0 = initial
        x1 = initial + delta

        if bracket is not None:
            res = root_scalar(set_and_get, x0=x0, x1=x1, bracket=bracket, xtol=tol)
        else:
            res = root_scalar(set_and_get, x0=x0, x1=x1, xtol=tol)

        self._print(res)

        if res.converged:
            return True

        # not converged, but maybe still within tolerance

        # evaluate result
        final_value = eval(evaluate)
        if abs(final_value - target) > tol_out:
            raise ValueError(
                "Target not reached. Target was {}, reached value is {}".format(
                    target, final_value
                )
            )

        return True

    def plot_effect(self, evaluate, change_node, change_property, start, to, steps):
        """Produces a 2D plot with the relation between two properties of the scene. For example the length of a cable
        versus the force in another cable.

        The evaluate argument is processed using "eval" and may contain python code. This may be used to combine multiple
        properties to one value. For example calculate the diagonal load distribution from four independent loads.

        The plot is produced using matplotlob. The plot is produced in the current figure (if any) and plt.show is not executed.

        Args:
            evaluate (str): code to be evaluated to yield the value on the y-axis. Eg: s['poi'].fx Scene is abbiviated as "s"
            change_node(Node or str):  node to be adjusted
            change_property (str): property of that node to be adjusted
            start : left side of the interval
            to : right side of the interval
            steps : number of steps in the interval

        Returns:
            Tuple (x,y) with x and y coordinates

        Examples:
            >>> s.plot_effect("s['cable'].tension", "cable", "length", 11, 14, 10)
            >>> import matplotlib.pyplot as plt
            >>> plt.show()

        """
        s = self
        change_node = self._node_from_node_or_str(change_node)

        # check that the attributes exist and are single numbers
        test = eval(evaluate)

        try:
            float(test)
        except:
            raise ValueError("Evaluation of {} does not result in a float")

        def set_and_get(x):
            setattr(change_node, change_property, x)
            self.solve_statics()
            s = self
            result = eval(evaluate)
            self._print("setting {} results in {}".format(x, result))
            return result

        xs = np.linspace(start, to, steps)
        y = []
        for x in xs:
            y.append(set_and_get(x))

        y = np.array(y)
        import matplotlib.pyplot as plt

        plt.plot(xs, y)
        plt.xlabel("{} of {}".format(change_property, change_node.name))
        plt.ylabel(evaluate)

        return (xs, y)

    # ======== reports =========

    def _validate_reports(self):
        """This method is called whenever a node is deleted. It ultimately triggers the validation of all report sections
        (as those may depend on the node that was deleted)"""

        for report in self.reports:
            report._validate_sections()

    # ======= timelines =====

    def _validate_timelines(self):
        """This method is called whenever a node is deleted"""

        if self.t is not None:
            self.t.validate_node_references()

    # ======== create functions =========

    def new_frame(
        self,
        name,
        parent=None,
        position=None,
        rotation=None,
        inertia=None,
        inertia_radii=None,
        fixed: bool or (bool, bool, bool, bool, bool, bool) = True,
    ) -> Frame:
        """Creates a new *frame* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node
            position: optional, position for the node (x,y,z)
            rotation: optional, rotation for the node (rx,ry,rz)
            intertia: optional, inertia [mT] for node
            inertia_radii: optional, radii (m,m,m) for frame
            fixed [True]: optional, determines whether the frame is fixed [True] or free [False]. May also be a sequence of 6 booleans.

        Returns:
            Reference to newly created frame

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if position is not None:
            assert3f(position, "Position ")
        if rotation is not None:
            assert3f(rotation, "Rotation ")

        if inertia is not None:
            assert1f_positive_or_zero(inertia, "inertia ")

        if inertia_radii is not None:
            assert3f_positive(inertia_radii, "Radii of inertia")
            assert inertia is not None, ValueError(
                "Can not set radii of gyration without specifying inertia"
            )

        if not isinstance(fixed, bool):
            if len(fixed) != 6:
                raise Exception(
                    '"fixed" parameter should either be True/False or a 6x bool sequence such as (True,True,False,False,True,False)'
                )

        # then create
        new_node = Frame(self, name)

        # and set properties
        if b is not None:
            new_node.parent = b
        if position is not None:
            new_node.position = position
        if rotation is not None:
            new_node.rotation = rotation
        if inertia is not None:
            new_node.inertia = inertia
        if inertia_radii is not None:
            new_node.inertia_radii = inertia_radii

        if isinstance(fixed, bool):
            if fixed:
                new_node.set_fixed()
            else:
                new_node.set_free()
        else:
            new_node.fixed = fixed

        # self._nodes.append(new_node)
        return new_node

    def new_component(
        self,
        name,
        path="res: default_component.dave",
        parent=None,
        position=None,
        rotation=None,
        fixed=True,
    ) -> Component:
        """Creates a new *component* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node
            position: optional, position for the node (x,y,z)
            rotation: optional, rotation for the node (rx,ry,rz)
            fixed [True]: optional, determines whether the frame is fixed [True] or free [False]. May also be a sequence of 6 booleans.
            path: component resource (.dave file)

        Returns:
            Reference to newly created component

        """

        # check if we can import the provided path
        try:
            filename = self.get_resource_path(path)
        except Exception as E:
            raise ValueError(
                f'Error creating component {name}.\nCan not find  path "{path}"; \n {str(E)}'
            )
        try:
            t = Scene(
                filename=filename,
                resource_provider=self.resource_provider,
            )
        except Exception as E:
            raise ValueError(
                f'Error creating component {name}.\nCan not import "{filename}" because {str(E)}'
            )

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if position is not None:
            assert3f(position, "Position ")
        if rotation is not None:
            assert3f(rotation, "Rotation ")

        if not isinstance(fixed, bool):
            if len(fixed) != 6:
                raise Exception(
                    '"fixed" parameter should either be True/False or a 6x bool sequence such as (True,True,False,False,True,False)'
                )

        # then create
        new_node = Component(self, name)

        # and set properties
        if b is not None:
            new_node.parent = b
        if position is not None:
            new_node.position = position
        if rotation is not None:
            new_node.rotation = rotation
        if isinstance(fixed, bool):
            if fixed:
                new_node.set_fixed()
            else:
                new_node.set_free()
        else:
            new_node.fixed = fixed

        new_node.path = path

        # self._nodes.append(new_node)
        return new_node

    def new_geometriccontact(
        self,
        name,
        child,
        parent,
        inside=False,
        swivel=None,
        rotation_on_parent=None,
        child_rotation=None,
        swivel_fixed=True,
        fixed_to_parent=False,
        child_fixed=False,
    ) -> GeometricContact:
        """Creates a new *new_geometriccontact* node and adds it to the scene.

        Geometric contact connects two circular elements and can be used to model bar-bar connections or pin-in-hole connections.

        By default a bar-bar connection is created between item1 and item2.

        Args:
            name: Name for the node, should be unique
            child : [Sheave] will be the nodeA of the connection
            parent : [Sheave] will be the nodeB of the connection
            inside: [False] False creates a pinpin connection. True creates a pin-hole type of connection
            swivel: Rotation angle between the two items. Defaults to 90 for pinpin and 0 for pin-hole
            rotation_on_parent: Angle of the connecting hinge relative to nodeA or None for default
            child_rotation: Angle of the nodeB relative to the connecting hinge or None for default
            swivel_fixed: Fix swivel [True]
            fixed_to_parent: Fix connecting hinge to nodeA [False]
            child_fixed: Fix nodeB to connecting hinge [False]

        Note:
            For pin-hole connections there is no geometrical difference between the pin and the hole. Therefore it is not needed to specify
            which is the pin and which is the hole

        Returns:
            Reference to newly created new_geometriccontact

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)

        name_prefix = name + MANAGED_NODE_IDENTIFIER
        postfixes = [
            "_axis_on_parent",
            "_pin_hole_connection",
            "_axis_on_child",
            "_connection_axial_rotation",
        ]

        for pf in postfixes:
            self._verify_name_available(name_prefix + pf)

        child = self._sheave_from_node(child)
        parent = self._sheave_from_node(parent)

        assertBool(inside, "inside")
        assertBool(swivel_fixed, "swivel_fixed")
        assertBool(fixed_to_parent, "fixed_to_parent")
        assertBool(child_fixed, "child_fixed")

        GeometricContact._assert_parent_child_possible(parent, child)

        if swivel is None:
            if inside:
                swivel = 0
            else:
                swivel = 90

        assert1f(swivel, "swivel_angle")

        if rotation_on_parent is not None:
            assert1f(rotation_on_parent, "rotation_on_parent should be either None or ")
        if child_rotation is not None:
            assert1f(child_rotation, "child_rotation should be either None or ")

        if child is None:
            raise ValueError("child needs to be a sheave-type node")
        if parent is None:
            raise ValueError("parent needs to be a sheave-type node")

        if child.parent.parent is None:
            raise ValueError(
                f"The parent {child.parent.name} of the child item {child.name} is not located on an axis. Can not create the connection because there is no axis to nodeB"
            )

        if child.parent.parent.manager is not None:
            self.print_node_tree()
            raise ValueError(
                f"The axis or body that {child.name} is on is already managed by {child.parent.parent.manager.name} and can therefore not be changed - unable to create geometric contact"
            )

        new_node = GeometricContact(self, name, child, parent)
        if inside:
            new_node.set_pin_in_hole_connection()
        else:
            new_node.set_pin_pin_connection()

        new_node.swivel = swivel
        if rotation_on_parent is not None:
            new_node.rotation_on_parent = rotation_on_parent
        if child_rotation is not None:
            new_node.child_rotation = child_rotation

        new_node.fixed_to_parent = fixed_to_parent
        new_node.child_fixed = child_fixed
        new_node.swivel_fixed = swivel_fixed

        return new_node

    def new_waveinteraction(
        self,
        name,
        path,
        parent=None,
        offset=None,
    ) -> WaveInteraction1:
        """Creates a new *wave interaction* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            path: Path to the hydrodynamic database
            parent: optional, name of the parent of the node
            offset: optional, position for the node (x,y,z)

        Returns:
            Reference to newly created wave-interaction object

        """

        if not parent:
            raise ValueError("Wave-interaction has to be located on an Axis")

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if b is None:
            raise ValueError("Wave-interaction has to be located on an Axis")

        if offset is not None:
            assert3f(offset, "Offset ")

        self.get_resource_path(path)  # raises error when resource is not found

        # then create
        new_node = WaveInteraction1(self, name)

        new_node.path = path
        new_node.parent = parent

        # and set properties
        new_node.parent = b
        if offset is not None:
            new_node.offset = offset

        return new_node

    def new_visual(
        self, name, path, parent=None, offset=None, rotation=None, scale=None
    ) -> Visual:
        """Creates a new *Visual* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            path: Path to the resource
            parent: optional, name of the parent of the node
            offset: optional, position for the node (x,y,z)
            rotation: optional, rotation for the node (rx,ry,rz)
            scale : optional, scale of the visual (x,y,z).

        Returns:
            Reference to newly created visual

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if offset is not None:
            assert3f(offset, "Offset ")
        if rotation is not None:
            assert3f(rotation, "Rotation ")

        self.get_resource_path(path)  # raises error when resource is not found

        # then create

        new_node = Visual(self, name)

        new_node.name = name
        new_node.path = path
        new_node.parent = parent

        # and set properties
        if b is not None:
            new_node.parent = b
        if offset is not None:
            new_node.offset = offset
        if rotation is not None:
            new_node.rotation = rotation
        if scale is not None:
            new_node.scale = scale

        # self._nodes.append(new_node)
        return new_node

    def new_point(self, name, parent=None, position=None) -> Point:
        """Creates a new *poi* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node
            position: optional, position for the node (x,y,z)


        Returns:
            Reference to newly created poi

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if position is not None:
            assert3f(position, "Position ")

        # then create
        new_node = Point(self, name)

        # and set properties
        if b is not None:
            new_node.parent = b
        if position is not None:
            new_node.position = position

        # self._nodes.append(new_node)
        return new_node

    def new_rigidbody(
        self,
        name: str,
        mass: float = 0,
        cog: (float, float, float) = (0, 0, 0),
        parent=None,
        position=None,
        rotation=None,
        inertia_radii=None,
        fixed: bool or (bool, bool, bool, bool, bool, bool) = True,
    ) -> RigidBody:
        """Creates a new *rigidbody* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            mass: optional, [0] mass in mT
            cog: optional, (0,0,0) cog-position in (m,m,m)
            parent: optional, name of the parent of the node
            position: optional, position for the node (x,y,z)
            rotation: optional, rotation for the node (rx,ry,rz)
            inertia_radii : optional, radii of gyration (rxx,ryy,rzz); only used for dynamics
            fixed [True]: optional, determines whether the frame is fixed [True] or free [False]. May also be a sequence of 6 booleans.

        Examples:
            scene.new_rigidbody("heavy_thing", mass = 10000, cog = (1.45, 0, -0.7))

        Returns:
            Reference to newly created RigidBody

        """

        # check input
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if position is not None:
            assert3f(position, "Position ")
        if rotation is not None:
            assert3f(rotation, "Rotation ")

        if inertia_radii is not None:
            assert3f_positive(inertia_radii, "Radii of inertia")

            if not mass > 0:
                warnings.warn(
                    f"Can not set radii of gyration without specifying mass - ignoring radii of gyration for {name}"
                )
                inertia_radii = None

        if not isinstance(fixed, bool):
            if len(fixed) != 6:
                raise Exception(
                    '"fixed" parameter should either be True/False or a 6x bool sequence such as (True,True,False,False,True,False)'
                )

        r = RigidBody(self, name)

        r.cog = cog  # set inertia
        r.mass = mass

        # and set properties
        if b is not None:
            r.parent = b
        if position is not None:
            r.position = position
        if rotation is not None:
            r.rotation = rotation

        if inertia_radii is not None:
            r.inertia_radii = inertia_radii

        if isinstance(fixed, bool):
            if fixed:
                r.set_fixed()
            else:
                r.set_free()
        else:
            r.fixed = fixed

        # self._nodes.append(r)
        return r

    def new_cable(
        self,
        name,
        endA=None,
        endB=None,
        length=None,
        EA=0,
        diameter: float = 0,
        sheaves=None,
        mass=None,
        connections=None,
        reversed=None,
        mass_per_length=None,
        friction=None,
        offsets=None,
    ) -> Cable:
        """Creates a new *cable* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            endA : A Poi element to connect the first end of the cable to
            endB : A Poi element to connect the other end of the cable to
            length [-1] : un-stretched length of the cable in m; default [-1] create a cable with the current distance between the endpoints A and B
            EA [0] : stiffness of the cable in kN/m; default
            mass [0] or mass_per_length [0] : mass of the cable - warning: only valid if tension in cable > 10x cable weight.
            mass_per_length [alternative for mass]
            sheaves : [optional] A list of pois, these are sheaves that the cable runs over. Defined from endA to endB
            connections [optional] : Alternative to [EndA, sheaves, EndB]
            reversed [optional] : Reversed property for each of the connections
            friction : [optional] A list of friction coefficients for each connection. aligned with connection
            offsets : [optional] A list of offsets for each connection. aligned with connection

            connections: May be used instead of endA, endB and sheaves. If connections is provided then endA = connections[0], endB = connections[-1] and sheaves = connections[1:-1]

        Examples:

            scene.new_cable('cable_name' endA='poi_start', endB = 'poi_end')  # minimal use

            scene.new_cable('cable_name', length=50, EA=1000, endA=poi_start, endB = poi_end, sheaves=[sheave1, sheave2])

            scene.new_cable('cable_name', length=50, EA=1000, endA='poi_start', endB = 'poi_end', sheaves=['single_sheave']) # also a single sheave needs to be provided as a list

        Notes:
            - The default options for length and EA can be used to measure distances between points
            - Cable mass is only valid for cables under high tension, for example lifting slings, when cable tension > 10x cable weight.

        Returns:
            Reference to newly created Cable

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        if length is not None:
            assert1f(length, "length")
        assert1f(EA, "EA")

        # check if connections is supplied
        if connections is not None:
            if endA is not None:
                warnings.warn(
                    "provided EndA will not be used, it is overwritten by connections"
                )
            if endB is not None:
                warnings.warn(
                    "provided EndB will not be used, it is overwritten by connections"
                )
            if sheaves is not None:
                warnings.warn(
                    "provided sheaves will not be used, it is overwritten by connections"
                )

            endA = connections[0]
            endB = connections[-1]
            sheaves = connections[1:-1]

        endA = self._poi_or_sheave_from_node(endA)
        endB = self._poi_or_sheave_from_node(endB)

        pois = [endA]
        if sheaves is not None:
            if isinstance(sheaves, Point):  # single sheave as poi or string
                sheaves = [sheaves]

            if isinstance(sheaves, Circle):  # single sheave as poi or string
                sheaves = [sheaves]

            if isinstance(sheaves, str):
                sheaves = [sheaves]

            for s in sheaves:
                # s may be a poi or a sheave
                pois.append(self._poi_or_sheave_from_node(s))

        pois.append(endB)

        # default options
        if length is not None:
            if length < 0:
                raise ValueError("Length should be >= 0")

            if length < 1e-9:
                if EA > 0:
                    raise ValueError("Length should be more than 0 (if EA>0)")

        if EA < 0:
            raise ValueError(f"EA should be >= 0, not {EA}")

        assert1f(diameter, "Diameter should be a number >= 0")

        if diameter < 0:
            raise Exception("Diameter should be >= 0")

        if mass is None and mass_per_length is None:
            mass_per_length = 0
        elif mass is not None and mass_per_length is not None:
            raise ValueError("Can not provide both mass and mass_per_length")

        if mass_per_length is not None:
            assert1f(mass_per_length, "mass per length")

        if mass is not None:
            assert1f(mass, "mass")

        if friction is not None:
            req_len = len(pois) - 2
            is_loop = False
            if connections[0] == connections[-1]:
                is_loop = True
                req_len += 1

            if is_loop:
                assert (
                    len(friction) == req_len
                ), f"friction (for a loop) should be a list with the same length as the number of unique connections (={req_len}), got {len(friction)}"
            else:
                assert (
                    len(friction) == req_len
                ), "friction should be a list with the same length as the number of intermediate points/circles (={req_len}), got {len(friction)}"

            for _ in friction:
                assert isinstance(
                    _, (float, int, type(None))
                ), "friction should be a list with floats or None"

        if reversed is not None:
            assert len(reversed) == len(
                pois
            ), "reversed should be a list with the same length as the number of connections"
            for _ in reversed:
                assert isinstance(_, bool), "reversed should be a list with booleans"

        if offsets is not None:
            assert len(offsets) == len(
                pois
            ), "offsets should be a list with the same length as the number of connections"
            for _ in offsets:
                assert isinstance(
                    _, (float, int)
                ), "offsets should be a list with floats"

        # then create

        new_node = Cable(self, name)

        try:
            if length is not None:
                new_node.length = length
            else:
                new_node.length = 1e-8  # set dummy length

            new_node.EA = EA

            new_node.diameter = diameter

            new_node.connections = pois

            if friction is not None:
                new_node.friction = friction

            if reversed is not None:
                new_node.reversed = reversed

            if offsets is not None:
                new_node.offsets = offsets

            # and add to the scene
            # self._nodes.append(new_node)

            if length is None:
                self._vfc.state_update()
                new_length = new_node.stretch + 1e-8

                if new_length > 0:
                    new_node.length = new_length
                else:
                    # is is possible that all nodes are at the same location which means the total length becomes 0
                    raise ValueError(
                        "No lengh has been supplied and all connection points are at the same location - unable to determine a non-zero default length. Please supply a length"
                    )

            if mass is not None:
                mass_per_length = mass / new_node.length

            new_node.mass_per_length = mass_per_length

            new_node.update()

        except Exception as E:
            # remove created node
            self.delete(new_node.name)
            raise E

        # set contact parameters
        try:
            new_node._vfNode.contact_distance  # only available if the core supports it
            new_node._vfNode.contact_distance = 0
            new_node._vfNode.contact_k1 = 1000
            new_node._vfNode.contact_k2 = 0
        except:
            pass

        return new_node

    def new_force(
        self, name, parent=None, local=False, force=None, moment=None
    ) -> Force:
        """Creates a new *force* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Poi]
            local: optional, if True the force is applied in the local coordinate system of the parent
            force: optional, global force on the node (x,y,z)
            moment: optional, global force on the node (x,y,z)


        Returns:
            Reference to newly created force

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._poi_from_node(parent)

        if force is not None:
            assert3f(force, "Force ")

        if moment is not None:
            assert3f(moment, "Moment ")

        assertBool(local, "Local property")

        # then create
        new_node = Force(self, name)

        # and set properties
        if b is not None:
            new_node.parent = b
        if force is not None:
            new_node.force = force
        if moment is not None:
            new_node.moment = moment

        new_node.local = local

        # self._nodes.append(new_node)
        return new_node

    def _new_area(self, is_wind, name, parent, direction, Cd, A, areakind):
        """Creates a new WindArea* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Poi]
            Cd : Cd-coefficient
            A  : Area
            kind : interpretation of the direction (Area.PLANE, AREA.SPHERE, AREA.CYLINDER)
            direction : direction of the area

        Returns:
            Reference to newly created wind area

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._poi_from_node(parent)

        assert3f(direction, "Direction ")
        assert np.linalg.norm(direction) > 0, ValueError("Direction shall not be 0,0,0")
        assert1f_positive_or_zero(Cd, "Cd coefficient")
        assert1f_positive_or_zero(A, "Area ")
        assert isinstance(areakind, AreaKind)

        if is_wind:
            new_node = WindArea(self, name)
        else:
            new_node = CurrentArea(self, name)

        # and set properties
        if b is not None:
            new_node.parent = b
        new_node.areakind = areakind
        new_node.direction = direction
        new_node.Cd = Cd
        new_node.A = A

        return new_node

    def new_windarea(
        self,
        name,
        parent=None,
        direction=(0, 1, 0),
        Cd=2,
        A=10,
        areakind=AreaKind.PLANE,
    ) -> WindArea:
        """Creates a new *WindArea* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Poi]
            Cd : Cd-coefficient
            A  : Area
            kind : interpretation of the direction (Area.PLANE, AREA.SPHERE, AREA.CYLINDER)
            direction : direction of the area

        Returns:
            Reference to newly created wind area

        """

        return self._new_area(
            True,
            name=name,
            parent=parent,
            direction=direction,
            Cd=Cd,
            A=A,
            areakind=areakind,
        )

    def new_currentarea(
        self,
        name,
        parent=None,
        direction=(0, 1, 0),
        Cd=2,
        A=10,
        areakind=AreaKind.PLANE,
    ) -> CurrentArea:
        """Creates a new *CurrentArea* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Poi]
            Cd : Cd-coefficient
            A  : Area
            kind : interpretation of the direction (Area.PLANE, AREA.SPHERE, AREA.CYLINDER)
            direction : direction of the area

        Returns:
            Reference to newly created wind area

        """

        return self._new_area(
            False,
            name=name,
            parent=parent,
            direction=direction,
            Cd=Cd,
            A=A,
            areakind=areakind,
        )

    def new_circle(self, name, parent, axis, radius=0.0, roundbar=False) -> Circle:
        """Creates a new *sheave* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Poi]
            axis: direction of the axis of rotation (x,y,z)
            radius: optional, radius of the sheave
            roundbar: optional, circle is a roundbar (cylinder)


        Returns:
            Reference to newly created Circle

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._poi_from_node(parent)

        assert3f(axis, "Axis of rotation ")

        assert1f(radius, "Radius of sheave")
        assertBool(roundbar, "Roundbar property")

        new_node = Circle(self, name)

        # and set properties
        new_node.parent = b
        new_node.axis = axis
        new_node.radius = radius
        new_node.is_roundbar = roundbar

        # self._nodes.append(new_node)
        return new_node

    def new_hydspring(
        self,
        name,
        parent,
        cob,
        BMT,
        BML,
        COFX,
        COFY,
        kHeave,
        waterline,
        displacement_kN,
    ) -> HydSpring:
        """Creates a new *hydspring* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Axis]
            cob: position of the CoB (x,y,z) in the parent axis system
            BMT: Vertical distance between CoB and meta-center for roll
            BML: Vertical distance between CoB and meta-center for pitch
            COFX: X-location of center of flotation (center of waterplane) relative to CoB
            COFY: Y-location of center of flotation (center of waterplane) relative to CoB
            kHeave : heave stiffness (typically Awl * rho * g)
            waterline : Z-position (elevation) of the waterline relative to CoB
            displacement_kN : displacement (typically volume * rho * g)


        Returns:
            Reference to newly created hydrostatic spring

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)
        assert3f(cob, "CoB ")
        assert1f(BMT, "BMT ")
        assert1f(BML, "BML ")
        assert1f(COFX, "COFX ")
        assert1f(COFY, "COFY ")
        assert1f(kHeave, "kHeave ")
        assert1f(waterline, "waterline ")
        assert1f(displacement_kN, "displacement_kN ")

        # then create

        new_node = HydSpring(self, name)

        new_node.cob = cob
        new_node.parent = b
        new_node.BMT = BMT
        new_node.BML = BML
        new_node.COFX = COFX
        new_node.COFY = COFY
        new_node.kHeave = kHeave
        new_node.waterline = waterline
        new_node.displacement_kN = displacement_kN

        # self._nodes.append(new_node)

        return new_node

    def new_linear_connector_6d(self, name, secondary, main, stiffness=None) -> LC6d:
        """Creates a new *linear connector 6d* node and adds it to the scene. The node connects secondary to main.

        Args:
            name: Name for the node, should be unique
            main: Main axis system [Axis]
            secondary: Secondary axis system [Axis]
            stiffness: optional, connection stiffness (x,y,z, rx,ry,rz)

        See :py:class:`LC6d` for details

        Returns:
            Reference to newly created connector

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        m = self._parent_from_node(main)
        s = self._parent_from_node(secondary)

        if stiffness is not None:
            assert6f(stiffness, "Stiffness ")
        else:
            stiffness = (0, 0, 0, 0, 0, 0)

        # then create
        new_node = LC6d(self, name)

        # and set properties
        new_node.main = m
        new_node.secondary = s
        new_node.stiffness = stiffness

        return new_node

    def new_connector2d(
        self, name, nodeA, nodeB, k_linear=0, k_angular=0
    ) -> Connector2d:
        """Creates a new *new_connector2d* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            nodeB: First axis system [Axis]
            nodeA: Second axis system [Axis]

            k_linear : linear stiffness in kN/m
            k_angular : angular stiffness in kN*m / rad

        Returns:
            Reference to newly created connector2d

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        m = self._parent_from_node(nodeA)
        s = self._parent_from_node(nodeB)

        assert1f(k_linear, "Linear stiffness")
        assert1f(k_angular, "Angular stiffness")

        # then create
        new_node = Connector2d(self, name)

        # and set properties
        new_node.nodeA = m
        new_node.nodeB = s
        new_node.k_linear = k_linear
        new_node.k_angular = k_angular

        return new_node

    def new_beam(
        self,
        name,
        nodeA,
        nodeB,
        EIy=0,
        EIz=0,
        GIp=0,
        EA=0,
        L=None,
        mass=0,
        n_segments=1,
        tension_only=False,
    ) -> Beam:
        """Creates a new *beam* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            nodeA: First axis system [Axis]
            nodeB: Second axis system [Axis]

            All stiffness terms default to 0
            The length defaults to the distance between nodeA and nodeB


        See :py:class:`LinearBeam` for details

        Returns:
            Reference to newly created beam

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        m = self._parent_from_node(nodeA)
        s = self._parent_from_node(nodeB)

        if L is None:
            L = np.linalg.norm(
                np.array(m.global_position) - np.array(s.global_position)
            )
        else:
            if L <= 0:
                raise ValueError("L should be > 0 as stiffness is defined per length.")

        assert1f_positive_or_zero(EIy, "EIy should be >= 0")
        assert1f_positive_or_zero(EIz, "EIz should be >= 0")
        assert1f_positive_or_zero(GIp, "GIp should be >= 0")
        assert1f_positive_or_zero(EA, "EA should be >= 0")
        assertBool(tension_only, "tension_only should be bool")
        assert1f(mass, "Mass shall be a number")
        n_segments = int(round(n_segments))

        # then create

        new_node = Beam(self, name)

        # and set properties
        new_node.nodeA = m
        new_node.nodeB = s
        new_node.EIy = EIy
        new_node.EIz = EIz
        new_node.GIp = GIp
        new_node.EA = EA
        new_node.L = L
        new_node.mass = mass
        new_node.n_segments = n_segments
        new_node.tension_only = tension_only

        # self._nodes.append(new_node)
        return new_node

    def new_buoyancy(self, name, parent=None) -> Buoyancy:
        """Creates a new *buoyancy* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node


        Returns:
            Reference to newly created buoyancy

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if b is None:
            raise ValueError("A valid parent must be defined for a Buoyancy node")

        # then create
        new_node = Buoyancy(self, name)

        # and set properties
        if b is not None:
            new_node.parent = b

        return new_node

    def new_tank(self, name, parent=None, density=1.025, free_flooding=False) -> Tank:
        """Creates a new *tank* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node

        Returns:
            Reference to newly created Tank

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if b is None:
            raise ValueError("A valid parent must be defined for a Tank")

        assert isinstance(free_flooding, bool), ValueError(
            "free_flooding shall be True or False"
        )

        assert1f(density, "density")

        # then create
        new_node = Tank(self, name)
        new_node.density = density

        # and set properties
        if b is not None:
            new_node.parent = b

        new_node.free_flooding = free_flooding

        # self._nodes.append(new_node)
        return new_node

    def new_contactmesh(self, name, parent=None) -> ContactMesh:
        """Creates a new *contactmesh* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node

        Returns:
            Reference to newly created contact mesh

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        # then create
        new_node = ContactMesh(self, name)

        # and set properties
        if b is not None:
            new_node.parent = b

        # self._nodes.append(new_node)
        return new_node

    def new_spmt(
        self,
        name,
        parent,
        reference_force=0,
        reference_extension=1.5,
        k=1e5,
        spacing_length=1.4,
        spacing_width=1.45,
        n_length=6,
        n_width=2,
        meshes=None,
        use_friction=False,
    ) -> SPMT:
        """Creates a new *SPMT* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Axis]
            reference_force : total force (sum of all axles) when at reference extension [kN]
            reference_extension : nominal extension of axles for reference force [m]
            k : force variation as result of average axle extension relative to reference_extension
            spacing_length : distance between axles in length direction
            spacing_width : distance between axles in tranverse direction
            n_length : number of axles in length direction
            n_width : number of axles in transverse direction
            meshes : [] List of contact meshes that the SPMT sees. If empty then the SPMT sees all contact meshes.
            use_friction : (True) Use friction


        Returns:
            Reference to newly created SPMT

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        parent = self._node_from_node_or_str(parent)
        assert isinstance(parent, Frame), ValueError(
            f"Parent should be an axis system or derived, not a {type(parent)}"
        )

        assert1f_positive_or_zero(reference_force, "reference force")
        assert1f_positive_or_zero(reference_extension, "reference extension")
        assert1f_positive(k, "stiffness (k)")
        assert1f_positive(spacing_length, "spacing length")
        assert1f_positive(spacing_width, "spacing width")
        assert1f_positive(n_length, "n-length")
        assert1f_positive(n_width, "n-width")
        assertBool(use_friction, "use_friction")

        if meshes is not None:
            meshes = make_iterable(meshes)
            for mesh in meshes:
                test = self._node_from_node(
                    mesh, ContactMesh
                )  # throws error if not found

        # then create

        new_node = SPMT(self, name)

        # and set properties
        new_node.parent = parent

        new_node._reference_force = reference_force
        new_node._reference_extension = reference_extension
        new_node._k = k
        new_node._spacing_length = spacing_length
        new_node._spacing_width = spacing_width
        new_node._n_length = n_length
        new_node._n_width = n_width
        new_node.use_friction = use_friction
        new_node._update_vfNode()

        if meshes is not None:
            new_node.meshes = meshes

        # self._nodes.append(new_node)
        return new_node

    def new_contactball(
        self, name, parent=None, radius=1, k=9999, meshes=None
    ) -> ContactBall:
        """Creates a new *force* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Poi]
            force: optional, global force on the node (x,y,z)
            moment: optional, global force on the node (x,y,z)


        Returns:
            Reference to newly created force

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._poi_from_node(parent)

        assert1f_positive_or_zero(radius, "Radius ")
        assert1f_positive_or_zero(k, "k ")

        if meshes is not None:
            meshes = make_iterable(meshes)
            for mesh in meshes:
                test = self._node_from_node(mesh, ContactMesh)

        # then create
        new_node = ContactBall(self, name)

        # and set properties
        if b is not None:
            new_node.parent = b
        if k is not None:
            new_node.k = k
        if radius is not None:
            new_node.radius = radius

        if meshes is not None:
            new_node.meshes = meshes

        # self._nodes.append(new_node)
        return new_node

    def new_ballastsystem(self, name, parent: Frame or str) -> BallastSystem:
        """Creates a new *rigidbody* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the ballast system (ie: the vessel axis system)

        Examples:
            scene.new_ballastsystem("cheetah_ballast", parent="Cheetah")

        Returns:
            Reference to newly created BallastSystem

        """

        # check input
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        parent = self._parent_from_node(parent)  # handles verification of type as well

        # make elements
        r = BallastSystem(self, name)
        r.parent = parent

        return r

    # def new_sling(
    #     self,
    #     name,
    #     length: float = -1,
    #     EA=None,
    #     mass=0.1,
    #     endA=None,
    #     endB=None,
    #     LeyeA=None,
    #     LeyeB=None,
    #     LspliceA=None,
    #     LspliceB=None,
    #     diameter=0.1,
    #     sheaves=None,
    #     k_total=None,
    # ) -> Sling:
    #     """
    #     Creates a new sling, adds it to the scene and returns a reference to the newly created object.
    #
    #     See Also:
    #         Sling
    #
    #     Args:
    #         name:    name
    #         length:  length of the sling [m], defaults to distance between endpoints
    #         EA:      stiffness in kN, default: 1.0 (note: equilibrium will fail if mass >0 and EA=0)
    #         k_total: stiffness in kN/m, default: None
    #         mass:    mass in mT, default  0.1
    #         endA:    element to connect end A to [poi, circle]
    #         endB:    element to connect end B to [poi, circle]
    #         LeyeA:   inside eye on side A length [m], defaults to 1/6th of length
    #         LeyeB:   inside eye on side B length [m], defaults to 1/6th of length
    #         LspliceA: splice length on side A [m] (the part where the cable is connected to itself)
    #         LspliceB: splice length on side B [m] (the part where the cable is connected to itself)
    #         diameter: cable diameter in m, defaul to 0.1
    #         sheaves:  optional: list of sheaves/pois that the sling runs over
    #
    #     Returns:
    #         a reference to the newly created Sling object.
    #
    #     """
    #
    #     # first check
    #     assertValidName(name)
    #     self._verify_name_available(name)
    #
    #     name_prefix = name + MANAGED_NODE_IDENTIFIER
    #     postfixes = [
    #         "_spliceA",
    #         "_spliceA",
    #         "_spliceA2",
    #         "_spliceAM",
    #         "_spliceA_visual",
    #         "spliceB",
    #         "_spliceB1",
    #         "_spliceB2",
    #         "_spliceBM",
    #         "_spliceB_visual",
    #         "_main_part",
    #         "_eyeA",
    #         "_eyeB",
    #     ]
    #
    #     for pf in postfixes:
    #         self._verify_name_available(name_prefix + pf)
    #
    #     endA = self._poi_or_sheave_from_node(endA)
    #     endB = self._poi_or_sheave_from_node(endB)
    #
    #     if length == -1:  # default
    #         if endA is None or endB is None:
    #             raise ValueError(
    #                 "Length for cable is not provided, so defaults to distance between endpoints; but at least one of the endpoints is None."
    #             )
    #
    #         length = np.linalg.norm(
    #             np.array(endA.global_position) - np.array(endB.global_position)
    #         )
    #
    #     if LeyeA is None:  # default
    #         LeyeA = length / 6
    #     if LeyeB is None:  # default
    #         LeyeB = length / 6
    #     if LspliceA is None:  # default
    #         LspliceA = length / 6
    #     if LspliceB is None:  # default
    #         LspliceB = length / 6
    #
    #     if sheaves is None:
    #         sheaves = []
    #
    #     if EA is not None and k_total is not None:
    #         warnings.warn(
    #             "Value for EA is given by will not be used as k_total is defined as well. Value for EA will be derived from k_total"
    #         )
    #
    #     if EA is None:
    #         EA = 1  # possibly overwritten by k_total
    #
    #     assert1f_positive_or_zero(diameter, "Diameter")
    #     assert1f_positive_or_zero(mass, "mass")
    #
    #     assert1f_positive(length, "Length")
    #     assert1f_positive(LeyeA, "length of eye A")
    #     assert1f_positive(LeyeB, "length of eye B")
    #     assert1f_positive(LspliceA, "length of splice A")
    #     assert1f_positive(LspliceB, "length of splice B")
    #
    #     if k_total is not None:
    #         assert1f_positive_or_zero(k_total, "Total stiffness (k_total)")
    #
    #     for s in sheaves:
    #         _ = self._poi_or_sheave_from_node(s)
    #
    #     # then make element
    #     # __init__(self, scene, name, Ltotal, LeyeA, LeyeB, LspliceA, LspliceB, diameter, EA, mass, endA = None, endB=None, sheaves=None):
    #
    #     node = Sling(
    #         scene=self,
    #         name=name,
    #         length=length,
    #         LeyeA=LeyeA,
    #         LeyeB=LeyeB,
    #         LspliceA=LspliceA,
    #         LspliceB=LspliceB,
    #         diameter=diameter,
    #         EA=EA,
    #         mass=mass,
    #         endA=endA,
    #         endB=endB,
    #         sheaves=sheaves,
    #     )
    #
    #     if k_total is not None:
    #         node.k_total = k_total
    #
    #     # self._nodes.append(node)
    #
    #     return node

    def new_shackle(self, name, kind="GP500"):
        """
        Creates a new shackle, adds it to the scene and returns a reference to the newly created object.

        See Also:
            Shackle

        Args:
            name:   name
            kind:  type of shackle; eg 'GP500'


        Returns:
            a reference to the newly created Shackle object.

        """

        # first check
        assertValidName(name)
        self._verify_name_available(name)

        name_prefix = name + MANAGED_NODE_IDENTIFIER
        postfixes = [
            "/body",
            "/pin_point",
            "/bow_point",
            "/inside_circle_center",
            "/inside",
            "/visual",
        ]
        for pf in postfixes:
            self._verify_name_available(name_prefix + pf)

        try:
            from DAVE_rigging import Shackle
        except ImportError:
            raise ImportError(
                "DAVE_rigging extension not found. This extension is needed to create a shackle."
            )

        warnings.warn("Using depricated function new_shackle. Use Shackle instead")

        # then make element
        node = Shackle(scene=self, name=name, kind=kind)

        return node

    def print_python_code(self):
        """Prints the python code that generates the current scene

        See also: give_python_code
        """
        for line in self.give_python_code().split("\n"):
            print(line)

    def give_python_code(
        self,
        nodes=None,
        export_environment_settings=True,
        _no_sort_nodes=False,
        state_only=False,
        no_reports=False,
        no_timeline=False,
    ):
        """Generates the python code that rebuilds the scene and elements in its current state.

        Args:
            nodes [None] : generate only for these node(s)
            export_environment_settings [True] : export the environment (wind, gravity, etc)
            _no_sort_nodes [False] : skip sorting of nodes (use if sure that nodes are already sorted)
            state_only [False] : nodes and settings only, no timelines, reports etc
        """

        import datetime
        import getpass

        if not _no_sort_nodes:
            self.sort_nodes_by_dependency()

        if nodes is None:
            nodes_to_be_exported = self._nodes
        else:
            nodes_to_be_exported = [node for node in self._nodes if node in nodes]

        code = []
        code.append("# auto generated python code")
        try:
            code.append("# By {}".format(getpass.getuser()))
        except:
            code.append("# By an unknown")

        code.append("# Time: {} UTC".format(str(datetime.datetime.now()).split(".")[0]))

        if self._export_code_with_solved_function:
            code.append(
                "\n# To be able to distinguish the important number (eg: fixed positions) from"
            )
            code.append(
                "# non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'."
            )
            code.append(
                "# For anything written as solved(number) that actual number does not influence the static solution"
            )
            code.append("\ndef solved(number):\n    return number\n")

        if export_environment_settings:
            code.append("\n# Environment settings")

            for prop in ds.ENVIRONMENT_PROPERTIES:
                code.append(f"s.{prop} = {getattr(self, prop)}")

        non_default_solver_settings = self.solver_settings.non_default_props()
        if non_default_solver_settings:
            code.append("\n# Solver settings (non-default values)")
            for prop in non_default_solver_settings:
                code.append(
                    f"s.solver_settings.{prop} = {getattr(self.solver_settings, prop)}"
                )

        code.append("\n")

        for n in nodes_to_be_exported:
            if n._manager is None:
                code.append("\n" + n.give_python_code())
            else:
                # check if one of the managers creates this node
                manager = n._manager
                while True:
                    if manager.creates(n):
                        break
                    else:
                        if manager._manager is None:
                            code.append("\n" + n.give_python_code())
                            break
                        else:
                            manager = manager._manager

                # print(f'skipping {n.name} ')

        if not state_only:
            # store the visibility code separately

            for n in nodes_to_be_exported:
                if not n.visible:
                    code.append(
                        f"\ns['{n.name}']._visible = False"  # use private, cause may be managed (in which case this statement is probably obsolete)
                    )  # only report is not the default value

            code.append("\n# Limits")

            for n in nodes_to_be_exported:
                if n.manager is None:
                    for key, value in n.limits.items():
                        code.append(f"s['{n.name}'].limits['{key}'] = {value}")
                else:
                    # Limits of managed nodes are only exported if they have been overridden
                    # or are additional.
                    # This is traced using the _limits_by_manager dict

                    lbm = getattr(n, "_limits_by_manager", None)
                    if lbm is not None:
                        for key, value in n.limits.items():
                            if key not in lbm:
                                code.append(
                                    f"s['{n.name}'].limits['{key}'] = {value}  # additional limit on managed node"
                                )
                            else:
                                if value != lbm[key]:
                                    code.append(
                                        f"s['{n.name}'].limits['{key}'] = {value}  # limit overridden"
                                    )
                    else:
                        warnings.warn(
                            f"Managed node {n.name} does not have _limits_by_manager set"
                        )

            code.append("\n# Watches")

            for n in nodes_to_be_exported:
                if n.manager is None:
                    for key, value in n.watches.items():
                        code.append(f"s['{n.name}'].watches['{key}'] = {value}")
                else:
                    # Watches of managed nodes are only exported if they have been overridden
                    # or are additional.
                    # This is traced using the _watches_by_manager dict

                    lbm = getattr(n, "_watches_by_manager", None)
                    if lbm is not None:
                        for key, value in n.watches.items():
                            if key not in lbm:
                                code.append(
                                    f"s['{n.name}'].watches['{key}'] = {value}  # watch limit on managed node"
                                )
                            else:
                                if value != lbm[key]:
                                    code.append(
                                        f"s['{n.name}'].watches['{key}'] = {value}  # watch overridden"
                                    )
                                else:
                                    pass  # watch set by manager, so do not export
                    else:
                        logging.info(
                            f"Managed node {n.name} does not have _watches_by_manager set"
                        )

            code.append("\n# Tags")

            for n in nodes_to_be_exported:
                if n.tags:
                    code.append(f"s['{n.name}'].add_tags({n.tags})")

            code.append("\n# Colors")

            for n in nodes_to_be_exported:
                if n.manager is None:
                    if n.color is not None:
                        code.append(f"s['{n.name}'].color = {n.color}")

            # Solved state of managed DOFs nodes

            _modes = ("x", "y", "z", "rx", "ry", "rz")
            _dofs = []
            for n in self.nodes_of_type(Frame):
                if n.manager is not None:
                    d = [*n.position, *n.rotation]
                    for i, f in enumerate(n.fixed):
                        if f is False:  # free dof
                            _dofs.append((n.name, _modes[i], d[i]))
                            # code.append(f"s['{n.name}'].{_modes[i]} = {d[i]}")
            if _dofs:
                code.append("\n# Solved state of managed DOFs nodes")
                code.append(
                    "# wrapped in try/except because some nodes or dofs may not be present anymore (eg changed components)"
                )
                code.append("solved_dofs = [")
                for dof in _dofs:
                    code.append(f"    ('{dof[0]}', '{dof[1]}', {dof[2]}),")
                code.append("]")
                code.append("for dof in solved_dofs:")
                code.append("    try:")
                code.append("       setattr(s[dof[0]],dof[1],dof[2])")
                code.append("    except:")
                code.append("       pass")
                code.append("")

            # Optional Reports
            if self.reports and not no_reports:
                code.append("\n# Reports")
                for r in self.reports:
                    yml = r.to_yml()
                    code.append(f"\n# Exporting report {r.name}")
                    code.append(f'report_contents = r"""\n{yml}"""')
                    code.append("s.reports.append(Report(s,yml=report_contents))")

            # Optional Timelines
            if self.t and not no_timeline:
                code.extend(self.t.give_python_code())

        # Exposed properties of components
        exposed = getattr(self, "exposed", [])
        if exposed:
            code.append("exposed = list()")
            for e in exposed:
                code.append(f"exposed.append({str(e)})")
            code.append("s.exposed = exposed")

        return "\n".join(code)

    def save_scene(self, filename, no_reports=False, no_timeline=False):
        """Saves the scene to a file

        This saves the scene in its current state to a file.
        Opening the saved file will reproduce exactly this scene.

        This sounds nice, but beware that it only saves the resulting model, not the process of creating the model.
        This means that if you created the model in a parametric fashion or assembled the model from other models then these are not re-evaluated when the model is openened again.
        So lets say this model uses a sub-model of a lifting hook which is imported from another file. If that other file is updated then
        the results of that update will not be reflected in the saved model.

        If no path is present in the file-name then the model will be saved in the last (lowest) resource-path (if any)

        Args:
            filename : filename or file-path to save the file. Default extension is .dave

        Returns:
            the full path to the saved file

        """

        code = self.give_python_code(no_reports=no_reports, no_timeline=no_timeline)

        filename = Path(filename)

        # add .dave extension if needed
        if filename.suffix != ".dave":
            filename = Path(str(filename) + ".dave")

        # add path if not provided
        if not filename.is_absolute():
            try:
                filename = Path(self.resource_provider.resources_paths[-1]) / filename
            except:
                pass  # save in current folder

        # make sure directory exists
        directory = filename.parent
        if not directory.exists():
            directory.mkdir()

        f = open(filename, "w+")
        f.write(code)
        f.close()

        self._print("Saved as {}".format(filename))

        return filename

    def print_node_tree(self, more=False):
        self.sort_nodes_by_parent()
        to_be_printed = self._nodes.copy()

        if more:
            c = self.get_created_by_dict()
            cb = dict()
            for k, v in c.items():
                for node in v:
                    cb[node] = k

        def print_deps(node, spaces):
            deps = self.nodes_with_parent(node)

            extra = ""
            if more:
                created_by = None
                managed_by = None
                if node in cb:
                    created_by = cb[node].name
                    extra += f" Created by: {cb[node].name}"
                if node.manager is not None:
                    extra += f" Managed by: {node.manager.name} "
                    managed_by = node.manager.name

                if created_by is not None:
                    if created_by == managed_by:
                        extra = " Created and managed by: " + created_by

            print(
                spaces
                + node.name
                + " ["
                + str(type(node)).split(".")[-1][:-2]
                + "]"
                + extra
            )

            if deps is not None:
                for dep in deps:
                    if spaces == "":
                        spaces_plus = " |-> "
                    else:
                        spaces_plus = " |   " + spaces
                    print_deps(dep, spaces_plus)

            if node not in to_be_printed:
                print('** node "{}" occured before'.format(node.name))
            else:
                to_be_printed.remove(node)

        while to_be_printed:
            node = to_be_printed[0]
            # if node.name == "string_2/Shackle_1":
            #     print("stop")
            print_deps(node, "")

    def run_code(self, code, package_folder=None):
        """Runs the provided code with 's' as self"""

        import DAVE

        locals = DAVE.__dict__
        locals["s"] = self

        if package_folder is not None:
            locals["package_folder"] = package_folder

        locals.update(ds.DAVE_ADDITIONAL_RUNTIME_MODULES)

        try:
            exec(code, {}, locals)
        except Exception as M:
            message = get_code_error(code)

            try:
                M.add_note(message)  # new in python 3.11
            except:
                print(message)  # fallback for older python versions

            raise M

    def load_scene(self, filename=None):
        """Loads the contents of filename into the current scene.

        This function is typically used on an empty scene.

        Filename is appended with .dave if needed.
        File is searched for in the resource-paths.

        See also: import scene"""

        if filename is None:
            raise Exception("Please provide a file-name")

        try:
            filename = self.get_resource_path(filename)
        except:
            if not str(filename).endswith(".dave"):
                filename = Path(str(filename) + ".dave")

        print("Loading {}".format(filename))

        f = open(file=filename, mode="r")
        code = ""
        for line in f:
            code += line + "\n"

        try:
            self.run_code(code)
        except Exception as M:
            raise ModelInvalidException(M)

    def import_scene(
        self,
        other,
        prefix="",
        containerize=True,
        nodes=None,
        container=None,
        settings=True,
        quick=False,
    ):
        """Copy-paste all nodes of scene "other" into current scene.

        To avoid double names it is recommended to use a prefix. This prefix will be added to all element names.

        Args:
            containerize : place all the nodes without a parent in a dedicated Frame
            nodes [None] : if provided then import only these nodes
            settings     : import settings (gravity, wind etc. ) from other scene as well
            prefix       : a prefix is applied to all names of the imported nodes


        Returns:
            Contained (Axis-type Node) : if the imported scene is containerized then a reference to the created container is returned.
        """

        if container is not None:
            if not containerize:
                warnings.warn(
                    "containerize = False does not work in combination with supplying a container. Containerize set to true"
                )
                containerize = True

        if isinstance(other, Path):
            other = str(other)

        if isinstance(other, str):
            other = Scene(
                filename=other,
                resource_provider=self.resource_provider,
            )

        if not isinstance(other, Scene):
            raise TypeError("Other should be a Scene but is a " + str(type(other)))

        # apply prefix
        other.prefix_element_names(prefix)

        # check for double names after applying prefix
        for imported_node in other._nodes:
            if not self.name_available(imported_node.name):
                raise NameError(
                    'An element with name "{}" is already present. Please use a prefix to avoid double names'.format(
                        imported_node.name
                    )
                )

        store_export_code_with_solved_function = other._export_code_with_solved_function
        other._export_code_with_solved_function = False  # quicker
        code = other.give_python_code(
            nodes=nodes, export_environment_settings=settings, state_only=quick
        )
        other._export_code_with_solved_function = store_export_code_with_solved_function

        try:
            self.run_code(code)
        except Exception as M:
            raise ModelInvalidException(M)

        # Move all imported elements without a parent into a newly created or supplied frame (container)
        if containerize:
            if container is None:
                container_name = self.available_name_like("import_container")
                container = self.new_frame(prefix + container_name)

            imported_element_names = [node.name for node in other._nodes]
            for name in imported_element_names:
                imported_node = self[name]

                if not imported_node.manager:
                    if not hasattr(imported_node, "parent"):
                        continue

                    if imported_node.parent is None:
                        imported_node.parent = container

            return container

        return None

    def prefix_element_names(self, prefix=""):
        """Applies the given prefix to all un-managed nodes"""

        if prefix:
            for node in self._nodes:
                if node.manager is None:
                    node.name = prefix + node.name

    def copy(self, nodes=None, quick=False):
        """Creates a full and independent copy of the scene and returns it.

        Args:
            nodes [None]  : copy only these nodes
            quick [False] : copy only the scene itself - for solving DOFs in separate threads

        Example:
            s = Scene()
            c = s.copy()
            c.new_frame('only in c')

        """
        copy_resource_provider = deepcopy(self.resource_provider)

        c = Scene(
            resource_provider=copy_resource_provider,
        )

        c.import_scene(self, containerize=False, nodes=nodes, quick=quick)
        return c

    def get_free_frame_state_dict(self) -> dict:
        """Returns a dictionary with the positions and rotations of all Frames that have at least one dof free
        key: Node name
        value: 6d tuple with global position and rotation
        """
        result = dict()

        for frame in self.nodes_of_type(Frame):
            if not all(frame.fixed):  # at least one free
                result[frame.name] = (*frame.global_position, *frame.global_rotation)

        return result

    def maximum_relative_rotation(self, reference_state: dict) -> tuple:
        """Returns the maximum relative rotation between the current state and the reference state.
        reference_state is a state as obtained from get_free_frame_state_dict

        Returns the largest angle of rotation in degrees and the name of the node where that occurs

        """

        maxrot = 0
        name = "Rotations match"
        state2 = self.get_free_frame_state_dict()
        for key, value in reference_state.items():
            this_rotation = state2[key][3:]
            ref_rotation = value[3:]

            # compare
            rel_rot = angle_between_rotvects(this_rotation, ref_rotation)

            if rel_rot > maxrot:
                maxrot = rel_rot
                name = key

        return (maxrot, name)

    @property
    def state(self):
        """The state of the model is the values of all free dofs. This is what the solver solves.
        The state is returned as a list of tuples containing (node-name (str), mode (str), value)
        """
        state = []

        modes = ("x", "y", "z", "rx", "ry", "rz")

        for frame in self.nodes_of_type(Frame):
            for i, mode in enumerate(modes):
                if not frame.fixed[i]:  # if solved
                    value = getattr(frame, mode)
                    state.append((frame.name, mode, value))

        for beam in self.nodes_of_type(Beam):
            # if the Beam has only 1 segment then there are no shapeDofs
            state.append((beam.name, "_shapeDofs", beam._shapeDofs))

        return state

    @state.setter
    def state(self, value):
        for name, prop, val in value:
            setattr(self[name], prop, val)

    def duplicate_node(self, node):
        """Duplicates node, the copy will get the first available name.

        Returns: reference to the copy
        """
        if isinstance(node, str):
            node = self[node]

        name = node.name
        name_of_duplicate = self.available_name_like(name)

        # get the python code to generate the node with the new name
        remember = self._godmode
        self._godmode = True  # the node may be managed
        node.name = name_of_duplicate  # temporary rename just for code-generation

        try:
            self._export_code_with_solved_function = False
            code = node.give_python_code()
            self._export_code_with_solved_function = True
        finally:
            node.name = name  # and restore
            self._godmode = remember

        self.run_code(code)

        return self[name_of_duplicate]

    def duplicate_branch(self, root_node):
        """Duplicates a whole branch of the node-tree. Branch is defined by all the nodes that have the root_node as
        (grand) parent as well as all the nodes whose dependancies are within the branch (ie: cables between child-nodes)
        """

        if isinstance(root_node, str):
            root_node = self[root_node]

        nodes = self.nodes_with_parent(root_node, recursive=True)
        more_nodes = self.nodes_with_dependencies_in_and_satifsfied_by(nodes)
        branch = list({*nodes, *more_nodes})  # unique nodes (use set)

        to_be_copied = [
            node for node in branch if node.manager is None
        ]  # exclude managed nodes

        to_be_copied.append(root_node)

        # first copy each of these nodes
        copies = dict()
        new_names = dict()
        for node in to_be_copied:
            copies[node] = self.duplicate_node(node)
            new_names[node.name] = copies[node].name

        # now loop through the copies. If the parent or one of the connections is in the to-be-copied
        # nodes, then replace it with the copy.

        possible_attributes = (
            "parent",
            "child" "main",  # geometric contact  # LC6d
            "secondary",
            "nodeA",  # beam ; connector2d
            "nodeB",
            "endA",
            "endB",
        )

        for node in copies.values():
            for att in possible_attributes:
                if hasattr(node, att):
                    value = getattr(node, att)
                    if value in to_be_copied:
                        setattr(node, att, copies[value])

            # cables, slings, etc
            if hasattr(node, "connections"):
                for i, connection in enumerate(node.connections):
                    if connection in to_be_copied:
                        connections = list(node.connections)
                        connections[i] = copies[connection]
                        node.connections = connections

            # meshes
            if hasattr(node, "meshes_names"):
                meshes = list(node.meshes_names)
                for i, mesh in enumerate(meshes):
                    if mesh in new_names:
                        meshes[i] = new_names[mesh]
                node.meshes_names = meshes

    def to_frame(self, body: RigidBody):
        """Converts the body to a frame"""
        name = self.available_name_like("temp")
        new_frame = self.new_frame(
            name=name,
            parent=body.parent,
            position=body.position,
            rotation=body.rotation,
            inertia=body.inertia,
            inertia_radii=body.inertia_radii,
            fixed=body.fixed,
        )
        for node in self._nodes:
            parent = getattr(node, "parent", None)
            if parent == body:
                node.parent = new_frame

        name = body.name
        self.delete(body)
        new_frame.name = name

        return new_frame

    def to_rigidbody(self, frame: Frame):
        """Converts the body to a frame"""
        name = self.available_name_like("temp")
        new_body = self.new_rigidbody(
            name=name,
            parent=frame.parent,
            position=frame.position,
            rotation=frame.rotation,
            mass=frame.inertia,
            fixed=frame.fixed,
        )
        if new_body.mass > 0:
            new_body.inertia_radii = frame.inertia_radii

        for node in self._nodes:
            parent = getattr(node, "parent", None)
            if parent == frame:
                node.parent = new_body

        name = frame.name
        self.delete(frame)
        new_body.name = name

        return new_body

    def insert_frame_before(self, frame: Frame):
        """Inserts a new frame between this frame and its parent. Then re-parents
        the current frame to the newly created frame"""

        this_name = frame.name
        if frame.parent is None:
            name = "before_" + this_name
        else:
            name = "bewteen_" + frame.parent.name + "_and_" + this_name

        new_frame = self.new_frame(
            name=self.available_name_like(name),
            parent=frame.parent,
            position=frame.position,
            rotation=frame.rotation,
            fixed=True,
        )
        frame.parent = new_frame
        frame.rotation = (0, 0, 0)
        frame.position = (0, 0, 0)

        return new_frame

    # =================== DYNAMICS ==================

    def dynamics_M(self, delta=1e-6):
        """Returns the mass matrix of the scene"""
        self.update()

        return self._vfc.M(delta)

    def dynamics_K(self, delta=1e-6):
        """Returns the stiffness matrix of the scene for a perturbation of delta

        A component is positive if a displacement introduces an reaction force in the opposite direction.
        or:
        A component is positive if a positive force is needed to introduce a positive displacement.
        """
        self.update()

        return -self._vfc.K(delta)

    def dynamics_nodes(self):
        """Returns a list of nodes associated with the rows/columns of M and K"""
        self.update()
        nodes = self._vfc.get_dof_elements()

        node_names = [n.name for n in self._nodes]

        r = []
        for n in nodes:
            if n.name in node_names:
                r.append(self[n.name])
            else:
                r.append(None)

        return r

    def dynamics_modes(self):
        """Returns a list of modes (0=x ... 5=rotation z) associated with the rows/columns of M and K"""
        self.update()
        return self._vfc.get_dof_modes()
