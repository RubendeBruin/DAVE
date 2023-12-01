from copy import copy, deepcopy
from pathlib import Path

import pytest

from DAVE.resource_provider import DaveResourceProvider




def test_get_resource_gui():
    assert False, "Disabled due to GUI use"

    s = DaveResourceProvider()

    from PySide6.QtWidgets import QApplication

    app = QApplication()

    res = s.get_resource_path("res: cube.stl")

