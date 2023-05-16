"""These are the pure-python classes for DAVE nodes"""
from pathlib import Path

from .abstracts import *
from .enums import *
from .helpers import *

class Visual(NodePurePython):
    """
    Visual

    .. image:: ./images/visual.png

    A Visual node contains a 3d visual, typically obtained from a .obj file.
    A visual node can be placed on an axis-type node.

    It is used for visualization. It does not affect the forces, dynamics or statics.

    The visual can be given an offset, rotation and scale. These are applied in the following order

    1. scale
    2. rotate
    3. offset

    """

    def __init__(self, scene, name : str):

        super().__init__(scene, name)

        self.offset = [0, 0, 0]
        """Offset (x,y,z) of the visual. Offset is applied after scaling"""
        self.rotation = [0, 0, 0]
        """Rotation (rx,ry,rz) of the visual"""

        self.scale = [1, 1, 1]
        """Scaling of the visual. Scaling is applied before offset."""

        self.path = ""
        """Filename of the visual"""

        self.parent = None
        """Parent : Frame-type"""

        self.visual_outline = VisualOutlineType.FEATURE_AND_SILHOUETTE
        """For visualization"""

    @property
    def file_path(self) -> Path:
        """Resolved path of the visual [Path]
        #NOGUI"""
        return self._scene.get_resource_path(self.path)

    def depends_on(self):
        if self.parent is None:
            return []
        else:
            return [self.parent]

    def give_python_code(self):
        code = "# code for {}".format(self.name)

        code += "\ns.new_visual(name='{}',".format(self.name)
        if self.parent is not None:
            code += "\n            parent='{}',".format(self.parent.name)
        code += "\n            path=r'{}',".format(self.path)
        code += "\n            offset=({:.6g}, {:.6g}, {:.6g}), ".format(*self.offset)
        code += "\n            rotation=({:.6g}, {:.6g}, {:.6g}), ".format(*self.rotation)
        code += "\n            scale=({:.6g}, {:.6g}, {:.6g}) )".format(*self.scale)
        if self.visual_outline != VisualOutlineType.FEATURE_AND_SILHOUETTE:
            code += f"\ns['{self.name}'].visual_outline = {self.visual_outline}"

        return code

    @node_setter_manageable
    def change_parent_to(self, new_parent):

        from.core import Frame

        if not (isinstance(new_parent, Frame) or new_parent is None):
            raise ValueError(
                "Visuals can only be attached to an axis (or derived) or None"
            )

        # get current position and orientation
        if self.parent is not None:
            cur_position = self.parent.to_glob_position(self.offset)
            cur_rotation = self.parent.to_glob_rotation(self.rotation)
        else:
            cur_position = self.offset
            cur_rotation = self.rotation

        self.parent = new_parent

        if new_parent is None:
            self.offset = cur_position
            self.rotation = cur_rotation
        else:
            self.offset = new_parent.to_loc_position(cur_position)
            self.rotation = new_parent.to_loc_rotation(cur_rotation)

