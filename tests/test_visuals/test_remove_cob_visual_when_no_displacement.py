from DAVE import *
from DAVE.visual_helpers.simple_scene_renderer import SimpleSceneRenderer


def model():
    s = Scene()

    # code for Frame
    f = s.new_frame(name='Frame',
                    position=(0,
                              0,
                              0),
                    rotation=(0,
                              10,
                              0),
                    fixed=(True, True, True, True, True, True),
                    )

    # code for Tank
    mesh = s.new_buoyancy(name='Shape',
                      parent='Frame')
    mesh.trimesh.load_file(r'res: cube.obj', scale=(10.0, 10.0, 10.0), rotation=(0.0, 0.0, 0.0), offset=(0.0, 0.0, 0.0))
    t = s['Shape']

    return s, f, t

def test_remove_cob_visual_when_no_displacement():
    s, f, t = model()


    renderer = SimpleSceneRenderer(s)

    # get the cob visual
    cob_visual = renderer.actor_from_node(t).actors['cob']
    assert cob_visual.GetVisibility()

    f.z = 20

    renderer.position_visuals()
    cob_visual = renderer.actor_from_node(t).actors['cob']
    assert not cob_visual.GetVisibility()

