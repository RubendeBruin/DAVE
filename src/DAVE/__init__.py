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
from .scene import Scene, NodeSelector
from .nodes import *
from .exceptions import ModelInvalidException
from .helpers.profiling_timing import TimeElapsed

from .annotations import custom_layers  # defines the custom annotation layers

# Convenience helper to set __all__
# generate = list(DAVE_ADDITIONAL_RUNTIME_MODULES.keys()) + [
#     "ModelInvalidException",
#     "Scene",
# ]
# print(generate)

__all__ = [
    "NodeSelector",
    "Measurement",
    "MeasurementDirection",
    "MeasurementType",
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
    "HasParentAbstract",
    "HasSubScene",
    "HasContainer",
    "RigidBodyContainer",
    "ClaimManagement",
    "VisualOutlineType",
    "ModelInvalidException",
    "Scene",
    "DAVE_load_extensions",
    "DG",
    "TimeElapsed",
]


def DAVE_load_extensions():
    """Attempts to load all optional packages."""
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


# convenience function for showing the gui
def DG(
    scene: object = None,
    bare: object = False,
    block: object = True,
    autosave=True,
    filename=None,
    workspace=None,
) -> "DAVE.gui.Gui":
    print("loading gui")
    from .gui import Gui

    # try to load all optional packages
    if not bare:
        DAVE_load_extensions()

    return Gui(
        scene,
        block=block,
        autosave_enabled=autosave,
        filename=filename,
        workspace=workspace,
    )
