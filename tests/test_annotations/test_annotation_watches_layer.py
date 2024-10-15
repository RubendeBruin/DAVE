import pytest

from DAVE.annotations.custom_layers import WatchesLayer
from DAVE.visual_helpers.image_screen_renderer import ImageRenderer


def test_watches_annotation_layer(cable):
    s = cable
    cable = s["cable"]

    s.try_add_watch('cable', 'EA')
    s.try_add_watch('cable', 'actual_length')

    v = ImageRenderer(s)
    v.zoom_all()

    L = WatchesLayer( scene_renderer=v, scene=s, do_not_update_yet = False)
    v.layers.append(L)
    # L.update_annotations()
    L.update()
    #
    v.show()

@pytest.mark.skip(reason="This test is for GUI testing")
def test_watches_annotation_layer_GUI(cable):
    s = cable
    cable = s["cable"]

    s.try_add_watch('cable', 'EA')
    s.try_add_watch('cable', 'length')
    s.try_add_watch('cable', 'actual_length')

    from DAVE import DG
    DG(s)