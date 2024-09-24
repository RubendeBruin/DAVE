from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QComboBox, QHBoxLayout, QToolButton, QGridLayout, QLabel, QApplication, \
    QMainWindow

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

        self.dialog = None

        self.layout = QGridLayout()
        self.dropdown = QComboBox()
        self.dropdown.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.dropdown.setEditable(True)
        self.button = QToolButton()
        self.button.setIcon(QIcon(":/v2/icons/open.svg"))

        # button on the left
        self.layout.addWidget(self.button,0,0)
        self.layout.addWidget(self.dropdown,0,1)

        self.setLayout(self.layout)

        self.dropdown.currentTextChanged.connect(self.valueChanged)
        self.button.clicked.connect(self.open_browser)

        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)

        self.resources = []


    def initialize(self, scene, resource_types, callback):
        """Convenience function for setting all required properties"""
        self.scene = scene
        self.resource_provider = scene.resource_provider
        self.resource_types = resource_types
        self.callback = callback

        self.update_resource_list()


    def update_resource_list(self):

        self.resources = []

        # scan res including subdirs
        self.resources.extend(
            self.resource_provider.get_resource_list(extension=self.resource_types, include_subdirs=True,
                                                     include_current_dir=False))

        # scan cd excluding subdirs
        self.resources.extend(
            self.resource_provider.get_resource_list(extension=self.resource_types, include_subdirs=False,
                                                     include_current_dir=True))

        update_combobox_items_with_completer(self.dropdown, self.resources)



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
        if self.dialog is None:
            self.dialog = ResourceBrowserDialog(self.scene, self.resource_types)
        if self.dialog.open_dialog():
            if self.dialog.selected_file != self.value:
                self.setValue(self.dialog.selected_file)
                self.valueChanged()


    def pick_clicked(self):
        pass

if __name__ == '__main__':
    from DAVE import *

    app = QApplication.instance() or QApplication([])
    win = QMainWindow()
    win.show()
    scene = Scene()

    selector = QResourceSelector(win)
    selector.initialize(scene, ['.obj'], lambda x: print(x))
    selector.setValue('res: cube2.obj')

    win.setCentralWidget(selector)
    app.exec()



