from pytest import raises
from DAVE import *
def test_ask_nicely_no_gui():
    s = Scene()
    s.new_point("point")

    with raises(ValueError):
        s['Point']

def test_ask_nicely_gui_default():
    s = Scene()
    s.new_point("point")

    from PySide6.QtWidgets import QApplication
    app = QApplication([])

    with raises(ValueError):
        s['Point']

def test_ask_nicely_gui():
    s = Scene()
    s.new_point("point")

    from PySide6.QtWidgets import QApplication
    app = QApplication([])

    from DAVE import gui_globals
    gui_globals.do_ask_user_for_unavailable_nodenames = True

    s['Point']