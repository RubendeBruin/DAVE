"""
constants.py

This is the configuration file.

This file defines constants and settings used throughout the package.
Among which:
- paths,
- filenames,
- environmental constants and
- colors

ALL PROGRAM WIDE VARIABLES ARE DEFINED IN UPPERCASE

"""



"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


"""

from os.path import expanduser
from os.path import dirname
from os import mkdir
from pathlib import Path

# ======== Constants ===========

G = 9.81
RHO = 1.025

# ======== Folders ===========
#



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

"""
 =========== Visuals ==================
 
 This section defines color and geometry options for visualization in VTK
 
"""


# ============ visuals :: sea ===========

VISUAL_BUOYANCY_PLANE_EXTEND = 5
TEXTURE_SEA = str(RESOURCE_PATH[0] / 'virtualSea.jpg')
ALPHA_SEA = 0.8

# ============ visuals :: geometry =========

RESOLUTION_SPHERE = 12
RESOLUTION_ARROW = 12

# ============ visuals :: colors ===========

_BLACK = [0,0,0]
_RED = [144,33,30]
_ORANGE = [200,80,33]
_BROWN = [187,134,41]
_GREEN = [0,127,14]
_YELLOW = [255,216,0]
_PURPLE = [87,0,127]
_WHITE = [255,255,255]
_BLUE = [12,106,146]
_BLUE_LIGHT = [203,224,239]
_BLUE_DARK = [57,76,90]
_PINK = [247,17,228]
_DARK_GRAY = [45,45,48]
_LIGHT_GRAY = [200,200,203]

def rgb(col):
    return (col[0]/255, col[1]/255, col[2]/255)

COLOR_SELECT = rgb(_YELLOW)
COLOR_VISUAL = rgb(_BLUE_LIGHT)

COLOR_CABLE = rgb(_BLACK)
COLOR_POI   = rgb(_WHITE)
COLOR_WAVEINTERACTION = rgb(_BLUE)
COLOR_FORCE = rgb(_ORANGE)
COLOR_SHEAVE = rgb(_WHITE)
COLOR_COG = rgb(_PURPLE)
COLOR_BUOYANCY_MESH_FILL = None
COLOR_BUOYANCY_MESH_LINES = rgb(_BLUE_DARK)
LINEWIDTH_SUBMERGED_MESH = 3

COLOR_X = rgb(_RED)
COLOR_Y = rgb(_GREEN)
COLOR_Z = rgb(_BLUE)

COLOR_WATER = rgb(_BLUE_DARK)

COLOR_BG2 = rgb(_LIGHT_GRAY)
COLOR_BG1 = rgb(_LIGHT_GRAY)

COLOR_BG2_ENV = rgb(_WHITE)         # colors when global elements (waterplane) are shown
COLOR_BG1_ENV = rgb(_BLUE_LIGHT)


# COLOR_BG1 = rgb(_DARK_GRAY)
# COLOR_BG2 = rgb(_DARK_GRAY)
# _DARK_GRAY

# COLOR_BG1 =rgb(_WHITE)
ALPHA_VISUAL = 0.3 # standard alpha value for visual when a node is selected
ALPHA_BUOYANCY = 1.0

OUTLINE_WIDTH = 1

VISUAL_DIFFUSE = 0.4
VISUAL_SPECULAR = 0.05
VISUAL_AMBIENT = 0.5

"""
========= GUI =================

Gui specific settings

"""


# displayed properties of nodes
PROPS_NODE = ['name']
PROPS_AXIS = ['global_position','global_rotation','applied_force','connection_force','equilibrium_error',
              'x','y','z','gz','gy','gz','rx','ry','rz','grx','gry','grz',
              'connection_force_x','connection_force_y','connection_force_z','connection_moment_x','connection_moment_y','connection_moment_z'
              ]
PROPS_POI = ['global_position','applied_force_and_moment_global','x','y','z','gz','gy','gz']
PROPS_CABLE = ['tension','stretch']
PROPS_CON2D = ['angle','moment','force']
PROPS_BODY = [*PROPS_AXIS, 'cog', 'cogx', 'cogy', 'cogz', 'mass']
PROPS_BUOY_MESH = ['cob', 'displacement']


# ======= Animate after solving =========
GUI_DO_ANIMATE = True
GUI_SOLVER_ANIMATION_DURATION = 0.5 # S
GUI_ANIMATION_FPS = 60

# ========== BLENDER ==============

BLENDER_EXEC = r"C:\Program Files\Blender Foundation\Blender\blender.exe"
BLENDER_BASE_SCENE = r"C:\data\Dave\Public\Blender visuals\base ocean.blend"
BLENDER_DEFAULT_OUTFILE = PATH_TEMP / 'blenderout.blend'
BLENDER_CABLE_DIA = 0.1 # m