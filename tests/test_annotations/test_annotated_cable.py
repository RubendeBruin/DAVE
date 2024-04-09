from DAVE.annotations import AnnotationLayer, Annotation
from DAVE.visual_helpers.image_screen_renderer import ImageRenderer


def test_annotated_cable(cable):
    s = cable
    cable = s["cable"]

    v = ImageRenderer(s)
    v.zoom_all()

    L = AnnotationLayer(name = "test", scene_renderer=v)
    v.layers.append(L)

    # add an annotation to the cable
    a = Annotation.create_node_label_annotation(cable)
    # a.anchor.position_1f = 0.8

    a.get_anchor_3d(v)

    L.add_annotation(a)
    L.update()
    #
    v.show()
