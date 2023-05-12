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
from dataclasses import dataclass

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


"""


DAVE_ADDITIONAL_RUNTIME_MODULES = dict()
"""Variables in this dict will be made available to the interpreter when executing code. Useful when introducing new  
Node types via plugins.
"""

QUICK_ACTION_REGISTER = []
"""Functions in this list are called by the Quick Action widget in the gui and can be used to add buttons to the
quick-action widget. 

QUICK_ACTION_REGISTER demo:

def qa_demo(scene, selection, *args):
    if any([isinstance(node, Point) for node in selection]):
        btn = QPushButton('Good point!')
        btn.setIcon(QIcon(":/icons/circle.png"))
        return [(btn,"print('Told ya')")]
    return []

QUICK_ACTION_REGISTER.append(qa_demo)
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
FD_GLOBAL_MIN_DAMPING_FRACTION = 0.005

# ======== Folders ===========

# Default user directory
#
# By default we create a subfolder DAVE_models in the users home folder

home = Path(expanduser("~"))
default_user_dir = home / 'DAVE_models'
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
RESOURCE_PATH.append(cdir / 'resources')
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

DAVE_DEFAULT_SOLVER_MOBILITY = 60
"""Mobility of the solver"""

DAVE_DEFAULT_SOLVER_TOLERANCE = 1e-4
"""Tolerance"""

DAVE_DEFAULT_SOLVER_DO_LINEAR_FIRST = True
"""Solver linear before full solve"""


# print('default resource folders:')
# for a in RESOURCE_PATH:
#     print(a)

# temporary files:
#
# Save temporary files in the default user dir

PATH_TEMP = Path(default_user_dir / 'temp')   # stored in the user dir by default
if not PATH_TEMP.exists():
    mkdir(PATH_TEMP)
PATH_TEMP_SCREENSHOT = PATH_TEMP / 'screenshot.png'


"""
Debugging/logging

By default a file "log.txt" is saved in the users temporary folder
"""
LOGFILE = PATH_TEMP / 'log.txt'

"""
Node-name settings
"""

VF_NAME_SPLIT = "-->"    # used for node-names, eg:    Body23-->Cog

MANAGED_NODE_IDENTIFIER = "/"  # used for managed nodes, eg: SlingSL1242>>>eyeA

"""
 =========== Visuals ==================
 
 This section defines color and geometry options for visualization in VTK
 
"""
 # Moved settings_visuals


"""

Registration of properties

"""

@dataclass
class NodePropertyInfo:
    node_class : type
    property_name : str
    property_type : type
    doc_short : str
    doc_long : str
    units : str
    remarks : str
    is_settable : bool
    is_single_settable : bool
    is_single_numeric : bool

    def as_tuple(self):

        # derive class name
        class_name = None
        assert self.node_class in DAVE_ADDITIONAL_RUNTIME_MODULES.values(), f'{self.node_class} not found in DAVE_ADDITIONAL_RUNTIME_MODULES'
        for key, value in DAVE_ADDITIONAL_RUNTIME_MODULES.items():
            if value==self.node_class:
                class_name = key
                break

        # derive type name
        type_name = self.property_type.__name__


        return (class_name,
                self.property_name,
                type_name,
                self.doc_short,
                self.units,
                self.remarks,
                self.is_settable,
                self.is_single_settable,
                self.is_single_numeric,
                self.doc_long)


    def header_as_tuple(self):
        return ('Class',
                'Property',
                'Property value type',
                'Doc (short)',
                'units',
                'remarks',
                'is_settable',
                'is_single_settable',
                'is_single_numeric',
                'Doc (long)')


DAVE_NODEPROP_INFO = dict()

# Convenience function to add a prop to the register
def register_nodeprop(node_class: type,
                      property_name: str,
                      property_type: type,
                      doc_short: str,
                      doc_long: str,
                      units: str,
                      remarks: str,
                      is_settable: bool,
                      is_single_settable: bool,
                      is_single_numeric: bool):

    new_type = NodePropertyInfo(node_class, property_name, property_type, doc_short, doc_long, units, remarks,
                                is_settable, is_single_settable, is_single_numeric)

    if node_class not in DAVE_NODEPROP_INFO:
        DAVE_NODEPROP_INFO[node_class] = dict()

    DAVE_NODEPROP_INFO[node_class][property_name] = new_type


# ======= Animate after solving =========

GUI_DO_ANIMATE = True
GUI_SOLVER_ANIMATION_DURATION = 0.5 # S
GUI_ANIMATION_FPS = 60

# ========== BLENDER ==============

# try to find the blender executable
BLENDER_EXEC_DEFAULT_WIN = r"C:\Program Files\Blender Foundation\Blender\blender.exe"

import platform
if platform.system().lower().startswith('win'):
    # on windows we can possibly get blender from the registry
    import winreg
    import os

    def find_blender_from_reg(where, key):
        try:
            pt = winreg.QueryValue(where, key)
            if pt:
                if '%1' in pt:
                    pt = pt[1:-6] # strip the %1

                if os.path.exists(pt):
                    return pt
                else:
                    pass
                    # print(f'Blender NOT found here {pt} as listed in {key}')
        except Exception as E:
            # print(f'Error when looking for blender here: {key} - {str(E)}')
            raise ValueError('Not found here')

    BLENDER_EXEC = None

    where_is_blender_in_the_registry = [
        (winreg.HKEY_CLASSES_ROOT, r'Applications\blender.exe\shell\open\command'),
        (winreg.HKEY_CLASSES_ROOT, r'Applications\blender-launcher.exe\shell\open\command'),
        (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Classes\Applications\blender-launcher.exe\shell\open\command'),
        (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Classes\Applications\blender-launcher.exe\shell\open\command'),
        (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Classes\blendfile\shell\open\command'),
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Classes\blendfile\shell\open\command')

    ]

    for possibility in where_is_blender_in_the_registry:
        try:
            BLENDER_EXEC = find_blender_from_reg(*possibility)
        except:
            pass

    # find it in a path
    # by default the windows-store version seems to be installed in a location which is in the path

    if BLENDER_EXEC == None:

        paths = os.environ['PATH'].split(';')
        for pth in paths:
            test = pth + r'\\blender-launcher.exe'
            if os.path.exists(test):
                BLENDER_EXEC = test
                break

    if BLENDER_EXEC:
        print("Blender found at: {}".format(BLENDER_EXEC))
    else:
        print("! Blender not found - Blender can be installed from the microsoft windows store."
              "   if you have blender already and want to be able to use blender then please either:\n"
              "   - configure windows to open .blend files with blender automatically \n"
              "   - add the folder containing blender-launcher.exe to the PATH variable.")

    # print('\nLoading DAVE...')
else: # assume we're on linux
    BLENDER_EXEC = 'blender'


BLENDER_BASE_SCENE = RESOURCE_PATH[0] / 'base ocean.blend'
BLENDER_DEFAULT_OUTFILE = PATH_TEMP / 'blenderout.blend'
BLENDER_CABLE_DIA = 0.1 # m
BLENDER_BEAM_DIA = 0.5 # m
BLENDER_FPS = 30