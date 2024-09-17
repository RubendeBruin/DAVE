# This file contains custom annotation layers for DAVE.

from DAVE import NodeSelector, Scene, Cable, RigidBody, Tank, Measurement
from DAVE.annotations import Annotation, AnnotationLayer
from DAVE.annotations.layer import CustomNodeLayer
from DAVE.settings import DAVE_ANNOTATION_LAYERS

# from DAVE.visual_helpers.scene_renderer import AbstractSceneRenderer


class NodeLabelLayer(CustomNodeLayer):
    """Annotation layer for node labels for all nodes of a certain type."""

    def provide_annotation_for_node(self, node):
        return Annotation.create_node_label_annotation(node)


DAVE_ANNOTATION_LAYERS["Node labels"] = NodeLabelLayer

# ================================================================


class CableTensionLayer(CustomNodeLayer):
    """Annotation layer that adds the tension in kN to all Cable nodes."""

    default_selector = NodeSelector(kind=(Cable,))

    def provide_annotation_for_node(self, node):
        return Annotation.create_node_property_annotation(node, "tension")


DAVE_ANNOTATION_LAYERS["Cable tension"] = CableTensionLayer

# ================================================================


class MeasurementsLayer(CustomNodeLayer):
    """Annotation layer that adds the tension in kN to all Cable nodes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_color = (0, 50, 220)

    default_selector = NodeSelector(kind=(Measurement,))

    def provide_annotation_for_node(self, node):
        return Annotation.create_node_property_raw_annotation(node, "value_str")


DAVE_ANNOTATION_LAYERS["Measurements"] = MeasurementsLayer

# ================================================================


class WeightsLayer(CustomNodeLayer):
    """Annotation layer that adds the weight in tonnes to all Cable nodes."""

    default_selector = NodeSelector(kind=(Cable, RigidBody))

    def provide_annotation_for_node(self, node):
        annotation = Annotation.create_node_property_annotation(node, "mass")
        annotation.text_producer.hide = "node.mass == 0"  # hide if mass is zero

        if isinstance(node, RigidBody):
            annotation.anchor.position_3d = node.cog

        return annotation


DAVE_ANNOTATION_LAYERS["Weights"] = WeightsLayer

# ================================================================


class BallastLayer(CustomNodeLayer):
    """Annotation layer that adds the weight in tonnes to all Cable nodes."""

    default_selector = NodeSelector(kind=(Tank))

    def provide_annotation_for_node(self, node):
        annotation = Annotation.create_eval_annotation(
            node,
            "node.label if node.fill_pct == 0 else node.label + '<br>' + str(round(node.fill_pct)) + '%'",
        )

        if isinstance(node, RigidBody):
            annotation.anchor.position_3d = node.cog_local

        return annotation


DAVE_ANNOTATION_LAYERS["Tanks"] = BallastLayer
