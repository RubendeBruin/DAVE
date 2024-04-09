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

    def __init__(self, name, scene_renderer: AbstractSceneRenderer):
        """Initializes the annotation layer.

        Args:
            name: A string with the name of the layer.
        """
        self.annotations = []
        self.name = name

        self.font = ImageFont.truetype("arial.ttf", 16)
        
        self.scene_renderer = scene_renderer

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

        This method should be called whenever the model is updated.
        """
        for annotation in self.annotations:
            annotation.update()

        self.annotations = [annotation for annotation in self.annotations if annotation.is_valid]

        self._update_buffered_properties()

    def _update_buffered_properties(self):
        """Prepares buffered properties of the annotations such that they can be rendered.

        This method should be called after the annotations have been updated and before calling render_on
        """

        # create Overlay actors
        for annotation in self.annotations:
            if not hasattr(annotation, '_overlay_actor'):
                annotation._overlay_actor = OverlayActor()


        # Update the text of the annotations
        for a in self.annotations:
            text = getattr(a, '_text', None)
            if text == a.get_text():
                continue

            a._text = a.get_text()
            a._overlay_actor.set_text(text = a._text, font=self.font)

        # Update the position of the annotations
        for a in self.annotations:
            a._p3 = a.get_anchor_3d(self.scene_renderer)


    @property
    def is_valid(self):
        return True


    def render(self):
        """Renders the annotations on a render window.
        """

        for annotation in self.annotations:
            p3 = annotation._p3  # all private properties used here are created by _update_buffered_properties
            p2 = self.scene_renderer.to_screenspace(p3)
            offset = annotation.anchor.screenspace_offset

            annotation._overlay_actor.render_at(render_window=self.scene_renderer.window, x=p2[0] + offset[0], y=p2[1] + offset[1])



class NodeLabelLayer(AnnotationLayer):
    """Annotation layer for node labels for all nodes of a certain type.
    """

    def __init__(self, scene : Scene,
                 scene_renderer: AbstractSceneRenderer,
                 selector : NodeSelector or None = None):
        """Initializes the annotation layer.
        """
        super().__init__(scene_renderer=scene_renderer, name="Node Labels")

        if selector is None:
            selector = NodeSelector()

        self.selector = selector

        self._scene = scene

        self.update()

    def update(self):
        """Updates the layer.
        """

        # get all nodes of the specified types from scene
        nodes = self._scene.nodes(self.selector)

        annotated_nodes = [a.text_producer.node for a in self.annotations]

        # missing
        missing_nodes = set(nodes).difference(set(annotated_nodes))

        for node in missing_nodes:
            annotation = Annotation.create_node_label_annotation(node)
            self.add_annotation(annotation)

        super().update()  # removes invalid annotations
