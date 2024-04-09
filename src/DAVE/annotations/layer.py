from PIL import ImageFont

from DAVE import Scene, NodeSelector
from DAVE.annotations.annotation import Annotation
from DAVE.annotations.has_node_reference import HasNodeReference
from DAVE.visual_helpers.overlay_actor import OverlayActor
from DAVE.visual_helpers.scene_renderer import AbstractSceneRenderer


class AnnotationLayer(HasNodeReference):
    """A layer of annotations.

    Attributes:
        annotations: A list of annotations.
        name: A string with the name of the layer.
    """

    def __init__(self, name):
        """Initializes the annotation layer.

        Args:
            name: A string with the name of the layer.
        """
        self.annotations = []
        self.name = name

        self.font = ImageFont.truetype("arial.ttf", 16)

    def add_annotation(self, annotation):
        """Adds an annotation to the layer.

        Args:
            annotation: An Annotation object.
        """
        self.annotations.append(annotation)

    def remove_annotation(self, annotation):
        """Removes an annotation from the layer.

        Args:
            annotation: An Annotation object.
        """
        self.annotations.remove(annotation)

    def update(self):
        """Updates the layer.

        This method should be called whenever the visual is updated.
        """
        for annotation in self.annotations:
            annotation.update()

        self.annotations = [annotation for annotation in self.annotations if annotation.is_valid]

    @property
    def is_valid(self):
        return True

    def render_on(self, viewport : AbstractSceneRenderer):
        """Renders the annotations on a render window.

        Args:
            render_window: A vtkRenderWindow object.
        """

        # create overlay actors
        for annotation in self.annotations:
            actor = OverlayActor()
            actor.set_text(text = annotation.get_text(), font=self.font)

            anchor = annotation.get_anchor(viewport)
            actor.render_at(render_window=viewport.window, x=anchor[0], y=anchor[1])



class NodeLabelLayer(AnnotationLayer):
    """Annotation layer for node labels for all nodes of a certain type.
    """

    def __init__(self, scene : Scene, selector : NodeSelector or None = None):
        """Initializes the annotation layer.
        """
        super().__init__("Labels")

        if selector is None:
            selector = NodeSelector()

        self.selector = selector

        self._scene = scene

        self.update()

    def update(self):
        """Updates the layer.
        """

        super().update()  # removes invalid annotations

        # get all nodes of the specified types from scene
        nodes = self._scene.nodes(self.selector)

        annotated_nodes = [a.text_producer.node for a in self.annotations]

        # missing
        missing_nodes = set(nodes).difference(set(annotated_nodes))

        for node in missing_nodes:
            annotation = Annotation.create_node_label_annotation(node)
            self.add_annotation(annotation)

