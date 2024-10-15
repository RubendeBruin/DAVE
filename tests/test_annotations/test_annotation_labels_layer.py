from DAVE.annotations import AnnotationLayer, Annotation
from DAVE.annotations.custom_layers import NodeLabelLayer
from DAVE.visual_helpers.image_screen_renderer import ImageRenderer
from DAVE.visual_helpers.simple_scene_renderer import SimpleSceneRenderer


def test_labels(model):
    s= model
    v = SimpleSceneRenderer(s)
    a = NodeLabelLayer(s,v)
    assert len(a.annotations) == len(s._nodes)


def test_labels_positions_and_labels(model):
    s= model
    v = SimpleSceneRenderer(s)
    L = NodeLabelLayer(s,v)

    node_labels = [node.label for node in s.nodes()]

    for a in L.annotations:
        # get the node from the annotation
        text = a.get_text()
        assert text in node_labels


def test_labels_remove(model):
    s = model
    v = SimpleSceneRenderer(s)
    L = NodeLabelLayer(s,v)

    s.clear()
    L.update()

    assert len(L.annotations) == 0


def test_labels_add(model):
    s = model
    v = SimpleSceneRenderer(s)
    L = NodeLabelLayer(s,v)

    s.new_point("new_point", position=(0, 0, 0))

    L.update()

    assert len(L.annotations) == len(s._nodes)

    s.clear()
    L.update()

    assert len(L.annotations) == 0

def test_multiline_annotation(cable):
    s = cable
    cable = s["cable"]

    v = ImageRenderer(s)
    v.zoom_all()

    L = AnnotationLayer(name = "test", scene_renderer=v, scene=s)
    v.layers.append(L)

    # add an annotation to the cable
    a = Annotation.create_eval_annotation(node = cable, code_to_eval='"Multi_line<br>annotation<br>test"')
    # a.anchor.position_1f = 0.8

    a.get_anchor_3d(v)

    L.add_annotation(a)
    L.update()
    #
    v.show()