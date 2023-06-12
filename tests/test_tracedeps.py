from time import time

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

def test_sort_by_parent():
    s = Scene()

    last = None
    for i in range(200):
        last = s.new_frame(f'frame{i}', parent = last)

    tic = time()
    s.sort_nodes_by_parent()
    toc = time() - tic
    print(toc)

def test_noncore_direct_parent():
    s = Scene()
    s.new_frame('frame')
    v = s.new_visual('vis', parent = s['frame'], path="res: cube.obj")
    assert v.name in s.nodes_depending_on('frame')
