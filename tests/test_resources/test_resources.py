import pytest
from pathlib import Path

from DAVE import *


def test_get_res():
    s = Scene()
    f = s.get_resource_path("res:cube.obj")
    assert f.name == "cube.obj"


def test_get_res_gracefull_warning():
    s = Scene()
    f = s.get_resource_path("cube.obj")
    assert f.name == "cube.obj"


def test_get_res_gracefull_warning_path():
    s = Scene()
    f = s.get_resource_path(Path("cube.obj"))
    assert f.name == "cube.obj"


def test_get_res_spaces():
    s = Scene()
    f = s.get_resource_path("res:     cube.obj")
    assert f.name == "cube.obj"


def test_probably_an_error():

    """Note: fails when a gui is open
    Run independently of the rest of the tests"""

    s = Scene()
    with pytest.raises(Exception):
        f = s.get_resource_path("res: unlikely to exist.obj")


def test_get_res_visual():
    s = Scene()
    s.new_frame("dummy")
    v = s.new_visual("flower", parent="dummy", path="res: cube.obj")
    assert v.file_path.name == "cube.obj"


def test_get_res_hyddb1():
    s = Scene()
    s.new_frame("dummy")
    v = s.new_waveinteraction(
        "flower", parent="dummy", path="res: cube.obj"
    )  # not a hydb, but for the test that does not matter
    assert v.file_path.name == "cube.obj"


def test_scene():
    s = Scene("res: cheetah.dave")


def test_get_resource():
    s = Scene()
    res = s.get_resource_path('res: cheetah.dave')


def test_get_resources():
    s = Scene("cheetah.dave")
    print(s.get_used_resources())

def test_nested_resources():
    s = Scene()
    path = Path(__file__).parent.parent / 'files'
    s.add_resources_paths(path)
    s.new_component('outer_component', 'res: outer_component.dave')

    resource_list = s.get_used_resources()

    for r,p in resource_list:
        print(r, p)

