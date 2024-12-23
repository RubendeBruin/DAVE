from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QComboBox,
    QHBoxLayout,
    QToolButton,
    QGridLayout,
    QLabel,
)

from DAVE.gui.helpers.my_qt_helpers import update_combobox_items_with_completer

"""
Call Initialize after creation

callback is called when a new node is selected
register_func is called with self as argument to register this widget as handler for selection events
call unregister to remove registration

call NodesSelected() when a node is selected. Will return True if the selection in handled (false otherwise)
setValue / value to get/set the value

Suggested implementation:

- make a "generate code" function and set callback to that
- assign register_func to NodeEditor.node_picker_register_func
- update .node, and .scene whenever needed

"""


class QNodePicker(QWidget):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.layout = QGridLayout()
        self.dropdown = QComboBox()
        self.dropdown.setEditable(True)
        self.dropdown.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self.button = QToolButton()
        self.button.setIcon(QIcon(":/icons/cross.png"))
        self.button.setAutoRaise(True)
        self.button.setCheckable(True)

        self.layout.addWidget(self.dropdown, 0, 0)
        self.layout.addWidget(self.button, 0, 1)

        self.label = QLabel("Select node in tree or view to continue")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { background : orange; }")
        self.layout.addWidget(self.label, 1, 0, 1, 2)
        self.label.setVisible(False)

        self.setLayout(self.layout)

        self.dropdown.currentTextChanged.connect(self.valueChanged)
        self.button.clicked.connect(self.pick_clicked)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.picking = False

    def initialize(self, scene, nodetypes, callback, register_func, NoneAllowed, node):
        """Convenience function for setting all required properties"""
        self.scene = scene
        self.nodetypes = nodetypes
        self.callback = callback
        self.register_func = register_func
        self.NoneAllowed = NoneAllowed
        self.node = node

    def fill(self, property_name="parent"):
        """Use 'keep' as property-name to try to maintain the old value"""

        old_value = self.value
        nodes = self.scene.nodes_of_type(self.nodetypes)

        # exclude self
        if self.node is None:
            names = [node.name for node in nodes]
        else:
            names = [node.name for node in nodes if node.name != self.node.name]

        if self.NoneAllowed:
            names.insert(0, "")
        update_combobox_items_with_completer(self.dropdown, names)

        if property_name == "keep" and old_value in names:
            self.setValue(old_value)

        else:
            prop_node = getattr(self.node, property_name, None)

            if prop_node is None:
                self.setValue("")
            else:
                self.setValue(prop_node.name)

    def setValue(self, value):
        self.dropdown.blockSignals(True)
        self.dropdown.setCurrentText(value)
        self.dropdown.blockSignals(False)

    @property
    def value(self):
        return self.dropdown.currentText()

    def valueChanged(self):
        if self.callback is not None:
            if self.value == "":
                self.callback()
            else:
                try:
                    node = self.scene[self.value]
                except:
                    return

                if isinstance(node, self.nodetypes):
                    self.callback()

    def pick_clicked(self):

        if self.picking:
            self.unregister()
        else:
            self.picking = True
            self.register_func(self)
            self.button.setChecked(True)
            self.label.setVisible(True)

    def nodesSelected(self, nodes):
        for node in nodes:
            if isinstance(node, self.nodetypes):
                name = node.name
                if self.value != name:
                    self.dropdown.setCurrentText(name)
                self.unregister()
                return True
        return False

    def unregister(self):
        self.button.setChecked(False)
        self.picking = False
        self.label.setVisible(False)
