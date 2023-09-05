import numpy as np
from DAVE import *

def test_tank_inertia():
    """Tanks have only linear inertia"""

    s = Scene()
    s.new_frame(name = 'Frame')
    s['Frame'].fixed = False
    s.new_tank(name = 'Tank' , parent = 'Frame').trimesh.load_file('res: cube.obj')
    s['Tank'].fill_pct = 100.0

    m = s.dynamics_M()

    expected = np.zeros((6,6))
    expected[0,0] = 1.025
    expected[1,1] = 1.025
    expected[2,2] = 1.025

    assert np.allclose(m, expected)







