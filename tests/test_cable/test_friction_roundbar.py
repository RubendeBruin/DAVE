"""
Round-Bars with friction

- Round bars can have friction
- When a round-bar is used in a loop, then the round-bar can not be used as unknown-friction connection. This is because it may not be present.
"""
import numpy as np
import pytest

from DAVE import *

def model():
    s = Scene()
    s.new_point(name="p1", position=(-10, 0, 0))
    s.new_point(name="p2", position=(10, 0, 0))
    s.new_circle(name="c_p2", parent="p2", axis=(0, 1, 0), radius=1)
    s.new_point(name="b", position=(0, 0, 2))
    s.new_circle(name="bar", parent="b", radius=1.2, axis=(0, 1, 0), roundbar=True)
    
    c = s.new_cable(connections=["p1", "bar", "c_p2", "p1"], name="cable", EA=1e6, length=20)
    
    return s, c

def test_roundbar_in_loop_continuous_tension():
    s,c = model()

    c.friction = (0.1, 0.1, None)

    force0 = []

    s["cable"].watches["Force"] = Watch(
        evaluate="self.segment_mean_tensions[0]", condition="", decimals=3
    )

    for z in np.linspace(-1,0, num=100):
        s['b'].gz = z
        s.update()
        force0.append(c.segment_mean_tensions[0])

    print(np.max(np.diff(force0)))

    assert np.max(np.diff(force0)) < 150

def test_roundbar_in_loop_set_friction_on_roundbar_to_None():
    s,c = model()

    with pytest.raises(ValueError):
        c.friction = (0.1, None, 0.1)
