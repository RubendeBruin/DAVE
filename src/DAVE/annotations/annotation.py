from DAVE import Node
from DAVE.annotations.anchor import Anchor
from DAVE.annotations.text_producer import TextProducer, ProduceTextAlgorithm
from DAVE.annotations.has_node_reference import HasNodeReference
from DAVE.visual_helpers.scene_renderer import AbstractSceneRenderer


class Annotation(HasNodeReference):
    def __init__(self, text_producer: TextProducer, anchor: Anchor):
        self.text_producer: TextProducer = text_producer
        self.anchor: Anchor = anchor

    def as_dict(self):
        return {
            "text_producer": self.text_producer.as_dict(),
            "anchor": self.anchor.as_dict(),
        }

    @staticmethod
    def from_dict(d, scene):
        return Annotation(
            TextProducer.from_dict(d["text_producer"], scene),
            Anchor.from_dict(d["anchor"], scene),
        )

    def update(self):
        self.text_producer.update()
        self.anchor.update()

    @property
    def hide(self):
        return self.text_producer.hide

    @hide.setter
    def hide(self, value):
        self.text_producer.hide = value

    @property
    def hidden(self):
        return self.text_producer.hidden


    @property
    def is_valid(self):
        return self.text_producer.is_valid and self.anchor.is_valid

    def get_text(self):
        return self.text_producer.get_text()

    def get_anchor_3d(self, viewport: AbstractSceneRenderer):
        return self.anchor.get_anchor_3d(viewport)

    def get_offset(self):
        return self.anchor.screenspace_offset

    @staticmethod
    def create_node_label_annotation(node: Node):
        text_producer = TextProducer(
            node=node, text="label", how=ProduceTextAlgorithm.PROPERTY_RAW
        )
        anchor = Anchor(node=node)
        return Annotation(text_producer, anchor)

    @staticmethod
    def create_eval_annotation(node: Node, code_to_eval: str):
        text_producer = TextProducer(
            node=node, text=code_to_eval, how=ProduceTextAlgorithm.EVAL
        )
        anchor = Anchor(node=node)
        return Annotation(text_producer, anchor)

    @staticmethod
    def create_node_property_annotation(
        node: Node, property: str, anchor: Anchor or None = None
    ):
        if anchor is None:
            anchor = Anchor(node=node)
        text_producer = TextProducer(
            node=node, text=property, how=ProduceTextAlgorithm.PROPERTY
        )
        return Annotation(text_producer, anchor)

    @staticmethod
    def create_node_property_raw_annotation(
        node: Node, property: str, anchor: Anchor or None = None
    ):
        if anchor is None:
            anchor = Anchor(node=node)
        text_producer = TextProducer(
            node=node, text=property, how=ProduceTextAlgorithm.PROPERTY_RAW
        )
        return Annotation(text_producer, anchor)

    @staticmethod
    def create_node_text_annotation(
            node: Node, text: str, anchor: Anchor or None = None
    ):
        if anchor is None:
            anchor = Anchor(node=node)
        text_producer = TextProducer(
            node=node, text=text, how=ProduceTextAlgorithm.NOTHING
        )
        return Annotation(text_producer, anchor)

