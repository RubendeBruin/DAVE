"""Are we well protected against trying to modify an item that has been deleted?"""

import pytest
from DAVE import *

def test_change_name_on_deleted_item():
    scene = Scene()
    p = scene.new_point('test')
    scene.delete('test')
    with pytest.raises(ValueError):
        p.name = "Demo"

def test_get_name_on_deleted_item():
    scene = Scene()
    p = scene.new_point('test')
    scene.delete('test')

    assert p.name is None

    with pytest.raises(Exception):
        print(p.warnings)
