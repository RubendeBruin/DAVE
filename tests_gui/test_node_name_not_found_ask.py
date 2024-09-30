from PySide6.QtWidgets import QApplication

from DAVE import *
from DAVE.gui.error_interaction import ErrorInteraction


def test_ask_nicely_gui():
    s = Scene()
    s.new_point("point")

    app = QApplication.instance() or QApplication([])
    s.error_interaction = ErrorInteraction()

    s['Point']  #<--- trigger the gui

def test_ask_nicely_gui_resource():
    s = Scene()
    s.new_point("point")

    app = QApplication.instance() or QApplication([])
    s.error_interaction = ErrorInteraction()

    s.new_visual("visual", "res: test/sh.stl")

    s.new_visual("visual2", "res: test/sh.stl")

    assert isinstance(s['visual'].path, str)

    DG(s)