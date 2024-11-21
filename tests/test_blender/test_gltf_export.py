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

def test_blender_all_export(test_files):
    s = Scene()

    path = test_files / 'visuals'

    assert path.exists()

    assert (path / 'suz.glb').exists()

    f = s.new_frame(name='Frame', position = (0,0,2))
    s.new_visual(name='Visual', path=path / 'suz.glb', parent = f)
    f1 = s.new_frame(name='Frame1', position = (5,0,2))
    f2 = s.new_frame(name='Frame2', position = (-5,0,2))

    s.new_visual(name='Visual2', path=path / 'suz.obj', parent = f1)
    s.new_visual(name='Visual3', path=path / 'suz_blend.glb', parent = f2)


    blender_exe = try_get_blender_executable()

    create_blend_and_open(
        s,
        blender_exe_path=blender_exe,
    )

