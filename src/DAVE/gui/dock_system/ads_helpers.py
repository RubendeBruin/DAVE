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

from PySide6 import QtWidgets

import PySide6QtAds
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, Qt


# from DAVE.gui.helpers.my_qt_helpers import remove_from_stylesheet


def customize_stylesheet(stylesheet: str, identifier: str) -> str:
    """Changes the icon size,
    removes the splitter styling
    """

    old_size = "ads--CAutoHideTab {\n	qproperty-iconSize: 16px 16px;"
    new_size = "ads--CAutoHideTab {\n	qproperty-iconSize: 32px 32px;"

    if old_size not in stylesheet:
        raise ValueError("Old icon size not found")
    stylesheet = stylesheet.replace(old_size, new_size)

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


def create_dock_manager(main_window, settings=None):
    PySide6QtAds.CDockManager.setConfigFlag(
        PySide6QtAds.CDockManager.OpaqueSplitterResize, True
    )
    PySide6QtAds.CDockManager.setConfigFlag(
        PySide6QtAds.CDockManager.XmlCompressionEnabled, False
    )
    PySide6QtAds.CDockManager.setConfigFlag(
        PySide6QtAds.CDockManager.FocusHighlighting, False
    )
    PySide6QtAds.CDockManager.setConfigFlag(
        PySide6QtAds.CDockManager.ActiveTabHasCloseButton, False
    )
    PySide6QtAds.CDockManager.setConfigFlag(
        PySide6QtAds.CDockManager.DockAreaCloseButtonClosesTab, True
    )

    # auto-hide icons

    PySide6QtAds.CDockManager.setAutoHideConfigFlag(
        PySide6QtAds.CDockManager.DefaultAutoHideConfig
    )

    PySide6QtAds.CDockManager.setAutoHideConfigFlag(
        PySide6QtAds.CDockManager.AutoHideSideBarsIconOnly, True
    )

    dock_manager = PySide6QtAds.CDockManager(main_window)

    dock_manager.setConfigFlag(PySide6QtAds.CDockManager.ActiveTabHasCloseButton, False)
    ss = dock_manager.styleSheet()
    ss = customize_stylesheet(ss, "ads--CDockSplitter::handle")
    dock_manager.setStyleSheet(ss)

    if settings is not None:
        try:
            dock_manager.loadPerspectives(settings)
        except:
            import warnings

            warnings.warn(
                "Dockmanager: can not open perspectives from settings, continuing without"
            )

    return dock_manager


def set_as_central_widget(
    dock_manager: PySide6QtAds.CDockManager, widget: QtWidgets.QWidget
):
    central_dock_widget = PySide6QtAds.CDockWidget("CentralWidget")

    central_dock_widget.setWidget(widget)
    central_dock_area = dock_manager.setCentralWidget(central_dock_widget)
    central_dock_widget.setFeature(PySide6QtAds.CDockWidget.DockWidgetClosable, False)
    central_dock_area.setAllowedAreas(PySide6QtAds.DockWidgetArea.OuterDockAreas)
    return central_dock_widget


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
    print(f"hiding {d}")
    all_widgets = get_all_active_docks(manager)

    if d not in all_widgets:
        return  # already hidden

    if d.isClosed():
        return

    if d.isVisible() or d.isHidden():
        d.toggleViewAction().trigger()


def dock_show(manager: PySide6QtAds.CDockManager, d: PySide6QtAds.CDockWidget, force_bring_to_front=False):
    """Makes sure a dock is present in the gui

    if force_bring_to_front is True, the dock will be brought to the front as well (which can be annoying)
    """
    try:
        print(f"showing {d}")
    except RuntimeError:
        print("Can not show dock because it was already deleted")

    if d.isVisible():
        return  # already visible

    if d.isHidden():
        if force_bring_to_front:
            d.setAsCurrentTab()

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


def add_global_dock(
    manager: PySide6QtAds.CDockManager,
    d: PySide6QtAds.CDockWidget,
    icon=":v2/icons/empty_box.svg",
):
    """Adds a dock to the manager and make it a 'global' dock.
    Global docks are docks that can not be closed and are hidden on the top right by default.
    """
    assert isinstance(d, PySide6QtAds.CDockWidget)

    if icon is not None:
        if isinstance(icon, str):
            icon = QIcon(icon)
        d.setIcon(icon)

    container = manager.addAutoHideDockWidget(
        PySide6QtAds._ads.SideBarLocation.SideBarRight, d
    )  # Ref: https://github.com/mborgerson/pyside6_PySide6QtAds/issues/23

    d.setFeature(PySide6QtAds.CDockWidget.DockWidgetFeature.CustomCloseHandling, True)
    d.closeRequested.connect(lambda dock=d: _dock_return_to_hidden_state(dock))

    container.setSize(350)

    return d


if __name__ == "__main__":
    from PySide6.QtWidgets import (
        QApplication,
        QWidget,
        QVBoxLayout,
        QPushButton,
        QMainWindow,
        QLabel,
        QToolBar,
    )

    from PySide6 import QtGui, QtCore

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

    d = add_global_dock(dock_manager, global_dock1)
    d.setIcon(QIcon(r"/guis/icons/footprint90.svg"))

    global_widget2 = QLabel("Global widget 2")
    global_widget2.setStyleSheet("background-color: green;")
    global_dock2 = PySide6QtAds.CDockWidget("Global Dock 2", mw)
    global_dock2.setWidget(global_widget2)
    d = add_global_dock(dock_manager, global_dock2)

    icon = QIcon(r"/guis/icons/footprint90.svg")

    d.setIcon(icon)

    # ==== Setup the normal docks
    #
    # Connect them to a button group on the main toolbar

    top_toolbar = QToolBar("Top Toolbar")
    mw.addToolBar(Qt.ToolBarArea.TopToolBarArea, top_toolbar)

    top_left_widget = QWidget()
    top_toolbar.addWidget(top_left_widget)

    docks = list()
    actions = list()
    left = None
    for i in range(4):
        d = PySide6QtAds.CDockWidget(f"Dock {i}", mw)
        lbl = QLabel(f"Widget {i}")
        r = 120 + 20 * i
        g = 100 + 20 * i
        b = 100 + 20 * i
        lbl.setStyleSheet(f"background-color: rgb({r},{g},{b});")
        d.setWidget(lbl)
        docks.append(d)

        d.is_left = True

        if i > 0:
            if docks[0].is_left:
                dock_manager.addDockWidget(
                    PySide6QtAds.DockWidgetArea.BottomDockWidgetArea,
                    d,
                    docks[0].dockAreaWidget(),
                )
        else:
            dock_manager.addDockWidget(
                PySide6QtAds.DockWidgetArea.LeftDockWidgetArea, d
            )

        action = d.toggleViewAction()
        action.setIcon(QIcon(r"/guis/icons/footprint.svg"))
        top_toolbar.addAction(action)
        actions.append(action)

    # add a horizontal spacer to the top toolbar
    spacer = QWidget()
    spacer.setSizePolicy(
        QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
    )
    top_toolbar.addWidget(spacer)

    # add a button to close all docks
    close_all_docks = QPushButton("Button on the right")
    top_toolbar.addWidget(close_all_docks)
    top_toolbar.setMovable(False)

    # Vertical toolbar on left side
    left_toolbar = QToolBar("Left Toolbar")
    mw.addToolBar(Qt.ToolBarArea.LeftToolBarArea, left_toolbar)
    left_toolbar.setOrientation(Qt.Vertical)
    left_toolbar.setIconSize(QSize(32, 32))
    left_toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    left_toolbar.addAction(actions[0])
    left_toolbar.addAction(actions[1])
    left_toolbar.addAction(actions[2])
    left_toolbar.addAction(actions[3])

    left_toolbar.setMovable(False)

    mw.setStyleSheet(mw.styleSheet() + "\nQToolBar {border: none;}")

    top_left_widget.setFixedWidth(left_toolbar.sizeHint().width())

    # remove the window title bar but keep the frame
    # mw.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    mw.show()

    top_toolbar.removeAction(actions[2])

    app.exec()
