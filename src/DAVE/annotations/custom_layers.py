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
    """Annotation layer that adds the tension in kN to all Cable nodes."""

    default_selector = NodeSelector(kind=(Cable,))

    def provide_annotation_for_node(self, node):
        return Annotation.create_node_property_annotation(node, "tension")


DAVE_ANNOTATION_LAYERS["Cable tension"] = CableTensionLayer

DAVE_ANNOTATION_LAYERS["Node labels"] = NodeLabelLayer
