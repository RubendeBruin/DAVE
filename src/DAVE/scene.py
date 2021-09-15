"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""
import warnings
from abc import ABC, abstractmethod
from enum import Enum

import pyo3d
import numpy as np
import DAVE.settings as vfc
from DAVE.tools import *
from os.path import isfile, split, dirname, exists
from os import listdir
from pathlib import Path
import datetime


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


# Wrapper (decorator) for managed nodes
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
        assert isinstance(scene, Scene)
        if manager is not None:
            assert isinstance(manager, Manager)
        self.scene = scene
        self.manager = manager

    def __enter__(self):
        self._old_manager = self.scene.current_manager
        self.scene.current_manager = self.manager

    def __exit__(self, *args, **kwargs):
        self.scene.current_manager = self._old_manager


class AreaKind(Enum):
    SPHERE = 1
    PLANE = 2
    CYLINDER = 3


class Node(ABC):
    """ABSTRACT CLASS - Properties defined here are applicable to all derived classes
    Master class for all nodes"""

    def __init__(self, scene):
        self._scene: Scene = scene
        """reference to the scene that the node lives is"""

        self._name: str = "A manager without a name"
        """Unique name of the node"""

        self._manager: Node or None = None
        """Reference to a node that controls this node"""

        self.observers = list()
        """List of nodes observing this node."""

        self._visible: bool = True
        """Determines if the visual for of this node (if any) should be visible"""

    def __repr__(self):
        return f"{self.name} <{self.__class__.__name__}>"

    def __str__(self):
        return self.name

    @property
    def class_name(self):
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
    def visible(self):
        if self.manager:
            return self.manager.visible
        return self._visible

    @visible.setter
    @node_setter_manageable
    @node_setter_observable
    def visible(self, value):
        self._visible = value

    @property
    def manager(self):
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
        if self._scene._godmode:
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

    @property
    def name(self):
        """Name of the node (str), must be unique"""
        return self._name

    @name.setter
    @node_setter_manageable
    @node_setter_observable
    def name(self, name):

        self._name = name

    def _delete_vfc(self):
        """Removes any internally created core objects"""
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


class CoreConnectedNode(Node):
    """ABSTRACT CLASS - Properties defined here are applicable to all derived classes
    Master class for all nodes with a connected eqCore element"""

    def __init__(self, scene, vfNode):
        super().__init__(scene)
        self._vfNode = vfNode

    @property
    def name(self):
        """Name of the node (str), must be unique"""
        return self._vfNode.name

    @name.setter
    @node_setter_manageable
    @node_setter_observable
    def name(self, name):

        if not name == self._vfNode.name:
            self._scene._verify_name_available(name)
            self._vfNode.name = name

    def _delete_vfc(self):
        self._scene._vfc.delete(self._vfNode.name)


class NodeWithCoreParent(CoreConnectedNode):
    """
    NodeWithParent

    Do not use this class directly.
    This is a base-class for all nodes that have a "parent" property.
    """

    def __init__(self, scene, vfNode):
        super().__init__(scene, vfNode)
        self._parent = None
        self._None_parent_acceptable = False
        self._parent_for_code_export = True
        """True : use parent, 
        None : use None, 
        Node : use that Node
        Used to prevent circular references, see groups section in documentation"""

    def depends_on(self):
        if self.parent_for_export is not None:
            return [self.parent_for_export]
        else:
            return []

    @property
    def parent_for_export(self):
        if self._parent_for_code_export == True:
            return self._parent
        else:
            return self._parent_for_code_export

    @property
    def parent(self):
        """Determines the parent of the node if any."""
        if self._vfNode.parent is None:
            return None
        else:
            return self._parent
            # return Axis(self._scene, self._vfNode.parent)

    @parent.setter
    @node_setter_manageable
    @node_setter_observable
    def parent(self, var):
        """Assigns a new parent. Keeps the local position and rotations the same

        See also: change_parent_to
        """

        if var is None:

            if not self._None_parent_acceptable:
                raise ValueError(
                    "None is not an acceptable parent for {} of {}".format(
                        self.name, type(self)
                    )
                )

            self._parent = None
            self._vfNode.parent = None
        else:

            var = self._scene._node_from_node_or_str(var)

            if isinstance(var, Frame) or isinstance(var, GeometricContact):
                self._parent = var
                self._vfNode.parent = var._vfNode
            elif isinstance(var, Point):
                self._parent = var
                self._vfNode.parent = var._vfNode
            else:
                raise Exception(
                    "Parent can only be set to an instance of Axis or Poi, not to a {}".format(
                        type(var)
                    )
                )

    def change_parent_to(self, new_parent):
        """Assigns a new parent to the node but keeps the global position and rotation the same.

        See also: .parent (property)

        Args:
            new_parent: new parent node

        """

        if isinstance(self, Point) and isinstance(new_parent, Point):
            raise TypeError("Points can not be placed on points")

        try:
            self.rotation
            has_rotation = True
        except:
            has_rotation = False

        try:
            self.position
            has_position = True
        except:
            has_position = False

        # it is possible that this function is called on an object without position/rotation
        # in that case just fall-back to a change of parent
        if not has_position and not has_rotation:
            self.parent = new_parent
            return

        # check new_parent
        if new_parent is not None:

            if not isinstance(new_parent, Frame):
                if not has_rotation:
                    if not isinstance(new_parent, Point):
                        raise TypeError(
                            "Only Poi-type nodes (or derived types) can be used as parent. You tried to use a {} as parent".format(
                                type(new_parent)
                            )
                        )
                else:
                    raise TypeError(
                        "Only None or Axis-type nodes (or derived types)  can be used as parent. You tried to use a {} as parent".format(
                            type(new_parent)
                        )
                    )

        glob_pos = self.global_position

        if has_rotation:
            glob_rot = self.global_rotation

        self.parent = new_parent

        if new_parent is None:
            self.position = glob_pos
            if has_rotation:
                self.rotation = glob_rot

        else:
            self.position = new_parent.to_loc_position(glob_pos)
            if has_rotation:
                self.rotation = new_parent.to_loc_direction(glob_rot)


class NodeWithParentAndFootprint(NodeWithCoreParent):
    """
    NodeWithParentAndFootprint

    Do not use this class directly.
    This is a base-class for all nodes that have a "footprint" property as well as a parent
    """

    def __init__(self, scene, vfNode):
        super().__init__(scene, vfNode)

    @property
    def footprint(self):
        """tuple of tuples ((x1,y1,z1), (x2,y2,z2), .... (xn,yn,zn)"""
        r = []
        for i in range(self._vfNode.nFootprintVertices):
            r.append(self._vfNode.footprintVertexGet(i))
        return tuple(r)

    @footprint.setter
    def footprint(self, value):
        """Sets the footprint vertices. Supply as an iterable with each element containing three floats"""
        for t in value:
            assert3f(t, "Each entry of value assigned to footprints ")

        self._vfNode.footprintVertexClearAll()
        for t in value:
            self._vfNode.footprintVertexAdd(*t)

    def add_footprint_python_code(self):
        if self.footprint:
            return f"\ns['{self.name}'].footprint = {str(self.footprint)}"
        else:
            return ""


# ==============================================================


class Visual(Node):
    """
    Visual

    .. image:: ./images/visual.png

    A Visual node contains a 3d visual, typically obtained from a .obj file.
    A visual node can be placed on an axis-type node.

    It is used for visualization. It does not affect the forces, dynamics or statics.

    The visual can be given an offset, rotation and scale. These are applied in the following order

    1. rotate
    2. scale
    3. offset

    Hint: To scale before rotation place the visual on a dedicated axis and rotate that axis.

    """

    def __init__(self, scene):

        super().__init__(scene)

        self.offset = [0, 0, 0]
        """Offset (x,y,z) of the visual. Offset is applied after scaling"""
        self.rotation = [0, 0, 0]
        """Rotation (rx,ry,rz) of the visual"""

        self.scale = [1, 1, 1]
        """Scaling of the visual. Scaling is applied before offset."""

        self.path = ""
        """Filename of the visual"""

        self.parent = None
        """Parent : Axis-type"""

    @property
    def file_path(self):
        return self._scene.get_resource_path(self.path)

    def depends_on(self):
        return [self.parent]

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_visual(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent.name)
        code += "\n            path=r'{}',".format(self.path)
        code += "\n            offset=({}, {}, {}), ".format(*self.offset)
        code += "\n            rotation=({}, {}, {}), ".format(*self.rotation)
        code += "\n            scale=({}, {}, {}) )".format(*self.scale)

        return code

    def change_parent_to(self, new_parent):

        if not (isinstance(new_parent, Frame) or new_parent is None):
            raise ValueError(
                "Visuals can only be attached to an axis (or derived) or None"
            )

        # get current position and orientation
        if self.parent is not None:
            cur_position = self.parent.to_glob_position(self.offset)
            cur_rotation = self.parent.to_glob_direction(self.rotation)
        else:
            cur_position = self.offset
            cur_rotation = self.rotation

        self.parent = new_parent

        if new_parent is None:
            self.offset = cur_position
            self.rotation = cur_rotation
        else:
            self.offset = new_parent.to_loc_position(cur_position)
            self.rotation = new_parent.to_loc_direction(cur_rotation)


class Frame(NodeWithParentAndFootprint):
    """
    Axis

    Axes are the main building blocks of the geometry. They have a position and an rotation in space. Other nodes can be placed on them.
    Axes can be nested by parent/child relationships meaning that an axis can be placed on an other axis.
    The possible movements of an axis can be controlled in each degree of freedom using the "fixed" property.

    Axes are also the main building block of inertia.
    Dynamics are controlled using the inertia properties of an axis: inertia [mT], inertia_position[m,m,m] and inertia_radii [m,m,m]


    Notes:
         - circular references are not allowed: It is not allowed to place a on b and b on a

    """

    def __init__(self, scene, vfAxis):
        super().__init__(scene, vfAxis)
        self._None_parent_acceptable = True

        self._inertia = 0
        self._inertia_position = (0, 0, 0)
        self._inertia_radii = (0, 0, 0)

        self._pointmasses = list()
        for i in range(6):
            p = scene._vfc.new_pointmass(
                self.name + vfc.VF_NAME_SPLIT + "pointmass_{}".format(i)
            )
            p.parent = vfAxis
            self._pointmasses.append(p)
        self._update_inertia()

    def depends_on(self):
        if self.parent is None:
            return []
        else:
            return [self.parent]

    def _delete_vfc(self):
        for p in self._pointmasses:
            self._scene._vfc.delete(p.name)

        super()._delete_vfc()

    @property
    def inertia(self):
        """The linear inertia of the axis in [mT] Aka: "Mass"
        - used only for dynamics"""
        return self._inertia

    @inertia.setter
    @node_setter_manageable
    @node_setter_observable
    def inertia(self, val):

        assert1f(val, "Inertia")
        self._inertia = val
        self._update_inertia()

    @property
    def inertia_position(self):
        """The position of the center of inertia. Aka: "cog" [m,m,m] (local axis)
        - used only for dynamics
        - defined in local axis system"""
        return tuple(self._inertia_position)

    @inertia_position.setter
    @node_setter_manageable
    @node_setter_observable
    def inertia_position(self, val):

        assert3f(val, "Inertia position")
        self._inertia_position = tuple(val)
        self._update_inertia()

    @property
    def inertia_radii(self):
        """The radii of gyration of the inertia [m,m,m] (local axis)

        Used to calculate the mass moments of inertia via

        Ixx = rxx^2 * inertia
        Iyy = rxx^2 * inertia
        Izz = rxx^2 * inertia

        Note that DAVE does not directly support cross terms in the interia matrix of an axis system. If you want to
        use cross terms then combine multiple axis system to reach the same result. This is because inertia matrices with
        diagonal terms can not be translated.
        """
        return np.array(self._inertia_radii, dtype=float)

    @inertia_radii.setter
    @node_setter_manageable
    @node_setter_observable
    def inertia_radii(self, val):

        assert3f_positive(val, "Inertia radii of gyration")
        self._inertia_radii = val
        self._update_inertia()

    def _update_inertia(self):
        # update mass
        for i in range(6):
            self._pointmasses[i].inertia = self._inertia / 6

        if self._inertia <= 0:
            return

        # update radii and position
        pos = radii_to_positions(*self._inertia_radii)
        for i in range(6):
            p = (
                pos[i][0] + self._inertia_position[0],
                pos[i][1] + self._inertia_position[1],
                pos[i][2] + self._inertia_position[2],
            )
            self._pointmasses[i].position = p
            # print('{} at {} {} {}'.format(self._inertia/6, *p))

    @property
    def fixed(self):
        """Determines which of the six degrees of freedom are fixed, if any. (x,y,z,rx,ry,rz).
        True means that that degree of freedom will not change when solving statics.
        False means a that is may be changed in order to find equilibrium.

        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)

        See Also: set_free, set_fixed
        """
        return self._vfNode.fixed

    @fixed.setter
    @node_setter_manageable
    @node_setter_observable
    def fixed(self, var):

        if var == True:
            var = (True, True, True, True, True, True)
        if var == False:
            var = (False, False, False, False, False, False)

        self._vfNode.fixed = var

    def set_free(self):
        """Sets .fixed to (False,False,False,False,False,False)"""
        self._vfNode.set_free()

    def set_fixed(self):
        """Sets .fixed to (True,True,True,True,True,True)"""

        self._vfNode.set_fixed()

    @property
    def x(self):
        """The x-component of the position vector (parent axis) [m]"""
        return self.position[0]

    @property
    def y(self):
        """The y-component of the position vector (parent axis) [m]"""
        return self.position[1]

    @property
    def z(self):
        """The z-component of the position vector (parent axis) [m]"""
        return self.position[2]

    @x.setter
    @node_setter_manageable
    @node_setter_observable
    def x(self, var):

        a = self.position
        self.position = (var, a[1], a[2])

    @y.setter
    @node_setter_manageable
    @node_setter_observable
    def y(self, var):

        a = self.position
        self.position = (a[0], var, a[2])

    @z.setter
    @node_setter_manageable
    @node_setter_observable
    def z(self, var):

        a = self.position
        self.position = (a[0], a[1], var)

    @property
    def position(self):
        """Position of the axis (parent axis) [m,m,m]

        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)"""
        return self._vfNode.position

    @position.setter
    @node_setter_manageable
    @node_setter_observable
    def position(self, var):

        assert3f(var, "Position ")
        self._vfNode.position = var
        self._scene._geometry_changed()

    @property
    def rx(self):
        """The x-component of the rotation vector [degrees] (parent axis)"""
        return self.rotation[0]

    @property
    def ry(self):
        """The y-component of the rotation vector [degrees] (parent axis)"""
        return self.rotation[1]

    @property
    def rz(self):
        """The z-component of the rotation vector [degrees], (parent axis)"""
        return self.rotation[2]

    @rx.setter
    @node_setter_manageable
    @node_setter_observable
    def rx(self, var):

        a = self.rotation
        self.rotation = (var, a[1], a[2])

    @ry.setter
    @node_setter_manageable
    @node_setter_observable
    def ry(self, var):

        a = self.rotation
        self.rotation = (a[0], var, a[2])

    @rz.setter
    @node_setter_manageable
    @node_setter_observable
    def rz(self, var):

        a = self.rotation
        self.rotation = (a[0], a[1], var)

    @property
    def rotation(self):
        """Rotation of the axis about its origin (rx,ry,rz).
        Defined as a rotation about an axis where the direction of the axis is (rx,ry,rz) and the angle of rotation is |(rx,ry,rz| degrees.
        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)"""
        return np.rad2deg(self._vfNode.rotation)

    @rotation.setter
    @node_setter_manageable
    @node_setter_observable
    def rotation(self, var):

        # convert to degrees
        assert3f(var, "Rotation ")
        self._vfNode.rotation = np.deg2rad(var)
        self._scene._geometry_changed()

    # we need to over-ride the parent property to be able to call _geometry_changed afterwards
    @property
    def parent(self):
        """Determines the parent of the axis. Should either be another axis or 'None'

        Other axis may be refered to by reference or by name (str). So the following are identical

            p = s.new_frame('parent_axis')
            c = s.new_frame('child axis')

            c.parent = p
            c.parent = 'parent_axis'

        To define that an axis does not have a parent use

            c.parent = None

        """
        return super().parent

    @parent.setter
    @node_setter_manageable
    @node_setter_observable
    def parent(self, val):

        if val is not None:
            # Circular reference check: are we trying to make self depend on val while val depends on self?
            if self._scene.node_A_core_depends_on_B_core(val, self):
                if isinstance(val, Frame):  # it better be
                    val.change_parent_to(
                        None
                    )  # change the parent of other to None, this breaks the previous dependancy

        NodeWithCoreParent.parent.fset(self, val)
        self._scene._geometry_changed()

    @property
    def gx(self):
        """The x-component of the global position vector [m] (global axis )"""
        return self.global_position[0]

    @property
    def gy(self):
        """The y-component of the global position vector [m] (global axis )"""
        return self.global_position[1]

    @property
    def gz(self):
        """The z-component of the global position vector [m] (global axis )"""
        return self.global_position[2]

    @gx.setter
    @node_setter_manageable
    @node_setter_observable
    def gx(self, var):

        a = self.global_position
        self.global_position = (var, a[1], a[2])

    @gy.setter
    @node_setter_manageable
    @node_setter_observable
    def gy(self, var):

        a = self.global_position
        self.global_position = (a[0], var, a[2])

    @gz.setter
    @node_setter_manageable
    @node_setter_observable
    def gz(self, var):

        a = self.global_position
        self.global_position = (a[0], a[1], var)

    @property
    def global_position(self):
        """The global position of the origin of the axis system  [m,m,m] (global axis)"""
        return self._vfNode.global_position

    @global_position.setter
    @node_setter_manageable
    @node_setter_observable
    def global_position(self, val):

        assert3f(val, "Global Position")
        if self.parent:
            self.position = self.parent.to_loc_position(val)
        else:
            self.position = val

    @property
    def grx(self):
        """The x-component of the global rotation vector [degrees] (global axis)"""
        return self.global_rotation[0]

    @property
    def gry(self):
        """The y-component of the global rotation vector [degrees] (global axis)"""
        return self.global_rotation[1]

    @property
    def grz(self):
        """The z-component of the global rotation vector [degrees] (global axis)"""
        return self.global_rotation[2]

    @grx.setter
    @node_setter_manageable
    @node_setter_observable
    def grx(self, var):

        a = self.global_rotation
        self.global_rotation = (var, a[1], a[2])

    @gry.setter
    @node_setter_manageable
    @node_setter_observable
    def gry(self, var):

        a = self.global_rotation
        self.global_rotation = (a[0], var, a[2])

    @grz.setter
    @node_setter_manageable
    @node_setter_observable
    def grz(self, var):

        a = self.global_rotation
        self.global_rotation = (a[0], a[1], var)

    @property
    def tilt_x(self):
        """Tilt percentage. This is the z-component of the unit y vector [%].

        See Also: heel
        """
        y = (0, 1, 0)
        uy = self.to_glob_direction(y)
        return float(100 * uy[2])

    @property
    def heel(self):
        """Heel in degrees. SB down is positive [deg].
        This is the inverse sin of the unit y vector(This is the arcsin of the tiltx)

        See also: tilt_x
        """
        return np.rad2deg(np.arcsin(self.tilt_x / 100))

    @property
    def tilt_y(self):
        """Tilt percentage. This is the z-component of the unit -x vector [%].
        So a positive rotation about the y axis results in a positive tilt_y.

        See Also: trim
        """
        x = (-1, 0, 0)
        ux = self.to_glob_direction(x)
        return float(100 * ux[2])

    @property
    def trim(self):
        """Trim in degrees. Bow-down is positive [deg].

        This is the inverse sin of the unit -x vector(This is the arcsin of the tilt_y)

        See also: tilt_y
        """
        return np.rad2deg(np.arcsin(self.tilt_y / 100))

    @property
    def heading(self):
        """Direction (0..360) [deg] of the local x-axis relative to the global x axis. Measured about the global z axis

        heading = atan(u_y,u_x)

        typically:
            heading 0  --> local axis align with global axis
            heading 90 --> local x-axis in direction of global y axis


        See also: heading_compass
        """
        x = (1, 0, 0)
        ux = self.to_glob_direction(x)
        heading = np.rad2deg(np.arctan2(ux[1], ux[0]))
        return np.mod(heading, 360)

    @property
    def heading_compass(self):
        """The heading (0..360)[deg] assuming that the global y-axis is North and global x-axis is East and rotation accoring compass definition"""
        return np.mod(90 - self.heading, 360)

    @property
    def global_rotation(self):
        """Rotation [deg,deg,deg] (global axis)"""
        return tuple(np.rad2deg(self._vfNode.global_rotation))

    @global_rotation.setter
    @node_setter_manageable
    @node_setter_observable
    def global_rotation(self, val):

        assert3f(val, "Global Rotation")
        if self.parent:
            self.rotation = self.parent.to_loc_rotation(val)
        else:
            self.rotation = val

    @property
    def global_transform(self):
        """Read-only: The global transform of the axis system [matrix]"""
        return self._vfNode.global_transform

    @property
    def connection_force(self):
        """The forces and moments that this axis applies on its parent at the origin of this axis system. [kN, kN, kN, kNm, kNm, kNm] (Parent axis)

        If this axis would be connected to a point on its parent, and that point would be located at the location of the origin of this axis system
        then the connection force equals the force and moment applied on that point.

        Example:
            parent axis with name A
            this axis with name B
            this axis is located on A at position (10,0,0)
            there is a Point at the center of this axis system.
            A force with Fz = -10 acts on the Point.

            The connection_force is (-10,0,0,0,0,0)

            This is the force and moment as applied on A at point (10,0,0)


        """
        return self._vfNode.connection_force

    @property
    def connection_force_x(self):
        """The x-component of the connection-force vector [kN] (Parent axis)"""
        return self.connection_force[0]

    @property
    def connection_force_y(self):
        """The y-component of the connection-force vector [kN] (Parent axis)"""
        return self.connection_force[1]

    @property
    def connection_force_z(self):
        """The z-component of the connection-force vector [kN] (Parent axis)"""
        return self.connection_force[2]

    @property
    def connection_moment_x(self):
        """The mx-component of the connection-force vector [kNm] (Parent axis)"""
        return self.connection_force[3]

    @property
    def connection_moment_y(self):
        """The my-component of the connection-force vector [kNm] (Parent axis)"""
        return self.connection_force[4]

    @property
    def connection_moment_z(self):
        """The mx-component of the connection-force vector [kNm] (Parent axis)"""
        return self.connection_force[5]

    @property
    def applied_force(self):
        """The force and moment that is applied on origin of this axis [kN, kN, kN, kNm, kNm, kNm] (Global axis)"""
        return self._vfNode.applied_force

    @property
    def ux(self):
        """The unit x axis [m,m,m] (Global axis)"""
        return self.to_glob_direction((1, 0, 0))

    @property
    def uy(self):
        """The unit y axis [m,m,m] (Global axis)"""
        return self.to_glob_direction((0, 1, 0))

    @property
    def uz(self):
        """The unit z axis [m,m,m] (Global axis)"""
        return self.to_glob_direction((0, 0, 1))

    @property
    def equilibrium_error(self):
        """The unresolved force and moment that on this axis. Should be zero when in equilibrium  (applied-force minus connection force, Parent axis)"""
        return self._vfNode.equilibrium_error

    def to_loc_position(self, value):
        """Returns the local position of a point in the global axis system.
        This considers the position and the rotation of the axis system.
        See Also: to_loc_direction
        """
        return self._vfNode.global_to_local_point(value)

    def to_glob_position(self, value):
        """Returns the global position of a point in the local axis system.
        This considers the position and the rotation of the axis system.
        See Also: to_glob_direction
        """
        return self._vfNode.local_to_global_point(value)

    def to_loc_direction(self, value):
        """Returns the local direction of a point in the global axis system.
        This considers only the rotation of the axis system.
        See Also: to_loc_position
        """
        return self._vfNode.global_to_local_vector(value)

    def to_glob_direction(self, value):
        """Returns the global direction of a point in the local axis system.
        This considers only the rotation of the axis system.
        See Also: to_glob_position"""
        return self._vfNode.local_to_global_vector(value)

    def to_loc_rotation(self, value):
        """Returns the local rotation. Used for rotating rotations.
        See Also: to_loc_position, to_loc_direction
        """
        return np.rad2deg(self._vfNode.global_to_local_rotation(np.deg2rad(value)))

    def to_glob_rotation(self, value):
        """Returns the global rotation. Used for rotating rotations.
        See Also: to_loc_position, to_loc_direction
        """
        return np.rad2deg(self._vfNode.local_to_global_rotation(np.deg2rad(value)))

    def give_load_shear_moment_diagram(
        self, axis_system=None
    ) -> "LoadShearMomentDiagram":
        """Returns a LoadShearMoment diagram

        Args:
            axis_system : optional : coordinate system [axis node] to be used for calculation of the diagram.
            Defaults to the local axis system
        """

        if axis_system is None:
            axis_system = self

        assert isinstance(axis_system, Frame), ValueError(
            f"axis_system shall be an instance of Axis, but it is of type {type(axis_system)}"
        )

        self._scene.update()

        # calculate in the right global direction
        glob_dir = axis_system.to_glob_direction((1, 0, 0))
        self._scene._vfc.calculateBendingMoments(*glob_dir)

        lsm = self._vfNode.getBendingMomentDiagram(axis_system._vfNode)

        return LoadShearMomentDiagram(lsm)

    def change_parent_to(self, new_parent):
        """Assigns a new parent to the node but keeps the global position and rotation the same.

        See also: .parent (property)

        Args:
            new_parent: new parent node

        """

        # check new_parent
        if new_parent is not None:
            if not (
                isinstance(new_parent, Frame)
                or isinstance(new_parent, GeometricContact)
            ):
                raise TypeError(
                    "Only None or Axis-type nodes (or derived types) can be used as parent. You tried to use a {} as parent".format(
                        type(new_parent)
                    )
                )

        glob_pos = self.global_position
        glob_rot = self.global_rotation
        self.parent = new_parent
        self.global_position = glob_pos
        self.global_rotation = glob_rot

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\ns.new_frame(name='{}',".format(self.name)
        if self.parent_for_export:
            code += "\n           parent='{}',".format(self.parent_for_export.name)

        # position

        if self.fixed[0] or not self._scene._export_code_with_solved_function:
            code += "\n           position=({},".format(self.position[0])
        else:
            code += "\n           position=(solved({}),".format(self.position[0])
        if self.fixed[1] or not self._scene._export_code_with_solved_function:
            code += "\n                     {},".format(self.position[1])
        else:
            code += "\n                     solved({}),".format(self.position[1])
        if self.fixed[2] or not self._scene._export_code_with_solved_function:
            code += "\n                     {}),".format(self.position[2])
        else:
            code += "\n                     solved({})),".format(self.position[2])

        # rotation

        if self.fixed[3] or not self._scene._export_code_with_solved_function:
            code += "\n           rotation=({},".format(self.rotation[0])
        else:
            code += "\n           rotation=(solved({}),".format(self.rotation[0])
        if self.fixed[4] or not self._scene._export_code_with_solved_function:
            code += "\n                     {},".format(self.rotation[1])
        else:
            code += "\n                     solved({}),".format(self.rotation[1])
        if self.fixed[5] or not self._scene._export_code_with_solved_function:
            code += "\n                     {}),".format(self.rotation[2])
        else:
            code += "\n                     solved({})),".format(self.rotation[2])

        # inertia and radii of gyration
        if self.inertia > 0:
            code += "\n                     inertia = {},".format(self.inertia)

        if np.any(self.inertia_radii > 0):
            code += "\n                     inertia_radii = ({}, {}, {}),".format(
                *self.inertia_radii
            )

        # fixeties
        code += "\n           fixed =({}, {}, {}, {}, {}, {}) )".format(*self.fixed)

        code += self.add_footprint_python_code()

        return code


class Point(NodeWithParentAndFootprint):
    """A location on an axis"""

    # init parent and name are fully derived from NodeWithParent
    # _vfNode is a poi
    def __init__(self, scene, vfPoi):
        super().__init__(scene, vfPoi)
        self._None_parent_acceptable = True

    def on_observed_node_changed(self, changed_node):
        print(changed_node.name + " has changed")

    @property
    def x(self):
        """x component of local position [m] (parent axis)"""
        return self.position[0]

    @property
    def y(self):
        """y component of local position [m] (parent axis)"""
        return self.position[1]

    @property
    def z(self):
        """z component of local position [m] (parent axis)"""
        return self.position[2]

    @x.setter
    @node_setter_manageable
    @node_setter_observable
    def x(self, var):

        a = self.position
        self.position = (var, a[1], a[2])

    @y.setter
    @node_setter_manageable
    @node_setter_observable
    def y(self, var):

        a = self.position
        self.position = (a[0], var, a[2])

    @z.setter
    @node_setter_manageable
    @node_setter_observable
    @node_setter_manageable
    def z(self, var):

        """z component of local position"""
        a = self.position
        self.position = (a[0], a[1], var)

    @property
    def position(self):
        """Local position [m,m,m] (parent axis)"""
        return self._vfNode.position

    @position.setter
    @node_setter_manageable
    @node_setter_observable
    def position(self, new_position):

        assert3f(new_position)
        self._vfNode.position = new_position

    @property
    def applied_force_and_moment_global(self):
        """Applied force and moment on this point [kN, kN, kN, kNm, kNm, kNm] (Global axis)"""
        return self._vfNode.applied_force

    @property
    def gx(self):
        """x component of position [m] (global axis)"""
        return self.global_position[0]

    @property
    def gy(self):
        """y component of position [m] (global axis)"""
        return self.global_position[1]

    @property
    def gz(self):
        """z component of position [m] (global axis)"""
        return self.global_position[2]

    @gx.setter
    @node_setter_manageable
    @node_setter_observable
    def gx(self, var):

        a = self.global_position
        self.global_position = (var, a[1], a[2])

    @gy.setter
    @node_setter_manageable
    @node_setter_observable
    def gy(self, var):

        a = self.global_position
        self.global_position = (a[0], var, a[2])

    @gz.setter
    @node_setter_manageable
    @node_setter_observable
    def gz(self, var):

        a = self.global_position
        self.global_position = (a[0], a[1], var)

    @property
    def global_position(self):
        """Global position [m,m,m] (global axis)"""
        return self._vfNode.global_position

    @global_position.setter
    @node_setter_manageable
    @node_setter_observable
    def global_position(self, val):

        assert3f(val, "Global Position")
        if self.parent:
            self.position = self.parent.to_loc_position(val)
        else:
            self.position = val

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\ns.new_point(name='{}',".format(self.name)
        if self.parent_for_export:
            code += "\n          parent='{}',".format(self.parent_for_export.name)

        # position

        code += "\n          position=({},".format(self.position[0])
        code += "\n                    {},".format(self.position[1])
        code += "\n                    {}))".format(self.position[2])

        code += self.add_footprint_python_code()

        return code


class RigidBody(Frame):
    """A Rigid body, internally composed of an axis, a point (cog) and a force (gravity)"""

    def __init__(self, scene, axis, poi, force):
        super().__init__(scene, axis)

        # The axis is the Node
        # poi and force are added separately

        self._vfPoi = poi
        self._vfForce = force

    # override the following properties
    # - name : sets the names of poi and force as well

    def _delete_vfc(self):
        super()._delete_vfc()
        self._scene._vfc.delete(self._vfPoi.name)
        self._scene._vfc.delete(self._vfForce.name)

    @property  # can not define a setter without a getter..?
    def name(self):
        return super().name

    @name.setter
    @node_setter_manageable
    @node_setter_observable
    def name(self, newname):
        """Name of the node (str), must be unique"""

        # super().name = newname
        super(RigidBody, self.__class__).name.fset(self, newname)
        self._vfPoi.name = newname + vfc.VF_NAME_SPLIT + "cog"
        self._vfForce.name = newname + vfc.VF_NAME_SPLIT + "gravity"

    @property
    def footprint(self):
        return super().footprint

    @footprint.setter
    def footprint(self, value):
        """Sets the footprint vertices. Supply as an iterable with each element containing three floats"""
        super(RigidBody, type(self)).footprint.fset(
            self, value
        )  # https://bugs.python.org/issue14965

        # assign the footprint to the CoG as well,
        # but subtract the cog position as
        self._sync_selfweight_footprint()

    def _sync_selfweight_footprint(self):
        """The footprint of the CoG is defined relative to the CoG, so its needs to be updated
        whenever the CoG or the footprint changes"""

        fp = self.footprint

        self._vfPoi.footprintVertexClearAll()
        for t in fp:
            pos = np.array(t, dtype=float)
            relpos = pos - self.cog
            self._vfPoi.footprintVertexAdd(*relpos)

    @property
    def cogx(self):
        """x-component of cog position [m] (local axis)"""
        return self.cog[0]

    @property
    def cogy(self):
        """y-component of cog position [m] (local axis)"""
        return self.cog[1]

    @property
    def cogz(self):
        """z-component of cog position [m] (local axis)"""
        return self.cog[2]

    @property
    def cog(self):
        """Center of Gravity position [m,m,m] (local axis)"""
        return self._vfPoi.position

    @cogx.setter
    @node_setter_manageable
    @node_setter_observable
    def cogx(self, var):

        a = self.cog
        self.cog = (var, a[1], a[2])

    @cogy.setter
    @node_setter_manageable
    @node_setter_observable
    def cogy(self, var):

        a = self.cog
        self.cog = (a[0], var, a[2])

    @cogz.setter
    @node_setter_manageable
    @node_setter_observable
    def cogz(self, var):

        a = self.cog
        self.cog = (a[0], a[1], var)

    @cog.setter
    @node_setter_manageable
    @node_setter_observable
    def cog(self, newcog):

        assert3f(newcog)
        self._vfPoi.position = newcog
        self.inertia_position = self.cog
        self._sync_selfweight_footprint()

    @property
    def mass(self):
        """Static mass of the body [mT]

        See Also: inertia
        """
        return self._vfForce.force[2] / -self._scene.g

    @mass.setter
    @node_setter_manageable
    @node_setter_observable
    def mass(self, newmass):

        assert1f(newmass)
        self.inertia = newmass
        self._vfForce.force = (0, 0, -self._scene.g * newmass)

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\ns.new_rigidbody(name='{}',".format(self.name)
        code += "\n                mass={},".format(self.mass)
        code += "\n                cog=({},".format(self.cog[0])
        code += "\n                     {},".format(self.cog[1])
        code += "\n                     {}),".format(self.cog[2])

        if self.parent_for_export:
            code += "\n                parent='{}',".format(self.parent_for_export.name)

        # position

        if self.fixed[0] or not self._scene._export_code_with_solved_function:
            code += "\n                position=({},".format(self.position[0])
        else:
            code += "\n                position=(solved({}),".format(self.position[0])
        if self.fixed[1] or not self._scene._export_code_with_solved_function:
            code += "\n                          {},".format(self.position[1])
        else:
            code += "\n                          solved({}),".format(self.position[1])
        if self.fixed[2] or not self._scene._export_code_with_solved_function:
            code += "\n                          {}),".format(self.position[2])
        else:
            code += "\n                          solved({})),".format(self.position[2])

        # rotation

        if self.fixed[3] or not self._scene._export_code_with_solved_function:
            code += "\n                rotation=({},".format(self.rotation[0])
        else:
            code += "\n                rotation=(solved({}),".format(self.rotation[0])
        if self.fixed[4] or not self._scene._export_code_with_solved_function:
            code += "\n                          {},".format(self.rotation[1])
        else:
            code += "\n                          solved({}),".format(self.rotation[1])
        if self.fixed[5] or not self._scene._export_code_with_solved_function:
            code += "\n                          {}),".format(self.rotation[2])
        else:
            code += "\n                          solved({})),".format(self.rotation[2])

        if np.any(self.inertia_radii > 0):
            code += "\n                     inertia_radii = ({}, {}, {}),".format(
                *self.inertia_radii
            )

        code += "\n                fixed =({}, {}, {}, {}, {}, {}) )".format(
            *self.fixed
        )

        code += self.add_footprint_python_code()

        return code


class Cable(CoreConnectedNode):
    """A Cable represents a linear elastic wire running from a Poi or sheave to another Poi of sheave.

    A cable has a un-stretched length [length] and a stiffness [EA] and may have a diameter [m]. The tension in the cable is calculated.

    Intermediate pois or sheaves may be added.

    - Pois are considered as sheaves with a zero diameter.
    - Sheaves are considered sheaves with the given geometry. If defined then the diameter of the cable is considered when calculating the geometry. The cable runs over the sheave in the positive direction (right hand rule) as defined by the axis of the sheave.

    For cables running over a sheave the friction in sideways direction is considered to be infinite. The geometry is calculated such that the
    cable section between sheaves is perpendicular to the vector from the axis of the sheave to the point where the cable leaves the sheave.

    This assumption results in undefined behaviour when the axis of the sheave is parallel to the cable direction.

    Notes:
        If pois or sheaves on a cable come too close together (<1mm) then they will be pushed away from eachother.
        This prevents the unwanted situation where multiple pois end up at the same location. In that case it can not be determined which amount of force should be applied to each of the pois.


    """

    def __init__(self, scene, node):
        super().__init__(scene, node)
        self._pois = list()

    def depends_on(self):
        return [*self._pois]

    @property
    def tension(self):
        """Tension in the cable [kN]"""
        return self._vfNode.tension

    @property
    def stretch(self):
        """Stretch of the cable [m]

        Tension [kN] = EA [kN] * stretch [m] / length [m]
        """
        return self._vfNode.stretch

    @property
    def length(self):
        """Length of the cable when in rest [m]

        Tension [kN] = EA [kN] * stretch [m] / length [m]
        """
        return self._vfNode.Length

    @length.setter
    @node_setter_manageable
    @node_setter_observable
    def length(self, val):

        if val < 1e-9:
            raise Exception(
                "Length shall be more than 0 (otherwise stiffness EA/L becomes infinite)"
            )
        self._vfNode.Length = val

    @property
    def EA(self):
        """Stiffness of the cable [kN]

        Tension [kN] = EA [kN] * stretch [m] / length [m]
        """
        return self._vfNode.EA

    @EA.setter
    @node_setter_manageable
    @node_setter_observable
    def EA(self, ea):

        self._vfNode.EA = ea

    @property
    def diameter(self):
        """Diameter of the cable. Used when a cable runs over a circle. [m]"""
        return self._vfNode.diameter

    @diameter.setter
    @node_setter_manageable
    @node_setter_observable
    def diameter(self, diameter):

        self._vfNode.diameter = diameter

    @property
    def connections(self):
        """List or Tuple of nodes that this cable is connected to. Nodes may be passed by name (string) or by reference.

        Example:
            p1 = s.new_point('point 1')
            p2 = s.new_point('point 2', position = (0,0,10)
            p3 = s.new_point('point 3', position = (10,0,10)
            c1 = s.new_circle('circle 1',parent = p3, axis = (0,1,0), radius = 1)
            c = s.new_cable("cable_1", endA="Point", endB = "Circle", length = 1.2, EA = 10000)

            c.connections = ('point 1', 'point 2', 'point 3')
            # or
            c.connections = (p1, p2,p3)
            # or
            c.connections = [p1, 'point 2', p3]  # all the same

        Notes:
            1. Circles can not be used as endpoins. If one of the endpoints is a Circle then the Point that that circle
            is located on is used instead.
            2. Points should not be repeated directly.

        The following will fail:
        c.connections = ('point 1', 'point 3', 'circle 1')

        because the last point is a circle. So circle 1 will be replaced with the point that the circle is on: point 3.

        so this becomes
        ('point 1','point 3','point 3')

        this is invalid because point 3 is repeated.

        """
        return tuple(self._pois)

    @connections.setter
    @node_setter_manageable
    @node_setter_observable
    def connections(self, value):

        if len(value) < 2:
            raise ValueError("At least two connections required")

        nodes = []
        for p in value:
            n = self._scene._node_from_node_or_str(p)

            if not (isinstance(n, Point) or isinstance(n, Circle)):
                raise ValueError(
                    f"Only Sheaves and Pois can be used as connection, but {n.name} is a {type(n)}"
                )
            nodes.append(n)

        # check for repeated nodes
        n = len(nodes)
        for i in range(n - 1):
            node1 = nodes[i]
            node2 = nodes[i + 1]

            # Taken care off in c++
            # # # if first or last node is a sheave, the this will be replaced by the poi of the sheave
            # # Except if the fist and the last sheave are the same (loop)
            #
            # if nodes[0] != nodes[-1]:  # first node is not the same as last node
            #     if i == 0 and isinstance(node1, Circle):
            #         node1 = node1.parent
            #     if i == n - 2 and isinstance(node2, Circle):
            #         node2 = node2.parent

            if node1 == node2:
                raise ValueError(
                    f"It is not allowed to have the same node repeated - you have {node1.name} and {node2.name}"
                )

        self._pois.clear()
        self._pois.extend(nodes)
        self._update_pois()

    def get_points_for_visual(self):
        """A list of 3D locations which can be used for visualization"""
        return self._vfNode.global_points

    def _add_connection_to_core(self, connection):
        if isinstance(connection, Point):
            self._vfNode.add_connection_poi(connection._vfNode)
        if isinstance(connection, Circle):
            self._vfNode.add_connection_sheave(connection._vfNode)

    def _update_pois(self):
        self._vfNode.clear_connections()
        for point in self._pois:
            self._add_connection_to_core(point)

    def _give_poi_names(self):
        """Returns a list with the names of all the pois"""
        r = list()
        for p in self._pois:
            r.append(p.name)
        return r

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        poi_names = self._give_poi_names()
        n_sheaves = len(poi_names) - 2

        code += "\ns.new_cable(name='{}',".format(self.name)
        code += "\n            endA='{}',".format(poi_names[0])
        code += "\n            endB='{}',".format(poi_names[-1])
        code += "\n            length={},".format(self.length)

        if self.diameter != 0:
            code += "\n            diameter={},".format(self.diameter)

        if len(poi_names) <= 2:
            code += "\n            EA={})".format(self.EA)
        else:
            code += "\n            EA={},".format(self.EA)

            if n_sheaves == 1:
                code += "\n            sheaves = ['{}'])".format(poi_names[1])
            else:
                code += "\n            sheaves = ['{}',".format(poi_names[1])
                for i in range(n_sheaves - 2):
                    code += "\n                       '{}',".format(poi_names[2 + i])
                code += "\n                       '{}']),".format(poi_names[-2])

        return code


class Force(NodeWithCoreParent):
    """A Force models a force and moment on a poi.

    Both are expressed in the global axis system.

    """

    @property
    def force(self):
        """The x,y and z components of the force [kN,kN,kN] (global axis)

        Example s['wind'].force = (12,34,56)
        """
        return self._vfNode.force

    @force.setter
    @node_setter_manageable
    @node_setter_observable
    def force(self, val):

        assert3f(val)
        self._vfNode.force = val

    @property
    def fx(self):
        """The global x-component of the force [kN] (global axis)"""
        return self.force[0]

    @fx.setter
    @node_setter_manageable
    @node_setter_observable
    def fx(self, var):

        a = self.force
        self.force = (var, a[1], a[2])

    @property
    def fy(self):
        """The global y-component of the force [kN]  (global axis)"""
        return self.force[1]

    @fy.setter
    @node_setter_manageable
    @node_setter_observable
    def fy(self, var):

        a = self.force
        self.force = (a[0], var, a[2])

    @property
    def fz(self):
        """The global z-component of the force [kN]  (global axis)"""

        return self.force[2]

    @fz.setter
    @node_setter_manageable
    @node_setter_observable
    def fz(self, var):

        a = self.force
        self.force = (a[0], a[1], var)

    @property
    def moment(self):
        """The x,y and z components of the moment (kNm,kNm,kNm) in the global axis system.

        Example s['wind'].moment = (12,34,56)
        """
        return self._vfNode.moment

    @moment.setter
    @node_setter_manageable
    @node_setter_observable
    def moment(self, val):

        assert3f(val)
        self._vfNode.moment = val

    @property
    def mx(self):
        """The global x-component of the moment [kNm]  (global axis)"""
        return self.moment[0]

    @mx.setter
    @node_setter_manageable
    @node_setter_observable
    def mx(self, var):

        a = self.moment
        self.moment = (var, a[1], a[2])

    @property
    def my(self):
        """The global y-component of the moment [kNm]  (global axis)"""
        return self.moment[1]

    @my.setter
    @node_setter_manageable
    @node_setter_observable
    def my(self, var):

        a = self.moment
        self.moment = (a[0], var, a[2])

    @property
    def mz(self):
        """The global z-component of the moment [kNm]  (global axis)"""
        return self.moment[2]

    @mz.setter
    @node_setter_manageable
    @node_setter_observable
    def mz(self, var):

        a = self.moment
        self.moment = (a[0], a[1], var)

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        # new_force(self, name, parent=None, force=None, moment=None):

        code += "\ns.new_force(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent_for_export.name)
        code += "\n            force=({}, {}, {}),".format(*self.force)
        code += "\n            moment=({}, {}, {}) )".format(*self.moment)
        return code


class _Area(NodeWithCoreParent):
    """Abstract Based class for wind and current areas."""

    @property
    def force(self):
        """The x,y and z components of the force [kN,kN,kN] (global axis)"""
        return self._vfNode.force

    @property
    def fx(self):
        """The global x-component of the force [kN] (global axis)"""
        return self.force[0]

    @property
    def fy(self):
        """The global y-component of the force [kN]  (global axis)"""
        return self.force[1]

    @property
    def fz(self):
        """The global z-component of the force [kN]  (global axis)"""

        return self.force[2]

    @property
    def A(self):
        """Total area [m2]. See also Ae"""
        return self._vfNode.A0

    @A.setter
    def A(self, value):
        assert1f_positive_or_zero(value, "Area")
        self._vfNode.A0 = value

    @property
    def Ae(self):
        """Effective area [m2]. This is the projection of the total to the actual wind/current direction. Read only."""
        return self._vfNode.Ae

    @property
    def Cd(self):
        """Cd coefficient [-]"""
        return self._vfNode.Cd

    @Cd.setter
    def Cd(self, value):
        assert1f_positive_or_zero(value, "Cd")
        self._vfNode.Cd = value

    @property
    def direction(self):
        """Depends on 'areakind'. For 'plane' this is the direction of the normal of the plane, for 'cylindrical' this is
        the direction of the axis and for 'sphere' this is not used [m,m,m]"""
        return self._vfNode.direction

    @direction.setter
    def direction(self, value):
        assert3f(value, "direction")
        assert np.linalg.norm(value) > 0, ValueError("direction can not be 0,0,0")

        self._vfNode.direction = value

    @property
    def areakind(self):
        """Defines how to interpret the area.
        See also: `direction`"""
        return AreaKind(self._vfNode.type)

    @areakind.setter
    def areakind(self, value):
        if not isinstance(value, AreaKind):
            raise ValueError("kind shall be an instance of Area")
        self._vfNode.type = value.value

    def _give_python_code(self, new_command):
        code = "# code for {}".format(self.name)

        # new_force(self, name, parent=None, force=None, moment=None):

        code += "\ns.{}(name='{}',".format(new_command, self.name)
        code += "\n            parent='{}',".format(self.parent_for_export.name)
        code += f"\n            A={self.A}, "
        code += f"\n            Cd={self.Cd}, "
        if self.areakind != AreaKind.SPHERE:
            code += "\n            direction=({},{},{}),".format(*self.direction)
        code += f"\n            areakind={str(self.areakind)})"

        return code


class WindArea(_Area):
    def give_python_code(self):
        return self._give_python_code("new_windarea")


class CurrentArea(_Area):
    def give_python_code(self):
        return self._give_python_code("new_currentarea")


class ContactMesh(NodeWithCoreParent):
    """A ContactMesh is a tri-mesh with an axis parent"""

    def __init__(self, scene, vfContactMesh):
        super().__init__(scene, vfContactMesh)
        self._None_parent_acceptable = True
        self._trimesh = TriMeshSource(
            self._scene, self._vfNode.trimesh
        )  # the tri-mesh is wrapped in a custom object

    @property
    def trimesh(self):
        """The TriMeshSource object which can be used to change the mesh

        Example:
            s['Contactmesh'].trimesh.load_file('cube.obj', scale = (1.0,1.0,1.0), rotation = (0.0,0.0,0.0), offset = (0.0,0.0,0.0))
        """
        return self._trimesh

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\nmesh = s.new_contactmesh(name='{}'".format(self.name)
        if self.parent_for_export:
            code += ", parent='{}')".format(self.parent_for_export.name)
        else:
            code += ")"
        code += "\nmesh.trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}))".format(
            self.trimesh._path,
            *self.trimesh._scale,
            *self.trimesh._rotation,
            *self.trimesh._offset,
        )

        return code


class ContactBall(NodeWithCoreParent):
    """A ContactBall is a linear elastic ball which can contact with ContactMeshes.

    It is modelled as a sphere around a Poi. Radius and stiffness can be controlled using radius and k.

    The force is applied on the Poi and it not registered separately.
    """

    def __init__(self, scene, node):
        super().__init__(scene, node)
        self._meshes = list()

    @property
    def can_contact(self) -> bool:
        """True if the ball ball is perpendicular to at least one of the faces of one of the meshes. So when contact is possible. To check if there is contact use "force"
        See Also: Force
        """
        return self._vfNode.has_contact

    @property
    def contact_force(self) -> tuple:
        """Returns the force on the ball [kN, kN, kN] (global axis)

        The force is applied at the center of the ball

        See Also: contact_force_magnitude
        """
        return self._vfNode.force

    @property
    def contact_force_magnitude(self) -> float:
        """Returns the absolute force on the ball, if any [kN]

        The force is applied on the center of the ball

        See Also: contact_force
        """
        return np.linalg.norm(self._vfNode.force)

    @property
    def compression(self) -> float:
        """Returns the absolute compression of the ball, if any [m]"""
        return self._vfNode.force

    @property
    def contactpoint(self):
        """The nearest point on the nearest mesh. Only defined"""
        return self._vfNode.contact_point

    def update(self):
        """Updates the contact-points and applies forces on mesh and point"""
        self._vfNode.update()

    @property
    def meshes(self) -> tuple:
        """List of contact-mesh nodes.
        When getting this will yield a list of node references.
        When setting node references and node-names may be used.

        eg: ball.meshes = [mesh1, 'mesh2']
        """
        return tuple(self._meshes)

    @meshes.setter
    @node_setter_manageable
    @node_setter_observable
    def meshes(self, value):

        meshes = []

        for m in value:
            cm = self._scene._node_from_node_or_str(m)

            if not isinstance(cm, ContactMesh):
                raise ValueError(
                    f"Only ContactMesh nodes can be used as mesh, but {cm.name} is a {type(cm)}"
                )
            if cm in meshes:
                raise ValueError(f"Can not add {cm.name} twice")

            meshes.append(cm)

        # copy to meshes
        self._meshes.clear()
        self._vfNode.clear_contactmeshes()
        for mesh in meshes:
            self._meshes.append(mesh)
            self._vfNode.add_contactmesh(mesh._vfNode)

    @property
    def meshes_names(self) -> list:
        """List with the names of the meshes"""
        return [m.name for m in self._meshes]

    @property
    def radius(self):
        """Radius of the contact-ball [m]"""
        return self._vfNode.radius

    @radius.setter
    @node_setter_manageable
    @node_setter_observable
    def radius(self, value):

        assert1f_positive_or_zero(value, "radius")
        self._vfNode.radius = value
        pass

    @property
    def k(self):
        """Compression stiffness of the ball in force per meter of compression [kN/m]"""
        return self._vfNode.k

    @k.setter
    @node_setter_manageable
    @node_setter_observable
    def k(self, value):

        assert1f_positive_or_zero(value, "k")
        self._vfNode.k = value
        pass

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_contactball(name='{}',".format(self.name)
        code += "\n                  parent='{}',".format(self.parent_for_export.name)
        code += "\n                  radius={},".format(self.radius)
        code += "\n                  k={},".format(self.k)
        code += "\n                  meshes = [ "

        for m in self._meshes:
            code += '"' + m.name + '",'
        code = code[:-1] + "])"

        return code

    # =======================================================================


class SPMT(NodeWithCoreParent):
    """An SPMT is a Self-propelled modular transporter

    These are platform vehicles

    ============  =======
    0 0 0 0 0 0   0 0 0 0

    A number of axles share a common suspension system.

    The SPMT node models such a system of axles.

    The SPMT is attached to an axis system.
    The upper locations of the axles are given as an array of 3d vectors.

    Rays are extended from these points in local -Z direction (down) until they hit a contact-shape.

    If no contact shape is found (or not within the maximum distance per axles) then the maximum defined extension for that axle is used.

    A shared pressure is obtained from the combination of all individual extensions.

    Finally an equal force is applied on all the axle connection points. This force acts in local Z direction.

    """

    def __init__(self, scene, node):
        super().__init__(scene, node)
        self._meshes = list()

    # read-only

    @property
    def axle_force(self) -> tuple:
        """Returns the force on each of the axles [kN, kN, kN] (global axis)"""
        return self._vfNode.force

    @property
    def compression(self) -> float:
        """Returns the total compression of all the axles together [m]"""
        return self._vfNode.compression

    def get_actual_global_points(self):
        """Returns a list of points: axle1, bottom wheels 1, axle2, bottom wheels 2, etc"""
        gp = self._vfNode.actual_global_points

        pts = []
        n2 = int(len(gp) / 2)
        for i in range(n2):
            pts.append(gp[2 * i + 1])
            pts.append(gp[2 * i])

            if i < n2 - 1:
                pts.append(gp[2 * i + 2])

        return pts

    # controllable

    # name is derived
    # parent is derived

    @property
    def k(self):
        """Compression stiffness of the ball in force per meter of compression [kN/m]"""
        return self._vfNode.k

    @k.setter
    @node_setter_manageable
    @node_setter_observable
    def k(self, value):

        assert1f_positive_or_zero(value, "k")
        self._vfNode.k = value
        pass

    @property
    def nominal_length(self):
        """Average Axle extension (defined point to bottom of wheel) for zero force [m]"""
        return self._vfNode.nominal_length

    @nominal_length.setter
    @node_setter_manageable
    @node_setter_observable
    def nominal_length(self, value):

        assert1f_positive_or_zero(value, "nominal_length")
        self._vfNode.nominal_length = value
        pass

    @property
    def max_length(self):
        """Maximum axle extension per axle (defined point to bottom of wheel) [m]"""
        return self._vfNode.max_length

    @max_length.setter
    @node_setter_manageable
    @node_setter_observable
    def max_length(self, value):

        assert1f_positive_or_zero(value, "max_length")
        self._vfNode.max_length = value
        pass

    # === control meshes ====

    @property
    def meshes(self) -> tuple:
        """List of contact-mesh nodes.
        When getting this will yield a list of node references.
        When setting node references and node-names may be used.

        eg: ball.meshes = [mesh1, 'mesh2']
        """
        return tuple(self._meshes)

    @meshes.setter
    @node_setter_manageable
    @node_setter_observable
    def meshes(self, value):

        meshes = []

        for m in value:
            cm = self._scene._node_from_node_or_str(m)

            if not isinstance(cm, ContactMesh):
                raise ValueError(
                    f"Only ContactMesh nodes can be used as mesh, but {cm.name} is a {type(cm)}"
                )
            if cm in meshes:
                raise ValueError(f"Can not add {cm.name} twice")

            meshes.append(cm)

        # copy to meshes
        self._meshes.clear()
        self._vfNode.clear_contact_meshes()
        for mesh in meshes:
            self._meshes.append(mesh)
            self._vfNode.add_contact_mesh(mesh._vfNode)

    @property
    def meshes_names(self) -> list:
        """List with the names of the meshes"""
        return [m.name for m in self._meshes]

    # === control axles ====

    def make_grid(self, nx=3, ny=1, dx=1.4, dy=1.45):
        offx = nx * dx / 2
        offy = ny * dy / 2
        self._vfNode.clear_axles()

        for ix in range(nx):
            for iy in range(ny):
                self._vfNode.add_axle(ix * dx - offx, iy * dy - offy, 0)

    @property
    def axles(self):
        """Axles is a list axle positions. Each entry is a (x,y,z) entry which determines the location of the axle on
        SPMT. This is relative to the parent of the SPMT.

        Example:
            [(-10,0,0),(-5,0,0),(0,0,0)] for three axles
        """
        return self._vfNode.get_axles()

    @axles.setter
    @node_setter_manageable
    @node_setter_observable
    def axles(self, value):
        self._vfNode.clear_axles()
        for v in value:
            assert3f(v, "Each entry should contain three floating point numbers")
            self._vfNode.add_axle(*v)

    # actions

    def update(self):
        """Updates the contact-points and applies forces on mesh and point"""
        self._vfNode.update()

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_spmt(name='{}',".format(self.name)
        code += "\n                  parent='{}',".format(self.parent_for_export.name)
        code += "\n                  maximal_length={},".format(self.max_length)
        code += "\n                  nominal_length={},".format(self.nominal_length)
        code += "\n                  k={},".format(self.k)
        code += "\n                  meshes = [ "

        for m in self._meshes:
            code += '"' + m.name + '",'
        code = code[:-1] + "],"

        code += "\n                  axles = [ "

        for p in self.axles:
            code += f"({p[0]}, {p[1]}, {p[2]}),"

        code = code[:-1] + "])"

        return code


class Circle(NodeWithCoreParent):
    """A Circle models a circle shape based on a diameter and an axis direction"""

    @property
    def axis(self) -> tuple:
        """Direction of the sheave axis (x,y,z) in parent axis system.

        Note:
            The direction of the axis is also used to determine the positive direction over the circumference of the
            circle. This is then used when cables run over the circle or the circle is used for geometric contacts. So
            if a cable runs over the circle in the wrong direction then a solution is to change the axis direction to
            its opposite:  circle.axis =- circle.axis. (another solution in that case is to define the connections of
            the cable in the reverse order)
        """
        return self._vfNode.axis_direction

    @axis.setter
    @node_setter_manageable
    @node_setter_observable
    def axis(self, val):

        assert3f(val)
        if np.linalg.norm(val) == 0:
            raise ValueError("Axis can not be 0,0,0")
        self._vfNode.axis_direction = val

    @property
    def radius(self):
        """Radius of the circle [m]"""
        return self._vfNode.radius

    @radius.setter
    @node_setter_manageable
    @node_setter_observable
    def radius(self, val):

        assert1f(val)
        self._vfNode.radius = val

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\ns.new_circle(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent_for_export.name)
        code += "\n            axis=({}, {}, {}),".format(*self.axis)
        code += "\n            radius={} )".format(self.radius)
        return code

    @property
    def global_position(self):
        """Returns the global position of the center of the sheave.

        Note: this is the same as the global position of the parent point.
        """
        return self.parent.global_position


class HydSpring(NodeWithCoreParent):
    """A HydSpring models a linearized hydrostatic spring.

    The cob (center of buoyancy) is defined in the parent axis system.
    All other properties are defined relative to the cob.

    """

    @property
    def cob(self):
        """Center of buoyancy in parent axis system (m,m,m)"""
        return self._vfNode.position

    @cob.setter
    @node_setter_manageable
    @node_setter_observable
    def cob(self, val):

        assert3f(val)
        self._vfNode.position = val

    @property
    def BMT(self):
        """Vertical distance between cob and metacenter for roll [m]"""
        return self._vfNode.BMT

    @BMT.setter
    @node_setter_manageable
    @node_setter_observable
    def BMT(self, val):

        self._vfNode.BMT = val

    @property
    def BML(self):
        """Vertical distance between cob and metacenter for pitch [m]"""
        return self._vfNode.BML

    @BML.setter
    @node_setter_manageable
    @node_setter_observable
    def BML(self, val):

        self._vfNode.BML = val

    @property
    def COFX(self):
        """Horizontal x-position Center of Floatation (center of waterplane area), relative to cob [m]"""
        return self._vfNode.COFX

    @COFX.setter
    @node_setter_manageable
    @node_setter_observable
    def COFX(self, val):

        self._vfNode.COFX = val

    @property
    def COFY(self):
        """Horizontal y-position Center of Floatation (center of waterplane area), relative to cob [m]"""
        return self._vfNode.COFY

    @COFY.setter
    @node_setter_manageable
    @node_setter_observable
    def COFY(self, val):

        self._vfNode.COFY = val

    @property
    def kHeave(self):
        """Heave stiffness [kN/m]"""
        return self._vfNode.kHeave

    @kHeave.setter
    @node_setter_manageable
    @node_setter_observable
    def kHeave(self, val):

        self._vfNode.kHeave = val

    @property
    def waterline(self):
        """Waterline-elevation relative to cob for un-stretched heave-spring. Positive if cob is below the waterline (which is where is normally is) [m]"""
        return self._vfNode.waterline

    @waterline.setter
    @node_setter_manageable
    @node_setter_observable
    def waterline(self, val):

        self._vfNode.waterline = val

    @property
    def displacement_kN(self):
        """Displacement when waterline is at waterline-elevation [kN]"""
        return self._vfNode.displacement_kN

    @displacement_kN.setter
    @node_setter_manageable
    @node_setter_observable
    def displacement_kN(self, val):

        self._vfNode.displacement_kN = val

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        # new_force(self, name, parent=None, force=None, moment=None):

        code += "\ns.new_hydspring(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent_for_export.name)
        code += "\n            cob=({}, {}, {}),".format(*self.cob)
        code += "\n            BMT={},".format(self.BMT)
        code += "\n            BML={},".format(self.BML)
        code += "\n            COFX={},".format(self.COFX)
        code += "\n            COFY={},".format(self.COFY)
        code += "\n            kHeave={},".format(self.kHeave)
        code += "\n            waterline={},".format(self.waterline)
        code += "\n            displacement_kN={} )".format(self.displacement_kN)

        return code


class LC6d(CoreConnectedNode):
    """A LC6d models a Linear Connector with 6 dofs.

    It connects two Axis elements with six linear springs.

    The first axis system is called "main", the second is called "secondary". The difference is that
    the "main" axis system is used for the definition of the stiffness values.

    The translational-springs are easy. The rotational springs may not be as intuitive. They are defined as:

      - rotation_x = arc-tan ( uy[0] / uy[1] )
      - rotation_y = arc-tan ( -ux[0] / ux[2] )
      - rotation_z = arc-tan ( ux[0] / ux [1] )

    which works fine for small rotations and rotations about only a single axis.

    Tip:
    It is better to use use the "fixed" property of axis systems to create joints.

    """

    def __init__(self, scene, node):
        super().__init__(scene, node)
        self._main = None
        self._secondary = None

    def depends_on(self):
        return [self._main, self._secondary]

    @property
    def stiffness(self):
        """Stiffness of the connector: kx, ky, kz, krx, kry, krz in [kN/m and kNm/rad] (axis system of the main axis)"""
        return self._vfNode.stiffness

    @stiffness.setter
    @node_setter_manageable
    @node_setter_observable
    def stiffness(self, val):

        self._vfNode.stiffness = val

    @property
    def main(self):
        """Main axis system. This axis system dictates the axis system that the stiffness is expressed in"""
        return self._main

    @main.setter
    @node_setter_manageable
    @node_setter_observable
    def main(self, val):

        val = self._scene._node_from_node_or_str(val)
        if not isinstance(val, Frame):
            raise TypeError("Provided nodeA should be a Axis")

        self._main = val
        self._vfNode.master = val._vfNode

    @property
    def secondary(self):
        """Secondary (connected) axis system"""
        return self._secondary

    @secondary.setter
    @node_setter_manageable
    @node_setter_observable
    def secondary(self, val):

        val = self._scene._node_from_node_or_str(val)
        if not isinstance(val, Frame):
            raise TypeError("Provided nodeA should be a Axis")

        self._secondary = val
        self._vfNode.slave = val._vfNode

    @property
    def fgx(self):
        """Force on main in global coordinate frame [kN]"""
        return self._vfNode.global_force[0]

    @property
    def fgy(self):
        """Force on main in global coordinate frame [kN]"""
        return self._vfNode.global_force[1]

    @property
    def fgz(self):
        """Force on main in global coordinate frame [kN]"""
        return self._vfNode.global_force[2]

    @property
    def force_global(self):
        """Force on main in global coordinate frame [kN]"""
        return self._vfNode.global_force

    @property
    def mgx(self):
        """Moment on main in global coordinate frame [kNm]"""
        return self._vfNode.global_moment[0]

    @property
    def mgy(self):
        """Moment on main in global coordinate frame [kNm]"""
        return self._vfNode.global_moment[1]

    @property
    def mgz(self):
        """Moment on main in global coordinate frame [kNm]"""
        return self._vfNode.global_moment[2]

    @property
    def moment_global(self):
        """Moment on main in global coordinate frame [kNm]"""
        return self._vfNode.global_moment

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_linear_connector_6d(name='{}',".format(self.name)
        code += "\n            main='{}',".format(self.main.name)
        code += "\n            secondary='{}',".format(self.secondary.name)
        code += "\n            stiffness=({}, {}, {}, ".format(*self.stiffness[:3])
        code += "\n                       {}, {}, {}) )".format(*self.stiffness[3:])

        return code


class Connector2d(CoreConnectedNode):
    """A Connector2d linear connector with acts both on linear displacement and angular displacement.

    * the linear stiffness is defined by k_linear and is defined over the actual shortest direction between nodeA and nodeB.
    * the angular stiffness is defined by k_angular and is defined over the actual smallest angle between the two systems.
    """

    def __init__(self, scene, node):
        super().__init__(scene, node)
        self._nodeA = None
        self._nodeB = None

    def depends_on(self):
        return [self._nodeA, self._nodeB]

    @property
    def angle(self):
        """Actual angle between nodeA and nodeB [deg] (read-only)"""
        return np.rad2deg(self._vfNode.angle)

    @property
    def force(self):
        """Actual force between nodeA and nodeB [kN] (read-only)"""
        return self._vfNode.force

    @property
    def moment(self):
        """Actual moment between nodeA and nodeB [kNm] (read-only)"""
        return self._vfNode.moment

    @property
    def axis(self):
        """Actual rotation axis between nodeA and nodeB (read-only)"""
        return self._vfNode.axis

    @property
    def ax(self):
        """X component of actual rotation axis between nodeA and nodeB (read-only)"""
        return self._vfNode.axis[0]

    @property
    def ay(self):
        """Y component of actual rotation axis between nodeA and nodeB (read-only)"""
        return self._vfNode.axis[1]

    @property
    def az(self):
        """Z component of actual rotation axis between nodeA and nodeB (read-only)"""
        return self._vfNode.axis[2]

    @property
    def k_linear(self):
        """Linear stiffness [kN/m]"""
        return self._vfNode.k_linear

    @k_linear.setter
    @node_setter_manageable
    @node_setter_observable
    def k_linear(self, value):

        self._vfNode.k_linear = value

    @property
    def k_angular(self):
        """Angular stiffness [kNm/rad]"""
        return self._vfNode.k_angular

    @k_angular.setter
    @node_setter_manageable
    @node_setter_observable
    def k_angular(self, value):

        self._vfNode.k_angular = value

    @property
    def nodeA(self) -> Frame:
        """Connected axis system A"""
        return self._nodeA

    @nodeA.setter
    @node_setter_manageable
    @node_setter_observable
    def nodeA(self, val):

        val = self._scene._node_from_node_or_str(val)
        if not isinstance(val, Frame):
            raise TypeError("Provided nodeA should be a Axis")

        self._nodeA = val
        self._vfNode.master = val._vfNode

    @property
    def nodeB(self) -> Frame:
        """Connected axis system B"""
        return self._nodeB

    @nodeB.setter
    @node_setter_manageable
    @node_setter_observable
    def nodeB(self, val):

        val = self._scene._node_from_node_or_str(val)
        if not isinstance(val, Frame):
            raise TypeError("Provided nodeA should be a Axis")

        self._nodeB = val
        self._vfNode.slave = val._vfNode

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_connector2d(name='{}',".format(self.name)
        code += "\n            nodeA='{}',".format(self.nodeA.name)
        code += "\n            nodeB='{}',".format(self.nodeB.name)
        code += "\n            k_linear ={},".format(self.k_linear)
        code += "\n            k_angular ={})".format(self.k_angular)

        return code


class Beam(CoreConnectedNode):
    """A LinearBeam models a FEM-like linear beam element.

    A LinearBeam node connects two Axis elements

    By definition the beam runs in the X-direction of the nodeA axis system. So it may be needed to create a
    dedicated Axis element for the beam to control the orientation.

    The beam is defined using the following properties:

    *  EIy  - bending stiffness about y-axis
    *  EIz  - bending stiffness about z-axis
    *  GIp  - torsional stiffness about x-axis
    *  EA   - axis stiffness in x-direction
    *  L    - the un-stretched length of the beam
    *  mass - mass of the beam in [mT]

    The beam element is in rest if the nodeB axis system

    1. has the same global orientation as the nodeA system
    2. is at global position equal to the global position of local point (L,0,0) of the nodeA axis. (aka: the end of the beam)

    The scene.new_linearbeam automatically creates a dedicated axis system for each end of the beam. The orientation of this axis-system
    is determined as follows:

    First the direction from nodeA to nodeB is determined: D
    The axis of rotation is the cross-product of the unit x-axis and D    AXIS = ux x D
    The angle of rotation is the angle between the nodeA x-axis and D
    The rotation about the rotated X-axis is undefined.

    """

    def __init__(self, scene, node):
        super().__init__(scene, node)
        self._nodeA = None
        self._nodeB = None

    def depends_on(self):
        return [self._nodeA, self._nodeB]

    @property
    def n_segments(self):
        return self._vfNode.nSegments

    @n_segments.setter
    @node_setter_manageable
    @node_setter_observable
    def n_segments(self, value):
        if value < 1:
            raise ValueError("Number of segments in beam should be 1 or more")
        self._vfNode.nSegments = int(value)

    @property
    def EIy(self):
        """E * Iyy : bending stiffness in the XZ plane [kN m2]

        E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)
        Iyy is the cross section moment of inertia [m4]
        """
        return self._vfNode.EIy

    @EIy.setter
    @node_setter_manageable
    @node_setter_observable
    def EIy(self, value):

        self._vfNode.EIy = value

    @property
    def EIz(self):
        """E * Izz : bending stiffness in the XY plane [kN m2]

        E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)
        Iyy is the cross section moment of inertia [m4]
        """
        return self._vfNode.EIz

    @EIz.setter
    @node_setter_manageable
    @node_setter_observable
    def EIz(self, value):

        self._vfNode.EIz = value

    @property
    def GIp(self):
        """G * Ipp : torsional stiffness about the X (length) axis [kN m2]

        G is the shear-modulus of elasticity; for steel 75-80 GPa (10^6 kN/m2)
        Ip is the cross section polar moment of inertia [m4]
        """
        return self._vfNode.GIp

    @GIp.setter
    @node_setter_manageable
    @node_setter_observable
    def GIp(self, value):

        self._vfNode.GIp = value

    @property
    def EA(self):
        """E * A : stiffness in the length direction [kN]

        E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)
        A is the cross-section area in [m2]
        """
        return self._vfNode.EA

    @EA.setter
    @node_setter_manageable
    @node_setter_observable
    def EA(self, value):

        self._vfNode.EA = value

    @property
    def tension_only(self):
        """axial stiffness (EA) only applicable to tension [True/False]"""
        return self._vfNode.tensionOnly

    @tension_only.setter
    @node_setter_manageable
    @node_setter_observable
    def tension_only(self, value):
        assert isinstance(value, bool), ValueError(
            "Value for tension_only shall be True or False"
        )
        self._vfNode.tensionOnly = value

    @property
    def mass(self):
        """Mass of the beam in [mT]"""
        return self._vfNode.Mass

    @mass.setter
    @node_setter_manageable
    @node_setter_observable
    def mass(self, value):

        assert1f(value, "Mass shall be a number")
        self._vfNode.Mass = value
        pass

    @property
    def L(self):
        """Length of the beam in unloaded condition [m]"""
        return self._vfNode.L

    @L.setter
    @node_setter_manageable
    @node_setter_observable
    def L(self, value):

        self._vfNode.L = value

    @property
    def nodeA(self):
        """The axis system that the A-end of the beam is connected to. The beam leaves this axis system along the X-axis"""
        return self._nodeA

    @nodeA.setter
    @node_setter_manageable
    @node_setter_observable
    def nodeA(self, val):

        val = self._scene._node_from_node_or_str(val)

        if not isinstance(val, Frame):
            raise TypeError("Provided nodeA should be a Axis")

        self._nodeA = val
        self._vfNode.master = val._vfNode

    @property
    def nodeB(self):
        """The axis system that the B-end of the beam is connected to. The beam arrives at this axis system along the X-axis"""
        return self._nodeB

    @nodeB.setter
    @node_setter_manageable
    @node_setter_observable
    def nodeB(self, val):

        val = self._scene._node_from_node_or_str(val)
        if not isinstance(val, Frame):
            raise TypeError("Provided nodeA should be a Axis")

        self._nodeB = val
        self._vfNode.slave = val._vfNode

    # read-only
    @property
    def moment_A(self):
        """Moment on beam at node A (kNm, kNm, kNm) , axis system of node A"""
        return self._vfNode.moment_on_master

    @property
    def moment_B(self):
        """Moment on beam at node B (kNm, kNm, kNm) , axis system of node B"""
        return self._vfNode.moment_on_slave

    @property
    def tension(self):
        """Tension in the beam [kN], negative for compression

        tension is calculated at the midpoints of the beam segments.
        """
        return self._vfNode.tension

    @property
    def torsion(self):
        """Torsion moment [kNm]. Positive if end B has a positive rotation about the x-axis of end A

        torsion is calculated at the midpoints of the beam segments.
        """
        return self._vfNode.torsion

    @property
    def X_nodes(self):
        """Returns the x-positions of the end nodes and internal nodes along the length of the beam [m]"""
        return self._vfNode.x

    @property
    def X_midpoints(self):
        """X-positions of the beam centers measured along the length of the beam [m]"""
        return tuple(
            0.5 * (np.array(self._vfNode.x[:-1]) + np.array(self._vfNode.x[1:]))
        )

    @property
    def global_positions(self):
        """Global-positions of the end nodes and internal nodes [m,m,m]"""
        return np.array(self._vfNode.global_position, dtype=float)

    @property
    def global_orientations(self):
        """Global-orientations of the end nodes and internal nodes [deg,deg,deg]"""
        return np.rad2deg(self._vfNode.global_orientation)

    @property
    def bending(self):
        """Bending forces of the end nodes and internal nodes [0, kNm, kNm]"""
        return np.array(self._vfNode.bending)

    def give_python_code(self):
        code = "# code for beam {}".format(self.name)
        code += "\ns.new_beam(name='{}',".format(self.name)
        code += "\n            nodeA='{}',".format(self.nodeA.name)
        code += "\n            nodeB='{}',".format(self.nodeB.name)
        code += "\n            n_segments={},".format(self.n_segments)
        code += "\n            tension_only={},".format(self.tension_only)
        code += "\n            EIy ={},".format(self.EIy)
        code += "\n            EIz ={},".format(self.EIz)
        code += "\n            GIp ={},".format(self.GIp)
        code += "\n            EA ={},".format(self.EA)
        code += "\n            mass ={},".format(self.mass)
        code += "\n            L ={}) # L can possibly be omitted".format(self.L)

        return code


class TriMeshSource(Node):
    """
    TriMesh

    A TriMesh node contains triangular mesh which can be used for buoyancy or contact

    """

    def __init__(self, scene, source):

        super().__init__(scene)

        # Note: Visual does not have a corresponding vfCore Node in the scene but does have a vfCore
        self._TriMesh = source
        self._new_mesh = True  # cheat for visuals

        self._path = ""  # stores the data that was used to load the obj
        self._offset = (0, 0, 0)
        self._scale = (1, 1, 1)
        self._rotation = (0, 0, 0)

        self._invert_normals = False

        self.boundary_edges = []
        self.non_manifold_edges = []

    def depends_on(self) -> list:
        return []

    def AddVertex(self, x, y, z):
        """Adds a vertex (point)"""
        self._TriMesh.AddVertex(x, y, z)

    def AddFace(self, i, j, k):
        """Adds a triangular face between vertex numbers i,j and k"""
        self._TriMesh.AddFace(i, j, k)

    def get_extends(self):
        """Returns the extends of the mesh in global coordinates

        Returns: (minimum_x, maximum_x, minimum_y, maximum_y, minimum_z, maximum_z)

        """

        t = self._TriMesh

        if t.nFaces == 0:
            return (0, 0, 0, 0, 0, 0)

        v = t.GetVertex(0)
        xn = v[0]
        xp = v[0]
        yn = v[1]
        yp = v[1]
        zn = v[2]
        zp = v[2]

        for i in range(t.nVertices):
            v = t.GetVertex(i)
            x = v[0]
            y = v[1]
            z = v[2]

            if x < xn:
                xn = x
            if x > xp:
                xp = x
            if y < yn:
                yn = y
            if y > yp:
                yp = y
            if z < zn:
                zn = z
            if z > zp:
                zp = z

        return (xn, xp, yn, yp, zn, zp)

    def _fromVTKpolydata(
        self, polydata, offset=None, rotation=None, scale=None, invert_normals=False
    ):

        import vtk

        tri = vtk.vtkTriangleFilter()

        tri.SetInputConnection(polydata)

        scaleFilter = vtk.vtkTransformPolyDataFilter()
        rotationFilter = vtk.vtkTransformPolyDataFilter()

        s = vtk.vtkTransform()
        s.Identity()
        r = vtk.vtkTransform()
        r.Identity()

        rotationFilter.SetInputConnection(tri.GetOutputPort())
        scaleFilter.SetInputConnection(rotationFilter.GetOutputPort())

        if scale is not None:
            s.Scale(*scale)

        if rotation is not None:
            q = rotation
            angle = (q[0] ** 2 + q[1] ** 2 + q[2] ** 2) ** (0.5)
            if angle > 0:
                r.RotateWXYZ(angle, q[0] / angle, q[1] / angle, q[2] / angle)

        if offset is None:
            offset = [0, 0, 0]

        scaleFilter.SetTransform(s)
        rotationFilter.SetTransform(r)

        clean = vtk.vtkCleanPolyData()
        clean.SetInputConnection(scaleFilter.GetOutputPort())

        clean.ConvertLinesToPointsOff()
        clean.ConvertPolysToLinesOff()
        clean.ConvertStripsToPolysOff()
        clean.PointMergingOn()
        clean.ToleranceIsAbsoluteOn()
        clean.SetAbsoluteTolerance(0.001)

        clean.Update()
        data = clean.GetOutput()

        self._TriMesh.Clear()

        for i in range(data.GetNumberOfPoints()):
            point = data.GetPoint(i)
            self._TriMesh.AddVertex(
                point[0] + offset[0], point[1] + offset[1], point[2] + offset[2]
            )

        for i in range(data.GetNumberOfCells()):
            cell = data.GetCell(i)

            if isinstance(cell, vtk.vtkLine):
                print("Cell nr {} is a line, not adding to mesh".format(i))
                continue

            if isinstance(cell, vtk.vtkVertex):
                print("Cell nr {} is a vertex, not adding to mesh".format(i))
                continue

            id0 = cell.GetPointId(0)
            id1 = cell.GetPointId(1)
            id2 = cell.GetPointId(2)

            if invert_normals:
                self._TriMesh.AddFace(id2, id1, id0)
            else:
                self._TriMesh.AddFace(id0, id1, id2)

        # check if anything was loaded
        if self._TriMesh.nFaces == 0:
            raise Exception(
                "No faces in poly-data - no geometry added (hint: empty obj file?)"
            )
        self._new_mesh = True
        self._scene.update()

    def check_shape(self):
        """Performs some checks on the shape in the trimesh
        - Boundary edges (edge with only one face attached)
        - Non-manifold edges (edit with more than two faces attached)
        - Volume should be positive
        """

        tm = self._TriMesh

        if tm.nFaces == 0:
            return ["No mesh"]

        # # make sure the mesh is clean: vertices should be unique
        # vertices = []
        # for i in range(tm.nVertices):
        #     vertex = np.array(tm.GetVertex(i))
        #     for v in vertices:
        #         if np.linalg.norm(vertex-v) < 0.001:
        #             print("Duplicate vertex" + str(vertex-v))
        #     else:
        #         vertices.append(vertex)

        # Make a list of all boundaries using their vertex IDs
        boundaries = np.zeros((3 * tm.nFaces, 2), dtype=int)
        for i in range(tm.nFaces):
            face = tm.GetFace(i)
            boundaries[3 * i] = [face[0], face[1]]
            boundaries[3 * i + 1] = [face[1], face[2]]
            boundaries[3 * i + 2] = [face[2], face[0]]

        # For an edge is doesn't matter in which direction it runs
        boundaries.sort(axis=1)

        # every boundary should be present twice

        values, rows_occurance_count = np.unique(
            boundaries, axis=0, return_counts=True
        )  # count of rows

        n_boundary = np.count_nonzero(rows_occurance_count == 1)
        n_nonmanifold = np.count_nonzero(rows_occurance_count > 2)

        messages = []

        boundary_edges = []
        non_manifold_edges = []

        if n_boundary > 0:
            messages.append(f"Mesh contains {n_boundary} boundary edges")

            i_boundary = np.argwhere(rows_occurance_count == 1)
            for i in i_boundary:
                edge = values[i][0]
                v1 = tm.GetVertex(edge[0])
                v2 = tm.GetVertex(edge[1])
                boundary_edges.append((v1, v2))

        if n_nonmanifold > 0:
            messages.append(f"Mesh contains {n_nonmanifold} non-manifold edges")
            i_boundary = np.argwhere(rows_occurance_count > 2)
            for i in i_boundary:
                edge = values[i][0]
                v1 = tm.GetVertex(edge[0])
                v2 = tm.GetVertex(edge[1])
                non_manifold_edges.append((v1, v2))

        if len(messages) == 2:
            messages.append("Boundary edges are shown in Red")
            messages.append("Non-manifold edges are shown in Pink")

        # Do not check for volume if we have nonmanifold geometry or boundary edges
        try:
            volume = tm.Volume()
        except:
            volume = 1  # no available in every pyo3d yet

        if volume < 0:
            messages.append(
                f"Total mesh volume is negative ({volume:.2f} m3 of enclosed volume)."
            )
            messages.append("Hint: Use invert-normals")

        self.boundary_edges = boundary_edges
        self.non_manifold_edges = non_manifold_edges

        return messages

    def load_vtk_polydataSource(self, polydata):
        """Fills the triangle data from a vtk polydata such as a cubeSource.

        The vtk TriangleFilter is used to triangulate the source

        Examples:
            cube = vtk.vtkCubeSource()
            cube.SetXLength(122)
            cube.SetYLength(38)
            cube.SetZLength(10)
            trimesh.load_vtk_polydataSource(cube)
        """

        self._fromVTKpolydata(polydata.GetOutputPort())

    def load_obj(
        self, filename, offset=None, rotation=None, scale=None, invert_normals=False
    ):
        self.load_file(filename, offset, rotation, scale, invert_normals)

    def load_file(
        self, url, offset=None, rotation=None, scale=None, invert_normals=False
    ):
        """Loads an .obj or .stl file and and triangulates it.

        Order of modifications:

        1. rotate
        2. scale
        3. offset

        Args:
            url: (str or path or resource): file to load
            offset: : offset
            rotation:  : rotation
            scale:  scale

        """

        self._path = str(url)

        filename = str(self._scene.get_resource_path(url))

        import vtk

        ext = filename.lower()[-3:]
        if ext == "obj":
            obj = vtk.vtkOBJReader()
            obj.SetFileName(filename)
        elif ext == "stl":
            obj = vtk.vtkSTLReader()
            obj.SetFileName(filename)
        else:
            raise ValueError(
                f"File should be an .obj or .stl file but has extension {ext}"
            )

        # Add cleaning
        cln = vtk.vtkCleanPolyData()
        cln.SetInputConnection(obj.GetOutputPort())

        self._fromVTKpolydata(
            cln.GetOutputPort(),
            offset=offset,
            rotation=rotation,
            scale=scale,
            invert_normals=invert_normals,
        )

        self._scale = scale
        self._offset = offset
        self._rotation = rotation

        if self._scale is None:
            self._scale = (1.0, 1.0, 1.0)
        if self._offset is None:
            self._offset = (0.0, 0.0, 0.0)
        if self._rotation is None:
            self._rotation = (0.0, 0.0, 0.0)
        self._invert_normals = invert_normals

    def _load_from_privates(self):
        """(Re)Loads the mesh using the values currently stored in _scale, _offset, _rotation and _invert_normals"""
        self.load_file(
            url=self._path,
            scale=self._scale,
            offset=self._offset,
            rotation=self._rotation,
            invert_normals=self._invert_normals,
        )

    def give_python_code(self):
        code = "# No code generated for TriMeshSource"
        return code

    # def change_parent_to(self, new_parent):
    #
    #     if not (isinstance(new_parent, Axis) or new_parent is None):
    #         raise ValueError('Visuals can only be attached to an axis (or derived) or None')
    #
    #     # get current position and orientation
    #     if self.parent is not None:
    #         cur_position = self.parent.to_glob_position(self.offset)
    #         cur_rotation = self.parent.to_glob_direction(self.rotation)
    #     else:
    #         cur_position = self.offset
    #         cur_rotation = self.rotation
    #
    #     self.parent = new_parent
    #
    #     if new_parent is None:
    #         self.offset = cur_position
    #         self.rotation = cur_rotation
    #     else:
    #         self.offset = new_parent.to_loc_position(cur_position)
    #         self.rotation = new_parent.to_loc_direction(cur_rotation)


class Buoyancy(NodeWithCoreParent):
    """Buoyancy provides a buoyancy force based on a buoyancy mesh. The mesh is triangulated and chopped at the instantaneous flat water surface. Buoyancy is applied as an upwards force that the center of buoyancy.
    The calculation of buoyancy is as accurate as the provided geometry.

    There as no restrictions to the size or aspect ratio of the panels. It is excellent to model as box using 6 faces. Using smaller panels has a negative effect on performance.

    The normals of the panels should point towards to water.
    """

    # init parent and name are fully derived from NodeWithParent
    # _vfNode is a buoyancy
    def __init__(self, scene, vfBuoyancy):
        super().__init__(scene, vfBuoyancy)
        self._None_parent_acceptable = False
        self._trimesh = TriMeshSource(
            self._scene, self._vfNode.trimesh
        )  # the tri-mesh is wrapped in a custom object

    def update(self):
        self._vfNode.reloadTrimesh()

    @property
    def trimesh(self) -> TriMeshSource:
        return self._trimesh

    @property
    def cob(self):
        """GLOBAL position of the center of buoyancy [m,m,m] (global axis)"""
        return self._vfNode.cob

    @property
    def cob_local(self):
        """Position of the center of buoyancy [m,m,m] (local axis)"""

        return self.parent.to_loc_position(self.cob)

    @property
    def displacement(self):
        """Displaced volume of fluid [m^3]"""
        return self._vfNode.displacement

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\nmesh = s.new_buoyancy(name='{}',".format(self.name)

        code += "\n          parent='{}')".format(self.parent_for_export.name)

        if self.trimesh._invert_normals:
            code += "\nmesh.trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}), invert_normals=True)".format(
                self.trimesh._path,
                *self.trimesh._scale,
                *self.trimesh._rotation,
                *self.trimesh._offset,
            )
        else:
            code += "\nmesh.trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}))".format(
                self.trimesh._path,
                *self.trimesh._scale,
                *self.trimesh._rotation,
                *self.trimesh._offset,
            )

        return code


class Tank(NodeWithCoreParent):
    """Tank provides a fillable tank based on a mesh. The mesh is triangulated and chopped at the instantaneous flat fluid surface. Gravity is applied as an downwards force that the center of fluid.
    The calculation of fluid volume and center is as accurate as the provided geometry.

    There as no restrictions to the size or aspect ratio of the panels. It is excellent to model as box using 6 faces. Using smaller panels has a negative effect on performance.

    The normals of the panels should point *away* from the fluid. This means that the same basic shapes can be used for both buoyancy and tanks.
    """

    # init parent and name are fully derived from NodeWithParent
    # _vfNode is a tank
    def __init__(self, scene, vfTank):
        super().__init__(scene, vfTank)
        self._None_parent_acceptable = False
        self._trimesh = TriMeshSource(
            self._scene, self._vfNode.trimesh
        )  # the tri-mesh is wrapped in a custom object

        self._inertia = scene._vfc.new_pointmass(
            self.name + vfc.VF_NAME_SPLIT + "inertia"
        )

    def update(self):
        self._vfNode.reloadTrimesh()

        # update inertia
        self._inertia.parent = self.parent._vfNode
        self._inertia.position = self.cog_local
        self._inertia.inertia = self.volume * self.density

    def _delete_vfc(self):
        self._scene._vfc.delete(self._inertia.name)
        super()._delete_vfc()

    @property
    def trimesh(self) -> TriMeshSource:
        return self._trimesh

    @property
    def free_flooding(self):
        return self._vfNode.free_flooding

    @free_flooding.setter
    def free_flooding(self, value):
        assert isinstance(value, bool), ValueError(
            f"free_flooding shall be a bool, you passed a {type(value)}"
        )
        self._vfNode.free_flooding = value

    @property
    def permeability(self):
        """Permeability is the fraction of the enclosed volume that can be filled with fluid [-]"""
        return self._vfNode.permeability

    @permeability.setter
    def permeability(self, value):
        assert1f_positive_or_zero(value)
        self._vfNode.permeability = value

    @property
    def cog(self):
        """Returns the GLOBAL position of the center of volume / gravity"""
        return self._vfNode.cog

    @property
    def cog_local(self):
        """Returns the local position of the center of gravity"""
        return self.parent.to_loc_position(self.cog)

    @property
    def cog_when_full(self):
        """Returns the LOCAL position of the center of volume / gravity of the tank when it is filled"""
        return self._vfNode.cog_when_full

    @property
    def fill_pct(self):
        """Amount of volume in tank as percentage of capacity [%]"""
        if self.capacity == 0:
            return 0
        return 100 * self.volume / self.capacity

    @fill_pct.setter
    @node_setter_observable
    def fill_pct(self, value):

        if value < 0 and value > -0.01:
            value = 0

        assert1f_positive_or_zero(value)

        if value > 100.1:
            raise ValueError(
                f"Fill percentage should be between 0 and 100 [%], {value} is not valid"
            )
        if value > 100:
            value = 100
        self.volume = value * self.capacity / 100

    @property
    def level_global(self):
        """The fluid plane elevation in the global axis system. Setting this adjusts the volume"""
        return self._vfNode.fluid_level_global

    @level_global.setter
    @node_setter_manageable
    @node_setter_observable
    def level_global(self, value):
        assert1f(value)
        self._vfNode.fluid_level_global = value

    @property
    def volume(self):
        """The actual volume of fluid in the tank in m3. Setting this adjusts the fluid level"""
        return self._vfNode.volume

    @volume.setter
    @node_setter_observable
    def volume(self, value):
        assert1f_positive_or_zero(value, "Volume")
        self._vfNode.volume = value

    @property
    def density(self):
        """Density of the fluid in the tank in mT/m3"""
        return self._vfNode.density

    @density.setter
    @node_setter_manageable
    @node_setter_observable
    def density(self, value):
        assert1f(value)
        self._vfNode.density = value

    @property
    def capacity(self):
        """Returns the capacity of the tank in m3. This is calculated from the defined geometry and permeability."""
        return self._vfNode.capacity

    @property
    def ullage(self):
        """Ullage of the tank [m].
        The ullage is the distance between a measurement point and the fluid surface. The point is [xf,yf,zv] where
        xf and yf are the x and y coordinates (local) of the center of fluid when the tank is full. zv is the largest z value
        of all the vertices of the tank.
        The measurement direction is in local z-direction. If the tank is under an angle then this is not perpendicular to the fluid.
        It is possible that this definition returns an ullage larger than the physical tank depth. In that case the physical depth of
        the tank is returned instead.
        """
        return self._vfNode.ullage

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\nmesh = s.new_tank(name='{}',".format(self.name)

        if self.density != 1.025:
            code += f"\n          density={self.density},"

        if self.free_flooding:
            code += f"\n          free_flooding=True,"

        code += "\n          parent='{}')".format(self.parent_for_export.name)

        if self.trimesh._invert_normals:
            code += "\nmesh.trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}), invert_normals=True)".format(
                self.trimesh._path,
                *self.trimesh._scale,
                *self.trimesh._rotation,
                *self.trimesh._offset,
            )
        else:
            code += "\nmesh.trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}))".format(
                self.trimesh._path,
                *self.trimesh._scale,
                *self.trimesh._rotation,
                *self.trimesh._offset,
            )
        code += f"\ns['{self.name}'].volume = {self.volume}   # first load mesh, then set volume"

        return code


class BallastSystem(Node):
    """The BallastSystemNode is a non-physical node that marks a groups of Tank nodes as being the ballast system
    of a vessel.

    The BallastSystem node can interface with the ballast-solver to automatically determine a suitable ballast configuration.

    The tank objects are created separately and only their references are assigned to this ballast-system object.
    That is done using the .tanks property which is a list.
    The parent if this node is the vessel that the tanks belong to. The parent of the ballast system is expected to be
    a Frame or Rigidbody which can be ballasted (should not have a parent).

    Tanks can be excluded from the ballast algorithms by adding their names to the 'frozen' list.

    Typical use:
    - create vessel
    - create tanks
    - create ballast system
    - adds tanks to ballast system using ballast_system.tanks.append(tank node)
    - set the draft: ballast_system.target_elevation = -5.0 # note, typically negative
    - and solve the tank fills: ballast_system.solve_ballast


    """

    def __init__(self, scene, parent):
        super().__init__(scene)

        self.tanks = []
        """List of Tank objects"""

        self.frozen = []
        """List of names of frozen tanks - The contents of a frozen tank should not be changed"""

        self.parent = parent

        self._target_elevation = None
        """Target elevation of the parent Frame (global, m)"""
        self._target_cog = None
        """Required cog of all the ballast tanks to reach the target z, calculated when setting target_elevation"""
        self._target_weight = None
        """Required total amount of water ballast to reach the target z, calculated when setting target_elevation"""

    @property
    def target_elevation(self):
        """The target elevation of the parent of the ballast system."""
        return self._target_elevation

    @target_elevation.setter
    def target_elevation(self, value):

        assert1f(value, "target elevation")

        # empty all connected tanks
        fills = [tank.fill_pct for tank in self.tanks]
        for tank in self.tanks:
            tank.fill_pct = 0

        try:

            from DAVE.solvers.ballast import force_vessel_to_evenkeel_and_draft

            (F, x, y) = force_vessel_to_evenkeel_and_draft(
                self._scene, self.parent, value
            )
            self._target_elevation = value
            self._target_cog = (x, y)
            self._target_weight = -F

        finally:  # restore all connected tanks
            for tank, fill in zip(self.tanks, fills):
                tank.fill_pct = fill

    def solve_ballast(self, method=1, use_current_fill=False):
        """Attempts to find a suitable filling of the ballast tanks to position parent at even-keel and target-elevation

        Args:
            method: algorithm to use (named 1 and 2)
            use_current_fill: use current tank fill as start for the algorithm

        See Also: target_elevation"""

        if self._target_weight is None:
            raise ValueError(
                "Please set target_elevation first (eg: target_elevation = -5)"
            )

        from DAVE.solvers.ballast import BallastSystemSolver

        ballast_solver = BallastSystemSolver(self)

        assert method == 1 or method == 2, "Method shall be 1 or 2"

        ballast_solver.ballast_to(
            self._target_cog[0],
            self._target_cog[1],
            self._target_weight,
            start_empty=not use_current_fill,
            method=method,
        )

    def new_tank(
        self, name, position, capacity_kN, rho=1.025, frozen=False, actual_fill=0
    ):
        """Adds a new cubic shaped tank with the given volume as derived from capacity and rho

        Warning: provided for backwards compatibility only.
        """

        from warnings import warn

        warn(
            "BallastSystem.new_tank is outdated and may be removed in a future version."
        )

        tnk = self._scene.new_tank(name, parent=self.parent, density=rho)
        volume = capacity_kN / (9.81 * rho)
        side = volume ** (1 / 3)
        tnk.trimesh.load_file(
            "res: cube.obj",
            scale=(side, side, side),
            rotation=(0.0, 0.0, 0.0),
            offset=position,
        )
        if actual_fill > 0:
            tnk.fill_pct = actual_fill

        if frozen:
            tnk.frozen = frozen

        self.tanks.append(tnk)

        return tnk

    # for gui
    def change_parent_to(self, new_parent):
        if not (isinstance(new_parent, Frame) or new_parent is None):
            raise ValueError(
                "Visuals can only be attached to an axis (or derived) or None"
            )
        self.parent = new_parent

    # for node
    def depends_on(self):
        return [self.parent, *self.tanks]

    def is_frozen(self, name):
        """Returns True if the tank with this name if frozen"""
        return name in self.frozen

    def reorder_tanks(self, names):
        """Places tanks with given names at the top of the list. Other tanks are appended afterwards in original order.

        For a complete re-order give all tank names.

        Example:
            let tanks be 'a','b','c','d','e'

            then re_order_tanks(['e','b']) will result in ['e','b','a','c','d']
        """
        for name in names:
            if name not in self.tank_names():
                raise ValueError("No tank with name {}".format(name))

        old_tanks = self.tanks.copy()
        self.tanks.clear()
        to_be_deleted = list()

        for name in names:
            for tank in old_tanks:
                if tank.name == name:
                    self.tanks.append(tank)
                    to_be_deleted.append(tank)

        for tank in to_be_deleted:
            old_tanks.remove(tank)

        for tank in old_tanks:
            self.tanks.append(tank)

    def order_tanks_by_elevation(self):
        """Re-orders the existing tanks such that the lowest tanks are higher in the list"""

        zs = [tank.cog_when_full[2] for tank in self.tanks]
        inds = np.argsort(zs)
        self.tanks = [self.tanks[i] for i in inds]

    def order_tanks_by_distance_from_point(self, point, reverse=False):
        """Re-orders the existing tanks such that the tanks *furthest* from the point are first on the list

        Args:
            point : (x,y,z)  - reference point to determine the distance to
            reverse: (False) - order in reverse order: tanks nearest to the points first on list


        """
        pos = [tank.cog_when_full for tank in self.tanks]
        pos = np.array(pos, dtype=float)
        pos -= np.array(point)

        dist = np.apply_along_axis(np.linalg.norm, 1, pos)

        if reverse:
            inds = np.argsort(dist)
        else:
            inds = np.argsort(-dist)

        self.tanks = [self.tanks[i] for i in inds]

    def order_tanks_to_maximize_inertia_moment(self):
        """Re-order tanks such that tanks furthest from center of system are first on the list"""
        self._order_tanks_to_inertia_moment()

    def order_tanks_to_minimize_inertia_moment(self):
        """Re-order tanks such that tanks nearest to center of system are first on the list"""
        self._order_tanks_to_inertia_moment(maximize=False)

    def _order_tanks_to_inertia_moment(self, maximize=True):
        """Re-order tanks such that tanks furthest away from center of system are first on the list"""
        pos = [tank.cog_when_full for tank in self.tanks]
        m = [tank.capacity for tank in self.tanks]
        pos = np.array(pos, dtype=float)
        mxmymz = np.vstack((m, m, m)).transpose() * pos
        total = np.sum(m)
        point = sum(mxmymz) / total

        if maximize:
            self.order_tanks_by_distance_from_point(point)
        else:
            self.order_tanks_by_distance_from_point(point, reverse=True)

    def tank_names(self):
        return [tank.name for tank in self.tanks]

    def fill_tank(self, name, fill):

        assert1f(fill, "tank fill")

        for tank in self.tanks:
            if tank.name == name:
                tank.pct = fill
                return
        raise ValueError("No tank with name {}".format(name))

    def xyzw(self):
        """Gets the current ballast cog in GLOBAL axis system weight from the tanks

        Returns:
            (x,y,z), weight [mT]
        """
        """Calculates the weight and inertia properties of the tanks"""

        mxmymz = np.array((0.0, 0.0, 0.0))
        wt = 0

        for tank in self.tanks:
            w = tank.volume * tank.density
            p = np.array(tank.cog, dtype=float)
            mxmymz += p * w

            wt += w

        if wt == 0:
            xyz = np.array((0.0, 0.0, 0.0))
        else:
            xyz = mxmymz / wt

        return xyz, wt

    def empty_all_usable_tanks(self):
        """Empties all non-frozen tanks.
        Returns a list with tank number and fill percentage of all affected tanks. This can be used to restore the
        ballast situation as it was before emptying.

        See also: restore tank fillings
        """
        restore = []

        for i, t in enumerate(self.tanks):
            if not self.is_frozen(t.name):
                restore.append((i, t.fill_pct))
                t.fill_pct = 0

        return restore

    def restore_tank_fillings(self, restore):
        """Restores the tank fillings as per restore.

        Restore is typically obtained from the "empty_all_usable_tanks" function.

        See Also: empty_all_usable_tanks
        """

        for r in restore:
            i, pct = r
            self.tanks[i].fill_pct = pct

    def tank(self, name):

        for t in self.tanks:
            if t.name == name:
                return t
        raise ValueError("No tank with name {}".format(name))

    def __getitem__(self, item):
        return self.tank(item)

    @property
    def cogx(self):
        """X position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]"""
        return self.cog[0]

    @property
    def cogy(self):
        """Y position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]"""
        return self.cog[1]

    @property
    def cogz(self):
        """Z position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]"""
        return self.cog[2]

    @property
    def cog(self):
        """Combined CoG of all tank contents in the ballast-system. (global coordinate) [m,m,m]"""
        cog, wt = self.xyzw()
        return (cog[0], cog[1], cog[2])

    @property
    def weight(self):
        """Total weight of all tank fillings in the ballast system [kN]"""
        cog, wt = self.xyzw()
        return wt * 9.81

    def give_python_code(self):
        code = "\n# code for {} and its tanks".format(self.name)

        code += "\nbs = s.new_ballastsystem('{}', parent = '{}')".format(
            self.name, self.parent.name
        )

        for tank in self.tanks:
            code += "\nbs.tanks.append(s['{}'])".format(tank.name)

        return code


class WaveInteraction1(Node):
    """
    WaveInteraction

    Wave-interaction-1 couples a first-order hydrodynamic database to an axis.

    This adds:
    - wave-forces
    - damping
    - added mass

    The data is provided by a Hyddb1 object which is defined in the MaFreDo package. The contents are not embedded
    but are to be provided separately in a file. This node contains only the file-name.

    """

    def __init__(self, scene):

        super().__init__(scene)

        self.offset = [0, 0, 0]
        """Position (x,y,z) of the hydrodynamic origin in its parents axis system"""

        self.parent = None
        """Parent : Axis-type"""

        self.path = None
        """Filename of a file that can be read by a Hyddb1 object"""

    @property
    def file_path(self):
        return self._scene.get_resource_path(self.path)

    def depends_on(self):
        return [self.parent]

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_waveinteraction(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent.name)
        code += "\n            path=r'{}',".format(self.path)
        code += "\n            offset=({}, {}, {}) )".format(*self.offset)

        return code

    def change_parent_to(self, new_parent):

        if not (isinstance(new_parent, Frame)):
            raise ValueError(
                "Hydrodynamic databases can only be attached to an axis (or derived)"
            )

        # get current position and orientation
        if self.parent is not None:
            cur_position = self.parent.to_glob_position(self.offset)
        else:
            cur_position = self.offset

        self.parent = new_parent
        self.offset = new_parent.to_loc_position(cur_position)


# ============== Managed nodes


class Manager(Node, ABC):
    """
    Notes:
        1. A manager shall manage the names of all nodes it creates
    """


    @abstractmethod
    def delete(self):
        """Carefully remove the manager, reinstate situation as before.
        - Delete all the nodes it created.
        - Release management on all other nodes
        - Do not delete the manager itself
        """
        pass

    @abstractmethod
    def creates(self, node: Node):
        """Returns True if node is created by this manager"""
        pass

    @property
    @abstractmethod
    def name(self):
        """Name of the node (str), must be unique"""
        # Example:
        #     @property
        #     def name(self):
        #         """Name of the node (str), must be unique"""
        #         return RigidBody.name.fget(self)
        #

        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        # example
        # @name.setter
        # def name(self, value):
        #     old_name = self.name
        #     RigidBody.name.fset(self,value)
        #     self._rename_all_manged_nodes(old_name, value)
        #
        pass

    def _rename_all_manged_nodes(self, old_name, new_name):
        """Helper to quickly rename all managed nodes"""
        with ClaimManagement(self._scene, self):
            for node in self.managed_nodes():
                node.name = node.name.replace(old_name, new_name)



class GeometricContact(Manager):
    """
    GeometricContact

    A GeometricContact can be used to construct geometric connections between circular members:
        - 	steel bars and holes, such as a shackle pin in a padeye (pin-hole)
        -	steel bars and steel bars, such as a shackle-shackle connection


    Situation before creation of geometric contact:

    Axis1
        Point1
            Circle1
    Axis2
        Point2
            Circle2

    Create a geometric contact with Circle1 and parent and Circle2 as child

    Axis1
        Point1              : observed, referenced as parent_circle_parent
            Circle1         : observed, referenced as parent_circle

        _axis_on_parent                 : managed
            _pin_hole_connection        : managed
                _connection_axial_rotation : managed
                    _axis_on_child      : managed
                        Axis2           : managed    , referenced as child_circle_parent_parent
                            Point2      : observed   , referenced as child_circle_parent
                                Circle2 : observed   , referenced as child_circle







    """

    def __init__(self, scene, child_circle, parent_circle, name, inside=True):
        """
        circle1 becomes the nodeB
        circle2 becomes the nodeA

        (attach circle 1 to circle 2)
        Args:
            scene:
            vfAxis:
            parent_circle:
            child_circle:
        """

        if parent_circle.parent.parent is None:
            raise ValueError(
                "The slaved pin is not located on an axis. Can not create the connection because there is no axis to nodeB"
            )

        super().__init__(scene)


        name_prefix = self.name + vfc.MANAGED_NODE_IDENTIFIER

        self._parent_circle = parent_circle
        self._parent_circle_parent = parent_circle.parent  # point

        self._child_circle = child_circle
        self._child_circle_parent = child_circle.parent  # point
        self._child_circle_parent_parent = child_circle.parent.parent  # axis

        self._flipped = False
        self._inside_connection = inside

        self._axis_on_parent = self._scene.new_frame(
            scene.available_name_like(name_prefix + "_axis_on_parent")
        )
        """Axis on the nodeA axis at the location of the center of hole or pin"""

        self._pin_hole_connection = self._scene.new_frame(
            scene.available_name_like(name_prefix + "_pin_hole_connection")
        )
        """axis between the center of the hole and the center of the pin. Free to rotate about the center of the hole as well as the pin"""

        self._axis_on_child = self._scene.new_frame(
            scene.available_name_like(name_prefix + "_axis_on_child")
        )
        """axis to which the slaved body is connected. Either the center of the hole or the center of the pin """

        self._connection_axial_rotation = self._scene.new_frame(
            scene.available_name_like(name_prefix + "_connection_axial_rotation")
        )

        # prohibit changes to nodes that were used in the creation of this connection
        for node in self.managed_nodes():
            node.manager = self

        # observe circles and their points
        self._parent_circle.observers.append(self)
        self._parent_circle_parent.observers.append(self)

        self._child_circle.observers.append(self)
        self._child_circle_parent.observers.append(self)

        self._child_circle_parent_parent._parent_for_code_export = None

        self.name = name

        self._update_connection()

    def on_observed_node_changed(self, changed_node):
        self._update_connection()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert self._scene.name_available(value), f"Name {value} already in use"

        self._rename_all_manged_nodes(self.name, value)
        self._name = value

    @staticmethod
    def _assert_parent_child_possible(parent, child):
        if parent.parent.parent == child.parent.parent:
            raise ValueError(
                f"A GeometricContact can not be created between two circles on the same axis or body. Both circles are located on {parent.parent.parent}"
            )

    @property
    def child(self):
        """The Circle that is connected to the GeometricContact [Node]

        See Also: parent
        """
        return self._child_circle

    @child.setter
    def child(self, value):
        new_child = self._scene._node_from_node_or_str(value)
        if not isinstance(new_child, Circle):
            raise ValueError(
                f"Child of a geometric contact should be a Circle, but {new_child.name} is a {type(new_child)}"
            )

        if new_child.parent.parent is None:
            raise ValueError(
                f"Child circle {new_child.name} is not located on an axis or body and can thus not be used as child"
            )

        self._assert_parent_child_possible(self.parent, new_child)

        store = self._scene.current_manager
        self._scene.current_manager = self

        # release old child
        self._child_circle.observers.remove(self)
        self._child_circle_parent.observers.remove(self)

        # release the slaved axis system
        self._child_circle_parent_parent._parent_for_code_export = True
        self._child_circle_parent_parent.manager = None

        # set new parent
        self._child_circle = new_child
        self._child_circle_parent = new_child.parent
        self._child_circle_parent_parent = new_child.parent.parent

        # and observe
        self._child_circle.observers.append(self)
        self._child_circle_parent.observers.append(self)

        # and manage
        self._child_circle_parent_parent._parent_for_code_export = None
        self._child_circle_parent_parent.manager = self

        self._scene.current_manager = store

        self._update_connection()

    @property
    def parent(self):
        """The Circle that the GeometricConnection is connected to [Node]

        See Also: child
        """
        return self._parent_circle

    @parent.setter
    @node_setter_manageable
    @node_setter_observable
    def parent(self, var):
        if var is None:
            raise ValueError(
                "Parent of a geometric contact should be a Circle, not None"
            )

        new_parent = self._scene._node_from_node_or_str(var)
        if not isinstance(new_parent, Circle):
            raise ValueError(
                f"Parent of a geometric contact should be a Circle, but {new_parent.name} is a {type(new_parent)}"
            )

        self._assert_parent_child_possible(new_parent, self.child)

        # release old parent
        self._parent_circle.observers.remove(self)
        self._parent_circle_parent.observers.remove(self)

        # set new parent
        self._parent_circle = new_parent
        self._parent_circle_parent = new_parent.parent

        # and observe
        self._parent_circle.observers.append(self)
        self._parent_circle_parent.observers.append(self)

        self._update_connection()

    def change_parent_to(self, new_parent):
        self.parent = new_parent

    def delete(self):

        # release management
        for node in self.managed_nodes():
            node._manager = None

        self._child_circle_parent_parent.change_parent_to(None)

        self._scene.delete(self._axis_on_child)
        self._scene.delete(self._pin_hole_connection)
        self._scene.delete(self._axis_on_parent)

        # release observers
        self._parent_circle.observers.remove(self)
        self._parent_circle_parent.observers.remove(self)

        self._child_circle.observers.remove(self)
        self._child_circle_parent.observers.remove(self)

    def _update_connection(self):

        remember = self._scene.current_manager
        self._scene.current_manager = self  # claim management

        # get current properties

        c_swivel = self.swivel
        c_swivel_fixed = self.swivel_fixed
        c_rotation_on_parent = self.rotation_on_parent
        c_fixed_to_parent = self.fixed_to_parent
        c_child_rotation = self.child_rotation
        c_child_fixed = self.child_fixed

        pin1 = self._child_circle  # nodeB
        pin2 = self._parent_circle  # nodeA

        if pin1.parent.parent is None:
            raise ValueError(
                "The slaved pin is not located on an axis. Can not create the connection because there is no axis to nodeB"
            )

        # --------- prepare hole

        if pin2.parent.parent is not None:
            self._axis_on_parent.parent = pin2.parent.parent
        self._axis_on_parent.position = pin2.parent.position
        self._axis_on_parent.fixed = (True, True, True, True, True, True)

        self._axis_on_parent.rotation = rotation_from_y_axis_direction(pin2.axis)

        # Position connection axis at the center of the nodeA axis (pin2)
        # and allow it to rotate about the pin
        self._pin_hole_connection.position = (0, 0, 0)
        self._pin_hole_connection.parent = self._axis_on_parent
        self._pin_hole_connection.fixed = (True, True, True, True, False, True)

        self._connection_axial_rotation.parent = self._pin_hole_connection
        self._connection_axial_rotation.position = (0, 0, 0)

        # Position the connection pin (self) on the target pin and
        # place the parent of the parent of the pin (the axis) on the connection axis
        # and fix it
        slaved_axis = pin1.parent.parent

        slaved_axis.parent = self._axis_on_child
        slaved_axis.position = -np.array(pin1.parent.position)
        slaved_axis.rotation = rotation_from_y_axis_direction(-1 * np.array(pin1.axis))

        slaved_axis.fixed = True

        self._axis_on_child.parent = self._connection_axial_rotation
        self._axis_on_child.rotation = (0, 0, 0)
        self._axis_on_child.fixed = (True, True, True, True, False, True)

        if self._inside_connection:

            # Place the pin in the hole
            self._connection_axial_rotation.rotation = (0, 0, 0)
            self._axis_on_child.position = (pin2.radius - pin1.radius, 0, 0)

        else:

            # pin-pin connection
            self._axis_on_child.position = (pin1.radius + pin2.radius, 0, 0)
            self._connection_axial_rotation.rotation = (90, 0, 0)

        # restore settings
        self.swivel = c_swivel
        self.swivel_fixed = c_swivel_fixed
        self.rotation_on_parent = c_rotation_on_parent
        self.fixed_to_parent = c_fixed_to_parent
        self.child_rotation = c_child_rotation
        self.child_fixed = c_child_fixed

        self._scene.current_manager = remember

    def set_pin_pin_connection(self):
        """Sets the connection to be of type pin-pin"""

        self._inside_connection = False
        if self.swivel == 0:
            self.swivel = 90
        elif self.swivel == 180:
            self.swivel = 270

        self._update_connection()

    def set_pin_in_hole_connection(self):
        """Sets the connection to be of type pin-in-hole

        The axes of the two sheaves are aligned by rotating the slaved body
        The axes of the two sheaves are placed at a distance hole_dia - pin_dia apart, perpendicular to the axis direction
        An axes is created at the centers of the two sheaves
        These axes are connected with a shore axis which is allowed to rotate relative to the nodeA axis
        the nodeB axis is fixed to this rotating axis
        """
        self._inside_connection = True

        if self.swivel == 90:
            self.swivel = 0
        elif self.swivel == 270:
            self.swivel = 180

        self._update_connection()

    def managed_nodes(self):
        """Returns a list of managed nodes"""

        return [
            self._child_circle_parent_parent,
            self._axis_on_parent,
            self._axis_on_child,
            self._pin_hole_connection,
            self._connection_axial_rotation,
        ]

    def depends_on(self):
        return [self._parent_circle, self._child_circle]

    def creates(self, node: Node):
        return node in [
            self._axis_on_parent,
            self._axis_on_child,
            self._pin_hole_connection,
            self._connection_axial_rotation,
        ]

    def flip(self):
        """Changes the swivel angle by 180 degrees"""
        self.swivel = np.mod(self.swivel + 180, 360)

    def change_side(self):
        self.rotation_on_parent = np.mod(self.rotation_on_parent + 180, 360)
        self.child_rotation = np.mod(self.child_rotation + 180, 360)

    @property
    def swivel(self):
        """Swivel angle between parent and child objects [degrees]"""
        return self._connection_axial_rotation.rotation[0]

    @swivel.setter
    @node_setter_manageable
    @node_setter_observable
    def swivel(self, value):
        remember = self._scene.current_manager  # claim management
        self._scene.current_manager = self
        self._connection_axial_rotation.rx = value
        self._scene.current_manager = remember  # restore old manager

    @property
    def swivel_fixed(self):
        """Allow parent and child to swivel relative to eachother [boolean]"""
        return self._connection_axial_rotation.fixed[3]

    @swivel_fixed.setter
    @node_setter_manageable
    @node_setter_observable
    def swivel_fixed(self, value):
        remember = self._scene.current_manager  # claim management
        self._scene.current_manager = self
        self._connection_axial_rotation.fixed = [True, True, True, value, True, True]
        self._scene.current_manager = remember  # restore old manager

    @property
    def rotation_on_parent(self):
        """Angle between the line connecting the centers of the circles and the axis system of the parent node [degrees]"""
        return self._pin_hole_connection.ry

    @rotation_on_parent.setter
    @node_setter_manageable
    @node_setter_observable
    def rotation_on_parent(self, value):
        remember = self._scene.current_manager  # claim management
        self._scene.current_manager = self
        self._pin_hole_connection.ry = value
        self._scene.current_manager = remember  # restore old manager

    @property
    def fixed_to_parent(self):
        """Allow rotation around parent [boolean]

        see also: rotation_on_parent"""
        return self._pin_hole_connection.fixed[4]

    @fixed_to_parent.setter
    @node_setter_manageable
    @node_setter_observable
    def fixed_to_parent(self, value):
        remember = self._scene.current_manager  # claim management
        self._scene.current_manager = self
        self._pin_hole_connection.fixed = [True, True, True, True, value, True]
        self._scene.current_manager = remember  # restore old manager

    @property
    def child_rotation(self):
        """Angle between the line connecting the centers of the circles and the axis system of the child node [degrees]"""
        return self._axis_on_child.ry

    @child_rotation.setter
    @node_setter_manageable
    @node_setter_observable
    def child_rotation(self, value):
        remember = self._scene.current_manager  # claim management
        self._scene.current_manager = self
        self._axis_on_child.ry = value
        self._scene.current_manager = remember  # restore old manager

    @property
    def child_fixed(self):
        """Allow rotation of child relative to connection, see also: child_rotation [boolean]"""
        return self._axis_on_child.fixed[4]

    @child_fixed.setter
    @node_setter_manageable
    @node_setter_observable
    def child_fixed(self, value):
        remember = self._scene.current_manager  # claim management
        self._scene.current_manager = self
        self._axis_on_child.fixed = [True, True, True, True, value, True]
        self._scene.current_manager = remember  # restore old manager

    @property
    def inside(self):
        """Type of connection: True means child circle is inside parent circle, False means the child circle is outside but the circumferences contact [boolean]"""
        return self._inside_connection

    @inside.setter
    @node_setter_manageable
    @node_setter_observable
    def inside(self, value):
        if value == self._inside_connection:
            return

        if value:
            self.set_pin_in_hole_connection()
        else:
            self.set_pin_pin_connection()

    def give_python_code(self):

        old_manger = self._scene.current_manager
        self._scene.current_manager = self

        code = []

        # code.append('#  create the connection')
        code.append(f"s.new_geometriccontact(name = '{self.name}',")
        code.append(f"                       child = '{self._child_circle.name}',")
        code.append(f"                       parent = '{self._parent_circle.name}',")
        code.append(f"                       inside={self.inside},")

        if self.inside and self.swivel == 0:
            pass  # default for inside
        else:
            if not self.inside and self.swivel == 90:
                pass  # default for outside
            else:
                if self.swivel_fixed:
                    code.append(f"                       swivel={self.swivel},")
                else:
                    code.append(f"                       swivel=solved({self.swivel}),")

        if not self.swivel_fixed:
            code.append(f"                       swivel_fixed={self.swivel_fixed},")

        # There the three optional degrees of freedom:
        #     gc.rotation_on_parent
        #     gc.child_rotation
        #     gc.swivel


        if self.fixed_to_parent:
            code.append(
                f"                       rotation_on_parent={self.rotation_on_parent},"
            )
            code.append(
                f"                       fixed_to_parent={self.fixed_to_parent},"
            )
        else:
            code.append(
                f"                       rotation_on_parent=solved({self.rotation_on_parent}),"
            )

        if self.child_fixed:
            code.append(f"                       child_fixed={self.child_fixed},")
            code.append(f"                       child_rotation={self.child_rotation},")
        else:
            code.append(
                f"                       child_rotation=solved({self.child_rotation}),"
            )


        code = [
            *code[:-1],
            code[-1][:-1] + " )",
        ]  # remove the , from the last entry [should be a quicker way to do this]

        self._scene.current_manager = old_manger

        return "\n".join(code)


class Sling(Manager):
    """A Sling is a single wire with an eye on each end. The eyes are created by splicing the end of the sling back
    into the itself.

    The geometry of a sling is defined as follows:

    diameter : diameter of the wire
    LeyeA, LeyeB : inside lengths of the eyes
    LsplicaA, LspliceB : the length of the splices
    Ultimate length : the distance between the insides of ends of the eyes A and B when pulled straight (= Ultimate Length).

    Stiffness:
    The stiffness of the sling is specified by a single value: EA. EA can be set directly or by providing a k_total
    This determines the stiffnesses of the individual parts as follows:
    Wire in the eyes: EA
    Splices: Infinity (rigid)

    See Also: Grommet

    """

    def __init__(
        self,
        scene,
        name,
        length,
        LeyeA,
        LeyeB,
        LspliceA,
        LspliceB,
        diameter,
        EA,
        mass,
        endA=None,
        endB=None,
        sheaves=None,
    ):
        """
        Creates a new sling with the following structure

            endA
            eyeA (cable)
            splice (body , mass/2)
            nodeA (cable)     [optional: runs over sheave]
            splice (body, mass/2)
            eyeB (cable)
            endB

        Args:
            scene:     The scene in which the sling should be created
            name:  Name prefix
            length: Total length measured between the inside of the eyes of the sling is pulled straight.
            LeyeA: Total inside length in eye A if stretched flat
            LeyeB: Total inside length in eye B if stretched flat
            LspliceA: Length of the splice at end A
            LspliceB: Length of the splice at end B
            diameter: Diameter of the sling
            EA: Effective mean EA of the sling
            mass: total mass
            endA : Sheave or poi to fix end A of the sling to [optional]
            endB : Sheave or poi to fix end A of the sling to [optional]
            sheave : Sheave or poi for the nodeA part of the sling

        Returns:

        """

        super().__init__(scene)


        name_prefix = self.name + vfc.MANAGED_NODE_IDENTIFIER

        # store the properties
        self._length = length
        self._LeyeA = LeyeA
        self._LeyeB = LeyeB
        self._LspliceA = LspliceA
        self._LspliceB = LspliceB
        self._diameter = diameter
        self._EA = EA
        self._mass = mass
        self._endA = scene._poi_or_sheave_from_node(endA)
        self._endB = scene._poi_or_sheave_from_node(endB)

        # create the two splices

        self.sa = scene.new_rigidbody(
            scene.available_name_like(name_prefix + "_spliceA"), fixed=False
        )
        self.a1 = scene.new_point(
            scene.available_name_like(name_prefix + "_spliceA"), parent=self.sa
        )
        self.a2 = scene.new_point(
            scene.available_name_like(name_prefix + "_spliceA2"), parent=self.sa
        )
        self.am = scene.new_point(
            scene.available_name_like(name_prefix + "_spliceAM"), parent=self.sa
        )

        self.avis = scene.new_visual(
            name + "_spliceA_visual",
            parent=self.sa,
            path=r"cylinder 1x1x1 lowres.obj",
            offset=(-LspliceA / 2, 0.0, 0.0),
            rotation=(0.0, 90.0, 0.0),
            scale=(LspliceA, 2 * diameter, diameter),
        )

        self.sb = scene.new_rigidbody(
            scene.available_name_like(name_prefix + "_spliceB"),
            rotation=(0, 0, 180),
            fixed=False,
        )
        self.b1 = scene.new_point(
            scene.available_name_like(name_prefix + "_spliceB1"), parent=self.sb
        )
        self.b2 = scene.new_point(
            scene.available_name_like(name_prefix + "_spliceB2"), parent=self.sb
        )
        self.bm = scene.new_point(
            scene.available_name_like(name_prefix + "_spliceBM"), parent=self.sb
        )

        self.bvis = scene.new_visual(
            scene.available_name_like(name_prefix + "_spliceB_visual"),
            parent=self.sb,
            path=r"cylinder 1x1x1 lowres.obj",
            offset=(-LspliceB / 2, 0.0, 0.0),
            rotation=(0.0, 90.0, 0.0),
            scale=(LspliceB, 2 * diameter, diameter),
        )

        self.main = scene.new_cable(
            scene.available_name_like(name_prefix + "_main_part"),
            endA=self.am,
            endB=self.bm,
            length=1,
            EA=1,
            diameter=diameter,
        )

        self.eyeA = scene.new_cable(
            scene.available_name_like(name_prefix + "_eyeA"),
            endA=self.a1,
            endB=self.a2,
            length=1,
            EA=1,
        )
        self.eyeB = scene.new_cable(
            scene.available_name_like(name_prefix + "_eyeB"),
            endA=self.b1,
            endB=self.b2,
            length=1,
            EA=1,
        )

        # set initial positions of splices if we can
        if self._endA is not None and self._endB is not None:
            a = np.array(self._endA.global_position)
            b = np.array(self._endB.global_position)

            dir = b - a
            if np.linalg.norm(dir) > 1e-6:
                dir /= np.linalg.norm(dir)

                self.sa.rotation = rotation_from_x_axis_direction(-dir)
                self.sb.rotation = rotation_from_x_axis_direction(dir)
                self.sa.position = a + (LeyeA + 0.5 * LspliceA) * dir
                self.sb.position = b - (LeyeB + 0.5 * LspliceB) * dir

        # Update properties
        self.sheaves = sheaves
        self._update_properties()

        self.name = name

        for n in self.managed_nodes():
            n.manager = self

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert self._scene.name_available(value), f"Name {value} already in use"

        self._rename_all_manged_nodes(self.name, value)
        self._name = value

    @property
    def _Lmain(self):
        """Length of the main section"""
        return (
            self._length - self._LspliceA - self._LspliceB - self._LeyeA - self._LeyeB
        )

    @property
    def _LwireEyeA(self):
        return 2 * self._LeyeA + 0.5 * np.pi * self._diameter

    @property
    def _LwireEyeB(self):
        return 2 * self._LeyeB + 0.5 * np.pi * self._diameter

    @property
    def k_total(self):
        """Total stiffness of the sling in kN/m"""

        k_eye_A = 4 * self._EA / self._LwireEyeA
        k_eye_B = 4 * self._EA / self._LwireEyeB

        k_splice_A = 2 * self._EA / (self._LspliceA)
        k_splice_B = 2 * self._EA / (self._LspliceB)

        k_main = self._EA / self._Lmain

        k_total = 1 / (
            1 / k_eye_A + 1 / k_eye_B + 1 / k_splice_A + 1 / k_splice_B + 1 / k_main
        )

        return k_total

    @k_total.setter
    def k_total(self, value):
        assert1f_positive_or_zero(value)

        EA = (
            0.25
            * value
            * (
                self._LwireEyeA
                + self._LwireEyeB
                + 4.0 * self._Lmain
                + 2.0 * self.LspliceA
                + 2.0 * self._LspliceB
            )
        )

        self.EA = EA

    def _update_properties(self):

        # The stiffness of the main part is corrected to account for the stiffness of the splices.
        # It is considered that the stiffness of the splices is two times that of the wire.
        #
        # Springs in series: 1/Ktotal = 1/k1 + 1/k2 + 1/k3

        backup = self._scene.current_manager  # store
        self._scene.current_manager = self

        Lmain = (
            self._length - self._LspliceA - self._LspliceB - self._LeyeA - self._LeyeB
        )

        if self._EA == 0:
            EAmain = 0
        else:
            ka = 2 * self._EA / self._LspliceA
            kb = 2 * self._EA / self._LspliceB
            kmain = self._EA / Lmain
            k_total = 1 / ((1 / ka) + (1 / kmain) + (1 / kb))

            EAmain = k_total * Lmain

        self.sa.mass = self._mass / 2

        self.sa.inertia_radii = radii_from_box_shape(
            self._LspliceA,
            self._LspliceA,
            self._diameter,
        )

        self.a1.position = (self._LspliceA / 2, self._diameter / 2, 0)
        self.a2.position = (self._LspliceA / 2, -self._diameter / 2, 0)
        self.am.position = (-self._LspliceA / 2, 0, 0)

        self.avis.offset = (-self._LspliceA / 2, 0.0, 0.0)
        self.avis.scale = (self._LspliceA, 2 * self._diameter, self._diameter)

        self.sb.mass = self._mass / 2

        self.sb.inertia_radii = radii_from_box_shape(
            self._LspliceB,
            self._LspliceB,
            self._diameter,
        )

        self.b1.position = (self._LspliceB / 2, self._diameter / 2, 0)
        self.b2.position = (self._LspliceB / 2, -self._diameter / 2, 0)
        self.bm.position = (-self._LspliceB / 2, 0, 0)

        self.bvis.offset = (-self._LspliceB / 2, 0.0, 0.0)
        self.bvis.scale = (self._LspliceB, 2 * self._diameter, self._diameter)

        self.main.length = Lmain
        self.main.EA = EAmain
        self.main.diameter = self._diameter
        self.main.connections = tuple([self.am, *self._sheaves, self.bm])

        self.eyeA.length = self._LwireEyeA
        self.eyeA.EA = self._EA
        self.eyeA.diameter = self._diameter

        if self._endA is not None:
            self.eyeA.connections = (self.a1, self._endA, self.a2)
        else:
            self.eyeA.connections = (self.a1, self.a2)

        self.eyeB.length = self._LwireEyeB
        self.eyeB.EA = self._EA
        self.eyeB.diameter = self._diameter

        if self._endB is not None:
            self.eyeB.connections = (self.b1, self._endB, self.b2)
        else:
            self.eyeB.connections = (self.b1, self.b2)

        self._scene.current_manager = backup  # restore

    def depends_on(self):
        """The sling depends on the endpoints and sheaves (if any)"""

        a = list()

        if self._endA is not None:
            a.append(self._endA)
        if self._endB is not None:
            a.append(self._endB)

        a.extend(self.sheaves)

        return a

    def managed_nodes(self):
        a = [
            self.sa,
            self.a1,
            self.a2,
            self.am,
            self.avis,
            self.sb,
            self.b1,
            self.b2,
            self.bm,
            self.bvis,
            self.main,
            self.eyeA,
            self.eyeB,
        ]

        return a

    def creates(self, node: Node):
        return node in self.managed_nodes()  # all these are created

    def delete(self):

        # delete created nodes
        a = self.managed_nodes()

        for n in a:
            n._manager = None

        for n in a:
            if n in self._scene._nodes:
                self._scene.delete(n)  # delete if it is still available

    def give_python_code(self):
        code = f"# Exporting {self.name}"

        code += "\n# Create sling"

        # (self, scene, name, Ltotal, LeyeA, LeyeB, LspliceA, LspliceB, diameter, EA, mass, endA = None, endB=None, sheaves=None):

        code += f'\ns.new_sling("{self.name}", length = {self.length},'
        code += f"\n            LeyeA = {self.LeyeA},"
        code += f"\n            LeyeB = {self.LeyeB},"
        code += f"\n            LspliceA = {self.LspliceA},"
        code += f"\n            LspliceB = {self.LspliceB},"
        code += f"\n            diameter = {self.diameter},"
        code += f"\n            EA = {self.EA},"
        code += f"\n            mass = {self.mass},"
        code += f'\n            endA = "{self.endA.name}",'
        code += f'\n            endB = "{self.endB.name}",'

        if self.sheaves:
            sheaves = "["
            for s in self.sheaves:
                sheaves += f'"{s.name}", '
            sheaves = sheaves[:-2] + "]"
        else:
            sheaves = "None"

        code += f"\n            sheaves = {sheaves})"

        return code

    # properties
    @property
    def length(self):
        """Total length measured between the INSIDE of the eyes of the sling is pulled straight. [m]"""
        return self._length

    @length.setter
    @node_setter_manageable
    @node_setter_observable
    def length(self, value):

        min_length = self.LeyeA + self.LeyeB + self.LspliceA + self.LspliceB
        if value <= min_length:
            raise ValueError(
                "Total length of the sling should be at least the length of the eyes plus the length of the splices"
            )

        self._length = value
        self._update_properties()

    @property
    def LeyeA(self):
        """Total length inside eye A if stretched flat [m]"""
        return self._LeyeA

    @LeyeA.setter
    @node_setter_manageable
    @node_setter_observable
    def LeyeA(self, value):

        max_length = self.length - (self.LeyeB + self.LspliceA + self.LspliceB)
        if value >= max_length:
            raise ValueError(
                "Total length of the sling should be at least the length of the eyes plus the length of the splices"
            )

        self._LeyeA = value
        self._update_properties()

    @property
    def LeyeB(self):
        """Total length inside eye B if stretched flat [m]"""
        return self._LeyeB

    @LeyeB.setter
    @node_setter_manageable
    @node_setter_observable
    def LeyeB(self, value):

        max_length = self.length - (self.LeyeA + self.LspliceA + self.LspliceB)
        if value >= max_length:
            raise ValueError(
                "Total length of the sling should be at least the length of the eyes plus the length of the splices"
            )

        self._LeyeB = value
        self._update_properties()

    @property
    def LspliceA(self):
        """Length of the splice at end A [m]"""
        return self._LspliceA

    @LspliceA.setter
    @node_setter_manageable
    @node_setter_observable
    def LspliceA(self, value):

        max_length = self.length - (self.LeyeA + self.LeyeB + self.LspliceB)
        if value >= max_length:
            raise ValueError(
                "Total length of the sling should be at least the length of the eyes plus the length of the splices"
            )

        self._LspliceA = value
        self._update_properties()

    @property
    def LspliceB(self):
        """Length of the splice at end B [m]"""
        return self._LspliceB

    @LspliceB.setter
    @node_setter_manageable
    @node_setter_observable
    def LspliceB(self, value):

        max_length = self.length - (self.LeyeA + self.LeyeB + self.LspliceA)
        if value >= max_length:
            raise ValueError(
                "Total length of the sling should be at least the length of the eyes plus the length of the splices"
            )

        self._LspliceB = value
        self._update_properties()

    @property
    def diameter(self):
        """Diameter of the sling (except the splices) [m]"""
        return self._diameter

    @diameter.setter
    @node_setter_manageable
    @node_setter_observable
    def diameter(self, value):
        self._diameter = value
        self._update_properties()

    @property
    def EA(self):
        """EA of the wire of the sling. See also: k_total"""
        return self._EA

    @EA.setter
    @node_setter_manageable
    @node_setter_observable
    def EA(self, value):
        self._EA = value
        self._update_properties()

    @property
    def mass(self):
        """Mass and weight of the sling. This mass is discretized  distributed over the two splices [mT]"""
        return self._mass

    @mass.setter
    @node_setter_manageable
    @node_setter_observable
    def mass(self, value):
        self._mass = value
        self._update_properties()

    @property
    def endA(self):
        """End A [circle or point node]"""
        return self._endA

    @endA.setter
    @node_setter_manageable
    @node_setter_observable
    def endA(self, value):
        node = self._scene._node_from_node_or_str(value)
        self._endA = self._scene._poi_or_sheave_from_node(node)
        self._update_properties()

    @property
    def endB(self):
        """End B [circle or point node]"""
        return self._endB

    @endB.setter
    @node_setter_manageable
    @node_setter_observable
    def endB(self, value):
        node = self._scene._node_from_node_or_str(value)
        self._endB = self._scene._poi_or_sheave_from_node(node)
        self._update_properties()

    @property
    def sheaves(self):
        """List of sheaves (circles, points) that the sling runs over between the two ends.

        May be provided as list of nodes or node-names.
        """
        return self._sheaves

    @sheaves.setter
    @node_setter_manageable
    @node_setter_observable
    def sheaves(self, value):
        s = []
        for v in value:
            node = self._scene._node_from_node_or_str(v)
            s.append(self._scene._poi_or_sheave_from_node(node))
        self._sheaves = s
        self._update_properties()


class Shackle(Manager, RigidBody):
    """
    Green-Pin Heavy Duty Bow Shackle BN

    visual from: https://www.traceparts.com/en/product/green-pinr-p-6036-green-pinr-heavy-duty-bow-shackle-bn-hdgphm0800-mm?CatalogPath=TRACEPARTS%3ATP04001002006&Product=10-04072013-086517&PartNumber=HDGPHM0800
    details from: https://www.greenpin.com/sites/default/files/2019-04/brochure-april-2019.pdf

    wll a b c d e f g h i j k weight
    [t] [mm]  [kg]
    120 95 95 208 95 147 400 238 647 453 428 50 110
    150 105 108 238 105 169 410 275 688 496 485 50 160
    200 120 130 279 120 179 513 290 838 564 530 70 235
    250 130 140 299 130 205 554 305 904 614 565 70 295
    300 140 150 325 140 205 618 305 996 644 585 80 368
    400 170 175 376 164 231 668 325 1114 690 665 70 560
    500 180 185 398 164 256 718 350 1190 720 710 70 685
    600 200 205 444 189 282 718 375 1243 810 775 70 880
    700 210 215 454 204 308 718 400 1263 870 820 70 980
    800 210 220 464 204 308 718 400 1270 870 820 70 1100
    900 220 230 485 215 328 718 420 1296 920 860 70 1280
    1000 240 240 515 215 349 718 420 1336 940 900 70 1460
    1250 260 270 585 230 369 768 450 1456 1025 970 70 1990
    1500 280 290 625 230 369 818 450 1556 1025 1010 70 2400

    Returns:

    """

    data = dict()
    # key = wll in t
    # dimensions a..k in [mm]
    #             a     b    c   d     e    f    g    h     i     j    k   weight[kg]
    # index       0     1    2    3    4    5    6    7     8     9    10   11
    data["GP120"] = (95, 95, 208, 95, 147, 400, 238, 647, 453, 428, 50, 110)
    data["GP150"] = (105, 108, 238, 105, 169, 410, 275, 688, 496, 485, 50, 160)
    data["GP200"] = (120, 130, 279, 120, 179, 513, 290, 838, 564, 530, 70, 235)
    data["GP250"] = (130, 140, 299, 130, 205, 554, 305, 904, 614, 565, 70, 295)
    data["GP300"] = (140, 150, 325, 140, 205, 618, 305, 996, 644, 585, 80, 368)
    data["GP400"] = (170, 175, 376, 164, 231, 668, 325, 1114, 690, 665, 70, 560)
    data["GP500"] = (180, 185, 398, 164, 256, 718, 350, 1190, 720, 710, 70, 685)
    data["GP600"] = (200, 205, 444, 189, 282, 718, 375, 1243, 810, 775, 70, 880)
    data["GP700"] = (210, 215, 454, 204, 308, 718, 400, 1263, 870, 820, 70, 980)
    data["GP800"] = (210, 220, 464, 204, 308, 718, 400, 1270, 870, 820, 70, 1100)
    data["GP900"] = (220, 230, 485, 215, 328, 718, 420, 1296, 920, 860, 70, 1280)
    data["GP1000"] = (240, 240, 515, 215, 349, 718, 420, 1336, 940, 900, 70, 1460)
    data["GP1250"] = (260, 270, 585, 230, 369, 768, 450, 1456, 1025, 970, 70, 1990)
    data["GP1500"] = (280, 290, 625, 230, 369, 818, 450, 1556, 1025, 1010, 70, 2400)

    def defined_kinds(self):
        """Defined shackle kinds"""
        list = [a for a in Shackle.data.keys()]
        return list

    def _give_values(self, kind):
        if kind not in Shackle.data:
            for key in Shackle.data.keys():
                print(key)
            raise ValueError(
                f"No data available for a Shackle of kind {kind}. Available values printed above"
            )

        return Shackle.data[kind]

    def __init__(self, scene, name, kind, a, p, g):

        Manager.__init__(self, scene)
        RigidBody.__init__(self, scene, axis=a, poi=p, force=g)

        _ = self._give_values(kind)  # to make sure it exists

        # origin is at center of pin
        # z-axis up
        # y-axis in direction of pin

        # self.body = scene.new_rigidbody(name=name + '_body')

        # pin
        self.pin_point = scene.new_point(
            name=name + "_pin_point", parent=self, position=(0.0, 0.0, 0.0)
        )
        self.pin = scene.new_circle(
            name=name + "_pin", parent=self.pin_point, axis=(0.0, 1.0, 0.0)
        )

        # bow
        self.bow_point = scene.new_point(name=name + "_bow_point", parent=self)

        self.bow = scene.new_circle(
            name=name + "_bow", parent=self.bow_point, axis=(0.0, 1.0, 0.0)
        )

        # inside circle
        self.inside_point = scene.new_point(
            name=name + "_inside_circle_center", parent=self
        )
        self.inside = scene.new_circle(
            name=name + "_inside", parent=self.inside_point, axis=(1.0, 0, 0)
        )

        # code for GP800_visual
        self.visual_node = scene.new_visual(
            name=name + "_visual",
            parent=self,
            path=r"shackle_gp800.obj",
            offset=(0, 0, 0),
            rotation=(0, 0, 0),
        )

        self.kind = kind
        self.name = name

        for n in self.managed_nodes():
            n.manager = self

    def depends_on(self):
        return []

    @property
    def kind(self):
        """Type of shackle, for example GP800 [text]"""
        return self._kind

    @kind.setter
    # @node_setter_manageable   : allow changing of shackle kind
    @node_setter_observable
    def kind(self, kind):

        values = self._give_values(kind)
        weight = values[11] / 1000  # convert to tonne
        pin_dia = values[1] / 1000
        bow_dia = values[0] / 1000
        bow_length_inside = values[5] / 1000
        bow_circle_inside = values[6] / 1000

        cogz = 0.5 * pin_dia + bow_length_inside / 3  # estimated

        remember = self._scene.current_manager

        self._scene.current_manager = (
            self.manager
        )  # WORK-AROUND : in case the shackle itself is managed, fake management

        self.mass = weight
        self.cog = (0, 0, cogz)

        self._scene.current_manager = self  # register self a manager (as it should)

        self.pin.radius = pin_dia / 2

        self.bow_point.position = (
            0.0,
            0.0,
            0.5 * pin_dia + bow_length_inside + 0.5 * bow_dia,
        )
        self.bow.radius = bow_dia / 2

        self.inside_point.position = (
            0,
            0,
            0.5 * pin_dia + bow_length_inside - 0.5 * bow_circle_inside,
        )
        self.inside.radius = bow_circle_inside / 2

        # determine the scale for the shackle
        # based on a GP800
        #
        actual_size = 0.5 * pin_dia + 0.5 * bow_dia + bow_length_inside
        gp800_size = 0.5 * 0.210 + 0.5 * 0.220 + 0.718

        scale = actual_size / gp800_size

        self.visual_node.scale = [scale, scale, scale]

        self._scene.current_manager = remember

        self._kind = kind

    def managed_nodes(self):
        return [
            self.pin_point,
            self.pin,
            self.bow_point,
            self.bow,
            self.inside_point,
            self.inside,
            self.visual_node,
        ]

    def creates(self, node: Node):
        return node in self.managed_nodes()  # all these are created

    def delete(self):

        # delete created nodes
        a = self.managed_nodes()

        for n in a:
            n._manager = None

        for n in a:
            if n in self._scene._nodes:
                self._scene.delete(n)  # delete if it is still available

    @property
    def name(self):
        """Name of the node (str), must be unique"""
        return RigidBody.name.fget(self)

    @name.setter
    def name(self, value):
        old_name = self.name
        RigidBody.name.fset(self,value)
        self._rename_all_manged_nodes(old_name, value)



    def give_python_code(self):
        code = f"# Exporting {self.name}"

        code += "\n# Create Shackle"
        code += f'\ns.new_shackle("{self.name}", kind = "{self.kind}")'  # , elastic={self.elastic})'

        if self.parent_for_export:
            code += f"\ns['{self.name}'].parent = s['{self.parent_for_export.name}']"

        code += "\ns['{}'].position = ({},{},{})".format(self.name, *self.position)
        code += "\ns['{}'].rotation = ({},{},{})".format(self.name, *self.rotation)
        if not np.all(self.fixed):
            code += "\ns['{}'].fixed = ({},{},{},{},{},{})".format(self.name, *self.fixed)



        return code


# =============== Scene


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

    def __init__(self, filename=None, copy_from=None, code=None):
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

        self._savepoint = None
        """Python code to re-create the scene, see savepoint_make()"""

        self._name_prefix = ""
        """An optional prefix to be applied to node names. Used when importing scenes."""

        self.current_manager = None
        """Setting this to an instance of a Manager allows nodes with that manager to be changed"""

        self._godmode = False
        """Icarus warning, wear proper PPE"""

        self._export_code_with_solved_function = True
        """Wrap solved values in 'solved' function when exporting python code"""

        if filename is not None:
            self.load_scene(filename)

        if copy_from is not None:
            self.import_scene(copy_from, containerize=False)

        if code is not None:
            self.run_code(code)

    def clear(self):
        """Deletes all nodes"""

        self._nodes = []
        del self._vfc
        self._vfc = pyo3d.Scene()

    # =========== settings =============

    @property
    def g(self):
        """Gravity in kg*m/s2"""
        return self._vfc.g

    @g.setter
    def g(self, value):
        assert1f(value)
        rbs = self.nodes_of_type(RigidBody)
        for n in rbs:
            n._mass = n.mass
        self._vfc.g = value
        for n in rbs:
            n.mass = n._mass

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

    def _prefix_name(self, name):
        return self._name_prefix + name

    def _verify_name_available(self, name):
        """Throws an error if a node with name 'name' already exists"""
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
            node = self[self._name_prefix + node]

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

        for name in original_fixes.keys():
            self.node_by_name(name).fixed = original_fixes[name]

    def _check_and_fix_geometric_contact_orientations(self) -> (bool, str):
        """A Geometric pin on pin contact may end up with tension in the contact. Fix that by moving the child pin to the other side of the parent pin

        Returns:
            True if anything was changed; False otherwise
        """

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

    def get_resource_list(self, extension):
        """Returns a list of all file-paths (strings) given extension in any of the resource-paths"""

        r = []

        for dir in self.resources_paths:
            try:
                files = listdir(dir)
                for file in files:
                    if file.lower().endswith(extension):
                        if file not in r:
                            r.append("res: " + file)
            except FileNotFoundError:
                pass

        return r

    # ======== element functions =========

    def node_by_name(self, node_name, silent=False):
        for N in self._nodes:
            if N.name == node_name:
                return N

        if not silent:
            self.print_node_tree()
        raise ValueError(
            'No node with name "{}". Available names printed above.'.format(node_name)
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

    def sort_nodes_by_parent(self):
        """Sorts the nodes such that the parent of this node (if any) occurs earlier in the list.

        See Also:
            sort_nodes_by_dependency
        """

        self.assert_unique_names()

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

        # scene_names = [n.name for n in self._nodes]
        #
        # self._vfc.state_update()  # use the function from the core.
        # new_list = []
        # for name in self._vfc.names:  # and then build a new list using the names
        #     if vfc.VF_NAME_SPLIT in name:
        #         continue
        #
        #     if name not in scene_names:
        #         raise Exception('Something went wrong with sorting the the nodes by dependency. '
        #                         'Node naming between core and scene is inconsistent for node {}'.format(name))
        #
        #     new_list.append(self[name])
        #
        # # and add the nodes without a vfc-core connection
        # for node in self._nodes:
        #     if not node in new_list:
        #         new_list.append(node)
        #
        # self._nodes = new_list

    def assert_name_available(self, name):
        """Raises an error is name is not available"""
        assert self.name_available(name), f"Name {name} is already in use"

    def name_available(self, name):
        """Returns True if the name is still available"""
        names = [n.name for n in self._nodes]
        names.extend(self._vfc.names)
        return not (name in names)

    def available_name_like(self, like):
        """Returns an available name like the one given, for example Axis23"""
        if self.name_available(like):
            return like
        counter = 1
        while True:
            name = like + "_" + str(counter)
            if self.name_available(name):
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

    def nodes_with_parent(self, node):
        """Returns a list of nodes that have given node as a parent. Good for making trees.
        For checking physical connections use nodes_depending_on instead.

        Args:
            node : Node or node-name

        Returns:
            list of names

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
                r.append(n.name)

        return r

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

        # First delete the dependencies
        for d in depending_nodes:
            if not self.name_available(d):  # element is still here
                self.delete(d)

        # then remove the vtk node itself
        # self._print('removing vfc node')
        node._delete_vfc()
        self._nodes.remove(node)

    def dissolve(self, node):
        """Attempts to delete the given node without affecting the rest of the model.

        1. Look for nodes that have this node as parent
        2. Attach those nodes to the parent of this node.
        3. Delete this node.

        There are many situations in which this will fail because an it is impossible to dissolve
        the element. For example a poi can only be dissolved when nothing is attached to it.

        For now this function only works on AXIS and Managers
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

                    if hasattr(node, "parent"):
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
                "Only nodes of type Axis and Manager can be dissolved at this moment"
            )

        self.delete(node)  # do not call delete as that will fail on managers

    def savepoint_make(self):
        self._savepoint = self.give_python_code()

    def savepoint_restore(self):
        if self._savepoint is not None:
            self.clear()
            exec(self._savepoint, {}, {"s": self})
            self._savepoint = None
            return True
        else:
            return False

    # ========= The most important functions ========

    def update(self):
        """Updates the interface between the nodes and the core. This includes the re-calculation of all forces,
        buoyancy positions, ballast-system cogs etc.
        """
        for n in self._nodes:
            n.update()
        self._vfc.state_update()

    def solve_statics(self, silent=False, timeout=None):
        """Solves statics

        Args:
            silent: Do not print if successfully solved

        Returns:
            bool: True if successful, False otherwise.

        """
        self.update()

        if timeout is None:
            solve_func = self._vfc.state_solve_statics
        else:
            #       bool doStabilityCheck,
            #       double timeout,
            # 		bool do_prepare_state,
            # 		bool solve_linear_dofs_first,
            # 		double stability_check_delta
            solve_func = lambda: self._vfc.state_solve_statics_with_timeout(
                True, timeout, True, True, 0
            )  # default stability value

        # pass 1
        orignal_fixes = self._fix_vessel_heel_trim()
        succes = solve_func()
        if not succes:
            self._restore_original_fixes(orignal_fixes)
            return False

        if orignal_fixes:
            # pass 2
            self._restore_original_fixes(orignal_fixes)
            succes = solve_func()

        if self.verify_equilibrium():

            changed, message = self._check_and_fix_geometric_contact_orientations()
            if changed:
                print(message)
                solve_func()
                if not self.verify_equilibrium():
                    return False

            if not silent:
                self._print(f"Solved to {self._vfc.Emaxabs:.3e} kN")
            return True

        d = np.array(self._vfc.get_dofs())
        if np.any(np.abs(d) > 2000):
            print(
                "Error: One of the degrees of freedom exceeded the boundary of 2000 [m]/[rad]."
            )
            return False

        return False

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
        """Creates a new *axis* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node
            position: optional, position for the node (x,y,z)
            rotation: optional, rotation for the node (rx,ry,rz)
            fixed [True]: optional, determines whether the axis is fixed [True] or free [False]. May also be a sequence of 6 booleans.

        Returns:
            Reference to newly created axis

        """

        # apply prefixes
        name = self._prefix_name(name)

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
        a = self._vfc.new_axis(name)

        new_node = Frame(self, a)

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

        self._nodes.append(new_node)
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

        # apply prefixes
        name = self._prefix_name(name)

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

        new_node = GeometricContact(self, child, parent, name)
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

        self._nodes.append(new_node)
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

        # apply prefixes
        name = self._prefix_name(name)

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

        new_node = WaveInteraction1(self)

        new_node.name = name
        new_node.path = path
        new_node.parent = parent

        # and set properties
        new_node.parent = b
        if offset is not None:
            new_node.offset = offset

        self._nodes.append(new_node)
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

        # apply prefixes
        name = self._prefix_name(name)

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

        new_node = Visual(self)

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

        self._nodes.append(new_node)
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

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if position is not None:
            assert3f(position, "Position ")

        # then create
        a = self._vfc.new_poi(name)

        new_node = Point(self, a)

        # and set properties
        if b is not None:
            new_node.parent = b
        if position is not None:
            new_node.position = position

        self._nodes.append(new_node)
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
            fixed [True]: optional, determines whether the axis is fixed [True] or free [False]. May also be a sequence of 6 booleans.

        Examples:
            scene.new_rigidbody("heavy_thing", mass = 10000, cog = (1.45, 0, -0.7))

        Returns:
            Reference to newly created RigidBody

        """

        # apply prefixes
        name = self._prefix_name(name)

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
            assert mass > 0, ValueError(
                "Can not set radii of gyration without specifying mass"
            )

        if not isinstance(fixed, bool):
            if len(fixed) != 6:
                raise Exception(
                    '"fixed" parameter should either be True/False or a 6x bool sequence such as (True,True,False,False,True,False)'
                )

        # make elements

        a = self._vfc.new_axis(name)

        p = self._vfc.new_poi(name + vfc.VF_NAME_SPLIT + "cog")
        p.parent = a
        p.position = cog

        g = self._vfc.new_force(name + vfc.VF_NAME_SPLIT + "gravity")
        g.parent = p
        g.force = (0, 0, -self.g * mass)

        r = RigidBody(self, a, p, g)

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

        self._nodes.append(r)
        return r

    def new_cable(
        self, name, endA, endB, length=-1, EA=0, diameter=0, sheaves=None
    ) -> Cable:
        """Creates a new *cable* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            endA : A Poi element to connect the first end of the cable to
            endB : A Poi element to connect the other end of the cable to
            length [-1] : un-stretched length of the cable in m; default [-1] create a cable with the current distance between the endpoints A and B
            EA [0] : stiffness of the cable in kN/m; default

            sheaves : [optional] A list of pois, these are sheaves that the cable runs over. Defined from endA to endB

        Examples:

            scene.new_cable('cable_name' endA='poi_start', endB = 'poi_end')  # minimal use

            scene.new_cable('cable_name', length=50, EA=1000, endA=poi_start, endB = poi_end, sheaves=[sheave1, sheave2])

            scene.new_cable('cable_name', length=50, EA=1000, endA='poi_start', endB = 'poi_end', sheaves=['single_sheave']) # also a single sheave needs to be provided as a list

        Notes:
            The default options for length and EA can be used to measure distances between points

        Returns:
            Reference to newly created Cable

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
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
        if length > -1:
            if length < 1e-9:
                raise Exception("Length should be more than 0")

        if EA < 0:
            raise Exception("EA should be more than 0")

        assert1f(diameter, "Diameter should be a number >= 0")

        if diameter < 0:
            raise Exception("Diameter should be >= 0")

        # then create
        a = self._vfc.new_cable(name)
        new_node = Cable(self, a)
        if length > 0:
            new_node.length = length
        new_node.EA = EA
        new_node.diameter = diameter

        new_node.connections = pois

        # and add to the scene
        self._nodes.append(new_node)

        if length < 0:
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

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._poi_from_node(parent)

        if force is not None:
            assert3f(force, "Force ")

        if moment is not None:
            assert3f(moment, "Moment ")

        # then create
        a = self._vfc.new_force(name)

        new_node = Force(self, a)

        # and set properties
        if b is not None:
            new_node.parent = b
        if force is not None:
            new_node.force = force
        if moment is not None:
            new_node.moment = moment

        self._nodes.append(new_node)
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

        # apply prefixes
        name = self._prefix_name(name)

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

        self._nodes.append(new_node)
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

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._poi_from_node(parent)

        assert3f(axis, "Axis of rotation ")

        assert1f(radius, "Radius of sheave")

        # then create
        a = self._vfc.new_sheave(name)

        new_node = Circle(self, a)

        # and set properties
        new_node.parent = b
        new_node.axis = axis
        new_node.radius = radius

        self._nodes.append(new_node)
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

        # apply prefixes
        name = self._prefix_name(name)

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

        self._nodes.append(new_node)

        return new_node

    def new_linear_connector_6d(self, name, main, secondary, stiffness=None) -> LC6d:
        """Creates a new *linear connector 6d* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            main: Main axis system [Axis]
            secondary: Secondary axis system [Axis]
            stiffness: optional, connection stiffness (x,y,z, rx,ry,rz)

        See :py:class:`LC6d` for details

        Returns:
            Reference to newly created connector

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        m = self._parent_from_node(secondary)
        s = self._parent_from_node(main)

        if stiffness is not None:
            assert6f(stiffness, "Stiffness ")
        else:
            stiffness = (0, 0, 0, 0, 0, 0)

        # then create
        a = self._vfc.new_linearconnector6d(name)

        new_node = LC6d(self, a)

        # and set properties
        new_node.main = m
        new_node.secondary = s
        new_node.stiffness = stiffness

        self._nodes.append(new_node)
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

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        m = self._parent_from_node(nodeA)
        s = self._parent_from_node(nodeB)

        assert1f(k_linear, "Linear stiffness")
        assert1f(k_angular, "Angular stiffness")

        # then create
        a = self._vfc.new_connector2d(name)

        new_node = Connector2d(self, a)

        # and set properties
        new_node.nodeA = m
        new_node.nodeB = s
        new_node.k_linear = k_linear
        new_node.k_angular = k_angular

        self._nodes.append(new_node)
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

        # apply prefixes
        name = self._prefix_name(name)

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
        a = self._vfc.new_linearbeam(name)

        new_node = Beam(self, a)

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

        self._nodes.append(new_node)
        return new_node

    def new_buoyancy(self, name, parent=None) -> Buoyancy:
        """Creates a new *buoyancy* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node


        Returns:
            Reference to newly created buoyancy

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        if b is None:
            raise ValueError("A valid parent must be defined for a Buoyancy node")

        # then create
        a = self._vfc.new_buoyancy(name)
        new_node = Buoyancy(self, a)

        # and set properties
        if b is not None:
            new_node.parent = b

        self._nodes.append(new_node)
        return new_node

    def new_tank(self, name, parent=None, density=1.025, free_flooding=False) -> Tank:
        """Creates a new *tank* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node

        Returns:
            Reference to newly created Tank

        """

        # apply prefixes
        name = self._prefix_name(name)

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
        a = self._vfc.new_tank(name)
        new_node = Tank(self, a)
        new_node.density = density

        # and set properties
        if b is not None:
            new_node.parent = b

        new_node.free_flooding = free_flooding

        self._nodes.append(new_node)
        return new_node

    def new_contactmesh(self, name, parent=None) -> ContactMesh:
        """Creates a new *contactmesh* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: optional, name of the parent of the node

        Returns:
            Reference to newly created contact mesh

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        # then create
        a = self._vfc.new_contactmesh(name)
        new_node = ContactMesh(self, a)

        # and set properties
        if b is not None:
            new_node.parent = b

        self._nodes.append(new_node)
        return new_node

    def new_spmt(
        self,
        name,
        parent,
        maximal_length=1.8,
        nominal_length=1.5,
        k=1e6,
        meshes=None,
        axles=None,
    ) -> SPMT:
        """Creates a new *SPMT* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the node [Axis]
            maximal_length: optional, maximum distance between top and bottom of wheel (1.5m + 300mm)
            nominal_length: optional, nominal distance between top and bottom of wheel [1.5m]
            k : stiffness per axle [kN/m]
            meshes : list of contact meshes
            axles  : list of axle locations [(x,y,z),(x,y,z), ... ]

        Returns:
            Reference to newly created SPMT

        """

        # apply prefixes
        name = self._prefix_name(name)

        # first check
        assertValidName(name)
        self._verify_name_available(name)
        parent = self._node_from_node_or_str(parent)
        assert isinstance(parent, Frame), ValueError(
            f"Parent should be an axis system or derived, not a {type(parent)}"
        )

        assert1f_positive_or_zero(maximal_length, "maximal_length ")
        assert1f_positive_or_zero(nominal_length, "nominal_length ")

        if meshes is not None:
            meshes = make_iterable(meshes)
            for mesh in meshes:
                test = self._node_from_node(
                    mesh, ContactMesh
                )  # throws error if not found

        if axles is not None:
            for p in axles:
                assert3f(p, "axle locations should be (x,y,z)")

        # then create
        a = self._vfc.new_spmt(name)

        new_node = SPMT(self, a)

        # and set properties
        new_node.parent = parent
        new_node.k = k
        new_node.max_length = maximal_length
        new_node.nominal_length = nominal_length

        if meshes is not None:
            new_node.meshes = meshes

        if axles is not None:
            new_node.axles = axles

        self._nodes.append(new_node)
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

        # apply prefixes
        name = self._prefix_name(name)

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
        a = self._vfc.new_contactball(name)

        new_node = ContactBall(self, a)

        # and set properties
        if b is not None:
            new_node.parent = b
        if k is not None:
            new_node.k = k
        if radius is not None:
            new_node.radius = radius

        if meshes is not None:
            new_node.meshes = meshes

        self._nodes.append(new_node)
        return new_node

    def new_ballastsystem(self, name, parent: Frame) -> BallastSystem:
        """Creates a new *rigidbody* node and adds it to the scene.

        Args:
            name: Name for the node, should be unique
            parent: name of the parent of the ballast system (ie: the vessel axis system)

        Examples:
            scene.new_ballastsystem("cheetah_ballast", parent="Cheetah")

        Returns:
            Reference to newly created BallastSystem

        """

        # apply prefixes
        name = self._prefix_name(name)

        # check input
        assertValidName(name)
        self._verify_name_available(name)
        b = self._parent_from_node(parent)

        parent = self._parent_from_node(parent)  # handles verification of type as well

        # make elements
        r = BallastSystem(self, parent)
        r.name = name

        self._nodes.append(r)
        return r

    def new_sling(
        self,
        name,
        length=-1,
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

        # apply prefixes
        name = self._prefix_name(name)

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

        self._nodes.append(node)

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

        # apply prefixes
        name = self._prefix_name(name)

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

        a = self._vfc.new_axis(name)

        p = self._vfc.new_poi(name + vfc.VF_NAME_SPLIT + "cog")
        p.parent = a

        g = self._vfc.new_force(name + vfc.VF_NAME_SPLIT + "gravity")
        g.parent = p

        node = Shackle(scene=self, name=name, kind=kind, a=a, p=p, g=g)

        self._nodes.append(node)

        return node

    def print_python_code(self):
        """Prints the python code that generates the current scene

        See also: give_python_code
        """
        for line in self.give_python_code().split("\n"):
            print(line)

    def give_python_code(self):
        """Generates the python code that rebuilds the scene and elements in its current state."""

        import datetime
        import getpass

        self.sort_nodes_by_dependency()

        code = "# auto generated pyhton code"
        try:
            code += "\n# By {}".format(getpass.getuser())
        except:
            code += "\n# By an unknown"

        code += "\n# Time: {} UTC".format(str(datetime.datetime.now()).split(".")[0])

        if self._export_code_with_solved_function:

            code += "\n\n# To be able to distinguish the important number (eg: fixed positions) from"
            code += "\n# non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'."
            code += "\n# For anything written as solved(number) that actual number does not influence the static solution"
            code += "\ndef solved(number):\n    return number\n"

        code += "\n# Environment settings"

        for prop in ds.ENVIRONMENT_PROPERTIES:
            code += f"\ns.{prop} = {getattr(self, prop)}"

        code += "\n"

        for n in self._nodes:

            if n._manager is None:
                code += "\n" + n.give_python_code()
            else:
                if n._manager.creates(n):
                    pass
                else:
                    code += "\n" + n.give_python_code()

                # print(f'skipping {n.name} ')

        # store the visibility code separately

        for n in self._nodes:
            if not n.visible:
                code += f"\ns['{n.name}'].visible = False"  # only report is not the default value

        return code

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

        to_be_printed = []
        for n in self._nodes:
            to_be_printed.append(n.name)

        # to_be_printed.reverse()

        def print_deps(name, spaces):

            node = self[name]
            deps = self.nodes_with_parent(node)
            print(spaces + name + " [" + str(type(node)).split(".")[-1][:-2] + "]")

            if deps is not None:
                for dep in deps:
                    if spaces == "":
                        spaces_plus = " |-> "
                    else:
                        spaces_plus = " |   " + spaces
                    print_deps(dep, spaces_plus)

            to_be_printed.remove(name)

        while to_be_printed:
            name = to_be_printed[0]
            print_deps(name, "")

    def run_code(self, code):
        """Runs the provided code with 's' as self"""

        import DAVE

        locals = DAVE.__dict__
        locals["s"] = self

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

    def import_scene(self, other, prefix="", containerize=True):
        """Copy-paste all nodes of scene "other" into current scene.

        To avoid double names it is recommended to use a prefix. This prefix will be added to all element names.

        Returns:
            Contained (Axis-type Node) : if the imported scene is containerized then a reference to the created container is returned.
        """

        if isinstance(other, Path):
            other = str(other)

        if isinstance(other, str):
            other = Scene(other)

        if not isinstance(other, Scene):
            raise TypeError("Other should be a Scene but is a " + str(type(other)))

        old_prefix = self._name_prefix
        imported_element_names = []

        for n in other._nodes:
            imported_element_names.append(prefix + n.name)

        # check for double names

        for new_node_name in imported_element_names:
            if not self.name_available(new_node_name):
                raise NameError(
                    'An element with name "{}" is already present. Please use a prefix to avoid double names'.format(
                        new_node_name
                    )
                )

        self._name_prefix = prefix

        code = other.give_python_code()

        self.run_code(code)

        self._name_prefix = old_prefix  # restore

        # Move all imported elements without a parent into a newly created axis system
        if containerize:

            container_name = self.available_name_like("import_container")

            c = self.new_frame(prefix + container_name)

            for name in imported_element_names:

                node = self[name]

                if not node.manager:
                    if not hasattr(node, "parent"):
                        continue

                    if node.parent is None:
                        node.change_parent_to(c)

            return c

        return None

    def copy(self):
        """Creates a full and independent copy of the scene and returns it.

        Example:
            s = Scene()
            c = s.copy()
            c.new_frame('only in c')

        """

        c = Scene()
        c.import_scene(self, containerize=False)
        return c

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

    def plot(self, grid_n=100, merge_adjacent_loads=True, filename=None):
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

        ax1.plot(x, m.Vz, "k-", linewidth=linewidth)

        i = np.argmax(np.abs(m.Vz))
        ax1.plot(x[i], m.Vz[i], "b*")
        ax1.text(x[i], m.Vz[i], f"{m.Vz[i]:.2f}")

        ax1.grid()
        ax1.set_title("Shear")
        ax1.set_ylabel("[kN]")

        ax2.plot(x, m.My, "k-", linewidth=linewidth)
        i = np.argmax(np.abs(m.My))
        ax2.plot(x[i], m.My[i], "b*")
        ax2.text(x[i], m.My[i], f"{m.My[i]:.2f}")

        ax2.grid()
        ax2.set_title("Moment")
        ax2.set_ylabel("[kN*m]")

        if filename is None:
            plt.show()
        else:
            fig.savefig(filename)
