"""Not a volume mesh"""

from DAVE import *

def test_mesh_errors():


    s = Scene()

    s.new_frame(name='Frame')
    s.new_tank(name='Tank', parent='Frame').trimesh.load_file('res: cube.obj')


    s['Tank'].trimesh.load_file(r'res: plane.obj', scale=(1.0, 1.0, 1.0), rotation=(0.0, 0.0, 0.0),
                                offset=(0.0, 0.0, 0.0))


    s.update()

    ers = s.node_errors

    for er in ers:
        print(er)

    assert len(ers) >= 2
    assert ers[0][0].name == 'Tank'