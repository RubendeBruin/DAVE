from DAVE import DG, Visual, Scene, Frame
from DAVE.visual_helpers.simple_scene_renderer import SimpleSceneRenderer


def test_render_gltf():

    s = Scene()
    v = s.new_visual("Visual", path = r"res: koala_hull.glb")
    # v.rotation = (90,0,0)

    # DG(s)
    #
    # renderer = SimpleSceneRenderer(s)
    # renderer.show()