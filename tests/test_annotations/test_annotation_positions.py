from DAVE.annotations.custom_layers import NodeLabelLayer
from DAVE.visual_helpers.image_screen_renderer import ImageRenderer
from DAVE.visual_helpers.qt_embedded_renderer import QtEmbeddedSceneRenderer
from DAVE.visual_helpers.simple_scene_renderer import SimpleSceneRenderer


def test_annotation_positions_image(model):
    s= model

    v = ImageRenderer(s)
    L = NodeLabelLayer(scene=s,scene_renderer = v)
    v.layers.append(L)

    for a in L.annotations:
        anchor = a.get_anchor_3d(v)
        print(anchor)

    v.show()


def test_annotation_positions_interactive(model):
    s= model
    v = SimpleSceneRenderer(s)
    L = NodeLabelLayer(scene=s,scene_renderer = v)

    v.layers.append(L)

    v.show()

def test_annotation_positions_interactive_qt(model):
    s= model

    from PySide6.QtWidgets import QApplication
    app = QApplication([])

    from PySide6.QtWidgets import QWidget
    widget = QWidget()

    viewer = QtEmbeddedSceneRenderer(s, widget)
    viewer.settings.show_sea = False
    viewer.update_visibility()
    viewer.update_outlines()

    L = NodeLabelLayer(scene=s,scene_renderer = viewer)
    viewer.layers.append(L)


    viewer.interactor.Initialize()

    widget.show()
    viewer.interactor.Start()

    viewer.zoom_all()
    app.exec()
