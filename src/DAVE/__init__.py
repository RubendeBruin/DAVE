from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "useDAVE"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "2.2.3 (build 231205)"
finally:
    del version, PackageNotFoundError

from . import auto_download
from .scene import Scene
from .nodes import *
from .exceptions import ModelInvalidException

# Convenience helper to set __all__
# generate = list(DAVE_ADDITIONAL_RUNTIME_MODULES.keys()) + [
#     "ModelInvalidException",
#     "Scene",
# ]
# print(generate)

__all__ = [
    "Watch",
    "AreaKind",
    "BallastSystem",
    "Beam",
    "Buoyancy",
    "Cable",
    "Circle",
    "Component",
    "Connector2d",
    "ContactBall",
    "ContactMesh",
    "CurrentArea",
    "Force",
    "Frame",
    "GeometricContact",
    "HydSpring",
    "LC6d",
    "LoadShearMomentDiagram",
    "Point",
    "RigidBody",
    # "SimpleSling",
    "SPMT",
    "Tank",
    "TriMeshSource",
    "Visual",
    "WaveInteraction1",
    "WindArea",
    "WindOrCurrentArea",
    "DAVENodeBase",
    "NodeCoreConnected",
    "NodePurePython",
    "Manager",
    "Node",
    "HasFootprint",
    "HasTrimesh",
    "HasParent",
    "HasSubScene",
    "HasContainer",
    "RigidBodyContainer",
    "ClaimManagement",
    "VisualOutlineType",
    "ModelInvalidException",
    "Scene",
    "DG",
]


# convenience function for showing the gui
def DG(scene=None, bare=False, block=True):
    print("loading gui")
    from .gui import Gui

    # try to load all optional packages
    if not bare:
        try:
            import DAVE_timeline.gui
        except:
            pass

        try:
            import DAVE_reporting.gui
        except:
            pass

        try:
            import DAVE_BaseExtensions.gui
        except:
            pass

        try:
            import DAVE_rigging.gui
        except:
            pass

        try:
            import DAVE_vessels.gui
        except:
            pass

        try:
            import netCDF4
        except:
            pass

        try:
            import DAVE_dynamics.gui
        except:
            pass

        try:
            from HD import HEBO_CraneVessel
            import HD.gui
        except:
            pass

    return Gui(scene, block=block)
