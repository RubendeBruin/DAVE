from . import Annotation, TextProducer, Anchor
from .layer import BaseAnnotationLayer
from .. import Cable
from ..settings import DAVE_ANNOTATION_LAYERS


class CableInternalForceLayer(BaseAnnotationLayer):

    def post_init(self):
        self._annotations = []

    def update(self):
        self._update_annotations()
        super().update()

    def _update_annotations(self):
        self._annotations = []

        for cable in self._scene.nodes_where(kind=Cable):


            for d in cable.get_annotation_data():

                f1 = d[0]
                tension = d[1]

                # The anchor defines the position of the annotation
                # using 1f (length along the cable)
                anchor = Anchor(node=cable, position_1f=f1)

                # the text is just a fixed string
                text_producer = TextProducer(node=None,
                                             text=tension)


                annotation = Annotation(text_producer, anchor)

                self._annotations.append(annotation)

    @property
    def annotations(self) -> list[Annotation]:
        return self._annotations

DAVE_ANNOTATION_LAYERS["Cable internal forces"] = CableInternalForceLayer