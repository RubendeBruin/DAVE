from DAVE import *

def test_tracedeps():
    s = Scene()

    last = None
    for i in range(200):
        last = s.new_frame(f'frame{i}', parent = last)

    fr40 = s['frame40']
    vis = s.new_visual('vis', parent = fr40, path="res: cube.obj")

    print('tracing', flush=True)
    deps  = s.nodes_depending_on('frame0')

    assert fr40.name in deps
    assert vis.name in deps
