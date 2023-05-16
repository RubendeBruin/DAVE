"""Enums for nodes"""

from enum import Enum

class AreaKind(Enum):
    SPHERE = 1
    PLANE = 2
    CYLINDER = 3


class VisualOutlineType(Enum):
    NONE = 0
    FEATURE = 1
    FEATURE_AND_SILHOUETTE = 2
