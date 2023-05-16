"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

"""
Core --> core-connected classes
Pure --> pure-python classes

Base --> fully implemented base classes
Mixins --> mixin classes
Abstracts --> abstract classes


all classes use super().__init__(scene, node)
This errors out at ABC which end up calling object with those arguments. This is worked-around by
introducing an intermediate class myABC with strips the arguments and calls
ABC.__init__(self) explicitly. 


"""
import csv
from dataclasses import dataclass


import fnmatch
import glob
import warnings
from abc import ABC, abstractmethod
from enum import Enum
from typing import List  # for python<3.9

import DAVEcore as DC
import numpy as np
from DAVE.tools import *
from os.path import isfile, split, dirname, exists
from os import listdir
from pathlib import Path
import datetime
import DAVE.settings as vfc

from .nds.abstracts import *
from .nds.enums import *
from .nds.helpers import *
from .nds.mixins import *
from .nds.base import *
from .nds.pure import *
from .nds.core import *

# we are wrapping all methods of DAVEcore such that:
# - it is more user-friendly
# - code-completion is more robust
# - we can do some additional checks. DAVEcore is written for speed, not robustness.
# - DAVEcore is not a hard dependency
#
# notes and choices:
# - properties are returned as tuple to make sure they are not editable.
#    --> node.position[2] = 5 is not allowed



# Wrapper (decorator) for managed nodes














#
#
# class Force(NodeWithCoreParent):
#     """A Force models a force and moment on a poi.
#
#     Both are expressed in the global axis system.
#
#     """
#
#     def __init__(self, scene, name):
#         NodeWithCoreParent.__init__(self, scene, scene._vfc.new_force(name))
#
#     @property
#     def force(self)->tuple[float,float,float]:
#         """The x,y and z components of the force [kN,kN,kN] (global axis)
#
#         Example s['wind'].force = (12,34,56)
#         """
#         return self._vfNode.force
#
#     @force.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def force(self, val):
#
#         assert3f(val)
#         self._vfNode.force = val
#
#     @property
#     def fx(self)->float:
#         """The global x-component of the force [kN] (global axis)"""
#         return self.force[0]
#
#     @fx.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def fx(self, var):
#
#         a = self.force
#         self.force = (var, a[1], a[2])
#
#     @property
#     def fy(self)->float:
#         """The global y-component of the force [kN]  (global axis)"""
#         return self.force[1]
#
#     @fy.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def fy(self, var):
#
#         a = self.force
#         self.force = (a[0], var, a[2])
#
#     @property
#     def fz(self)->float:
#         """The global z-component of the force [kN]  (global axis)"""
#
#         return self.force[2]
#
#     @fz.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def fz(self, var):
#
#         a = self.force
#         self.force = (a[0], a[1], var)
#
#     @property
#     def moment(self)->tuple[float,float,float]:
#         """Moment [kNm,kNm,kNm] (global).
#
#         Example s['wind'].moment = (12,34,56)
#         """
#         return self._vfNode.moment
#
#     @moment.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def moment(self, val):
#
#         assert3f(val)
#         self._vfNode.moment = val
#
#     @property
#     def mx(self)->float:
#         """The global x-component of the moment [kNm]  (global axis)"""
#         return self.moment[0]
#
#     @mx.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def mx(self, var):
#
#         a = self.moment
#         self.moment = (var, a[1], a[2])
#
#     @property
#     def my(self)->float:
#         """The global y-component of the moment [kNm]  (global axis)"""
#         return self.moment[1]
#
#     @my.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def my(self, var):
#
#         a = self.moment
#         self.moment = (a[0], var, a[2])
#
#     @property
#     def mz(self)->float:
#         """The global z-component of the moment [kNm]  (global axis)"""
#         return self.moment[2]
#
#     @mz.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def mz(self, var):
#
#         a = self.moment
#         self.moment = (a[0], a[1], var)
#
#     def give_python_code(self):
#         code = "# code for {}".format(self.name)
#
#         # new_force(self, name, parent=None, force=None, moment=None):
#
#         code += "\ns.new_force(name='{}',".format(self.name)
#         code += "\n            parent='{}',".format(self.parent_for_export.name)
#         code += "\n            force=({:.6g}, {:.6g}, {:.6g}),".format(*self.force)
#         code += "\n            moment=({:.6g}, {:.6g}, {:.6g}) )".format(*self.moment)
#         return code
#
#
# class _Area(NodeWithCoreParent):
#     """Abstract Based class for wind and current areas."""
#
#     def Ae_for_global_direction(self, global_direction):
#         """Returns the effective area in the provided global direction, see"""
#
#         if self.parent.parent is not None:
#             dir = self.parent.parent.to_glob_direction(self.direction)
#         else:
#             dir = self.direction
#
#         if self.areakind == AreaKind.SPHERE:
#             return self.A
#         elif self.areakind == AreaKind.PLANE:
#             return self.A * abs(np.dot(global_direction, dir))
#         elif self.areakind == AreaKind.CYLINDER:
#             dot = np.dot(global_direction, dir)
#             return self.A * np.sqrt(1 - dot ** 2)
#         else:
#             raise ValueError("Unknown area-kind")
#
#     @property
#     def force(self)->tuple[float,float,float]:
#         """The x,y and z components of the force [kN,kN,kN] (global axis)"""
#         return self._vfNode.force
#
#     @property
#     def fx(self)->float:
#         """The global x-component of the force [kN] (global axis)"""
#         return self.force[0]
#
#     @property
#     def fy(self)->float:
#         """The global y-component of the force [kN]  (global axis)"""
#         return self.force[1]
#
#     @property
#     def fz(self)->float:
#         """The global z-component of the force [kN]  (global axis)"""
#
#         return self.force[2]
#
#     @property
#     def A(self)->float:
#         """Total area [m2]. See also Ae"""
#         return self._vfNode.A0
#
#     @A.setter
#     def A(self, value):
#         assert1f_positive_or_zero(value, "Area")
#         self._vfNode.A0 = value
#
#     @property
#     def Ae(self)->float:
#         """Effective area [m2]. This is the projection of the total to the actual wind/current direction. Read only."""
#         return self._vfNode.Ae
#
#     @property
#     def Cd(self)->float:
#         """Cd coefficient [-]"""
#         return self._vfNode.Cd
#
#     @Cd.setter
#     def Cd(self, value):
#         assert1f_positive_or_zero(value, "Cd")
#         self._vfNode.Cd = value
#
#     @property
#     def direction(self)->tuple[float,float,float]:
#         """Depends on 'areakind'. For 'plane' this is the direction of the normal of the plane, for 'cylindrical' this is
#         the direction of the axis and for 'sphere' this is not used [m,m,m]"""
#         return self._vfNode.direction
#
#     @direction.setter
#     def direction(self, value):
#         assert3f(value, "direction")
#         assert np.linalg.norm(value) > 0, ValueError("direction can not be 0,0,0")
#
#         self._vfNode.direction = value
#
#     @property
#     def areakind(self)->AreaKind:
#         """Defines how to interpret the area.
#         See also: `direction`"""
#         return AreaKind(self._vfNode.type)
#
#     @areakind.setter
#     def areakind(self, value):
#         if not isinstance(value, AreaKind):
#             raise ValueError("kind shall be an instance of Area")
#         self._vfNode.type = value.value
#
#     def _give_python_code(self, new_command):
#         code = "# code for {}".format(self.name)
#
#         # new_force(self, name, parent=None, force=None, moment=None):
#
#         code += "\ns.{}(name='{}',".format(new_command, self.name)
#         code += "\n            parent='{}',".format(self.parent_for_export.name)
#         code += f"\n            A={self.A:.6g}, "
#         code += f"\n            Cd={self.Cd:.6g}, "
#         if self.areakind != AreaKind.SPHERE:
#             code += "\n            direction=({:.6g},{:.6g},{:.6g}),".format(*self.direction)
#         code += f"\n            areakind={str(self.areakind)})"
#
#         return code
#
#
# class WindArea(_Area):
#     def give_python_code(self):
#         return self._give_python_code("new_windarea")
#
#
# class CurrentArea(_Area):
#     def give_python_code(self):
#         return self._give_python_code("new_currentarea")
#
#
# class ContactMesh(NodeWithCoreParentAndTrimesh):
#     """A ContactMesh is a tri-mesh with an axis parent"""
#
#     def __init__(self, scene, name):
#         NodeWithCoreParentAndTrimesh.__init__(self, scene, scene._vfc.new_contactmesh(name))
#
#     def give_python_code(self):
#         code = "# code for {}".format(self.name)
#         code += "\nmesh = s.new_contactmesh(name='{}'".format(self.name)
#         if self.parent_for_export:
#             code += ", parent='{}')".format(self.parent_for_export.name)
#         else:
#             code += ")"
#         code += "\nmesh.trimesh.load_file(r'{}', scale = ({:.6g},{:.6g},{:.6g}), rotation = ({:.6g},{:.6g},{:.6g}), offset = ({:.6g},{:.6g},{:.6g}))".format(
#             self.trimesh._path,
#             *self.trimesh._scale,
#             *self.trimesh._rotation,
#             *self.trimesh._offset,
#         )
#
#         return code
#
#
# class ContactBall(NodeWithCoreParent):
#     """A ContactBall is a linear elastic ball which can contact with ContactMeshes.
#
#     It is modelled as a sphere around a Poi. Radius and stiffness can be controlled using radius and k.
#
#     The force is applied on the Poi and it not registered separately.
#     """
#
#     def __init__(self, scene, name : str):
#         NodeWithCoreParent.__init__(self, scene, scene._vfc.new_contactball(name))
#
#         self._meshes = list()
#
#     @property
#     def can_contact(self) -> bool:
#         """True if the ball is currently perpendicular to at least one of the faces of one of the meshes. So when contact is possible. To check if there is contact use "force".
#         See Also: Force
#         """
#         return self._vfNode.has_contact
#
#     @property
#     def contact_force(self) -> tuple:
#         """Returns the force on the ball [kN, kN, kN] (global axis)
#
#         The force is applied at the center of the ball
#
#         See Also: contact_force_magnitude
#         """
#         return self._vfNode.force
#
#     @property
#     def contact_force_magnitude(self) -> float:
#         """Returns the absolute force on the ball, if any [kN]
#
#         The force is applied on the center of the ball
#
#         See Also: contact_force
#         """
#         return np.linalg.norm(self._vfNode.force)
#
#     @property
#     def compression(self) -> float:
#         """Returns the absolute compression of the ball, if any [m]"""
#         return self._vfNode.force
#
#     @property
#     def contactpoint(self) -> tuple[float,float,float]:
#         """Nearest point on the nearest mesh, if contact [m,m,m] (global)"""
#         return self._vfNode.contact_point
#
#     def update(self):
#         """Updates the contact-points and applies forces on mesh and point"""
#         self._vfNode.update()
#
#     @property
#     def meshes(self) -> tuple:
#         """List of contact-mesh nodes.
#         When getting this will yield a list of node references.
#         When setting node references and node-names may be used.
#
#         eg: ball.meshes = [mesh1, 'mesh2']
#         """
#         return tuple(self._meshes)
#
#     @meshes.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def meshes(self, value):
#
#         meshes = []
#
#         for m in value:
#             cm = self._scene._node_from_node_or_str(m)
#
#             if not isinstance(cm, ContactMesh):
#                 raise ValueError(
#                     f"Only ContactMesh nodes can be used as mesh, but {cm.name} is a {type(cm)}"
#                 )
#             if cm in meshes:
#                 raise ValueError(f"Can not add {cm.name} twice")
#
#             meshes.append(cm)
#
#         # copy to meshes
#         self._meshes.clear()
#         self._vfNode.clear_contactmeshes()
#         for mesh in meshes:
#             self._meshes.append(mesh)
#             self._vfNode.add_contactmesh(mesh._vfNode)
#
#     @property
#     def meshes_names(self) -> tuple[str]:
#         """List with the names of the meshes"""
#         return tuple([m.name for m in self._meshes])
#
#     @property
#     def radius(self) ->float:
#         """Radius of the contact-ball [m]"""
#         return self._vfNode.radius
#
#     @radius.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def radius(self, value):
#
#         assert1f_positive_or_zero(value, "radius")
#         self._vfNode.radius = value
#         pass
#
#     @property
#     def k(self) ->float:
#         """Compression stiffness of the ball in force per meter of compression [kN/m]"""
#         return self._vfNode.k
#
#     @k.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def k(self, value):
#
#         assert1f_positive_or_zero(value, "k")
#         self._vfNode.k = value
#         pass
#
#     def give_python_code(self):
#         code = "# code for {}".format(self.name)
#
#         code += "\ns.new_contactball(name='{}',".format(self.name)
#         code += "\n                  parent='{}',".format(self.parent_for_export.name)
#         code += "\n                  radius={:.6g},".format(self.radius)
#         code += "\n                  k={:.6g},".format(self.k)
#         code += "\n                  meshes = [ "
#
#         for m in self._meshes:
#             code += '"' + m.name + '",'
#         code = code[:-1] + "])"
#
#         return code
#
#     # =======================================================================
#
#
# class SPMT(NodeWithCoreParent):
#     """An SPMT is a Self-propelled modular transporter
#
#     These are platform vehicles
#
#     ============  =======
#     0 0 0 0 0 0   0 0 0 0
#
#     This SPMT node models the wheels and hydraulics of a single suspension system.
#
#     A set of wheels is called an "axle". The hydraulics are modelled as a linear spring.
#     The axles can make contact with a contact shape.
#
#     The positions of the axles are controlled by n_length, n_width, spacing_length and spacing_width.
#     The hydraulics are controlled by reference_extension, reference_force and k.
#
#     Setting use_friction to True (default) adds friction such that all contact-forces are purely vertical.
#     Setting use_friction to False will make contact-forces perpendicular to the contacted surface.
#
#     """
#
#     def __init__(self, scene, name : str):
#         NodeWithCoreParent.__init__(self, scene, scene._vfc.new_spmt(name))
#
#         self._meshes = list()
#
#         # These are set by Scene.new_spmt
#         self._k = None
#         self._reference_extension = None
#         self._reference_force = None
#         self._spacing_length = None
#         self._spacing_width = None
#         self._n_length = None
#         self._n_width = None
#
#     def depends_on(self):
#         inherited = NodeWithCoreParent.depends_on(self)
#         inherited.extend(self.meshes)
#
#         return inherited
#
#     # read-only properties
#
#     @property
#     def force(self) -> tuple[float]:
#         """Returns the force component perpendicular to the SPMT in each of the axles (negative mean uplift) [kN]"""
#         return self._vfNode.force
#
#     @property
#     def contact_force(self) -> tuple[tuple[float]]:
#         """Returns the contact force in each of the axles (global) [kN,kN,kN]"""
#         return self._vfNode.forces
#
#     @property
#     def compression(self) -> float:
#         """Returns the total compression (negative means uplift) [m]"""
#         return self._vfNode.compression
#
#     @property
#     def extensions(self) -> tuple[float]:
#         """Returns the extension of each of the axles (bottom of wheel to top of spmt) [m]"""
#         return tuple(self._vfNode.extensions)
#
#     @property
#     def max_extension(self) -> float:
#         """Maximum extension of the axles [m]
#         See Also: extensions"""
#         return max(self.extensions)
#
#     @property
#     def min_extension(self) -> float:
#         """Minimum extension of the axles [m]
#         See Also: extensions"""
#         return min(self.extensions)
#
#     def get_actual_global_points(self):
#         """Returns a list of points: axle1, bottom wheels 1, axle2, bottom wheels 2, etc"""
#         gp = self._vfNode.actual_global_points
#
#         pts = []
#         n2 = int(len(gp) / 2)
#         for i in range(n2):
#             pts.append(gp[2 * i + 1])
#             pts.append(gp[2 * i])
#
#             if i < n2 - 1:
#                 pts.append(gp[2 * i + 2])
#
#         return pts
#
#     # controllable
#
#     # name is derived
#     # parent is derived
#
#     # axles and stiffness are combined
#     def _update_vfNode(self):
#         """Updates vfNode with stiffness and axles"""
#         offx = (self._n_length - 1) * self._spacing_length / 2
#         offy = (self._n_width - 1) * self._spacing_width / 2
#         self._vfNode.clear_axles()
#
#         for ix in range(self._n_length):
#             for iy in range(self._n_width):
#                 self._vfNode.add_axle(ix * self._spacing_length - offx, iy * self._spacing_width - offy, 0)
#
#         n_axles = self._n_length * self._n_width
#         self._vfNode.k = self._k / (n_axles*n_axles)
#         self._vfNode.nominal_length = self._reference_extension + self._reference_force / self._k
#
#     @property
#     def n_width(self) -> int:
#         """number of axles in transverse direction [-]"""
#         return self._n_width
#
#     @n_width.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def n_width(self, value):
#         assert1i_positive_or_zero(value, "n_width")
#         self._n_width = value
#         self._update_vfNode()
#
#     @property
#     def n_length(self)->int:
#         """number of axles in length direction [-]"""
#         return self._n_length
#
#     @n_length.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def n_length(self, value):
#         assert1i_positive_or_zero(value, "n_length")
#         self._n_length = value
#         self._update_vfNode()
#
#     @property
#     def spacing_width(self) -> float:
#         """distance between axles in transverse direction [m]"""
#         return self._spacing_width
#
#     @spacing_width.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def spacing_width(self, value):
#         assert1f_positive_or_zero(value, "spacing_width")
#         self._spacing_width = value
#         self._update_vfNode()
#
#     @property
#     def spacing_length(self)->float:
#         """distance between axles in length direction [m]"""
#         return self._spacing_length
#
#     @spacing_length.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def spacing_length(self, value):
#         assert1f_positive_or_zero(value, "spacing_length")
#         self._spacing_length = value
#         self._update_vfNode()
#
#     @property
#     def reference_force(self)->float:
#         """total force (sum of all axles) when at reference extension [kN]"""
#         return self._reference_force
#
#     @reference_force.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def reference_force(self, value):
#         assert1f_positive_or_zero(value, "reference_force")
#         self._reference_force = value
#         self._update_vfNode()
#
#     @property
#     def reference_extension(self)->float:
#         """Distance between top of SPMT and bottom of wheel at which compression is zero [m]"""
#         return self._reference_extension
#
#     @reference_extension.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def reference_extension(self, value):
#         """nominal extension of axles for reference force [m]"""
#         assert1f_positive_or_zero(value, "reference_extension")
#         self._reference_extension = value
#         self._update_vfNode()
#
#     @property
#     def k(self)->float:
#         """Vertical stiffness of all axles together [kN/m]"""
#         return self._k
#
#     @k.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def k(self, value):
#         assert1f_positive_or_zero(value, "k")
#         self._k = value
#         self._update_vfNode()
#
#     # ==== friction ====
#
#     @property
#     def use_friction(self)->bool:
#         """Apply friction between wheel and surface such that resulting force is vertical [True/False]
#         False: Force is perpendicular to the surface
#         True: Force is vertical
#         """
#         return self._vfNode.use_friction
#
#     @use_friction.setter
#     def use_friction(self, value):
#         assertBool(value, "use friction")
#         self._vfNode.use_friction = value
#
#     # === control meshes ====
#
#     @property
#     def meshes(self) -> tuple:
#         """List of contact-mesh nodes. If empty list then the SPMT can contact all contact meshes.
#         When getting this will yield a list of node references.
#         When setting node references and node-names may be used.
#
#         eg: ball.meshes = [mesh1, 'mesh2']
#         """
#         return tuple(self._meshes)
#
#     @meshes.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def meshes(self, value):
#
#         meshes = []
#
#         for m in value:
#             cm = self._scene._node_from_node_or_str(m)
#
#             if not isinstance(cm, ContactMesh):
#                 raise ValueError(
#                     f"Only ContactMesh nodes can be used as mesh, but {cm.name} is a {type(cm)}"
#                 )
#             if cm in meshes:
#                 raise ValueError(f"Can not add {cm.name} twice")
#
#             meshes.append(cm)
#
#         # copy to meshes
#         self._meshes.clear()
#         self._vfNode.clear_contact_meshes()
#         for mesh in meshes:
#             self._meshes.append(mesh)
#             self._vfNode.add_contact_mesh(mesh._vfNode)
#
#     @property
#     def meshes_names(self) -> tuple[str]:
#         """List with the names of the meshes"""
#         return tuple([m.name for m in self._meshes])
#
#     # === control axles ====
#
#
#     @property
#     def axles(self) -> tuple[tuple[float,float,float]]:
#         """Axles is a list axle positions [m,m,m] (parent axis)
#         Each entry is a (x,y,z) entry which determines the location of the axle on SPMT. This is relative to the parent of the SPMT.
#
#         Example:
#             [(-10,0,0),(-5,0,0),(0,0,0)] for three axles
#         """
#         return self._vfNode.get_axles()
#
#     @axles.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def axles(self, value):
#         self._vfNode.clear_axles()
#         for v in value:
#             assert3f(v, "Each entry should contain three floating point numbers")
#             self._vfNode.add_axle(*v)
#
#     # actions
#
#     def update(self):
#         """Updates the contact-points and applies forces on mesh and point"""
#         self._vfNode.update()
#
#     def give_python_code(self):
#         code = ["# code for {}".format(self.name)]
#
#         code.append(f"s.new_spmt(name='{self.name}',")
#         code.append(f"           parent='{self.parent_for_export.name}',")
#         code.append(f"           reference_force = {self.reference_force:.6g},")
#         code.append(f"           reference_extension = {self.reference_extension:.6g},")
#         code.append(f"           k = {self.k},")
#         code.append(f"           spacing_length = {self.spacing_length:.6g},")
#         code.append(f"           spacing_width = {self.spacing_width:.6g},")
#         code.append(f"           n_length = {self.n_length},")
#         code.append(f"           n_width = {self.n_width},")
#
#         if self._meshes:
#             code.append("                  meshes = [ ")
#             for m in self._meshes:
#                 code.append('"' + m.name + '",')
#             code.append("                           ],")
#         code.append("            )")
#
#         return '\n'.join(code)
#
#

#
# class HydSpring(NodeWithCoreParent):
#     """A HydSpring models a linearized hydrostatic spring.
#
#     The cob (center of buoyancy) is defined in the parent axis system.
#     All other properties are defined relative to the cob.
#
#     """
#
#     @property
#     def cob(self)->tuple[float,float,float]:
#         """Center of buoyancy in (parent axis) [m,m,m]"""
#         return self._vfNode.position
#
#     @cob.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def cob(self, val):
#
#         assert3f(val)
#         self._vfNode.position = val
#
#     @property
#     def BMT(self)->float:
#         """Vertical distance between cob and metacenter for roll [m]"""
#         return self._vfNode.BMT
#
#     @BMT.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def BMT(self, val):
#
#         self._vfNode.BMT = val
#
#     @property
#     def BML(self)->float:
#         """Vertical distance between cob and metacenter for pitch [m]"""
#         return self._vfNode.BML
#
#     @BML.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def BML(self, val):
#
#         self._vfNode.BML = val
#
#     @property
#     def COFX(self)->float:
#         """Horizontal x-position Center of Floatation (center of waterplane area), relative to cob [m]"""
#         return self._vfNode.COFX
#
#     @COFX.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def COFX(self, val):
#
#         self._vfNode.COFX = val
#
#     @property
#     def COFY(self)->float:
#         """Horizontal y-position Center of Floatation (center of waterplane area), relative to cob [m]"""
#         return self._vfNode.COFY
#
#     @COFY.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def COFY(self, val):
#
#         self._vfNode.COFY = val
#
#     @property
#     def kHeave(self)->float:
#         """Heave stiffness [kN/m]"""
#         return self._vfNode.kHeave
#
#     @kHeave.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def kHeave(self, val):
#
#         self._vfNode.kHeave = val
#
#     @property
#     def waterline(self)->float:
#         """Waterline-elevation relative to cob for un-stretched heave-spring. Positive if cob is below the waterline (which is where is normally is) [m]"""
#         return self._vfNode.waterline
#
#     @waterline.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def waterline(self, val):
#
#         self._vfNode.waterline = val
#
#     @property
#     def displacement_kN(self)->float:
#         """Displacement when waterline is at waterline-elevation [kN]"""
#         return self._vfNode.displacement_kN
#
#     @displacement_kN.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def displacement_kN(self, val):
#
#         self._vfNode.displacement_kN = val
#
#     def give_python_code(self):
#         code = "# code for {}".format(self.name)
#
#         # new_force(self, name, parent=None, force=None, moment=None):
#
#         code += "\ns.new_hydspring(name='{}',".format(self.name)
#         code += "\n            parent='{}',".format(self.parent_for_export.name)
#         code += "\n            cob=({}, {}, {}),".format(*self.cob)
#         code += "\n            BMT={},".format(self.BMT)
#         code += "\n            BML={},".format(self.BML)
#         code += "\n            COFX={},".format(self.COFX)
#         code += "\n            COFY={},".format(self.COFY)
#         code += "\n            kHeave={},".format(self.kHeave)
#         code += "\n            waterline={},".format(self.waterline)
#         code += "\n            displacement_kN={} )".format(self.displacement_kN)
#
#         return code
#
#
# class LC6d(CoreConnectedNode):
#     """A LC6d models a Linear Connector with 6 dofs.
#
#     It connects two Axis elements with six linear springs.
#
#     The first axis system is called "main", the second is called "secondary". The difference is that
#     the "main" axis system defines the directions of the stiffness values.
#
#     The translational-springs are straight forward. The rotational springs may not be as intuitive. They are defined as:
#
#       - rotation_x = arc-tan ( uy[0] / uy[1] )
#       - rotation_y = arc-tan ( -ux[0] / ux[2] )
#       - rotation_z = arc-tan ( ux[0] / ux [1] )
#
#     which works fine for small rotations and rotations about only a single axis.
#
#     Tip:
#     It is better to use the "fixed" property of axis systems to create joints.
#
#     """
#
#     def __init__(self, scene, name : str):
#         CoreConnectedNode.__init__(self, scene, scene._vfc.new_linearconnector6d(name))
#
#         self._main = None
#         self._secondary = None
#
#     def depends_on(self):
#         return [self._main, self._secondary]
#
#     @property
#     def stiffness(self)->tuple[float,float,float,float,float,float]:
#         """Stiffness of the connector: kx, ky, kz, krx, kry, krz in [kN/m and kNm/rad] (axis system of the main axis)"""
#         return self._vfNode.stiffness
#
#     @stiffness.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def stiffness(self, val):
#
#         self._vfNode.stiffness = val
#
#     @property
#     def main(self)->Frame:
#         """Main axis system. This axis system dictates the axis system that the stiffness is expressed in
#         #NOGUI"""
#         return self._main
#
#     @main.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def main(self, val):
#
#         val = self._scene._node_from_node_or_str(val)
#         if not isinstance(val, Frame):
#             raise TypeError("Provided nodeA should be a Axis")
#
#         self._main = val
#         self._vfNode.master = val._vfNode
#
#     @property
#     def secondary(self)->Frame:
#         """Secondary (connected) axis system
#         #NOGUI"""
#         return self._secondary
#
#     @secondary.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def secondary(self, val):
#
#         val = self._scene._node_from_node_or_str(val)
#         if not isinstance(val, Frame):
#             raise TypeError("Provided nodeA should be a Axis")
#
#         self._secondary = val
#         self._vfNode.slave = val._vfNode
#
#     @property
#     def fgx(self)->float:
#         """Force on main in global coordinate frame [kN]"""
#         return self._vfNode.global_force[0]
#
#     @property
#     def fgy(self)->float:
#         """Force on main in global coordinate frame [kN]"""
#         return self._vfNode.global_force[1]
#
#     @property
#     def fgz(self)->float:
#         """Force on main in global coordinate frame [kN]"""
#         return self._vfNode.global_force[2]
#
#     @property
#     def force_global(self)->tuple[float,float,float]:
#         """Force on main in global coordinate frame [kN,kN,kN,kNm,kNm,kNm]"""
#         return self._vfNode.global_force
#
#     @property
#     def mgx(self)->float:
#         """Moment on main in global coordinate frame [kNm]"""
#         return self._vfNode.global_moment[0]
#
#     @property
#     def mgy(self)->float:
#         """Moment on main in global coordinate frame [kNm]"""
#         return self._vfNode.global_moment[1]
#
#     @property
#     def mgz(self)->float:
#         """Moment on main in global coordinate frame [kNm]"""
#         return self._vfNode.global_moment[2]
#
#     @property
#     def moment_global(self)->tuple[float,float,float]:
#         """Moment on main in global coordinate frame [kNm, kNm, kNm]"""
#         return self._vfNode.global_moment
#
#     def give_python_code(self):
#         code = "# code for {}".format(self.name)
#
#         code += "\ns.new_linear_connector_6d(name='{}',".format(self.name)
#         code += "\n            main='{}',".format(self.main.name)
#         code += "\n            secondary='{}',".format(self.secondary.name)
#         code += "\n            stiffness=({:.6g}, {:.6g}, {:.6g}, ".format(*self.stiffness[:3])
#         code += "\n                       {:.6g}, {:.6g}, {:.6g}) )".format(*self.stiffness[3:])
#
#         return code
#
#
# class Connector2d(CoreConnectedNode):
#     """A Connector2d linear connector with acts both on linear displacement and angular displacement.
#
#     * the linear stiffness is defined by k_linear and is defined over the actual shortest direction between nodeA and nodeB.
#     * the angular stiffness is defined by k_angular and is defined over the actual smallest angle between the two systems.
#     """
#
#     def __init__(self, scene, name : str):
#         CoreConnectedNode.__init__(self, scene, scene._vfc.new_connector2d(name))
#
#         self._nodeA = None
#         self._nodeB = None
#
#     def depends_on(self):
#         return [self._nodeA, self._nodeB]
#
#     @property
#     def angle(self) -> float:
#         """Actual angle between nodeA and nodeB [deg] (read-only)"""
#         return np.rad2deg(self._vfNode.angle)
#
#     @property
#     def force(self)-> float:
#         """Actual force between nodeA and nodeB [kN] (read-only)"""
#         return self._vfNode.force
#
#     @property
#     def moment(self)-> float:
#         """Actual moment between nodeA and nodeB [kNm] (read-only)"""
#         return self._vfNode.moment
#
#     @property
#     def axis(self)->tuple[float,float,float]:
#         """Actual rotation axis between nodeA and nodeB [m,m,m](read-only)"""
#         return self._vfNode.axis
#
#     @property
#     def ax(self)-> float:
#         """X component of actual rotation axis between nodeA and nodeB [deg](read-only)"""
#         return self._vfNode.axis[0]
#
#     @property
#     def ay(self)-> float:
#         """Y component of actual rotation axis between nodeA and nodeB [deg] (read-only)"""
#         return self._vfNode.axis[1]
#
#     @property
#     def az(self)-> float:
#         """Z component of actual rotation axis between nodeA and nodeB [deg] (read-only)"""
#         return self._vfNode.axis[2]
#
#     @property
#     def k_linear(self)-> float:
#         """Linear stiffness [kN/m]"""
#         return self._vfNode.k_linear
#
#     @k_linear.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def k_linear(self, value):
#
#         self._vfNode.k_linear = value
#
#     @property
#     def k_angular(self)-> float:
#         """Angular stiffness [kNm/rad]"""
#         return self._vfNode.k_angular
#
#     @k_angular.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def k_angular(self, value):
#
#         self._vfNode.k_angular = value
#
#     @property
#     def nodeA(self) -> Frame:
#         """Connected axis system A
#         #NOGUI"""
#         return self._nodeA
#
#     @nodeA.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def nodeA(self, val):
#
#         val = self._scene._node_from_node_or_str(val)
#         if not isinstance(val, Frame):
#             raise TypeError("Provided nodeA should be a Axis")
#
#         self._nodeA = val
#         self._vfNode.master = val._vfNode
#
#     @property
#     def nodeB(self) -> Frame:
#         """Connected axis system B
#         #NOGUI"""
#         return self._nodeB
#
#     @nodeB.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def nodeB(self, val):
#
#         val = self._scene._node_from_node_or_str(val)
#         if not isinstance(val, Frame):
#             raise TypeError("Provided nodeA should be a Axis")
#
#         self._nodeB = val
#         self._vfNode.slave = val._vfNode
#
#     def give_python_code(self):
#         code = "# code for {}".format(self.name)
#
#         code += "\ns.new_connector2d(name='{}',".format(self.name)
#         code += "\n            nodeA='{}',".format(self.nodeA.name)
#         code += "\n            nodeB='{}',".format(self.nodeB.name)
#         code += "\n            k_linear ={:.6g},".format(self.k_linear)
#         code += "\n            k_angular ={:.6g})".format(self.k_angular)
#
#         return code
#
#
# class Beam(CoreConnectedNode):
#     """A LinearBeam models a FEM-like linear beam element.
#
#     A LinearBeam node connects two Axis elements
#
#     By definition the beam runs in the X-direction of the nodeA axis system. So it may be needed to create a
#     dedicated Axis element for the beam to control the orientation.
#
#     The beam is defined using the following properties:
#
#     *  EIy  - bending stiffness about y-axis
#     *  EIz  - bending stiffness about z-axis
#     *  GIp  - torsional stiffness about x-axis
#     *  EA   - axis stiffness in x-direction
#     *  L    - the un-stretched length of the beam
#     *  mass - mass of the beam in [mT]
#
#     The beam element is in rest if the nodeB axis system
#
#     1. has the same global orientation as the nodeA system
#     2. is at global position equal to the global position of local point (L,0,0) of the nodeA axis. (aka: the end of the beam)
#
#     The scene.new_linearbeam automatically creates a dedicated axis system for each end of the beam. The orientation of this axis-system
#     is determined as follows:
#
#     First the direction from nodeA to nodeB is determined: D
#     The axis of rotation is the cross-product of the unit x-axis and D    AXIS = ux x D
#     The angle of rotation is the angle between the nodeA x-axis and D
#     The rotation about the rotated X-axis is undefined.
#
#     """
#
#     def __init__(self, scene, name : str):
#         CoreConnectedNode.__init__(self, scene, scene._vfc.new_linearbeam(name))
#
#         self._nodeA = None
#         self._nodeB = None
#
#     def depends_on(self):
#         return [self._nodeA, self._nodeB]
#
#     @property
#     def n_segments(self)-> int:
#         """Number of segments used in beam [-]"""
#         return self._vfNode.nSegments
#
#     @n_segments.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def n_segments(self, value):
#         if value < 1:
#             raise ValueError("Number of segments in beam should be 1 or more")
#         self._vfNode.nSegments = int(value)
#
#     @property
#     def EIy(self)-> float:
#         """E * Iyy : bending stiffness in the XZ plane [kN m2]
#
#         E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)
#         Iyy is the cross section moment of inertia [m4]
#         """
#         return self._vfNode.EIy
#
#     @EIy.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def EIy(self, value):
#
#         self._vfNode.EIy = value
#
#     @property
#     def EIz(self)-> float:
#         """E * Izz : bending stiffness in the XY plane [kN m2]
#
#         E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)
#         Iyy is the cross section moment of inertia [m4]
#         """
#         return self._vfNode.EIz
#
#     @EIz.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def EIz(self, value):
#
#         self._vfNode.EIz = value
#
#     @property
#     def GIp(self)-> float:
#         """G * Ipp : torsional stiffness about the X (length) axis [kN m2]
#
#         G is the shear-modulus of elasticity; for steel 75-80 GPa (10^6 kN/m2)
#         Ip is the cross section polar moment of inertia [m4]
#         """
#         return self._vfNode.GIp
#
#     @GIp.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def GIp(self, value):
#
#         self._vfNode.GIp = value
#
#     @property
#     def EA(self)-> float:
#         """E * A : stiffness in the length direction [kN]
#
#         E is the modulus of elasticity; for steel 190-210 GPa (10^6 kN/m2)
#         A is the cross-section area in [m2]
#         """
#         return self._vfNode.EA
#
#     @EA.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def EA(self, value):
#
#         self._vfNode.EA = value
#
#     @property
#     def tension_only(self)->bool:
#         """axial stiffness (EA) only applicable to tension [True/False]"""
#         return self._vfNode.tensionOnly
#
#     @tension_only.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def tension_only(self, value):
#         assert isinstance(value, bool), ValueError(
#             "Value for tension_only shall be True or False"
#         )
#         self._vfNode.tensionOnly = value
#
#     @property
#     def mass(self)-> float:
#         """Mass of the beam in [mT]"""
#         return self._vfNode.Mass
#
#     @mass.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def mass(self, value):
#
#         assert1f(value, "Mass shall be a number")
#         self._vfNode.Mass = value
#         pass
#
#     @property
#     def L(self)-> float:
#         """Length of the beam in unloaded condition [m]"""
#         return self._vfNode.L
#
#     @L.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def L(self, value):
#
#         self._vfNode.L = value
#
#     @property
#     def nodeA(self) -> Frame:
#         """The axis system that the A-end of the beam is connected to. The beam leaves this axis system along the X-axis [Frame]"""
#         return self._nodeA
#
#     @nodeA.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def nodeA(self, val):
#
#         val = self._scene._node_from_node_or_str(val)
#
#         if not isinstance(val, Frame):
#             raise TypeError("Provided nodeA should be a Axis")
#
#         self._nodeA = val
#         self._vfNode.master = val._vfNode
#
#     @property
#     def nodeB(self)->Frame:
#         """The axis system that the B-end of the beam is connected to. The beam arrives at this axis system along the X-axis [Frame]"""
#         return self._nodeB
#
#     @nodeB.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def nodeB(self, val):
#
#         val = self._scene._node_from_node_or_str(val)
#         if not isinstance(val, Frame):
#             raise TypeError("Provided nodeA should be a Axis")
#
#         self._nodeB = val
#         self._vfNode.slave = val._vfNode
#
#     # private, for beam-shapes in timeline
#     @property
#     def _shapeDofs(self):
#         return self._vfNode.shapeDofs
#
#     @_shapeDofs.setter
#     def _shapeDofs(self, value):
#         self._vfNode.shapeDofs = value
#
#     # read-only
#     @property
#     def moment_A(self) -> tuple[float,float,float]:
#         """Moment on beam at node A [kNm, kNm, kNm] (axis system of node A)"""
#         return self._vfNode.moment_on_master
#
#     @property
#     def moment_B(self)-> tuple[float,float,float]:
#         """Moment on beam at node B [kNm, kNm, kNm] (axis system of node B)"""
#         return self._vfNode.moment_on_slave
#
#     @property
#     def tension(self)->float:
#         """Tension in the beam [kN], negative for compression
#
#         tension is calculated at the midpoints of the beam segments.
#         """
#         return self._vfNode.tension
#
#     @property
#     def torsion(self)->float:
#         """Torsion moment [kNm]. Positive if end B has a positive rotation about the x-axis of end A
#
#         torsion is calculated at the midpoints of the beam segments.
#         """
#         return self._vfNode.torsion
#
#     @property
#     def X_nodes(self)->tuple[float]:
#         """Returns the x-positions of the end nodes and internal nodes along the length of the beam [m]"""
#         return self._vfNode.x
#
#     @property
#     def X_midpoints(self)->tuple[float]:
#         """X-positions of the beam centers measured along the length of the beam [m]"""
#         return tuple(
#             0.5 * (np.array(self._vfNode.x[:-1]) + np.array(self._vfNode.x[1:]))
#         )
#
#     @property
#     def global_positions(self)->tuple[tuple[float,float,float]]:
#         """Global-positions of the end nodes and internal nodes [m,m,m]"""
#         return np.array(self._vfNode.global_position, dtype=float)
#
#     @property
#     def global_orientations(self)->tuple[tuple[float,float,float]]:
#         """Global-orientations of the end nodes and internal nodes [deg,deg,deg]"""
#         return np.rad2deg(self._vfNode.global_orientation)
#
#     @property
#     def bending(self)->tuple[tuple[float,float,float]]:
#         """Bending forces of the end nodes and internal nodes [0, kNm, kNm]"""
#         return np.array(self._vfNode.bending)
#
#     def give_python_code(self):
#         code = "# code for beam {}".format(self.name)
#         code += "\ns.new_beam(name='{}',".format(self.name)
#         code += "\n            nodeA='{}',".format(self.nodeA.name)
#         code += "\n            nodeB='{}',".format(self.nodeB.name)
#         code += "\n            n_segments={},".format(self.n_segments)
#         code += "\n            tension_only={},".format(self.tension_only)
#         code += "\n            EIy ={:.6g},".format(self.EIy)
#         code += "\n            EIz ={:.6g},".format(self.EIz)
#         code += "\n            GIp ={:.6g},".format(self.GIp)
#         code += "\n            EA ={:.6g},".format(self.EA)
#         code += "\n            mass ={:.6g},".format(self.mass)
#         code += "\n            L ={:.6g}) # L can possibly be omitted".format(self.L)
#
#         return code
#
#
# class TriMeshSource():  # not an instance of Node
#     """
#     TriMesh
#
#     A TriMesh node contains triangular mesh which can be used for buoyancy or contact.
#
#     The mesh is first scaled, then rotated and then offset
#
#     """
#
#     def __init__(self, scene, source):
#
#         # name = scene.available_name_like("Names of trimesh-sources are not used")
#         # super().__init__(scene, name=name, _do_not_add_to_scene=True)
#
#         self._scene = scene
#
#         # Note: TriMeshSource does not have a corresponding vfCore Node in the scene but does have a vfCore
#         self._TriMesh = source
#         self._new_mesh = True  # cheat for visuals
#
#         self._path = ""  # stores the data that was used to load the obj
#         self._offset = (0, 0, 0)
#         self._scale = (1, 1, 1)
#         self._rotation = (0, 0, 0)
#
#         self._invert_normals = False
#
#         self.boundary_edges = []
#         self.non_manifold_edges = []
#
#     def depends_on(self) -> list:
#         return []
#
#     def AddVertex(self, x, y, z):
#         """Adds a vertex (point)"""
#         self._TriMesh.AddVertex(x, y, z)
#
#     def AddFace(self, i, j, k):
#         """Adds a triangular face between vertex numbers i,j and k"""
#         self._TriMesh.AddFace(i, j, k)
#
#     def get_extends(self):
#         """Returns the extends of the mesh in global coordinates
#
#         Returns: (minimum_x, maximum_x, minimum_y, maximum_y, minimum_z, maximum_z)
#
#         """
#
#         t = self._TriMesh
#
#         if t.nFaces == 0:
#             return (0, 0, 0, 0, 0, 0)
#
#         v = t.GetVertex(0)
#         xn = v[0]
#         xp = v[0]
#         yn = v[1]
#         yp = v[1]
#         zn = v[2]
#         zp = v[2]
#
#         for i in range(t.nVertices):
#             v = t.GetVertex(i)
#             x = v[0]
#             y = v[1]
#             z = v[2]
#
#             if x < xn:
#                 xn = x
#             if x > xp:
#                 xp = x
#             if y < yn:
#                 yn = y
#             if y > yp:
#                 yp = y
#             if z < zn:
#                 zn = z
#             if z > zp:
#                 zp = z
#
#         return (xn, xp, yn, yp, zn, zp)
#
#     def _fromVTKpolydata(
#         self, polydata, offset=None, rotation=None, scale=None, invert_normals=False
#     ):
#
#         import vtk
#
#         tri = vtk.vtkTriangleFilter()
#
#         tri.SetInputConnection(polydata)
#
#         scaleFilter = vtk.vtkTransformPolyDataFilter()
#         rotationFilter = vtk.vtkTransformPolyDataFilter()
#
#         s = vtk.vtkTransform()
#         s.Identity()
#         r = vtk.vtkTransform()
#         r.Identity()
#
#         scaleFilter.SetInputConnection(tri.GetOutputPort())
#         rotationFilter.SetInputConnection(scaleFilter.GetOutputPort())
#
#         if scale is not None:
#             s.Scale(*scale)
#
#         if rotation is not None:
#             q = rotation
#             angle = (q[0] ** 2 + q[1] ** 2 + q[2] ** 2) ** (0.5)
#             if angle > 0:
#                 r.RotateWXYZ(angle, q[0] / angle, q[1] / angle, q[2] / angle)
#
#         if offset is None:
#             offset = [0, 0, 0]
#
#         scaleFilter.SetTransform(s)
#         rotationFilter.SetTransform(r)
#
#         clean = vtk.vtkCleanPolyData()
#         clean.SetInputConnection(rotationFilter.GetOutputPort())
#
#         clean.ConvertLinesToPointsOff()
#         clean.ConvertPolysToLinesOff()
#         clean.ConvertStripsToPolysOff()
#         clean.PointMergingOn()
#         clean.ToleranceIsAbsoluteOn()
#         clean.SetAbsoluteTolerance(0.001)
#
#         clean.Update()
#         data = clean.GetOutput()
#
#         self._TriMesh.Clear()
#
#         for i in range(data.GetNumberOfPoints()):
#             point = data.GetPoint(i)
#             self._TriMesh.AddVertex(
#                 point[0] + offset[0], point[1] + offset[1], point[2] + offset[2]
#             )
#
#         for i in range(data.GetNumberOfCells()):
#             cell = data.GetCell(i)
#
#             if isinstance(cell, vtk.vtkLine):
#                 print("Cell nr {} is a line, not adding to mesh".format(i))
#                 continue
#
#             if isinstance(cell, vtk.vtkVertex):
#                 print("Cell nr {} is a vertex, not adding to mesh".format(i))
#                 continue
#
#             id0 = cell.GetPointId(0)
#             id1 = cell.GetPointId(1)
#             id2 = cell.GetPointId(2)
#
#             if invert_normals:
#                 self._TriMesh.AddFace(id2, id1, id0)
#             else:
#                 self._TriMesh.AddFace(id0, id1, id2)
#
#         # check if anything was loaded
#         if self._TriMesh.nFaces == 0:
#             raise Exception(
#                 "No faces in poly-data - no geometry added (hint: empty obj file?)"
#             )
#         self._new_mesh = True
#         self._scene.update()
#
#     def check_shape(self):
#         """Performs some checks on the shape in the trimesh
#         - Boundary edges (edge with only one face attached)
#         - Non-manifold edges (edit with more than two faces attached)
#         - Volume should be positive
#         """
#
#         tm = self._TriMesh
#
#         if tm.nFaces == 0:
#             return ["No mesh"]
#
#         # # make sure the mesh is clean: vertices should be unique
#         # vertices = []
#         # for i in range(tm.nVertices):
#         #     vertex = np.array(tm.GetVertex(i))
#         #     for v in vertices:
#         #         if np.linalg.norm(vertex-v) < 0.001:
#         #             print("Duplicate vertex" + str(vertex-v))
#         #     else:
#         #         vertices.append(vertex)
#
#         # Make a list of all boundaries using their vertex IDs
#         boundaries = np.zeros((3 * tm.nFaces, 2), dtype=int)
#         for i in range(tm.nFaces):
#             face = tm.GetFace(i)
#             boundaries[3 * i] = [face[0], face[1]]
#             boundaries[3 * i + 1] = [face[1], face[2]]
#             boundaries[3 * i + 2] = [face[2], face[0]]
#
#         # For an edge is doesn't matter in which direction it runs
#         boundaries.sort(axis=1)
#
#         # every boundary should be present twice
#
#         values, rows_occurance_count = np.unique(
#             boundaries, axis=0, return_counts=True
#         )  # count of rows
#
#         n_boundary = np.count_nonzero(rows_occurance_count == 1)
#         n_nonmanifold = np.count_nonzero(rows_occurance_count > 2)
#
#         messages = []
#
#         boundary_edges = []
#         non_manifold_edges = []
#
#         if n_boundary > 0:
#             messages.append(f"Mesh contains {n_boundary} boundary edges")
#
#             i_boundary = np.argwhere(rows_occurance_count == 1)
#             for i in i_boundary:
#                 edge = values[i][0]
#                 v1 = tm.GetVertex(edge[0])
#                 v2 = tm.GetVertex(edge[1])
#                 boundary_edges.append((v1, v2))
#
#         if n_nonmanifold > 0:
#             messages.append(f"Mesh contains {n_nonmanifold} non-manifold edges")
#             i_boundary = np.argwhere(rows_occurance_count > 2)
#             for i in i_boundary:
#                 edge = values[i][0]
#                 v1 = tm.GetVertex(edge[0])
#                 v2 = tm.GetVertex(edge[1])
#                 non_manifold_edges.append((v1, v2))
#
#         if len(messages) == 2:
#             messages.append("Boundary edges are shown in Red")
#             messages.append("Non-manifold edges are shown in Pink")
#
#         try:
#             volume = tm.Volume()
#         except:
#             volume = 1  # no available in every DAVEcore yet
#
#         if volume < 0:
#             messages.append(
#                 f"Total mesh volume is negative ({volume:.2f} m3 of enclosed volume)."
#             )
#             messages.append("Hint: Use invert-normals")
#
#         self.boundary_edges = boundary_edges
#         self.non_manifold_edges = non_manifold_edges
#
#         return messages
#
#     def load_vtk_polydataSource(self, polydata):
#         """Fills the triangle data from a vtk polydata such as a cubeSource.
#
#         The vtk TriangleFilter is used to triangulate the source
#
#         Examples:
#             cube = vtk.vtkCubeSource()
#             cube.SetXLength(122)
#             cube.SetYLength(38)
#             cube.SetZLength(10)
#             trimesh.load_vtk_polydataSource(cube)
#         """
#
#         self._fromVTKpolydata(polydata.GetOutputPort())
#
#     def load_obj(
#         self, filename, offset=None, rotation=None, scale=None, invert_normals=False
#     ):
#         self.load_file(filename, offset, rotation, scale, invert_normals)
#
#     def load_file(
#         self, url, offset=None, rotation=None, scale=None, invert_normals=False
#     ):
#         """Loads an .obj or .stl file and and triangulates it.
#
#         Order of modifications:
#
#         1. rotate
#         2. scale
#         3. offset
#
#         Args:
#             url: (str or path or resource): file to load
#             offset: : offset
#             rotation:  : rotation
#             scale:  scale
#
#         """
#
#         self._path = str(url)
#
#         filename = str(self._scene.get_resource_path(url))
#
#         import vtk
#
#         ext = filename.lower()[-3:]
#         if ext == "obj":
#             obj = vtk.vtkOBJReader()
#             obj.SetFileName(filename)
#         elif ext == "stl":
#             obj = vtk.vtkSTLReader()
#             obj.SetFileName(filename)
#         else:
#             raise ValueError(
#                 f"File should be an .obj or .stl file but has extension {ext}"
#             )
#
#         # Add cleaning
#         cln = vtk.vtkCleanPolyData()
#         cln.SetInputConnection(obj.GetOutputPort())
#
#         self._fromVTKpolydata(
#             cln.GetOutputPort(),
#             offset=offset,
#             rotation=rotation,
#             scale=scale,
#             invert_normals=invert_normals,
#         )
#
#         self._scale = scale
#         self._offset = offset
#         self._rotation = rotation
#
#         if self._scale is None:
#             self._scale = (1.0, 1.0, 1.0)
#         if self._offset is None:
#             self._offset = (0.0, 0.0, 0.0)
#         if self._rotation is None:
#             self._rotation = (0.0, 0.0, 0.0)
#         self._invert_normals = invert_normals
#
#     def _load_from_privates(self):
#         """(Re)Loads the mesh using the values currently stored in _scale, _offset, _rotation and _invert_normals"""
#         self.load_file(
#             url=self._path,
#             scale=self._scale,
#             offset=self._offset,
#             rotation=self._rotation,
#             invert_normals=self._invert_normals,
#         )
#
#     def give_python_code(self):
#         code = "# No code generated for TriMeshSource"
#         return code
#
#     # def change_parent_to(self, new_parent):
#     #
#     #     if not (isinstance(new_parent, Axis) or new_parent is None):
#     #         raise ValueError('Visuals can only be attached to an axis (or derived) or None')
#     #
#     #     # get current position and orientation
#     #     if self.parent is not None:
#     #         cur_position = self.parent.to_glob_position(self.offset)
#     #         cur_rotation = self.parent.to_glob_direction(self.rotation)
#     #     else:
#     #         cur_position = self.offset
#     #         cur_rotation = self.rotation
#     #
#     #     self.parent = new_parent
#     #
#     #     if new_parent is None:
#     #         self.offset = cur_position
#     #         self.rotation = cur_rotation
#     #     else:
#     #         self.offset = new_parent.to_loc_position(cur_position)
#     #         self.rotation = new_parent.to_loc_direction(cur_rotation)
#
#
# class Buoyancy(NodeWithCoreParentAndTrimesh):
#     """Buoyancy provides a buoyancy force based on a buoyancy mesh. The mesh is triangulated and chopped at the instantaneous flat water surface. Buoyancy is applied as an upwards force that the center of buoyancy.
#     The calculation of buoyancy is as accurate as the provided geometry.
#
#     There as no restrictions to the size or aspect ratio of the panels. It is excellent to model as box using 6 faces. Using smaller panels has a negative effect on performance.
#
#     The normals of the panels should point towards to water.
#     """
#
#     # init parent and name are fully derived from NodeWithParent
#     # _vfNode is a buoyancy
#     def __init__(self, scene, name : str):
#         NodeWithCoreParentAndTrimesh.__init__(self, scene, scene._vfc.new_buoyancy(name))
#
#     def update(self):
#         self._vfNode.reloadTrimesh()
#
#     @property
#     def cob(self)->tuple[tuple[float,float,float]]:
#         """GLOBAL position of the center of buoyancy [m,m,m] (global axis)"""
#         return self._vfNode.cob
#
#     @property
#     def cob_local(self)->tuple[tuple[float,float,float]]:
#         """Position of the center of buoyancy [m,m,m] (local axis)"""
#
#         return self.parent.to_loc_position(self.cob)
#
#     @property
#     def displacement(self)->float:
#         """Displaced volume of fluid [m^3]"""
#         return self._vfNode.displacement
#
#     def give_python_code(self):
#         code = "# code for {}".format(self.name)
#         code += "\nmesh = s.new_buoyancy(name='{}',".format(self.name)
#
#         code += "\n          parent='{}')".format(self.parent_for_export.name)
#
#         if self.trimesh._invert_normals:
#             code += "\nmesh.trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}), invert_normals=True)".format(
#                 self.trimesh._path,
#                 *self.trimesh._scale,
#                 *self.trimesh._rotation,
#                 *self.trimesh._offset,
#             )
#         else:
#             code += "\nmesh.trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}))".format(
#                 self.trimesh._path,
#                 *self.trimesh._scale,
#                 *self.trimesh._rotation,
#                 *self.trimesh._offset,
#             )
#
#         return code
#
#
# class Tank(NodeWithCoreParentAndTrimesh):
#     """Tank provides a fillable tank based on a mesh. The mesh is triangulated and chopped at the instantaneous flat fluid surface. Gravity is applied as an downwards force that the center of fluid.
#     The calculation of fluid volume and center is as accurate as the provided geometry.
#
#     There as no restrictions to the size or aspect ratio of the panels. It is excellent to model as box using 6 faces. Using smaller panels has a negative effect on performance.
#
#     The normals of the panels should point *away* from the fluid. This means that the same basic shapes can be used for both buoyancy and tanks.
#     """
#
#     # init parent and name are fully derived from NodeWithParent
#     # _vfNode is a tank
#     def __init__(self, scene, name):
#
#         NodeWithCoreParentAndTrimesh.__init__(self, scene, scene._vfc.new_tank(name))
#
#         self._inertia = scene._vfc.new_pointmass(
#             self.name + vfc.VF_NAME_SPLIT + "inertia"
#         )
#
#     def update(self):
#         self._vfNode.reloadTrimesh()
#
#         # update inertia
#         self._inertia.parent = self.parent._vfNode
#         self._inertia.position = self.cog_local
#         self._inertia.inertia = self.volume * self.density
#
#     def _delete_vfc(self):
#         self._scene._vfc.delete(self._inertia.name)
#         NodeWithCoreParentAndTrimesh._delete_vfc(self)
#
#     @property
#     def free_flooding(self)->bool:
#         """Tank is filled till global waterline (aka: damaged) [bool]"""
#         return self._vfNode.free_flooding
#
#     @free_flooding.setter
#     def free_flooding(self, value):
#         assert isinstance(value, bool), ValueError(
#             f"free_flooding shall be a bool, you passed a {type(value)}"
#         )
#         self._vfNode.free_flooding = value
#
#     @property
#     def permeability(self)->float:
#         """Permeability is the fraction of the meshed volume that can be filled with fluid [-]"""
#         return self._vfNode.permeability
#
#     @permeability.setter
#     def permeability(self, value):
#         assert1f_positive_or_zero(value)
#         self._vfNode.permeability = value
#
#     @property
#     def cog(self)->tuple[tuple[float,float,float]]:
#         """Global position of the center of volume / gravity [m,m,m] (global)"""
#         return self._vfNode.cog
#
#     @property
#     def cog_local(self)->tuple[tuple[float,float,float]]:
#         """Center of gravity [m,m,m] (parent axis)"""
#         return self.parent.to_loc_position(self.cog)
#
#     @property
#     def cog_when_full_global(self) -> tuple[tuple[float, float, float]]:
#         """Global position of the center of volume / gravity of the tank when it is filled [m,m,m] (global)"""
#         return self.parent.to_glob_position(self._vfNode.cog_when_full)
#
#     @property
#     def cog_when_full(self)->tuple[float,float,float]:
#         """LOCAL position of the center of volume / gravity of the tank when it is filled [m,m,m] (parent axis)"""
#         return self._vfNode.cog_when_full
#
#     @property
#     def cogx_when_full(self)->float:
#         """x position of the center of volume / gravity of the tank when it is filled [m] (parent axis)"""
#         return self._vfNode.cog_when_full[0]
#
#     @property
#     def cogy_when_full(self) -> float:
#         """y position of the center of volume / gravity of the tank when it is filled [m] (parent axis)"""
#         return self._vfNode.cog_when_full[1]
#
#     @property
#     def cogz_when_full(self) -> float:
#         """z position of the center of volume / gravity of the tank when it is filled [m] (parent axis)"""
#         return self._vfNode.cog_when_full[2]
#
#     @property
#     def fill_pct(self)->float:
#         """Amount of volume in tank as percentage of capacity [%]"""
#         if self.capacity == 0:
#             return 0
#         return 100 * self.volume / self.capacity
#
#     @fill_pct.setter
#     @node_setter_observable
#     def fill_pct(self, value):
#
#         if value < 0 and value > -0.01:
#             value = 0
#
#         assert1f_positive_or_zero(value)
#
#         if value > 100.1:
#             raise ValueError(
#                 f"Fill percentage should be between 0 and 100 [%], {value} is not valid"
#             )
#         if value > 100:
#             value = 100
#         self.volume = value * self.capacity / 100
#
#     @property
#     def level_global(self)->float:
#         """The fluid plane elevation in the global axis system [m]
#         Setting this adjusts the volume"""
#         return self._vfNode.fluid_level_global
#
#     @level_global.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def level_global(self, value):
#         assert1f(value)
#         self._vfNode.fluid_level_global = value
#
#     @property
#     def volume(self)->float:
#         """The actual volume of fluid in the tank [m3]
#         Setting this adjusts the fluid level"""
#         return self._vfNode.volume
#
#     @volume.setter
#     @node_setter_observable
#     def volume(self, value):
#         assert1f_positive_or_zero(value, "Volume")
#         self._vfNode.volume = value
#
#     @property
#     def used_density(self):
#         """Density of the fluid in the tank [mT/m3]"""
#         if self.density > 0:
#             return self.density
#         else:
#             return self._scene.rho_water
#
#     @property
#     def density(self)->float:
#         """Density of the fluid in the tank. Density < 0 means use outside water density. See also used_density [mT/m3]"""
#         return self._vfNode.density
#
#     @density.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def density(self, value):
#         assert1f(value)
#         self._vfNode.density = value
#
#     @property
#     def capacity(self)->float:
#         """Fillable volume of the tank calcualted as mesh volume times permeability [m3]
#         This is calculated from the defined geometry and permeability.
#         See also: mesh_volume"""
#         return self._vfNode.capacity
#
#     @property
#     def mesh_volume(self) -> float:
#         """Volume enclosed by the mesh the tank [m3]
#         This is calculated from the defined geometry and does not account for permeability.
#         See also: capacity"""
#         return self._vfNode.capacity / self._vfNode.permeability
#
#     @property
#     def ullage(self)->float:
#         """Ullage of the tank [m]
#         The ullage is the distance between a measurement point and the fluid surface. The point is [xf,yf,zv] where
#         xf and yf are the x and y coordinates (local) of the center of fluid when the tank is full. zv is the largest z value
#         of all the vertices of the tank.
#         The measurement direction is in local z-direction. If the tank is under an angle then this is not perpendicular to the fluid.
#         It is possible that this definition returns an ullage larger than the physical tank depth. In that case the physical depth of
#         the tank is returned instead.
#         """
#         return self._vfNode.ullage
#
#     def give_python_code(self):
#         code = "# code for {}".format(self.name)
#         code += "\nmesh = s.new_tank(name='{}',".format(self.name)
#
#         if self.density != 1.025:
#             code += f"\n          density={self.density:.6g},"
#
#         if self.free_flooding:
#             code += f"\n          free_flooding=True,"
#
#         code += "\n          parent='{}')".format(self.parent_for_export.name)
#
#         if self.trimesh._invert_normals:
#             code += "\nmesh.trimesh.load_file(r'{}', scale = ({:.6g},{:.6g},{:.6g}), rotation = ({:.6g},{:.6g},{:.6g}), offset = ({:.6g},{:.6g},{:.6g}), invert_normals=True)".format(
#                 self.trimesh._path,
#                 *self.trimesh._scale,
#                 *self.trimesh._rotation,
#                 *self.trimesh._offset,
#             )
#         else:
#             code += "\nmesh.trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}))".format(
#                 self.trimesh._path,
#                 *self.trimesh._scale,
#                 *self.trimesh._rotation,
#                 *self.trimesh._offset,
#             )
#         code += f"\ns['{self.name}'].volume = {self.volume:.6g}   # first load mesh, then set volume"
#
#         return code
#
#
# class BallastSystem(Node):
#     """The BallastSystemNode is a non-physical node that marks a groups of Tank nodes as being the ballast system
#     of a vessel.
#
#     The BallastSystem node can interface with the ballast-solver to automatically determine a suitable ballast configuration.
#
#     The tank objects are created separately and only their references are assigned to this ballast-system object.
#     That is done using the .tanks property which is a list.
#     The parent if this node is the vessel that the tanks belong to. The parent of the ballast system is expected to be
#     a Frame or Rigidbody which can be ballasted (should not have a parent).
#
#     Tanks can be excluded from the ballast algorithms by adding their names to the 'frozen' list.
#
#     Typical use:
#     - create vessel
#     - create tanks
#     - create ballast system
#     - adds tanks to ballast system using ballast_system.tanks.append(tank node)
#     - set the draft: ballast_system.target_elevation = -5.0 # note, typically negative
#     - and solve the tank fills: ballast_system.solve_ballast
#
#
#     """
#
#     def __init__(self, scene, name, parent):
#         Node.__init__(self, scene, name)
#
#         self.tanks = []
#         """List of Tank objects"""
#
#         self.frozen = []
#         """List of names of frozen tanks - The contents of a frozen tank should not be changed"""
#
#         self.parent = parent
#
#         self._target_elevation = None
#         """Target elevation of the parent Frame (global, m)"""
#         self._target_cog = None
#         """Required cog of all the ballast tanks to reach the target z, calculated when setting target_elevation"""
#         self._target_weight = None
#         """Required total amount of water ballast to reach the target z, calculated when setting target_elevation"""
#
#     @property
#     def target_elevation(self) -> float:
#         """The target elevation of the parent of the ballast system [m]"""
#         return self._target_elevation
#
#     @target_elevation.setter
#     def target_elevation(self, value):
#
#         assert1f(value, "target elevation")
#
#         # empty all connected tanks
#         fills = [tank.fill_pct for tank in self.tanks]
#         for tank in self.tanks:
#             tank.fill_pct = 0
#
#         try:
#
#             from DAVE.solvers.ballast import force_vessel_to_evenkeel_and_draft
#
#             (F, x, y) = force_vessel_to_evenkeel_and_draft(
#                 self._scene, self.parent, value
#             )
#             self._target_elevation = value
#             self._target_cog = (x, y)
#             self._target_weight = -F
#
#         finally:  # restore all connected tanks
#             for tank, fill in zip(self.tanks, fills):
#                 tank.fill_pct = fill
#
#     def solve_ballast(self, method=1, use_current_fill=False):
#         """Attempts to find a suitable filling of the ballast tanks to position parent at even-keel and target-elevation
#
#         Args:
#             method: algorithm to use (named 1 and 2)
#             use_current_fill: use current tank fill as start for the algorithm
#
#         See Also: target_elevation"""
#
#         if self._target_weight is None:
#             raise ValueError(
#                 "Please set target_elevation first (eg: target_elevation = -5)"
#             )
#
#         from DAVE.solvers.ballast import BallastSystemSolver
#
#         ballast_solver = BallastSystemSolver(self)
#
#         assert method == 1 or method == 2, "Method shall be 1 or 2"
#
#         if not ballast_solver.ballast_to(
#             self._target_cog[0],
#             self._target_cog[1],
#             self._target_weight,
#             start_empty=not use_current_fill,
#             method=method,
#         ):
#             raise ValueError('Could not obtain tank fillings to satisfy required condition - requesting a different draft may help')
#
#     def new_tank(
#         self, name, position, capacity_kN, rho=1.025, frozen=False, actual_fill=0
#     ):
#         """Adds a new cubic shaped tank with the given volume as derived from capacity and rho
#
#         Warning: provided for backwards compatibility only.
#         """
#
#         from warnings import warn
#
#         warn(
#             "BallastSystem.new_tank is outdated and may be removed in a future version."
#         )
#
#         tnk = self._scene.new_tank(name, parent=self.parent, density=rho)
#         volume = capacity_kN / (9.81 * rho)
#         side = volume ** (1 / 3)
#         tnk.trimesh.load_file(
#             "res: cube.obj",
#             scale=(side, side, side),
#             rotation=(0.0, 0.0, 0.0),
#             offset=position,
#         )
#         if actual_fill > 0:
#             tnk.fill_pct = actual_fill
#
#         if frozen:
#             tnk.frozen = frozen
#
#         self.tanks.append(tnk)
#
#         return tnk
#
#     # for gui
#     def change_parent_to(self, new_parent):
#         if not (isinstance(new_parent, Frame) or new_parent is None):
#             raise ValueError(
#                 "Visuals can only be attached to an axis (or derived) or None"
#             )
#         self.parent = new_parent
#
#     # for node
#     def depends_on(self):
#         return [self.parent, *self.tanks]
#
#     def is_frozen(self, name):
#         """Returns True if the tank with this name if frozen"""
#         return name in self.frozen
#
#     def reorder_tanks(self, names):
#         """Places tanks with given names at the top of the list. Other tanks are appended afterwards in original order.
#
#         For a complete re-order give all tank names.
#
#         Example:
#             let tanks be 'a','b','c','d','e'
#
#             then re_order_tanks(['e','b']) will result in ['e','b','a','c','d']
#         """
#         for name in names:
#             if name not in self.tank_names():
#                 raise ValueError("No tank with name {}".format(name))
#
#         old_tanks = self.tanks.copy()
#         self.tanks.clear()
#         to_be_deleted = list()
#
#         for name in names:
#             for tank in old_tanks:
#                 if tank.name == name:
#                     self.tanks.append(tank)
#                     to_be_deleted.append(tank)
#
#         for tank in to_be_deleted:
#             old_tanks.remove(tank)
#
#         for tank in old_tanks:
#             self.tanks.append(tank)
#
#     def order_tanks_by_elevation(self):
#         """Re-orders the existing tanks such that the lowest tanks are higher in the list"""
#
#         zs = [tank.cog_when_full[2] for tank in self.tanks]
#         inds = np.argsort(zs)
#         self.tanks = [self.tanks[i] for i in inds]
#
#     def order_tanks_by_distance_from_point(self, point, reverse=False):
#         """Re-orders the existing tanks such that the tanks *furthest* from the point are first on the list
#
#         Args:
#             point : (x,y,z)  - reference point to determine the distance to
#             reverse: (False) - order in reverse order: tanks nearest to the points first on list
#
#
#         """
#         pos = [tank.cog_when_full for tank in self.tanks]
#         pos = np.array(pos, dtype=float)
#         pos -= np.array(point)
#
#         dist = np.apply_along_axis(np.linalg.norm, 1, pos)
#
#         if reverse:
#             inds = np.argsort(dist)
#         else:
#             inds = np.argsort(-dist)
#
#         self.tanks = [self.tanks[i] for i in inds]
#
#     def order_tanks_to_maximize_inertia_moment(self):
#         """Re-order tanks such that tanks furthest from center of system are first on the list"""
#         self._order_tanks_to_inertia_moment()
#
#     def order_tanks_to_minimize_inertia_moment(self):
#         """Re-order tanks such that tanks nearest to center of system are first on the list"""
#         self._order_tanks_to_inertia_moment(maximize=False)
#
#     def _order_tanks_to_inertia_moment(self, maximize=True):
#         """Re-order tanks such that tanks furthest away from center of system are first on the list"""
#         pos = [tank.cog_when_full for tank in self.tanks]
#         m = [tank.capacity for tank in self.tanks]
#         pos = np.array(pos, dtype=float)
#         mxmymz = np.vstack((m, m, m)).transpose() * pos
#         total = np.sum(m)
#         point = sum(mxmymz) / total
#
#         if maximize:
#             self.order_tanks_by_distance_from_point(point)
#         else:
#             self.order_tanks_by_distance_from_point(point, reverse=True)
#
#     def tank_names(self):
#         return [tank.name for tank in self.tanks]
#
#     def fill_tank(self, name, fill):
#
#         assert1f(fill, "tank fill")
#
#         for tank in self.tanks:
#             if tank.name == name:
#                 tank.pct = fill
#                 return
#         raise ValueError("No tank with name {}".format(name))
#
#     def xyzw(self):
#         """Gets the current ballast cog in GLOBAL axis system weight from the tanks
#
#         Returns:
#             (x,y,z), weight [mT]
#         """
#         """Calculates the weight and inertia properties of the tanks"""
#
#         mxmymz = np.array((0.0, 0.0, 0.0))
#         wt = 0
#
#         for tank in self.tanks:
#             w = tank.volume * tank.density
#             p = np.array(tank.cog, dtype=float)
#             mxmymz += p * w
#
#             wt += w
#
#         if wt == 0:
#             xyz = np.array((0.0, 0.0, 0.0))
#         else:
#             xyz = mxmymz / wt
#
#         return xyz, wt
#
#     def empty_all_usable_tanks(self):
#         """Empties all non-frozen tanks.
#         Returns a list with tank number and fill percentage of all affected tanks. This can be used to restore the
#         ballast situation as it was before emptying.
#
#         See also: restore tank fillings
#         """
#         restore = []
#
#         for i, t in enumerate(self.tanks):
#             if not self.is_frozen(t.name):
#                 restore.append((i, t.fill_pct))
#                 t.fill_pct = 0
#
#         return restore
#
#     def restore_tank_fillings(self, restore):
#         """Restores the tank fillings as per restore.
#
#         Restore is typically obtained from the "empty_all_usable_tanks" function.
#
#         See Also: empty_all_usable_tanks
#         """
#
#         for r in restore:
#             i, pct = r
#             self.tanks[i].fill_pct = pct
#
#     def tank(self, name):
#
#         for t in self.tanks:
#             if t.name == name:
#                 return t
#         raise ValueError("No tank with name {}".format(name))
#
#     def __getitem__(self, item):
#         return self.tank(item)
#
#     @property
#     def cogx(self)->float:
#         """X position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]"""
#         return self.cog[0]
#
#     @property
#     def cogy(self)->float:
#         """Y position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]"""
#         return self.cog[1]
#
#     @property
#     def cogz(self)->float:
#         """Z position of combined CoG of all tank contents in the ballast-system. (global coordinate) [m]"""
#         return self.cog[2]
#
#     @property
#     def cog(self)->tuple[float,float,float]:
#         """Combined CoG of all tank contents in the ballast-system. (global coordinate) [m,m,m]"""
#         cog, wt = self.xyzw()
#         return (cog[0], cog[1], cog[2])
#
#     @property
#     def weight(self)->float:
#         """Total weight of all tank fillings in the ballast system [kN]"""
#         cog, wt = self.xyzw()
#         return wt * 9.81
#
#     def give_python_code(self):
#         code = "\n# code for {} and its tanks".format(self.name)
#
#         code += "\nbs = s.new_ballastsystem('{}', parent = '{}')".format(
#             self.name, self.parent.name
#         )
#
#         for tank in self.tanks:
#             code += "\nbs.tanks.append(s['{}'])".format(tank.name)
#
#         return code
#
#
# class WaveInteraction1(Node):
#     """
#     WaveInteraction
#
#     Wave-interaction-1 couples a first-order hydrodynamic database to an axis.
#
#     This adds:
#     - wave-forces
#     - damping
#     - added mass
#
#     The data is provided by a Hyddb1 object which is defined in the MaFreDo package. The contents are not embedded
#     but are to be provided separately in a file. This node contains only the file-name.
#
#     """
#
#     def __init__(self, scene, name : str):
#
#         Node.__init__(self, scene, name)
#
#         self.offset = [0, 0, 0]
#         """Position (x,y,z) of the hydrodynamic origin in its parents axis system"""
#
#         self.parent = None
#         """Parent : Axis-type"""
#
#         self.path = None
#         """Filename of a file that can be read by a Hyddb1 object"""
#
#     @property
#     def file_path(self)->str:
#         """Resolved path of the visual (str)
#         #NOGUI"""
#         return self._scene.get_resource_path(self.path)
#
#     def depends_on(self):
#         return [self.parent]
#
#     def give_python_code(self):
#         code = "# code for {}".format(self.name)
#
#         code += "\ns.new_waveinteraction(name='{}',".format(self.name)
#         code += "\n            parent='{}',".format(self.parent.name)
#         code += "\n            path=r'{}',".format(self.path)
#         code += "\n            offset=({}, {}, {}) )".format(*self.offset)
#
#         return code
#
#     @node_setter_manageable
#     def change_parent_to(self, new_parent):
#
#         if not (isinstance(new_parent, Frame)):
#             raise ValueError(
#                 "Hydrodynamic databases can only be attached to an axis (or derived)"
#             )
#
#         # get current position and orientation
#         if self.parent is not None:
#             cur_position = self.parent.to_glob_position(self.offset)
#         else:
#             cur_position = self.offset
#
#         self.parent = new_parent
#         self.offset = new_parent.to_loc_position(cur_position)
#
#
# # ============== Managed nodes
#
#
# class GeometricContact(Manager):  # Note: can not derive from Container because managed nodes is not equal to created nodes
#     """
#     GeometricContact
#
#     A GeometricContact can be used to construct geometric connections between circular members:
#         - 	steel bars and holes, such as a shackle pin in a padeye (pin-hole)
#         -	steel bars and steel bars, such as a shackle-shackle connection
#
#
#     Situation before creation of geometric contact:
#
#     Axis1
#         Point1
#             Circle1
#     Axis2
#         Point2
#             Circle2
#
#     Create a geometric contact with Circle1 and parent and Circle2 as child
#
#     Axis1
#         Point1              : observed, referenced as parent_circle_parent
#             Circle1         : observed, referenced as parent_circle
#
#         _axis_on_parent                 : managed    --> aligned with Circle1
#             _pin_hole_connection        : managed
#                 _connection_axial_rotation : managed
#                     _axis_on_child      : managed    --> aligned with Circle2
#                         Axis2           : managed    , referenced as child_circle_parent_parent
#                             Point2      : observed   , referenced as child_circle_parent
#                                 Circle2 : observed   , referenced as child_circle
#
#
#
#
#
#
#
#     """
#
#     def __init__(self, scene, name, child_circle, parent_circle, inside=True):
#         """
#         circle1 becomes the nodeB
#         circle2 becomes the nodeA
#
#         (attach circle 1 to circle 2)
#         Args:
#             scene:
#             parent_circle:
#             child_circle:
#             inside:
#         """
#
#         if child_circle.parent.parent is None:
#             raise ValueError(
#                 "The child circle needs to be located on an axis but is not."
#             )
#
#         Manager.__init__(self, scene, name)
#
#         name_prefix = self.name + vfc.MANAGED_NODE_IDENTIFIER
#
#         self._parent_circle = parent_circle
#         self._parent_circle_parent = parent_circle.parent  # point
#
#         self._child_circle = child_circle
#         self._child_circle_parent = child_circle.parent  # point
#         self._child_circle_parent_parent = child_circle.parent.parent  # axis
#
#         self._flipped = False
#         self._inside_connection = inside
#
#         self._axis_on_parent = self._scene.new_frame(
#             scene.available_name_like(name_prefix + "_axis_on_parent")
#         )
#         """Axis on the nodeA axis at the location of the center of hole or pin"""
#
#         self._pin_hole_connection = self._scene.new_frame(
#             scene.available_name_like(name_prefix + "_pin_hole_connection")
#         )
#         """axis between the center of the hole and the center of the pin. Free to rotate about the center of the hole as well as the pin"""
#
#         self._axis_on_child = self._scene.new_frame(
#             scene.available_name_like(name_prefix + "_axis_on_child")
#         )
#         """axis to which the slaved body is connected. Either the center of the hole or the center of the pin """
#
#         self._connection_axial_rotation = self._scene.new_frame(
#             scene.available_name_like(name_prefix + "_connection_axial_rotation")
#         )
#
#         # prohibit changes to nodes that were used in the creation of this connection
#         for node in self.managed_nodes():
#             node.manager = self
#
#         # observe circles and their points
#         self._parent_circle.observers.append(self)
#         self._parent_circle_parent.observers.append(self)
#
#         self._child_circle.observers.append(self)
#         self._child_circle_parent.observers.append(self)
#
#         self._child_circle_parent_parent._parent_for_code_export = None
#
#         self._update_connection()
#
#     def on_observed_node_changed(self, changed_node):
#         self._update_connection()
#
#     @property
#     def name(self)->str:
#         """Name of the node (str), must be unique"""
#         return self._name
#
#     @name.setter
#     def name(self, value):
#         assert self._scene.name_available(value), f"Name {value} already in use"
#
#         # not all managed nodes are created
#         self._rename_all_created_nodes(self._name, value)
#
#         self._name = value
#
#     @staticmethod
#     def _assert_parent_child_possible(parent, child):
#         if parent.parent.parent == child.parent.parent:
#             raise ValueError(
#                 f"A GeometricContact can not be created between two circles on the same axis or body. Both circles are located on {parent.parent.parent}"
#             )
#
#     @property
#     def child(self)->Circle:
#         """The Circle that is connected to the GeometricContact [Node]
#
#         See Also: parent
#         #NOGUI
#         """
#         return self._child_circle
#
#     @child.setter
#     def child(self, value):
#         new_child = self._scene._node_from_node_or_str(value)
#         if not isinstance(new_child, Circle):
#             raise ValueError(
#                 f"Child of a geometric contact should be a Circle, but {new_child.name} is a {type(new_child)}"
#             )
#
#         if new_child.parent.parent is None:
#             raise ValueError(
#                 f"Child circle {new_child.name} is not located on an axis or body and can thus not be used as child"
#             )
#
#         self._assert_parent_child_possible(self.parent, new_child)
#
#         store = self._scene.current_manager
#         self._scene.current_manager = self
#
#         # release old child
#         self._child_circle.observers.remove(self)
#         self._child_circle_parent.observers.remove(self)
#
#         # release the slaved axis system
#         self._child_circle_parent_parent._parent_for_code_export = True
#         self._child_circle_parent_parent.manager = None
#
#         # set new parent
#         self._child_circle = new_child
#         self._child_circle_parent = new_child.parent
#         self._child_circle_parent_parent = new_child.parent.parent
#
#         # and observe
#         self._child_circle.observers.append(self)
#         self._child_circle_parent.observers.append(self)
#
#         # and manage
#         self._child_circle_parent_parent._parent_for_code_export = None
#         self._child_circle_parent_parent.manager = self
#
#         self._scene.current_manager = store
#
#         self._update_connection()
#
#     @property
#     def parent(self)->Circle:
#         """The Circle that the GeometricConnection is connected to [Node]
#
#         See Also: child
#         #NOGUI
#         """
#         return self._parent_circle
#
#     @parent.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def parent(self, var):
#         if var is None:
#             raise ValueError(
#                 "Parent of a geometric contact should be a Circle, not None"
#             )
#
#         new_parent = self._scene._node_from_node_or_str(var)
#         if not isinstance(new_parent, Circle):
#             raise ValueError(
#                 f"Parent of a geometric contact should be a Circle, but {new_parent.name} is a {type(new_parent)}"
#             )
#
#         self._assert_parent_child_possible(new_parent, self.child)
#
#         # release old parent
#         self._parent_circle.observers.remove(self)
#         self._parent_circle_parent.observers.remove(self)
#
#         # set new parent
#         self._parent_circle = new_parent
#         self._parent_circle_parent = new_parent.parent
#
#         # and observe
#         self._parent_circle.observers.append(self)
#         self._parent_circle_parent.observers.append(self)
#
#         self._update_connection()
#
#     @node_setter_manageable
#     def change_parent_to(self, new_parent):
#         self.parent = new_parent
#
#     def delete(self):
#
#         # release management
#         for node in self.managed_nodes():
#             node._manager = None
#
#         self._child_circle_parent_parent.change_parent_to(None)
#
#         self._scene.delete(self._axis_on_child)
#         self._scene.delete(self._pin_hole_connection)
#         self._scene.delete(self._axis_on_parent)
#
#         # release observers
#         self._parent_circle.observers.remove(self)
#         self._parent_circle_parent.observers.remove(self)
#
#         self._child_circle.observers.remove(self)
#         self._child_circle_parent.observers.remove(self)
#
#     def _update_connection(self):
#
#         remember = self._scene.current_manager
#         self._scene.current_manager = self  # claim management
#
#         # get current properties
#
#         c_swivel = self.swivel
#         c_swivel_fixed = self.swivel_fixed
#         c_rotation_on_parent = self.rotation_on_parent
#         c_fixed_to_parent = self.fixed_to_parent
#         c_child_rotation = self.child_rotation
#         c_child_fixed = self.child_fixed
#
#         child_circle = self._child_circle  # nodeB
#         parent_circle = self._parent_circle  # nodeA
#
#         if child_circle.parent.parent is None:
#             raise ValueError(
#                 "The pin that is to be connected is not located on a Frame. Can not create the connection because there is no Frame for nodeB"
#             )
#
#         # --------- prepare hole
#
#         if parent_circle.parent.parent is not None:
#             self._axis_on_parent.parent = parent_circle.parent.parent
#             z = parent_circle.parent.parent.uz
#         else:
#             z = (0,0,1)
#         self._axis_on_parent.position = parent_circle.parent.position
#         self._axis_on_parent.fixed = (True, True, True, True, True, True)
#
#         # self._axis_on_parent.global_rotation = rotvec_from_y_and_z_axis_direction(parent_circle.global_axis, z)  # this rotation is not unique. It would be nice to have the Z-axis pointing "upwards" as much as possible; especially for the creation of shackles.
#         self._axis_on_parent.rotation = rotvec_from_y_and_z_axis_direction(parent_circle.axis, (0,0,1))  # this rotation is not unique. It would be nice to have the Z-axis pointing "upwards" as much as possible; especially for the creation of shackles.
#
#         # a1 = self._axis_on_parent.uy
#         # a2 = parent_circle.global_axis
#
#         # Position connection axis at the center of the nodeA axis (pin2)
#         # and allow it to rotate about the pin
#         self._pin_hole_connection.position = (0, 0, 0)
#         self._pin_hole_connection.parent = self._axis_on_parent
#         self._pin_hole_connection.fixed = (True, True, True, True, False, True)
#
#         self._connection_axial_rotation.parent = self._pin_hole_connection
#         self._connection_axial_rotation.position = (0, 0, 0)
#
#         # Position the connection pin (self) on the target pin and
#         # place the parent of the parent of the pin (the axis) on the connection axis
#         # and fix it
#         child_frame = child_circle.parent.parent
#
#         child_frame.parent = self._axis_on_child
#         # slaved_axis.rotation = rotation_from_y_axis_direction(-1 * np.array(pin1.axis))
#
#         # the child frame needs to be rotated by the inverse of the circle rotation
#         #
#         rotation = rotvec_from_y_and_z_axis_direction(y = child_circle.axis, z = (0,0,1)) # local rotation
#         child_frame.rotation = rotvec_inverse(rotation)
#
#         parent_to_point = child_frame.to_glob_direction(child_circle.parent.position)
#
#         child_frame.position = -np.array(self._axis_on_child.to_loc_direction(parent_to_point))
#
#         child_frame.fixed = True
#
#         self._axis_on_child.parent = self._connection_axial_rotation
#         self._axis_on_child.rotation = (0, 0, 0)
#         self._axis_on_child.fixed = (True, True, True, True, False, True)
#
#         if self._inside_connection:
#
#             # Place the pin in the hole
#             self._connection_axial_rotation.rotation = (0, 0, 0)
#             self._axis_on_child.position = (parent_circle.radius - child_circle.radius, 0, 0)
#
#         else:
#
#             # pin-pin connection
#             self._axis_on_child.position = (child_circle.radius + parent_circle.radius, 0, 0)
#             self._connection_axial_rotation.rotation = (90, 0, 0)
#
#         # restore settings
#         self.swivel = c_swivel
#         self.swivel_fixed = c_swivel_fixed
#         self.rotation_on_parent = c_rotation_on_parent
#         self.fixed_to_parent = c_fixed_to_parent
#         self.child_rotation = c_child_rotation
#         self.child_fixed = c_child_fixed
#
#         self._scene.current_manager = remember
#
#     def set_pin_pin_connection(self):
#         """Sets the connection to be of type pin-pin"""
#
#         self._inside_connection = False
#         if self.swivel == 0:
#             self.swivel = 90
#         elif self.swivel == 180:
#             self.swivel = 270
#
#         self._update_connection()
#
#     def set_pin_in_hole_connection(self):
#         """Sets the connection to be of type pin-in-hole
#
#         The axes of the two sheaves are aligned by rotating the slaved body
#         The axes of the two sheaves are placed at a distance hole_dia - pin_dia apart, perpendicular to the axis direction
#         An axes is created at the centers of the two sheaves
#         These axes are connected with a shore axis which is allowed to rotate relative to the nodeA axis
#         the nodeB axis is fixed to this rotating axis
#         """
#         self._inside_connection = True
#
#         if self.swivel == 90:
#             self.swivel = 0
#         elif self.swivel == 270:
#             self.swivel = 180
#
#         self._update_connection()
#
#     def managed_nodes(self):
#         """Returns a list of managed nodes"""
#
#         return [
#             self._child_circle_parent_parent,
#             self._axis_on_parent,
#             self._axis_on_child,
#             self._pin_hole_connection,
#             self._connection_axial_rotation,
#         ]
#
#     def depends_on(self):
#         return [self._parent_circle, self._child_circle]
#
#     def created_nodes(self):
#         """Nodes created by the geometric contact - Note that this is different from managed nodes"""
#         return (
#             self._axis_on_parent,
#             self._axis_on_child,
#             self._pin_hole_connection,
#             self._connection_axial_rotation,
#         )
#
#     def creates(self, node: Node):
#         return node in self.created_nodes()
#
#     @node_setter_manageable
#     def flip(self):
#         """Changes the swivel angle by 180 degrees"""
#         self.swivel = np.mod(self.swivel + 180, 360)
#
#     @node_setter_manageable
#     def change_side(self):
#         self.rotation_on_parent = np.mod(self.rotation_on_parent + 180, 360)
#         self.child_rotation = np.mod(self.child_rotation + 180, 360)
#
#     @property
#     def swivel(self)->float:
#         """Swivel angle between parent and child objects [degrees]"""
#         return self._connection_axial_rotation.rotation[0]
#
#     @swivel.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def swivel(self, value):
#         remember = self._scene.current_manager  # claim management
#         self._scene.current_manager = self
#         self._connection_axial_rotation.rx = value
#         self._scene.current_manager = remember  # restore old manager
#
#     @property
#     def swivel_fixed(self)->bool:
#         """Allow parent and child to swivel relative to eachother [boolean]"""
#         return self._connection_axial_rotation.fixed[3]
#
#     @swivel_fixed.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def swivel_fixed(self, value):
#         remember = self._scene.current_manager  # claim management
#         self._scene.current_manager = self
#         self._connection_axial_rotation.fixed = [True, True, True, value, True, True]
#         self._scene.current_manager = remember  # restore old manager
#
#     @property
#     def rotation_on_parent(self)->float:
#         """Angle between the line connecting the centers of the circles and the axis system of the parent node [degrees]"""
#         return self._pin_hole_connection.ry
#
#     @rotation_on_parent.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def rotation_on_parent(self, value):
#         remember = self._scene.current_manager  # claim management
#         self._scene.current_manager = self
#         self._pin_hole_connection.ry = value
#         self._scene.current_manager = remember  # restore old manager
#
#     @property
#     def fixed_to_parent(self)->bool:
#         """Allow rotation around parent [boolean]
#
#         see also: rotation_on_parent"""
#         return self._pin_hole_connection.fixed[4]
#
#     @fixed_to_parent.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def fixed_to_parent(self, value):
#         remember = self._scene.current_manager  # claim management
#         self._scene.current_manager = self
#         self._pin_hole_connection.fixed = [True, True, True, True, value, True]
#         self._scene.current_manager = remember  # restore old manager
#
#     @property
#     def child_rotation(self)->float:
#         """Angle between the line connecting the centers of the circles and the axis system of the child node [degrees]"""
#         return self._axis_on_child.ry
#
#     @child_rotation.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def child_rotation(self, value):
#         remember = self._scene.current_manager  # claim management
#         self._scene.current_manager = self
#         self._axis_on_child.ry = value
#         self._scene.current_manager = remember  # restore old manager
#
#     @property
#     def child_fixed(self)->bool:
#         """Allow rotation of child relative to connection, see also: child_rotation [boolean]"""
#         return self._axis_on_child.fixed[4]
#
#     @child_fixed.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def child_fixed(self, value):
#         remember = self._scene.current_manager  # claim management
#         self._scene.current_manager = self
#         self._axis_on_child.fixed = [True, True, True, True, value, True]
#         self._scene.current_manager = remember  # restore old manager
#
#     @property
#     def inside(self)->bool:
#         """Type of connection: True means child circle is inside parent circle, False means the child circle is outside but the circumferences contact [boolean]"""
#         return self._inside_connection
#
#     @inside.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def inside(self, value):
#         if value == self._inside_connection:
#             return
#
#         if value:
#             self.set_pin_in_hole_connection()
#         else:
#             self.set_pin_pin_connection()
#
#     def give_python_code(self):
#
#         old_manger = self._scene.current_manager
#         self._scene.current_manager = self
#
#         code = []
#
#         # code.append('#  create the connection')
#         code.append(f"s.new_geometriccontact(name = '{self.name}',")
#         code.append(f"                       child = '{self._child_circle.name}',")
#         code.append(f"                       parent = '{self._parent_circle.name}',")
#         code.append(f"                       inside={self.inside},")
#
#         if self.inside and self.swivel == 0:
#             pass  # default for inside
#         else:
#             if not self.inside and self.swivel == 90:
#                 pass  # default for outside
#             else:
#                 if (
#                     self.swivel_fixed
#                     or not self._scene._export_code_with_solved_function
#                 ):
#                     code.append(f"                       swivel={self.swivel},")
#                 else:
#                     code.append(f"                       swivel=solved({self.swivel}),")
#
#         if not self.swivel_fixed:
#             code.append(f"                       swivel_fixed={self.swivel_fixed},")
#
#         # There the three optional degrees of freedom:
#         #     gc.rotation_on_parent
#         #     gc.child_rotation
#         #     gc.swivel
#
#         if self.fixed_to_parent:
#             code.append(
#                 f"                       rotation_on_parent={self.rotation_on_parent},"
#             )
#             code.append(
#                 f"                       fixed_to_parent={self.fixed_to_parent},"
#             )
#         else:
#             if self._scene._export_code_with_solved_function:
#                 code.append(
#                     f"                       rotation_on_parent=solved({self.rotation_on_parent}),"
#                 )
#             else:
#                 code.append(
#                     f"                       rotation_on_parent={self.rotation_on_parent},"
#                 )
#
#         if self.child_fixed:
#             code.append(f"                       child_fixed={self.child_fixed},")
#             code.append(f"                       child_rotation={self.child_rotation},")
#         else:
#             if self._scene._export_code_with_solved_function:
#                 code.append(
#                     f"                       child_rotation=solved({self.child_rotation}),"
#                 )
#             else:
#                 code.append(
#                     f"                       child_rotation={self.child_rotation},"
#                 )
#
#         code = [
#             *code[:-1],
#             code[-1][:-1] + " )",
#         ]  # remove the , from the last entry [should be a quicker way to do this]
#
#         self._scene.current_manager = old_manger
#
#         return "\n".join(code)
#
#
# class Sling(Container):
#     """A Sling is a single wire with an eye on each end. The eyes are created by splicing the end of the sling back
#     into the itself.
#
#     The geometry of a sling is defined as follows:
#
#     diameter : diameter of the wire
#     LeyeA, LeyeB : inside lengths of the eyes
#     LsplicaA, LspliceB : the length of the splices
#     Ultimate length : the distance between the insides of ends of the eyes A and B when pulled straight (= Ultimate Length).
#
#     Stiffness:
#     The stiffness of the sling is specified by a single value: EA. EA can be set directly or by providing a k_total
#     This determines the stiffnesses of the individual parts as follows:
#     Wire in the eyes: EA
#     Splices: Infinity (rigid)
#
#     See Also: Grommet
#
#     """
#
#     SPLICE_AS_BEAM = False
#     """Model the splices as beams - could have some numerical benefits to allow compression"""
#
#     def __init__(
#         self,
#         scene,
#         name,
#         length,
#         LeyeA,
#         LeyeB,
#         LspliceA,
#         LspliceB,
#         diameter,
#         EA,
#         mass,
#         endA=None,
#         endB=None,
#         sheaves=None,
#     ):
#         """
#         Creates a new sling with the following structure
#
#             endA
#             eyeA (cable)
#
#             sa2 (body, mass/4)
#             splice (beam)
#             sa1 (body, mass/4)
#
#             main (cable)     [optional: runs over sheave]
#
#             sb1 (body, mass/4)
#             splice (beam)
#             sb2 (body, mass/4)
#
#             eyeB (cable)
#             endB
#
#         Args:
#             scene:     The scene in which the sling should be created
#             name:  Name prefix
#             length: Total length measured between the inside of the eyes of the sling is pulled straight.
#             LeyeA: Total inside length in eye A if stretched flat
#             LeyeB: Total inside length in eye B if stretched flat
#             LspliceA: Length of the splice at end A
#             LspliceB: Length of the splice at end B
#             diameter: Diameter of the sling
#             EA: Effective mean EA of the sling
#             mass: total mass
#             endA : Sheave or poi to fix end A of the sling to [optional]
#             endB : Sheave or poi to fix end A of the sling to [optional]
#             sheave : Sheave or poi for the nodeA part of the sling
#
#         Returns:
#
#         """
#
#         Manager.__init__(self, scene, name)
#         name_prefix = self.name + vfc.MANAGED_NODE_IDENTIFIER
#
#         # store the properties
#         self._length = length
#         self._LeyeA = LeyeA
#         self._LeyeB = LeyeB
#         self._LspliceA = LspliceA
#         self._LspliceB = LspliceB
#         self._diameter = diameter
#         self._EA = EA
#         self._mass = mass
#         self._endA = scene._poi_or_sheave_from_node(endA)
#         self._endB = scene._poi_or_sheave_from_node(endB)
#
#         # create the two splices
#
#         self.sa1 = scene.new_rigidbody(
#             scene.available_name_like(name_prefix + "spliceA1"), fixed=(False,False,False,True,True,True)
#         )
#
#         self.sa2 = scene.new_rigidbody(
#             scene.available_name_like(name_prefix + "spliceA2"), fixed=(False,False,False,True,True,True)
#         )
#
#         self.a1 = scene.new_point(
#             scene.available_name_like(name_prefix + "spliceA1p"), parent=self.sa1
#         )
#         self.a2 = scene.new_point(
#             scene.available_name_like(name_prefix + "spliceA2p"), parent=self.sa2
#         )
#
#
#         self.sb1 = scene.new_rigidbody(
#             scene.available_name_like(name_prefix + "spliceB1"),
#             rotation=(0, 0, 180),
#             fixed=(False,False,False,True,True,True),
#         )
#
#         self.sb2 = scene.new_rigidbody(
#             scene.available_name_like(name_prefix + "spliceB2"),
#             rotation=(0, 0, 180),
#             fixed=(False,False,False,True,True,True),
#         )
#
#
#
#         self.b1 = scene.new_point(
#             scene.available_name_like(name_prefix + "spliceB1p"), parent=self.sb1
#         )
#         self.b2 = scene.new_point(
#             scene.available_name_like(name_prefix + "spliceB2p"), parent=self.sb2
#         )
#
#
#         self.main = scene.new_cable(
#             scene.available_name_like(name_prefix + "main_part"),
#             endA=self.a1,
#             endB=self.b1,
#             length=1,
#             EA=1,
#             diameter=diameter,
#         )
#
#         self.eyeA = scene.new_cable(
#             scene.available_name_like(name_prefix + "eyeA"),
#             endA=self.a2,
#             endB=self.a2,
#             sheaves = self._endA,
#             length=1,
#             EA=1,
#         )
#         self.eyeB = scene.new_cable(
#             scene.available_name_like(name_prefix + "eyeB"),
#             endA=self.b2,
#             endB=self.b2,
#             sheaves=self._endB,
#             length=1,
#             EA=1,
#         )
#
#         # create splice cables
#
#         if self.SPLICE_AS_BEAM:
#             # Model splices as beams
#             self.spliceA = scene.new_beam(
#                 scene.available_name_like(name_prefix + "spliceA"),
#                 nodeA=self.sa1, nodeB=self.sa2,
#                 mass=0,
#                 EA=1,
#                 L=1,
#                 n_segments=1
#             )
#
#             self.spliceB = scene.new_beam(
#                 scene.available_name_like(name_prefix + "spliceB"),
#                 nodeA=self.sb1, nodeB=self.sb2,
#                 mass=0,
#                 EA=1,
#                 L=1,
#                 n_segments=1
#             )
#
#         else:
#             self.spliceA = scene.new_cable(
#                 scene.available_name_like(name_prefix + "spliceA"),
#                 endA=self.a1,
#                 endB=self.a2,
#                 length=1,
#                 EA=1,
#             )
#
#             self.spliceB = scene.new_cable(
#                 scene.available_name_like(name_prefix + "spliceB"),
#                 endA=self.b1,
#                 endB=self.b2,
#                 length=1,
#                 EA=1,
#             )
#
#             self.spliceA._draw_fat = True
#             self.spliceB._draw_fat = True
#             self.spliceA.color = (117,94,78)
#             self.spliceB.color = (117,94,78)
#
#
#
#
#
#         # Update properties
#         self.sheaves = sheaves
#         self._update_properties()
#
#         self._nodes = [
#             self.spliceA,
#             self.a1,
#             self.sa1,
#             self.a2,
#             self.sa2,
#             # self.am,
#             # self.avis,
#             # self.sb,
#             self.b1,
#             self.sb1,
#             self.b2,
#             self.sb2,
#             self.spliceB,
#             # self.bvis,
#             self.main,
#             self.eyeA,
#             self.eyeB,
#         ]
#
#         for n in self._nodes:
#             n.manager = self
#
#
#
#     @property
#     def _Lmain(self):
#         """Length of the main section"""
#         return (
#             self._length - self._LspliceA - self._LspliceB - self._LeyeA - self._LeyeB
#         )
#
#
#     def _calcEyeWireLength(self, Leye):
#         r = 0.5 * self._diameter
#         straight = np.sqrt(Leye ** 2 - r ** 2)
#         alpha = np.arccos(r / Leye)
#         circular_length_rad = 2 * (np.pi - alpha)
#         bend = circular_length_rad * r
#
#         return 2 * straight + bend
#
#     @property
#     def _LwireEyeA(self):
#         """The length of wire used to create the eye on side A.
#
#         This is calculated from the inside length and the diameter of the sling. The inside length of the eye is
#         measured around a pin with zero diameter.
#         """
#         return self._calcEyeWireLength(self._LeyeA)
#
#
#     @property
#     def _LwireEyeB(self):
#         return self._calcEyeWireLength(self._LeyeB)
#
#     @property
#     def k_total(self)->float:
#         """Total stiffness of the sling [kN/m]"""
#
#         k_eye_A = 4 * self._EA / self._LwireEyeA
#         k_eye_B = 4 * self._EA / self._LwireEyeB
#
#         k_splice_A = 2 * self._EA / (self._LspliceA)
#         k_splice_B = 2 * self._EA / (self._LspliceB)
#
#         k_main = self._EA / self._Lmain
#
#         k_total = 1 / (
#             1 / k_eye_A + 1 / k_eye_B + 1 / k_splice_A + 1 / k_splice_B + 1 / k_main
#         )
#
#         return k_total
#
#     @k_total.setter
#     def k_total(self, value):
#         assert1f_positive_or_zero(value)
#
#         EA = (
#             0.25
#             * value
#             * (
#                 self._LwireEyeA
#                 + self._LwireEyeB
#                 + 4.0 * self._Lmain
#                 + 2.0 * self.LspliceA
#                 + 2.0 * self._LspliceB
#             )
#         )
#
#         self.EA = EA
#
#     def _update_properties(self):
#
#         # The stiffness of the main part is corrected to account for the stiffness of the splices.
#         # It is considered that the stiffness of the splices is two times that of the wire.
#         #
#         # Springs in series: 1/Ktotal = 1/k1 + 1/k2 + 1/k3
#
#         backup = self._scene.current_manager  # store
#         self._scene.current_manager = self
#
#         Lmain = (
#             self._length - self._LspliceA - self._LspliceB - self._LeyeA - self._LeyeB
#         )
#
#
#         self.sa1.mass = self._mass / 4
#         self.sa2.mass = self._mass / 4
#         self.sb1.mass = self._mass / 4
#         self.sb2.mass = self._mass / 4
#
#         self.main.length = Lmain
#         self.main.EA = self._EA
#         self.main.diameter = self._diameter
#         self.main.connections = tuple([self.a2, *self._sheaves, self.b2])
#
#         if self.SPLICE_AS_BEAM:
#             self.spliceA.L = self._LspliceA
#             self.spliceB.L = self._LspliceB
#         else:
#             self.spliceA.length = self._LspliceA
#             self.spliceB.length = self._LspliceB
#
#         self.spliceA.EA = 2*self._EA
#         self.spliceA.diameter = 2*self._diameter
#
#         self.spliceB.EA = 2*self._EA
#         self.spliceB.diameter = 2*self._diameter
#
#         self.eyeA.length = self._LwireEyeA
#         self.eyeA.EA = self._EA
#         self.eyeA.diameter = self._diameter
#
#         if self._endA is not None:
#             self.eyeA.connections = (self.a1, self._endA, self.a1)
#         else:
#             raise ValueError('End A needs to be connected to something')
#             # self.eyeA.connections = (self.a1, self.a1)
#
#         self.eyeB.length = self._LwireEyeB
#         self.eyeB.EA = self._EA
#         self.eyeB.diameter = self._diameter
#
#         if self._endB is not None:
#             self.eyeB.connections = (self.b1, self._endB, self.b1)
#         else:
#             raise ValueError('End B needs to be connected to something')
#             # self.eyeB.connections = (self.b1, self.b1)
#
#         # Set positions of splice bodies
#         A = np.array(self._endA.global_position)
#         B = np.array(self._endB.global_position)
#
#         D = B-A
#         Lmain = (
#                 self._length - self._LspliceA - self._LspliceB - self._LeyeA - self._LeyeB
#         )
#
#         if self._endA is not None and self._endB is not None:
#
#
#             # endA
#
#             a = np.array(self._endA.global_position)
#             if len(self.connections) > 2:
#                 p = np.array(self._scene._node_from_node_or_str(self.connections[1]).global_position)
#             else:
#                 p = np.array(self._endB.global_position)
#
#             dir = p - a
#             if np.linalg.norm(dir) > 1e-6:
#                 dir /= np.linalg.norm(dir)
#                 self.sa1.position = a + (self._LeyeA) * dir
#                 self.sa2.position = a + (self._LeyeA + self._LspliceA) * dir
#
#             # endB
#
#             b = np.array(self._endB.global_position)
#             if len(self.connections) > 2:
#                 p = np.array(self._scene._node_from_node_or_str(self.connections[-2]).global_position)
#             else:
#                 p = np.array(self._endA.global_position)
#
#             dir = p - b
#             if np.linalg.norm(dir) > 1e-6:
#                 dir /= np.linalg.norm(dir)
#                 self.sb1.position = b + self._LeyeB * dir
#                 self.sb2.position = b + (self._LeyeB + self._LspliceB) * dir
#
#
#         self._scene.current_manager = backup  # restore
#
#     def depends_on(self):
#         """The sling depends on the endpoints and sheaves (if any)"""
#
#         a = list()
#
#         if self._endA is not None:
#             a.append(self._endA)
#         if self._endB is not None:
#             a.append(self._endB)
#
#         a.extend(self.sheaves)
#
#         return a
#
#
#
#     @property
#     def spliceApos(self)->tuple[float,float,float,float,float,float]:
#         """The 6-dof of splice on end A. Solved [m,m,m,m,m,m]
#         #NOGUI"""
#         return (*self.sa1.position, *self.sa2.position)
#
#     @spliceApos.setter
#     def spliceApos(self, value):
#         self.sa1._vfNode.position = value[:3]
#         self.sa2._vfNode.position = value[3:]
#
#     @property
#     def spliceBpos(self) -> tuple[float, float, float, float, float, float]:
#         """The 6-dof of splice on end A. Solved [m,m,m,m,m,m]
#         #NOGUI"""
#         return (*self.sb1.position, *self.sb2.position)
#
#     @spliceBpos.setter
#     def spliceBpos(self, value):
#         self.sb1._vfNode.position = value[:3]
#         self.sb2._vfNode.position = value[3:]
#
#     # @property
#     # def spliceAposrot(self)->tuple[float,float,float,float,float,float]:
#     #     """The 6-dof of splice on end A. Solved [m,m,m,deg,deg,deg]
#     #     #NOGUI"""
#     #     pass
#     #     # return (*self.sa.position, *self.sa.rotation)
#     #
#     # @spliceAposrot.setter
#     # def spliceAposrot(self, value):
#     #     pass
#     #     # self.sa._vfNode.position = value[:3]
#     #     # self.sa._vfNode.rotation = np.deg2rad(value[3:])
#     #
#     # @property
#     # def spliceBposrot(self)->tuple[float,float,float,float,float,float]:
#     #     """The 6-dof of splice on end B. Solved [m,m,m,deg,deg,deg]
#     #     #NOGUI"""
#     #     pass
#     #     # return (*self.sb.position, *self.sb.rotation)
#     #
#     # @spliceBposrot.setter
#     # def spliceBposrot(self, value):
#     #     pass
#     #     # self.sb._vfNode.position = value[:3]
#     #     # self.sb._vfNode.rotation = np.deg2rad(value[3:])
#
#     @property
#     def connections(self)->tuple[Point or Circle]:
#         """List or Tuple of nodes (Points or Circles) that this sling is connected to. Nodes may be passed by name (string) or by reference.
#         """
#         return (self.endA, *self.main.connections[1:-1], self.endB)
#
#     @connections.setter
#     def connections(self, value):
#         with ClaimManagement(self._scene, self):
#             self.endA = value[0]
#             self.endB = value[-1]
#
#             # ma = self.main.connections[0]
#             # mb = self.main.connections[-1]
#             self.sheaves = value[1:-1]
#
#             # self.main.connections = (ma, *value[1:-1], mb)
#
#     @property
#     def reversed(self) -> tuple[bool]:
#         """The directions over which the sling runs over any intermediate connection circles"""
#         return (False, *self.main.reversed[1:-1], False)
#
#     @reversed.setter
#     def reversed(self, value):
#         with ClaimManagement(self._scene, self):
#             self.main.reversed = (False, *value[1:-1], False)
#
#     @property
#     def tension(self) -> float:
#         """Tension in (main part of) the sling [kN]"""
#         return self.main.tension
#
#     def give_python_code(self):
#         code = f"# Exporting {self.name}"
#
#         code += "\n# Create sling"
#
#         # (self, scene, name, Ltotal, LeyeA, LeyeB, LspliceA, LspliceB, diameter, EA, mass, endA = None, endB=None, sheaves=None):
#
#         code += f'\nsl = s.new_sling("{self.name}", length = {self.length:.6g},'
#         code += f"\n            LeyeA = {self.LeyeA:.6g},"
#         code += f"\n            LeyeB = {self.LeyeB:.6g},"
#         code += f"\n            LspliceA = {self.LspliceA:.6g},"
#         code += f"\n            LspliceB = {self.LspliceB:.6g},"
#         code += f"\n            diameter = {self.diameter:.6g},"
#         code += f"\n            EA = {self.EA:.6g},"
#         code += f"\n            mass = {self.mass:.6g},"
#         code += f'\n            endA = "{self.endA.name}",'
#         code += f'\n            endB = "{self.endB.name}",'
#
#         if self.sheaves:
#             sheaves = "["
#             for s in self.sheaves:
#                 sheaves += f'"{s.name}", '
#             sheaves = sheaves[:-2] + "]"
#         else:
#             sheaves = "None"
#
#         code += f"\n            sheaves = {sheaves})"
#         code += "\nsl.spliceApos = ({},{},{},{},{},{}) # solved".format(*self.spliceApos)
#         code += "\nsl.spliceBpos = ({},{},{},{},{},{}) # solved".format(*self.spliceBpos)
#
#         if self.sheaves:
#             if np.any(self.reversed):
#                 code += f"\nsl.reversed = {self.reversed}"
#
#
#         return code
#
#     # properties
#     @property
#     def length(self)->float:
#         """Total length measured between the INSIDE of the eyes of the sling is pulled straight. [m]"""
#         return self._length
#
#     @length.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def length(self, value):
#
#         min_length = self.LeyeA + self.LeyeB + self.LspliceA + self.LspliceB
#         if value <= min_length:
#             raise ValueError(
#                 "Total length of the sling should be at least the length of the eyes plus the length of the splices"
#             )
#
#         self._length = value
#         self._update_properties()
#
#     @property
#     def LeyeA(self)->float:
#         """Total length inside eye A if stretched flat [m]"""
#         return self._LeyeA
#
#     @LeyeA.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def LeyeA(self, value):
#
#         max_length = self.length - (self.LeyeB + self.LspliceA + self.LspliceB)
#         if value >= max_length:
#             raise ValueError(
#                 "Total length of the sling should be at least the length of the eyes plus the length of the splices"
#             )
#
#         self._LeyeA = value
#         self._update_properties()
#
#     @property
#     def LeyeB(self)->float:
#         """Total length inside eye B if stretched flat [m]"""
#         return self._LeyeB
#
#     @LeyeB.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def LeyeB(self, value):
#
#         max_length = self.length - (self.LeyeA + self.LspliceA + self.LspliceB)
#         if value >= max_length:
#             raise ValueError(
#                 "Total length of the sling should be at least the length of the eyes plus the length of the splices"
#             )
#
#         self._LeyeB = value
#         self._update_properties()
#
#     @property
#     def LspliceA(self)->float:
#         """Length of the splice at end A [m]"""
#         return self._LspliceA
#
#     @LspliceA.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def LspliceA(self, value):
#
#         max_length = self.length - (self.LeyeA + self.LeyeB + self.LspliceB)
#         if value >= max_length:
#             raise ValueError(
#                 "Total length of the sling should be at least the length of the eyes plus the length of the splices"
#             )
#
#         self._LspliceA = value
#         self._update_properties()
#
#     @property
#     def LspliceB(self)->float:
#         """Length of the splice at end B [m]"""
#         return self._LspliceB
#
#     @LspliceB.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def LspliceB(self, value):
#
#         max_length = self.length - (self.LeyeA + self.LeyeB + self.LspliceA)
#         if value >= max_length:
#             raise ValueError(
#                 "Total length of the sling should be at least the length of the eyes plus the length of the splices"
#             )
#
#         self._LspliceB = value
#         self._update_properties()
#
#     @property
#     def diameter(self)->float:
#         """Diameter of the sling (except the splices) [m]"""
#         return self._diameter
#
#     @diameter.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def diameter(self, value):
#         self._diameter = value
#         self._update_properties()
#
#     @property
#     def EA(self)->float:
#         """EA of the wire of the sling [kN]
#         See also: k_total"""
#         return self._EA
#
#     @EA.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def EA(self, value):
#         self._EA = value
#         self._update_properties()
#
#     @property
#     def mass(self)->float:
#         """Mass and weight of the sling. This mass is distributed over the two splices [mT]"""
#         return self._mass
#
#     @mass.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def mass(self, value):
#         self._mass = value
#         self._update_properties()
#
#     @property
#     def endA(self)->Circle or Point:
#         """End A [circle or point node]
#         #NOGUI"""
#         return self._endA
#
#     @endA.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def endA(self, value):
#         node = self._scene._node_from_node_or_str(value)
#         self._endA = self._scene._poi_or_sheave_from_node(node)
#         self._update_properties()
#
#     @property
#     def endB(self)->Circle or Point:
#         """End B [circle or point node]
#         #NOGUI"""
#         return self._endB
#
#     @endB.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def endB(self, value):
#         node = self._scene._node_from_node_or_str(value)
#         self._endB = self._scene._poi_or_sheave_from_node(node)
#         self._update_properties()
#
#     @property
#     def sheaves(self)->tuple[Circle or Point]:
#         """List of sheaves (circles, points) that the sling runs over between the two ends.
#
#         May be provided as list of nodes or node-names.
#         #NOGUI
#         """
#         return self._sheaves
#
#     @sheaves.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def sheaves(self, value):
#         s = []
#         for v in value:
#             node = self._scene._node_from_node_or_str(v)
#             s.append(self._scene._poi_or_sheave_from_node(node))
#         self._sheaves = s
#         self._update_properties()
#
# class RigidBodyContainer(Container, RigidBody):
#     """A container that is also a rigid body - used by Shackles and LiftPoint"""
#
#     def __init__(self, scene, name):
#         RigidBody.__init__(self, scene, name)
#         Container.__init__(self, scene, name)
#
#
#
#     @property
#     def name(self)->str:
#         """Name of the node (str), must be unique"""
#         return RigidBody.name.fget(self)
#
#     @name.setter
#     def name(self, value):
#         RigidBody.name.fset(self, value)  # rename self
#         Container.name.fset(self, value)  # rename managed nodes
#
#     def dissolve(self) -> tuple:
#         """First try to dissolve the container, then see if we can dissolve the rigidbody as well"""
#
#         s = self._scene
#
#         # first check if it is possible to dissolve
#         # but temporary set as fully fixed because free dofs are a case that we CAN handle
#         remember_fixed = self.fixed
#         self.fixed = True
#         can, reason = Frame._can_dissolve(self, allowed_managers=(self, None))
#         self.fixed = remember_fixed
#         if not can:
#             return False, reason
#
#         # start with actual dissolve
#
#         RB = s.new_rigidbody(s.available_name_like(self.name + "_dissolved"),
#                         position=self.position,
#                         rotation=self.rotation,
#                         mass=self.mass,
#                         inertia_radii=self.inertia_radii,
#                         fixed=self.fixed,
#                         parent=self.parent,
#                         )
#
#         # un-manage
#
#         # created nodes == managed nodes
#         for node in self._nodes:
#             if node.manager == self:
#                 node._manager = None
#
#         # re-parent
#         for node in self._nodes:
#             if getattr(node, 'parent', None) == self:
#                 node.parent = RB
#
#         # try to dissolve the rigidBody
#         s.dissolve_attempt(RB)
#
#         self._dissolved = True
#
#         if self.name == "system_3/Shackle":
#             print('stop here')
#
#         s.delete(self)
#
#         return True, ""
#
# class Shackle(RigidBodyContainer):
#     """
#     Shackle catalog
#     - GP: Green-Pin Heavy Duty Bow Shackle BN (P-6036 Green Pin® Heavy Duty Bow Shackle BN (mm))
#     - WB: P-6033 Green Pin® Sling Shackle BN (mm)
#
#
#     visual from: https://www.traceparts.com/en/product/green-pinr-p-6036-green-pinr-heavy-duty-bow-shackle-bn-hdgphm0800-mm?CatalogPath=TRACEPARTS%3ATP04001002006&Product=10-04072013-086517&PartNumber=HDGPHM0800
#     details from:
#      - https://www.greenpin.com/sites/default/files/2019-04/brochure-april-2019.pdf
#      - https://www.thecrosbygroup.com/products/shackles/heavy-lift/crosby-2140-alloy-bolt-type-shackles/
#      -
#
#
#
#     Returns:
#
#     """
#
#     data = dict()
#     _suppressed_node_editors = [RigidBody]
#
#     # Read the shackle data
#
#
#     cdir = Path(dirname(__file__))
#     filename = cdir / './resources/shackle_data.csv'
#
#     if filename.exists():
#         with open(filename, newline='') as csvfile:
#             __shackle_data = csv.reader(csvfile)
#             header = __shackle_data.__next__()  # skip the header
#
#             for row in __shackle_data:
#                 name = row[0]
#                 data[name] = row[1:]
#
#
#     else:
#         warnings.warn(f'Could not load shackle data because {filename} does not exist')
#
#     # ======================
#
#
#
#
#     def defined_kinds(self):
#         """Defined shackle kinds"""
#         list = [a for a in Shackle.data.keys()]
#         return list
#
#     @staticmethod
#     def shackle_kind_properties(kind):
#         if kind not in Shackle.data:
#             for key in Shackle.data.keys():
#                 print(key)
#             raise ValueError(
#                 f"No data available for a Shackle of kind {kind}. Available values printed above"
#             )
#
#         data = Shackle.data[kind]
#         return {'kind':kind,
#                 'description':data[0],
#                 'WLL':float(data[1]),
#                 'MBL':float(data[2]),
#                 'weight':float(data[3]),
#                 'pin_diameter':float(data[4]),
#                 'bow_diameter':float(data[5]),
#                 'inside_length':float(data[6]),
#                 'inside_width':float(data[7]),
#                 'visual':data[8],
#                 'scale':float(data[9])}
#
#     def __init__(self, scene, name, kind='GP800'):
#
#         _ = self.shackle_kind_properties(kind)  # to make sure it exists
#
#         RigidBodyContainer.__init__(self, scene, name)
#
#         # origin is at center of pin
#         # z-axis up
#         # y-axis in direction of pin
#
#         # self.body = scene.new_rigidbody(name=name + '_body')
#
#         # pin
#         self.pin_point = scene.new_point(
#             name=name + "/pin_point", parent=self, position=(0.0, 0.0, 0.0)
#         )
#         self.pin = scene.new_circle(
#             name=name + "/pin", parent=self.pin_point, axis=(0.0, 1.0, 0.0)
#         )
#
#         # bow
#         self.bow_point = scene.new_point(name=name + "/bow_point", parent=self)
#
#         self.bow = scene.new_circle(
#             name=name + "/bow", parent=self.bow_point, axis=(0.0, 1.0, 0.0)
#         )
#
#         # inside circle
#         self.inside_point = scene.new_point(
#             name=name + "/inside_circle_center", parent=self
#         )
#         self.inside = scene.new_circle(
#             name=name + "/inside", parent=self.inside_point, axis=(1.0, 0, 0)
#         )
#
#         # code for GP800_visual
#         self.visual_node = scene.new_visual(
#             name=name + "/visual",
#             parent=self,
#             path=r"res: shackle_gp800.obj",
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#         )
#
#         self.kind = kind
#
#         self.inside_point._visible = False
#         self.bow_point._visible = False
#         self.pin_point._visible = False
#
#         self._nodes = [
#             self.pin_point,
#             self.pin,
#             self.bow_point,
#             self.bow,
#             self.inside_point,
#             self.inside,
#             self.visual_node,
#         ]
#
#         for node in self._nodes:
#             node._manager = self
#
#         self.name = name  # do not set name in managed nodes, names there are already set
#         # so that would raise an error
#
#     @property
#     def kind(self)->str:
#         """Type of shackle, for example GP800 [text]"""
#         return self._kind
#
#     @kind.setter
#     # @node_setter_manageable   : allow changing of shackle kind
#     @node_setter_observable
#     def kind(self, kind):
#
#         values = self.shackle_kind_properties(kind)
#         weight = values['weight'] / 1000  # convert to tonne
#         pin_dia = values['pin_diameter'] / 1000
#         bow_dia = values['bow_diameter'] / 1000
#         bow_length_inside = values['inside_length'] / 1000
#         bow_circle_inside = values['inside_width'] / 1000
#
#         cogz = 0.5 * pin_dia + bow_length_inside / 3  # estimated
#
#         remember = self._scene.current_manager
#
#         self._scene.current_manager = (
#             self.manager
#         )  # WORK-AROUND : in case the shackle itself is managed, fake management
#
#         self.mass = weight
#         self.cog = (0, 0, cogz)
#
#         self._scene.current_manager = self  # register self a manager (as it should)
#
#         self.pin.radius = pin_dia / 2
#
#         self.bow_point.position = (
#             0.0,
#             0.0,
#             0.5 * pin_dia + bow_length_inside + 0.5 * bow_dia,
#         )
#         self.bow.radius = bow_dia / 2
#
#         self.inside_point.position = (
#             0,
#             0,
#             0.5 * pin_dia + bow_length_inside - 0.5 * bow_circle_inside,
#         )
#         self.inside.radius = bow_circle_inside / 2
#
#         self.visual_node.path = values['visual']
#         scale = values['scale']
#         self.visual_node.scale = [scale, scale, scale]
#
#         self._scene.current_manager = remember
#
#         self._kind = kind
#
#
#
#
#
#
#     @property
#     def shackle_data_dict(self) -> dict:
#         """Returns the shackle data for the actual shackle kind"""
#         return self.shackle_kind_properties(self._kind)
#
#     @property
#     def MBL(self) -> float:
#         """MBL [t]"""
#         return self.shackle_data_dict['MBL']
#
#     @property
#     def load(self)-> float:
#         """The force traveling through this shackle [kN]
#
#         Calculated as the maximum absolute value of all nodes attached to the shackle as well as the connection force. May be incorrect
#         for situations where more than two nodes connect to different locations on the shackle.
#         """
#         s = self._scene  # alias
#         F = 0            # initial value
#
#         child_nodes = s.nodes_with_parent(self, recursive=False)
#
#         F = max(F, np.linalg.norm(self.connection_force[:3]))
#         F = max(F, np.linalg.norm(self.applied_force[:3]))
#
#         for node in child_nodes:
#             if isinstance(node, Frame):
#                 F = max(F, np.linalg.norm(node.connection_force[:3]))
#             elif isinstance(node, Point):
#                 F = max(F, np.linalg.norm(node.applied_force[:3]))
#
#         return F
#
#
#     def give_python_code(self):
#         code = f"# Exporting {self.name}"
#
#         code += "\n# Create Shackle"
#         code += f'\ns.new_shackle("{self.name}", kind = "{self.kind}")'  # , elastic={self.elastic})'
#
#         if self.parent_for_export:
#             code += f"\ns['{self.name}'].parent = s['{self.parent_for_export.name}']"
#
#         code += "\ns['{}'].position = ({:.6g},{:.6g},{:.6g})".format(self.name, *self.position)
#         code += "\ns['{}'].rotation = ({:.6g},{:.6g},{:.6g})".format(self.name, *self.rotation)
#         if not np.all(self.fixed):
#             code += "\ns['{}'].fixed = ({},{},{},{},{},{})".format(
#                 self.name, *self.fixed
#             )
#
#         return code
#
#
#
# class Component(SubScene, Frame):
#     """Components are frame-nodes containing a scene. The imported scene is referenced by a file-name. All impored nodes
#     are placed in the components frame.
#     """
#
#     def __init__(self, scene, name):
#         SubScene.__init__(self, scene, name=name)
#         Frame.__init__(self, scene, name=name)
#
#         self._path = ""
#
#         self._exposed = []
#         """List of tuples containing the exposed properties (if any)"""
#
#     @property
#     def name(self)->str:
#         """Name of the node (str), must be unique"""
#         return SubScene.name.fget(self)
#
#     @name.setter
#     @node_setter_manageable
#     def name(self, value):
#
#         SubScene.name.fset(self, value)
#         self._vfNode.name = value
#
#     def _import_scene_func(self, other_scene):
#         self._scene.import_scene(
#             other=other_scene,
#             prefix=self.name + "/",
#             container=self,
#             settings=False,  # do not import environment and other settings
#         )
#
#     def give_python_code(self):
#
#         code = []
#         code.append("# code for {}".format(self.name))
#         code.append("c = s.new_component(name='{}',".format(self.name))
#         code.append("               path=r'{}',".format(self.path))
#         if self.parent_for_export:
#             code.append("           parent='{}',".format(self.parent_for_export.name))
#
#         # position
#
#         if self.fixed[0] or not self._scene._export_code_with_solved_function:
#             code.append("           position=({:.6g},".format(self.position[0]))
#         else:
#             code.append("           position=(solved({:.6g}),".format(self.position[0]))
#         if self.fixed[1] or not self._scene._export_code_with_solved_function:
#             code.append("                     {:.6g},".format(self.position[1]))
#         else:
#             code.append("                     solved({:.6g}),".format(self.position[1]))
#         if self.fixed[2] or not self._scene._export_code_with_solved_function:
#             code.append("                     {:.6g}),".format(self.position[2]))
#         else:
#             code.append("                     solved({:.6g})),".format(self.position[2]))
#
#         # rotation
#
#         if self.fixed[3] or not self._scene._export_code_with_solved_function:
#             code.append("           rotation=({:.6g},".format(self.rotation[0]))
#         else:
#             code.append("           rotation=(solved({:.6g}),".format(self.rotation[0]))
#         if self.fixed[4] or not self._scene._export_code_with_solved_function:
#             code.append("                     {:.6g},".format(self.rotation[1]))
#         else:
#             code.append("                     solved({:.6g}),".format(self.rotation[1]))
#         if self.fixed[5] or not self._scene._export_code_with_solved_function:
#             code.append("                     {:.6g}),".format(self.rotation[2]))
#         else:
#             code.append("                     solved({:.6g})),".format(self.rotation[2]))
#
#         # fixeties
#         code.append("           fixed =({}, {}, {}, {}, {}, {}) )".format(*self.fixed))
#
#         code.append(self.add_footprint_python_code())
#
#         # exposed properties (if any)
#         for ep in self.exposed_properties:
#             code.append(f"c.set_exposed('{ep}', {self.get_exposed(ep)})")
#
#         return '\n'.join(code)
#
#
# # =================== None-Node Classes
#
# """This is a container for a DC.MomentDiagram object providing plot methods"""
#
#
# class LoadShearMomentDiagram:
#     def __init__(self, datasource):
#         """
#
#         Args:
#             datasource: DC.MomentDiagram object
#         """
#
#         self.datasource = datasource
#
#     def give_shear_and_moment(self, grid_n=100):
#         """Returns (position, shear, moment)"""
#         x = self.datasource.grid(grid_n)
#         return x, self.datasource.Vz, self.datasource.My
#
#     def give_loads_table(self):
#         """Returns a 'table' with all the loads.
#         point_loads : (Name, location, force, moment) ; all local
#         distributed load : (Name, Fz, mean X, start x , end x
#         """
#
#         m = self.datasource  # alias
#         n = m.nLoads
#
#         point_loads = []
#         distributed_loads = []
#         for i in range(n):
#
#             load = list(m.load_origin(i))
#             effect = m.load(i)
#
#             plotx = effect[0]
#
#             is_distributed = len(plotx) > 2
#
#             if is_distributed:
#                 load[0] += ' *' #(add a * to the name))
#
#             if (
#                     np.linalg.norm(load[2]) > 1e-6 or np.linalg.norm(load[3]) > 1e-6
#             ):  # only forces that actually do something
#                 point_loads.append(load)
#
#             if is_distributed:
#
#                 name = effect[-1]  # name without the *
#                 P = load[1]
#                 F = load[2]
#                 M = load[3]
#
#                 Fz = F[2]
#                 My = M[1]
#
#                 if abs(Fz)> 1e-10:
#                     dx = -My / Fz
#                     x = P[0] + dx
#                 else:
#                     x = P[0]
#
#                 distributed_loads.append([name, Fz, x, plotx[0], plotx[-1]])
#
#         return point_loads, distributed_loads
#
#     def plot_simple(self, **kwargs):
#         """Plots the bending moment and shear in a single yy-plot.
#         Creates a new figure
#
#         any keyword arguments are passed to plt.figure(), so for example dpi=150 will increase the dpi
#
#         Returns: figure
#         """
#         x, Vz, My = self.give_shear_and_moment()
#         import matplotlib.pyplot as plt
#
#         plt.rcParams.update({"font.family": "sans-serif"})
#         plt.rcParams.update({"font.sans-serif": "consolas"})
#         plt.rcParams.update({"font.size": 10})
#
#         fig, ax1 = plt.subplots(1, 1, **kwargs)
#         ax2 = ax1.twinx()
#
#         ax1.plot(x, My, "g", lw=1, label="Bending Moment")
#         ax2.plot(x, Vz, "b", lw=1, label="Shear Force")
#
#         from DAVE.gui.helpers.align_zeros_of_yyplots import align_y0_axis
#
#         align_y0_axis(ax1, ax2)
#
#         ax1.set_xlabel("Position [m]")
#         ax1.set_ylabel("Bending Moment [kNm]")
#         ax2.set_ylabel("Shear Force [kN]")
#
#         ax1.tick_params(axis="y", colors="g")
#         ax2.tick_params(axis="y", colors="b")
#
#         # fig.legend()  - obvious from the axis
#
#         ext = 0.1 * (np.max(x) - np.min(x))
#         xx = [np.min(x) - ext, np.max(x) + ext]
#         ax1.plot(xx, [0, 0], c=[0.5, 0.5, 0.5], lw=1, linestyle=":")
#         ax1.set_xlim(xx)
#
#         return fig
#
#     def plot(self, grid_n=100, merge_adjacent_loads=True, filename=None, do_show=False):
#         """Plots the load, shear and bending moments. Returns figure"""
#         m = self.datasource  # alias
#
#         x = m.grid(grid_n)
#         linewidth = 1
#
#         n = m.nLoads
#
#         import matplotlib.pyplot as plt
#
#         #
#         plt.rcParams.update({"font.family": "sans-serif"})
#         plt.rcParams.update({"font.sans-serif": "consolas"})
#         plt.rcParams.update({"font.size": 6})
#
#         fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(8.27, 11.69), dpi=100)
#         textsize = 6
#
#         # get loads
#
#         loads = [m.load(i) for i in range(n)]
#
#         texts = []  # for label placement
#         texts_second = []  # for label placement
#
#         # merge loads with same source and matching endpoints
#
#         if merge_adjacent_loads:
#
#             to_be_plotted = [loads[0]]
#
#             for load in loads[1:]:
#                 name = load[2]
#
#                 # if the previous load is a continuous load from the same source
#                 # and the current load is also a continuous load
#                 # then merge the two.
#                 prev_load = to_be_plotted[-1]
#
#                 if len(prev_load[0]) != 2:  # not a point-load
#                     if len(load[0]) != 2:  # not a point-load
#                         if prev_load[2] == load[2]:  # same name
#
#                             # merge the two
#                             # remove the last (zero) entry of the previous lds
#                             # as well as the first entry of these
#
#                             # smoothed
#                             xx = [*prev_load[0][:-1], *load[0][2:]]
#                             yy = [
#                                 *prev_load[1][:-2],
#                                 0.5 * (prev_load[1][-2] + load[1][1]),
#                                 *load[1][2:],
#                             ]
#
#                             to_be_plotted[-1] = (xx, yy, load[2])
#
#                             continue
#                 # else
#                 if np.max(np.abs(load[1])) > 1e-6:
#                     to_be_plotted.append(load)
#
#         else:
#             to_be_plotted = loads
#
#         #
#         from matplotlib import cm
#
#         colors = cm.get_cmap("hsv", lut=len(to_be_plotted))
#
#         from matplotlib.patches import Polygon
#
#         ax0_second = ax0.twinx()
#
#         for icol, ld in enumerate(to_be_plotted):
#
#             xx = ld[0]
#             yy = ld[1]
#             name = ld[2]
#
#             if np.max(np.abs(yy)) < 1e-6:
#                 continue
#
#             is_concentrated = len(xx) == 2
#
#             # determine the name, default to Force / q-load if no name is present
#             if name == "":
#                 if is_concentrated:
#                     name = "Force "
#                 else:
#                     name = "q-load "
#
#             col = [0.8 * c for c in colors(icol)]
#             col[3] = 1.0  # alpha
#
#             if is_concentrated:  # concentrated loads on left axis
#                 lbl = f" {name} {ld[1][1]:.2f}"
#                 texts.append(
#                     ax0.text(
#                         xx[0], yy[1], lbl, fontsize=textsize, horizontalalignment="left"
#                     )
#                 )
#                 ax0.plot(xx, yy, label=lbl, color=col, linewidth=linewidth)
#                 if yy[1] > 0:
#                     ax0.plot(xx[1], yy[1], marker="^", color=col, linewidth=linewidth)
#                 else:
#                     ax0.plot(xx[1], yy[1], marker="v", color=col, linewidth=linewidth)
#
#             else:  # distributed loads on right axis
#                 lbl = f"{name}"  # {yy[1]:.2f} kN/m at {xx[0]:.3f}m .. {yy[-2]:.2f} kN/m at {xx[-1]:.3f}m"
#
#                 vertices = [(xx[i], yy[i]) for i in range(len(xx))]
#
#                 ax0_second.add_patch(
#                     Polygon(vertices, facecolor=[col[0], col[1], col[2], 0.2])
#                 )
#                 ax0_second.plot(xx, yy, label=lbl, color=col, linewidth=linewidth)
#
#                 lx = np.mean(xx)
#                 ly = np.interp(lx, xx, yy)
#
#                 texts_second.append(
#                     ax0_second.text(
#                         lx,
#                         ly,
#                         lbl,
#                         color=[0, 0, 0],
#                         horizontalalignment="center",
#                         fontsize=textsize,
#                     )
#                 )
#
#         ax0.grid()
#         ax0.set_title("Loads")
#         ax0.set_ylabel("Load [kN]")
#         ax0_second.set_ylabel("Load [kN/m]")
#
#         # plot moments
#         # each concentrated load may have a moment as well
#         for i in range(m.nLoads):
#             mom = m.moment(i)
#             if np.linalg.norm(mom) > 1e-6:
#                 load = m.load(i)
#                 xx = load[0][0]
#                 lbl = f"{load[2]}, m = {mom[1]:.2f} kNm"
#                 ax0.plot(xx, 0, marker="x", label=lbl, color=(0, 0, 0, 1))
#                 texts.append(
#                     ax0.text(
#                         xx, 0, lbl, horizontalalignment="center", fontsize=textsize
#                     )
#                 )
#
#         fig.legend(loc="upper right")
#
#         # add a zero-line
#         xx = [np.min(x), np.max(x)]
#         ax0.plot(xx, (0, 0), "k-")
#
#         from DAVE.gui.helpers.align_zeros_of_yyplots import align_y0_axis
#
#         align_y0_axis(ax0, ax0_second)
#
#         from DAVE.reporting.utils.TextAvoidOverlap import minimizeTextOverlap
#
#         minimizeTextOverlap(
#             texts_second,
#             fig=fig,
#             ax=ax0_second,
#             vertical_only=True,
#             optimize_initial_positions=False,
#             annotate=False,
#         )
#         minimizeTextOverlap(
#             texts,
#             fig=fig,
#             ax=ax0,
#             vertical_only=True,
#             optimize_initial_positions=False,
#             annotate=False,
#         )
#
#         ax0.spines["top"].set_visible(False)
#         ax0.spines["bottom"].set_visible(False)
#
#         ax0_second.spines["top"].set_visible(False)
#         ax0_second.spines["bottom"].set_visible(False)
#
#         dx = (np.max(x) - np.min(x)) / 20  # plot scale
#         ax1.plot(x, m.Vz, "k-", linewidth=linewidth)
#
#         i = np.argmax(m.Vz)
#         ax1.plot((x[i] - dx, x[i] + dx), (m.Vz[i], m.Vz[i]), "k-", linewidth=0.5)
#         ax1.text(x[i], m.Vz[i], f"{m.Vz[i]:.2f}", va="bottom", ha="center")
#
#         i = np.argmin(m.Vz)
#         ax1.plot((x[i] - dx, x[i] + dx), (m.Vz[i], m.Vz[i]), "k-", linewidth=0.5)
#         ax1.text(x[i], m.Vz[i], f"{m.Vz[i]:.2f}", va="top", ha="center")
#
#         ax1.grid()
#         ax1.set_title("Shear")
#         ax1.set_ylabel("[kN]")
#
#         ax2.plot(x, m.My, "k-", linewidth=linewidth)
#
#         i = np.argmax(m.My)
#         ax2.plot((x[i] - dx, x[i] + dx), (m.My[i], m.My[i]), "k-", linewidth=0.5)
#         ax2.text(x[i], m.My[i], f"{m.My[i]:.2f}", va="bottom", ha="center")
#
#         i = np.argmin(m.My)
#         ax2.plot((x[i] - dx, x[i] + dx), (m.My[i], m.My[i]), "k-", linewidth=0.5)
#         ax2.text(x[i], m.My[i], f"{m.My[i]:.2f}", va="top", ha="center")
#
#         ax2.grid()
#         ax2.set_title("Moment")
#         ax2.set_ylabel("[kN*m]")
#
#         if do_show:
#             plt.show()
#         if filename is not None:
#             fig.savefig(filename)
#
#         return fig
#
#
# # ======= Register nodes and documentation =====
#
# from DAVE.settings import DAVE_ADDITIONAL_RUNTIME_MODULES,RESOURCE_PATH
#
# DAVE_ADDITIONAL_RUNTIME_MODULES['Watch'] = Watch
# DAVE_ADDITIONAL_RUNTIME_MODULES['AreaKind'] = AreaKind
# DAVE_ADDITIONAL_RUNTIME_MODULES['BallastSystem'] = BallastSystem
# DAVE_ADDITIONAL_RUNTIME_MODULES['Beam'] = Beam
# DAVE_ADDITIONAL_RUNTIME_MODULES['Buoyancy'] = Buoyancy
# DAVE_ADDITIONAL_RUNTIME_MODULES['Cable'] = Cable
# DAVE_ADDITIONAL_RUNTIME_MODULES['Circle'] = Circle
# DAVE_ADDITIONAL_RUNTIME_MODULES['Component'] = Component
# DAVE_ADDITIONAL_RUNTIME_MODULES['Connector2d'] = Connector2d
# DAVE_ADDITIONAL_RUNTIME_MODULES['ContactBall'] = ContactBall
# DAVE_ADDITIONAL_RUNTIME_MODULES['ContactMesh'] = ContactMesh
# DAVE_ADDITIONAL_RUNTIME_MODULES['CurrentArea'] = CurrentArea
# DAVE_ADDITIONAL_RUNTIME_MODULES['Force'] = Force
# DAVE_ADDITIONAL_RUNTIME_MODULES['Frame'] = Frame
# DAVE_ADDITIONAL_RUNTIME_MODULES['GeometricContact'] = GeometricContact
# DAVE_ADDITIONAL_RUNTIME_MODULES['HydSpring'] = HydSpring
# DAVE_ADDITIONAL_RUNTIME_MODULES['LC6d'] = LC6d
# DAVE_ADDITIONAL_RUNTIME_MODULES['LoadShearMomentDiagram'] = LoadShearMomentDiagram
# DAVE_ADDITIONAL_RUNTIME_MODULES['Point'] = Point
# DAVE_ADDITIONAL_RUNTIME_MODULES['RigidBody'] = RigidBody
# DAVE_ADDITIONAL_RUNTIME_MODULES['Shackle'] = Shackle
# DAVE_ADDITIONAL_RUNTIME_MODULES['Sling'] = Sling
# DAVE_ADDITIONAL_RUNTIME_MODULES['SPMT'] = SPMT
# DAVE_ADDITIONAL_RUNTIME_MODULES['Tank'] = Tank
# DAVE_ADDITIONAL_RUNTIME_MODULES['TriMeshSource'] = TriMeshSource
# DAVE_ADDITIONAL_RUNTIME_MODULES['Visual'] = Visual
# DAVE_ADDITIONAL_RUNTIME_MODULES['WaveInteraction1'] = WaveInteraction1
# DAVE_ADDITIONAL_RUNTIME_MODULES['WindArea'] = WindArea
#
# # ABSTRACTS
# DAVE_ADDITIONAL_RUNTIME_MODULES['Manager'] = Manager
# DAVE_ADDITIONAL_RUNTIME_MODULES['Node'] = Node
# DAVE_ADDITIONAL_RUNTIME_MODULES['NodeWithParentAndFootprint'] = NodeWithParentAndFootprint
# DAVE_ADDITIONAL_RUNTIME_MODULES['_Area'] = _Area
# DAVE_ADDITIONAL_RUNTIME_MODULES['CoreConnectedNode'] = CoreConnectedNode
#
# # Helpers
# DAVE_ADDITIONAL_RUNTIME_MODULES['AreaKind'] = AreaKind
# DAVE_ADDITIONAL_RUNTIME_MODULES['ClaimManagement'] = ClaimManagement
# DAVE_ADDITIONAL_RUNTIME_MODULES['VisualOutlineType'] = VisualOutlineType
#
#
# # Register the documentation
#
# cdir = Path(dirname(__file__))
# filename = cdir / './resources/node_prop_info.csv'
# from DAVE.settings import DAVE_NODEPROP_INFO, NodePropertyInfo
#
# if filename.exists():
#
#     types = DAVE_ADDITIONAL_RUNTIME_MODULES.copy()
#     types['tuple'] = tuple
#     types['int'] = int
#     types['float'] = float
#     types['bool'] = bool
#     types['str'] = str
#     types['dict'] = type(dict)
#
#     btypes = dict()
#     btypes['True'] = True
#     btypes['False'] = False
#     btypes['true'] = True
#     btypes['false'] = False
#
#
#     with open(filename, newline='') as csvfile:
#         prop_reader = csv.reader(csvfile)
#         header = prop_reader.__next__()  # skip the header
#         for row in prop_reader:
#             cls_name = row[0]
#             cls = DAVE_ADDITIONAL_RUNTIME_MODULES[cls_name]
#
#             prop_name = row[1]
#             val_type = types[row[2]]
#
#             info = NodePropertyInfo(node_class=cls,
#                                     property_name=row[1],
#                                     property_type=val_type,
#                                     doc_short=row[3],
#                                     units=row[4],
#                                     remarks=row[5],
#                                     is_settable=btypes[row[6]],
#                                     is_single_settable=btypes[row[7]],
#                                     is_single_numeric=btypes[row[8]],
#                                     doc_long=row[9])
#
#             if cls not in DAVE_NODEPROP_INFO:
#                 DAVE_NODEPROP_INFO[cls] = dict()
#             DAVE_NODEPROP_INFO[cls][prop_name]=info
#
# else:
#     print(f'Could not register node property info because {filename} does not exist')
