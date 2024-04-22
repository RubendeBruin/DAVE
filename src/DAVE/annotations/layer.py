import dataclasses
from abc import abstractmethod

from PIL import ImageFont

from DAVE import Scene, NodeSelector, Node
from DAVE.annotations.annotation import Annotation
from DAVE.annotations.has_node_reference import HasNodeReference
from DAVE.visual_helpers.overlay_actor import OverlayActor
from DAVE.visual_helpers.scene_renderer import AbstractSceneRenderer


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
        self.scene_renderer = scene_renderer

        self.annotations = []
        self.name = name

        self.font = DEFAULT_ANNOTATION_FONT
        self.background_rgba = (255, 255, 255, 200)
        self.padding = (2, 4, 2, 4)
        self.border_width = 1
        self.border_rgba = (128, 128, 128, 255)

    def as_dict(self):
        return {
            "name": self.name,
            "annotations": [a.as_dict() for a in self.annotations],
            "font_file": self.font.path,
            "font_size": self.font.size,
            "background_rgba": self.background_rgba,
            "padding": self.padding,
            "border_width": self.border_width,
            "border_rgba": self.border_rgba,
        }

    @classmethod
    def from_dict(cls, d, scene, scene_renderer: AbstractSceneRenderer):
        layer = AnnotationLayer(d["name"], scene_renderer)
        layer.font = ImageFont.truetype(d["font_file"], d["font_size"])
        layer.background_rgba = d["background_rgba"]
        layer.padding = d["padding"]
        layer.border_width = d["border_width"]
        layer.border_rgba = d["border_rgba"]

        for a in d["annotations"]:
            layer.add_annotation(Annotation.from_dict(a, scene))

        return layer

    def enforce_rerender_actors(self):
        for a in self.annotations:
            a._text = "RECREATE ME"

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

        self.annotations = [
            annotation for annotation in self.annotations if annotation.is_valid
        ]

        self._update_buffered_properties()

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
            )

        # Update the position of the annotations
        for a in self.annotations:
            a._p3 = a.get_anchor_3d(self.scene_renderer)

    @property
    def is_valid(self):
        return True

    def render(self):
        """Renders the annotations on a render window."""

        for annotation in self.annotations:
            p3 = (
                annotation._p3
            )  # all private properties used here are created by _update_buffered_properties
            p2 = self.scene_renderer.to_screenspace(p3)
            offset = annotation.anchor.screenspace_offset

            if (
                annotation._text.strip() != ""
            ):  # only render annotation that are not empty
                annotation._overlay_actor.render_at(
                    render_window=self.scene_renderer.window,
                    x=p2[0] + offset[0],
                    y=p2[1] + offset[1],
                )


class CustomNodeLayer(AnnotationLayer):
    default_selector = NodeSelector()

    def __init__(
        self,
        scene: Scene,
        scene_renderer: AbstractSceneRenderer,
        do_not_update_yet=False,
    ):
        """Initializes the annotation layer."""
        super().__init__(scene_renderer=scene_renderer, name="Custom Node Layer")

        self._scene = scene
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

        super().update()  # removes invalid annotations

    @abstractmethod
    def provide_annotation_for_node(self, node: Node) -> Annotation:
        pass
