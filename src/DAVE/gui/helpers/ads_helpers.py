"""
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

import PySide6QtAds as QtAds

from DAVE.gui.helpers.my_qt_helpers import remove_from_stylesheet


def create_dock_manager(main_window):
    QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.OpaqueSplitterResize, True)
    QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.XmlCompressionEnabled, False)
    QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.FocusHighlighting, True)
    QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.ActiveTabHasCloseButton, False)
    QtAds.CDockManager.setConfigFlag(
        QtAds.CDockManager.DockAreaCloseButtonClosesTab, True
    )

    QtAds.CDockManager.setAutoHideConfigFlag(QtAds.CDockManager.DefaultAutoHideConfig)

    dock_manager = QtAds.CDockManager(main_window)

    dock_manager.setConfigFlag(QtAds.CDockManager.ActiveTabHasCloseButton, False)
    ss = dock_manager.styleSheet()
    ss = remove_from_stylesheet(ss, "ads--CDockSplitter::handle")
    dock_manager.setStyleSheet(ss)

    return dock_manager


def get_all_active_docks(manager: QtAds.CDockManager):
    """Returns a list of all active dock-widgets"""
    all_active_widgets = manager.dockWidgets()

    for fw in manager.floatingWidgets():
        all_active_widgets.extend(fw.dockWidgets())

    return all_active_widgets


def dock_add_to_gui(manager: QtAds.CDockManager, d: QtAds.CDockWidget):
    """Make an exisiting dock visible"""

    if d not in get_all_active_docks(manager):
        d.toggleViewAction().trigger()
        return

    if d.isVisible():
        return
    else:
        d.toggleViewAction().trigger()

    manager.setDockWidgetFocused(d)


def dock_remove_from_gui(manager: QtAds.CDockManager, d: QtAds.CDockWidget):
    """Makes sure a dock is hidden"""
    print("hiding {d}")
    if d not in get_all_active_docks(manager):
        return  # already hidden

    d.toggleViewAction().trigger()

def dock_hide(manager: QtAds.CDockManager, d: QtAds.CDockWidget):
    dock_remove_from_gui(manager, d)

def dock_ensure_visible(manager: QtAds.CDockManager, d: QtAds.CDockWidget):
    """Makes sure a dock is visible"""
    print("showing {d}")
    if d.isVisible():
        return # already visible

    if d not in get_all_active_docks(manager):
        d.toggleViewAction().trigger()

    if d.isClosed():
        d.toggleViewAction().trigger()

    if d.isVisible():
        return

    manager.setDockWidgetFocused(d)
    d.update()


