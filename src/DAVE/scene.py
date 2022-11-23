"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""
# import fnmatch
# import glob
# import warnings
# from abc import ABC, abstractmethod
# from enum import Enum
# from typing import List  # for python<3.9
import weakref
from typing import Tuple

import pyo3d
# import numpy as np
import DAVE.settings as vfc
from DAVE.tools import *
# from os.path import isfile, split, dirname, exists
# from os import listdir
# from pathlib import Path
# import datetime

from .nodes import *
from .nodes import _Area

# we are wrapping all methods of pyo3d such that:
# - it is more user-friendly
# - code-completion is more robust
# - we can do some additional checks. pyo3d is written for speed, not robustness.
# - pyo3d is not a hard dependency
#
# notes and choices:
# - properties are returned as tuple to make sure they are not editable.
#    --> node.position[2] = 5 is not allowed


import functools

from .tools import assert1f


class Scene:
    """
    A Scene is the main component of DAVE.

    It provides a world to place nodes (elements) in.
    It interfaces with the equilibrium core for all calculations.

    By convention a Scene element is created with the name s, but create as many scenes as you want.

    Examples:

        s = Scene()
        s.new_frame('my_axis', position = (0,0,1))

        a = Scene() # another world
        a.new_point('a point')


    """

    def __init__(self, filename=None, copy_from=None, code=None, resource_paths=None):
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

        self._vfc = pyo3d.Scene()
        """_vfc : DAVE Core, where the actual magic happens"""

        self._nodes = []
        """Contains a list of all nodes in the scene"""

        self.static_tolerance = 0.01
        """Desired tolerance when solving statics"""

        self.resources_paths = []
        """A list of paths where to look for resources such as .obj files. Priority is given to paths earlier in the list."""
        self.resources_paths.extend(vfc.RESOURCE_PATH)

        if resource_paths is not None:
            for rp in resource_paths:
                if rp not in self.resources_paths:
                    self.resources_paths.append(rp)

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

        if filename is not None:
            self.load_scene(filename)

        if copy_from is not None:
            self.import_scene(copy_from, containerize=False, settings=True)

        if code is not None:
            self.run_code(code)

    def clear(self):
        """Deletes all nodes - leaves settings and reports in place"""

        # manually remove all references to the core
        # this avoids dangling pointers in copies of nodes
        for node in self._nodes:
            node.invalidate()
            node._delete_vfc()

        self._nodes = []
        del self._vfc

        # validate reports
        self._validate_reports()
        self.reports.clear()  # and then delete them

        self.t = None  # reset timelines (if any)

        self._vfc = pyo3d.Scene()

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

    def _check_and_fix_geometric_contact_orientations(self) -> Tuple[bool, str]:
        """A Geometric pin on pin contact may end up with tension in the contact. Fix that by moving the child pin to the other side of the parent pin

        Returns:
            True if anything was changed; False otherwise
        """

        remember = self._godmode
        self._godmode = True

        changed = False
        message = ""
        for n in self.nodes_of_type(GeometricContact):
            if not n.inside:

                # connection force of the child is the
                # force applied on the connecting rod
                # in the axis system of the rod
                if n._axis_on_child.connection_force_x > 0:
                    message += f"Changing side of pin-pin connection {n.name} due to tension in connection\n"
                    n.change_side()
                    changed = True

        self._godmode = remember

        return (changed, message)

    # ======== resources =========

    def get_resource_path(self, url) -> Path:
        """Resolves the path on disk for resource url. Urls statring with res: result in a file from the resources system.

        Looks for a file with "name" in the specified resource-paths and returns the full path to the the first one
        that is found.
        If name is a full path to an existing file, then that is returned.

        See Also:
            resource_paths


        Returns:
            Full path to resource

        Raises:
            FileExistsError if resource is not found

        """

        # warning and work-around for backwards compatibility
        # filenames without a path get res: in front of it
        try:
            if isinstance(url, Path):
                test = str(url)
            else:
                test = url

            if not test.startswith("res:"):
                test = Path(test)
                if str(test.parent) == ".":
                    # from warnings import warn
                    #
                    # warn(
                    #     f'Resources should start with res: --> fixing "{url}" to "res: {url}"'
                    # )
                    url = "res: " + str(test)
        except:
            pass

        if isinstance(url, Path):
            file = url
        elif isinstance(url, str):
            if not url.startswith("res:"):
                file = Path(url)
            else:
                # we have a string starting with 'res:'
                filename = url[4:].strip()

                for res in self.resources_paths:
                    p = Path(res)

                    file = p / filename
                    if isfile(file):
                        return file

                # prepare feedback for error
                ext = str(url).split(".")[-1]  # everything after the last .

                print("Resource folders:")
                for res in self.resources_paths:
                    print(str(res))

                print(
                    "The following resources with extension {} are available with ".format(
                        ext
                    )
                )
                available = self.get_resource_list(ext)
                for a in available:
                    print(a)
                raise FileExistsError(
                    'Resource "{}" not found in resource paths. A list with available resources with this extension is printed above this error'.format(
                        url
                    )
                )
        else:
            raise ValueError(
                f"Provided url shall be a Path or a string, not a {type(url)}"
            )

        if file.exists():
            return file

        raise FileExistsError(
            'File "{}" not found.\nHint: To obtain a resource put res: in front of the name.'.format(
                url
            )
        )

    def get_resource_list(self, extension, include_subdirs=False):
        """Returns a list of all resources (strings) with given extension in any of the resource-paths"""

        # include subdirs excludes the root dir. Scan the root-dir first by doing a non-recursive call
        if include_subdirs:
            r = self.get_resource_list(extension=extension, include_subdirs=False)
        else:
            r = []

        for dir in self.resources_paths:
            try:
                # files = listdir(dir)
                # for file in files:
                #     if file.lower().endswith(extension):
                #         if file not in r:
                #             r.append("res: " + file)
                if include_subdirs:
                    mask = str(dir) + "/**/*" + extension
                    recursive = True
                else:
                    mask = str(dir) + "/*" + extension
                    recursive = False

                for file in glob.glob(mask, recursive=recursive):

                    file = file.replace(str(dir), "")
                    if file.startswith("\\"):
                        file = file[1:]
                    file = file.replace("\\", "/")

                    if file not in r:
                        r.append("res: " + file)

            except FileNotFoundError:
                pass

        r = list(set(r)) # remove doubles

        return r

    # ======== element functions =========

    @property
    def unmanged_nodes(self):
        """Returns a tuple containing references to all nodes that do not have a manager"""
        nodes = [node for node in self._nodes if node.manager is None]
        return tuple(nodes)

    @property
    def manged_nodes(self):
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

        docs = None

        for anchestor in reversed(anchestors):
            if anchestor in DAVE_NODEPROP_INFO:
                info = DAVE_NODEPROP_INFO[anchestor]
                if property_name in info:
                    docs = info[property_name]

        return docs

    def node_by_name(self, node_name, silent=False):

        assert isinstance(
            node_name, str
        ), f"Node name should be a string, but is a {type(node_name)}"


        for N in self._nodes:
            if N.name == node_name:
                return N

        if not silent:
            self.print_node_tree()

        # See if we can give a good hint using fuzzy

        choices = [node.name for node in self._nodes]
        suggestion = MostLikelyMatch(node_name, choices)

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

        exported = []
        to_be_exported = self._nodes.copy()
        counter = 0

        while to_be_exported:

            counter += 1
            if counter > len(self._nodes):
                raise Exception(
                    "Could not sort nodes by dependency, circular references exist?"
                )

            can_be_exported = []

            for node in to_be_exported:

                if hasattr(node, "parent"):
                    parent = node.parent
                    if parent is not None and parent not in exported:
                        continue

                if node.manager is not None and node.manager not in exported:
                    continue

                # otherwise the node can be exported
                can_be_exported.append(node)

            # remove exported nodes from
            for n in can_be_exported:
                to_be_exported.remove(n)

            exported.extend(can_be_exported)

        self._nodes = exported

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

        while to_be_exported:

            counter += 1
            if counter > len(self._nodes):

                print("Error when exporting, could not resolve dependancies:")

                for node in to_be_exported:
                    print(f"Node : {node.name}")
                    for d in node.depends_on():
                        print(f"  depends on: {d.name}")
                    if node._manager:
                        print(f"   managed by: {node._manager.name}")

                raise Exception(
                    "Could not sort nodes by dependency, circular references exist?"
                )

            can_be_exported = []

            for node in to_be_exported:
                # if node._manager:
                #     if node._manager in exported:
                #         can_be_exported.append(node)
                # el
                if all(el in exported for el in node.depends_on()):
                    can_be_exported.append(node)

            # remove exported nodes from
            for n in can_be_exported:
                to_be_exported.remove(n)

            exported.extend(can_be_exported)

        self._nodes = exported

    def assert_name_available(self, name):
        """Raises an error is name is not available"""
        assert self.name_available(name), f"Name {name} is already in use"

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

    def available_name_like(self, like, _additional_names=()):
        """Returns an available name like the one given, for example Axis23

        Args
            _additional_names [()] : if provided then the name shall not be one of these either
        """

        if self.name_available(like):
            if like not in _additional_names:
                return like
        counter = 1
        while True:
            name = like + "_" + str(counter)
            if self.name_available(name):
                if name not in _additional_names:
                    return name
            counter += 1

    def node_A_core_depends_on_B_core(self, A, B):
        """Returns True if the node core of node A depends on the core node of node B"""

        A = self._node_from_node_or_str(A)
        B = self._node_from_node_or_str(B)

        if not isinstance(A, CoreConnectedNode):
            raise ValueError(
                f"{A.name} is not connected to a core node. Dependancies can not be traced using this function"
            )
        if not isinstance(B, CoreConnectedNode):
            raise ValueError(
                f"{B.name} is not connected to a core node. Dependancies can not be traced using this function"
            )

        return self._vfc.element_A_depends_on_B(A._vfNode.name, B._vfNode.name)

    def nodes_managed_by(self, manager: Manager):
        """Returns a list of nodes managed by manager"""

        return [node for node in self._nodes if node.manager == manager]

    def nodes_depending_on(self, node):
        """Returns a list of nodes that physically depend on node. Only direct dependants are obtained with a connection to the core.
        This function should be used to determine if a node can be created, deleted, exported.

        For making node-trees please use nodes_with_parent instead.

        Args:
            node : Node or node-name

        Returns:
            list of names

        See Also: nodes_with_parent
        """

        if isinstance(node, Node):
            node = node.name

        # check the node type
        _node = self[node]
        if not isinstance(_node, CoreConnectedNode):
            return []
        else:
            names = self._vfc.elements_depending_directly_on(node)

        r = []
        for name in names:
            try:
                node = self.node_by_name(name, silent=True)
                r.append(node.name)
            except:
                pass

        # check all other nodes in the scene

        for n in self._nodes:
            if _node in n.depends_on():
                if n.name not in r:
                    r.append(n.name)

        # for v in [*self.nodes_of_type(Visual), *self.nodes_of_type(WaveInteraction1)]:
        #     if v.parent is _node:
        #         r.append(v.name)

        return r

    def common_ancestor_of_nodes(self, nodes: List[Node]) -> Node or None:
        """Finds a nearest ancestor (parent) that is common to all of the nodes.

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

    def nodes_with_dependancies_in_and_satifsfied_by(self, nodes):
        """Returns a list of all nodes that have dependancies and whose dependancies that are all within 'nodes'

        Often used in combination with nodes_with_parent, for example to find cables that fall within a branch of the
        node-tree.
        """

        r = []

        for node in self._nodes:
            deps = node.depends_on()
            if not deps:
                continue  # skip nodes without dependancies

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
        node._delete_vfc()
        self._nodes.remove(node)

        # validate reports
        self._validate_reports()

        # validate timelines
        self._validate_timelines()

    def dissolve(self, node):
        """Attempts to delete the given node without affecting the rest of the model.

        1. Look for nodes that have this node as parent
        2. Attach those nodes to the parent of this node.
        3. Delete this node.

        There are many situations in which this will fail because an it is impossible to dissolve
        the element. For example a poi can only be dissolved when nothing is attached to it.

        For now this function only works on Frames and Managers
        """

        if isinstance(node, str):
            node = self[node]

        if node.manager is not None:
            raise Exception("Managed nodes can not be dissolved")

        if isinstance(node, Manager):

            if isinstance(node, RigidBody):

                p = self.new_rigidbody(
                    node.name + "_dissolved",
                    mass=node.mass,
                    position=node.position,
                    rotation=node.rotation,
                    inertia_radii=node.inertia_radii,
                    fixed=node.fixed,
                    cog=node.cog,
                    parent=node.parent,
                )
            elif isinstance(node, Frame):
                p = self.new_frame(
                    node.name + "_dissolved",
                    position=node.position,
                    rotation=node.rotation,
                    inertia=node.inertia,
                    inertia_radii=node.inertia_radii,
                    fixed=node.fixed,
                    parent=node.parent,
                )
            else:
                p = None

            with ClaimManagement(self, node):
                for d in self.nodes_managed_by(node):
                    if node in d.observers:
                        d.observers.remove(node)
                    d.manager = None

                    if hasattr(d, "parent"):
                        if d.parent == node:
                            d.parent = p

                for d in self.nodes_depending_on(node):
                    self[d].change_parent_to(p)

            node._dissolved = True  # signal for the .delete function to skip deletion of nodes created by the manager

        elif isinstance(node, Frame):
            for d in self.nodes_depending_on(node):
                self[d].change_parent_to(node.parent)

        else:
            raise TypeError(
                "Only nodes of type Frame and Manager can be dissolved at this moment"
            )

        self.delete(node)  # do not call delete as that will fail on managers

    def savepoint_make(self):
        self._savepoint = self.give_python_code()

    def savepoint_restore(self):
        if self._savepoint is not None:
            self.clear()
            self.run_code(self._savepoint)
            self._savepoint = None
            return True
        else:
            return False

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

    def update(self):
        """Updates the interface between the nodes and the core. This includes the re-calculation of all forces,
        buoyancy positions, ballast-system cogs etc.
        """
        for n in self._nodes:
            n.update()
        self._vfc.state_update()

    def _solve_debug_tiny_step(self, s=0.001):

        self._solve_statics_with_optional_control(
            do_terminate_func=lambda: True, timeout_s=s
        )

    def _solve_statics_with_optional_control(
        self, feedback_func=None, do_terminate_func=None, timeout_s=1
    ):
        """Solves statics with a time-out and feedback/terminate functions.

        Specifying a time-out means that feedback / termination is evaluated every timeout_s seconds. This does not mean
        that the function terminates after timeout_s. In fact the function will keep trying indefinitely (no maximum
        number of iterations)

        1. Reduce degrees of freedom: Freezes all vessels at their current heel and trim
        2. Solve statics

        3. Restore original degrees of freedom
        4. Solve statics

        5. Check geometric contacts
            if ok: Done
            if not ok: Correct and go back to 4

        Options for feedback to user and termination control during solving:

        feedback_func     : func(str)
        do_terminate_func : func() -> bool
        """

        # # fallback to normal solve if feedback and control arguments are not provided
        # if feedback_func is None or do_terminate_func is None:
        #     return self.solve_statics()

        # Two quick helper functions for running in controlled mode
        def give_feedback(txt):
            if feedback_func is not None:
                feedback_func(txt)

        def should_terminate():
            if do_terminate_func is not None:
                return do_terminate_func()
            else:
                return False

        self.update()

        if timeout_s is None:
            timeout_s = -1

        # solve_func = lambda: self._vfc.state_solve_statics_with_timeout(
        #     True, timeout_s, True, True, 0
        # )  # 0 = default stability value

        phase = 1
        original_dofs_dict = None

        first = True

        while True:

            if not first and should_terminate():
                if original_dofs_dict is not None:
                    self._restore_original_fixes(original_dofs_dict)
                    self.update()
                return False

            if phase == 1:  # prepare to go to phase 1 (or directly to phase 2)

                old_dofs = self._vfc.get_dofs()
                if len(old_dofs) == 0:
                    return True  # <---- trivial case

                original_dofs_dict = self._fix_vessel_heel_trim()
                phase = 2

            elif phase == 2:

                this_is_a_re_init = not first

                try:
                    debug = self._vfc.to_string()

                    #
                    status = self._vfc.state_solve_statics_with_timeout(
                        True, timeout_s, True, True, 0, this_is_a_re_init
                    )
                except:
                    print(debug)
                    raise ValueError('oops')

                first = False

                if status == 0 or status == -2:

                    # phase 3
                    self._restore_original_fixes(original_dofs_dict)
                    phase = 4

                else:
                    if (
                        timeout_s < 0
                    ):  # we were not using a timeout, so the solver failed
                        self._restore_original_fixes(original_dofs_dict)
                        raise ValueError(
                            f"Could not solve - solver return code {status} during phase 2. Maximum error = {self._vfc.Emaxabs:.6e}"
                        )

                give_feedback(f"Maximum error = {self._vfc.Emaxabs:.6e} (phase 2)")

            elif phase == 4:

                status = self._vfc.state_solve_statics_with_timeout(
                    True, timeout_s, True, True, 0, this_is_a_re_init
                )

                if status == 0 or status == -2:
                    # phase 5
                    (
                        changed,
                        msg,
                    ) = self._check_and_fix_geometric_contact_orientations()

                    if not changed:
                        # we are done!

                        if self.t is not None:
                            self.t.store_solved_results()

                        return True  # <------------- You've found the proper exit!

                    give_feedback(msg)

                else:
                    give_feedback(f"Maximum error = {self._vfc.Emaxabs:.6e} (phase 4)")

    def solve_statics(self, silent=False, timeout=None):
        """Solves statics

        If a timeout is provided then each pass will take at most 'timeout' seconds. This means you may need to call
        this function repeatedly to reach an equilibrium.

        This function takes the following steps:

        Phase 1:
        1. Reduce degrees of freedom: Freezes all vessels at their current heel and trim
        2. Solve statics

        Phase 2:
        3. Restore original degrees of freedom
        4. Solve statics

        Phase 3:
        5. Check geometric contacts
            if ok: Done
            if not ok: Correct and go back to step 4


        Args:
            silent: Do not print if successfully solved

        Returns:
            bool: True if successful, False otherwise.

        """
        if timeout is None:
            timeout = -1

        if self.gui_solve_func is not None:
            return self.gui_solve_func(self, called_by_user=False)
        else:
            return self._solve_statics_with_optional_control(timeout_s=timeout)

    def verify_equilibrium(self, tol=1e-2):
        """Checks if the current state is an equilibrium

        Returns:
            bool: True if successful, False if not an equilibrium.

        """
        self.update()
        return self._vfc.Emaxabs < tol

    # ====== goal seek ========

    def goal_seek(
        self, evaluate, target, change_node, change_property, bracket=None, tol=1e-3
    ):
        """goal_seek

        Goal seek is the classic goal-seek. It changes a single property of a single node in order to get
        some property of some node to a specified value. Just like excel.

        Args:
            evaluate : code to be evaluated to yield the value that is solved for. Eg: s['poi'].fx Scene is abbiviated as "s"
            target (number):       target value for that property
            change_node(Node or str):  node to be adjusted
            change_property (str): property of that node to be adjusted
            range(optional)  : specify the possible search-interval

        Returns:
            bool: True if successful, False otherwise.

        Examples:
            Change the y-position of the cog of a rigid body ('Barge')  in order to obtain zero roll (rx)
            >>> s.goal_seek("s['Barge'].fx",0,'Barge','cogy')

        """
        s = self

        change_node = self._node_from_node_or_str(change_node)

        # check that the attributes exist and are single numbers
        test = eval(evaluate)

        try:
            float(test)
        except:
            raise ValueError("Evaluation of {} does not result in a float")

        self._print(
            "Attempting to evaluate {} to {} (now {})".format(evaluate, target, test)
        )

        initial = getattr(change_node, change_property)
        self._print(
            "By changing the value of {}.{} (now {})".format(
                change_node.name, change_property, initial
            )
        )

        def set_and_get(x):
            setattr(change_node, change_property, x)
            self.solve_statics(silent=True)
            s = self
            result = eval(evaluate)
            self._print("setting {} results in {}".format(x, result))
            return result - target

        from scipy.optimize import root_scalar

        x0 = initial
        x1 = initial + 0.0001

        if bracket is not None:
            res = root_scalar(set_and_get, x0=x0, x1=x1, bracket=bracket, xtol=tol)
        else:
            res = root_scalar(set_and_get, x0=x0, x1=x1, xtol=tol)

        self._print(res)

        # evaluate result
        final_value = eval(evaluate)
        if abs(final_value - target) > 1e-3:
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
            self.solve_statics(silent=True)
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

    def new_axis(
        self,
        name,
        parent=None,
        position=None,
        rotation=None,
        inertia=None,
        inertia_radii=None,
        fixed=True,
    ) -> Frame:

        warnings.warn("new_axis is deprecated, use new_frame instead")

        return self.new_frame(
            name, parent, position, rotation, inertia, inertia_radii, fixed
        )

    def new_frame(
        self,
        name,
        parent=None,
        position=None,
        rotation=None,
        inertia=None,
        inertia_radii=None,
        fixed=True,
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
            t = Scene(filename)
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

        name_prefix = name + vfc.MANAGED_NODE_IDENTIFIER
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

        # self._nodes.append(new_node)
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

        # self._nodes.append(new_node)
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
        name,
        mass=0,
        cog=(0, 0, 0),
        parent=None,
        position=None,
        rotation=None,
        inertia_radii=None,
        fixed=True,
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
                warnings.warn(f"Can not set radii of gyration without specifying mass - ignoring radii of gyration for {name}")
                inertia_radii = None

        if not isinstance(fixed, bool):
            if len(fixed) != 6:
                raise Exception(
                    '"fixed" parameter should either be True/False or a 6x bool sequence such as (True,True,False,False,True,False)'
                )

        # make elements

        # a = self._vfc.new_axis(name)

        # p = self._vfc.new_poi(name + vfc.VF_NAME_SPLIT + "cog")
        # p.parent = a
        # p.position = cog
        #
        # g = self._vfc.new_force(name + vfc.VF_NAME_SPLIT + "gravity")
        # g.parent = p
        # g.force = (0, 0, -self.g * mass)

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
        endA,
        endB,
        length=None,
        EA=0,
        diameter:float=0,
        sheaves=None,
        mass=None,
        mass_per_length=None,
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
            if length < 1e-9:
                raise Exception("Length should be more than 0")

        if EA < 0:
            raise Exception("EA should be more than 0")

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

        # then create

        new_node = Cable(self, name)
        if length is not None:
            new_node.length = length
        new_node.EA = EA

        new_node.diameter = diameter

        new_node.connections = pois

        # and add to the scene
        # self._nodes.append(new_node)

        if length is None:
            new_node.length = 1e-8
            self._vfc.state_update()

            new_length = new_node.stretch + 1e-8

            if new_length > 0:
                new_node.length = new_length
            else:
                # is is possible that all nodes are at the same location which means the total length becomes 0
                self.delete(new_node.name)
                raise ValueError(
                    "No lengh has been supplied and all connection points are at the same location - unable to determine a non-zero default length. Please supply a length"
                )

        if mass is not None:
            mass_per_length = mass / new_node.length

        new_node.mass_per_length = mass_per_length

        return new_node

    def new_force(self, name, parent=None, force=None, moment=None) -> Force:
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

        if force is not None:
            assert3f(force, "Force ")

        if moment is not None:
            assert3f(moment, "Moment ")

        # then create
        new_node = Force(self, name)

        # and set properties
        if b is not None:
            new_node.parent = b
        if force is not None:
            new_node.force = force
        if moment is not None:
            new_node.moment = moment

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

        a = self._vfc.new_wind(name)

        if is_wind:
            a.isWind = True
            new_node = WindArea(self, a)
        else:
            a.isWind = False
            new_node = CurrentArea(self, a)

        # and set properties
        if b is not None:
            new_node.parent = b
        new_node.areakind = areakind
        new_node.direction = direction
        new_node.Cd = Cd
        new_node.A = A

        # self._nodes.append(new_node)
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

    def new_circle(self, name, parent, axis, radius=0.0) -> Circle:
        """Creates a new *sheave* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Poi]
            axis: direction of the axis of rotation (x,y,z)
            radius: optional, radius of the sheave


        Returns:
            Reference to newly created sheave

        """



        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._poi_from_node(parent)

        assert3f(axis, "Axis of rotation ")

        assert1f(radius, "Radius of sheave")

        new_node = Circle(self, name)

        # and set properties
        new_node.parent = b
        new_node.axis = axis
        new_node.radius = radius

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
        a = self._vfc.new_hydspring(name)
        new_node = HydSpring(self, a)

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

        # self._nodes.append(new_node)
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

        # self._nodes.append(new_node)
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

        # self._nodes.append(new_node)
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
        r = BallastSystem(self, name, parent)

        # self._nodes.append(r)
        return r

    def new_sling(
        self,
        name,
        length:float=-1,
        EA=None,
        mass=0.1,
        endA=None,
        endB=None,
        LeyeA=None,
        LeyeB=None,
        LspliceA=None,
        LspliceB=None,
        diameter=0.1,
        sheaves=None,
        k_total=None,
    ) -> Sling:
        """
        Creates a new sling, adds it to the scene and returns a reference to the newly created object.

        See Also:
            Sling

        Args:
            name:    name
            length:  length of the sling [m], defaults to distance between endpoints
            EA:      stiffness in kN, default: 1.0 (note: equilibrium will fail if mass >0 and EA=0)
            k_total: stiffness in kN/m, default: None
            mass:    mass in mT, default  0.1
            endA:    element to connect end A to [poi, circle]
            endB:    element to connect end B to [poi, circle]
            LeyeA:   inside eye on side A length [m], defaults to 1/6th of length
            LeyeB:   inside eye on side B length [m], defaults to 1/6th of length
            LspliceA: splice length on side A [m] (the part where the cable is connected to itself)
            LspliceB: splice length on side B [m] (the part where the cable is connected to itself)
            diameter: cable diameter in m, defaul to 0.1
            sheaves:  optional: list of sheaves/pois that the sling runs over

        Returns:
            a reference to the newly created Sling object.

        """



        # first check
        assertValidName(name)
        self._verify_name_available(name)

        name_prefix = name + vfc.MANAGED_NODE_IDENTIFIER
        postfixes = [
            "_spliceA",
            "_spliceA",
            "_spliceA2",
            "_spliceAM",
            "_spliceA_visual",
            "spliceB",
            "_spliceB1",
            "_spliceB2",
            "_spliceBM",
            "_spliceB_visual",
            "_main_part",
            "_eyeA",
            "_eyeB",
        ]

        for pf in postfixes:
            self._verify_name_available(name_prefix + pf)

        endA = self._poi_or_sheave_from_node(endA)
        endB = self._poi_or_sheave_from_node(endB)

        if length == -1:  # default
            if endA is None or endB is None:
                raise ValueError(
                    "Length for cable is not provided, so defaults to distance between endpoints; but at least one of the endpoints is None."
                )

            length = np.linalg.norm(
                np.array(endA.global_position) - np.array(endB.global_position)
            )

        if LeyeA is None:  # default
            LeyeA = length / 6
        if LeyeB is None:  # default
            LeyeB = length / 6
        if LspliceA is None:  # default
            LspliceA = length / 6
        if LspliceB is None:  # default
            LspliceB = length / 6

        if sheaves is None:
            sheaves = []

        if EA is not None and k_total is not None:
            warnings.warn(
                "Value for EA is given by will not be used as k_total is defined as well. Value for EA will be derived from k_total"
            )

        if EA is None:
            EA = 1  # possibly overwritten by k_total

        assert1f_positive_or_zero(diameter, "Diameter")
        assert1f_positive_or_zero(mass, "mass")

        assert1f_positive(length, "Length")
        assert1f_positive(LeyeA, "length of eye A")
        assert1f_positive(LeyeB, "length of eye B")
        assert1f_positive(LspliceA, "length of splice A")
        assert1f_positive(LspliceB, "length of splice B")

        if k_total is not None:
            assert1f_positive_or_zero(k_total, "Total stiffness (k_total)")

        for s in sheaves:
            _ = self._poi_or_sheave_from_node(s)

        # then make element
        # __init__(self, scene, name, Ltotal, LeyeA, LeyeB, LspliceA, LspliceB, diameter, EA, mass, endA = None, endB=None, sheaves=None):

        node = Sling(
            scene=self,
            name=name,
            length=length,
            LeyeA=LeyeA,
            LeyeB=LeyeB,
            LspliceA=LspliceA,
            LspliceB=LspliceB,
            diameter=diameter,
            EA=EA,
            mass=mass,
            endA=endA,
            endB=endB,
            sheaves=sheaves,
        )

        if k_total is not None:
            node.k_total = k_total

        # self._nodes.append(node)

        return node

    def new_shackle(self, name, kind="GP500") -> Shackle:
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

        name_prefix = name + vfc.MANAGED_NODE_IDENTIFIER
        postfixes = [
            "_body",
            "_pin_point",
            "_bow_point",
            "_inside_circle_center",
            "_inside",
            "_visual",
        ]
        for pf in postfixes:
            self._verify_name_available(name_prefix + pf)

        # then make element

        # make elements
        #
        # a = self._vfc.new_axis(name)
        #
        # p = self._vfc.new_poi(name + vfc.VF_NAME_SPLIT + "cog")
        # p.parent = a
        #
        # g = self._vfc.new_force(name + vfc.VF_NAME_SPLIT + "gravity")
        # g.parent = p

        node = Shackle(scene=self, name=name, kind=kind)

        # self._nodes.append(node)

        return node

    def print_python_code(self):
        """Prints the python code that generates the current scene

        See also: give_python_code
        """
        for line in self.give_python_code().split("\n"):
            print(line)

    def give_python_code(
        self, nodes=None, export_environment_settings=True, _no_sort_nodes=False
    ):
        """Generates the python code that rebuilds the scene and elements in its current state.

        Args:
            nodes [None] : generate only for these node(s)
            export_environment_settings [True] : export the environment (wind, gravity, etc)
            _no_sort_nodes [False] : skip sorting of nodes (use if sure that nodes are already sorted)
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

        # store the visibility code separately

        for n in nodes_to_be_exported:
            if not n.visible:
                code.append(
                    f"\ns['{n.name}']._visible = False"  # use private, cause may be managed (in which case this statement is probably obsolete)
                )  # only report is not the default value

        code.append("\n# Limits of un-managed nodes ")

        for n in nodes_to_be_exported:
            if n.manager is None:
                for key, value in n.limits.items():
                    code.append(f"s['{n.name}'].limits['{key}'] = {value}")

        code.append("\n# Tags")

        for n in nodes_to_be_exported:
            if n.manager is None:
                if n.tags:
                    code.append(f"s['{n.name}'].add_tags({n.tags})")

        code.append("\n# Colors")

        for n in nodes_to_be_exported:
            if n.manager is None:
                if n.color is not None:
                    code.append(f"s['{n.name}'].color = {n.color}")

        # Optional Reports
        if self.reports:
            code.append("\n# Reports")
            for r in self.reports:
                yml = r.to_yml()
                code.append(f"\n# Exporting report {r.name}")
                code.append(f'report_contents = r"""\n{yml}"""')
                code.append("s.reports.append(Report(s,yml=report_contents))")

        # Optional Timelines
        if self.t:
            code.extend(self.t.give_python_code())

        return "\n".join(code)

    def save_scene(self, filename):
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

        code = self.give_python_code()

        filename = Path(filename)

        # add .dave extension if needed
        if filename.suffix != ".dave":
            filename = Path(str(filename) + ".dave")

        # add path if not provided
        if not filename.is_absolute():
            try:
                filename = Path(self.resources_paths[-1]) / filename
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

    def print_node_tree(self):

        self.sort_nodes_by_dependency()
        to_be_printed = self._nodes.copy()

        def print_deps(node, spaces):

            deps = self.nodes_with_parent(node)

            print(spaces + node.name + " [" + str(type(node)).split(".")[-1][:-2] + "]")

            if deps is not None:
                for dep in deps:
                    if spaces == "":
                        spaces_plus = " |-> "
                    else:
                        spaces_plus = " |   " + spaces
                    print_deps(dep, spaces_plus)

            to_be_printed.remove(node)

        while to_be_printed:
            node = to_be_printed[0]
            print_deps(node, "")

    def run_code(self, code):
        """Runs the provided code with 's' as self"""

        import DAVE

        locals = DAVE.__dict__
        locals["s"] = self

        locals.update(ds.DAVE_ADDITIONAL_RUNTIME_MODULES)

        try:
            exec(code, {}, locals)
        except Exception as M:
            for i, line in enumerate(code.split("\n")):
                print(f"{i} {line}")
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

        self.run_code(code)

    def import_scene(
        self,
        other,
        prefix="",
        containerize=True,
        nodes=None,
        container=None,
        settings=True,
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
            other = Scene(other, resource_paths=self.resources_paths)

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
        code = other.give_python_code(nodes=nodes, export_environment_settings=settings)
        other._export_code_with_solved_function = store_export_code_with_solved_function

        self.run_code(code)

        

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

    def prefix_element_names(self, prefix=''):
        """Applies the given prefix to all un-managed nodes"""

        if prefix:
            for node in self._nodes:
                if node.manager is None:
                    node.name = prefix + node.name

    def copy(self, nodes=None):
        """Creates a full and independent copy of the scene and returns it.

        Args:
            nodes [None] : copy only these nodes

        Example:
            s = Scene()
            c = s.copy()
            c.new_frame('only in c')

        """

        c = Scene()
        c.resources_paths.clear()
        c.resources_paths.extend(self.resources_paths)
        c.import_scene(self, containerize=False, nodes=nodes)
        return c

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
        self._godmode = True # the node may be managed
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
        (grand) parent as well as all the nodes whose dependancies are within the branch (ie: cables between child-nodes)"""

        if isinstance(root_node, str):
            root_node = self[root_node]

        # set the parent of the root_node to None (if any)
        old_parent = getattr(root_node, "parent", None)
        if old_parent is not None:
            root_node.parent = None

        nodes = self.nodes_with_parent(root_node, recursive=True)
        more_nodes = self.nodes_with_dependancies_in_and_satifsfied_by(nodes)
        branch = list({*nodes, *more_nodes})  # unique nodes (use set)

        branch = [node for node in branch if node.manager is None] # exclude managed nodes

        branch.append(root_node)

        # make a copy of these nodes in a new scene
        s2 = self.copy(branch)

        copy_of_root_node_in_s2 = s2[root_node.name]

        # now find new names for all of the nodes.
        # names need to be unique in both self and s2
        for n in s2._nodes:
            if n.manager is None:
                node_names_in_s2 = [node.name for node in s2._nodes]
                new_name = self.available_name_like(
                    n.name, _additional_names=node_names_in_s2
                )
                n.name = new_name

        self.import_scene(s2, containerize=False)

        # restore the parent (if any)
        if old_parent is not None:
            copy_of_root_node = self[copy_of_root_node_in_s2.name]
            copy_of_root_node.parent = old_parent
            root_node.parent = old_parent

    # =================== Conversions ===============

    def to_cable(self, sling_node : Sling, zero_weight=False):
        """Converts a sling to an equivalent cable"""
        name = self.available_name_like(sling_node.name)

        # calculate the new length
        length_lossA = 0
        if isinstance(sling_node.endA, Circle):
            r = sling_node.endA.radius + sling_node.diameter/2
            length_lossA = np.pi * r

        length_lossB = 0
        if isinstance(sling_node.endB, Circle):
            r = sling_node.endB.radius + sling_node.diameter / 2
            length_lossB = np.pi * r

        # If both ends are the same circle then the cable would become a grommet.
        # to avoid that, connect endA to the Point instead
        original_endA_parent = None
        if isinstance(sling_node.endB, Circle) and (sling_node.endA == sling_node.endB):
            original_endA_parent = sling_node.endA
            sling_node.endA = sling_node.endA.parent




        length = sling_node.length - length_lossA - length_lossB

        # calcualte EA from total stiffness of the sling and the new length
        # such that the total stiffness is identical
        EA = sling_node.k_total * length

        if zero_weight:
            mass_per_length = 0
        else:
            mass_per_length = sling_node.mass/length

        cable = self.new_cable(name, endA = sling_node.endA, endB=sling_node.endB, sheaves=sling_node.sheaves,
                       length=length, mass_per_length=mass_per_length, EA=EA,diameter=sling_node.diameter)

        name = sling_node.name
        self.delete(sling_node)

        if original_endA_parent is not None:
            cable.original_endA_parent = weakref.ref(original_endA_parent)

        cable.name = name

        return cable

    def to_sling(self, cable_node : Cable, mass=-1):
        """Converts a sling to an equivalent cable

        if mass < 0 (default) then the mass of the cable is used. Else the given mass is used.
        """
        name = self.available_name_like(cable_node.name)

        endA = cable_node.connections[0]

        original_endA_parent = getattr(cable_node, 'original_endA_parent', None)
        if original_endA_parent is not None:
            if valid_node_weakref(original_endA_parent):
                endA = original_endA_parent()

        endB = cable_node.connections[-1]

        # calculate the new length
        length_lossA = 0
        if isinstance(endA, Circle):
            r = endA.radius + cable_node.diameter / 2
            length_lossA = np.pi * r

        length_lossB = 0
        if isinstance(endB, Circle):
            r = endB.radius + cable_node.diameter / 2
            length_lossB = np.pi * r

        length = cable_node.length + length_lossA + length_lossB

        # calculate EA from total stiffness of the sling and the new length
        # such that the total stiffness is identical
        EAL = cable_node.EA / cable_node.length

        if mass<0:
            mass = cable_node.mass

        sling = self.new_sling(name, endA = endA, endB=endB, sheaves=cable_node.connections[1:-1],
                               length=length, mass=mass, k_total = EAL, diameter=cable_node.diameter)

        name = cable_node.name
        self.delete(cable_node)

        sling.name = name

        return sling

    def to_frame(self, body: RigidBody):
        """Converts the body to a frame"""
        name = self.available_name_like('temp')
        new_frame = self.new_frame(name=name,
                                   parent=body.parent,
                                   position = body.position,
                                   rotation = body.rotation,
                                   inertia = body.inertia,
                                   inertia_radii = body.inertia_radii,
                                   fixed= body.fixed)
        for node in self._nodes:
            parent = getattr(node,'parent',None)
            if parent == body:
                node.parent = new_frame

        name = body.name
        self.delete(body)
        new_frame.name = name

        return new_frame

    def to_rigidbody(self, frame: Frame):
        """Converts the body to a frame"""
        name = self.available_name_like('temp')
        new_body = self.new_rigidbody(name=name,
                                       parent=frame.parent,
                                       position=frame.position,
                                       rotation=frame.rotation,
                                       mass=frame.inertia,
                                       fixed=frame.fixed)
        if new_body.mass > 0:
            new_body.inertia_radii = frame.inertia_radii

        for node in self._nodes:
            parent = getattr(node, 'parent', None)
            if parent == frame:
                node.parent = new_body

        name = frame.name
        self.delete(frame)
        new_body.name = name

        return new_body

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


# =================== None-Node Classes

"""This is a container for a pyo3d.MomentDiagram object providing plot methods"""


class LoadShearMomentDiagram:
    def __init__(self, datasource):
        """

        Args:
            datasource: pyo3d.MomentDiagram object
        """

        self.datasource = datasource

    def give_shear_and_moment(self, grid_n=100):
        """Returns (position, shear, moment)"""
        x = self.datasource.grid(grid_n)
        return x, self.datasource.Vz, self.datasource.My

    def give_loads_table(self):
        """Returns a 'table' with all the loads.
        point_loads : (Name, location, force, moment) ; all local
        distributed load : (Name, Fz, mean X, start x , end x
        """

        m = self.datasource  # alias
        n = m.nLoads

        point_loads = []
        distributed_loads = []
        for i in range(n):

            load = list(m.load_origin(i))
            effect = m.load(i)

            plotx = effect[0]

            is_distributed = len(plotx) > 2

            if is_distributed:
                load[0] += " *"  # (add a * to the name))

            if (
                np.linalg.norm(load[2]) > 1e-6 or np.linalg.norm(load[3]) > 1e-6
            ):  # only forces that actually do something
                point_loads.append(load)

            if is_distributed:

                name = effect[-1]  # name without the *
                P = load[1]
                F = load[2]
                M = load[3]

                Fz = F[2]
                My = M[1]

                if abs(Fz) > 1e-10:
                    dx = -My / Fz
                    x = P[0] + dx
                else:
                    x = P[0]

                distributed_loads.append([name, Fz, x, plotx[0], plotx[-1]])

        return point_loads, distributed_loads

    def plot_simple(self, **kwargs):
        """Plots the bending moment and shear in a single yy-plot.
        Creates a new figure

        any keyword arguments are passed to plt.figure(), so for example dpi=150 will increase the dpi

        Returns: figure
        """
        x, Vz, My = self.give_shear_and_moment()
        import matplotlib.pyplot as plt

        plt.rcParams.update({"font.family": "sans-serif"})
        plt.rcParams.update({"font.sans-serif": "consolas"})
        plt.rcParams.update({"font.size": 10})

        fig, ax1 = plt.subplots(1, 1, **kwargs)
        ax2 = ax1.twinx()

        ax1.plot(x, My, "g", lw=1, label="Bending Moment")
        ax2.plot(x, Vz, "b", lw=1, label="Shear Force")

        from DAVE.gui.helpers.align_zeros_of_yyplots import align_y0_axis

        align_y0_axis(ax1, ax2)

        ax1.set_xlabel("Position [m]")
        ax1.set_ylabel("Bending Moment [kNm]")
        ax2.set_ylabel("Shear Force [kN]")

        ax1.tick_params(axis="y", colors="g")
        ax2.tick_params(axis="y", colors="b")

        # fig.legend()  - obvious from the axis

        ext = 0.1 * (np.max(x) - np.min(x))
        xx = [np.min(x) - ext, np.max(x) + ext]
        ax1.plot(xx, [0, 0], c=[0.5, 0.5, 0.5], lw=1, linestyle=":")
        ax1.set_xlim(xx)

        return fig

    def plot(self, grid_n=100, merge_adjacent_loads=True, filename=None, do_show=False):
        """Plots the load, shear and bending moments. Returns figure"""
        m = self.datasource  # alias

        x = m.grid(grid_n)
        linewidth = 1

        n = m.nLoads

        import matplotlib.pyplot as plt

        #
        plt.rcParams.update({"font.family": "sans-serif"})
        plt.rcParams.update({"font.sans-serif": "consolas"})
        plt.rcParams.update({"font.size": 6})

        fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(8.27, 11.69), dpi=100)
        textsize = 6

        # get loads

        loads = [m.load(i) for i in range(n)]

        texts = []  # for label placement
        texts_second = []  # for label placement

        # merge loads with same source and matching endpoints

        if merge_adjacent_loads:

            to_be_plotted = [loads[0]]

            for load in loads[1:]:
                name = load[2]

                # if the previous load is a continuous load from the same source
                # and the current load is also a continuous load
                # then merge the two.
                prev_load = to_be_plotted[-1]

                if len(prev_load[0]) != 2:  # not a point-load
                    if len(load[0]) != 2:  # not a point-load
                        if prev_load[2] == load[2]:  # same name

                            # merge the two
                            # remove the last (zero) entry of the previous lds
                            # as well as the first entry of these

                            # smoothed
                            xx = [*prev_load[0][:-1], *load[0][2:]]
                            yy = [
                                *prev_load[1][:-2],
                                0.5 * (prev_load[1][-2] + load[1][1]),
                                *load[1][2:],
                            ]

                            to_be_plotted[-1] = (xx, yy, load[2])

                            continue
                # else
                if np.max(np.abs(load[1])) > 1e-6:
                    to_be_plotted.append(load)

        else:
            to_be_plotted = loads

        #
        from matplotlib import cm

        colors = cm.get_cmap("hsv", lut=len(to_be_plotted))

        from matplotlib.patches import Polygon

        ax0_second = ax0.twinx()

        for icol, ld in enumerate(to_be_plotted):

            xx = ld[0]
            yy = ld[1]
            name = ld[2]

            if np.max(np.abs(yy)) < 1e-6:
                continue

            is_concentrated = len(xx) == 2

            # determine the name, default to Force / q-load if no name is present
            if name == "":
                if is_concentrated:
                    name = "Force "
                else:
                    name = "q-load "

            col = [0.8 * c for c in colors(icol)]
            col[3] = 1.0  # alpha

            if is_concentrated:  # concentrated loads on left axis
                lbl = f" {name} {ld[1][1]:.2f}"
                texts.append(
                    ax0.text(
                        xx[0], yy[1], lbl, fontsize=textsize, horizontalalignment="left"
                    )
                )
                ax0.plot(xx, yy, label=lbl, color=col, linewidth=linewidth)
                if yy[1] > 0:
                    ax0.plot(xx[1], yy[1], marker="^", color=col, linewidth=linewidth)
                else:
                    ax0.plot(xx[1], yy[1], marker="v", color=col, linewidth=linewidth)

            else:  # distributed loads on right axis
                lbl = f"{name}"  # {yy[1]:.2f} kN/m at {xx[0]:.3f}m .. {yy[-2]:.2f} kN/m at {xx[-1]:.3f}m"

                vertices = [(xx[i], yy[i]) for i in range(len(xx))]

                ax0_second.add_patch(
                    Polygon(vertices, facecolor=[col[0], col[1], col[2], 0.2])
                )
                ax0_second.plot(xx, yy, label=lbl, color=col, linewidth=linewidth)

                lx = np.mean(xx)
                ly = np.interp(lx, xx, yy)

                texts_second.append(
                    ax0_second.text(
                        lx,
                        ly,
                        lbl,
                        color=[0, 0, 0],
                        horizontalalignment="center",
                        fontsize=textsize,
                    )
                )

        ax0.grid()
        ax0.set_title("Loads")
        ax0.set_ylabel("Load [kN]")
        ax0_second.set_ylabel("Load [kN/m]")

        # plot moments
        # each concentrated load may have a moment as well
        for i in range(m.nLoads):
            mom = m.moment(i)
            if np.linalg.norm(mom) > 1e-6:
                load = m.load(i)
                xx = load[0][0]
                lbl = f"{load[2]}, m = {mom[1]:.2f} kNm"
                ax0.plot(xx, 0, marker="x", label=lbl, color=(0, 0, 0, 1))
                texts.append(
                    ax0.text(
                        xx, 0, lbl, horizontalalignment="center", fontsize=textsize
                    )
                )

        fig.legend(loc="upper right")

        # add a zero-line
        xx = [np.min(x), np.max(x)]
        ax0.plot(xx, (0, 0), "k-")

        from DAVE.gui.helpers.align_zeros_of_yyplots import align_y0_axis

        align_y0_axis(ax0, ax0_second)

        from DAVE.reporting.utils.TextAvoidOverlap import minimizeTextOverlap

        minimizeTextOverlap(
            texts_second,
            fig=fig,
            ax=ax0_second,
            vertical_only=True,
            optimize_initial_positions=False,
            annotate=False,
        )
        minimizeTextOverlap(
            texts,
            fig=fig,
            ax=ax0,
            vertical_only=True,
            optimize_initial_positions=False,
            annotate=False,
        )

        ax0.spines["top"].set_visible(False)
        ax0.spines["bottom"].set_visible(False)

        ax0_second.spines["top"].set_visible(False)
        ax0_second.spines["bottom"].set_visible(False)

        dx = (np.max(x) - np.min(x)) / 20  # plot scale
        ax1.plot(x, m.Vz, "k-", linewidth=linewidth)

        i = np.argmax(m.Vz)
        ax1.plot((x[i] - dx, x[i] + dx), (m.Vz[i], m.Vz[i]), "k-", linewidth=0.5)
        ax1.text(x[i], m.Vz[i], f"{m.Vz[i]:.2f}", va="bottom", ha="center")

        i = np.argmin(m.Vz)
        ax1.plot((x[i] - dx, x[i] + dx), (m.Vz[i], m.Vz[i]), "k-", linewidth=0.5)
        ax1.text(x[i], m.Vz[i], f"{m.Vz[i]:.2f}", va="top", ha="center")

        ax1.grid()
        ax1.set_title("Shear")
        ax1.set_ylabel("[kN]")

        ax2.plot(x, m.My, "k-", linewidth=linewidth)

        i = np.argmax(m.My)
        ax2.plot((x[i] - dx, x[i] + dx), (m.My[i], m.My[i]), "k-", linewidth=0.5)
        ax2.text(x[i], m.My[i], f"{m.My[i]:.2f}", va="bottom", ha="center")

        i = np.argmin(m.My)
        ax2.plot((x[i] - dx, x[i] + dx), (m.My[i], m.My[i]), "k-", linewidth=0.5)
        ax2.text(x[i], m.My[i], f"{m.My[i]:.2f}", va="top", ha="center")

        ax2.grid()
        ax2.set_title("Moment")
        ax2.set_ylabel("[kN*m]")

        if do_show:
            plt.show()
        if filename is not None:
            fig.savefig(filename)

        return fig
