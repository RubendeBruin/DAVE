from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QComboBox, QHBoxLayout, QToolButton

from DAVE.gui.helpers.my_qt_helpers import update_combobox_items_with_completer

"""
Call Initialize after creation

callback is called when a new node is selected
register is called with self as argument to register this widget as handler for selection events
call unregister to remove registration

call NodesSelected() when a node is selected. Will return True if the selection in handled (false otherwise)
setValue / value to get/set the value


"""


class QNodePicker(QWidget):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.layout = QHBoxLayout()
        self.dropdown = QComboBox()
        self.dropdown.setEditable(True)
        self.button = QToolButton()
        self.button.setIcon(QIcon(":/icons/cross.png"))
        self.button.setAutoRaise(True)
        self.button.setCheckable(True)

        self.layout.addWidget(self.dropdown)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.dropdown.currentTextChanged.connect(self.valueChanged)
        self.button.clicked.connect(self.pick_clicked)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

    def initialize(self, scene, nodetypes, callback, register_func, NoneAllowed, node):
        self.scene = scene
        self.nodetypes = nodetypes
        self.callback = callback
        self.register_func = register_func
        self.NoneAllowed = NoneAllowed
        self.node = node

    def fill(self):
        nodes = self.scene.nodes_of_type(self.nodetypes)
        names = [node.name for node in nodes if node.name != self.node.name]
        if self.NoneAllowed:
            names.insert(0,'')
        update_combobox_items_with_completer(self.dropdown, names)

        if self.node.parent is None:
            self.setValue('')
        else:
            self.setValue(self.node.parent.name)

    def setValue(self, value):
        self.dropdown.blockSignals(True)
        self.dropdown.setCurrentText(value)
        self.dropdown.blockSignals(False)

    @property
    def value(self):
        return self.dropdown.currentText()

    def valueChanged(self):

        if self.value == '':
            self.callback()
        else:
            try:
                node = self.scene[self.value]
            except:
                return

            if isinstance(node, self.nodetypes):
                self.callback()

    def pick_clicked(self):
        self.register_func(self)
        self.button.setChecked(True)

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




