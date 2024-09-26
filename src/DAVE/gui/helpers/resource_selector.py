from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QComboBox,
    QHBoxLayout,
    QToolButton,
    QGridLayout,
    QLabel,
    QApplication,
    QMainWindow, QMenu,
)

from DAVE.gui.helpers.gui_logger import DAVE_GUI_LOGGER
from DAVE.gui.helpers.my_qt_helpers import update_combobox_items_with_completer
from DAVE.gui.thumbnailer.resource_browser import ResourceBrowserDialog

"""
Displays a combobox with a button to select a resource for the node.

Needs:
- Scene for resource provider
- Allowable resource type
- Callback to call when resource is selected

Usage:
- Call Initialize after creation
- callback is called when a new resource is selected
- set_current is called when a new resource is selected from the outside (for example when the node is changed)

"""


class QResourceSelector(QWidget):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.dialog_buffer = (
            dict()
        )  # buffer for dialog instances, keys are the resource types

        self.layout = QGridLayout()
        self.dropdown = QComboBox()
        self.dropdown.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self.dropdown.setEditable(True)
        self.button = QToolButton()
        self.button.setIcon(QIcon(":/v2/icons/open.svg"))

        # button on the left
        self.layout.addWidget(self.button, 0, 0)
        self.layout.addWidget(self.dropdown, 0, 1)

        self.setLayout(self.layout)

        self.dropdown.currentTextChanged.connect(self.valueChanged)
        self.button.clicked.connect(self.open_browser)

        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # assign action to right-click on the dropdown or button
        self.dropdown.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dropdown.customContextMenuRequested.connect(self.context_menu)

        self.button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.button.customContextMenuRequested.connect(self.context_menu)

        self.resources = []
        self.callback_reload = None # callback to reload the current resource (to be assigned by the user, optional)

    def initialize(self, scene, resource_types, callback):
        """Convenience function for setting all required properties"""
        self.scene = scene
        self.resource_provider = scene.resource_provider
        self.resource_types = resource_types
        self.callback = callback

        DAVE_GUI_LOGGER.log(
            "Resource Selector initialized with types: " + str(resource_types)
        )

        self.update_resource_list()

    def update_resource_list(self):

        self.resources = []

        # scan res including subdirs
        self.resources.extend(
            self.resource_provider.get_resource_list(
                extension=self.resource_types,
                include_subdirs=True,
                include_current_dir=False,
            )
        )

        # scan cd excluding subdirs
        self.resources.extend(
            self.resource_provider.get_resource_list(
                extension=self.resource_types,
                include_subdirs=False,
                include_current_dir=True,
            )
        )

        update_combobox_items_with_completer(self.dropdown, self.resources)

    def reload_current_resource(self):
        if self.callback_reload is not None:
            self.callback_reload()

    def context_menu(self, pos):
        if self.callback_reload is None:
            return

        menu = QMenu()
        menu.addAction("Reload current resource", self.reload_current_resource)

        menu.exec(self.dropdown.mapToGlobal(pos))

    def setValue(self, value):
        self.dropdown.blockSignals(True)
        self.dropdown.setCurrentText(value)

        self._check_value()

        self.dropdown.blockSignals(False)

    @property
    def value(self):
        return self.dropdown.currentText()

    def _check_value(self):
        # try to get resource
        try:
            self.scene.resource_provider.get_resource_path(self.value, no_gui=True)
        except FileNotFoundError:
            self.dropdown.setStyleSheet("background-color: orange")
            return False

        self.dropdown.setStyleSheet("")
        return True

    def valueChanged(self):
        if self._check_value():
            if self.callback is not None:
                self.callback()

    def open_browser(self):

        # we want to re-use the dialog as much as possible to avoid delays.
        # but the resource selector is a singleton instance, so it may be
        # re-used for different resource types.

        key = ";".join(self.resource_types)

        if key not in self.dialog_buffer:
            self.dialog_buffer[key] = ResourceBrowserDialog(
                self.scene, self.resource_types
            )

        dialog = self.dialog_buffer[key]  # alias

        if dialog.open_dialog():
            if dialog.selected_file != self.value:
                self.setValue(dialog.selected_file)
                self.valueChanged()


if __name__ == "__main__":
    from DAVE import *

    app = QApplication.instance() or QApplication([])
    win = QMainWindow()
    win.show()
    scene = Scene()

    selector = QResourceSelector(win)
    selector.initialize(scene, [".obj"], lambda x: print(x))
    selector.setValue("res: cube2.obj")
    selector.callback_reload = lambda: print("reloading")

    win.setCentralWidget(selector)
    app.exec()
