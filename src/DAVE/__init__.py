import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "useDAVE"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from . import auto_download
from .scene import *
from .nodes import *
from .exceptions import ModelInvalidException

__all__ = list(DAVE_ADDITIONAL_RUNTIME_MODULES.keys()) + [
    "ModelInvalidException",
    "Scene",
]


# convenience function for showing the gui
def gui(scene=None):
    print("loading gui")
    from .gui import Gui

    Gui(scene)
