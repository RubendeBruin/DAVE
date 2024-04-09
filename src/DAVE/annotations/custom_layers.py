# This file contains custom annotation layers for DAVE.

from DAVE import NodeSelector, Scene, Cable
from DAVE.annotations import Annotation, AnnotationLayer
from DAVE.annotations.layer import CustomNodeLayer
from DAVE.settings import DAVE_ANNOTATION_LAYERS
from DAVE.visual_helpers.scene_renderer import AbstractSceneRenderer


class NodeLabelLayer(CustomNodeLayer):
    """Annotation layer for node labels for all nodes of a certain type."""

    def provide_annotation_for_node(self, node):
        return Annotation.create_node_label_annotation(node)


class CableTensionLayer(CustomNodeLayer):
    """Annotation layer for node labels for all nodes of a certain type."""

    def __init__(
        self,
        scene: Scene,
        scene_renderer: AbstractSceneRenderer,
        selector: NodeSelector or None = None,
        tonnes=False,
    ):
        """Initializes the annotation layer."""
        super().__init__(
            scene=scene,
            scene_renderer=scene_renderer,
            selector=selector,
            do_not_update_yet=True,
        )

        self.selector.kind = (Cable,)

        if tonnes:
            self._evalme = 'f"Tension = {node.tension/9.81:.2f} t"'
        else:
            self._evalme = 'f"Tension = {node.tension:.2f} kN"'

        self.update()

    def provide_annotation_for_node(self, node):
        return Annotation.create_eval_annotation(node, self._evalme)


DAVE_ANNOTATION_LAYERS["Node labels"] = NodeLabelLayer
DAVE_ANNOTATION_LAYERS["Cable tension"] = CableTensionLayer
