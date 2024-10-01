"""This is a gui to select a node and a single-valued numerical property"""
from PySide6.QtWidgets import QWidget, QGridLayout, QComboBox, QLabel

from DAVE import Scene, DG


class NodePropertySelectWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # node selector combobox
        self.node_selector = QComboBox()
        self.layout.addWidget(self.node_selector, 0, 0)

        # property selector combobox
        self.property_selector = QComboBox()
        self.layout.addWidget(self.property_selector, 0, 1)

        # feedback label
        self.feedback_label = QLabel()
        self.feedback_label.setWordWrap(True)
        self.layout.addWidget(self.feedback_label, 1, 0, 1, 2)

        self.node_selector.currentTextChanged.connect(self.update_properties)
        self.property_selector.currentTextChanged.connect(self.property_changed)

    def initialize(self, s : Scene, node: str or None = None, property: str or None = None):
        """Update the comboboxes with the nodes and properties of the scene"""
        self.scene = s

        self.node_selector.blockSignals(True)
        self.property_selector.blockSignals(True)

        self.node_selector.clear()
        self.property_selector.clear()

        self.node_selector.addItems(s.node_names)

        if node is None:
            self.node_selector.setCurrentIndex(0)
        else:
            self.node_selector.setCurrentText(node)

        self.update_properties()
        if property is not None:
            self.property_selector.setCurrentText(property)

        self.node_selector.blockSignals(False)
        self.property_selector.blockSignals(False)

        self.property_changed()


    def update_properties(self):
        currval = self.property_selector.currentText()

        node = self.scene[self.node_selector.currentText()]
        self.property_selector.clear()

        properties = self.scene.give_properties_for_node(node, single_numeric=True)

        self.property_selector.addItems(properties)

        if currval in properties:
            self.property_selector.setCurrentText(currval)
        else:
            self.property_selector.setCurrentIndex(0)

    def property_changed(self):
        node = self.node_selector.currentText()
        prop = self.property_selector.currentText()

        doc = self.scene.give_documentation(self.scene[node], prop)
        if doc is None:
            return

        text = doc.doc_long
        text += "\n\n"
        text += "Current value: " + str(getattr(self.scene[node],prop))
        text += "\nUnit : " + doc.units

        self.feedback_label.setText(text)

if __name__ == '__main__':
    s = Scene()

    s.import_scene("res: cheetah with crane.dave", containerize=False, prefix="")

    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    w = NodePropertySelectWidget()
    w._no_uc = True
    w.initialize(s, 'Cheetah', 'x')
    w.show()
    app.exec()


