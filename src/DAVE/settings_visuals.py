"""Contains the settings and data-classes used by the visuals.

Contains the pre-defined paints:

PAINTERS["paintset_name"]["NodeClass:status"] = ActorSettings


"""

from dataclasses import dataclass
from copy import copy, deepcopy
from matplotlib.cm import get_cmap
import DAVE.settings as ds

ICONS = dict()  # [class] = QIcon

PAINTERS = dict()  # this is the dictionary with sets of paint, it will be filled later

# ============ visuals :: sea ===========

VISUAL_BUOYANCY_PLANE_EXTEND = 5
TEXTURE_SEA = str(ds.RESOURCE_PATH[0] / "virtualSea.jpg")
LIGHT_TEXTURE_SKYBOX = ds.RESOURCE_PATH[0] / "white.png"
ALPHA_SEA = 0.8

# ============ visuals :: geometry =========

RESOLUTION_SPHERE = 12
RESOLUTION_ARROW = 12

# ============ visuals :: colors ===========

_BLACK = [0, 0, 0]
_RED = [144, 33, 30]
_ORANGE = [200, 80, 33]
_BROWN = [187, 134, 41]
_GREEN = [0, 127, 14]
_GREEN_DARK = [0, 110, 10]
_YELLOW = [255, 216, 0]
_YELLOW_DARK = [128, 108, 0]
_PURPLE = [87, 0, 127]
_WHITE = [255, 255, 255]
_BLUE = [12, 106, 146]
_BLUE_LIGHT = [203, 224, 239]
_BLUE_DARK = [57, 76, 90]
_PINK = [247, 17, 228]
_DARK_GRAY = [45, 45, 48]
_LIGHT_GRAY = [200, 200, 200]
_MEDIUM_GRAY = [145, 145, 145]

PALETTE = (
    _BLUE,
    _ORANGE,
    _GREEN,
    _PURPLE,
    _YELLOW_DARK,
    _MEDIUM_GRAY,
    _BLUE_LIGHT,
    _RED,
    _BROWN,
    _DARK_GRAY,
    _LIGHT_GRAY,
    _BLUE_DARK,
)


def rgb(col):
    return (col[0] / 255, col[1] / 255, col[2] / 255)


COLOR_WATER_TANK_5MIN = _BROWN
COLOR_WATER_TANK_SLACK = _ORANGE
COLOR_WATER_TANK_95PLUS = _BLUE
COLOR_WATER_TANK_FULL = _BLUE_DARK
COLOR_WATER_TANK_FREEFLOODING = _RED
COLOR_SELECT = rgb(_YELLOW)
COLOR_SELECT_255 = _YELLOW

OUTLINE_WIDTH = 1

COLOR_BG2 = rgb(_WHITE)
COLOR_BG1 = rgb(_BLUE_LIGHT)

COLOR_WATER = rgb(_BLUE_DARK)

# ------------ colormap for unity-checks

UC_CMAP = get_cmap("turbo", lut=100)

# import matplotlib.pyplot as plt
# import math
# for i in range(1000):
#     plt.plot(i/1000,0,marker='o', color = UC_CMAP(i))
#     plt.plot(1.1, 0, marker='o', color=(1,0,1,1))
# plt.show()

# ------------


@dataclass
class ActorSettings:
    """This dataclass contains settings for an vtk actor"""

    # overall
    alpha: float = 1  # alpha of the surface - 1.0 is totally opaque and 0.0 is completely transparent.
    xray: bool = False  # only outline visible

    # surface
    surfaceShow: bool = True
    surfaceColor: tuple = (247, 17, 228)  # Pink
    metallic: float = 0.4
    roughness: float = 0.9

    # lines , set lineWidth to 0 for no line
    lineWidth = 1
    lineColor = (0, 0, 0)

    # outline
    outlineColor = (0, 0, 0)

    # label
    labelShow = False


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
    cog_scale: float = 0.1

    # force
    force_do_normalize: bool = True  # Normalize force size to 1.0 for plotting
    force_scale: float = 1.6  # Scale to be applied on (normalized) force magnitude

    # geometry
    geometry_scale: float = 1.0  # poi radius of the pois and axis  - setting this scale to zero hides all geometry

    outline_width: float = (
        OUTLINE_WIDTH  # line-width of the outlines (cell-like shading)
    )

    # labels
    label_scale: float = 0.0  # scale for the labels, set 0 to turn labels off

    painter_settings: dict = None

    # Unity-checks
    paint_uc: bool = False  # use UC property for actor colors. If UC is none, then use the color defined in the painter_settings instead


# ============ Painters ================
#
#  Define some default paints
#


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

xray = ActorSettings()
xray.lineWidth = 0
xray.surfaceShow = 0
xray.xray = True

invisible = ActorSettings()
invisible.xray = False
invisible.surfaceShow = False
invisible.lineWidth = 0


# ======== Define the default palette =======
#
#   this is the "Construction" palette
#
#


painters = dict()
surf.surfaceColor = _LIGHT_GRAY
painters["Point"] = {"main": copy(surf)}
painters["Point"]["footprint"] = copy(invisible)

# ----- Frame

painters["Frame"] = dict()

surf.surfaceColor = _RED
painters["Frame"]["main"] = copy(surf)
surf.surfaceColor = _GREEN
painters["Frame"]["y"] = copy(surf)
surf.surfaceColor = _BLUE
painters["Frame"]["z"] = copy(surf)

painters["Frame"]["footprint"] = copy(invisible)

# ---- body
painters["RigidBody"] = dict()

surf.surfaceColor = _RED
painters["RigidBody"]["x"] = copy(surf)
surf.surfaceColor = _GREEN
painters["RigidBody"]["y"] = copy(surf)
surf.surfaceColor = _BLUE
painters["RigidBody"]["z"] = copy(surf)
surf.surfaceColor = _PURPLE
painters["RigidBody"]["main"] = copy(surf)
painters["RigidBody"]["footprint"] = copy(invisible)


# ---- circle
surf.surfaceColor = _LIGHT_GRAY
painters["Circle"] = {"main": copy(surf)}

# ---- visual
surf.surfaceColor = _BLUE_LIGHT
painters["Visual"] = {"main": copy(surf)}

# ---- force

surf.surfaceColor = _ORANGE
painters["Force"] = {"main": copy(surf), "moment1": copy(surf), "moment2": copy(surf)}


# --- cable
mesh.lineWidth = 3
mesh.lineColor = _BLACK
painters["Cable"] = {"main": copy(mesh)}
painters["Cable"]["main"].labelShow = True

# --- beam
mesh.lineWidth = 5
mesh.lineColor = _BLACK
painters["Beam"] = {"main": copy(mesh)}
painters["Beam"]["main"].labelShow = True

# lincon2d

mesh.lineColor = _RED
painters["Connector2d"] = {"main": copy(mesh)}

# LC6D

mesh.lineColor = _RED
painters["LC6d"] = {"main": copy(mesh)}


# SPMT

surf.surfaceColor = _LIGHT_GRAY
mesh.lineColor = _BLACK
painters["SPMT"] = {"main": copy(surf), "wheel": copy(surf), "line": copy(mesh)}


# ----- contact mesh

cm = ActorSettings()
cm.lineWidth = 1
cm.surfaceColor = _GREEN
cm.lineColor = _GREEN_DARK
cm.surfaceShow = True

painters["ContactMesh"] = {"main": cm}

# ----- contact ball

surf.surfaceColor = _GREEN_DARK
mesh.lineColor = _ORANGE
mesh.lineWidth = 1
painters["ContactBall:free"] = {"main": copy(surf), "contact": copy(mesh)}
mesh.lineWidth = 2
painters["ContactBall:contact"] = {"main": copy(mesh), "contact": copy(mesh)}


# ---- buoyancy
mesh.lineColor = _BLACK
mesh.lineWidth = 1
trans.surfaceColor = _YELLOW
painters["Buoyancy"] = {"main": copy(mesh)}

surf.surfaceColor = _BLUE_DARK
painters["Buoyancy"]["cob"] = copy(surf)

trans.surfaceColor = _BLUE_LIGHT
painters["Buoyancy"]["waterplane"] = copy(trans)

trans.surfaceColor = _YELLOW_DARK
painters["Buoyancy"]["submerged_mesh"] = copy(trans)

# ---------- Tanks
mesh.lineWidth = 1
mesh.lineColor = _BLACK
surf.surfaceColor = _RED

painters["Tank:freeflooding"] = {
    "main": copy(mesh),
    "cog": copy(surf),
    "fluid": copy(surf),
}

surf.surfaceColor = _BROWN
painters["Tank:empty"] = {"main": copy(mesh), "cog": copy(surf), "fluid": copy(surf)}

surf.surfaceColor = _ORANGE
painters["Tank:partial"] = {"main": copy(mesh), "cog": copy(surf), "fluid": copy(surf)}

surf.surfaceColor = _BLUE_DARK
painters["Tank:full"] = {"main": copy(mesh), "cog": copy(surf), "fluid": copy(surf)}

# WaveInteraction1

surf.surfaceColor = _PURPLE
painters["WaveInteraction1"] = {"main": copy(surf)}

surf.surfaceColor = _WHITE
surf.labelShow = False
painters["WindArea"] = {"main": copy(surf)}

surf.surfaceColor = _BLUE
surf.labelShow = False
painters["CurrentArea"] = {"main": copy(surf)}

painters["Component"] = deepcopy(painters["Frame"])


PAINTERS["Construction"] = deepcopy(painters)


# Define the paint for ballasting
# start with the active paints
# override only what is needed


ballast_painters = deepcopy(PAINTERS["Construction"])

# Hide points
ballast_painters["Point"]["main"] = copy(invisible)

# Hide axis
ballast_painters["Frame"]["main"] = copy(invisible)
ballast_painters["Frame"]["y"] = copy(invisible)
ballast_painters["Frame"]["z"] = copy(invisible)

# Hide rigidbody
ballast_painters["RigidBody"]["main"] = copy(invisible)
ballast_painters["RigidBody"]["x"] = copy(invisible)
ballast_painters["RigidBody"]["y"] = copy(invisible)
ballast_painters["RigidBody"]["z"] = copy(invisible)

# Hide wind and current areas
ballast_painters["WindArea"]["main"] = copy(invisible)
ballast_painters["CurrentArea"]["main"] = copy(invisible)

# SPMTS: Xray
ballast_painters["SPMT"]["main"] = copy(xray)
ballast_painters["SPMT"]["wheels"] = copy(xray)
ballast_painters["SPMT"]["line"] = copy(invisible)


# Hide circle
ballast_painters["Circle"]["main"] = copy(invisible)

# Visuals: Xray
ballast_painters["Visual"]["main"] = copy(xray)
ballast_painters["Visual"]["main"].outlineColor = _MEDIUM_GRAY

# Forces: unchanged

# Cables: thin gray lines
ballast_painters["Cable"]["main"].lineWidth = 1
ballast_painters["Cable"]["main"].lineColor = _MEDIUM_GRAY

#
ballast_painters["Connector2d"]["main"] = copy(invisible)
ballast_painters["ContactMesh"]["main"] = copy(invisible)

ballast_painters["ContactBall:free"]["main"] = copy(invisible)
ballast_painters["ContactBall:free"]["contact"] = copy(invisible)

ballast_painters["ContactBall:contact"]["main"] = copy(invisible)
ballast_painters["ContactBall:contact"]["contact"] = copy(invisible)

ballast_painters["WaveInteraction1"]["main"] = copy(invisible)

# Hide all labels
# disable all other labels
ballast_painters = deepcopy(ballast_painters)
for outer_key, visual in ballast_painters.items():
    for inner_key in visual.keys():
        ballast_painters[outer_key][inner_key].labelShow = False

# --- Buoyancy mesh
visual = dict()
paint = ActorSettings()
paint.alpha = 1
paint.xray = False
paint.surfaceShow = False
paint.surfaceColor = (247, 17, 228)
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0.0
paint.lineColor = [0, 0, 0]
visual["main"] = paint
paint = ActorSettings()
paint.alpha = 1
paint.xray = False
paint.surfaceShow = False
paint.surfaceColor = [57, 76, 90]
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0
visual["cob"] = paint
paint = ActorSettings()
paint.alpha = 0.3
paint.xray = False
paint.surfaceShow = True
paint.surfaceColor = [203, 224, 239]
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0
visual["waterplane"] = paint
paint = ActorSettings()
paint.alpha = 0.25
paint.xray = False
paint.surfaceShow = True
paint.surfaceColor = [128, 108, 0]
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0
visual["submerged_mesh"] = paint
ballast_painters["Buoyancy"] = visual

# --- Tanks
visual = dict()
paint = ActorSettings()
paint.alpha = 0.2
paint.xray = False
paint.surfaceShow = True
paint.surfaceColor = (255, 0, 127)
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0.0
paint.lineColor = [0, 0, 0]
paint.labelShow = True
visual["main"] = paint
paint = ActorSettings()
paint.alpha = 1
paint.xray = False
paint.surfaceShow = True
paint.surfaceColor = [144, 33, 30]
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0
visual["cog"] = paint
paint = ActorSettings()
paint.alpha = 1
paint.xray = False
paint.surfaceShow = True
paint.surfaceColor = [144, 33, 30]
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0
visual["fluid"] = paint
ballast_painters["Tank:freeflooding"] = visual

# ========= (Almost) Empty ========
visual = dict()
paint = ActorSettings()
paint.alpha = 0.5
paint.xray = True
paint.surfaceShow = True
paint.surfaceColor = (255, 255, 255)
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0
paint.lineColor = [0, 0, 0]
paint.labelShow = True

visual["main"] = paint

paint = ActorSettings()
paint.alpha = 1
paint.xray = False
paint.surfaceShow = True
paint.surfaceColor = [187, 134, 41]
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0
visual["cog"] = paint

paint = ActorSettings()
paint.alpha = 1
paint.xray = False
paint.surfaceShow = True
paint.surfaceColor = [187, 134, 41]
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0
visual["fluid"] = paint
ballast_painters["Tank:empty"] = visual  # empty is also almost empty

# --- paint for : {value} ---
visual = dict()
paint = ActorSettings()
paint.alpha = 1
paint.xray = True
paint.surfaceShow = False
paint.surfaceColor = (247, 17, 228)
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0.0
paint.lineColor = [0, 0, 0]
paint.labelShow = True
visual["main"] = paint
paint = ActorSettings()
paint.alpha = 1
paint.xray = False
paint.surfaceShow = False
paint.surfaceColor = [200, 80, 33]
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0
visual["cog"] = paint
paint = ActorSettings()
paint.alpha = 1
paint.xray = False
paint.surfaceShow = True
paint.surfaceColor = [200, 80, 33]
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0
visual["fluid"] = paint
ballast_painters["Tank:partial"] = visual

# --- paint for : {value} ---
visual = dict()
paint = ActorSettings()
paint.alpha = 1
paint.xray = True
paint.surfaceShow = False
paint.surfaceColor = (247, 17, 228)
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0.0
paint.lineColor = [0, 0, 0]
paint.labelShow = True
visual["main"] = paint
paint = ActorSettings()
paint.alpha = 1
paint.xray = False
paint.surfaceShow = False
paint.surfaceColor = [57, 76, 90]
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0
visual["cog"] = paint
paint = ActorSettings()
paint.alpha = 1
paint.xray = False
paint.surfaceShow = True
paint.surfaceColor = [57, 76, 90]
paint.metallic = 0.4
paint.roughness = 0.9
paint.lineWidth = 0

visual["fluid"] = paint
ballast_painters["Tank:full"] = visual


PAINTERS["Ballast"] = deepcopy(ballast_painters)

# Make Visual and physical only palette

# set all invisible
animation_painters = deepcopy(PAINTERS["Construction"])
for outer_key, visual in animation_painters.items():
    for inner_key in visual.keys():
        animation_painters[outer_key][inner_key] = copy(invisible)

surf.surfaceColor = _LIGHT_GRAY
animation_painters["Visual"]["main"] = copy(surf)
animation_painters["Cable"] = copy(PAINTERS["Construction"]["Cable"])
animation_painters["Beam"] = copy(PAINTERS["Construction"]["Beam"])
animation_painters["SPMT"] = copy(PAINTERS["Construction"]["SPMT"])

PAINTERS["Visual"] = animation_painters

# Rigging
PAINTERS["Rigging"] = deepcopy(animation_painters)
PAINTERS["Rigging"]["Circle"] = deepcopy(PAINTERS["Construction"]["Circle"])


# Xray
PAINTERS["X-ray"] = deepcopy(PAINTERS["Construction"])
PAINTERS["X-ray"]["Visual"]["main"].surfaceShow = False
PAINTERS["X-ray"]["Visual"]["main"].xray = True
PAINTERS["X-ray"]["SPMT"]["main"].xray = True
PAINTERS["X-ray"]["SPMT"]["main"].surfaceShow = False
PAINTERS["X-ray"]["SPMT"]["wheel"].xray = True
PAINTERS["X-ray"]["SPMT"]["wheel"].surfaceShow = False
PAINTERS["X-ray"]["SPMT"]["line"] = copy(invisible)

# No-mesh settings
#
# These are just the regular-paints but then with all line-widths set to 0


def remove_mesh(paintset):
    nodes = (
        "ContactMesh",
        "Buoyancy",
        "Tank:freeflooding",
        "Tank:empty",
        "Tank:partial",
        "Tank:full",
    )
    for node in nodes:
        for paint in paintset[node].values():
            paint.lineWidth = 0

    paintset["Buoyancy"]["waterplane"] = copy(invisible)


construction_nomesh = deepcopy(PAINTERS["Construction"])
remove_mesh(construction_nomesh)
# for value1 in construction_nomesh.values():
#     for value2 in value1.values():
#         value2.lineWidth = 0
PAINTERS["Construction, no mesh"] = construction_nomesh

xray_nomesh = deepcopy(PAINTERS["X-ray"])
remove_mesh(xray_nomesh)
PAINTERS["X-ray, no mesh"] = xray_nomesh

# Bendingmoment / footprints
foot_painters = deepcopy(PAINTERS["X-ray, no mesh"])

footprint_paint = copy(surf)
footprint_paint.lineWidth = 3
footprint_paint.lineColor = _PURPLE
footprint_paint.surfaceColor = _PURPLE

foot_painters["Point"]["footprint"] = copy(footprint_paint)
foot_painters["Frame"]["footprint"] = copy(footprint_paint)
foot_painters["RigidBody"]["footprint"] = copy(footprint_paint)

foot_painters["WindArea"] = {"main": copy(invisible)}
foot_painters["CurrentArea"] = {"main": copy(invisible)}

PAINTERS["Footprints"] = foot_painters

def AddPaintForNodeClassAsCopyOfOtherClass(node_class: str, other_class: str):
    for P in PAINTERS.values():
        P[node_class] = deepcopy(P[other_class])



if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.plot()

    for i,COL in enumerate(PALETTE):
        c = [r/255 for r in COL]
        plt.plot((0,10),(i,0), color = c, lw=10)

    plt.show()
