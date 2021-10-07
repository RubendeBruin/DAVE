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
from copy import deepcopy, copy

import pandas as pd

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

# get the current working directory
workdir = Path().absolute()

# The RESOURCE PATH is the initial value for
# Scene.resources_paths
#
# By default we fill it with the build-in assets
# and a subfolder 'DAVE_models' in the user directory
RESOURCE_PATH = []
RESOURCE_PATH.append(cdir / 'resources')
RESOURCE_PATH.append(default_user_dir)
RESOURCE_PATH.append(workdir)

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



print('default resource folders:')
for a in RESOURCE_PATH:
    print(a)

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

MANAGED_NODE_IDENTIFIER = ">>>"  # used for managed nodes, eg: SlingSL1242>>>eyeA

"""
 =========== Visuals ==================
 
 This section defines color and geometry options for visualization in VTK
 
"""



"""
========= GUI =================

Gui specific settings

"""

#
# # displayed properties of nodes
#
# Obsolete, now read from the .csv that is also used for the documentation
#
# PROPS_NODE = ['name']
# PROPS_FRAME = ['global_position','global_rotation','applied_force','connection_force','equilibrium_error',
#               'x','y','z','gz','gy','gz','rx','ry','rz','grx','gry','grz','ux','uy','uz',
#               'connection_force_x','connection_force_y','connection_force_z','connection_moment_x','connection_moment_y','connection_moment_z',
#               'tilt_x','heel','tilt_y','trim','heading','heading_compass']
# PROPS_POI = ['global_position','applied_force_and_moment_global','x','y','z','gx','gy','gz',
#              'applied_force','fx','fy','fz',
#              'applied_moment','mx','my','mz',]
# PROPS_CABLE = ['tension','stretch','length']
# PROPS_FORCE = ['force','fx','fy','fz','moment','mx','my','mz']
# PROPS_CON2D = ['angle','moment','force','ax','ay','az']
# PROPS_CON6D = ['force_global','fgx','fgy','fgz','moment_global','mgx','mgy','mgz']
# PROPS_BODY = ['cog', 'cogx', 'cogy', 'cogz', 'mass']
# PROPS_BUOY_MESH = ['cob', 'displacement', 'cob_local']
# PROPS_BEAM = ['tension', 'torsion', 'L', 'EIy', 'EIz', 'EA', 'GIp', 'n_segments']
# PROPS_CONTACTBALL = ['can_contact','contactpoint','contact_force_magnitude','contact_force']
# PROPS__AREA = ['A','Cd', 'Ae','fx','fy','fz','force']


cdir = Path(dirname(__file__))
DAVE_REPORT_PROPS = pd.read_csv(cdir / './resources/proplist.csv')

classes = set(DAVE_REPORT_PROPS['class'].tolist())

PROPS = dict()
PROPS_GUI = dict()
for c in classes:
    props_for_class = DAVE_REPORT_PROPS[DAVE_REPORT_PROPS['class'] == c]
    all_properties = props_for_class['property'].tolist()
    PROPS[c] =  all_properties
    docs = props_for_class['doc'].tolist()

    guiprops = []
    for (prop, doc) in zip(all_properties, docs):
        if '#NOGUI' not in doc:
            guiprops.append(prop)
        else:
            print(f'Skipping {doc}')

    PROPS_GUI[c] = guiprops



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
    pt = ''

    try:
        pt = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, r'Applications\blender.exe\shell\open\command')
    except:
        try:
            pt = winreg.QueryValue(winreg.HKEY_CURRENT_USER,r'SOFTWARE\Classes\blendfile\shell\open\command')
        except:
            try:
                pt = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Classes\blendfile\shell\open\command')
            except:
                pass
    if pt:
        BLENDER_EXEC = pt[1:-6]
    else:
        BLENDER_EXEC = BLENDER_EXEC_DEFAULT_WIN

    from os import path
    if path.exists(BLENDER_EXEC):
        print("Blender found at: {}".format(BLENDER_EXEC))
    else:
        print("! Blender not found - if you want to be able to use blender then please either:\n"
              "   edit BLENDER_EXEC_DEFAULT_WIN in settings.py or \n"
              "   set settings.BLENDER_EXEC or\n"
              "   configure windows to open .blend files with blender automatically")

        print('\nLoading DAVE...')
else: # assume we're on linux
    BLENDER_EXEC = 'blender'


BLENDER_BASE_SCENE = RESOURCE_PATH[0] / 'base ocean.blend'
BLENDER_DEFAULT_OUTFILE = PATH_TEMP / 'blenderout.blend'
BLENDER_CABLE_DIA = 0.1 # m
BLENDER_BEAM_DIA = 0.5 # m
BLENDER_FPS = 30