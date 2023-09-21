"""Ullage and Sounding are defined as follows:
https://usedave.nl/node_tank.html
"""

from DAVE import *

def test_ullage_and_sounding():
    s = Scene()
    f = s.new_frame('test')
    # code for Tank
    mesh = s.new_tank(name='Tank',
                      parent=f)
    mesh.trimesh.load_file(r'res: cube.obj', scale = (1.0,1.0,1.0), rotation = (0.0,0.0,0.0), offset = (3.0,0.0,2.0))
    s['Tank'].volume = 0.5   # first load mesh, then set volume

    assert mesh.ullage == 0.5
    assert mesh.sounding == 0.5

def test_ullage_and_sounding2():
    s = Scene()
    f = s.new_frame('test')
    # code for Tank
    mesh = s.new_tank(name='Tank',
                      parent=f)
    mesh.trimesh.load_file(r'res: cube.obj', scale = (10.0,10.0,10.0), rotation = (0.0,0.0,0.0), offset = (3.0,0.0,2.0))
    s['Tank'].volume = 100   # first load mesh, then set volume

    assert mesh.ullage == 9
    assert mesh.sounding == 1


