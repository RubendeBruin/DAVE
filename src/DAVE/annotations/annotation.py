from DAVE import Node
from DAVE.annotations.anchor import Anchor
from DAVE.annotations.text_producer import TextProducer, TextProducer_NodeProperty, TextProducer_Eval
from DAVE.annotations.has_node_reference import HasNodeReference
from DAVE.visual_helpers.scene_renderer import AbstractSceneRenderer


class Annotation(HasNodeReference):

    def __init__(self, text_producer: TextProducer, anchor: Anchor):
        self.text_producer: TextProducer = text_producer
        self.anchor: Anchor = anchor

    def update(self):
        self.text_producer.update()
        self.anchor.update()

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
        text_producer = TextProducer_NodeProperty(node=node, property="label")
        anchor = Anchor(node=node)
        return Annotation(text_producer, anchor)

    @staticmethod
    def create_eval_annotation(node: Node, code_to_eval: str):
        text_producer = TextProducer_Eval(node=node, code_to_eval=code_to_eval)
        anchor = Anchor(node=node)
        return Annotation(text_producer, anchor)