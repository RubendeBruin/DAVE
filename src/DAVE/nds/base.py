"""Fully implemented base classes"""

from .abstracts import *
from .core import RigidBody
from .geometry import Frame, Point, Circle
from .enums import *
from .mixins import NodeCoreConnected, HasParentCore, HasContainer, Manager
from ..tools import *



class RigidBodyContainer(RigidBody, HasContainer):
    """A container that is also a rigid body - used by Shackles and LiftPoint"""

    def __init__(self, scene, name):
        scene.assert_name_available(name)
        super().__init__(scene=scene, name=name)

    def dissolve(self):
        """Dissolve the container,
        downcast self to a rigidbody"""

        Manager.dissolve_some(self)

        del self._nodes
        self.__class__ = RigidBody


    def dissolve_some(self) -> tuple[bool, str]:
        """First try to dissolve the container, then see if we can dissolve the rigidbody as well"""

        return super().dissolve_some()
