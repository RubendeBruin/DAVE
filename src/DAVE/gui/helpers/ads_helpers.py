"""md:
Helper functions for creating the gui docks with PySide6QtAds
Example is shown as a stand-alone script at the bottom of this file.

create dock manager with: `create_dock_manager(main_window)`

Global docks
- on top right size
- auto-hidden by default
- will return to auto-hidden state when closed by user
- add using: `add_global_dock(manager, dock)`
- are not affected by "close all docks" action

Normal docks
- add using: `dock_add_to_gui(manager, dock)`








The status of a dock can be read from the following properties:


visible	floating	hidden	closed	isAutoHide
 False 	 False 	    False 	 False 	 True           --> created and folded up in dock
 True 	 False 	    False 	 False 	 True           --> auto hide but active and visible on top
 True 	 False 	    False 	 False 	 False          --> normal docked and visible
 False 	 False 	    True 	 False 	 False          --> docked but hidden behind another tab
 True 	 True 	    False 	 False 	 False          --> floating and visible

 False 	 False 	    False 	 True 	 False          --> closed, not in gui

How to close and remove a dock from the gui completely:
-------------------------------------------------------

"""

import PySide6QtAds
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon


# from DAVE.gui.helpers.my_qt_helpers import remove_from_stylesheet


def customize_stylesheet(stylesheet: str, identifier: str) -> str:
    """Changes the icon size,
    removes the splitter styling
    """

    old_size = "ads--CAutoHideTab {\n	qproperty-iconSize: 16px 16px;"
    new_size = "ads--CAutoHideTab {\n	qproperty-iconSize: 32px 32px;"

    if old_size not in stylesheet:
        raise ValueError("Old icon size not found")
    stylesheet = stylesheet.replace(old_size,new_size)

    lines = stylesheet.split("\n")
    new_lines = list()
    active = True
    for line in lines:
        if identifier in line:
            active = False

        if active:
            new_lines.append(line)

        if "}" in line:
            active = True

    return "\n".join(new_lines)


def create_dock_manager(main_window):
    PySide6QtAds.CDockManager.setConfigFlag(
        PySide6QtAds.CDockManager.OpaqueSplitterResize, True
    )
    PySide6QtAds.CDockManager.setConfigFlag(
        PySide6QtAds.CDockManager.XmlCompressionEnabled, False
    )
    PySide6QtAds.CDockManager.setConfigFlag(
        PySide6QtAds.CDockManager.FocusHighlighting, True
    )
    PySide6QtAds.CDockManager.setConfigFlag(
        PySide6QtAds.CDockManager.ActiveTabHasCloseButton, False
    )
    PySide6QtAds.CDockManager.setConfigFlag(
        PySide6QtAds.CDockManager.DockAreaCloseButtonClosesTab, True
    )

    PySide6QtAds.CDockManager.setAutoHideConfigFlag(
        PySide6QtAds.CDockManager.DefaultAutoHideConfig
    )

    dock_manager = PySide6QtAds.CDockManager(main_window)

    dock_manager.setConfigFlag(PySide6QtAds.CDockManager.ActiveTabHasCloseButton, False)
    ss = dock_manager.styleSheet()
    ss = customize_stylesheet(ss, "ads--CDockSplitter::handle")
    dock_manager.setStyleSheet(ss)

    return dock_manager


def get_all_active_docks(manager: PySide6QtAds.CDockManager):
    """Returns a list of all active dock-widgets"""
    all_active_widgets = manager.dockWidgets()

    for fw in manager.floatingWidgets():
        all_active_widgets.extend(fw.dockWidgets())

    return all_active_widgets

def dock_remove_from_gui(
    manager: PySide6QtAds.CDockManager, d: PySide6QtAds.CDockWidget
):
    """Makes sure a dock is hidden"""
    print("hiding {d}")
    if d not in get_all_active_docks(manager):
        return  # already hidden

    d.toggleViewAction().trigger()


def dock_hide(manager: PySide6QtAds.CDockManager, d: PySide6QtAds.CDockWidget):
    dock_remove_from_gui(manager, d)


def dock_show(
    manager: PySide6QtAds.CDockManager, d: PySide6QtAds.CDockWidget
):
    """Makes sure a dock is visible"""
    print("showing {d}")
    if d.isVisible():
        return  # already visible

    if d not in get_all_active_docks(manager):
        d.toggleViewAction().trigger()

    if d.isClosed():
        d.toggleViewAction().trigger()

    if d.isVisible():
        return

    manager.setDockWidgetFocused(d)
    d.update()


def _dock_return_to_hidden_state(d: PySide6QtAds.CDockWidget):
    """Callback for global docks,executed when dock is closed by user"""
    manager = d.dockManager()

    d.toggleViewAction().trigger()  # removes the dock from the gui

    manager.addAutoHideDockWidget(
        PySide6QtAds._ads.SideBarLocation.SideBarRight, d
    )  # Ref: https://github.com/mborgerson/pyside6_PySide6QtAds/issues/23



def add_global_dock(manager: PySide6QtAds.CDockManager, d: PySide6QtAds.CDockWidget):
    """Adds a dock to the manager and make it a 'global' dock.
    Global docks are docks that can not be closed and are hidden on the top right by default.
    """
    manager.addAutoHideDockWidget(
        PySide6QtAds._ads.SideBarLocation.SideBarRight, d
    )  # Ref: https://github.com/mborgerson/pyside6_PySide6QtAds/issues/23

    d.setFeature(PySide6QtAds.CDockWidget.DockWidgetFeature.CustomCloseHandling, True)
    d.closeRequested.connect(lambda dock=d: _dock_return_to_hidden_state(dock))

    return d


if __name__ == "__main__":
    from PySide6.QtWidgets import (
        QApplication,
        QWidget,
        QVBoxLayout,
        QPushButton,
        QMainWindow,
        QLabel,
    )

    app = QApplication()
    mw = QMainWindow()

    dock_manager = create_dock_manager(mw)

    # create the central widget dock
    main_widget = QLabel("Main Widget")
    main_widget.setStyleSheet("background-color: lightblue;")

    central_dock = PySide6QtAds.CDockWidget("Central Dock", mw)
    central_dock.setWidget(main_widget)
    central_dock_area = dock_manager.setCentralWidget(central_dock)
    central_dock_area.setAllowedAreas(PySide6QtAds.DockWidgetArea.OuterDockAreas)

    # create an un-closable dock on the right size
    global_widget1 = QLabel("Global widget 1")
    global_widget1.setStyleSheet("background-color: lightyellow;")
    global_dock1 = PySide6QtAds.CDockWidget("Global Dock 1", mw)
    global_dock1.setWidget(global_widget1)

    add_global_dock(dock_manager, global_dock1)

    global_widget2 = QLabel("Global widget 2")
    global_widget2.setStyleSheet("background-color: green;")
    global_dock2 = PySide6QtAds.CDockWidget("Global Dock 2", mw)
    global_dock2.setWidget(global_widget2)
    d = add_global_dock(dock_manager, global_dock2)

    d.setIcon(QIcon(r"C:\data\DAVE\public\DAVE\guis\icons\footprint.svg"))

    d.tabWidget().setIconSize(QSize(42, 42))

    mw.show()

    d.setFloating()

    app.exec()
