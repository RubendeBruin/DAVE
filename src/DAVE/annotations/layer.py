import dataclasses
from abc import abstractmethod, abstractproperty

from PIL import ImageFont

from DAVE import Scene, NodeSelector, Node
from DAVE.annotations.annotation import Annotation
from DAVE.annotations.has_node_reference import HasNodeReference
from DAVE.visual_helpers.overlay_actor import OverlayActor
from DAVE.visual_helpers.scene_renderer import AbstractSceneRenderer

import nooverlap

# Get the default font
# https://en.wikipedia.org/wiki/List_of_typefaces_included_with_Microsoft_Windows


class AnnotationLayerFont:
    def __init__(self):
        self.font = ImageFont.truetype("bahnschrift.ttf", 16)

    def getbbox(self, text):
        return self.font.getbbox(text)

    def getmask(self, *args, **kwargs):
        return self.font.getmask(*args, **kwargs)

    @property
    def size(self):
        return self.font.size

    @size.setter
    def size(self, value):
        self.font = ImageFont.truetype("bahnschrift.ttf", value)


DEFAULT_ANNOTATION_FONT = AnnotationLayerFont()


"""
BaseAnnotationLayer is the base class for all annotation layers.
It is an abstract class that defines the interface for annotation layers. 

Derived classes should implement the following methods:
- annotations: a property that returns a list of annotations

post_init is called after the __init__ method and can be used to initialize additional attributes.

update is called to update the layer. It is called whenever the model is updated.

For implementation examples see:
    AnnotationLayer
    WatchesLayer

"""

class BaseAnnotationLayer(HasNodeReference):

    def __init__(self, scene, scene_renderer: AbstractSceneRenderer, *args, **kwargs):
        """Initializes the annotation layer.
        """
        self.scene_renderer = scene_renderer
        self._scene = scene

        self.font = DEFAULT_ANNOTATION_FONT
        self.background_rgba = (255, 255, 255, 200)
        self.padding = (2, 4, 2, 4)
        self.border_width = 1
        self.border_rgba = (128, 128, 128, 255)
        self.text_color = (0, 0, 0)

        self.post_init()

    def post_init(self):
        pass

    def as_dict(self):
        return {
            "annotations": [a.as_dict() for a in self.annotations],
            "font_size": self.font.size,
            "background_rgba": self.background_rgba,
            "padding": self.padding,
            "border_width": self.border_width,
            "border_rgba": self.border_rgba,
            "text_color": self.text_color,
        }

    @classmethod
    def from_dict(cls, d, scene, scene_renderer: AbstractSceneRenderer):
        layer = AnnotationLayer(scene=scene, scene_renderer=scene_renderer)
        layer.font.size = d["font_size"]
        layer.background_rgba = d["background_rgba"]
        layer.padding = d["padding"]
        layer.border_width = d["border_width"]
        layer.border_rgba = d["border_rgba"]
        layer.text_color = d["text_color"]

        for a in d["annotations"]:
            layer.add_annotation(Annotation.from_dict(a, scene))

        return layer

    @property
    @abstractmethod
    def annotations(self) -> list[Annotation]:
        pass

    @property
    def is_valid(self):
        return True

    def give_annotation_data(self) -> list[tuple[Annotation, tuple,tuple]]:
        """Returns a list of annotations that should be rendered as well as their positions
        No rendering is done here.

        Returns
        -------
        list of tuple of (Annotation, position_in_3d_space, screenspace_offset)
            A list of annotations and their positions in screen space.

        """
        to_be_rendered = []

        for annotation in self.annotations:

            # try quick
            text = getattr(annotation, "_text", annotation.get_text())
            if (
                text.strip() != ""
            ):  # only render annotation that are not empty

                # try quick
                p3 = getattr(annotation, "_p3", annotation.get_anchor_3d(self.scene_renderer))

                to_be_rendered.append(
                    (annotation, p3, annotation.anchor.screenspace_offset)
                )


        return to_be_rendered

    def _update_buffered_properties(self):
        """Prepares buffered properties of the annotations such that they can be rendered.

        This method should be called after the annotations have been updated and before calling render_on
        """

        # create Overlay actors
        for annotation in self.annotations:
            if not hasattr(annotation, "_overlay_actor"):
                annotation._overlay_actor = OverlayActor()

        # Update the text of the annotations
        for a in self.annotations:
            text = getattr(a, "_text", None)
            if text == a.get_text():
                continue

            a._text = a.get_text()

            a._overlay_actor.set_text(
                text=a._text,
                font=self.font,
                background=self.background_rgba,
                padding=self.padding,
                border=self.border_width,
                border_color=self.border_rgba,
                text_color=self.text_color,
            )

        # Update the position of the annotations
        for a in self.annotations:
            a._p3 = a.get_anchor_3d(self.scene_renderer)

    def update(self):
        """Updates the layer.

        This method should be called whenever the model is updated.
        """

        self._update_buffered_properties()

    def enforce_rerender_actors(self):
        for a in self.annotations:
            a._text = "RECREATE ME"




class AnnotationLayer(BaseAnnotationLayer):
    """A layer of annotations.

    Attributes:
        annotations: A list of annotations.

    """

    def __init__(self, scene, scene_renderer: AbstractSceneRenderer):
        super().__init__(scene, scene_renderer)
        self._annotations = []

    @property
    def annotations(self):
        return self._annotations

    @annotations.setter
    def annotations(self, value):
        self._annotations = value




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







class CustomNodeLayer(AnnotationLayer):
    default_selector = NodeSelector()

    def __init__(
        self,
        scene: Scene,
        scene_renderer: AbstractSceneRenderer,
        do_not_update_yet=False,
    ):
        """Initializes the annotation layer."""
        super().__init__(scene = scene, scene_renderer=scene_renderer)

        self.selector = dataclasses.replace(self.default_selector)  # copy

        if not do_not_update_yet:
            self.update()

    def update(self):
        """Updates the layer."""

        # get all nodes of the specified types from scene
        nodes = self._scene.nodes(self.selector)

        annotated_nodes = [a.text_producer.node for a in self.annotations]

        # missing
        missing_nodes = set(nodes).difference(set(annotated_nodes))

        for node in missing_nodes:
            annotation = self.provide_annotation_for_node(node)
            if annotation is not None:
                self.add_annotation(annotation)

        for annotation in self.annotations:
            annotation.update()

        self.annotations = [
            annotation for annotation in self.annotations if annotation.is_valid
        ]


        super().update()  # removes invalid annotations

    @abstractmethod
    def provide_annotation_for_node(self, node: Node) -> Annotation:
        pass
