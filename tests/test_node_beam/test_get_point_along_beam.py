import numpy as np

from DAVE import *

def test_point_along_beam():
    s = Scene()

    # code for f1
    s.new_frame(name='f1')

    # code for f2
    s.new_frame(name='f2',  position=(15,
                          0,
                          0))


    # code for beam beam
    beam = s.new_beam(name='beam',
                      nodeA='f1',
                      nodeB='f2',
                      n_segments=20.0,
                      EA=100,
                      L=15)  # L can possibly be omitted

    s.update()

    for f in np.linspace(-1,1.1,num=23):
        p = beam.get_point_along_beam(f)
        assert isinstance(p, tuple)
        assert len(p) == 3
        assert all(isinstance(x, float) for x in p)