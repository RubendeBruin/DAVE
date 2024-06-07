from DAVE import *
from DAVE.io.blender import create_blend_and_open, try_get_blender_executable

def test_blender_gltf_export(test_files):
    s = Scene()

    path = test_files / 'gltf_test.glb'

    assert path.exists()

    s.new_visual(name='Visual', path=path)

    blender_exe = try_get_blender_executable()

    create_blend_and_open(
        s,
        blender_exe_path=blender_exe,
    )
