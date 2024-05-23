"""Contains the settings and data-classes used by the visuals.

Contains the pre-defined paints:

PAINTERS["paintset_name"]["NodeClass:status"] = ActorSettings


"""

from dataclasses import dataclass
from copy import copy, deepcopy

from DAVE.visual_helpers.constants import *


ICONS = dict()  # [class] = QIcon
PAINTERS = dict()  # this is the dictionary with sets of paint, it will be filled later



@dataclass
class ActorSettings:
    """This dataclass contains settings for an vtk actor"""

    # overall
    alpha: float = 1  # alpha of the surface - 1.0 is totally opaque and 0.0 is completely transparent.
    xray: bool = False  # only outline visible

    # surface
    surfaceShow: bool = True
    surfaceColor: tuple = (247, 17, 228)  # Pink
    metallic: float = 0.5
    roughness: float = 0.5

    # lines , set lineWidth to 0 for no line
    lineWidth = 1
    lineColor = (0, 0, 0)

    # outline
    outlineColor = (0, 0, 0)

    # label
    labelShow = True

    # "scale" property
    #  interpreted as follows:
    #   Cables : minimum diameter
    #
    # triggers re-creation of actors when changed
    optionalScale = 0

    def set_invisible(self):
        self.surfaceShow = False
        self.lineWidth = 0
        self.labelShow = False


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
    show_sea: bool = False  # show or hide the sea
    show_origin: bool = True  # show or hide the origin

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
    label_property: str or None = "name"  # property to use for labels; by default Name
    label_scale: float = 0  # scale for the labels, set 0 to turn labels off

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
mesh.lineColor = DARK_GRAY

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


def make_node_invisible(node):
    for key, value in node.items():
        value.set_invisible()


# ======== Define the default palette =======
#
#   this is the "Construction" palette
#
#


painters = dict()
surf.surfaceColor = LIGHT_GRAY
painters["Point"] = {"main": copy(surf)}
painters["Point"]["footprint"] = copy(invisible)

# ----- Frame

painters["Frame"] = dict()

surf.surfaceColor = RED
painters["Frame"]["main"] = copy(surf)
surf.surfaceColor = GREEN
painters["Frame"]["y"] = copy(surf)
surf.surfaceColor = BLUE
painters["Frame"]["z"] = copy(surf)

painters["Frame"]["footprint"] = copy(invisible)

# ---- body
painters["RigidBody"] = dict()

surf.surfaceColor = RED
painters["RigidBody"]["x"] = copy(surf)
surf.surfaceColor = GREEN
painters["RigidBody"]["y"] = copy(surf)
surf.surfaceColor = BLUE
painters["RigidBody"]["z"] = copy(surf)
surf.surfaceColor = PURPLE
painters["RigidBody"]["main"] = copy(surf)
painters["RigidBody"]["footprint"] = copy(invisible)


# ---- circle
surf.surfaceColor = COLOR_CIRCLE
painters["Circle"] = {"main": copy(surf)}

# ---- visual
surf.surfaceColor = BLUE_LIGHT
painters["Visual"] = {"main": copy(surf)}

# ---- force

surf.surfaceColor = ORANGE
painters["Force"] = {"main": copy(surf), "moment1": copy(surf), "moment2": copy(surf)}


# --- cable
# mesh.lineWidth = 3
# mesh.lineColor = BLACK
surf.surfaceColor = BLACK
painters["Cable"] = {"main": copy(surf)}
painters["Cable"]["main"].labelShow = False

# --- beam
mesh.lineWidth = 5
mesh.lineColor = BLACK
painters["Beam"] = {"main": copy(mesh)}
painters["Beam"]["main"].labelShow = False

# lincon2d

mesh.lineColor = RED
painters["Connector2d"] = {"main": copy(mesh)}

# LC6D

mesh.lineColor = RED
painters["LC6d"] = {"main": copy(mesh)}


# SPMT

surf.surfaceColor = LIGHT_GRAY
mesh.lineColor = BLACK
painters["SPMT"] = {"main": copy(surf), "wheel": copy(surf), "line": copy(mesh)}


# ----- contact mesh

cm = ActorSettings()
cm.lineWidth = 1
cm.surfaceColor = GREEN
cm.lineColor = GREEN_DARK
cm.surfaceShow = True

painters["ContactMesh"] = {"main": cm}

# ----- contact ball

surf.surfaceColor = GREEN_DARK
mesh.lineColor = ORANGE
mesh.lineWidth = 1
painters["ContactBall:free"] = {"main": copy(surf), "contact": copy(mesh)}
mesh.lineWidth = 2
painters["ContactBall:contact"] = {"main": copy(mesh), "contact": copy(mesh)}


# ---- buoyancy
mesh.lineColor = BLACK
mesh.lineWidth = 1
trans.surfaceColor = YELLOW
painters["Buoyancy"] = {"main": copy(mesh)}

surf.surfaceColor = BLUE_DARK
painters["Buoyancy"]["cob"] = copy(surf)

trans.surfaceColor = BLUE_LIGHT
painters["Buoyancy"]["waterplane"] = copy(trans)

trans.surfaceColor = YELLOW_DARK
painters["Buoyancy"]["submerged_mesh"] = copy(trans)

# ---------- Tanks
mesh.lineWidth = 1
mesh.lineColor = BLACK
surf.surfaceColor = RED

painters["Tank:freeflooding"] = {
    "main": copy(mesh),
    "cog": copy(surf),
    "fluid": copy(surf),
}

surf.surfaceColor = BROWN
painters["Tank:empty"] = {"main": copy(mesh), "cog": copy(surf), "fluid": copy(surf)}

surf.surfaceColor = ORANGE
painters["Tank:partial"] = {"main": copy(mesh), "cog": copy(surf), "fluid": copy(surf)}

surf.surfaceColor = BLUE_DARK
painters["Tank:full"] = {"main": copy(mesh), "cog": copy(surf), "fluid": copy(surf)}

# WaveInteraction1

surf.surfaceColor = PURPLE
painters["WaveInteraction1"] = {"main": copy(surf)}

surf.surfaceColor = WHITE
surf.labelShow = False
painters["WindArea"] = {"main": copy(surf)}

surf.surfaceColor = BLUE
surf.labelShow = False
painters["CurrentArea"] = {"main": copy(surf)}

painters["Component"] = deepcopy(painters["Frame"])


PAINTERS["Construction"] = deepcopy(painters)

# Construction - no areas

construction_no_areas = deepcopy(PAINTERS["Construction"])
make_node_invisible(construction_no_areas["WindArea"])
make_node_invisible(construction_no_areas["CurrentArea"])
PAINTERS["Construction, no areas"] = construction_no_areas



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
ballast_painters["Visual"]["main"].outlineColor = MEDIUM_GRAY

# Forces: unchanged

# Cables: thin gray lines
ballast_painters["Cable"]["main"].lineWidth = 1
ballast_painters["Cable"]["main"].lineColor = MEDIUM_GRAY

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

surf.surfaceColor = LIGHT_GRAY
animation_painters["Visual"]["main"] = copy(surf)
animation_painters["Cable"] = copy(PAINTERS["Construction"]["Cable"])
animation_painters["Beam"] = copy(PAINTERS["Construction"]["Beam"])
animation_painters["SPMT"] = copy(PAINTERS["Construction"]["SPMT"])

PAINTERS["Visual"] = animation_painters


# Xray
PAINTERS["X-ray"] = deepcopy(PAINTERS["Construction"])
PAINTERS["X-ray"]["Visual"]["main"].surfaceShow = False
PAINTERS["X-ray"]["Visual"]["main"].xray = True
PAINTERS["X-ray"]["SPMT"]["main"].xray = True
PAINTERS["X-ray"]["SPMT"]["main"].surfaceShow = False
PAINTERS["X-ray"]["SPMT"]["wheel"].xray = True
PAINTERS["X-ray"]["SPMT"]["wheel"].surfaceShow = False
PAINTERS["X-ray"]["SPMT"]["line"] = copy(invisible)

# Mooring
PAINTERS["Mooring"] = deepcopy(PAINTERS["Visual"])

pm = PAINTERS["Mooring"]  # alias

pm["Point"]["main"].surfaceColor = GREEN_DARK

make_node_invisible(pm["Buoyancy"])
make_node_invisible(pm["Tank:freeflooding"])
make_node_invisible(pm["Tank:empty"])
make_node_invisible(pm["Tank:partial"])
make_node_invisible(pm["Tank:full"])
pm["Frame"]["footprint"] = copy(invisible)
pm["Cable"]["main"].optionalScale = 0.3


# make points visible
# make circles visible
# make fenders visible
# make contact meshes visible
make_visible = (
    "Point",
    "Beam",
    "ContactMesh",
    "ContactBall:free",
    "ContactBall:contact",
    "Circle",
)

for node in make_visible:
    pm[node] = deepcopy(PAINTERS["Construction"][node])

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
footprint_paint.lineColor = PURPLE
footprint_paint.surfaceColor = PURPLE

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

    for i, COL in enumerate(PALETTE):
        c = [r / 255 for r in COL]
        plt.plot((0, 10), (i, 0), color=c, lw=10)

    plt.show()
