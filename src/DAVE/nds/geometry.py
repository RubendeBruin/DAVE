"""These are the nodes that define the geometry and the degrees of freedom"""
import logging

from .helpers import *
from .abstracts import *
from .mixins import *
from .enums import *
from .base import *
from .mixins import HasParentCore
from .trimesh import TriMeshSource

from ..settings import VF_NAME_SPLIT
from ..tools import *


class Frame(NodeCoreConnected, HasParentCore, HasFootprint):
    """
    Frame

    Frames are the main building blocks of the geometry. They have a position and a rotation in space. Other nodes can be placed on them.
    Frames can be nested by parent/child relationships meaning that an frame can be placed on another frame.
    The possible movements of a frame can be controlled in each degree of freedom using the "fixed" property.

    Frames are also the main building block of inertia.
    Dynamics are controlled using the inertia properties of an frame: inertia [mT], inertia_position[m,m,m] and inertia_radii [m,m,m]


    Notes:
         - circular references are not allowed: It is not allowed to place a on b and b on a

    """

    # _valid_parent_types = [Frame, type(None)]  # defined later in this file

    def __init__(self, scene, name: str):
        assert (
            getattr(self, "_vfNode", None) is None
        ), "A Node is already present in the core, error in constructor sequence?"

        assert scene.name_available(name), f"Name {name} is already taken in scene"

        self._vfNode = scene._vfc.new_axis(name)
        super().__init__(scene=scene, name=name)

        self._inertia = 0
        self._inertia_position = (0, 0, 0)
        self._inertia_radii = (0, 0, 0)

        self._pointmasses = list()
        for i in range(6):
            p = scene._vfc.new_pointmass(
                name + VF_NAME_SPLIT + "pointmass_{}".format(i)
            )
            p.parent = self._vfNode
            self._pointmasses.append(p)
        self._update_inertia()

    def depends_on(self):
        return HasParentCore.depends_on(self)

    def _on_name_changed(self):
        """Update the name of the pointmasses"""
        super()._on_name_changed()

        for i, p in enumerate(self._pointmasses):
            p.name = self.name + VF_NAME_SPLIT + "pointmass_{}".format(i)

    def _delete_vfc(self):
        for p in self._pointmasses:
            if p.name == "":
                raise ValueError(
                    f"Pointmass on node {self.name} has no name, can not be deleted - this is a bug"
                )
            self._scene._vfc.delete(p.name)

        super()._delete_vfc()

    @property
    def warnings(self) -> list[str]:
        """Returns a list of warnings that are present on this node"""
        ws = list(self._vfNode.warnings)

        # check for unsupported dofs
        # if two of the rotational dofs are free and the third is fixed then we have strange rotations
        if len([i for i in self.fixed[3:] if i == False]) == 2:
            ws.append("Frame:100 2 out of 3 rotational dofs are free. This is not recommended")

        return ws


    @property
    def inertia(self) -> float:
        """The linear inertia or 'mass' of the axis [mT]
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
    def inertia_position(self) -> tuple[float, float, float]:
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
    def inertia_radii(self) -> tuple[float, float, float]:
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
    def fixed(self) -> tuple[bool, bool, bool, bool, bool, bool]:
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

    def _getfixed(self, imode):
        return self.fixed[imode]

    def _setfixed(self, imode, value):
        assert isinstance(value, bool), f"Fixed needs to be a boolean, not {value}"
        fixed = list(self.fixed)
        fixed[imode] = value
        self.fixed = fixed

    @property
    def fixed_x(self) -> bool:
        """Restricts/allows movement in x direction of parent"""
        return self.fixed[0]

    @fixed_x.setter
    @node_setter_manageable
    @node_setter_observable
    def fixed_x(self, value):
        self._setfixed(0, value)

    @property
    def fixed_y(self) -> bool:
        """Restricts/allows movement in y direction of parent"""
        return self.fixed[1]

    @fixed_y.setter
    @node_setter_manageable
    @node_setter_observable
    def fixed_y(self, value):
        self._setfixed(1, value)

    @property
    def fixed_z(self) -> bool:
        """Restricts/allows movement in z direction of parent"""
        return self.fixed[2]

    @fixed_z.setter
    @node_setter_manageable
    @node_setter_observable
    def fixed_z(self, value):
        self._setfixed(2, value)

    @property
    def fixed_rx(self) -> bool:
        """Restricts/allows movement about x direction of parent"""
        return self.fixed[3]

    @fixed_rx.setter
    @node_setter_manageable
    @node_setter_observable
    def fixed_rx(self, value):
        self._setfixed(3, value)

    @property
    def fixed_ry(self) -> bool:
        """Restricts/allows movement about y direction of parent"""
        return self.fixed[4]

    @fixed_ry.setter
    @node_setter_manageable
    @node_setter_observable
    def fixed_ry(self, value):
        self._setfixed(4, value)

    @property
    def fixed_rz(self) -> bool:
        """Restricts/allows movement about z direction of parent"""
        return self.fixed[5]

    @fixed_rz.setter
    @node_setter_manageable
    @node_setter_observable
    def fixed_rz(self, value):
        self._setfixed(5, value)

    @node_setter_manageable
    def set_free(self):
        """Sets .fixed to (False,False,False,False,False,False)"""
        self._vfNode.set_free()

    @node_setter_manageable
    def set_fixed(self):
        """Sets .fixed to (True,True,True,True,True,True)"""

        self._vfNode.set_fixed()

    @node_setter_manageable
    def set_even_keel(self):
        """Changes the rotation of the node such that it is 'even-keel'"""
        if self.parent is not None:
            warnings.warn(
                f"Using set_even_keel may not work as expected because frame {self.name} is located on {self.parent.name}"
            )
        self.rotation = (0, 0, self.heading)

    @property
    def x(self) -> float:
        """The x-component of the position vector (parent axis) [m]"""
        return self.position[0]

    @property
    def y(self) -> float:
        """The y-component of the position vector (parent axis) [m]"""
        return self.position[1]

    @property
    def z(self) -> float:
        """The z-component of the position vector (parent axis) [m]"""
        return self.position[2]

    @x.setter
    @node_setter_observable
    def x(self, var):
        if self.fixed[0]:
            self._verify_change_allowed()

        a = self.position
        self.position = (var, a[1], a[2])

    @y.setter
    @node_setter_observable
    def y(self, var):
        if self.fixed[1]:
            self._verify_change_allowed()

        a = self.position
        self.position = (a[0], var, a[2])

    @z.setter
    @node_setter_observable
    def z(self, var):
        if self.fixed[2]:
            self._verify_change_allowed()

        a = self.position
        self.position = (a[0], a[1], var)

    @property
    def position(self) -> tuple[float, float, float]:
        """Position of the axis (parent axis) [m,m,m]

        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)
        """
        return self._vfNode.position

    @position.setter
    @node_setter_observable
    def position(self, var):
        current = self.position

        for i in range(3):
            if self.fixed[i] and abs(current[i] - var[i]) > 1e-6:
                self._verify_change_allowed()

        assert3f(var, "Position ")
        self._vfNode.position = var
        self._scene._geometry_changed()

    @property
    def rx(self) -> float:
        """The x-component of the rotation vector [degrees] (parent axis)"""
        return self.rotation[0]

    @property
    def ry(self) -> float:
        """The y-component of the rotation vector [degrees] (parent axis)"""
        return self.rotation[1]

    @property
    def rz(self) -> float:
        """The z-component of the rotation vector [degrees], (parent axis)"""
        return self.rotation[2]

    @rx.setter
    @node_setter_observable
    def rx(self, var):
        if self.fixed[3]:
            self._verify_change_allowed()

        a = self.rotation
        self.rotation = (var, a[1], a[2])

    @ry.setter
    @node_setter_observable
    def ry(self, var):
        if self.fixed[4]:
            self._verify_change_allowed()

        a = self.rotation
        self.rotation = (a[0], var, a[2])

    @rz.setter
    @node_setter_observable
    def rz(self, var):
        if self.fixed[5]:
            self._verify_change_allowed()

        a = self.rotation
        self.rotation = (a[0], a[1], var)

    @property
    def rotation(self) -> tuple[float, float, float]:
        """Rotation of the frame about its origin as rotation-vector (rx,ry,rz) [degrees].
        Defined as a rotation about an axis where the direction of the axis is (rx,ry,rz) and the angle of rotation is |(rx,ry,rz| degrees.
        These are the expressed on the coordinate system of the parent (if any) or the global axis system (if no parent)
        """
        return tuple(
            [n.item() for n in np.rad2deg(self._vfNode.rotation)]
        )  # convert to float

    @rotation.setter
    @node_setter_observable
    def rotation(self, var):
        # convert to degrees
        assert3f(var, "Rotation")

        current = self.rotation

        for i in range(3):
            if self.fixed[i + 3] and abs(current[i] - var[i]) % 360 > 1e-6:
                self._verify_change_allowed()

        var_rad = np.deg2rad(var)

        self._vfNode.rotation = var_rad
        self._scene._geometry_changed()

    # we need to over-ride the parent property to be able to call _geometry_changed afterwards
    @property
    def parent(self) -> "Frame" or None:
        """Determines the parent of the axis. Should either be another axis or 'None'

        Other axis may be refered to by reference or by name (str). So the following are identical

            p = s.new_frame('parent_axis')
            c = s.new_frame('child axis')

            c.parent = p
            c.parent = 'parent_axis'

        To define that an axis does not have a parent use

            c.parent = None

        """
        return HasParentCore.parent.fget(self)

    @parent.setter
    @node_setter_manageable
    @node_setter_observable
    def parent(self, val):
        val = self._scene._node_from_node_or_str_or_None(val)

        if val == self:
            raise ValueError(f"{self.name} can not be its own parent.")

        if val is not None:
            A = val.name
            B = self.name
            if self._scene._vfc.element_A_depends_on_B(A, B):
                raise ValueError(
                    f"Setting {val.name} as parent of {self.name} would create a circular dependency, that is not allowed"
                )

        HasParentCore.parent.fset(self, val)
        self._scene._geometry_changed()

    @property
    def gx(self) -> float:
        """The x-component of the global position vector [m] (global axis )"""
        return self.global_position[0]

    @property
    def gy(self) -> float:
        """The y-component of the global position vector [m] (global axis )"""
        return self.global_position[1]

    @property
    def gz(self) -> float:
        """The z-component of the global position vector [m] (global axis )"""
        return self.global_position[2]

    @gx.setter
    @node_setter_observable
    def gx(self, var):
        a = self.global_position
        self.global_position = (var, a[1], a[2])

    @gy.setter
    @node_setter_observable
    def gy(self, var):
        a = self.global_position
        self.global_position = (a[0], var, a[2])

    @gz.setter
    @node_setter_observable
    def gz(self, var):
        a = self.global_position
        self.global_position = (a[0], a[1], var)

    @property
    def global_position(self) -> tuple[float, float, float]:
        """The global position of the origin of the axis system  [m,m,m] (global axis)"""
        return self._vfNode.global_position

    @global_position.setter
    @node_setter_observable
    def global_position(self, val):
        assert3f(val, "Global Position")
        if self.parent:
            self.position = self.parent.to_loc_position(val)
        else:
            self.position = val

    @property
    def grx(self) -> float:
        """The x-component of the global rotation vector [degrees] (global axis)"""
        return self.global_rotation[0]

    @property
    def gry(self) -> float:
        """The y-component of the global rotation vector [degrees] (global axis)"""
        return self.global_rotation[1]

    @property
    def grz(self) -> float:
        """The z-component of the global rotation vector [degrees] (global axis)"""
        return self.global_rotation[2]

    @grx.setter
    @node_setter_observable
    def grx(self, var):
        a = self.global_rotation
        self.global_rotation = (var, a[1], a[2])

    @gry.setter
    @node_setter_observable
    def gry(self, var):
        a = self.global_rotation
        self.global_rotation = (a[0], var, a[2])

    @grz.setter
    @node_setter_observable
    def grz(self, var):
        a = self.global_rotation
        self.global_rotation = (a[0], a[1], var)

    @property
    def tilt_x(self) -> float:
        """Tilt about local x-axis [deg]
        This is the arc-sin of the z-component of the unit y vector.

        See Also: heel, tilt_y
        """
        y = (0, 1, 0)
        uy = self.to_glob_direction(y)
        return np.rad2deg(np.arcsin(uy[2]))

    @property
    def tilt_x_opposite(self) -> float:
        """Tilt about local NEGATIVE x-axis [deg]

        See Also: heel, tilt_y, tilt_x
        """
        return -self.tilt_x

    @property
    def tilt_y_opposite(self) -> float:
        """Tilt about local NEGATIVE y-axis [deg]

        See Also: heel, tilt_y, tilt_x
        """
        return -self.tilt_y

    @property
    def heel(self) -> float:
        """Heel in degrees. SB down is positive [deg]
        This is the inverse sin of the unit y vector(= tiltx)

        See also: tilt_x
        """
        angle = self.tilt_x

        if self.uz[2] < 0:  # rotation beyond 90 or -90 degrees
            if angle < 0:
                angle = -180 - angle
            else:
                angle = 180 - angle

        return angle

    @property
    def tilt_y(self) -> float:
        """Tilt about local y-axis [deg]

        This is arc-sin of the z-component of the unit -x vector.
        So a positive rotation about the y axis results in a positive tilt_y.

        See Also: trim
        """
        x = (-1, 0, 0)
        ux = self.to_glob_direction(x)
        return np.rad2deg(np.arcsin(ux[2]))

    @property
    def trim(self) -> float:
        """Trim in degrees. Bow-down is positive [deg]

        This is the inverse sin of the unit -x vector(= tilt_y)

        See also: tilt_y
        """
        return self.tilt_y

    @property
    def heading(self) -> float:
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
    def heading_compass(self) -> float:
        """The heading (0..360)[deg] assuming that the global y-axis is North and global x-axis is East and rotation according compass definition"""
        return np.mod(90 - self.heading, 360)

    @property
    def global_rotation(self) -> tuple[float, float, float]:
        """Rotation vector [deg,deg,deg] (global axis)"""
        return tuple(np.rad2deg(self._vfNode.global_rotation))

    @global_rotation.setter
    @node_setter_observable
    def global_rotation(self, val):
        assert3f(val, "Global Rotation")
        if self.parent:
            self.rotation = self.parent.to_loc_rotation(val)
        else:
            self.rotation = val

    @property
    def global_transform(
        self,
    ) -> tuple[
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
    ]:
        """Read-only: The global transform of the axis system [matrix]
        #NOGUI"""
        return self._vfNode.global_transform

    @property
    def connection_force(self) -> tuple[float, float, float, float, float, float]:
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
    def connection_force_x(self) -> float:
        """The x-component of the connection-force vector [kN] (Parent axis)"""
        return self.connection_force[0]

    @property
    def connection_force_y(self) -> float:
        """The y-component of the connection-force vector [kN] (Parent axis)"""
        return self.connection_force[1]

    @property
    def connection_force_z(self) -> float:
        """The z-component of the connection-force vector [kN] (Parent axis)"""
        return self.connection_force[2]

    @property
    def connection_moment_x(self) -> float:
        """The mx-component of the connection-force vector [kNm] (Parent axis)"""
        return self.connection_force[3]

    @property
    def connection_moment_y(self) -> float:
        """The my-component of the connection-force vector [kNm] (Parent axis)"""
        return self.connection_force[4]

    @property
    def connection_moment_z(self) -> float:
        """The mx-component of the connection-force vector [kNm] (Parent axis)"""
        return self.connection_force[5]

    @property
    def applied_force(self) -> tuple[float, float, float]:
        """The force and moment that is applied on origin of this axis [kN, kN, kN, kNm, kNm, kNm] (Global axis)"""
        return self._vfNode.applied_force

    @property
    def ux(self) -> tuple[float, float, float]:
        """The unit x axis [m,m,m] (Global axis)"""
        return self.to_glob_direction((1, 0, 0))

    @property
    def uy(self) -> tuple[float, float, float]:
        """The unit y axis [m,m,m] (Global axis)"""
        return self.to_glob_direction((0, 1, 0))

    @property
    def uz(self) -> tuple[float, float, float]:
        """The unit z axis [m,m,m] (Global axis)"""
        return self.to_glob_direction((0, 0, 1))

    @property
    def equilibrium_error(self) -> tuple[float, float, float, float, float, float]:
        """The remaining force and moment on this axis. Should be zero when in equilibrium [kN,kN,kN,kNm,kNm,kNm] (applied-force minus connection force, Parent axis)"""
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

        from DAVE import LoadShearMomentDiagram

        return LoadShearMomentDiagram(lsm)

    @node_setter_manageable
    def change_parent_to(self, new_parent):
        """Assigns a new parent to the node but keeps the global position and rotation the same.

        See also: .parent (property)

        Args:
            new_parent: new parent node

        """

        glob_pos = self.global_position
        glob_rot = self.global_rotation

        self.parent = new_parent  # all checks are preformed here

        self.global_position = glob_pos
        self.global_rotation = glob_rot

    def _can_dissolve(self, allowed_managers=(None,)) -> tuple:
        # Frames can only be dissolved when they are fixed
        if not all(self.fixed):
            return False, "This node has degrees of freedom"

        # All nodes depending on this Frame need to be able to function
        # without it.
        # That is possible if they have this node as parent and that parent is this node.
        for node_name in self._scene.nodes_depending_on(self, recursive=False):
            node = self._scene[node_name]
            parent = getattr(
                node, "parent", -1
            )  # -1 is a dummy value, None is a valid parent
            if parent is not self:
                return False, f"Node {node_name} can not function without this node."

            if node.manager not in allowed_managers:
                # It could be that the manager itself has a parent property and changes the parent of the node when it is changed.
                # this whole next part of code handles cases like that. One of the unit-checks that depends on this part of the
                # code is the "test_dissolve_filled_standard_equipment" from the SuperElements test suite.

                if getattr(node.manager, "parent", None) == self:
                    # We're not sure that this will fail, but we can't be sure that it will succeed either.
                    # so let's check using a dummy
                    s = self._scene
                    dummy = s.new_frame(s.available_name_like("dummy"))

                    if node.manager.manager is not None:
                        if node.manager.manager != self:
                            return (
                                False,
                                f"Node {node_name} on this node can not be moved to another parent because it is managed by {node.manager.name}.",
                            )

                    old_manager = self._scene.current_manager
                    self._scene.current_manager = self

                    node.manager.parent = dummy
                    if node.parent == dummy:
                        pass  # ok
                    else:
                        node.manager.parent = self  # resTore
                        s.delete(dummy)
                        self._scene.current_manager = old_manager
                        return (
                            False,
                            f"Node {node_name} on this node can not be moved to another parent because it is managed by {node.manager.name}.",
                        )

                    node.manager.parent = self  # resTore
                    s.delete(dummy)
                    self._scene.current_manager = old_manager

                    # -------------

                else:
                    # can not change the parent of this node
                    return (
                        False,
                        f"Node {node_name} on this node can not be moved to another parent because it is managed by {node.manager.name}.",
                    )

            none_parent_acceptable = getattr(node, "_None_parent_acceptable", True)
            if (
                self.parent is None and not none_parent_acceptable
            ):  # Trimesh based nodes do not accept None as parent
                return (
                    False,
                    f"Node {node_name} on this node needs to have a parent other than None.",
                )

        return True, ""

    def dissolve_some(self) -> tuple:
        """Dissolves the node and removes it from the scene. All children will be assigned to the parent of this node.

        There is some difficult logic involved with managed nodes, especially for the weird case where both the manager
        itself as well as a node that it manages show up as direct dependants of the node that is being dissolved. For
        example a WindAreaPoint.
        """

        work_done = False
        msg = ""

        # Frames can only be dissolved when they are fixed
        if not all(self.fixed):
            msg = f"Node {self.name} has degrees of freedom and can therefore not be dissolved\n"
        else:
            for node_name in self._scene.nodes_depending_on(self, recursive=False):
                node = self._scene[node_name]
                if node.manager is None:
                    if node.try_swap(self, self.parent):
                        work_done = True
                        if self.parent:
                            msg += f"Node {node_name} was moved to parent {self.parent.name}\n"
                        else:
                            msg += f"Node {node_name} was moved to parent None\n"
                    else:
                        msg += f"Node {node_name} could not be relocated\n"

        other_done, other_msg = super().dissolve_some()

        work_done = work_done or other_done
        msg = "\n".join([msg, other_msg]) if msg else other_msg

        return work_done, msg
        #
        # can, reason = self._can_dissolve()
        # if not can:
        #     return False, reason
        #
        # # All checks passed, we can dissolve this node
        # for node_name in (self._scene.nodes_depending_on(self)):
        #     node = self._scene[node_name]
        #
        #     # could be a managed node of which the parent is changed by the manager which itself is one of the nodes
        #     # of which the parent will be changed.
        #     if node.manager is None or node.manager == self._scene.current_manager:
        #         node.parent = self.parent
        #
        # # Check that we have indeed fixed all the dependencies, we've only checked for
        # # "parent" and assumed that changing the parent removes the dependancy.
        # # In the future there could be node-types that have other dependancies as well
        #
        # for node_name in (self._scene.nodes_depending_on(self)):
        #     raise ValueError(f'After changing parent, node {node_name} still depends on {self.name} - can not dissolve')
        #
        # self._scene.delete(self)
        # return True, ""

    def dissolve(self):
        work_done = True
        msg = ""

        while work_done:
            work_done, msg = self.dissolve_some()
            if work_done:
                self._partially_dissolved = True

        if not self._scene.nodes_depending_on(self):
            self._scene.delete(self)
        else:
            raise ValueError(
                f"Node {self.name} can not be dissolved because it still has dependants: {self._scene.nodes_depending_on(self)} , last message was: {msg}"
            )

    def same_position_and_orientation(self, other, tol=1e-9):
        """Compares the global position and rotation of this node with another node. Returns True if they are the same within the given tolerance."""

        if other is None:
            position = np.zeros(3)
            rotation = np.zeros(3)
        else:
            position = other.global_position
            rotation = other.global_rotation

        if not np.allclose(self.global_position, position, atol=tol):
            return False

        if not np.allclose(self.global_rotation, rotation, atol=tol):
            return False

        return True

    def _export_frame_property_code(self) -> str:
        # position
        code = ""

        if self._scene._export_code_with_solved_function:
            # export solved numbers using the "solved" function with full decimal precision
            # export fixed numbers using 6 decimals

            # position

            if self.fixed[0]:
                code += "\n           position=({:.6g},".format(self.position[0])
            else:
                code += "\n           position=(solved({}),".format(self.position[0])
            if self.fixed[1]:
                code += "\n                     {:.6g},".format(self.position[1])
            else:
                code += "\n                     solved({:}),".format(self.position[1])
            if self.fixed[2]:
                code += "\n                     {:.6g}),".format(self.position[2])
            else:
                code += "\n                     solved({:})),".format(self.position[2])

            # rotation
            if self.fixed[3]:
                code += "\n           rotation=({:.6g},".format(self.rotation[0])
            else:
                code += "\n           rotation=(solved({:.6g}),".format(
                    self.rotation[0]
                )
            if self.fixed[4]:
                code += "\n                     {:.6g},".format(self.rotation[1])
            else:
                code += "\n                     solved({:.6g}),".format(
                    self.rotation[1]
                )
            if self.fixed[5]:
                code += "\n                     {:.6g}),".format(self.rotation[2])
            else:
                code += "\n                     solved({:.6g})),".format(
                    self.rotation[2]
                )

        else:
            code += "\n           position=({}, {}, {}),".format(*self.position)
            code += "\n           rotation=({}, {}, {}),".format(*self.rotation)

        if np.any(self.inertia_radii):
            code += "\n           inertia_radii = ({}, {}, {}),".format(
                *self.inertia_radii
            )

        code += "\n           fixed =({}, {}, {}, {}, {}, {}),".format(*self.fixed)

        return code

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\ns.new_frame(name='{}',".format(self.name)
        if self.parent_for_export:
            code += "\n           parent='{}',".format(self.parent_for_export.name)

        code += self._export_frame_property_code()

        code += "\n            )"

        code += self.add_footprint_python_code()

        return code


Frame._valid_parent_types = (
    Frame,
    type(None),
)  # can only be exectuted after Frame class has been defined


class Point(NodeCoreConnected, HasParentCore, HasFootprint):
    """A location on an axis"""

    _valid_parent_types = (Frame, type(None))

    # init parent and name are fully derived from NodeWithParent
    # _vfNode is a poi
    def __init__(self, scene, name: str):
        logging.info("Point.__init__")
        scene.assert_name_available(name)

        self._vfNode = scene._vfc.new_poi(name)
        super().__init__(scene=scene, name=name)

    def change_parent_to(self, new_parent):
        gpos = self.global_position
        self.parent = new_parent
        self.global_position = gpos

    def depends_on(self) -> list:
        return HasParentCore.depends_on(self)

    @property
    def x(self) -> float:
        """x component of local position [m] (parent axis)"""
        return self.position[0]

    @property
    def y(self) -> float:
        """y component of local position [m] (parent axis)"""
        return self.position[1]

    @property
    def z(self) -> float:
        """z component of local position [m] (parent axis)"""
        return self.position[2]

    @property
    def applied_force(self) -> tuple[float, float, float]:
        """Applied force [kN,kN,kN] (parent axis)"""
        force = self.applied_force_and_moment_global[:3]
        if self.parent:
            return self.parent.to_loc_direction(force)
        else:
            return force

    @property
    def force(self) -> float:
        """total force magnitude as applied on the point [kN]"""
        return np.linalg.norm(self.applied_force)

    @property
    def fx(self) -> float:
        """x component of applied force [kN] (parent axis)"""
        return self.applied_force[0]

    @property
    def fy(self) -> float:
        """y component of applied force [kN] (parent axis)"""
        return self.applied_force[1]

    @property
    def fz(self) -> float:
        """z component of applied force [kN] (parent axis)"""
        return self.applied_force[2]

    @property
    def applied_moment(self) -> tuple[float, float, float]:
        """Applied moment [kNm,kNm,kNm] (parent axis)"""
        force = self.applied_force_and_moment_global[3:]
        if self.parent:
            return self.parent.to_loc_direction(force)
        else:
            return force

    @property
    def moment(self) -> float:
        """total moment magnitude as applied on the point [kNm]"""
        return np.linalg.norm(self.applied_moment)

    @property
    def mx(self) -> float:
        """x component of applied moment [kNm] (parent axis)"""
        return self.applied_moment[0]

    @property
    def my(self) -> float:
        """y component of applied moment [kNm] (parent axis)"""
        return self.applied_moment[1]

    @property
    def mz(self) -> float:
        """z component of applied moment [kNm] (parent axis)"""
        return self.applied_moment[2]

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
    def position(self) -> tuple[float, float, float]:
        """Local position [m,m,m] (parent axis)"""
        return self._vfNode.position

    @position.setter
    @node_setter_manageable
    @node_setter_observable
    def position(self, new_position):
        assert3f(new_position)
        self._vfNode.position = new_position

    @property
    def applied_force_and_moment_global(
        self,
    ) -> tuple[float, float, float, float, float, float]:
        """Applied force and moment on this point [kN, kN, kN, kNm, kNm, kNm] (Global axis)"""
        return self._vfNode.applied_force

    @property
    def gx(self) -> float:
        """x component of position [m] (global axis)"""
        return self.global_position[0]

    @property
    def gy(self) -> float:
        """y component of position [m] (global axis)"""
        return self.global_position[1]

    @property
    def gz(self) -> float:
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
    def global_position(self) -> tuple[float, float, float]:
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

        code += "\n          position=({:.6g},".format(self.position[0])
        code += "\n                    {:.6g},".format(self.position[1])
        code += "\n                    {:.6g}))".format(self.position[2])

        code += self.add_footprint_python_code()

        return code


class Circle(NodeCoreConnected, HasParentCore):
    """A Circle models a circle shape based on a diameter and an axis direction. Circles can be used by
    geometric contact nodes and cables/slings. For cables the direction of the axis determines the
    direction about which the cable runs over the sheave."""

    _valid_parent_types = (Point,)

    def __init__(self, scene, name):
        logging.info("Circle.__init__")

        scene._verify_name_available(name)
        self._vfNode = scene._vfc.new_circle(name)

        self.draw_start = -1
        self.draw_stop = 1

        super().__init__(scene=scene, name=name)

    def depends_on(self) -> list:
        return HasParentCore.depends_on(self)

    @property
    def axis(self) -> tuple[float, float, float]:
        """Direction of the sheave axis (parent axis system) [m,m,m]

        Note:
            The direction of the axis is also used to determine the positive direction over the circumference of the
            circle. This is then used when cables run over the circle or the circle is used for geometric contacts. So
            if a cable runs over the circle in the wrong direction then a solution is to change the axis direction to
            its opposite:  circle.axis =- circle.axis. (another solution in that case is to define the connections of
            the cable in the reverse order)
        """
        ad = self._vfNode.axis_direction
        l = np.linalg.norm(ad)
        if l == 0:
            return ad
        else:
            return (ad[0] / l, ad[1] / l, ad[2] / l)

    @axis.setter
    @node_setter_manageable
    @node_setter_observable
    def axis(self, val):
        assert3f(val)
        if np.linalg.norm(val) == 0:
            raise ValueError("Axis can not be 0,0,0")
        self._vfNode.axis_direction = val

    @property
    def radius(self) -> float:
        """Radius of the circle [m]"""
        return self._vfNode.radius

    @radius.setter
    @node_setter_manageable
    @node_setter_observable
    def radius(self, val):
        assert1f(val)
        self._vfNode.radius = val

    @property
    def is_roundbar(self) -> bool:
        """Flag to indicate that the circle should be treated as round-bar [true/false]"""
        return self._vfNode.is_roundbar

    @is_roundbar.setter
    def is_roundbar(self, value):
        # See issue 144
        # we should prohibit changing the type of a circle when it is in use.
        deps = self._scene.nodes_depending_on(self)
        if deps:
            raise ValueError(
                f"Can not change the type of a circle when it is in use. The following nodes depend on this circle: {deps}"
            )
        self._vfNode.is_roundbar = value

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\nc = s.new_circle(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent_for_export.name)
        code += "\n            axis=({:.6g}, {:.6g}, {:.6g}),".format(*self.axis)
        if self.is_roundbar:
            code += "\n            roundbar=True,"
        code += "\n            radius={:.6g} )".format(self.radius)

        if self.draw_start != -1:
            code += f"\nc.draw_start = {self.draw_start}"
        if self.draw_stop != 1:
            code += f"\nc.draw_stop = {self.draw_stop}"

        return code

    @property
    def global_position(self) -> tuple[float, float, float]:
        """Global position of the center of the sheave [m,m,m]

        Note: this is the same as the global position of the parent point.
        """
        return self.parent.global_position

    @property
    def global_axis(self) -> tuple[float, float, float]:
        """Global axis direction [m,m,m]"""
        if self.parent.parent is not None:
            return self.parent.parent.to_glob_direction(self.axis)
        else:
            return self.axis

    @global_axis.setter
    def global_axis(self, value):
        assert3f(value, "axis")

        if self.parent.parent is not None:
            self.axis = self.parent.parent.to_loc_direction(value)
        else:
            self.axis = value

    @property
    def position(self) -> tuple[float, float, float]:
        """Local position of the center of the sheave [m,m,m] (parent axis).

        Note: this is the same as the local position of the parent point.
        """
        return self.parent.position

    @node_setter_manageable
    def change_parent_to(self, new_parent):
        """Assigns a new parent to the node but keeps the global position and rotation the same.

        See also: .parent (property)

        Args:
            new_parent: new parent node

        """
        glob_axis = self.global_axis

        move = np.linalg.norm(
            np.array(self.global_position) - np.array(new_parent.global_position)
        )
        if move > 1e-7:
            raise ValueError(
                "Global position of new parent must be the same as the global position of the node"
            )

        self.parent = new_parent
        self.global_axis = glob_axis
