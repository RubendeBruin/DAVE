# This file contains custom annotation layers for DAVE.
from DAVE import NodeSelector, Scene, Cable, RigidBody, Tank, Measurement
from DAVE.annotations import Annotation, AnnotationLayer
from DAVE.annotations.layer import CustomNodeLayer, BaseAnnotationLayer
from DAVE.settings import DAVE_ANNOTATION_LAYERS
from DAVE.visual_helpers.constants import YELLOW, ERROR_COLOR_BACKGROUND


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
    """Annotation layer that adds the weight in tonnes to all Cable nodes and rigid body."""

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


# ================================================================

class WatchesLayer(BaseAnnotationLayer):
    """Annotation layer that renders the watches on nodes. Watches are grouped in a single annotation if a node has more than one watch."""

    def post_init(self):
        self._annotations = []
        self._formatter = '{prop}: {value:.3f} {unit}<br>'

    def update(self):
        """Updates the layer."""
        self._update_annotations()
        super().update()


    def _update_annotations(self):
        """Updates the layer."""

        self._annotations = []

        nodes, props, values, docs = self._scene.evaluate_watches()

        texts = dict()

        for node, prop, value, doc in zip(nodes, props, values, docs):
            if node not in texts:
                texts[node] = ''
            try:
                text = self._formatter.format(prop=prop, value=value, unit=doc.units)
            except:
                text = f'{prop}: {value} {doc.units}<br>'
            texts[node] += text

        for node, text in texts.items():
            annotation = Annotation.create_node_text_annotation(node, text)
            self._annotations.append(annotation)



    @property
    def annotations(self) -> list[Annotation]:
        return self._annotations

DAVE_ANNOTATION_LAYERS["Watches"] = WatchesLayer

# ============ Warnings layer =============

class WarningsLayer(BaseAnnotationLayer):
    """Annotation layer that renders the warnings on nodes. Warnings are grouped in a single annotation if a node has more than one warning."""

    def post_init(self):
        self._annotations = []



    def update(self):
        """Updates the layer."""

        self.background_rgba = (*YELLOW,)  # override
        self._update_annotations()
        super().update()

    def _update_annotations(self):
        """Updates the layer."""

        self._annotations = []

        warns = self._scene.warnings      # list[tuple[Node, str]]:
        texts = dict()

        for node, txt in warns:
            if node not in texts:
                texts[node] = 'WARNING:<br>'
            texts[node] += txt + '<br>'

        for node, text in texts.items():
            annotation = Annotation.create_node_text_annotation(node, text)
            self._annotations.append(annotation)

    @property
    def annotations(self) -> list[Annotation]:
        return self._annotations

DAVE_ANNOTATION_LAYERS["Warnings"] = WarningsLayer

# ============= Errors layer =============


class ErrorsLayer(BaseAnnotationLayer):
    """Annotation layer that renders the warnings on nodes. Warnings are grouped in a single annotation if a node has more than one warning."""

    def post_init(self):
        self._annotations = []


    def update(self):
        """Updates the layer."""

        self.background_rgba = (*ERROR_COLOR_BACKGROUND,)  # override
        self._update_annotations()
        super().update()

    def _update_annotations(self):
        """Updates the layer."""

        self._annotations = []

        errors = self._scene.node_errors  #  list[tuple[Node, str]]:

        texts = dict()

        for node, txt in errors:
            if node not in texts:
                texts[node] = 'ERROR:<br>'
            texts[node] += txt + '<br>'

        for node, text in texts.items():
            annotation = Annotation.create_node_text_annotation(node, text)
            self._annotations.append(annotation)

    @property
    def annotations(self) -> list[Annotation]:
        return self._annotations

DAVE_ANNOTATION_LAYERS["Errors"] = ErrorsLayer