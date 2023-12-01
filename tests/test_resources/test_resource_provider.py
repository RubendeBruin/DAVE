from copy import copy, deepcopy
from pathlib import Path

import pytest

from DAVE.resource_provider import DaveResourceProvider


def test_get_resource_res_root():
    s = DaveResourceProvider()

    res = s.get_resource_path("res: cheetah.dave")
    assert res.name == "cheetah.dave"


def test_get_resource_res_subdir():
    s = DaveResourceProvider()

    res = s.get_resource_path("res: cheetah/tanks/c8.stl")
    assert res.name == "c8.stl"


def test_get_resource_cd():
    path = Path(__file__).parent.parent / "files"
    s = DaveResourceProvider(cd=path)

    res = s.get_resource_path("cd: inner_component.dave")
    assert res.name == "inner_component.dave"

#
# def test_get_resource_gui():
#     assert False, "Disabled due to GUI use"
#
#     s = DaveResourceProvider()
#
#     from PySide6.QtWidgets import QApplication
#
#     app = QApplication()
#
#     res = s.get_resource_path("res: cube.stl")


def test_constructor():
    s = DaveResourceProvider("aap", "noot", "mies")
    assert Path("noot") in s.resources_paths
    assert Path("mies") in s.resources_paths
    assert Path("aap") not in s.resources_paths


def test_logging():
    s = DaveResourceProvider()
    resources = ("res: cheetah.dave", "res: billy.dave", "res: cube.obj")
    for r in resources:
        s.get_resource_path(r)

    log = s.getLog()
    assert len(log) == 3
    assert log[0][0] == "res: cheetah.dave"  # url
    assert log[0][1].name == "cheetah.dave"  # resolved
    assert len(log[0]) == 2


def test_get_all_resources_of_type():
    s = DaveResourceProvider()
    lst = s.get_resource_list(".stl", include_subdirs=True, include_current_dir=False)
    assert len(lst) >= 2
    assert "res: cheetah/tanks/c8.stl" in lst


def test_get_all_resources_of_type_no_error_no_cd():
    s = DaveResourceProvider()

    lst = s.get_resource_list(
        ".dave", include_subdirs=True, include_current_dir=True
    )


def test_copy():
    s = DaveResourceProvider()
    s2 = deepcopy(s)  # deep-copy is required for the lists to be independent

    s.resources_paths.append("BS")

    assert s.resources_paths != s2.resources_paths
