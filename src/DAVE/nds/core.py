# pylint: disable=protected-access

"""These are the core-connected classes for DAVE nodes"""

import logging
from math import floor
from typing import Tuple

from .helpers import *
from .abstracts import *
from .mixins import *
from .geometry import *
from .enums import *
from .mixins import HasParentCore
from .trimesh import TriMeshSource

from ..settings import (
    VF_NAME_SPLIT,
    RENDER_CURVE_RESOLUTION,
    RENDER_CATENARY_RESOLUTION,
)
from ..settings_visuals import RESOLUTION_CABLE_OVER_CIRCLE, RESOLUTION_CABLE_SAG
from ..tools import *


DEFAULT_WINDING_ANGLE = 999  # for cables


class RigidBody(Frame):
    """A Rigid body, internally composed of an axis, a point (cog) and a force (gravity)"""

    def __init__(self, scene, name: str):
        # Some checks on properties of the node to make sure MRO is going well
        assert (
            getattr(self, "_vfPoi", None) is None
        ), "A Poi is already present in the core, error in constructor sequence?"
        assert (
            getattr(self, "_vfForce", None) is None
        ), "A Force is already present in the core, error in constructor sequence?"

        super().__init__(scene=scene, name=name)

        # The axis is the Node
        # poi and force are added separately

        p = scene._vfc.new_poi(name + VF_NAME_SPLIT + "cog")
        p.parent = self._vfNode

        g = scene._vfc.new_force(name + VF_NAME_SPLIT + "gravity")
        g.parent = p

        self._vfPoi = p
        self._vfForce = g

    # override the following properties
    # - name : sets the names of poi and force as well

    def _delete_vfc(self):
        super()._delete_vfc()
        self._scene._vfc.delete(self._vfPoi.name)
        self._scene._vfc.delete(self._vfForce.name)

    def _on_name_changed(self):
        """Called when the name of the node changes"""
        super()._on_name_changed()
        self._vfPoi.name = self.name + VF_NAME_SPLIT + "cog"
        self._vfForce.name = self.name + VF_NAME_SPLIT + "gravity"

    @property
    def footprint(self) -> tuple[tuple[float, float, float]]:
        """Sets the footprint vertices. Supply as an iterable with each element containing three floats"""
        return Frame.footprint.fget(self)

    @footprint.setter
    def footprint(self, value):
        Frame.footprint.fset(self, value)  # https://bugs.python.org/issue14965

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
    def cogx(self) -> float:
        """x-component of cog position [m] (local axis)"""
        return self.cog[0]

    @property
    def cogy(self) -> float:
        """y-component of cog position [m] (local axis)"""
        return self.cog[1]

    @property
    def cogz(self) -> float:
        """z-component of cog position [m] (local axis)"""
        return self.cog[2]

    @property
    def cog(self) -> tuple[float, float, float]:
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
    def mass(self) -> float:
        """Static mass of the body [mT]

        See Also: inertia
        """
        return self._vfForce.force[2] / -self._scene.g

    @mass.setter
    @node_setter_manageable
    @node_setter_observable
    def mass(self, newmass):
        assert1f(newmass)
        if newmass == 0:
            self.inertia_radii = (0, 0, 0)
        self.inertia = newmass
        self._vfForce.force = (0, 0, -self._scene.g * newmass)

    def dissolve_some(self):
        """A RigidBody can only be dissolved if it has no mass, in that case it is actually a frame"""
        return super().dissolve_some()

    def dissolve(self):
        if self.mass == 0:
            return Frame.dissolve(self)

        else:
            raise ValueError(
                f"Cannot dissolve RigidBody {self.name} with mass {self.mass}. Only massless rigidbodies can be dissolved."
            )

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\ns.new_rigidbody(name='{}',".format(self.name)
        code += "\n                mass={:.6g},".format(self.mass)
        code += "\n                cog=({:.6g},".format(self.cog[0])
        code += "\n                     {:.6g},".format(self.cog[1])
        code += "\n                     {:.6g}),".format(self.cog[2])

        if self.parent_for_export:
            code += "\n                parent='{}',".format(self.parent_for_export.name)

        code += self._export_frame_property_code()
        code += "\n                )"  # end of new_rigidbody

        code += self.add_footprint_python_code()

        return code


RigidBody._valid_parent_types = (Frame, NoneType)


class Force(NodeCoreConnected, HasParentCore):
    """A Force models a force and moment on a poi.

    Both are expressed in the global axis system.

    """

    _valid_parent_types = (Point,)

    def __init__(self, scene, name):
        scene.assert_name_available(name)
        self._vfNode = scene._vfc.new_force(name)

        super().__init__(scene=scene, name=name)

    def depends_on(self) -> list:
        return HasParentCore.depends_on(self)

    def change_parent_to(self, new_parent):
        self.parent = new_parent

    @property
    def force(self) -> tuple[float, float, float]:
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
    def fx(self) -> float:
        """The global x-component of the force [kN] (global axis)"""
        return self.force[0]

    @fx.setter
    @node_setter_manageable
    @node_setter_observable
    def fx(self, var):
        a = self.force
        self.force = (var, a[1], a[2])

    @property
    def fy(self) -> float:
        """The global y-component of the force [kN]  (global axis)"""
        return self.force[1]

    @fy.setter
    @node_setter_manageable
    @node_setter_observable
    def fy(self, var):
        a = self.force
        self.force = (a[0], var, a[2])

    @property
    def fz(self) -> float:
        """The global z-component of the force [kN]  (global axis)"""

        return self.force[2]

    @fz.setter
    @node_setter_manageable
    @node_setter_observable
    def fz(self, var):
        a = self.force
        self.force = (a[0], a[1], var)

    @property
    def moment(self) -> tuple[float, float, float]:
        """Moment [kNm,kNm,kNm] (global).

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
    def mx(self) -> float:
        """The global x-component of the moment [kNm]  (global axis)"""
        return self.moment[0]

    @mx.setter
    @node_setter_manageable
    @node_setter_observable
    def mx(self, var):
        a = self.moment
        self.moment = (var, a[1], a[2])

    @property
    def my(self) -> float:
        """The global y-component of the moment [kNm]  (global axis)"""
        return self.moment[1]

    @my.setter
    @node_setter_manageable
    @node_setter_observable
    def my(self, var):
        a = self.moment
        self.moment = (a[0], var, a[2])

    @property
    def mz(self) -> float:
        """The global z-component of the moment [kNm]  (global axis)"""
        return self.moment[2]

    @mz.setter
    @node_setter_manageable
    @node_setter_observable
    def mz(self, var):
        a = self.moment
        self.moment = (a[0], a[1], var)

    @property
    def is_global(self) -> bool:
        """True if the force and moment are expressed in the global axis system. False if they are expressed in the local axis system, aka followers [-]"""
        return self._vfNode.is_global

    @is_global.setter
    def is_global(self, value: bool):
        assertBool(value, "is_global")
        self._vfNode.is_global = value

    @property
    def global_force(self) -> tuple[float, float, float]:
        """The force in the global axis system [kN,kN,kN]"""
        self._vfNode.update()
        return self._vfNode.global_force

    @property
    def global_moment(self) -> tuple[float, float, float]:
        """The moment in the global axis system [kNm,kNm,kNm]"""
        self._vfNode.update()
        return self._vfNode.global_moment

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        # new_force(self, name, parent=None, force=None, moment=None):

        code += "\ns.new_force(name='{}',".format(self.name)
        code += "\n            parent='{}',".format(self.parent_for_export.name)

        if not self.is_global:
            code += "\n            local=True,"

        code += "\n            force=({:.6g}, {:.6g}, {:.6g}),".format(*self.force)
        code += "\n            moment=({:.6g}, {:.6g}, {:.6g}) )".format(*self.moment)
        return code


class WindOrCurrentArea(NodeCoreConnected, HasParentCore):
    """Abstract Based class for wind and current areas."""

    _valid_parent_types = (Point,)

    # defined in the derived classes

    def __init__(self, scene, name):
        scene.assert_name_available(name)
        self._vfNode = scene._vfc.new_wind(name)

        super().__init__(scene=scene, name=name)

    def depends_on(self) -> list:
        return [self.parent]

    def change_parent_to(self, new_parent):
        self.parent = new_parent

    def Ae_for_global_direction(self, global_direction):
        """Returns the effective area in the provided global direction, see"""

        if self.parent.parent is not None:
            dir = self.parent.parent.to_glob_direction(self.direction)
        else:
            dir = self.direction

        if self.areakind == AreaKind.SPHERE:
            return self.A
        elif self.areakind == AreaKind.PLANE:
            return self.A * abs(np.dot(global_direction, dir))
        elif self.areakind == AreaKind.CYLINDER:
            dot = np.dot(global_direction, dir)
            return self.A * np.sqrt(1 - dot**2)
        else:
            raise ValueError("Unknown area-kind")

    @property
    def force(self) -> tuple[float, float, float]:
        """The x,y and z components of the force [kN,kN,kN] (global axis)"""
        return self._vfNode.force

    @property
    def fx(self) -> float:
        """The global x-component of the force [kN] (global axis)"""
        return self.force[0]

    @property
    def fy(self) -> float:
        """The global y-component of the force [kN]  (global axis)"""
        return self.force[1]

    @property
    def fz(self) -> float:
        """The global z-component of the force [kN]  (global axis)"""

        return self.force[2]

    @property
    def A(self) -> float:
        """Total area [m2]. See also Ae"""
        return self._vfNode.A0

    @A.setter
    def A(self, value):
        assert1f_positive_or_zero(value, "Area")
        self._vfNode.A0 = value

    @property
    def Ae(self) -> float:
        """Effective area [m2]. This is the projection of the total to the actual wind/current direction. Read only."""
        return self._vfNode.Ae

    @property
    def Cd(self) -> float:
        """Cd coefficient [-]"""
        return self._vfNode.Cd

    @Cd.setter
    def Cd(self, value):
        assert1f_positive_or_zero(value, "Cd")
        self._vfNode.Cd = value

    @property
    def direction(self) -> tuple[float, float, float]:
        """Depends on 'areakind'. For 'plane' this is the direction of the normal of the plane, for 'cylindrical' this is
        the direction of the axis and for 'sphere' this is not used [m,m,m]"""
        return self._vfNode.direction

    @direction.setter
    def direction(self, value):
        assert3f(value, "direction")
        assert np.linalg.norm(value) > 0, ValueError("direction can not be 0,0,0")

        self._vfNode.direction = value

    @property
    def areakind(self) -> AreaKind:
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
        code += f"\n            A={self.A:.6g}, "
        code += f"\n            Cd={self.Cd:.6g}, "
        if self.areakind != AreaKind.SPHERE:
            code += "\n            direction=({:.6g},{:.6g},{:.6g}),".format(
                *self.direction
            )
        code += f"\n            areakind={str(self.areakind)})"

        return code


class WindArea(WindOrCurrentArea):
    # _valid_parent_types = (Point, )

    def __init__(self, scene, name):
        super().__init__(scene=scene, name=name)
        self._vfNode.isWind = True

    def give_python_code(self):
        return self._give_python_code("new_windarea")


class CurrentArea(WindOrCurrentArea):
    # _valid_parent_types = (Point,)

    def __init__(self, scene, name):
        super().__init__(scene=scene, name=name)
        self._vfNode.isWind = True

    def give_python_code(self):
        return self._give_python_code("new_currentarea")


class ContactBall(NodeCoreConnected, HasParentCore):
    """A ContactBall is a linear elastic ball which can contact with ContactMeshes.

    It is modelled as a sphere around a Poi. Radius and stiffness can be controlled using radius and k.

    The force is applied on the Poi and it not registered separately.
    """

    _valid_parent_types = (Point,)

    def __init__(self, scene, name: str):
        scene.assert_name_available(name)
        self._vfNode = scene._vfc.new_contactball(name)

        super().__init__(scene=scene, name=name)

        self._meshes = list()

    def change_parent_to(self, new_parent):
        self.parent = new_parent

    def depends_on(self) -> list:
        deps = HasParentCore.depends_on(self)
        deps.extend(self._meshes)
        return deps

    @property
    def can_contact(self) -> bool:
        """True if the ball is currently perpendicular to at least one of the faces of one of the meshes. So when contact is possible. To check if there is contact use "force".
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
    def contactpoint(self) -> tuple[float, float, float]:
        """Nearest point on the nearest mesh, if contact [m,m,m] (global)"""
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
    def meshes_names(self) -> tuple[str]:
        """List with the names of the meshes"""
        return tuple([m.name for m in self._meshes])  # type: ignore

    @property
    def radius(self) -> float:
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
    def k(self) -> float:
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
        code += "\n                  radius={:.6g},".format(self.radius)
        code += "\n                  k={:.6g},".format(self.k)
        code += "\n                  meshes = [ "

        for m in self._meshes:
            code += '"' + m.name + '",'
        code = code[:-1] + "])"

        return code


class SPMT(NodeCoreConnected, HasParentCore):
    """An SPMT is a Self-propelled modular transporter

    These are platform vehicles

    ============  =======
    0 0 0 0 0 0   0 0 0 0

    This SPMT node models the wheels and hydraulics of a single suspension system.

    A set of wheels is called an "axle". The hydraulics are modelled as a linear spring.
    The axles can make contact with a contact shape.

    The positions of the axles are controlled by n_length, n_width, spacing_length and spacing_width.
    The hydraulics are controlled by reference_extension, reference_force and k.

    Setting use_friction to True (default) adds friction such that all contact-forces are purely vertical.
    Setting use_friction to False will make contact-forces perpendicular to the contacted surface.

    """

    _valid_parent_types = (Frame,)

    def __init__(self, scene, name: str):
        scene.assert_name_available(name)
        self._vfNode = scene._vfc.new_spmt(name)

        super().__init__(scene=scene, name=name)

        self._meshes = list()

        # These are set by Scene.new_spmt
        self._k = None
        self._reference_extension = None
        self._reference_force = None
        self._spacing_length = None
        self._spacing_width = None
        self._n_length = None
        self._n_width = None

    def change_parent_to(self, new_parent):
        self.parent = new_parent

    def depends_on(self) -> list:
        deps = HasParentCore.depends_on(self)
        deps.extend(self._meshes)
        return deps

    # read-only properties

    @property
    def force(self) -> tuple[float]:
        """Returns the force component perpendicular to the SPMT in each of the axles (negative mean uplift) [kN]"""
        return self._vfNode.force

    @property
    def contact_force(self) -> tuple[tuple[float]]:
        """Returns the contact force in each of the axles (global) [kN,kN,kN]"""
        return self._vfNode.forces

    @property
    def compression(self) -> float:
        """Returns the total compression (negative means uplift) [m]"""
        return self._vfNode.compression

    @property
    def extensions(self) -> tuple[float]:
        """Returns the extension of each of the axles (bottom of wheel to top of spmt) [m]"""
        return tuple(self._vfNode.extensions)

    @property
    def max_extension(self) -> float:
        """Maximum extension of the axles [m]
        See Also: extensions"""
        return max(self.extensions)

    @property
    def min_extension(self) -> float:
        """Minimum extension of the axles [m]
        See Also: extensions"""
        return min(self.extensions)

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

    # axles and stiffness are combined
    def _update_vfNode(self):
        """Updates vfNode with stiffness and axles"""
        offx = (self._n_length - 1) * self._spacing_length / 2
        offy = (self._n_width - 1) * self._spacing_width / 2
        self._vfNode.clear_axles()

        for ix in range(self._n_length):
            for iy in range(self._n_width):
                self._vfNode.add_axle(
                    ix * self._spacing_length - offx, iy * self._spacing_width - offy, 0
                )

        n_axles = self._n_length * self._n_width
        self._vfNode.k = self._k / (n_axles * n_axles)
        self._vfNode.nominal_length = (
            self._reference_extension + self._reference_force / self._k
        )

    @property
    def n_width(self) -> int:
        """number of axles in transverse direction [-]"""
        return self._n_width

    @n_width.setter
    @node_setter_manageable
    @node_setter_observable
    def n_width(self, value):
        assert1i_positive_or_zero(value, "n_width")
        self._n_width = value
        self._update_vfNode()

    @property
    def n_length(self) -> int:
        """number of axles in length direction [-]"""
        return self._n_length

    @n_length.setter
    @node_setter_manageable
    @node_setter_observable
    def n_length(self, value):
        assert1i_positive_or_zero(value, "n_length")
        self._n_length = value
        self._update_vfNode()

    @property
    def spacing_width(self) -> float:
        """distance between axles in transverse direction [m]"""
        return self._spacing_width

    @spacing_width.setter
    @node_setter_manageable
    @node_setter_observable
    def spacing_width(self, value):
        assert1f_positive_or_zero(value, "spacing_width")
        self._spacing_width = value
        self._update_vfNode()

    @property
    def spacing_length(self) -> float:
        """distance between axles in length direction [m]"""
        return self._spacing_length

    @spacing_length.setter
    @node_setter_manageable
    @node_setter_observable
    def spacing_length(self, value):
        assert1f_positive_or_zero(value, "spacing_length")
        self._spacing_length = value
        self._update_vfNode()

    @property
    def reference_force(self) -> float:
        """total force (sum of all axles) when at reference extension [kN]"""
        return self._reference_force

    @reference_force.setter
    @node_setter_manageable
    @node_setter_observable
    def reference_force(self, value):
        assert1f_positive_or_zero(value, "reference_force")
        self._reference_force = value
        self._update_vfNode()

    @property
    def reference_extension(self) -> float:
        """Distance between top of SPMT and bottom of wheel at which compression is zero [m]"""
        return self._reference_extension

    @reference_extension.setter
    @node_setter_manageable
    @node_setter_observable
    def reference_extension(self, value):
        """nominal extension of axles for reference force [m]"""
        assert1f_positive_or_zero(value, "reference_extension")
        self._reference_extension = value
        self._update_vfNode()

    @property
    def k(self) -> float:
        """Vertical stiffness of all axles together [kN/m]"""
        return self._k

    @k.setter
    @node_setter_manageable
    @node_setter_observable
    def k(self, value):
        assert1f_positive_or_zero(value, "k")
        self._k = value
        self._update_vfNode()

    # ==== friction ====

    @property
    def use_friction(self) -> bool:
        """Apply friction between wheel and surface such that resulting force is vertical [True/False]
        False: Force is perpendicular to the surface
        True: Force is vertical
        """
        return self._vfNode.use_friction

    @use_friction.setter
    def use_friction(self, value):
        assertBool(value, "use friction")
        self._vfNode.use_friction = value

    # === control meshes ====

    @property
    def meshes(self) -> tuple:
        """List of contact-mesh nodes. If empty list then the SPMT can contact all contact meshes.
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
    def meshes_names(self) -> tuple[str]:
        """List with the names of the meshes"""
        return tuple([m.name for m in self._meshes])  # type: ignore

    # === control axles ====

    @property
    def axles(self) -> tuple[tuple[float, float, float]]:
        """Axles is a list axle positions [m,m,m] (parent axis)
        Each entry is a (x,y,z) entry which determines the location of the axle on SPMT. This is relative to the parent of the SPMT.

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
        code = ["# code for {}".format(self.name)]

        code.append(f"s.new_spmt(name='{self.name}',")
        code.append(f"           parent='{self.parent_for_export.name}',")
        code.append(f"           reference_force = {self.reference_force:.6g},")
        code.append(f"           reference_extension = {self.reference_extension:.6g},")
        code.append(f"           k = {self.k},")
        code.append(f"           spacing_length = {self.spacing_length:.6g},")
        code.append(f"           spacing_width = {self.spacing_width:.6g},")
        code.append(f"           n_length = {self.n_length},")
        code.append(f"           n_width = {self.n_width},")

        if self._meshes:
            code.append("                  meshes = [ ")
            for m in self._meshes:
                code.append('"' + m.name + '",')
            code.append("                           ],")
        code.append("            )")

        return "\n".join(code)


class HydSpring(NodeCoreConnected, HasParentCore):
    """A HydSpring models a linearized hydrostatic spring.

    The cob (center of buoyancy) is defined in the parent axis system.
    All other properties are defined relative to the cob.

    """

    _valid_parent_types = (Frame,)

    def __init__(self, scene, name):
        scene.assert_name_available(name)

        self._vfNode = scene._vfc.new_hydspring(name)
        super().__init__(scene=scene, name=name)

    def depends_on(self) -> list:
        return HasParentCore.depends_on(self)

    def change_parent_to(self, new_parent):
        self.parent = new_parent

    @property
    def cob(self) -> tuple[float, float, float]:
        """Center of buoyancy in (parent axis) [m,m,m]"""
        return self._vfNode.position

    @cob.setter
    @node_setter_manageable
    @node_setter_observable
    def cob(self, val):
        assert3f(val)
        self._vfNode.position = val

    @property
    def BMT(self) -> float:
        """Vertical distance between cob and metacenter for roll [m]"""
        return self._vfNode.BMT

    @BMT.setter
    @node_setter_manageable
    @node_setter_observable
    def BMT(self, val):
        self._vfNode.BMT = val

    @property
    def BML(self) -> float:
        """Vertical distance between cob and metacenter for pitch [m]"""
        return self._vfNode.BML

    @BML.setter
    @node_setter_manageable
    @node_setter_observable
    def BML(self, val):
        self._vfNode.BML = val

    @property
    def COFX(self) -> float:
        """Horizontal x-position Center of Floatation (center of waterplane area), relative to cob [m]"""
        return self._vfNode.COFX

    @COFX.setter
    @node_setter_manageable
    @node_setter_observable
    def COFX(self, val):
        self._vfNode.COFX = val

    @property
    def COFY(self) -> float:
        """Horizontal y-position Center of Floatation (center of waterplane area), relative to cob [m]"""
        return self._vfNode.COFY

    @COFY.setter
    @node_setter_manageable
    @node_setter_observable
    def COFY(self, val):
        self._vfNode.COFY = val

    @property
    def kHeave(self) -> float:
        """Heave stiffness [kN/m]"""
        return self._vfNode.kHeave

    @kHeave.setter
    @node_setter_manageable
    @node_setter_observable
    def kHeave(self, val):
        self._vfNode.kHeave = val

    @property
    def waterline(self) -> float:
        """Waterline-elevation relative to cob for un-stretched heave-spring. Positive if cob is below the waterline (which is where is normally is) [m]"""
        return self._vfNode.waterline

    @waterline.setter
    @node_setter_manageable
    @node_setter_observable
    def waterline(self, val):
        self._vfNode.waterline = val

    @property
    def displacement_kN(self) -> float:
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


# =========== Parent and Trimesh


class ContactMesh(NodeCoreConnected, HasParentCore, HasTrimesh):
    """A ContactMesh is a tri-mesh with an axis parent"""

    _valid_parent_types = (
        Frame,
        NoneType,
    )

    def __init__(self, scene, name):
        logging.info("ContactMesh.__init__")
        scene.assert_name_available(name)

        self._vfNode = scene._vfc.new_contactmesh(name)
        super().__init__(scene=scene, name=name)

    def depends_on(self) -> list:
        return HasParentCore.depends_on(self)

    def change_parent_to(self, new_parent):
        HasTrimesh.change_parent_to(self, new_parent)

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\nmesh = s.new_contactmesh(name='{}'".format(self.name)
        if self.parent_for_export:
            code += ", parent='{}')".format(self.parent_for_export.name)
        else:
            code += ")"
        code += "\nmesh.trimesh.load_file(r'{}', scale = ({:.6g},{:.6g},{:.6g}), rotation = ({:.6g},{:.6g},{:.6g}), offset = ({:.6g},{:.6g},{:.6g}))".format(
            self.trimesh._path,
            *self.trimesh._scale,
            *self.trimesh._rotation,
            *self.trimesh._offset,
        )

        return code


class Buoyancy(NodeCoreConnected, HasParentCore, HasTrimesh):
    """Buoyancy provides a buoyancy force based on a buoyancy mesh. The mesh is triangulated and chopped at the instantaneous flat water surface. Buoyancy is applied as an upwards force that the center of buoyancy.
    The calculation of buoyancy is as accurate as the provided geometry.

    There as no restrictions to the size or aspect ratio of the panels. It is excellent to model as box using 6 faces. Using smaller panels has a negative effect on performance.

    The normals of the panels should point towards to water.
    """

    # init parent and name are fully derived from NodeWithParent
    # _vfNode is a buoyancy

    _valid_parent_types = (Frame,)

    def __init__(self, scene, name):
        logging.info("Buoyancy.__init__")
        scene.assert_name_available(name)

        self._vfNode = scene._vfc.new_buoyancy(name)
        super().__init__(scene=scene, name=name)

    def depends_on(self) -> list:
        return HasParentCore.depends_on(self)

    def change_parent_to(self, new_parent):
        HasTrimesh.change_parent_to(self, new_parent)

    def update(self):
        self._vfNode.reloadTrimesh()

    @property
    def cob(self) -> tuple[tuple[float, float, float]]:
        """GLOBAL position of the center of buoyancy [m,m,m] (global axis)"""
        return self._vfNode.cob

    @property
    def cob_local(self) -> tuple[tuple[float, float, float]]:
        """Position of the center of buoyancy [m,m,m] (local axis)"""

        return self.parent.to_loc_position(self.cob)

    @property
    def displacement(self) -> float:
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


class Tank(NodeCoreConnected, HasParentCore, HasTrimesh):
    """Tank provides a fillable tank based on a mesh. The mesh is triangulated and chopped at the instantaneous flat fluid surface. Gravity is applied as an downwards force that the center of fluid.
    The calculation of fluid volume and center is as accurate as the provided geometry.

    There as no restrictions to the size or aspect ratio of the panels. It is excellent to model as box using 6 faces. Using smaller panels has a negative effect on performance.

    The normals of the panels should point *away* from the fluid. This means that the same basic shapes can be used for both buoyancy and tanks.
    """

    # init parent and name are fully derived from NodeWithParent
    # _vfNode is a tank

    _valid_parent_types = (Frame,)

    def __init__(self, scene, name):
        logging.info("Tank.__init__")
        scene.assert_name_available(name)

        self._vfNode = scene._vfc.new_tank(name)
        super().__init__(scene=scene, name=name)

        self._inertia = scene._vfc.new_pointmass(self.name + VF_NAME_SPLIT + "inertia")

    def depends_on(self) -> list:
        return HasParentCore.depends_on(self)

    def change_parent_to(self, new_parent):
        HasTrimesh.change_parent_to(self, new_parent)

    def update(self):
        self._vfNode.reloadTrimesh()

        # update inertia
        self._inertia.parent = self.parent._vfNode
        self._inertia.position = self.cog_local
        self._inertia.inertia = self.volume * self.used_density

    def _delete_vfc(self):
        self._scene._vfc.delete(self._inertia.name)
        super()._delete_vfc()

    @property
    def free_flooding(self) -> bool:
        """Tank is filled till global waterline (aka: damaged) [bool]"""
        return self._vfNode.free_flooding

    @free_flooding.setter
    def free_flooding(self, value):
        assert isinstance(value, bool), ValueError(
            f"free_flooding shall be a bool, you passed a {type(value)}"
        )
        self._vfNode.free_flooding = value

    @property
    def permeability(self) -> float:
        """Permeability is the fraction of the meshed volume that can be filled with fluid [-]"""
        return self._vfNode.permeability

    @permeability.setter
    def permeability(self, value):
        assert1f_positive_or_zero(value)
        self._vfNode.permeability = value

    @property
    def cog(self) -> tuple[tuple[float, float, float]]:
        """Global position of the center of volume / gravity [m,m,m] (global)"""
        return self._vfNode.cog

    @property
    def cog_local(self) -> tuple[tuple[float, float, float]]:
        """Center of gravity [m,m,m] (parent axis)"""
        return self.parent.to_loc_position(self.cog)

    @property
    def cog_when_full_global(self) -> tuple[tuple[float, float, float]]:
        """Global position of the center of volume / gravity of the tank when it is filled [m,m,m] (global)"""
        return self.parent.to_glob_position(self._vfNode.cog_when_full)

    @property
    def cog_when_full(self) -> tuple[float, float, float]:
        """LOCAL position of the center of volume / gravity of the tank when it is filled [m,m,m] (parent axis)"""
        return self._vfNode.cog_when_full

    @property
    def cogx_when_full(self) -> float:
        """x position of the center of volume / gravity of the tank when it is filled [m] (parent axis)"""
        return self._vfNode.cog_when_full[0]

    @property
    def cogy_when_full(self) -> float:
        """y position of the center of volume / gravity of the tank when it is filled [m] (parent axis)"""
        return self._vfNode.cog_when_full[1]

    @property
    def cogz_when_full(self) -> float:
        """z position of the center of volume / gravity of the tank when it is filled [m] (parent axis)"""
        return self._vfNode.cog_when_full[2]

    @property
    def fill_pct(self) -> float:
        """Amount of volume in tank as percentage of capacity [%]"""
        if self.capacity == 0:
            return 0
        return 100 * self.volume / self.capacity

    @fill_pct.setter
    @node_setter_observable
    def fill_pct(self, value):
        if (value < 0) and (value > -0.01):
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
    def level_global(self) -> float:
        """The fluid plane elevation in the global axis system [m]
        Setting this adjusts the volume"""
        return self._vfNode.fluid_level_global

    @level_global.setter
    @node_setter_manageable
    @node_setter_observable
    def level_global(self, value):
        assert1f(value)
        self._vfNode.fluid_level_global = value

    @property
    def volume(self) -> float:
        """The actual volume of fluid in the tank [m3]
        Setting this adjusts the fluid level"""
        return self._vfNode.volume

    @volume.setter
    @node_setter_observable
    def volume(self, value):
        assert1f_positive_or_zero(value, "Volume")
        self._vfNode.volume = value

    @property
    def used_density(self) -> float:
        """Density of the fluid in the tank [mT/m3]"""
        if self.density > 0:
            return self.density
        else:
            return self._scene.rho_water

    @property
    def density(self) -> float:
        """Density of the fluid in the tank. Density < 0 means use outside water density. See also used_density [mT/m3]"""
        return self._vfNode.density

    @density.setter
    @node_setter_manageable
    @node_setter_observable
    def density(self, value):
        assert1f(value)
        self._vfNode.density = value

    @property
    def capacity(self) -> float:
        """Fillable volume of the tank calcualted as mesh volume times permeability [m3]
        This is calculated from the defined geometry and permeability.
        See also: mesh_volume"""
        return self._vfNode.capacity

    @property
    def mesh_volume(self) -> float:
        """Volume enclosed by the mesh the tank [m3]
        This is calculated from the defined geometry and does not account for permeability.
        See also: capacity"""
        return self._vfNode.capacity / self._vfNode.permeability

    @property
    def ullage(self) -> float:
        """Ullage of the tank [m]
        The ullage is the distance between a measurement point and the fluid surface. The point is [xf,yf,zv] where
        xf and yf are the x and y coordinates (local) of the center of fluid when the tank is full. zv is the largest z value
        of all the vertices of the tank.
        The measurement direction is in local z-direction. If the tank is under an angle then this is not perpendicular to the fluid.
        It is possible that this definition results in an ullage larger than the physical tank depth. In that case the physical depth of
        the tank is returned instead.
        """
        return self._vfNode.ullage

    @property
    def sounding(self) -> float:
        """Sounding of the tank [m]
        The sounding is the distance between a measurement point and the fluid surface. The point is [xf,yf,zv] where
        xf and yf are the x and y coordinates (local) of the center of fluid when the tank is full. zv is the lowest z value
        of all the vertices of the tank.
        The measurement direction is in local z-direction. If the tank is under an angle then this is not perpendicular to the fluid.
        It is possible that this definition results in a sounding larger than the physical tank depth. In that case the physical depth of
        the tank is returned instead.
        """
        return self._vfNode.sounding

    def give_python_code(self):
        code = "# code for {}".format(self.name)
        code += "\nmesh = s.new_tank(name='{}',".format(self.name)

        if self.density != 1.025:
            code += f"\n          density={self.density:.6g},"

        if self.free_flooding:
            code += f"\n          free_flooding=True,"

        code += "\n          parent='{}')".format(self.parent_for_export.name)

        if self.trimesh._invert_normals:
            code += "\nmesh.trimesh.load_file(r'{}', scale = ({:.6g},{:.6g},{:.6g}), rotation = ({:.6g},{:.6g},{:.6g}), offset = ({:.6g},{:.6g},{:.6g}), invert_normals=True)".format(
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
        code += f"\ns['{self.name}'].volume = {self.volume:.6g}   # first load mesh, then set volume"

        return code


# -------- non-parent types


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

    def __init__(self, scene, name: str):
        scene.assert_name_available(name)
        self._vfNode = scene._vfc.new_cable(name)

        super().__init__(scene=scene, name=name)

        self._pois = list()
        self._reversed: List[bool] = list()
        self._friction: List[float] = list()
        self._max_winding_angle: List[float] = list()
        self._offsets: List[float] = list()

        self._render_as_tube = True
        self.do_color_by_tension = True
        self._friction_factor = -1  # deprecated
        """Negative means use default formulation"""

    def depends_on(self):
        return [*self._pois]

    @property
    def tension(self) -> float:
        """Tension in the cable [kN]"""
        return self._vfNode.tension

    @property
    def stretch(self) -> float:
        """Stretch of the cable [m]"""
        return self._vfNode.stretch

    @property
    def actual_length(self) -> float:
        """Current length of the cable: length + stretch [m]"""
        return self.length + self.stretch

    @property
    def length(self) -> float:
        """Length of the cable when in rest [m]"""
        return self._vfNode.Length

    @length.setter
    @node_setter_manageable
    @node_setter_observable
    def length(self, val):
        if val < 1e-9:
            if self.EA > 0:
                raise ValueError(
                    "Length shall be more than 0 if EA>0 (otherwise stiffness EA/L becomes infinite)"
                )
        if val < 0:
            raise ValueError("Length shall be more than 0")
        self._vfNode.Length = val

    @property
    def EA(self) -> float:
        """Stiffness of the cable [kN]"""
        return self._vfNode.EA

    @EA.setter
    @node_setter_manageable
    @node_setter_observable
    def EA(self, ea):
        self._vfNode.EA = ea

        try:
            self.length = self.length
        except ValueError as E:
            self.EA = 0
            raise E

    @property
    def diameter(self) -> float:
        """Diameter of the cable. Used when a cable runs over a circle. [m]"""
        return self._vfNode.diameter

    @diameter.setter
    @node_setter_manageable
    @node_setter_observable
    def diameter(self, diameter):
        self._vfNode.diameter = diameter

    @property
    def mass_per_length(self) -> float:
        """Mass per length of the cable [mT/m]"""
        return self._vfNode.mass_per_length

    @mass_per_length.setter
    @node_setter_manageable
    @node_setter_observable
    def mass_per_length(self, mass_per_length):
        self._vfNode.mass_per_length = mass_per_length

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
    def reversed(self) -> tuple[bool]:
        """Diameter of the cable. Used when a cable runs over a circle. [m]"""
        return tuple(self._reversed)

    @reversed.setter
    @node_setter_manageable
    @node_setter_observable
    def reversed(self, reversed):
        self._reversed = list(reversed)
        self._update_pois()

    @property
    def _isloop(self):
        if len(self.connections) < 2:
            return False
        return self.connections[0] == self.connections[-1]

    @property
    def solve_segment_lengths(self) -> bool:
        """If True then lengths of the segment are solved for a continuous tension distribution including weight. If false then the segment lengths are determined only on the geometry [bool]
        Note that the solution is typically not unique!"""
        return self._vfNode.solve_section_lengths

    @solve_segment_lengths.setter
    def solve_segment_lengths(self, value):
        assertBool(value, "solve_segment_lengths")
        self._vfNode.solve_section_lengths = value

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

        if self._isloop:
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

        self._update_pois()

    @property
    def angles_at_connections(self) -> tuple[float, ...]:
        """Change in cable direction at each of the connections [deg]"""
        return tuple(np.rad2deg(self._vfNode.angles_at_connections))

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
        self._update_pois()

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
        self._update_pois()

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
        return tuple(self._vfNode.friction_forces)

    @property
    def calculated_friction_factor(self) -> float or None:
        """The friction factor that was left for DAVE to calculate [-], only applicable to loops"""
        if self._isloop:
            return self._vfNode.calculated_unknown_friction_factor
        else:
            return None

    @property
    def friction_factors_as_calculated(self) -> tuple[float]:
        """The friction factors as calculated by DAVE [-], only applicable to loops"""
        if self._isloop:
            fr = list(self.friction)
            fr[
                self._vfNode.unkonwn_friction_index
            ] = self._vfNode.calculated_unknown_friction_factor
            return tuple(fr)
        else:
            return self.friction

    @property
    def segment_end_tensions(self) -> tuple[tuple[float]]:
        """Tensions at the ends of each of the cable segments [kN, kN]
        These are identical if the cable weight is zero.
        """
        segment_end_forces = self._vfNode.get_segment_end_tensions
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

        # are we switching from a line to a loop?
        if not was_loop and self._isloop:
            # yes, we are switching from a line to a loop
            # so we need to add a friction factor (None) at the start and set the unknown friction index
            self._friction.insert(0, None)
            self._vfNode.unkonwn_friction_index = 0

        if was_loop and not self._isloop:
            # switching from loop to line
            # pop the first friction factor
            self._friction.pop(0)
            self._vfNode.unkonwn_friction_index = -1

        self._update_pois()

    def get_points_for_visual(self):
        """A list of 3D locations which can be used for visualization"""
        points, tensions = self._vfNode.get_drawing_data(
            RESOLUTION_CABLE_SAG, RESOLUTION_CABLE_OVER_CIRCLE, False
        )
        return points

    def get_points_and_tensions_for_visual(self):
        """A list of 3D locations which can be used for visualization"""
        points, tensions = self._vfNode.get_drawing_data(
            RESOLUTION_CABLE_SAG, RESOLUTION_CABLE_OVER_CIRCLE, False
        )
        return points, tensions

    def get_points_for_visual_blender(self):
        """A list of 3D locations which can be used for visualization"""
        constant_point_count = True
        points, tensions = self._vfNode.get_drawing_data(
            RENDER_CATENARY_RESOLUTION, RENDER_CURVE_RESOLUTION, constant_point_count
        )
        return points

    def _add_connection_to_core(
        self,
        connection,
        reversed=False,
        friction=0,
        max_winding=DEFAULT_WINDING_ANGLE,
        offset=0,
    ):
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

    def _update_pois(self):
        self._vfNode.clear_connections()

        # sync length of reversed
        while len(self._reversed) < len(self._pois):
            self._reversed.append(False)
        self._reversed = self._reversed[0 : len(self._pois)]

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
        self._max_winding_angle = self._max_winding_angle[0 : len(self._pois)]

        # sync length of offsets
        while len(self._offsets) < len(self._pois):
            self._offsets.append(0)
        self._offsets = self._offsets[0 : len(self._pois)]

        for point, reversed, max_winding, offset in zip(
            self._pois, self._reversed, self._max_winding_angle, self._offsets
        ):
            self._add_connection_to_core(
                point, reversed, 0, max_winding, offset
            )  # friction will be overwritten later

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

        # if self.friction_factor >0:
        #     code.append(f"s['{self.name}'].friction_factor = {self.friction_factor}")

        if np.any([_ != DEFAULT_WINDING_ANGLE for _ in self._max_winding_angle]):
            code.append(
                f"s['{self.name}'].max_winding_angles = {self._max_winding_angle}"
            )

        if np.any([_ != 0 for _ in self._offsets]):
            code.append(f"s['{self.name}'].offsets = {self._offsets}")

        if np.any(self._friction):
            code.append(f"s['{self.name}'].friction = {self._friction}")

        return "\n".join(code)


class LC6d(NodeCoreConnected):
    """A LC6d models a Linear Connector with 6 dofs.

    It connects two Axis elements with six linear springs.

    The first axis system is called "main", the second is called "secondary". The difference is that
    the "main" axis system defines the directions of the stiffness values.

    The translational-springs are straight forward. The rotational springs may not be as intuitive. They are defined as:

      - rotation_x = arc-tan ( uy[0] / uy[1] )
      - rotation_y = arc-tan ( -ux[0] / ux[2] )
      - rotation_z = arc-tan ( ux[0] / ux [1] )

    which works fine for small rotations and rotations about only a single axis.

    Tip:
    It is better to use the "fixed" property of axis systems to create joints.

    """

    def __init__(self, scene, name: str):
        scene.assert_name_available(name)
        self._vfNode = scene._vfc.new_linearconnector6d(name)
        super().__init__(scene=scene, name=name)

        self._main = None
        self._secondary = None

    def depends_on(self):
        return [self._main, self._secondary]

    def try_swap(self, old: Frame, new: Frame) -> bool:
        """Try to swap existing main/secondary connection with the new frame. Returns True if the swap was successful. Checks global position"""
        if new is None:
            return False  # not an acceptable connection

        if not old.same_position_and_orientation(new, tol=1e-9):
            return False

        if self._main == old:
            self.main = new
            return True
        if self._secondary == old:
            self.secondary = new
            return True
        return False

    @property
    def stiffness(self) -> tuple[float, float, float, float, float, float]:
        """Stiffness of the connector: kx, ky, kz, krx, kry, krz in [kN/m and kNm/rad] (axis system of the main axis)"""
        return self._vfNode.stiffness

    @stiffness.setter
    @node_setter_manageable
    @node_setter_observable
    def stiffness(self, val):
        self._vfNode.stiffness = val

    @property
    def main(self) -> Frame:
        """Main axis system. This axis system dictates the axis system that the stiffness is expressed in
        #NOGUI"""
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
    def secondary(self) -> Frame:
        """Secondary (connected) axis system
        #NOGUI"""
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
    def fgx(self) -> float:
        """Force on main in global coordinate frame [kN]"""
        return self._vfNode.global_force[0]

    @property
    def fgy(self) -> float:
        """Force on main in global coordinate frame [kN]"""
        return self._vfNode.global_force[1]

    @property
    def fgz(self) -> float:
        """Force on main in global coordinate frame [kN]"""
        return self._vfNode.global_force[2]

    @property
    def force_global(self) -> tuple[float, float, float]:
        """Force on main in global coordinate frame [kN,kN,kN,kNm,kNm,kNm]"""
        return self._vfNode.global_force

    @property
    def mgx(self) -> float:
        """Moment on main in global coordinate frame [kNm]"""
        return self._vfNode.global_moment[0]

    @property
    def mgy(self) -> float:
        """Moment on main in global coordinate frame [kNm]"""
        return self._vfNode.global_moment[1]

    @property
    def mgz(self) -> float:
        """Moment on main in global coordinate frame [kNm]"""
        return self._vfNode.global_moment[2]

    @property
    def moment_global(self) -> tuple[float, float, float]:
        """Moment on main in global coordinate frame [kNm, kNm, kNm]"""
        return self._vfNode.global_moment

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_linear_connector_6d(name='{}',".format(self.name)
        code += "\n            main='{}',".format(self.main.name)
        code += "\n            secondary='{}',".format(self.secondary.name)
        code += "\n            stiffness=({:.6g}, {:.6g}, {:.6g}, ".format(
            *self.stiffness[:3]
        )
        code += "\n                       {:.6g}, {:.6g}, {:.6g}) )".format(
            *self.stiffness[3:]
        )

        return code


class Connector2d(NodeCoreConnected):
    """A Connector2d linear connector with acts both on linear displacement and angular displacement.

    * the linear stiffness is defined by k_linear and is defined over the actual shortest direction between nodeA and nodeB.
    * the angular stiffness is defined by k_angular and is defined over the actual smallest angle between the two systems.
    """

    def __init__(self, scene, name: str):
        scene.assert_name_available(name)
        self._vfNode = scene._vfc.new_connector2d(name)
        super().__init__(scene=scene, name=name)

        self._nodeA = None
        self._nodeB = None

    def depends_on(self):
        return [self._nodeA, self._nodeB]

    def try_swap(self, old: Frame, new: Frame) -> bool:
        """Try to swap existing main/secondary connection with the new frame. Returns True if the swap was successful. Checks global position"""
        if new is None:
            return False  # not an acceptable connection

        if not old.same_position_and_orientation(new, tol=1e-9):
            return False

        if self.nodeA == old:
            self.nodeA = new
            return True
        if self.nodeB == old:
            self.nodeB = new
            return True
        return False

    @property
    def angle(self) -> float:
        """Actual angle between nodeA and nodeB [deg] (read-only)"""
        return np.rad2deg(self._vfNode.angle)

    @property
    def force(self) -> float:
        """Actual force between nodeA and nodeB [kN] (read-only)"""
        return self._vfNode.force

    @property
    def moment(self) -> float:
        """Actual moment between nodeA and nodeB [kNm] (read-only)"""
        return self._vfNode.moment

    @property
    def axis(self) -> tuple[float, float, float]:
        """Actual rotation axis between nodeA and nodeB [m,m,m](read-only)"""
        return self._vfNode.axis

    @property
    def ax(self) -> float:
        """X component of actual rotation axis between nodeA and nodeB [deg](read-only)"""
        return self._vfNode.axis[0]

    @property
    def ay(self) -> float:
        """Y component of actual rotation axis between nodeA and nodeB [deg] (read-only)"""
        return self._vfNode.axis[1]

    @property
    def az(self) -> float:
        """Z component of actual rotation axis between nodeA and nodeB [deg] (read-only)"""
        return self._vfNode.axis[2]

    @property
    def k_linear(self) -> float:
        """Linear stiffness [kN/m]"""
        return self._vfNode.k_linear

    @k_linear.setter
    @node_setter_manageable
    @node_setter_observable
    def k_linear(self, value):
        self._vfNode.k_linear = value

    @property
    def k_angular(self) -> float:
        """Angular stiffness [kNm/rad]"""
        return self._vfNode.k_angular

    @k_angular.setter
    @node_setter_manageable
    @node_setter_observable
    def k_angular(self, value):
        self._vfNode.k_angular = value

    @property
    def nodeA(self) -> Frame:
        """Connected axis system A
        #NOGUI"""
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
        """Connected axis system B
        #NOGUI"""
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
        code += "\n            k_linear ={:.6g},".format(self.k_linear)
        code += "\n            k_angular ={:.6g})".format(self.k_angular)

        return code


class Beam(NodeCoreConnected):
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

    def __init__(self, scene, name: str):
        scene.assert_name_available(name)
        self._vfNode = scene._vfc.new_linearbeam(name)
        super().__init__(scene=scene, name=name)

        self._nodeA = None
        self._nodeB = None

        self._nodeA = None
        self._nodeB = None

    def depends_on(self):
        return [self._nodeA, self._nodeB]

    def try_swap(self, old: Frame, new: Frame) -> bool:
        """Try to swap existing nodeA, nodeB connection with the new frame. Returns True if the swap was successful. Checks global position"""
        if new is None:
            return False  # not an acceptable connection

        if not old.same_position_and_orientation(new, tol=1e-9):
            return False

        if self.nodeA == old:
            self.nodeA = new
            return True
        if self.nodeB == old:
            self.nodeB = new
            return True
        return False

    @property
    def n_segments(self) -> int:
        """Number of segments used in beam [-]"""
        return self._vfNode.nSegments

    @n_segments.setter
    @node_setter_manageable
    @node_setter_observable
    def n_segments(self, value):
        if value < 1:
            raise ValueError("Number of segments in beam should be 1 or more")
        self._vfNode.nSegments = int(value)

    @property
    def EIy(self) -> float:
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
    def EIz(self) -> float:
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
    def GIp(self) -> float:
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
    def EA(self) -> float:
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
    def tension_only(self) -> bool:
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
    def mass(self) -> float:
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
    def L(self) -> float:
        """Length of the beam in unloaded condition [m]"""
        return self._vfNode.L

    @L.setter
    @node_setter_manageable
    @node_setter_observable
    def L(self, value):
        self._vfNode.L = value

    @property
    def nodeA(self) -> Frame:
        """The axis system that the A-end of the beam is connected to. The beam leaves this axis system along the X-axis [Frame]"""
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
        """The axis system that the B-end of the beam is connected to. The beam arrives at this axis system along the X-axis [Frame]"""
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

    # private, for beam-shapes in timeline
    @property
    def _shapeDofs(self):
        return self._vfNode.shapeDofs

    @_shapeDofs.setter
    def _shapeDofs(self, value):
        self._vfNode.shapeDofs = value

    # read-only
    @property
    def moment_A(self) -> tuple[float, float, float]:
        """Moment on beam at node A [kNm, kNm, kNm] (axis system of node A)"""
        return self._vfNode.moment_on_master

    @property
    def moment_B(self) -> tuple[float, float, float]:
        """Moment on beam at node B [kNm, kNm, kNm] (axis system of node B)"""
        return self._vfNode.moment_on_slave

    @property
    def tension(self) -> float:
        """Tension in the beam [kN], negative for compression

        tension is calculated at the midpoints of the beam segments.
        """
        return self._vfNode.tension

    @property
    def torsion(self) -> float:
        """Torsion moment [kNm]. Positive if end B has a positive rotation about the x-axis of end A

        torsion is calculated at the midpoints of the beam segments.
        """
        return self._vfNode.torsion

    @property
    def X_nodes(self) -> tuple[float]:
        """Returns the x-positions of the end nodes and internal nodes along the length of the beam [m]"""
        return self._vfNode.x

    @property
    def X_midpoints(self) -> tuple[float]:
        """X-positions of the beam centers measured along the length of the beam [m]"""
        return tuple(
            0.5 * (np.array(self._vfNode.x[:-1]) + np.array(self._vfNode.x[1:]))
        )

    @property
    def global_positions(self) -> np.array:
        """Global-positions of the end nodes and internal nodes [m,m,m]
        #NOGUI"""
        return np.array(self._vfNode.global_position, dtype=float)

    @property
    def global_orientations(self) -> np.array:
        """Global-orientations of the end nodes and internal nodes [deg,deg,deg]
        #NOGUI"""
        return np.rad2deg(self._vfNode.global_orientation, dtype=float)

    @property
    def bending(self) -> np.array:
        """Bending forces of the end nodes and internal nodes [0, kNm, kNm]"""
        return np.array(self._vfNode.bending)

    def give_python_code(self):
        code = "# code for beam {}".format(self.name)
        code += "\ns.new_beam(name='{}',".format(self.name)
        code += "\n            nodeA='{}',".format(self.nodeA.name)
        code += "\n            nodeB='{}',".format(self.nodeB.name)
        code += "\n            n_segments={},".format(self.n_segments)
        code += "\n            tension_only={},".format(self.tension_only)
        code += "\n            EIy ={:.6g},".format(self.EIy)
        code += "\n            EIz ={:.6g},".format(self.EIz)
        code += "\n            GIp ={:.6g},".format(self.GIp)
        code += "\n            EA ={:.6g},".format(self.EA)
        code += "\n            mass ={:.6g},".format(self.mass)
        code += "\n            L ={:.6g}) # L can possibly be omitted".format(self.L)

        return code
