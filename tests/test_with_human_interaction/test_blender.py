from DAVE import *
from DAVE.io.blender import create_blend_and_open


s = Scene()
s.new_point('p1', position=(5, 0, 0))
s.new_point('p2', position=(0, 0, 10))
s.new_circle('c2', parent='p2', radius=1, axis=(0, 1, 0))
s.new_point('p3', position=(-5, 0, 0))

c = s.new_cable(connections=['p3', 'c2', 'p1'], name='cable', EA=122345, mass= 10, length=40)


from DAVE.gui.dialog_blender import try_get_blender_executable

blender_executable = try_get_blender_executable()
create_blend_and_open(s, blender_exe_path=blender_executable)