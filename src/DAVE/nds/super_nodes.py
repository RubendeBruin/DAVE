"""Nodes composed of basic nodes.

Sling
Shackle

"""


from os.path import dirname

from .geometry import Frame, Point, Circle
from .core import RigidBody
from .mixins import *

#
# class SimpleSling(NodePurePython, HasContainer):
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
#         scene.assert_name_available(name)
#
#         super().__init__(scene=scene, name=name)
#         name_prefix = self.name + "/"
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
#             scene.available_name_like(name_prefix + "spliceA1"),
#             fixed=(False, False, False, True, True, True),
#         )
#
#         self.sa2 = scene.new_rigidbody(
#             scene.available_name_like(name_prefix + "spliceA2"),
#             fixed=(False, False, False, True, True, True),
#         )
#
#         self.a1 = scene.new_point(
#             scene.available_name_like(name_prefix + "spliceA1p"), parent=self.sa1
#         )
#         self.a2 = scene.new_point(
#             scene.available_name_like(name_prefix + "spliceA2p"), parent=self.sa2
#         )
#
#         self.sb1 = scene.new_rigidbody(
#             scene.available_name_like(name_prefix + "spliceB1"),
#             rotation=(0, 0, 180),
#             fixed=(False, False, False, True, True, True),
#         )
#
#         self.sb2 = scene.new_rigidbody(
#             scene.available_name_like(name_prefix + "spliceB2"),
#             rotation=(0, 0, 180),
#             fixed=(False, False, False, True, True, True),
#         )
#
#         self.b1 = scene.new_point(
#             scene.available_name_like(name_prefix + "spliceB1p"), parent=self.sb1
#         )
#         self.b2 = scene.new_point(
#             scene.available_name_like(name_prefix + "spliceB2p"), parent=self.sb2
#         )
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
#             sheaves=self._endA,
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
#                 nodeA=self.sa1,
#                 nodeB=self.sa2,
#                 mass=0,
#                 EA=1,
#                 L=1,
#                 n_segments=1,
#             )
#
#             self.spliceB = scene.new_beam(
#                 scene.available_name_like(name_prefix + "spliceB"),
#                 nodeA=self.sb1,
#                 nodeB=self.sb2,
#                 mass=0,
#                 EA=1,
#                 L=1,
#                 n_segments=1,
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
#             self.spliceA.color = (117, 94, 78)
#             self.spliceB.color = (117, 94, 78)
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
#     def dissolve(self):
#         HasContainer.dissolve(self)
#         self.__class__ = NodePurePython
#         self._scene.delete(self)
#
#     @property
#     def _Lmain(self):
#         """Length of the main section"""
#         return (
#             self._length - self._LspliceA - self._LspliceB - self._LeyeA - self._LeyeB
#         )
#
#     def _calcEyeWireLength(self, Leye):
#         r = 0.5 * self._diameter
#         straight = np.sqrt(Leye**2 - r**2)
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
#     @property
#     def _LwireEyeB(self):
#         return self._calcEyeWireLength(self._LeyeB)
#
#     @property
#     def k_total(self) -> float:
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
#         self.spliceA.EA = 2 * self._EA
#         self.spliceA.diameter = 2 * self._diameter
#
#         self.spliceB.EA = 2 * self._EA
#         self.spliceB.diameter = 2 * self._diameter
#
#         self.eyeA.length = self._LwireEyeA
#         self.eyeA.EA = self._EA
#         self.eyeA.diameter = self._diameter
#
#         if self._endA is not None:
#             self.eyeA.connections = (self.a1, self._endA, self.a1)
#         else:
#             raise ValueError("End A needs to be connected to something")
#             # self.eyeA.connections = (self.a1, self.a1)
#
#         self.eyeB.length = self._LwireEyeB
#         self.eyeB.EA = self._EA
#         self.eyeB.diameter = self._diameter
#
#         if self._endB is not None:
#             self.eyeB.connections = (self.b1, self._endB, self.b1)
#         else:
#             raise ValueError("End B needs to be connected to something")
#             # self.eyeB.connections = (self.b1, self.b1)
#
#         # Set positions of splice bodies
#         A = np.array(self._endA.global_position)
#         B = np.array(self._endB.global_position)
#
#         D = B - A
#         Lmain = (
#             self._length - self._LspliceA - self._LspliceB - self._LeyeA - self._LeyeB
#         )
#
#         if self._endA is not None and self._endB is not None:
#             # endA
#
#             a = np.array(self._endA.global_position)
#             if len(self.connections) > 2:
#                 p = np.array(
#                     self._scene._node_from_node_or_str(
#                         self.connections[1]
#                     ).global_position
#                 )
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
#                 p = np.array(
#                     self._scene._node_from_node_or_str(
#                         self.connections[-2]
#                     ).global_position
#                 )
#             else:
#                 p = np.array(self._endA.global_position)
#
#             dir = p - b
#             if np.linalg.norm(dir) > 1e-6:
#                 dir /= np.linalg.norm(dir)
#                 self.sb1.position = b + self._LeyeB * dir
#                 self.sb2.position = b + (self._LeyeB + self._LspliceB) * dir
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
#     @property
#     def spliceApos(self) -> tuple[float, float, float, float, float, float]:
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
#     def connections(self) -> tuple[Point or Circle]:
#         """List or Tuple of nodes (Points or Circles) that this sling is connected to. Nodes may be passed by name (string) or by reference."""
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
#         code += "\nsl.spliceApos = ({},{},{},{},{},{}) # solved".format(
#             *self.spliceApos
#         )
#         code += "\nsl.spliceBpos = ({},{},{},{},{},{}) # solved".format(
#             *self.spliceBpos
#         )
#
#         if self.sheaves:
#             if np.any(self.reversed):
#                 code += f"\nsl.reversed = {self.reversed}"
#
#         return code
#
#     # properties
#     @property
#     def length(self) -> float:
#         """Total length measured between the INSIDE of the eyes of the sling is pulled straight. [m]"""
#         return self._length
#
#     @length.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def length(self, value):
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
#     def LeyeA(self) -> float:
#         """Total length inside eye A if stretched flat [m]"""
#         return self._LeyeA
#
#     @LeyeA.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def LeyeA(self, value):
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
#     def LeyeB(self) -> float:
#         """Total length inside eye B if stretched flat [m]"""
#         return self._LeyeB
#
#     @LeyeB.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def LeyeB(self, value):
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
#     def LspliceA(self) -> float:
#         """Length of the splice at end A [m]"""
#         return self._LspliceA
#
#     @LspliceA.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def LspliceA(self, value):
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
#     def LspliceB(self) -> float:
#         """Length of the splice at end B [m]"""
#         return self._LspliceB
#
#     @LspliceB.setter
#     @node_setter_manageable
#     @node_setter_observable
#     def LspliceB(self, value):
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
#     def diameter(self) -> float:
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
#     def EA(self) -> float:
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
#     def mass(self) -> float:
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
#     def endA(self) -> Circle or Point:
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
#     def endB(self) -> Circle or Point:
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
#     def sheaves(self) -> tuple[Circle or Point]:
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


class Component(Frame, HasSubScene):
    """Components are frame-nodes containing a scene. The imported scene is referenced by a file-name. All impored nodes
    are placed in the components frame.
    """

    def __init__(self, scene, name):
        super().__init__(scene=scene, name=name)

        self._path = ""

        self._exposed = []
        """List of tuples containing the exposed properties (if any)"""

    def _import_scene_func(self, other_scene):
        self._scene.import_scene(
            other=other_scene,
            prefix=self.name + "/",
            container=self,
            settings=False,  # do not import environment and other settings
        )

    def dissolve(self):
        """Unmanange all contained nodes, downcast self to Frame"""

        HasSubScene.dissolve(self)
        self.__class__ = Frame

    def give_python_code(self):
        code = []
        code.append("# code for {}".format(self.name))
        code.append("c = s.new_component(name='{}',".format(self.name))
        code.append("               path=r'{}',".format(self.path))
        if self.parent_for_export:
            code.append("           parent='{}',".format(self.parent_for_export.name))

        # position

        if self.fixed[0] or not self._scene._export_code_with_solved_function:
            code.append("           position=({:.6g},".format(self.position[0]))
        else:
            code.append("           position=(solved({:.6g}),".format(self.position[0]))
        if self.fixed[1] or not self._scene._export_code_with_solved_function:
            code.append("                     {:.6g},".format(self.position[1]))
        else:
            code.append("                     solved({:.6g}),".format(self.position[1]))
        if self.fixed[2] or not self._scene._export_code_with_solved_function:
            code.append("                     {:.6g}),".format(self.position[2]))
        else:
            code.append(
                "                     solved({:.6g})),".format(self.position[2])
            )

        # rotation

        if self.fixed[3] or not self._scene._export_code_with_solved_function:
            code.append("           rotation=({:.6g},".format(self.rotation[0]))
        else:
            code.append("           rotation=(solved({:.6g}),".format(self.rotation[0]))
        if self.fixed[4] or not self._scene._export_code_with_solved_function:
            code.append("                     {:.6g},".format(self.rotation[1]))
        else:
            code.append("                     solved({:.6g}),".format(self.rotation[1]))
        if self.fixed[5] or not self._scene._export_code_with_solved_function:
            code.append("                     {:.6g}),".format(self.rotation[2]))
        else:
            code.append(
                "                     solved({:.6g})),".format(self.rotation[2])
            )

        # fixeties
        code.append("           fixed =({}, {}, {}, {}, {}, {}) )".format(*self.fixed))

        code.append(self.add_footprint_python_code())

        # exposed properties (if any)
        for ep in self.exposed_properties:
            code.append(f"c.set_exposed('{ep}', {self.get_exposed(ep)})")

        return "\n".join(code)
