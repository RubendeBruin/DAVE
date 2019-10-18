"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019



  This file defines constants and settings used throughout the package.


"""

# ======== Constants ===========

g = 9.81
rho = 1.025

# ======== Folders ===========

from os.path import expanduser
from os.path import dirname
home = expanduser("~")

RESOURCE_PATH = [home + '/models']
cdir = dirname(__file__)
RESOURCE_PATH.append(cdir + '/resources')

print('default resource folders:')
for a in RESOURCE_PATH:
    print(a)

# temporary files:

PATH_TEMP_SCREENSHOT = r'c:\data\screenshot.png'

# debugging / logging
LOGFILE = 'c:/data/vfLog.txt'


# TEXTURE_SEA = 'virtualSea'
VF_NAME_SPLIT = "-->"    # used for node-names, eg:    Body23-->Cog

# =========== Visuals ==================

# COLOR_SELECT = [1,1.0, 0]
# COLOR_VISUAL = [0.8, 0.8, 0.8]
#
# COLOR_CABLE = [0.1,0.1,0.1]
# COLOR_POI   = [0.41, 0.878, 0.8]
# COLOR_FORCE = [0.5, 1, .3]
#
# #COLOR_BG2 = [1,1,1]
# #COLOR_BG1 = [0.8,0.8,0.8]
#
# COLOR_BG2 = [0.41, 0.878, 1]
# COLOR_BG1 = [0, 0.286, 0.379]
# ALPHA_VISUAL = 0.3 # standard alpha value for visual when a node is selected
#
# OUTLINE_WIDTH = 1
#
# VISUAL_DIFFUSE = 0.4
# VISUAL_SPECULAR = 0.05
# VISUAL_AMBIENT = 0.5
#
# VISUAL_BUOYANCY_PLANE_EXTEND = 5

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

def rgb(col):
    return (col[0]/255, col[1]/255, col[2]/255)

COLOR_SELECT = rgb(_PINK)
COLOR_VISUAL = rgb(_BLUE_LIGHT)

COLOR_CABLE = rgb(_BLACK)
COLOR_POI   = rgb(_GREEN)
COLOR_FORCE = rgb(_YELLOW)
COLOR_COG = rgb(_PURPLE)
COLOR_BUOYANCY_MESH_FILL = None
COLOR_BUOYANCY_MESH_LINES = rgb(_BLUE_DARK)

COLOR_X = rgb(_RED)
COLOR_Y = rgb(_GREEN)
COLOR_Z = rgb(_BLUE)

COLOR_WATER = rgb(_BLUE_DARK)

COLOR_BG2 = rgb(_WHITE)
COLOR_BG1 = rgb(_BLUE_LIGHT)
ALPHA_VISUAL = 0.3 # standard alpha value for visual when a node is selected

OUTLINE_WIDTH = 1

VISUAL_DIFFUSE = 0.4
VISUAL_SPECULAR = 0.05
VISUAL_AMBIENT = 0.5

VISUAL_BUOYANCY_PLANE_EXTEND = 5

TEXTURE_SEA = ''
ALPHA_SEA = 0.8
ALPHA_BUOYANCY = 1.0


# ========= GUI =================


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
GUI_ANIMATION_NSTEPS = 24 # ANIMATION SPEED
GUI_ANIMATION_FPS = 24