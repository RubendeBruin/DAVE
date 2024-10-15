import numpy as np

from DAVE import Scene
from DAVE.annotations import AnnotationLayer, Annotation
from DAVE.annotations.custom_layers import CableTensionLayer
from DAVE.visual_helpers.image_screen_renderer import ImageRenderer



def test_annotated_cable(cable):
    s = cable
    cable = s["cable"]

    p = s.new_point(name='p3', position=(0, 20, 0))
    cable.connections = [*cable.connections, p]

    s.update()

    v = ImageRenderer(s)
    v.zoom_all()

    L = AnnotationLayer(scene_renderer=v, scene=s)
    v.layers.append(L)

    # add an annotation to the cable
    for p in np.linspace(0,1,10):
        a = Annotation.create_node_label_annotation(cable)
        a.anchor.position_1f = p
        L.add_annotation(a)
    L.update()
    #
    v.show()


def test_annotated_cable_slack(cable):
    s = cable
    cable = s["cable"]

    p = s.new_point(name='p3', position=(0, 20, 0))
    cable.connections = [*cable.connections, p]

    cable.EA = 1000
    cable.length = 40

    s.update()

    v = ImageRenderer(s)
    v.zoom_all()

    L = AnnotationLayer(scene_renderer=v, scene=s)
    v.layers.append(L)

    # add an annotation to the cable
    for p in np.linspace(0, 1, 10):
        a = Annotation.create_node_label_annotation(cable)
        a.anchor.position_1f = p
        L.add_annotation(a)
    L.update()
    #
    v.show()


def test_cable_tension_annotation(cable):
    s = cable
    cable = s["cable"]
    cable.EA = 1000
    cable.length = 10
    s.update()

    v = ImageRenderer(s)
    v.zoom_all()

    L = CableTensionLayer(scene = s, scene_renderer=v)
    v.layers.append(L)

    #
    v.show()

def test_cable_catenary_annotation():
    s = Scene()
    s.new_point(name='p1', position=(-10, 0, 0))
    s.new_point(name='p2', position=(0, 0, 0))
    s.new_point(name='p3', position=(10, 0, 0))

    c = s.new_cable(connections=['p1', 'p2','p3'], name='cable', EA=1e6, length=30)

    v = ImageRenderer(s)
    v.zoom_all()

    L = CableTensionLayer(scene=s, scene_renderer=v)
    v.layers.append(L)

    #
    v.show()
