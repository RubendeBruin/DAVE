"""Contains the settings and data-classes used by the visuals

separated from "settings" to avoid circular reference issues.
"""

from dataclasses import dataclass
from copy import copy, deepcopy

import DAVE.settings as ds

# ============ visuals :: sea ===========

VISUAL_BUOYANCY_PLANE_EXTEND = 5
TEXTURE_SEA = str(ds.RESOURCE_PATH[0] / 'virtualSea.jpg')
LIGHT_TEXTURE_SKYBOX = ds.RESOURCE_PATH[0] / 'white.png'
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
_GREEN_DARK = [0,110,10]
_YELLOW = [255,216,0]
_YELLOW_DARK = [128,108,0]
_PURPLE = [87,0,127]
_WHITE = [255,255,255]
_BLUE = [12,106,146]
_BLUE_LIGHT = [203,224,239]
_BLUE_DARK = [57,76,90]
_PINK = [247,17,228]
_DARK_GRAY = [45,45,48]
_LIGHT_GRAY = [200,200,200]
_MEDIUM_GRAY = [145,145,145]

def rgb(col):
    return (col[0]/255, col[1]/255, col[2]/255)


COLOR_WATER_TANK_5MIN = _BROWN
COLOR_WATER_TANK_SLACK = _YELLOW
COLOR_WATER_TANK_95PLUS = _BLUE_DARK
COLOR_WATER_TANK_FREEFLOODING = _RED
COLOR_SELECT = rgb(_YELLOW)

OUTLINE_WIDTH = 1

COLOR_BG2 = rgb(_LIGHT_GRAY)
COLOR_BG1 = rgb(_LIGHT_GRAY)

COLOR_WATER = rgb(_BLUE_DARK)

# -------- not used: -----
#
# COLOR_VISUAL = rgb(_BLUE_LIGHT)
#
# COLOR_CABLE = rgb(_BLACK)
# COLOR_POI   = rgb(_WHITE)
# COLOR_WAVEINTERACTION = rgb(_BLUE)
# COLOR_FORCE = rgb(_ORANGE)
# COLOR_COG = rgb(_PURPLE)
# COLOR_BEAM = rgb(_DARK_GRAY)
#
# COLOR_BUOYANCY_MESH_FILL = rgb(_YELLOW)
# COLOR_BUOYANCY_MESH_LINES = rgb(_BLUE_DARK)
#
# COLOR_CONTACT_MESH_FILL = rgb(_GREEN)
# COLOR_CONTACT_MESH_LINES = rgb(_BLUE_DARK)
#
# COLOR_TANK_MESH_FILL = None
# COLOR_TANK_MESH_LINES = rgb(_GREEN)
#
# LINEWIDTH_SUBMERGED_MESH = 3
#
# COLOR_X = rgb(_RED)
# COLOR_Y = rgb(_GREEN)
# COLOR_Z = rgb(_BLUE)
#
#
#
#

#
# COLOR_BG2_ENV = rgb(_WHITE)         # colors when global elements (waterplane) are shown
# COLOR_BG1_ENV = rgb(_BLUE_LIGHT)
#
#
# # COLOR_BG1 = rgb(_DARK_GRAY)
# # COLOR_BG2 = rgb(_DARK_GRAY)
# # _DARK_GRAY
#
# # COLOR_BG1 =rgb(_WHITE)
# ALPHA_VISUAL = 0.3 # standard alpha value for visual when a node is selected
# ALPHA_BUOYANCY = 1.0
# ALPHA_WATER_TANK = 0.9
#

#
# VISUAL_DIFFUSE = 0.4
# VISUAL_SPECULAR = 0.05
# VISUAL_AMBIENT = 0.5

# ------------

@dataclass
class ActorSettings:
    """This dataclass contains settings for an vtk actor"""

    # overall
    alpha: float = 1  # alpha of the surface - 1.0 is totally opaque and 0.0 is completely transparent.
    xray: bool = False  # only outline visible

    # surface
    surfaceShow = True
    surfaceColor: tuple = (247,17,228)  # Pink
    metallic: float = 0.4
    roughness: float = 0.9

    # lines , set lineWidth to 0 for no line
    lineWidth = 1
    lineColor = (0, 0, 0)


@dataclass
class ViewportSettings:
    """This class holds all visual settings of a viewport.

    It is a convenient way to handle all the different visual presets.

    Standard configurations are hard-coded in this class and can be activated using
    the static constructors.

    The way to change the settings of a viewport is to call "activateSettings" on viewport
    with a ViewportSettings object as argument.
    """

    show_force: bool = True  # show forces
    show_meshes: bool = True  # show meshes and connectors
    show_global: bool = False  # show or hide the environment (sea)

    # cogs
    show_cog: bool = True
    cog_do_normalize: bool = False
    cog_scale: float = 1.0

    # force
    force_do_normalize: bool = True  # Normalize force size to 1.0 for plotting
    force_scale: float = 1.6  # Scale to be applied on (normalized) force magnitude

    # geometry
    show_geometry: bool = True  # show or hide geometry objects (axis, pois, etc)
    geometry_scale: float = 1.0  # poi radius of the pois

    outline_width: float = (
        OUTLINE_WIDTH
    )  # line-width of the outlines (cell-like shading)

    painter_settings: dict = None


# ============ Painters ================

painters = dict()

surf = ActorSettings()
surf.lineWidth = 0
surf.surfaceShow = True

mesh = ActorSettings()
mesh.lineWidth = 1
mesh.surfaceShow = False
mesh.lineColor = _DARK_GRAY

trans = ActorSettings()
trans.lineWidth = 0
trans.surfaceShow = True
trans.alpha = 0.5

# ------ Point

surf.surfaceColor = _LIGHT_GRAY
painters['Point'] = {'main':copy(surf)}

# ----- Axis

painters['Axis'] = dict()

surf.surfaceColor = _RED
painters['Axis']['main'] = copy(surf)
surf.surfaceColor = _GREEN
painters['Axis']['y'] = copy(surf)
surf.surfaceColor = _BLUE
painters['Axis']['z'] = copy(surf)

# ---- body
painters['RigidBody'] = dict()

surf.surfaceColor = _RED
painters['RigidBody']['x'] = copy(surf)
surf.surfaceColor = _GREEN
painters['RigidBody']['y'] = copy(surf)
surf.surfaceColor = _BLUE
painters['RigidBody']['z'] = copy(surf)
surf.surfaceColor = _PURPLE
painters['RigidBody']['main'] = copy(surf)


# ---- circle
surf.surfaceColor = _LIGHT_GRAY
painters['Circle'] = {'main':copy(surf)}

# ---- visual
surf.surfaceColor = _MEDIUM_GRAY
painters['Visual'] = {'main':copy(surf)}

# ---- force

surf.surfaceColor = _ORANGE
painters['Force'] = {'main':copy(surf), 'moment1':copy(surf), 'moment2':copy(surf)}


# --- cable
mesh.lineWidth = 3
mesh.lineColor = _BLACK
painters['Cable'] = {'main':copy(mesh)}


# lincon2d

mesh.lineColor = _RED
painters['Connector2d'] = {'main':copy(mesh)}

# LC6D

mesh.lineColor = _RED
painters['LC6d'] = {'main':copy(mesh)}

# ----- contact mesh

cm = ActorSettings()
cm.lineWidth = 1
cm.surfaceColor = _GREEN
cm.lineColor = _GREEN_DARK
cm.surfaceShow = True

painters['ContactMesh'] = {'main':cm}

# ----- contact ball

surf.surfaceColor = _GREEN_DARK
mesh.lineColor = _ORANGE
mesh.lineWidth = 1
painters['ContactBall:free'] = {'main':copy(surf), 'contact':copy(mesh)}
mesh.lineWidth = 2
painters['ContactBall:contact'] = {'main':copy(mesh), 'contact':copy(mesh)}


# ---- buoyancy
mesh.lineColor = _BLACK
mesh.lineWidth = 1
trans.surfaceColor = _YELLOW
painters['Buoyancy'] = {'main':copy(mesh)}

surf.surfaceColor = _BLUE_DARK
painters['Buoyancy']['cob'] = copy(surf)

trans.surfaceColor = _BLUE_LIGHT
painters['Buoyancy']['waterplane'] = copy(trans)

trans.surfaceColor = _YELLOW_DARK
painters['Buoyancy']['submerged_mesh'] = copy(trans)

# ---------- Tanks
mesh.lineWidth = 1
mesh.lineColor = _BLACK
trans.surfaceColor = _RED
surf.surfaceColor = _RED

painters['Tank:freeflooding'] = {'main':copy(mesh), 'cog':copy(surf),'fluid':copy(trans)}

trans.surfaceColor = _BROWN
surf.surfaceColor = _BROWN
painters['Tank:empty'] = {'main':copy(mesh), 'cog':copy(surf),'fluid':copy(trans)}

trans.surfaceColor = _ORANGE
surf.surfaceColor = _ORANGE
painters['Tank:partial'] = {'main':copy(mesh), 'cog':copy(surf),'fluid':copy(trans)}

trans.surfaceColor = _BLUE_DARK
surf.surfaceColor = _BLUE_DARK
painters['Tank:full'] = {'main':copy(mesh), 'cog':copy(surf),'fluid':copy(trans)}




PAINTERS_DEFAULT = deepcopy(painters)