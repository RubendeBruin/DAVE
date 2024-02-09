from DAVE import Scene

"""Tests the default values of the calculation settings in the Scene class"""

def test_settings():
    s = Scene()

    assert s.waterlevel == 0.0
    assert s.nFootprintSlices == 50
    assert s.roundbar_entry_ease_in_distance_m == 0.001
