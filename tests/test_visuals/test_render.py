import pytest
from DAVE import DG, Visual

@pytest.mark.skip(reason="This test is interactive")
def test_render_basic_nodes(model_basic_nodes):

    s = model_basic_nodes
    s['Visual'].parent = None

    for node in s._nodes:
        if not isinstance(node, Visual):
            s.delete(node)

    from DAVE.visual_helpers.simple_scene_renderer import SimpleSceneRenderer
    renderer = SimpleSceneRenderer(s)
    renderer.show()