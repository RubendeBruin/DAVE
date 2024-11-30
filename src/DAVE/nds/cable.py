import warnings
import numbers
from contextlib import contextmanager

# define enum FrictionType for friction calculation with values None, Force, Position
from enum import Enum
from re import match
from typing import Tuple

import numpy as np

from .abstracts import NodeCoreConnected
from .core import DEFAULT_WINDING_ANGLE
from .geometry import Point, Circle
from .helpers import *

# from ..helpers.vector_compare_and_match import vector_compare_and_match
from ..settings import (
    VF_NAME_SPLIT,
    RENDER_CURVE_RESOLUTION,
    RENDER_CATENARY_RESOLUTION,
)
from ..tools import assert1f_positive_or_zero, assertBool, sync_inplace
from ..visual_helpers.constants import (
    RESOLUTION_CABLE_SAG,
    RESOLUTION_CABLE_OVER_CIRCLE,
)


class FrictionType(Enum):
    No = 0
    Force = 1
    Position = 2

    def __repr__(self):
        return self.__str__()


# noinspection PyProtectedMember
@contextmanager
def non_sticky_cable(cable: "Cable"):
    """Provides a non-sticky version of the cable.
    If the cable is stick, then a non-sticky copy is made and deleted.
    If the cable is non-sticky, this just yields the cable itself."""

    dummy_cable = False

    if not cable._multi_segment_model:
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


# noinspection PyProtectedMember
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
        self._vfPoiNodes = (
            dict()
        )  # key is the index of the connection that the poi belongs to (if any)
        self._vfCableNodes = [_vfNode]
        self._explicit_no_loop = False

        super().__init__(scene=scene, name=name)

        # These are the user-defined connections and connection properties
        # all except friction are aligned.
        # they are synchronized in length by the _synchronize_connection_definition_vector_lengths_to_connections method
        self._pois = list()
        self._reversed: list[bool] = list()
        self._max_winding_angle: list[float] = list()
        self._offsets: list[float] = list()

        # friction model
        # Friction parameters are defined at the intermediate connections
        # If the cable is a loop then friction is defined at the first (start) connection as well.
        # Hint: use _make_connection_aligned_copy_of_friction_vector to convert to connection aligned vector
        self._friction_type: list[FrictionType] = list()
        self._friction_force_factor: list[float or None] = (
            list()
        )  # length of friction is one or two less than pois
        self._friction_point_cable: list[float or None] = list()
        self._friction_point_connection: list[float or None] = list()

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

    def _give_poi_names(self):
        """Returns a list with the names of all the pois"""
        r = list()
        for p in self._pois:
            r.append(p.name)
        return r

    def _make_connection_aligned_copy_of_friction_vector(
        self, input_vector: tuple or list, insert_value=None
    ):
        """Make a copy of the input vector, but aligned with the connections

        See Also: _make_friction_vector_from_connection_aligned_vector
        """

        c = list(input_vector)  # copy

        # cut or sync to length
        n_req = self._req_friction_vector_length()
        if len(c) > n_req:
            c = c[:n_req]
        if len(c) < n_req:
            c.extend([insert_value] * (n_req - len(c)))

        if not self._isloop:
            c.insert(0, insert_value)
        c.append(insert_value)

        return c

    def _make_friction_vector_from_connection_aligned_vector(
        self, input_vector: tuple or list
    ):
        """Make a copy of the input vector, but aligned with the connections

        See Also: _make_connection_aligned_copy_of_friction_vector
        """

        c = list(input_vector)
        if not self._isloop:
            c.pop(0)
        c.pop(-1)

        return c

    def _assert_correct_friction_vector_length(self, vector):
        if self._isloop:
            assert (
                len(vector) == len(self._pois) - 1
            ), f"Friction vector should have length {len(self._pois) - 1}, but has length {len(vector)}"
        else:
            assert (
                len(vector) == len(self._pois) - 2
            ), f"Friction vector should have length {len(self._pois) - 2}, but has length {len(vector)}"

    @property
    def friction_type(self) -> tuple[FrictionType, ...]:
        """Friction model at the connections [FrictionType]"""
        return tuple(self._friction_type)

    @friction_type.setter
    def friction_type(self, value: tuple[FrictionType, ...] or FrictionType):
        """Supply a single value to set all indices to the same value"""

        if isinstance(value, FrictionType):
            value = [value] * len(self._friction_type)

        self.update_connections(friction_type=value)

    @property
    def friction_force_factor(self):
        return tuple(self._friction_force_factor)

    @friction_force_factor.setter
    def friction_force_factor(self, value):
        self.update_connections(friction_force_factor=value)

    @property
    def friction_point_cable(self):
        return tuple(self._friction_point_cable)

    @friction_point_cable.setter
    def friction_point_cable(self, value):
        self.update_connections(friction_point_cable=value)

    @property
    def friction_point_connection(self):
        return tuple(self._friction_point_connection)

    @friction_point_connection.setter
    def friction_point_connection(self, value):
        self.update_connections(friction_point_connection=value)

    @property
    def friction(self) -> tuple[float]:
        """Friction factors at the connections [-]"""

        warnings.warn(
            "Deprecated: Use friction_force_factor instead", DeprecationWarning
        )

        # noinspection PyTypeChecker
        return tuple(self._friction_force_factor)

    # note: not managed because it is technically a DOF (and we need it in rigging variations)
    @friction.setter
    @node_setter_observable
    def friction(self, value):

        warnings.warn(
            "Deprecated: Use friction_force_factor instead", DeprecationWarning
        )

    def set_friction_old_style(self, value):
        """Sets the friction to the old style friction factor and None for a single fixed point"""

        if None in value:

            self.friction_type = FrictionType.No

            positions = [None] * len(value)
            positions[value.index(None)] = 0

            self.friction_point_cable = positions
            self.friction_point_connection = positions

            self.friction_force_factor = [_ if _ is not None else 0 for _ in value]

            types = [
                FrictionType.Force if _ is not None else FrictionType.Position
                for _ in value
            ]
            self.friction_type = types

        else:
            self.friction_type = FrictionType.No
            self.friction_force_factor = value
            self.friction_type = FrictionType.Force

    # Only manage geometrical propertis, not the friction @node_setter_manageable
    def update_connections(
        self,
        friction_type=None,
        friction_force_factor=None,
        friction_point_cable=None,
        friction_point_connection=None,
        connections=None,
        reversed=None,
        max_winding_angles=None,
        offsets=None,
    ):
        """Applies multiple friction settings at once before validating their correctness.
        This may conveniently be used to work-around temporarily invalid states that may occur when setting
        multiple friction settings one-by-one.

        Raises ValueError if any of the settings are invalid.
        """

        if connections or offsets or reversed:
            self._verify_change_allowed()

        errors = self._check_friction_vectors(
            friction_type=friction_type,
            friction_force_factor=friction_force_factor,
            friction_point_cable=friction_point_cable,
            friction_point_connection=friction_point_connection,
            connections=connections,
        )

        if errors:
            raise ValueError("\n".join(errors))

        # -------- input is valid, apply the settings ----------

        if friction_type is None:
            friction_type = self._friction_type

        if friction_force_factor is None:
            friction_force_factor = self._friction_force_factor

        if friction_point_cable is None:
            friction_point_cable = self._friction_point_cable

        if friction_point_connection is None:
            friction_point_connection = self._friction_point_connection

        if connections is None:
            connections = self.connections
        else:
            connections = Cable._check_and_convert_connections(
                self._scene, self.name, connections
            )  # convert strings to Nodes

        if reversed is None:
            reversed = self.reversed

        if max_winding_angles is None:
            max_winding_angles = self.max_winding_angles

        if offsets is None:
            offsets = self.offsets

        # Make all lists, such that we can inplace adjust lengths
        friction_type = list(friction_type)
        friction_force_factor = list(friction_force_factor)
        friction_point_cable = list(friction_point_cable)
        friction_point_connection = list(friction_point_connection)
        connections = list(connections)
        reversed = list(reversed)
        max_winding_angles = list(max_winding_angles)
        offsets = list(offsets)

        # loop?
        is_loop = connections[0] == connections[-1] and not self._explicit_no_loop

        # sync all the vectors to the correct length
        req_len_connections = len(connections)

        sync_inplace(reversed, False, req_len_connections)
        sync_inplace(max_winding_angles, DEFAULT_WINDING_ANGLE, req_len_connections)
        sync_inplace(offsets, 0, req_len_connections)

        # make sure that all vectors are long enough,
        # even if not relevant (the check at the start only checks for relevant settings)
        n_req = len(connections) - 2
        if is_loop:
            n_req += 1

        sync_inplace(friction_type, FrictionType.No, n_req)
        sync_inplace(friction_force_factor, 0, n_req)
        sync_inplace(friction_point_cable, None, n_req)
        sync_inplace(friction_point_connection, None, n_req)

        # apply
        self._friction_type = friction_type
        self._friction_force_factor = friction_force_factor
        self._friction_point_cable = friction_point_cable
        self._friction_point_connection = friction_point_connection

        self._offsets = offsets
        self._max_winding_angle = max_winding_angles
        self._reversed = reversed

        self._pois.clear()
        self._pois.extend(connections)

        self.update()

    @property
    def is_sticky(self) -> bool:
        """True if the loop is sticky. If the cable is a loop then this is the case if the cable has more than one positional points,
        if the cable is not a loop then one positional point is sufficient to make the cable sticky[bool]
        """
        n_positions = self._friction_type.count(FrictionType.Position)

        if self._isloop:
            return n_positions > 1
        else:
            return n_positions > 0

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
        assert1f_positive_or_zero(mass, "mass")
        self.mass_per_length = mass / self.length

    @property
    def reversed(self) -> tuple[bool, ...]:
        """Defines the direction in which the cable runs over the connection [bool]
        Defined for each of the connections"""
        return tuple(self._reversed)

    @reversed.setter
    @node_setter_manageable
    @node_setter_observable
    def reversed(self, new_reversed):

        if isinstance(new_reversed, bool):
            new_reversed = [new_reversed] * len(self._poi)

        # check itereable
        try:
            iter(new_reversed)
        except TypeError:
            raise ValueError("reversed should be an iterable of booleans")

        # check values
        for r in new_reversed:
            assertBool(r, "reversed")

        # check length
        req_len = len(self._pois)
        assert (
            len(new_reversed) == req_len
        ), f"reversed should be defined for all {req_len} connections, got {len(new_reversed)} values."

        self._reversed = list(new_reversed)
        self._update_vfNodes()

    @property
    def _isloop(self):
        """True if the cable is a loop"""
        if len(self.connections) < 2:
            return False
        if self.connections[0] == self.connections[-1]:
            return not self._explicit_no_loop
        return False

    def _set_no_loop(self):
        """Set the cable to be a non-loop explicitly - this overrules the normal behaviour"""

        cable_was_loop = self._isloop
        self._explicit_no_loop = True

        for n in self._vfCableNodes:
            n.explicit_cable_no_loop = True

        if cable_was_loop:
            # self.make_friction_vectors_valid()
            self._update_vfNodes()

    def _unset_no_loop(self):
        """Remove the flag that sets the cable to be a loop explicitly - returning to normal behaviour"""

        cable_was_loop = self._isloop
        self._explicit_no_loop = False

        for n in self._vfCableNodes:
            n.explicit_cable_no_loop = False

        if not cable_was_loop:
            # self.make_friction_vectors_valid()
            self._update_vfNodes()

    @property
    def solve_segment_lengths(self) -> bool:
        """If True then lengths of the segment are solved for a continuous tension distribution including weight. If false then the segment lengths are determined only on the geometry [bool]
        Note that the solution is typically not unique!"""
        if self._multi_segment_model:
            return False
        return self._vfNode.solve_section_lengths

    @solve_segment_lengths.setter
    def solve_segment_lengths(self, value):
        assertBool(value, "solve_segment_lengths")
        if value and self._multi_segment_model:
            raise ValueError(
                "Solve segment lengths is implemented in combination with sticky"
            )
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

        if not self._isloop or isinstance(self.connections[0], Point):
            assert (
                result[0] == 0
            ), f"Getting material lengths from {self.name}; First segment length should be 0, but is {result[0]}"
            result = result[1:]

        return result

    @property
    def connected_bars_active(self) -> tuple[bool]:
        """True if the i-th bar is active False if the bar is not active [bool,...]"""
        result = []

        for n in self._vfCableNodes:
            ab = n.connected_bar_active  # tuple of bool
            result.extend(ab)

        # noinspection PyTypeChecker
        return tuple(result)

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

        results = []

        for i, c in enumerate(self.connections[:-1]):

            # Logic for bars.
            # bars are always intermediate between two connections
            if isinstance(c, Circle):
                if c.is_roundbar:
                    active = active_bars.pop(0)
                    if active:
                        results[-1] += all_segments.pop(0) + all_segments.pop(
                            0
                        )  # segment on the bar and the following segment
                    else:
                        pass  # not present in the results

                    continue

            # Segment length on intermediate circles
            # or fist segment on the first circle in a loop
            if isinstance(c, Circle):
                if i > 0 or i == 0 and self._isloop:
                    results.append(all_segments.pop(0))

            results.append(all_segments.pop(0))  # free segment

        # noinspection PyTypeChecker
        return tuple(results)

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
        if isinstance(max_winding_angles, numbers.Real):
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
        if isinstance(offset, numbers.Real):
            offset = [offset]

        # assert iterable
        try:
            iter(offset)
        except TypeError:
            raise ValueError("offset should be an iterable of floats")

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
    def _multi_segment_model(self):
        """True if the cable is modelled as multiple segments"""

        return len(self._vfCableNodes) > 1

    @property
    def friction_forces(self) -> tuple[float]:
        """Forces at the connections due to friction [kN]"""
        if self._multi_segment_model:

            # for each cable segment:
            #   - vfNode.friction_forces are the friction forces at the intermediate connections
            #   friction forces at the sticky connections can be obtained from the point

            forces = list()

            segments_indices = self._get_core_cable_indices()

            segment_end_force = None

            for n, indices in zip(self._vfCableNodes, segments_indices):

                i_from = indices[0]
                i_to = indices[-1]

                if segment_end_force is not None:
                    segment_start_force = n.get_segment_end_tensions[0]
                    friction = segment_start_force - segment_end_force
                    forces.append(friction)
                else:  # first segment
                    tension_at_start_of_first_segment = n.get_segment_end_tensions[0]

                internal_forces = n.friction_forces

                # remove the friction at connection before the added points (if segment begins or ends with a circle):
                # as this friction is 0 and is included in the friction at the point
                if isinstance(self.connections[i_from], Circle):
                    internal_forces = internal_forces[1:]
                if isinstance(self.connections[i_to], Circle):
                    internal_forces = internal_forces[:-1]

                forces.extend(internal_forces)

                segment_end_force = n.get_segment_end_tensions[-1]

            if self._isloop:
                # insert the friction at the end/start of the loop
                # noinspection PyUnboundLocalVariable
                forces.insert(0, tension_at_start_of_first_segment - segment_end_force)

            # if the first segment does not start at the first connection, then
            # we need to shift the indices accordingly

            i0 = segments_indices[0][0]
            if i0 != 0:
                forces = forces[-i0:] + forces[:-i0]

            # noinspection PyTypeChecker
            return tuple(forces)

        else:
            return tuple(self._vfNode.friction_forces)

    @property
    def calculated_friction_factor(self) -> float or None:
        """The friction factor that was left for DAVE to calculate [-], only applicable to non-sticky loops"""
        if self._isloop and not self._multi_segment_model:
            return self._vfNode.calculated_unknown_friction_factor
        else:
            return None

    @property
    def friction_factors_as_calculated(self) -> tuple[float]:
        """The friction factors as calculated by DAVE [-], only applicable to loops"""
        if self._isloop and not self._multi_segment_model:
            fr = list(self.friction_force_factor)
            fr[self._vfNode.unknown_friction_index] = (
                self._vfNode.calculated_unknown_friction_factor
            )
            # noinspection PyTypeChecker
            return tuple(fr)
        else:
            return self.friction_force_factor

    @property
    def segment_end_tensions(self) -> tuple[tuple[float]]:
        """Tensions at the ends of each of the cable segments [kN, kN]
        These are identical if the cable weight is zero.
        """
        combined = []

        if self.is_sticky:
            raise ValueError(
                "TODO: re-order the connections to match the segments, see friction_forces implementation"
            )

        for node in self._vfCableNodes:
            segment_end_forces = node.get_segment_end_tensions

            reshuffled = [
                (segment_end_forces[2 * i], segment_end_forces[2 * i + 1])
                for i in range(len(segment_end_forces) // 2)
            ]

            combined.extend(reshuffled)

        # noinspection PyTypeChecker
        return tuple(combined)

    @property
    def segment_mean_tensions(self) -> tuple[float]:
        """Mean tensions in the free segments of the cable [kN]
        Note that the tension in a segment is constant if the cable weight is zero.
        """
        # noinspection PyTypeChecker
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
        # noinspection PyTypeChecker
        return tuple(self._pois)

    @connections.setter
    @node_setter_manageable
    @node_setter_observable
    def connections(self, value):
        if len(value) < 2:
            raise ValueError("At least two connections required")

        self.update_connections(connections=value)

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

    # ============================================================
    #
    # Annotation data
    # - get_annotation data creates the annotation data
    # - this is then stored in the annotation layer
    # - the annotation layer calls get_point_along_cable to get the 3D location of the annotation
    #
    #  The location is stored and given back using the position_1f parameter. The definition and
    #  interpretation of this parameter is defined here.
    #  Alternatively we could buffer the annotation data in the cable object when get_annotation_data
    #  is called and retrieve it when get_point_along_cable is called. This would be more efficient but
    #  the current implementation is more flexible.
    # ============================================================

    def get_annotation_data(self):
        """Get the data for the annotation layer

        See Also: get_point_along_cable
        """

        # 0 : position measured along cable - this number is later passed to
        # 1 : text

        data = []

        # friction at the connections
        friction = self.friction_forces
        i_offset = 1
        if self._isloop:
            i_offset = 0
        for i, f in enumerate(friction):
            data.append((-(1000 + i + i_offset), f"friction: {f:.2f} kN"))

        # tensions at the segment ends
        segment_end_data = []

        i = 0
        for n in self._vfCableNodes:
            positions, tensions = n.get_drawing_data(5, 2, True)
            previous_pos = positions[-1]
            for pos, t in zip(positions, tensions):
                if np.linalg.norm(np.array(pos) - previous_pos) > 1e-3:
                    new_row = (-(2000 + i), f"tension: {t:.2f} kN")
                    segment_end_data.append(new_row)
                    previous_pos = pos
                i += 1

        # to reduce the clutter, merge entries with the same text into one entry using the first entry of the middle segment of the group

        if segment_end_data:
            # unique texts
            unique_texts = set([d[1] for d in segment_end_data])

            for text in unique_texts:
                group = [d for d in segment_end_data if d[1] == text]
                if len(group) > 1:
                    # merge the group
                    middle = len(group) // 2
                    data.append((group[middle][0], text))
                    # data.append((group[-1][0], text))
                    # data.append((group[0][0], text))
                    # data.extend(group)

                else:
                    data.append(group[0])

        return data

    def get_point_along_cable(self, pos1f=None) -> tuple[float, float, float]:
        """Returns the 3D location of the cable at a certain position along the cable.

        pos1f: float . If in range [0...1] the number if the fraction of the length along the cable
        If None, the position is set to the center of the first segment.
        If <0: special cases as follows:
        -

        Defaults to the center of the first segment.



        See Also: get_annotation_data
        """
        if pos1f is None:
            pos1f = 0.5

        if pos1f < 0:  # --- special cases ----
            special = -pos1f

            if 1000 <= special < 2000:  # friction point of the cable on the section
                i_connection = special - 1000

                # is this a sticky cable on a circle? If so then get the location of the point on the circle
                if i_connection in self._vfPoiNodes:
                    return self._vfPoiNodes[i_connection].global_position

                midpoints = self._get_cable_points_at_mid_of_connections()
                return midpoints[i_connection]

            if 2000 <= special < 3000:
                i = special - 2000

                # tensions at the segment ends
                poss = []
                for n in self._vfCableNodes:
                    positions, tensions = n.get_drawing_data(5, 2, True)
                    poss.extend(positions)
                return poss[i]

        # --- normal cases ---

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
        x = float(np.interp(pos, distance_along_line, points[:, 0]))
        y = float(np.interp(pos, distance_along_line, points[:, 1]))
        z = float(np.interp(pos, distance_along_line, points[:, 2]))

        return x, y, z

    # ============================================================
    #
    # Friction
    #
    # ============================================================

    def _req_friction_vector_length(self):
        n_req = len(self.connections) - 2
        if self._isloop:
            n_req += 1
        return n_req

    # ==============================================
    #
    # Check functions
    #
    # ==============================================

    #
    @staticmethod
    def _check_and_convert_connections(
        scene, name, connections: list[str or Point or Circle]
    ) -> list[Point or Circle]:
        """Check the connections and convert them to a list of nodes
        Raises an exception if the connections are not valid"""

        nodes = []
        for p in connections:
            n = scene._node_from_node_or_str(p)

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
                    f"Error when setting connections of {name} to {nodes_str}\n\nIt is not allowed to have the same node repeated - you have {node1.name} and {node2.name}"
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
                f"Error when setting connections of '{name}': First connection '{nodes[0].name}' is a round-bar. This is not allowed. Connections to a round-bar must always be between two non-roundbar connections"
            )
        if is_roundbar(nodes[-1]):
            raise ValueError(
                f"Error when setting connections of '{name}': Last connection '{nodes[-1].name}' is a round-bar. This is not allowed. Connections to a round-bar must always be between two non-roundbar connections"
            )

        for i in range(len(nodes) - 2):
            if is_roundbar(nodes[i + 1]):
                if is_roundbar(nodes[i]) or is_roundbar(nodes[i + 2]):
                    raise ValueError(
                        f"Error when setting connections of '{name}': Connection '{nodes[i + 1].name}' is a round-bar and is not surrounded by two non-roundbars. This is not allowed.\n"
                        f"Connections to a round-bar must always be between two non-roundbar connections\n"
                        f"before is {nodes[i].name} and after is {nodes[i + 2].name}"
                    )

        return nodes

    def _check_friction_vectors(
        self,
        connections=None,
        friction_type=None,
        friction_force_factor=None,
        friction_point_cable=None,
        friction_point_connection=None,
        max_winding_angles=None,
        offsets=None,
        reversed=None,
    ):
        """Check the friction vectors for consistency with connections.
        If do_raise is true then the first error is raised as an exception.
        Returns a list of errors

        All parameters are optional and default to the current values of the cable.
        """

        if connections is None:
            connections = self.connections
        else:
            # fill the connections with nodes
            try:
                connections = Cable._check_and_convert_connections(
                    self._scene, self.name, connections
                )
            except ValueError as e:
                return [str(e)]  # early return

        if reversed is None:
            reversed = self._reversed

        if max_winding_angles is None:
            max_winding_angles = self._max_winding_angle

        if offsets is None:
            offsets = self._offsets

        if friction_type is None:
            friction_type = self._friction_type

        if friction_force_factor is None:
            friction_force_factor = self._friction_force_factor

        if friction_point_cable is None:
            friction_point_cable = self._friction_point_cable

        if friction_point_connection is None:
            friction_point_connection = self._friction_point_connection

        errors = []

        # check values of offsets and max_winding_angles
        for _ in max_winding_angles:
            if _ > 0:
                assert (
                    _ > 180
                ), f"max_winding_angles should be more than 180 degrees, {_} is not."

        # any friction?
        any_friction = not all([_ == FrictionType.No for _ in friction_type])
        is_loop = connections[0] == connections[-1] and not self._explicit_no_loop

        if not any_friction:  # no further checks needed
            return errors

        # check lengths

        n_req = len(connections) - 2
        if is_loop:
            n_req += 1

        if len(friction_type) != n_req:
            errors.append(
                f"Friction type vector has length {len(friction_type)} but should have length {n_req}"
            )

        if len(friction_force_factor) != n_req:
            errors.append(
                f"Friction force factor vector has length {len(friction_force_factor)} but should have length {n_req}"
            )

        if len(friction_point_cable) != n_req:
            errors.append(
                f"Friction point cable vector has length {len(friction_point_cable)} but should have length {n_req}"
            )

        if len(friction_point_connection) != n_req:
            errors.append(
                f"Friction point connection vector has length {len(friction_point_connection)} but should have length {n_req}"
            )

        if errors:
            return errors

        # check friction definitions
        endA_is_first = True
        if is_loop:  # if loop
            cons = connections[:-1]
        else:
            cons = connections[1:-1]
            endA_is_first = False

        is_loop_with_single_positional_connection = (
            is_loop and friction_type.count(FrictionType.Position) == 1
        )

        # check values for active friction types
        errors.extend(
            self.check_friction_vector_properties(
                cons,
                friction_type,
                friction_force_factor,
                friction_point_cable,
                friction_point_connection,
                is_loop_with_single_positional_connection=is_loop_with_single_positional_connection,
                first_con_is_endA=endA_is_first,
                last_con_is_endB=False,
            )
        )

        # check loops
        if is_loop:
            if FrictionType.Force in friction_type:
                if FrictionType.Position not in friction_type:
                    errors.append(
                        "If 'Force' friction is defined on a LOOPED cable, then at least one of the other connections shall be set to 'Position' to absorb any remaining friction and ensure internal force balance."
                    )

        return errors

    @staticmethod
    def check_friction_vector_properties(
        cons,
        friction_type,
        friction_force_factor,
        friction_point_cable,
        friction_point_connection,
        is_loop_with_single_positional_connection=False,
        first_con_is_endA=False,
        last_con_is_endB=False,
    ) -> list[str]:
        """Check the friction vectors values. Input vectors to be aligned with connections, pass only that portion of the
        connections vector that has friction properties defined

        Args:
        - is_loop_with_single_positional_connection: bool : set to True if the cable is a loop and has only one connection with friction type Position
        - first_con_is_endA: bool : set to True if the first connection is the endA of the cable. This may not be the case if the first connection is not passed

        Returns a list of errors
        """

        errors = []
        previous_friction_point_cable = -1
        delta = 1e-6

        for i, (con, kind, ff, pcable, pconnector) in enumerate(
            zip(
                cons,
                friction_type,
                friction_force_factor,
                friction_point_cable,
                friction_point_connection,
            )
        ):

            if kind == FrictionType.No:
                continue

            if kind == FrictionType.Force:
                if ff is None:
                    pass  # ok, checked later
                else:
                    if not isinstance(ff, numbers.Real):
                        errors.append(
                            f"Friction force factor nr {i} is {ff} of type {type(ff)} but should be a number"
                        )
                    else:
                        if abs(ff) >= 1:
                            errors.append(
                                f"Friction force factor nr {i} is {ff} but should be in the range (-1,1)"
                            )

            if kind == FrictionType.Position:

                if isinstance(con, Circle):
                    if con.is_roundbar:
                        errors.append(
                            f"Friction type nr {i}is set to Position, but the connection is a round-bar. This is not allowed"
                        )

                if is_loop_with_single_positional_connection:
                    continue  # this connection will be re-written as Force later

                if isinstance(pcable, numbers.Real):
                    # Check 0 , only ok if this is the first connection
                    if pcable == 0:
                        if not first_con_is_endA and i == 0:
                            errors.append(
                                f"Friction type nr {i} is set to Position = 0, This can only be done for the first connection"
                            )
                    elif pcable == 1:
                        if not last_con_is_endB and i == len(cons) - 1:
                            errors.append(
                                f"Friction type nr {i} is set to Position = 1, This can only be done for the last connection"
                            )
                    elif 0 <= pcable <= 1:
                        pass  # ok
                    else:
                        errors.append(
                            f"Friction type nr {i} is set to Position, Position of cable is set to {pcable} but should be in range [0,1]"
                        )

                    if pcable < previous_friction_point_cable + delta:
                        errors.append(
                            f"'Friction point cable' nr {i} has value {pcable} but should be larger than the previous friction point cable with value {previous_friction_point_cable} (there shall be a non-zero length of cable between two connections)"
                        )

                    previous_friction_point_cable = pcable
                else:
                    errors.append(
                        f"Friction type nr {i} is set to Position, but the position of the cable is not valid: {pcable}"
                    )

                if isinstance(con, Circle):
                    if not isinstance(pconnector, numbers.Real):
                        errors.append(
                            f"Friction type nr {i}is set to Position, but the point on the connector is not valid {pconnector}"
                        )
                        continue

        return errors

    # ============================================================
    #
    # Sticky stuff  (as from stick-slip)
    #
    # For sticky cables, the cable is stuck to the connections. This is done by defining the position of the cable at the connections.
    # For this two pieces of data are needed:
    #   1. Which point of the cable is stuck to the connection  :  friction_point_cable
    #   2. To which point of the connection is the cable stuck  :  friction_point_connection
    #
    # The second piece is only applicable to circles. For points the cable is stuck to the point.
    #
    # The friction_point_cable is a vector of floats or None where None may be used if the connection is not sticky.
    # The friction_point_connection is a vector of floats (for circles) or None (for points). None may also be used if the connection is not sticky.
    #
    # Sitcky connections are active if the friction_model for the connector is FrictionModel.Position
    #
    # A cable is called "sticky" if at least one of the connections has its friction model set to FrictionModel.Position

    # ============================================================

    def get_zero_friction_sticky_data_from_current_geometry(self):
        """Gets all sticky friction position data using actual positions of the cable on the connections.

        Returns a tuple of two lists:
        - the position of the cable on the connections [0...1]
        - the position of the cable on the connection [0...360] for circles, None for points

        The returned data is such that there is no friction at the pinned positions.
        The returned lists align with the connections list.
        """

        lengths = self.material_lengths_no_bars  #
        L = sum(lengths)

        # assert (
        #     abs(L - self.length) < 1e-6
        # ), f"{self.name} : Length of the cable {self.length} is not equal to the sum of the segment lengths {L}"

        positions = self._get_cable_points_at_mid_of_connections()

        # if the cable is a loop, then the last position is the same as the first
        # if the cable is not a loop then sticky[0] and sticky[-1] are not used

        point_cable = []
        point_connection = []

        cum_length = 0
        i_segment = 0

        if self._isloop:
            cons = self.connections[:-1]
        else:
            cons = self.connections

        for i, c in enumerate(cons):

            if not self._isloop and (i == 0 or i == len(positions) - 1):
                if i == 0:
                    cum_length += lengths[i_segment]
                    i_segment += 1

                point_cable.append(None)
                point_connection.append(None)

                continue

            if isinstance(c, Point):
                point_cable.append(cum_length / L)
                point_connection.append(None)  # not applicable

            elif isinstance(c, Circle):
                if c.is_roundbar:
                    point_cable.append(None)
                    point_connection.append(None)

                    continue

                else:
                    length_on_connection = lengths[i_segment]
                    i_segment += 1

                    # get the position on the circumference of the circle
                    # this is the point where the cable sticks
                    p = positions[i]
                    theta = c.theta_from_point(p)

                    cum_length += length_on_connection / 2

                    point_cable.append(cum_length / L)
                    point_connection.append(np.rad2deg(theta))

                    cum_length += length_on_connection / 2

            # add free segement length
            cum_length += lengths[i_segment]
            i_segment += 1

        if self._isloop:
            point_cable.append(point_cable[0])
            point_connection.append(point_connection[0])

        return point_cable, point_connection

    def set_zero_friction_sticky_data_from_current_geometry(self):
        """Sets all sticky friction position data using actual positions of the cable on the connections such that there is no friction at the pinned positions."""

        point_cable, point_connection = (
            self.get_zero_friction_sticky_data_from_current_geometry()
        )

        if self._isloop:
            point_cable = point_cable[:-1]
            point_connection = point_connection[:-1]
        else:
            point_cable = point_cable[1:-1]
            point_connection = point_connection[1:-1]

        self.friction_point_cable = point_cable
        self.friction_point_connection = point_connection

    def _synchronize_connection_definition_vector_lengths_to_connections(self):
        """Synchronize the lengths of the connection definition vectors such that they
        match the length of the connections vector.

        Pad with default values if needed

        For friction the required length is len(connections) - 2 or len(connections) - 1 if the cable is a loop
        """

        # offsets and reversed have the same lenghts as connections

        n_req = len(self.connections)

        sync_inplace(self._offsets, 0, n_req)
        sync_inplace(self._reversed, False, n_req)

    def get_sticky_positions_and_directions(self, min_dia=0.1, scale=1.5):
        """For each of the sticky points, the endpoints of the cone that visualizes the sticky point are returned.
        Scale is the size of the cone in relation to the diameter of the cable.
        min_dia is the minimum diameter of the cable as used in the visualization"""

        diameter = self.diameter
        diameter = max(diameter, min_dia)

        p_to = []
        p_from = []

        sticky_position = self._make_connection_aligned_copy_of_friction_vector(
            self.friction_point_cable
        )
        sticky_connection = self._make_connection_aligned_copy_of_friction_vector(
            self.friction_point_connection
        )
        friction_type = self._make_connection_aligned_copy_of_friction_vector(
            self.friction_type
        )

        for i, (c, model, s_pos, theta) in enumerate(
            zip(self.connections, friction_type, sticky_position, sticky_connection)
        ):
            if model is not FrictionType.Position:
                continue

            if isinstance(c, Point):

                # cable has no orientation at a point
                # use the orientation of the previous segment and the next segment (if any)

                gp = np.array(c.global_position, dtype=float)
                direction = np.array((0, 0, 0), dtype=float)

                if i > 0:
                    direction = direction - self.connections[i - 1].global_position + gp

                if i < len(self.connections) - 1:
                    direction = direction - self.connections[i + 1].global_position + gp

                if np.linalg.norm(direction) < 1e-9:
                    direction[2] = 1
                else:
                    direction = direction / np.linalg.norm(direction)

                p_to.append(gp)
                p_from.append(gp + direction * diameter * scale)

            elif isinstance(c, Circle):
                # sticky location at a circle

                local_position_on_parent1 = c.point3_from_theta_and_r_local(
                    theta=np.deg2rad(theta), r=c.radius + diameter
                )
                local_position_on_parent2 = c.point3_from_theta_and_r_local(
                    theta=np.deg2rad(theta), r=c.radius + diameter * (1 + scale)
                )

                if c.parent.parent is not None:
                    p_to.append(
                        c.parent.parent.to_glob_position(local_position_on_parent1)
                    )
                    p_from.append(
                        c.parent.parent.to_glob_position(local_position_on_parent2)
                    )
                else:
                    p_to.append(local_position_on_parent1)
                    p_from.append(local_position_on_parent2)

            else:
                raise ValueError("Unknown connection type")

        return p_to, p_from

    def _get_partial_cable_length_fractions(self) -> list[float]:
        """For sticky cables, return a list of the fractions of the cable length that are between the sticky connections.
        For non-sticky cables returns 1.0. Aligned with _vfCables and _get_core_cable_indices so
        the first length is the length"""

        if self.is_sticky:

            positions = []

            for kind, pos_cable in zip(self._friction_type, self._friction_point_cable):
                if kind is FrictionType.Position:
                    positions.append(pos_cable)

            lengths = [
                positions[i + 1] - positions[i] for i in range(len(positions) - 1)
            ]
            lengths.append(1 - positions[-1])

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

        friction_type_c_aligned = self._make_connection_aligned_copy_of_friction_vector(
            self._friction_type, FrictionType.No
        )

        if self._isloop:

            connections_to_be_processed = list(
                range(len(self.connections) - 1)
            )  # all but the last connection
            core_cables = list()
            core_cable = None

            while True:
                if len(connections_to_be_processed) == 0:
                    core_cables.append(core_cable)
                    break

                connection = connections_to_be_processed.pop(0)

                if (
                    friction_type_c_aligned[connection] is FrictionType.Position
                ):  # this is a sticky connection,

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
                            connection
                        )  # re-add the connection to the list for later processing

            # close the loop, if needed
            if core_cables[-1][-1] != core_cables[0][0]:
                core_cables[-1].append(core_cables[0][0])

        else:  # not a loop, much easier to handle;

            cable = []
            core_cables = []

            for i_connection, connection in enumerate(self.connections):

                cable.append(i_connection)
                if friction_type_c_aligned[i_connection] is FrictionType.Position:
                    core_cables.append(cable)
                    cable = [i_connection]

            if len(cable) == 1:
                raise ValueError(
                    "Non-loop cable ended with sticky connection. This is not supported (and doesnt make any sense either)"
                )  # len1 can happen is the last connection is sticky (which is weird anyways)

            core_cables.append(cable)

        # self check
        assert all(
            [len(core_cable) > 1 for core_cable in core_cables]
        ), "Internal error in _get_core_cable_indices, a core cable has less than 2 connections. Did a non-loop cable end with a sticky connection?"
        return core_cables

    def _get_or_create_sticky_point_node_for(self, i_connection):
        """Returns the sticky point NODE for a connection. If it does not exist yet, it is created"""
        if i_connection == len(self.connections) - 1:  # last connection
            if self._isloop:
                i_connection = 0

        if i_connection not in self._vfPoiNodes:

            # create
            connection = self.connections[i_connection]

            if self._isloop:
                theta = self._friction_point_connection[i_connection]
            else:
                theta = self._friction_point_connection[i_connection - 1]

            position = connection.point3_from_theta_and_r_local(
                np.deg2rad(theta), r=connection.radius + 0.5 * self.diameter
            )

            parent = (
                connection.parent.parent
            )  # the parent of the point that the circle is on

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

        # special cases for loops ----:
        #   - a loop with a single sticky connection --> re-write sticky connection as None friction factor
        #   - Friction.No --> friction factor 0

        model_sticky = self.is_sticky
        friction_factors_copy = self._friction_force_factor.copy()

        for i, (kind, ff) in enumerate(zip(self._friction_type, friction_factors_copy)):
            if kind is not FrictionType.Force:
                friction_factors_copy[i] = 0

        # re-write the friction factors for loops with a single sticky connection
        if self._isloop:
            # do we have a single sticky connection?
            if self._friction_type.count(FrictionType.Position) == 1:
                i = self._friction_type.index(FrictionType.Position)
                friction_factors_copy[i] = None
                model_sticky = False

        connection_aligned_friction_factors = (
            self._make_connection_aligned_copy_of_friction_vector(
                friction_factors_copy, 0
            )
        )

        # end re-write

        if model_sticky:

            name = (
                self.name
            )  # copy here because it will not be available after deleting vfNodes

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

            core_cables_connection_indices = self._get_core_cable_indices()

            # by definition, each core-cable starts and ends with a sticky connection. So none of them are loops!
            # if the first or last connection of a core-cable is a circle, then we need to add a point to stick to

            for core_cable_indices in core_cables_connection_indices:

                # for the first cable, use  the name of the cable, for the others add a number
                if self._vfCableNodes:  # first cable
                    name = f"{name}{VF_NAME_SPLIT}core_cable#{len(self._vfCableNodes)}"

                vfCable = self._scene._vfc.new_cable(name)
                vfCable.explicit_cable_no_loop = (
                    True  # parts of a sticky cable are never a loop
                )
                self._vfCableNodes.append(vfCable)

                # start point -------------------
                i_connection = core_cable_indices[0]
                if isinstance(self.connections[i_connection], Circle):
                    if not self._isloop and (
                        i_connection == 0 or i_connection == len(self.connections) - 1
                    ):
                        pass
                    else:
                        vfCable.add_connection_poi(
                            self._get_or_create_sticky_point_node_for(i_connection), 0
                        )  # makes sure that the point is created, no friction

                # intermediate points ------------

                for i_connection in core_cable_indices:
                    connection = self.connections[i_connection]
                    friction = connection_aligned_friction_factors[i_connection]

                    if friction is None:
                        warnings.warn(
                            "Friction factor is None which is not allowed when using sticky cables, setting to 0"
                        )
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
                    if not self._isloop and (
                        i_connection == 0 or i_connection == len(self.connections) - 1
                    ):
                        pass
                    else:
                        vfCable.add_connection_poi(
                            self._get_or_create_sticky_point_node_for(i_connection), 0
                        )  # makes sure that the point is created

                # update the friction vector of the node
                vfCable.friction_factors = vfCable.friction_factors[1:-1]

            self._update_vfCable_scalar_properties()

        else:
            # reduce to a single cable node
            for node in self._vfCableNodes[1:]:
                self._scene._vfc.delete(node.name)
            self._vfCableNodes = self._vfCableNodes[0:1]

            for node in self._vfPoiNodes.values():
                self._scene._vfc.delete(node.name)
            self._vfPoiNodes.clear()

            cableNode = self._vfCableNodes[0]  # alias
            cableNode.explicit_cable_no_loop = self._explicit_no_loop

            cableNode.clear_connections()

            for connection, is_reversed, max_winding, offset in zip(
                self._pois, self._reversed, self._max_winding_angle, self._offsets
            ):

                friction = 0  # overruled later

                if isinstance(connection, Point):
                    self._vfNode.add_connection_poi(connection._vfNode, friction)
                if isinstance(connection, Circle):
                    self._vfNode.add_connection_sheave(
                        connection._vfNode,
                        is_reversed,
                        friction,
                        np.deg2rad(max_winding),
                        offset,
                    )

            # set friction

            # set the unknown friction index (if any)
            if self._isloop:
                if None in friction_factors_copy:
                    self._vfNode.unknown_friction_index = friction_factors_copy.index(
                        None
                    )
                else:
                    self._vfNode.unknown_friction_index = -1
                    # check that all entries at 0
                    if not all([f == 0 for f in friction_factors_copy]):
                        raise ValueError(
                            f"Invalid friction combination on {self.name}. If friction type 'Force' is specified on a looped cable then at least one of the points shall be set to 'Position' to absorb the resulting forces"
                        )

            # replace none friction by 0
            self._vfNode.friction_factors = [
                f if f is not None else 0 for f in friction_factors_copy
            ]

            self._update_vfCable_scalar_properties()
            self._vfNode.update()

    def _update_vfCable_scalar_properties(self):
        """Updates the lengths, masses and EA"""

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

    def _get_cable_points_at_mid_of_connections(self) -> list[tuple or None]:
        """Returns the 3d points at the mid of the connections.
        For points this is just the point,
        for circles or round this is the mid of the section on the circle.

        Inactive roundbars are returned as None

        ! This is a relatively slow function; it utilizes the drawing data to get the points !
        """

        # create a dummy copy of the cable to get the visual without interfering with the actual cable
        # and without sticky points
        #
        # with non_sticky_cable(self) as non_sticky:
        #
        #     n_free = 0
        #     n_circle = 3
        #     constant_pointcount = True
        #
        #     points, _ = non_sticky._vfNode.get_drawing_data(
        #         n_free, n_circle, constant_pointcount
        #     )
        #
        #     active_bars = list(non_sticky._vfNode.connected_bar_active)
        #
        # # loop over the connections,
        # # for each connection get the points that are on the connection (just check the distance)
        # cable_points = [np.array(p) for p in points]
        #
        # # for loops, the last connection is the same as the first connection
        # # but the visual breaks half-way the circle.
        # # copy the last few point to the start of the list
        # # end exclude the last connection from being processed
        #
        # is_loop = self._isloop
        # connections_to_be_processed = self.connections
        # if is_loop:
        #     cable_points.insert(0, cable_points[-1])  # add the last point at the start
        #     cable_points.insert(
        #         0, cable_points[-2]
        #     )  # add the for-last point at the start
        #     connections_to_be_processed = connections_to_be_processed[:-1]
        #
        # # tolerance for the distance
        # #
        # tolerance = self.diameter / 100
        # tolerance = max(tolerance, 1e-1)
        #
        # connection_points = []
        #

        # the easy way:
        with non_sticky_cable(self) as non_sticky:
            points = non_sticky._vfNode.get_connector_center_segment_positions()
            active_bars = list(non_sticky._vfNode.connected_bar_active)

        # check for non-active roundbars
        # and set the points to None

        assert len(points) == len(
            self.connections
        ), "Internal error in _get_cable_points_at_mid_of_connections returned wrong number of points"

        for i, c in enumerate(self.connections):
            if isinstance(c, Circle):
                if c.is_roundbar:
                    active = active_bars.pop(0)
                    if active:
                        pass
                    else:
                        assert points[i] == (
                            0,
                            0,
                            0,
                        ), "Internal error in _get_cable_points_at_mid_of_connections, non-active roundbar has non-zero position"
                        points[i] = None

        return points

    @node_setter_manageable
    def set_length_for_tension(self, target_tension):
        """Given the actual geometry and EA of the cable, change the length such that
        the tension in the cable becomes the supplied tension
        """

        # F = stretch * EA / L
        # so : L = L0*EA / (F + EA)

        self.length = self.actual_length * self.EA / (target_tension + self.EA)

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

        self._update_vfNodes()
        # self._update_vfCable_scalar_properties() # done by update vfNodes

        for node in self._vfCableNodes:
            node.update()

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

        # if np.any(self._friction_force_factor):
        #     code.append(f"s['{self.name}'].friction = {self._friction_force_factor}")

        if any(
            [_ is not FrictionType.No for _ in self._friction_type]
        ):  # friction is active

            code.append("# friction, first set values, then enable")

            if any([_ is FrictionType.Force for _ in self._friction_type]):
                code.append(
                    f"s['{self.name}'].friction_force_factor = {self._friction_force_factor}"
                )

            if any([_ is FrictionType.Position for _ in self._friction_type]):
                code.append(
                    f"s['{self.name}'].friction_point_cable = {self._friction_point_cable}"
                )

                if any([_ is not None for _ in self._friction_point_connection]):
                    code.append(
                        f"s['{self.name}'].friction_point_connection = {self._friction_point_connection}"
                    )

            code.append(f"s['{self.name}'].friction_type = {self._friction_type}")

        if self._explicit_no_loop:
            code.append(f"s['{self.name}']._set_no_loop()")

        return "\n".join(code)
