"""
settings.py

This is the global configuration file.

This file defines constants and settings used throughout the package.
Among which:
- paths,
- filenames,
- environmental constants and
- colors

ALL PROGRAM WIDE VARIABLES ARE DEFINED IN UPPERCASE

"""
import tempfile
from dataclasses import dataclass, fields

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


"""


DAVE_ADDITIONAL_RUNTIME_MODULES = dict()
"""Variables in this dict will be made available to the interpreter when executing code. Useful when introducing new  
Node types via plugins.
Example
DAVE_ADDITIONAL_RUNTIME_MODULES['MyNode'] = MyNode
"""


from os.path import expanduser
from os.path import dirname
from os import mkdir
from pathlib import Path

# ======== Environment =========

BEAUFORT_SCALE = (0, 1.5, 3.4, 5.4, 7.9, 10.7, 13.8, 17.1, 20.7, 24.4, 28.4, 32.6, 999)
# BEAUFORT_SCALE[x] is the upper bound wind-speed in beaufort x
# REF: https://rules.dnv.com/docs/pdf/DNV/ST/2016-07/DNVGL-ST-0111.pdf

# ======== Frequency domain ======

# Minimum damping for frequency domain analysis, as fraction of critical damping based on diagonal terms.
FD_GLOBAL_MIN_DAMPING_FRACTION = 0.005  # 0.5% of critical damping

# ======== Folders ===========

# Default user directory
#
# By default we create a subfolder DAVE_models in the users home folder

home = Path(expanduser("~"))
default_user_dir = home / "DAVE_models"
if not default_user_dir.exists():
    mkdir(default_user_dir)


# get the package directory
cdir = Path(dirname(__file__))

# The RESOURCE PATH is the initial value for
# Scene.resources_paths
#
# By default we fill it with the build-in assets
# and a subfolder 'DAVE_models' in the user directory
RESOURCE_PATH = []
RESOURCE_PATH.append(cdir / "resources")
RESOURCE_PATH.append(default_user_dir)

# ============ ENVIRONMENT SETTINGS =========

ENVIRONMENT_PROPERTIES = (
    "g",
    "waterlevel",
    "rho_air",
    "rho_water",
    "wind_direction",
    "wind_velocity",
    "current_direction",
    "current_velocity",
)
"""A list of all environment setting properties as available in Scene"""


# ============== SOLVER ===========

# OPEN_GUI_ON_SOLVER_TIMEOUT = False  # debugging feature, set to True to open GUI on solver timeout


@dataclass
class SolverSettings:
    timeout_s: float = 30  # solver timeout in seconds, set negative for no timeout
    mobility: float = 60  # solver mobility
    tolerance: float = 1e-4  # solver tolerance

    max_newton_iterations: int = 20  # [20] solver max newton iterations, when running deterministic the local and global descent
    # steps are per newton step (with this maximum number of iterations)

    do_linear_first: bool = False  # solver linear before full solve
    tolerance_during_linear_phase: float = (
        1  # solver tolerance during linear phase (always followed by full phase)
    )

    do_local_descent: bool = True  # solver local descent
    do_newton: bool = True  # solver newton
    do_global_descent: bool = True  # solver global

    up_is_up_factor: float = -1.0  # [-1.0] solver up-is-up factor, <= 0 means disabled

    do_deterministic: bool = False  # solver deterministic
    deterministic_global_steps: int = (
        250  # [250] solver deterministic global steps per outer iteration
    )
    deterministic_local_steps: int = (
        50  # [50] solver deterministic local-descent steps per outer iteration
    )

    def non_default_props(self):
        return [f.name for f in fields(self) if getattr(self, f.name) != f.default]

    def apply(self, BS):
        """Apply the current settings on the given BackgroundSolver"""
        BS.mobility = int(self.mobility)

        BS.do_solve_linear_first = self.do_linear_first
        BS.linear_phase_tolerance = self.tolerance_during_linear_phase
        BS.tolerance = self.tolerance

        BS.do_robust = self.do_local_descent
        BS.do_local = self.do_newton
        BS.do_global = self.do_global_descent

        BS.do_deterministic = self.do_deterministic
        BS.deterministic_global_steps = self.deterministic_global_steps
        BS.deterministic_robust_steps = self.deterministic_local_steps
        BS.maxiter_for_newton = self.max_newton_iterations

        BS.up_is_up_factor = self.up_is_up_factor


# temporary files:
#

_temp_path_context = tempfile.TemporaryDirectory()
PATH_TEMP = Path(_temp_path_context.name)
print(f"Temporary files are stored in {PATH_TEMP} - will be deleted on exit")

# For report/gui use

SOLVER_TERMINATED_SCENE = None  # will be set to the scene when solver is terminated by user - this is a reference, not a copy!

DAVE_CLIPBOARD_HEADER = "#DAVESCRIPT_RUN"

"""
Node-name settings
"""

VF_NAME_SPLIT = "-->"  # used for node-names, eg:    Body23-->Cog

MANAGED_NODE_IDENTIFIER = "/"  # used for managed nodes, eg: SlingSL1242>>>eyeA


"""

Registration of properties

"""


@dataclass
class NodePropertyInfo:
    node_class: type
    property_name: str
    property_type: type
    doc_short: str
    doc_long: str
    units: str
    remarks: str
    is_settable: bool
    is_single_settable: bool
    is_single_numeric: bool

    def as_tuple(self):
        # derive class name
        class_name = None
        assert (
            self.node_class in DAVE_ADDITIONAL_RUNTIME_MODULES.values()
        ), f"{self.node_class} not found in DAVE_ADDITIONAL_RUNTIME_MODULES"
        for key, value in DAVE_ADDITIONAL_RUNTIME_MODULES.items():
            if value == self.node_class:
                class_name = key
                break

        # derive type name
        type_name = self.property_type.__name__

        return (
            class_name,
            self.property_name,
            type_name,
            self.doc_short,
            self.units,
            self.remarks,
            self.is_settable,
            self.is_single_settable,
            self.is_single_numeric,
            self.doc_long,
        )

    def header_as_tuple(self):
        return (
            "Class",
            "Property",
            "Property value type",
            "Doc (short)",
            "units",
            "remarks",
            "is_settable",
            "is_single_settable",
            "is_single_numeric",
            "Doc (long)",
        )


DAVE_NODEPROP_INFO = dict()


# Convenience function to add a prop to the register
def register_nodeprop(
    node_class: type,
    property_name: str,
    property_type: type,
    doc_short: str,
    doc_long: str,
    units: str,
    remarks: str,
    is_settable: bool,
    is_single_settable: bool,
    is_single_numeric: bool,
):
    new_type = NodePropertyInfo(
        node_class,
        property_name,
        property_type,
        doc_short,
        doc_long,
        units,
        remarks,
        is_settable,
        is_single_settable,
        is_single_numeric,
    )

    if node_class not in DAVE_NODEPROP_INFO:
        DAVE_NODEPROP_INFO[node_class] = dict()

    DAVE_NODEPROP_INFO[node_class][property_name] = new_type


# ========== BLENDER ==============

BLENDER_BASE_SCENE = RESOURCE_PATH[0] / "base ocean.blend"
BLENDER_DEFAULT_OUTFILE = PATH_TEMP / "blenderout.blend"
BLENDER_CABLE_DIA = 0.1  # m
BLENDER_BEAM_DIA = 0.5  # m
BLENDER_FPS = 30

RENDER_CURVE_RESOLUTION = 50
RENDER_CATENARY_RESOLUTION = 50
