"""Fully implemented base classes"""

from .abstracts import *
from .core import RigidBody
from .geometry import Frame, Point, Circle
from .enums import *
from .mixins import NodeCoreConnected, HasParentCore, Container
from ..tools import *



class RigidBodyContainer(RigidBody, Container):
    """A container that is also a rigid body - used by Shackles and LiftPoint"""

    def __init__(self, scene, name):
        scene.assert_name_available(name)
        super().__init__(scene=scene, name=name)

    def dissolve(self) -> tuple[bool, str]:
        """First try to dissolve the container, then see if we can dissolve the rigidbody as well"""

        return super().dissolve()

        #
        # s = self._scene
        #
        # # first check if it is possible to dissolve
        # # but temporary set as fully fixed because free dofs are a case that we CAN handle
        # remember_fixed = self.fixed
        # self.fixed = True
        # can, reason = Frame._can_dissolve(self, allowed_managers=(self, None))
        # self.fixed = remember_fixed
        # if not can:
        #     return False, reason
        #
        # # start with actual dissolve
        #
        # RB = s.new_rigidbody(s.available_name_like(self.name + "_dissolved"),
        #                 position=self.position,
        #                 rotation=self.rotation,
        #                 mass=self.mass,
        #                 inertia_radii=self.inertia_radii,
        #                 fixed=self.fixed,
        #                 parent=self.parent,
        #                 )
        #
        # # un-manage
        #
        # # created nodes == managed nodes
        # for node in self._nodes:
        #     if node.manager == self:
        #         node._manager = None
        #
        # # re-parent
        # for node in self._nodes:
        #     if getattr(node, 'parent', None) == self:
        #         node.parent = RB
        #
        # # try to dissolve the rigidBody
        # s.dissolve_attempt(RB)
        #
        # self._dissolved = True
        #
        # s.delete(self)
        #
        # return True, ""

