from DAVE.scene import *
from DAVE.gui import Gui

s = Scene()

s.new_rigidbody(name='Tower',
                mass=100.0,
                cog=(0.0,
                     0.0,
                     32.0),
                position=(0.0,
                          0.0,
                          0.0),
                rotation=(0.0,
                          0.0,
                          0.0),
                fixed =(True, True, True, True, True, True) )
# code for Buoyancy mesh
mesh = s.new_buoyancy(name='Buoyancy mesh',
          parent='Tower')
mesh.trimesh.load_obj(s.get_resource_path(r'cone chopped.obj'), scale = (2.5,2.5,65.0), rotation = (0.0,0.0,0.0), offset = (0.0,0.0,0.0))


print(s._vfc.to_string())


Gui(s).show()