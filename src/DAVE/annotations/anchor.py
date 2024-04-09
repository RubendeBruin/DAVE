from vtkmodules.vtkRenderingCore import vtkCoordinate

from .has_node_reference import HasNodeReference

from DAVE import Node
from ..visual_helpers.actors import VisualActor
from ..visual_helpers.scene_renderer import AbstractSceneRenderer


class Anchor(HasNodeReference):

    def __init__(self, node : Node or None):

        self.node : Node or None = node

        """1D position of the anchor (f), passed to node-visual"""
        self.position_1f : float or None = None

        """3D position of the anchor (x, y, z), passed to node-visual"""
        self.position_3d : tuple[float,float,float] = (0.0, 0.0, 0.0)

        """Screen space 2d offset of the anchor (x, y), applied to the node-visual position after projection to screen space"""
        self.screenspace_offset : tuple[float, float] = (0.0, 0.0)

        self._visual : VisualActor or None = None # buffered visual



    def update(self):
        pass

    @property
    def is_valid(self):
        if self.node is None:
            return True

        return self.node.is_valid

    def get_anchor_3d(self, viewport) -> tuple[float, float, float]:
        """Gets the 3d anchor position in world coordinates"""
        # try to get the visual from the node
        if self.node is not None:
            self._visual = viewport.actor_from_node(self.node, guess=self._visual)
        else:
            self._visual = None

        if self._visual is None:
            return self.position_3d

        return self._visual.get_annotation_position(self.position_3d, self.position_1f)




