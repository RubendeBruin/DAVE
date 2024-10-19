"""Fully implemented base classes"""

from .core import RigidBody
from .mixins import HasContainer, Manager


class RigidBodyContainer(RigidBody, HasContainer):
    """A container that is also a rigid body - used by Shackles, GrommetProtector and LiftPoint"""

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


# register -- can not register in because of circular imports
# from .. import DAVE_ADDITIONAL_RUNTIME_MODULES
#
# DAVE_ADDITIONAL_RUNTIME_MODULES["RigidBodyContainer"] = RigidBodyContainer


class RigidBodyContainerMassReadOnly(RigidBodyContainer):
    """A RigidBodyContainer of which the mass and inertia properties are made read-only

    This is done by overriding the properties from RigidBody and making them read-only.
    By only defining a getter, we make the property read-only.
    trying to set the property will raise an AttributeError: AttributeError: property 'mass' of 'Shackle' object has no setter
    we need:
            "mass",
            "inertia",
            "cogx",
            "cogy",
            "cogz",
           "cog",
           "inertia_radii",

    To be able to use the properties internally, add private setter methods as replacement.

    """

    @property
    def mass(self) -> float:
        """Mass [t]"""
        return super().mass

    @property
    def inertia(self) -> float:
        """Inertia [t]"""
        return super().inertia

    @property
    def cogx(self) -> float:
        """Center of gravity x-coordinate [m]"""
        return super().cogx

    @property
    def cogy(self) -> float:
        """Center of gravity y-coordinate [m]"""
        return super().cogy

    @property
    def cogz(self) -> float:
        """Center of gravity z-coordinate [m]"""
        return super().cogz

    @property
    def cog(self) -> tuple[float, float, float]:
        """Center of gravity [m,m,m]"""
        return super().cog

    @property
    def inertia_radii(self) -> tuple[float, float, float]:
        """Radii of gyration [m,m,m]"""
        return super().inertia_radii

    @property
    def inertia_position(self) -> tuple[float, float, float]:
        """Radii of gyration [m,m,m]"""
        return super().inertia_position

    # def _set_mass(self, value: float):
    #     """Set the mass [t]"""
    #     RigidBody.mass.fset(self, value)
    #
    # def _set_inertia(self, value: float):
    #     """Set the inertia [t]"""
    #     RigidBody.inertia.fset(self, value)
    #
    # def _set_cogx(self, value: float):
    #     """Set the center of gravity x-coordinate [m]"""
    #     RigidBody.cogx.fset(self, value)
    #
    # def _set_cogy(self, value: float):
    #     """Set the center of gravity y-coordinate [m]"""
    #     RigidBody.cogy.fset(self, value)
    #
    # def _set_cogz(self, value: float):
    #     """Set the center of gravity z-coordinate [m]"""
    #     RigidBody.cogz.fset(self, value)
    #
    # def _set_cog(self, value: tuple[float, float, float]):
    #     """Set the center of gravity [m,m,m]"""
    #     RigidBody.cog.fset(self, value)
    #
    # def _set_inertia_radii(self, value: tuple[float, float, float]):
    #     """Set the radii of gyration [m,m,m]"""
    #     RigidBody.inertia_radii.fset(self, value)
