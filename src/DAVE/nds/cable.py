import warnings
from contextlib import contextmanager

import numpy as np

from .abstracts import NodeCoreConnected
from .core import DEFAULT_WINDING_ANGLE
from .helpers import *
from .geometry import Point, Circle
from ..settings import (
    VF_NAME_SPLIT,
    RENDER_CURVE_RESOLUTION,
    RENDER_CATENARY_RESOLUTION,
)
from ..tools import assert1f_positive_or_zero, assertBool
from ..visual_helpers.constants import RESOLUTION_CABLE_SAG, RESOLUTION_CABLE_OVER_CIRCLE

@contextmanager
def non_sticky_cable(cable: "Cable"):
    """Provides a non-sticky version of the cable.
    If the cable is stick, then a non-sticky copy is made and deleted.
    If the cable is non-sticky, this just yields the cable itself."""

    dummy_cable = False

    if not cable.is_sticky:
        yield cable

    else:

        try:
            available_name = cable._scene.available_name_like("dummy_cable")
            dummy_cable = Cable(scene=cable._scene, name=available_name)

            dummy_cable.connections = cable.connections
            dummy_cable.reversed = cable.reversed
            dummy_cable.max_winding_angles = cable.max_winding_angles
            dummy_cable.offsets = cable.offsets

            dummy_cable.EA = 0
            dummy_cable.Length = 0
            dummy_cable.diameter = cable.diameter

            dummy_cable._vfNode.update()

            yield dummy_cable

        finally:
            if dummy_cable:
                cable._scene.delete(dummy_cable)


class Cable(NodeCoreConnected):
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

    # We inherit from NodeCoreConnected, but we contain more than one node
    # so we need to override the _vfNode property to return the first cable node (which is always there)


    @property
    def _vfNode(self):
        return self._vfCableNodes[0]

    def __init__(self, scene, name: str):
        scene.assert_name_available(name)

        _vfNode = scene._vfc.new_cable(name)
        self._vfCableNodes = list()
        self._vfPoiNodes = dict()
        self._vfCableNodes = [_vfNode]

        super().__init__(scene=scene, name=name)

        # These are the user-defined connections and connection properties
        # all except friction are aligned.
        # they are synchronized in length by the _synchronize_connection_definition_vector_lengths_to_connections method
        self._pois = list()
        self._reversed: list[bool] = list()
        self._max_winding_angle: list[float] = list()
        self._offsets: list[float] = list()
        self._sticky: list[tuple or float or None] = list()
        self._friction: list[float] = list()   # length of friction is one or two less than pois


        # scalar properties
        self._length = 1
        self._EA = 0
        self._diameter = 0
        self._mass_per_length = 0

        # visual settings
        self._render_as_tube = True
        self.do_color_by_tension = True

    def depends_on(self):
        return [*self._pois]

    def _delete_vfc(self):
        names_to_be_deleted = []
        for n in self._vfCableNodes:
            names_to_be_deleted.append(n.name)
        for n in self._vfPoiNodes.values():
            names_to_be_deleted.append(n.name)

        for name in names_to_be_deleted:
            self._scene._vfc.delete(name)

        self._vfCableNodes.clear()
        self._vfPoiNodes.clear()

        self.invalidate()

    @property
    def sticky(self) -> tuple[float or None or tuple[float, float]]:
        """Positions at which the connections stick to the cable. Aligned with connections.
        None means no sticky connection,
        a value between 0 and 1 defines the position of the cable (as fraction of the cable length) at which the cable sticks
        if the connection is a circle then the sticky data needs to be a tuple of which the second entry is the 3d location defining
        the point at the circumference of the circle that cable point sticks to. This point does not need to be exactly on the circle
        as long as it is not on the axis.
        """
        return tuple(self._sticky)

    @sticky.setter
    def sticky(self, value):
        self._check_sticky(value)
        self._sticky = list(value)

        self._update_vfNodes()

    @property
    def is_sticky(self) -> bool:
        """True if any of the connections is sticky [bool]"""

        return any([s is not None for s in self._sticky])


    def _check_sticky(self, value):
        # check values
        #
        # length should be the same as the number of connections

        connections = self.connections # alias

        if len(value) != len(connections):
            raise ValueError(f"Length of sticky should be the same as the number of connections ({len(connections)})")

        for i, v in enumerate(value):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                if v < 0 or v > 1:
                    raise ValueError(f"Sticky value should be between 0 and 1, but {v} is not")

                if not isinstance(connections[i], Point):
                    raise ValueError(f"Sticky value for connection {i} is for a Point, but connection is not a Point but a {type(connections[i])}")

            elif isinstance(v, tuple):
                if len(v) != 2:
                    raise ValueError(f"Sticky value should be a tuple of 2 values, but {v} is not")
                if not isinstance(v[0], (int, float)):
                    raise ValueError(f"First value of sticky tuple should be a float, but {v[0]} is not")
                if not isinstance(v[1], (int, float)):
                    raise ValueError(f"Second value of sticky tuple should be a float, but {v[1]} is not")

                if not isinstance(connections[i], Circle):
                    raise ValueError(f"Sticky value for connection {i} is for a Circle, but connection is not a Circle but a {type(connections[i])}")

                if connections[i].is_roundbar:
                    raise ValueError(f"Sticky value for connection {i} tries to stick to a roundbar, but roundbars can not be made sticky")

            else:
                raise ValueError(f"Sticky value should be None, a float or a tuple, but {v} is a {type(v)}")





    @property
    def tension(self) -> float:
        """Tension in the cable [kN]
        Highest tension in the cable"""
        t = 0
        for n in self._vfCableNodes:
            t = max(t, n.tension)
        return t

    @property
    def stretch(self) -> float:
        """Stretch of the cable [m]"""
        s = 0
        for n in self._vfCableNodes:
            s += n.stretch
        return s

    @property
    def actual_length(self) -> float:
        """Current length of the cable: length + stretch [m]"""
        return self.length + self.stretch

    @property
    def length(self) -> float:
        """Length of the cable when in rest [m]"""
        return self._length


    @length.setter
    @node_setter_manageable
    @node_setter_observable
    def length(self, val):
        if val < 1e-9:
            if self.EA > 0:
                raise ValueError(
                    f"Can not set length of {self.label} to {val}.\nLength shall be more than 0 if EA>0 (otherwise stiffness EA/L becomes infinite)"
                )
        if val < 0:
            raise ValueError(
                f"Can not set length of {self.label} to {val}.\nLength shall be more than 0"
            )
        self._length = val
        self._update_vfCable_scalar_properties()

    @property
    def EA(self) -> float:
        """Stiffness of the cable [kN]"""
        return self._EA

    @EA.setter
    @node_setter_manageable
    @node_setter_observable
    def EA(self, ea):
        assert1f_positive_or_zero(ea, "EA")

        if ea > 0 and self.length < 1e-9:
            raise ValueError(
                f"Can not set EA of {self.label} to {ea}.\nLength shall be more than 0 if EA>0 (otherwise stiffness EA/L becomes infinite)"
            )

        self._EA = ea
        self._update_vfCable_scalar_properties()


    @property
    def diameter(self) -> float:
        """Diameter of the cable. Used when a cable runs over a circle. [m]"""
        return self._diameter

    @diameter.setter
    @node_setter_manageable
    @node_setter_observable
    def diameter(self, diameter):
        assert1f_positive_or_zero(diameter, "diameter")
        self._diameter = diameter
        self._update_vfCable_scalar_properties()

    @property
    def mass_per_length(self) -> float:
        """Mass per length of the cable [mT/m]"""
        return self._mass_per_length

    @mass_per_length.setter
    @node_setter_manageable
    @node_setter_observable
    def mass_per_length(self, mass_per_length):
        assert1f_positive_or_zero(mass_per_length, "mass_per_length")
        self._mass_per_length = mass_per_length
        self._update_vfCable_scalar_properties()

    @property
    def mass(self) -> float:
        """Mass of the cable (derived from length and mass-per-length) [mT]"""
        return self._vfNode.mass_per_length * self.length

    @mass.setter
    @node_setter_manageable
    @node_setter_observable
    def mass(self, mass):
        self._vfNode.mass_per_length = mass / self.length

    @property
    def reversed(self) -> tuple[bool, ...]:
        """Diameter of the cable. Used when a cable runs over a circle. [m]"""
        return tuple(self._reversed)

    @reversed.setter
    @node_setter_manageable
    @node_setter_observable
    def reversed(self, reversed):
        self._reversed = list(reversed)
        self._update_vfNodes()

    @property
    def _isloop(self):
        """True if the cable is a loop"""
        if len(self.connections) < 2:
            return False
        if self.connections[0] == self.connections[-1]:
            if not self._vfCableNodes: # no cable nodes defined
                return True
            else:
                return not self._vfNode.explicit_cable_no_loop
        return False


    def _set_no_loop(self):
        """Set the cable to be a non-loop explicitly - this overrules the normal behaviour"""
        cable_was_loop = self._isloop

        for n in self._vfCableNodes:
            n.explicit_cable_no_loop = True

        if cable_was_loop:
            # update friction
            self.friction = [f for f in self._friction if f is not None]
            self._update_vfNodes()

    def _unset_no_loop(self):
        """Remove the flag that sets the cable to be a loop explicitly - returning to normal behaviour"""
        for n in self._vfCableNodes:
            n.explicit_cable_no_loop = False

    @property
    def solve_segment_lengths(self) -> bool:
        """If True then lengths of the segment are solved for a continuous tension distribution including weight. If false then the segment lengths are determined only on the geometry [bool]
        Note that the solution is typically not unique!"""
        if self.sticky:
            return False
        return self._vfNode.solve_section_lengths

    @solve_segment_lengths.setter
    def solve_segment_lengths(self, value):
        assertBool(value, "solve_segment_lengths")
        if value and self.sticky:
            raise ValueError("Solve segment lengths is implemented in combination with sticky")
        self._vfNode.solve_section_lengths = value

    @property
    def segment_lengths(self) -> tuple[float]:
        """If EA>0: Length of material in each of the segments [m,...]
        If EA==0: Stretched lengths of the cable between each of the connections [m,...]
        This includes the sections on connections. The first entry is the length _on_ the first connection.
        Sections on a Point have length 0.
        A non-zero first entry means that the cable is a loop starting/ending with a circle, the value then represents the length of cable on the circle.
        """

        with non_sticky_cable(self) as non_sticky:
            return non_sticky._vfNode.material_lengths

    @property
    def material_lengths(self) -> tuple[float]:
        """Length of material in each of the segments [m,...]

        Amount of cable material in each of the segments.
        Segments are:
        - parts on a circle
        - parts between two connections

        If the cable is a loop and the connection entry is a circle, then the first entry is the length of cable material on that first circle.
        Otherwise the first entry is the length of cable material between the first two connections.

        See Also: segment_lengths
        """

        result = self.segment_lengths
        if self._isloop:
            if isinstance(self.connections[0], Point):
                result = result[1:]

        return result

    @property
    def connected_bars_active(self) -> tuple[bool]:
        """True if the i-th bar is active False if the bar is not active [bool,...]"""
        all = []

        for n in self._vfCableNodes:
            ab = n.connected_bar_active
            all.extend(ab)

        return tuple(all)


    @property
    def material_lengths_no_bars(self) -> tuple[float]:
        """Length of material in each of the segments [m,...] ignoring bars

        Amount of cable material in each of the segments.
        Segments are:
        - parts on a circle
        - parts between two connections

        If the cable is a loop and the connection entry is a circle, then the first entry is the length of cable material on that first circle.
        Otherwise the first entry is the length of cable material between the first two connections.

        Bars are excluded from the calculation. If a bar is present, then the length on the bar and the two adjacent
        free sections are merged into a single section.

        See Also: segment_lengths, material_lengths
        """

        all_segments = list(self.material_lengths)

        active_bars = list(self.connected_bars_active)

        if self._isloop:
            cons = self.connections[:-1]
        else:
            cons = self.connections

        results = []

        for c in cons:
            if isinstance(c, Point):
                results.append(all_segments.pop(0)) # segment after the point
            if isinstance(c, Circle):
                if c.is_roundbar:
                    active = active_bars.pop(0)
                    if active:
                        results[-1] += all_segments.pop(0) + all_segments.pop(0)  # segment on the bar and the following segment
                    else:
                        pass # not present in the results
                else:
                    results.append(all_segments.pop(0)) # segment on the circle
                    results.append(all_segments.pop(0))  # segment after the circle

        return tuple(results)











    @property
    def friction(self) -> tuple[float]:
        """Friction factors at the connections [-]"""
        return tuple(self._friction)

    # note: not managed because it is technically a DOF (and we need it in rigging variations)
    @friction.setter
    @node_setter_observable
    def friction(self, friction):
        if isinstance(friction, (float, int)):
            friction = [friction]

        # check length
        req_len = len(self._pois) - 2
        if self._isloop:
            req_len += 1
        assert (
            len(friction) == req_len
        ), f"Friction should be defined for {req_len} connections, got {len(friction)}."

        if self._isloop and not self.is_sticky:
            assert (
                list(friction).count(None) == 1
            ), f"When defining friction for a loop, exactly of the frictions should be 'None'. The friction at that last connection is calculated from the other frictions. Received: {friction}"

            # the None friction shall not be on a roundbar
            index = friction.index(None)
            connection = self.connections[index]
            if isinstance(connection, Circle):
                if connection.is_roundbar:
                    raise ValueError(
                        f"Defining the unknown friction for '{self.name}' to be on connection '{connection.name}' which is a round-bar. This would become invalid if the round-bar disconnected and is thus not allowed."
                    )

        self._friction = list(friction)

        if self._isloop:
            self._vfNode.unkonwn_friction_index = self._friction.index(None)

        self._update_vfNodes()

    @property
    def angles_at_connections(self) -> tuple[float, ...]:
        """Change in cable direction at each of the connections [deg]"""

        with non_sticky_cable(self) as non_sticky:
            return tuple(np.rad2deg(non_sticky._vfNode.angles_at_connections))


    @property
    def max_winding_angles(self) -> tuple[float, ...]:
        """Maximum winding angles at the connections [deg]"""
        return tuple(self._max_winding_angle)

    @max_winding_angles.setter
    @node_setter_manageable
    @node_setter_observable
    def max_winding_angles(self, max_winding_angles):
        if isinstance(max_winding_angles, (float, int)):
            max_winding_angles = [max_winding_angles]

        # check length
        req_len = len(self._pois)
        assert (
            len(max_winding_angles) == req_len
        ), f"max_winding_angles should be defined for all {req_len} connections, got {len(max_winding_angles)} values."

        for _ in max_winding_angles:
            if _ > 0:
                assert (
                    _ > 180
                ), f"max_winding_angles should be more than 180 degrees, {_} is not."

        self._max_winding_angle = list(max_winding_angles)
        self._update_vfNodes()

    @property
    def offsets(self) -> tuple[float, ...]:
        """Offset of the cable at each of the connections [m]"""
        return tuple(self._offsets)

    @offsets.setter
    @node_setter_manageable
    @node_setter_observable
    def offsets(self, offset):
        if isinstance(offset, (float, int)):
            offset = [offset]

        # check length
        req_len = len(self._pois)
        assert (
            len(offset) == req_len
        ), f"offsets should be defined for all {req_len} connections"

        self._offsets = list(offset)
        self._update_vfNodes()

    def _get_advanced_settings_dialog_settings(self):
        # Function to tell the dialog what is editable
        # returns: (endAFr, endAMaxWind, endBFr, endBMaxWind, is_grommet_in_line_mode)
        if self._isloop:
            return True, True, False, True, False
        else:
            return False, True, False, True, False

    @property
    def friction_forces(self) -> tuple[float]:
        """Forces at the connections due to friction [kN]"""
        if self.is_sticky:
            # TODO
            raise NotImplementedError("Friction forces are not implemented for sticky cables")

        else:
            return tuple(self._vfNode.friction_forces)

    @property
    def calculated_friction_factor(self) -> float or None:
        """The friction factor that was left for DAVE to calculate [-], only applicable to non-sticky loops"""
        if self._isloop and not self.is_sticky:
            return self._vfNode.calculated_unknown_friction_factor
        else:
            return None

    @property
    def friction_factors_as_calculated(self) -> tuple[float]:
        """The friction factors as calculated by DAVE [-], only applicable to loops"""
        if self._isloop and not self.is_sticky:
            fr = list(self.friction)
            fr[self._vfNode.unkonwn_friction_index] = (
                self._vfNode.calculated_unknown_friction_factor
            )
            return tuple(fr)
        else:
            return self.friction

    @property
    def segment_end_tensions(self) -> tuple[tuple[float]]:
        """Tensions at the ends of each of the cable segments [kN, kN]
        These are identical if the cable weight is zero.
        """
        segment_end_forces = []
        for n in self._vfCableNodes:
            segment_end_forces.extend(self._vfNode.get_segment_end_tensions)

        combined = [
            (segment_end_forces[2 * i], segment_end_forces[2 * i + 1])
            for i in range(len(segment_end_forces) // 2)
        ]

        return tuple(combined)

    @property
    def segment_mean_tensions(self) -> tuple[float]:
        """Mean tensions in the free segments of the cable [kN]
        Note that the tension in a segment is constant if the cable weight is zero.
        """
        return tuple([0.5 * (p[0] + p[1]) for p in self.segment_end_tensions])

    @property
    def connections(self) -> tuple[Point or Circle]:
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
        #NOGUI
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

            if node1 == node2:
                nodes_str = "\n-".join([node.name for node in nodes])
                raise ValueError(
                    f"Error when setting connections of {self.name} to {nodes_str}\n\nIt is not allowed to have the same node repeated - you have {node1.name} and {node2.name}"
                )

        # check for round-bar restrictions:
        #
        # If a connection is a round-bar, then it shall be surrounded by two nodes that are not round-bars.

        def is_roundbar(node):
            if isinstance(node, Circle):
                return node.is_roundbar
            else:
                return False

        if is_roundbar(nodes[0]):
            raise ValueError(
                f"Error when setting connections of '{self.name}': First connection '{nodes[0].name}' is a round-bar. This is not allowed. Connections to a round-bar must always be between two non-roundbar connections"
            )
        if is_roundbar(nodes[-1]):
            raise ValueError(
                f"Error when setting connections of '{self.name}': Last connection '{nodes[-1].name}' is a round-bar. This is not allowed. Connections to a round-bar must always be between two non-roundbar connections"
            )

        for i in range(len(nodes) - 2):
            if is_roundbar(nodes[i + 1]):
                if is_roundbar(nodes[i]) or is_roundbar(nodes[i + 2]):
                    raise ValueError(
                        f"Error when setting connections of '{self.name}': Connection '{nodes[i+1].name}' is a round-bar and is not surrounded by two non-roundbars. This is not allowed.\n"
                        f"Connections to a round-bar must always be between two non-roundbar connections\n"
                        f"before is {nodes[i].name} and after is {nodes[i+2].name}"
                    )

        was_loop = self._isloop

        self._pois.clear()
        self._pois.extend(nodes)

        # are we switching from a line to a loop
        if not was_loop and self._isloop and not self.is_sticky:
            # yes, we are switching from a line to a loop
            # so we need to add a friction factor (None) at the start and set the unknown friction index
            self._friction.insert(0, None)
            self._vfNode.unkonwn_friction_index = 0

        if was_loop and not self._isloop:
            # switching from loop to line
            # pop the first friction factor
            self._friction.pop(0)
            self._vfNode.unkonwn_friction_index = -1

        self._update_vfNodes()

    def get_points_for_visual(self):
        """A list of 3D locations which can be used for visualization"""

        if getattr(
            self, "_keep_taut_visual", None
        ):  # for frequency domain response movies
            rsag = 2
        else:
            rsag = RESOLUTION_CABLE_SAG

        if getattr(self, "_get_drawing_data_override", None):
            points, tensions = self._get_drawing_data_override(
                rsag, RESOLUTION_CABLE_OVER_CIRCLE
            )
            return points

        points = []
        for cableNode in self._vfCableNodes:
            pts, _ = cableNode.get_drawing_data(
                rsag, RESOLUTION_CABLE_OVER_CIRCLE, False
            )
            points.extend(pts)

        return points

    def get_points_and_tensions_for_visual(self):
        """A list of 3D locations which can be used for visualization"""

        if getattr(
            self, "_keep_taut_visual", None
        ):  # for frequency domain response movies
            rsag = 2
        else:
            rsag = RESOLUTION_CABLE_SAG

        if getattr(self, "_get_drawing_data_override", None):  # For Slings
            return self._get_drawing_data_override(rsag, RESOLUTION_CABLE_OVER_CIRCLE)

        points = []
        tensions = []

        for cableNode in self._vfCableNodes:
            pts, tens = cableNode.get_drawing_data(
                rsag, RESOLUTION_CABLE_OVER_CIRCLE, False
            )
            points.extend(pts)
            tensions.extend(tens)

        return points, tensions

    def get_points_for_visual_blender(self):
        """A list of 3D locations which can be used for visualization"""
        constant_point_count = True

        if getattr(self, "_get_drawing_data_override", None):  # For Slings
            points, tensions = self._get_drawing_data_override(
                RENDER_CATENARY_RESOLUTION, RENDER_CURVE_RESOLUTION
            )
        else:
            points, tensions = self._vfNode.get_drawing_data(
                RENDER_CATENARY_RESOLUTION,
                RENDER_CURVE_RESOLUTION,
                constant_point_count,
            )
        return points

    def get_point_along_cable(self, pos1f=None) -> tuple[float, float, float]:
        """Returns the 3D location of the cable at a certain position along the cable.
        Defaults to the center of the first segment."""

        points = self.get_points_for_visual()
        # calculate the length along the cable
        points = np.asarray(points)
        dxyz = np.diff(points, axis=0)
        lengths = np.linalg.norm(dxyz, axis=1)
        length = np.sum(lengths)

        distance_along_line = np.cumsum(lengths)
        distance_along_line = np.insert(distance_along_line, 0, 0)

        if pos1f is not None:
            pos = pos1f * length
        else:
            # Set the position to the center of the first segment
            SL = self.segment_lengths
            pos = SL[1] / 2  # the first free segment is nr 1

        # interpolate the position
        x = np.interp(pos, distance_along_line, points[:, 0])
        y = np.interp(pos, distance_along_line, points[:, 1])
        z = np.interp(pos, distance_along_line, points[:, 2])

        return (x, y, z)

    def set_all_sticky(self):
        """Sets all connections to sticky using cut actual positions of the cable on the connections. Then remove friction factors."""

        lengths = self.segment_lengths   #
        L = sum(lengths)

        # check the number of segment lengths
        req = 0
        if self._isloop:
            cons = self.connections[:-1]
        else:
            cons = self.connections
        for c in cons:
            if isinstance(c, Point):
                req += 1
            elif isinstance(c, Circle):
                req += 2

        assert len(lengths) == req, "Length of the cable is not equal to the sum of the segment lengths"


        assert L == self.length, "Length of the cable is not equal to the sum of the segment lengths"

        positions = self._get_cable_points_at_mid_of_connections()

        # if the cable is a loop, then the last position is the same as the first
        # if the cable is not a loop then sticky[0] and sticky[-1] are not used

        sticky = []
        cum_length = 0
        i_segment = 0

        for i, c in enumerate(cons):

            if not self._isloop and (i == 0 or i == len(positions)-1):
                sticky.append(None)
                continue

            # check for in-active bars!

            if isinstance(c, Point):
                sticky.append(cum_length / L)

            elif isinstance(c, Circle):
                if c.is_roundbar:
                    sticky.append(None)

                    # check if the bar is active
                    # TODO: implement this
                    raise NotImplementedError("Sticky cables with roundbars are not implemented yet")

                else:
                    length_on_connection = lengths[i_segment]
                    i_segment += 1

                    # get the position on the circumference of the circle
                    # this is the point where the cable sticks
                    p = positions[i]
                    theta = c.theta_from_point(p)

                    cum_length += length_on_connection/2
                    sticky.append((cum_length / L, theta))
                    cum_length += length_on_connection / 2


            cum_length += lengths[i_segment]
            i_segment += 1

        if self._isloop:
            # derive the first sticky position from the last
            # sticky.append(positions[-1])
            sticky.append(None) # last is not used

        self.sticky = sticky

        req_len = len(self.connections) - 2
        if self._isloop:
            req_len += 1

        self.friction = [None] * req_len











    def _synchronize_connection_definition_vector_lengths_to_connections(self):
        """Synchronize the lengths of the connection definition vectors such that they
        match the length of the connections vector for all except friction.
        """

        # sync length of reversed
        while len(self._reversed) < len(self._pois):
            self._reversed.append(False)
        self._reversed = self._reversed[0: len(self._pois)]

        # sync length of friction
        req_friction_length = len(self._pois) - 2
        if self._isloop:
            req_friction_length += 1

        while len(self._friction) < req_friction_length:
            self._friction.append(0)
        self._friction = self._friction[0:req_friction_length]

        # sync length of maximum winding angles
        while len(self._max_winding_angle) < len(self._pois):
            self._max_winding_angle.append(DEFAULT_WINDING_ANGLE)
        self._max_winding_angle = self._max_winding_angle[0: len(self._pois)]

        # sync length of offsets
        while len(self._offsets) < len(self._pois):
            self._offsets.append(0)
        self._offsets = self._offsets[0: len(self._pois)]

        # sync length of sticky
        while len(self._sticky) < len(self._pois):
            self._sticky.append(None)
        self._sticky = self._sticky[0: len(self._pois)]

        # for non-loops: remove sticky from the first and last connection if any. They are sticky by default
        if not self._isloop:
            if self._sticky[0] is not None:
                self._sticky[0] = None
            if self._sticky[-1] is not None:
                self._sticky[-1] = None

    def _get_connection_aligned_friction(self):
        """Return a list of frictions aligned with the connections.

        For loops: The first index is the friction at the start/end point of the loop.

        If the cable is a loop then the friction at the last connection is calculated from the other frictions.
        """

        if self._isloop:
            frictions = list(self._friction)
            frictions.append(0)
        else:
            frictions = [0, *self._friction, 0]

        return frictions


    def _get_partial_cable_length_fractions(self) -> list[float]:
        """For sticky cables, return a list of the fractions of the cable length that are between the sticky connections.
        For non-sticky cables returns 1.0. Aligned with _vfCables and _get_core_cable_indices so
        the first length is the length """

        if self.is_sticky:

            positions = []

            for sticky in self._sticky:
                if sticky is not None:
                    if isinstance(sticky, (int,float)):
                        positions.append(sticky)
                    elif len(sticky) == 2:
                        positions.append(sticky[0])
                    else:
                        raise ValueError("Invalid sticky format")



            lengths = [positions[i+1]-positions[i] for i in range(len(positions)-1)]
            lengths.append(1-positions[-1])

            if self._isloop:
                lengths[-1] += positions[0]
            else:
                lengths.insert(0, positions[0])

            return lengths

        else:
            return [1.0]


    def _get_core_cable_indices(self) -> list[list[int]]:
        """For sticky cables, return a list of lists of indices of the connections that are part of the core cables.


        Examples of the mapping for a loop

        API Definition      CoreCable1       CoreCable2

        Connection #        indeces[0]       indices[1]
        0    pointA
        1   sticky             1
        2                      2
        3                      3
        4   sticky             4                 4
        5    pointA                              5
                                                 0
                                                 1


API Definition      CoreCable1       CoreCable2

        Connection #        indeces[0]       indices[1]
        0   sticky             0
        1                      1
        2                      2
        3                      3
        4   sticky             4                 4
        5    pointA                              5
                                                 0



        """


        if self._isloop:

            connections_to_be_processed = list(range(len(self.connections)))
            core_cables = list()
            core_cable = None


            while True:
                if len(connections_to_be_processed) == 0:
                    core_cables.append(core_cable)
                    break

                connection = connections_to_be_processed.pop(0)

                if self._sticky[connection] is not None:  # this is a sticky connection,

                    # add the last connection to the current core_cable (if any)
                    if core_cable is not None:
                        core_cable.append(connection)
                        core_cables.append(core_cable)

                    # start a new core-cable
                    core_cable = list()
                    core_cable.append(connection)

                else:  # this is not a sticky connection
                    if core_cable is not None:
                        core_cable.append(connection)
                    else:
                        connections_to_be_processed.append(
                            connection)  # re-add the connection to the list for later processing

            return core_cables

        else:  # not a loop, much easier to handle;

            cable = []
            core_cables = []

            for i_connection, connection in enumerate(self.connections):

                cable.append(i_connection)
                if self._sticky[i_connection] is not None:
                    core_cables.append(cable)
                    cable = [i_connection]

            core_cables.append(cable)
            return core_cables

    def _get_or_create_sticky_point_for(self, i_connection):
        """Returns the sticky point for a connection. If it does not exist yet, it is created"""
        if i_connection == len(self.connections) - 1: # last connection
            if self._isloop:
                i_connection = 0

        if i_connection not in self._vfPoiNodes:

            # create
            connection = self.connections[i_connection]
            sticky = self._sticky[i_connection]

            assert len(sticky) == 2
            assert isinstance(connection, Circle)
            theta = sticky[1]
            assert isinstance(theta, (float, int))

            position = connection.point3_from_theta_and_r_local(theta, r = connection.radius + 0.5*self.diameter + 1e-3)

            parent = connection.parent.parent # the parent of the point that the circle is on

            # create a point at the position
            name = f"{self.name}{VF_NAME_SPLIT}sticky#{i_connection}"
            point = self._scene._vfc.new_poi(name)
            point.position = position
            if parent is None:
                point.parent = None
            else:
                point.parent = parent._vfNode

            self._vfPoiNodes[i_connection] = point

        return self._vfPoiNodes[i_connection]




    def _update_vfNodes(self):

        self._synchronize_connection_definition_vector_lengths_to_connections()

        if self.is_sticky:

            name = self.name # copy here because it will not be available after deleting vfNodes

            # clean up
            for node in self._vfCableNodes:
                self._scene._vfc.delete(node.name)
            self._vfCableNodes.clear()

            for node in self._vfPoiNodes.values():
                self._scene._vfc.delete(node.name)
            self._vfPoiNodes.clear()

            # If the cable has sticky connections then the core structure differs from the API structure.
            # In the core structure the definition starts with the first sticky connection and starts a new
            # cable at every other sticky connection.

            connection_aligned_friction = self._get_connection_aligned_friction()
            core_cables_connection_indices = self._get_core_cable_indices()

            # by definition, each core-cable starts and ends with a sticky connection. So none of them are loops!
            # if the first or last connection of a core-cable is a circle, then we need to add a point to stick to

            for core_cable_indices in core_cables_connection_indices:

                # for the first cable, use  the name of the cable, for the others add a number
                if self._vfCableNodes: # first cable
                    name = f"{name}{VF_NAME_SPLIT}core_cable#{len(self._vfCableNodes)}"

                vfCable = self._scene._vfc.new_cable(name)
                self._vfCableNodes.append(vfCable)

                # start point -------------------
                i_connection = core_cable_indices[0]
                if isinstance(self.connections[i_connection], Circle):
                    if not self._isloop and (i_connection == 0 or i_connection == len(self.connections)-1):
                        pass
                    else:
                        vfCable.add_connection_poi(self._get_or_create_sticky_point_for(i_connection), 0) # makes sure that the point is created, no friction

                # intermediate points ------------

                for i_connection in core_cable_indices:
                    connection = self.connections[i_connection]
                    friction = connection_aligned_friction[i_connection]

                    if friction is None:
                        warnings.warn("Friction factor is None which is not allowed when using sticky cables, setting to 0")
                        friction = 0

                    if isinstance(connection, Circle):
                        vfCable.add_connection_sheave(
                            connection._vfNode,
                            self.reversed[i_connection],
                            friction,
                            np.deg2rad(self.max_winding_angles[i_connection]),
                            self.offsets[i_connection],
                        )
                    else:
                        vfCable.add_connection_poi(connection._vfNode, friction)

                # last point if needed -------------------------
                i_connection = core_cable_indices[-1]

                if isinstance(self.connections[i_connection], Circle):
                    if not self._isloop and (i_connection == 0 or i_connection == len(self.connections) - 1):
                       pass
                    else:
                        vfCable.add_connection_poi(self._get_or_create_sticky_point_for(i_connection),0)  # makes sure that the point is created






        else:
            # reduce to a single cable node
            for node in self._vfCableNodes[1:]:
                self._scene._vfc.delete(node.name)
            self._vfCableNodes = self._vfCableNodes[0:1]

            for node in self._vfPoiNodes.values():
                self._scene._vfc.delete(node.name)
            self._vfPoiNodes.clear()

            cableNode = self._vfCableNodes[0] # alias

            cableNode.clear_connections()

            for connection, reversed, max_winding, offset in zip(
                self._pois, self._reversed, self._max_winding_angle, self._offsets
            ):

                friction = 0 # overruled later

                if isinstance(connection, Point):
                    self._vfNode.add_connection_poi(connection._vfNode, friction)
                if isinstance(connection, Circle):
                    self._vfNode.add_connection_sheave(
                        connection._vfNode,
                        reversed,
                        friction,
                        np.deg2rad(max_winding),
                        offset,
                    )

            # set friction
            # replace none friction by 0
            self._vfNode.friction_factors = [
                f if f is not None else 0 for f in self._friction
            ]

            self._vfNode.update()

    def _give_poi_names(self):
        """Returns a list with the names of all the pois"""
        r = list()
        for p in self._pois:
            r.append(p.name)
        return r

    def _update_vfCable_scalar_properties(self):
        """Updates the lengths, masses and EA """

        Lfrac = self._get_partial_cable_length_fractions()

        for n, f in zip(self._vfCableNodes, Lfrac):
            n.Length = self.length * f
            n.EA = self._EA
            n.diameter = self._diameter
            n.mass_per_length = self._mass_per_length

    def _create_dummy_cable(self) -> "Cable":
        """Creates a dummy cable without sticky segments"""

        available_name = self._scene.available_name_like("dummy_cable")
        dummy_cable = Cable(scene=self._scene, name=available_name)

        dummy_cable.connections = self.connections
        dummy_cable.reversed = self.reversed
        dummy_cable.max_winding_angles = self.max_winding_angles
        dummy_cable.offsets = self.offsets

        dummy_cable.EA = 0
        dummy_cable.Length = 0
        dummy_cable.diameter = self.diameter

        return dummy_cable



    def _get_cable_points_at_mid_of_connections(self):
        """Returns the 3d points at the mid of the connections.
        For points this is just the point,
        for circles or round this is the mid of the section on the circle.
        Roundbars are EXCLUDED

        ! This is a relatively slow function; it utilizes the drawing data to get the points !
        """

        # create a dummy copy of the cable to get the visual without interfering with the actual cable
        # and without sticky points

        with non_sticky_cable(self) as non_sticky:

            n_free = 0
            n_circle = 3
            constant_pointcount = True

            points, _  = non_sticky._vfNode.get_drawing_data(n_free, n_circle, constant_pointcount)

        # loop over the connections,
        # for each connection get the points that are on the connection (just check the distance)
        points = np.asarray(points)

        connection_points = []

        for c in self.connections:
            if isinstance(c, Point):
                connection_points.append(c.global_position)
            elif isinstance(c, Circle):
                if c.is_roundbar:
                    connection_points.append(None)
                else:
                    # get the points on the circumference of the circle
                    # the second point in row is the mid of the section on the circle
                    points_on_connection = []

                    for p in points:
                        distance = np.linalg.norm(p - c.global_position)
                        if np.abs(distance - c.radius - self.diameter/2) < self.diameter/2000:
                            points_on_connection.append(tuple(p))

                    if len(points_on_connection) == 3:
                        connection_points.append(points_on_connection[1])
                    elif len(points_on_connection) == 4:
                        connection_points.append(points_on_connection[0])
                    else:
                        raise ValueError("Could not find the mid of the section on the circle")


        return connection_points






    @node_setter_manageable
    def set_length_for_tension(self, target_tension):
        """Given the actual geometry and EA of the cable, change the length such that
        the tension in the cable becomes the supplied tension
        """

        # F = stretch * EA / L
        # so : L = L0*EA / (F + EA)

        self.length = (self.actual_length) * self.EA / (target_tension + self.EA)

    @node_setter_manageable
    def set_length_for_stretched_length_under_tension(
        self, stretched_length, target_tension=None
    ):
        """Changes the length of cable such that its stretched length under target-tension becomes stretched-length."""

        # F = stretch * EA / L
        # so : L = L0*EA / (F + EA)

        if target_tension is None:
            target_tension = self.tension

        self.length = stretched_length * self.EA / (target_tension + self.EA)

    def update(self):
        """Update the cable internals"""
        self._vfNode.update()

    def give_python_code(self):
        code = list()
        code.append("# code for {}".format(self.name))

        poi_names = self._give_poi_names()
        n_sheaves = len(poi_names) - 2

        code.append("s.new_cable(name='{}',".format(self.name))
        code.append("            endA='{}',".format(poi_names[0]))
        code.append("            endB='{}',".format(poi_names[-1]))
        code.append("            length={:.6g},".format(self.length))

        if self.mass_per_length != 0:
            code.append(
                "            mass_per_length={:.6g},".format(self.mass_per_length)
            )

        if self.diameter != 0:
            code.append("            diameter={:.6g},".format(self.diameter))

        if len(poi_names) <= 2:
            code.append("            EA={:.6g})".format(self.EA))
        else:
            code.append("            EA={},".format(self.EA))

            if n_sheaves == 1:
                code.append("            sheaves = ['{}'])".format(poi_names[1]))
            else:
                code.append("            sheaves = ['{}',".format(poi_names[1]))
                for i in range(n_sheaves - 2):
                    code.append("                       '{}',".format(poi_names[2 + i]))
                code.append("                       '{}'])".format(poi_names[-2]))

        if np.any(self.reversed):
            code.append(f"s['{self.name}'].reversed = {self.reversed}")

        if np.any([_ != DEFAULT_WINDING_ANGLE for _ in self._max_winding_angle]):
            code.append(
                f"s['{self.name}'].max_winding_angles = {self._max_winding_angle}"
            )

        if np.any([_ != 0 for _ in self._offsets]):
            code.append(f"s['{self.name}'].offsets = {self._offsets}")

        if np.any(self._friction):
            code.append(f"s['{self.name}'].friction = {self._friction}")

        if self._vfNode.explicit_cable_no_loop:
            code.append(f"s['{self.name}']._set_no_loop()")

        return "\n".join(code)

