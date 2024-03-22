from enum import Enum
from matplotlib.cm import get_cmap
import DAVE.settings as ds


class ActorType(Enum):
    FORCE = 1
    VISUAL = 2
    GEOMETRY = 3
    GLOBAL = 4
    CABLE = 5
    NOT_GLOBAL = 6
    BALLASTTANK = 7
    MESH_OR_CONNECTOR = 8
    COG = 9

# ================== visuals :: general =============

ACTOR_METALIC = 1.0
ACTOR_ROUGHESS = 0.1
ACTOR_COLOR = [0.7, 0.74, 0.74]  # a little on the cool side

# ============ visuals :: sea ===========

VISUAL_BUOYANCY_PLANE_EXTEND = 5
TEXTURE_SEA = str(ds.RESOURCE_PATH[0] / "virtualSea.jpg")
TEXTURE_WAVEPLANE = str(ds.RESOURCE_PATH[0] / "waveplane.jpg")
ALPHA_SEA = 0.8

# ============ visuals :: geometry and cables =========

RESOLUTION_SPHERE = 12
RESOLUTION_ARROW = 12
RESOLUTION_CABLE_OVER_CIRCLE = 36  # NUMBER OF POINTS IN A FULL CIRCLE
RESOLUTION_CABLE_SAG = 30  # NUMBER OF POINTS IN A CATENARY

CABLE_DIA_WHEN_DIA_IS_ZERO = 0.1  # diameter of the cable when the diameter is zero


# ============ visuals :: colors ===========

BLACK = [0, 0, 0]
RED = [144, 33, 30]
ORANGE = [200, 80, 33]
BROWN = [187, 134, 41]
GREEN = [0, 127, 14]
GREEN_DARK = [0, 110, 10]
YELLOW = [255, 216, 0]
YELLOW_DARK = [128, 108, 0]
PURPLE = [87, 0, 127]
WHITE = [255, 255, 255]
BLUE = [12, 106, 146]
BLUE_GREEN = [6, (127 + 106) / 2, (146 + 14) / 2]  # _BLUE + _GREEN / 2
BLUE_LIGHT = [203, 224, 239]
BLUE_DARK = [57, 76, 90]
PINK = [247, 17, 228]
DARK_GRAY = [45, 45, 48]
LIGHT_GRAY = [200, 200, 200]
MEDIUM_GRAY = [145, 145, 145]

PALETTE = (
    BLUE,
    ORANGE,
    GREEN,
    YELLOW_DARK,
    PURPLE,
    MEDIUM_GRAY,
    BLUE_LIGHT,
    RED,
    BROWN,
    DARK_GRAY,
    LIGHT_GRAY,
    BLUE_DARK,
)


def rgb(col):
    return col[0] / 255, col[1] / 255, col[2] / 255


COLOR_WATER_TANK_5MIN = BROWN
COLOR_WATER_TANK_SLACK = ORANGE
COLOR_WATER_TANK_95PLUS = BLUE
COLOR_WATER_TANK_FULL = BLUE_DARK
COLOR_WATER_TANK_FREEFLOODING = RED
COLOR_SELECT = rgb(YELLOW)
COLOR_SELECT_255 = YELLOW

COLOR_CIRCLE = BLUE_GREEN

OUTLINE_WIDTH = 1.5

COLOR_BG2 = rgb(WHITE)
COLOR_BG1 = rgb(WHITE)

COLOR_BG1_GUI = rgb((247, 247, 247))
COLOR_BG2_GUI = rgb((247, 247, 247))

COLOR_OUTLINE = rgb(BLACK)

COLOR_WATER = rgb(BLUE_DARK)

# ------------ colormap for unity-checks


UC_CMAP = get_cmap("turbo", lut=100)

# import matplotlib.pyplot as plt
# import math
# for i in range(1000):
#     plt.plot(i/1000,0,marker='o', color = UC_CMAP(i))
#     plt.plot(1.1, 0, marker='o', color=(1,0,1,1))
# plt.show()