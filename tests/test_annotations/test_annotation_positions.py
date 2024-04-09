from DAVE.annotations.layer import NodeLabelLayer
from DAVE.visual_helpers.image_screen_renderer import ImageRenderer
from DAVE.visual_helpers.simple_scene_renderer import SimpleSceneRenderer


def test_annotation_positions_image(model):
    s= model
    L = NodeLabelLayer(s)

    v = ImageRenderer(s)
    v.layers.append(L)

    for a in L.annotations:
        anchor = a.get_anchor(v)
        print(anchor)

    v.show()


def test_annotation_positions_interactive(model):
    s= model
    L = NodeLabelLayer(s)

    v = SimpleSceneRenderer(s)
    v.layers.append(L)

    for a in L.annotations:
        anchor = a.get_anchor(v)
        print(anchor)

    v.show()
