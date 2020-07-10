from DAVE.gui.main import Gui
from DAVE.scene import Scene

s = Scene()

# auto generated pyhton code
# By beneden
# Time: 2020-03-29 15:09:12 UTC

# To be able to distinguish the important number (eg: fixed positions) from
# non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
# For anything written as solved(number) that actual number does not influence the static solution
def solved(number):
    return number

# code for Vessel
s.new_axis(name='Vessel',
           position=(0.0,
                     0.0,
                     0.0),
           rotation=(0.0,
                     0.0,
                     0.0),
           fixed =(True, True, True, True, True, True) )
# code for Buoyancy mesh
mesh = s.new_buoyancy(name='Buoyancy mesh',
          parent='Vessel')
mesh.trimesh.load_file(s.get_resource_path(r'cube.obj'), scale = (40.0, 10.0, 3.0), rotation = (0.0, 0.0, 0.0), offset = (0.0, 0.0, 0.0))

BM = (1/12) * 10*10 / 1.5

s.new_rigidbody('vessel mass', parent = 'Vessel')
s['vessel mass'].position = (0.0, 0.0, 3.0)
s['vessel mass'].mass = 615.0



Gui(s)


#

# auto generated pyhton code
# By beneden
# Time: 2020-03-30 10:46:59 UTC

# To be able to distinguish the important number (eg: fixed positions) from
# non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
# For anything written as solved(number) that actual number does not influence the static solution
def solved(number):
    return number

# code for Vessel_global_motion
s.new_axis(name='Vessel_global_motion',
           position=(0.0,
                     0.0,
                     solved(0.0)),
           rotation=(0.0,
                     0.0,
                     0.0),
           fixed =(True, True, False, True, True, True) )
# code for Vessel_trim_motion
s.new_axis(name='Vessel_trim_motion',
           parent='Vessel_global_motion',
           position=(0.0,
                     0.0,
                     0.0),
           rotation=(0.0,
                     0.0,
                     0.0),
           fixed =(True, True, True, True, True, True) )
# code for Vessel_heel
s.new_axis(name='Vessel_heel',
           parent='Vessel_trim_motion',
           position=(0.0,
                     0.0,
                     0.0),
           rotation=(solved(40.0),
                     0.0,
                     0.0),
           fixed =(True, True, True, False, True, True) )
# code for Vessel
s.new_axis(name='Vessel',
           parent='Vessel_heel',
           position=(0.0,
                     0.0,
                     0.0),
           rotation=(0.0,
                     0.0,
                     0.0),
           fixed =(True, True, True, True, True, True) )
# code for Buoyancy mesh
mesh = s.new_buoyancy(name='Buoyancy mesh',
          parent='Vessel')
mesh.trimesh.load_file(s.get_resource_path(r'cube.obj'), scale = (40.0, 10.0, 3.0), rotation = (0.0, 0.0, 0.0), offset = (0.0, 0.0, 0.0))
# code for vessel mass
s.new_rigidbody(name='vessel mass',
                mass=515.0,
                cog=(0.0,
                     0.0,
                     0.0),
                parent='Vessel',
                position=(0.0,
                          0.0,
                          3.0),
                rotation=(0.0,
                          0.0,
                          0.0),
                fixed =(True, True, True, True, True, True) )
# # code for crane tip
# s.new_point(name='crane tip',
#           parent='Vessel',
#           position=(0.0,
#                     0.0,
#                     13.0))
# # code for Cargo
# s.new_rigidbody(name='Cargo',
#                 mass=100.0,
#                 cog=(0.0,
#                      0.0,
#                      0.0),
#                 parent='Vessel',
#                 position=(solved(0.0),
#                           solved(-0.0),
#                           solved(5.313)),
#                 rotation=(solved(0.0),
#                           solved(0.0),
#                           solved(0.0)),
#                 fixed =(False, False, False, False, False, False) )
# # code for liftpoint
# s.new_point(name='liftpoint',
#           parent='Cargo',
#           position=(0.0,
#                     0.0,
#                     0.0))
# # code for Cable
# s.new_cable(name='Cable',
#             poiA='liftpoint',
#             poiB='crane tip',
#             length=7.0,
#             EA=10000.0)
# # code for Visual - centerline
# s.new_visual(name='Visual - centerline',
#             parent='Vessel',
#             path=r'cube.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(1.0, 0.01, 100.0) )
# # code for Visual - visual
# s.new_visual(name='Visual - visual',
#             parent='Vessel',
#             path=r'cube.obj',
#             offset=(0, 0, 0),
#             rotation=(0, 0, 0),
#             scale=(40.0, 10.0, 3.0) )