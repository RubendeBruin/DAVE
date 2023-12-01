from DAVE import *


def test_ask_nicely_gui():
    s = Scene()
    s.new_point("point")

    from PySide6.QtWidgets import QApplication
    if QApplication.instance() is None:
        app = QApplication([])

    from DAVE import gui_globals
    gui_globals.do_ask_user_for_unavailable_nodenames = True

    s['Point']  #<--- trigger the gui