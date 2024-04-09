"""Annotations module.

Annotations are texts that can be added to the visual to provide additional information.

the text of an annotation is provided by a TextProducer object.
the position of an annotation is provided by an Anchor object.

annotations are organized in annotation-layers. Each layer contains a list of annotations.

Anchors and TextProducers may contain references to nodes. This means they can become invalid if the node is deleted.
This is handled by the update() method and is_valid property. Both are defined in abstract class "HasNodeReference"

"""

from .layer import AnnotationLayer
from .text_producer import TextProducer, TextProducer_NodeProperty
from .annotation import Annotation
from .anchor import Anchor
