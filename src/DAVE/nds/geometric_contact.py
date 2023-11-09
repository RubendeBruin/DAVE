"""Geometric contact between two circles

This is the most complex node in DAVE.

It is not a node itself, so NodePurePython as basis
Is creates and manages a number of nodes, so Container as mix-in

But is  also manages nodes that it does not create, so the standard "Container"
functionality is not sufficient. Therefore, it inherits from Manager directly

It also has a non-standard constructor signature as the circles are a hard requirement.

"""

from .geometry import *
from .abstracts import *


class GeometricContact(
    NodePurePython, Manager, HasParent
):  # Note: can not derive from Container because managed nodes is not equal to created nodes
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

        _axis_on_parent                 : managed    --> aligned with Circle1
            _pin_hole_connection        : managed
                _connection_axial_rotation : managed
                    _axis_on_child      : managed    --> aligned with Circle2
                        Axis2           : managed    , referenced as child_circle_parent_parent
                            Point2      : observed   , referenced as child_circle_parent
                                Circle2 : observed   , referenced as child_circle







    """

    def __init__(self, scene, name, child_circle, parent_circle, inside=True):
        """
        circle1 becomes the nodeB
        circle2 becomes the nodeA

        (attach circle 1 to circle 2)
        Args:
            scene:
            parent_circle:
            child_circle:
            inside:
        """

        scene.assert_name_available(name)

        if child_circle.parent.parent is None:
            raise ValueError(
                "The child circle needs to be located on an axis but is not."
            )

        super().__init__(scene=scene, name=name)

        self._name_prefix = self.name + "/"

        self._parent_circle = parent_circle
        self._parent_circle_parent = parent_circle.parent  # point

        self._child_circle = child_circle
        self._child_circle_parent = child_circle.parent  # point
        self._child_circle_parent_parent = child_circle.parent.parent  # axis

        self._flipped = False
        self._inside_connection = inside

        name_prefix = self._name_prefix  # alias

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

        self._update_connection()

    def dissolve_some(self) -> tuple:
        self.dissolve()
        return True, "Geometric contact dissolved"

    def dissolve(self):
        """Unmanages all created nodes and then deletes itself"""

        with ClaimManagement(self._scene, self):
            for node in self._scene.nodes_managed_by(self):
                node.manager = self.manager

            self._parent_circle.observers.remove(self)
            self._parent_circle_parent.observers.remove(self)

            self._child_circle.observers.remove(self)
            self._child_circle_parent.observers.remove(self)

            self._child_circle_parent_parent._parent_for_code_export = True

        self.__class__ = NodePurePython
        self._scene.delete(self)

    def on_observed_node_changed(self, changed_node):
        self._update_connection()

    def _on_name_changed(self):
        old_prefix = self._name_prefix
        new_prefix = self.name + "/"
        self.helper_update_node_prefix(self.created_nodes(), old_prefix, new_prefix)
        self._name_prefix = new_prefix

    @staticmethod
    def _assert_parent_child_possible(parent, child):
        if parent.parent.parent == child.parent.parent:
            raise ValueError(
                f"A GeometricContact can not be created between two circles on the same axis or body. Both circles are located on {parent.parent.parent}"
            )

    @property
    def child(self) -> Circle:
        """The Circle that is connected to the GeometricContact [Node]

        See Also: parent
        #NOGUI
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
    def parent(self) -> Circle:
        """The Circle that the GeometricConnection is connected to [Node]

        See Also: child
        #NOGUI
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

    @node_setter_manageable
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
        """Update the connection between the two circles"""

        # get current properties
        c_swivel = self.swivel
        c_swivel_fixed = self.swivel_fixed
        c_rotation_on_parent = self.rotation_on_parent
        c_fixed_to_parent = self.fixed_to_parent
        c_child_rotation = self.child_rotation
        c_child_fixed = self.child_fixed

        with ClaimManagement(self._scene, self):
            child_circle = self._child_circle  # nodeB
            parent_circle = self._parent_circle  # nodeA

            if child_circle.parent.parent is None:
                raise ValueError(
                    "The pin that is to be connected is not located on a Frame. Can not create the connection because there is no Frame for nodeB"
                )

            # --------- prepare hole

            if parent_circle.parent.parent is not None:
                self._axis_on_parent.parent = parent_circle.parent.parent
                z = parent_circle.parent.parent.uz
            else:
                z = (0, 0, 1)
            self._axis_on_parent.position = parent_circle.parent.position
            self._axis_on_parent.fixed = (True, True, True, True, True, True)

            # self._axis_on_parent.global_rotation = rotvec_from_y_and_z_axis_direction(parent_circle.global_axis, z)  # this rotation is not unique. It would be nice to have the Z-axis pointing "upwards" as much as possible; especially for the creation of shackles.
            self._axis_on_parent.rotation = rotvec_from_y_and_z_axis_direction(
                parent_circle.axis, (0, 0, 1)
            )  # this rotation is not unique. It would be nice to have the Z-axis pointing "upwards" as much as possible; especially for the creation of shackles.

            # a1 = self._axis_on_parent.uy
            # a2 = parent_circle.global_axis

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
            child_frame = child_circle.parent.parent

            child_frame.parent = self._axis_on_child
            # slaved_axis.rotation = rotation_from_y_axis_direction(-1 * np.array(pin1.axis))

            # the child frame needs to be rotated by the inverse of the circle rotation
            #
            rotation = rotvec_from_y_and_z_axis_direction(
                y=child_circle.axis, z=(0, 0, 1)
            )  # local rotation
            child_frame.rotation = rotvec_inverse(rotation)

            parent_to_point = child_frame.to_glob_direction(
                child_circle.parent.position
            )

            child_frame.position = -np.array(
                self._axis_on_child.to_loc_direction(parent_to_point)
            )

            child_frame.fixed = True

            self._axis_on_child.parent = self._connection_axial_rotation
            self._axis_on_child.rotation = (0, 0, 0)
            self._axis_on_child.fixed = (True, True, True, True, False, True)

            if self._inside_connection:
                # Place the pin in the hole
                self._connection_axial_rotation.rotation = (0, 0, 0)
                self._axis_on_child.position = (
                    parent_circle.radius - child_circle.radius,
                    0,
                    0,
                )

            else:
                # pin-pin connection
                self._axis_on_child.position = (
                    child_circle.radius + parent_circle.radius,
                    0,
                    0,
                )
                self._connection_axial_rotation.rotation = (90, 0, 0)

        # restore settings
        with ClaimManagement(self._scene, self._manager):
            self.swivel = c_swivel
            self.swivel_fixed = c_swivel_fixed
            self.rotation_on_parent = c_rotation_on_parent
            self.fixed_to_parent = c_fixed_to_parent
            self.child_rotation = c_child_rotation
            self.child_fixed = c_child_fixed

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

    def created_nodes(self):
        """Nodes created by the geometric contact - Note that this is different from managed nodes"""
        return (
            self._axis_on_parent,
            self._axis_on_child,
            self._pin_hole_connection,
            self._connection_axial_rotation,
        )

    def creates(self, node: Node):
        return node in self.created_nodes()

    @node_setter_manageable
    def flip(self):
        """Changes the swivel angle by 180 degrees"""
        self.swivel = np.mod(self.swivel + 180, 360)

    # @node_setter_manageable
    def change_side(self):
        self.rotation_on_parent = np.mod(self.rotation_on_parent + 180, 360)
        self.child_rotation = np.mod(self.child_rotation + 180, 360)

    @property
    def swivel(self) -> float:
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
    def swivel_fixed(self) -> bool:
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
    def rotation_on_parent(self) -> float:
        """Angle between the line connecting the centers of the circles and the axis system of the parent node [degrees]"""
        return self._pin_hole_connection.ry

    @rotation_on_parent.setter
    # @node_setter_manageable  (only if dof fixed)
    @node_setter_observable
    def rotation_on_parent(self, value):
        remember = self._scene.current_manager  # claim management
        self._scene.current_manager = self

        if self.fixed_to_parent:
            self._verify_change_allowed()

        self._pin_hole_connection.ry = value

        self._scene.current_manager = remember  # restore old manager

    @property
    def fixed_to_parent(self) -> bool:
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
    def child_rotation(self) -> float:
        """Angle between the line connecting the centers of the circles and the axis system of the child node [degrees]"""
        return self._axis_on_child.ry

    @child_rotation.setter
    # @node_setter_manageable ; only if child_fixed
    @node_setter_observable
    def child_rotation(self, value):
        remember = self._scene.current_manager  # claim management
        self._scene.current_manager = self

        if self.child_fixed:
            self._verify_change_allowed()

        self._axis_on_child.ry = value
        self._scene.current_manager = remember  # restore old manager

    @property
    def child_fixed(self) -> bool:
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
    def inside(self) -> bool:
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

    def inside_child_is_smaller_than_parent(self):
        """Returns True if this is the case, False otherwise. Only valid if connection type is inside"""
        if self.inside and self._child_circle.radius > self._parent_circle.radius:
            return False
        else:
            return True

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
                if (
                    self.swivel_fixed
                    or not self._scene._export_code_with_solved_function
                ):
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
            if self._scene._export_code_with_solved_function:
                code.append(
                    f"                       rotation_on_parent=solved({self.rotation_on_parent}),"
                )
            else:
                code.append(
                    f"                       rotation_on_parent={self.rotation_on_parent},"
                )

        if self.child_fixed:
            code.append(f"                       child_fixed={self.child_fixed},")
            code.append(f"                       child_rotation={self.child_rotation},")
        else:
            if self._scene._export_code_with_solved_function:
                code.append(
                    f"                       child_rotation=solved({self.child_rotation}),"
                )
            else:
                code.append(
                    f"                       child_rotation={self.child_rotation},"
                )

        code = [
            *code[:-1],
            code[-1][:-1] + " )",
        ]  # remove the , from the last entry [should be a quicker way to do this]

        self._scene.current_manager = old_manger

        return "\n".join(code)
