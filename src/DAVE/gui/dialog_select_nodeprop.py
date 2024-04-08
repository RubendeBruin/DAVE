from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QApplication, QDialogButtonBox
from DAVE.gui.forms.dlg_node_prop_select import Ui_Dialog

from DAVE.scene import Scene

class SelectNodePropDialog(QDialog):
    def __init__(self, parent, scene : Scene, node : str = "",
                 prop : str = "",
                 settable = None,
                 single_settable = None,
                 single_numeric = True):
        QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

        self.scene = scene
        self.node_class = None


        self.settable = settable
        self.single_settable = single_settable
        self.single_numeric = single_numeric

        # fill the lists
        self.ui.lwNodes.addItems(self.scene.node_names)
        self.ui.lwNodes.itemSelectionChanged.connect(self.node_selected)
        self.ui.lwProperties.itemSelectionChanged.connect(self.prop_selected)


        if node:
            # get list
            items = self.ui.lwNodes.findItems(node, Qt.MatchExactly)
            if items:
                item = items[0]
                item.setSelected(True)
                self.ui.lwNodes.scrollToItem(item)

                self.node_selected()

        if prop:
            # get list
            items = self.ui.lwProperties.findItems(prop, Qt.MatchExactly)
            if items:
                item = items[0]
                item.setSelected(True)
                self.ui.lwProperties.scrollToItem(item)

    def node_selected(self, *args):
        if not self.ui.lwNodes.selectedItems():
            return
        item = self.ui.lwNodes.selectedItems()[0]

        self.node = self.scene[item.text()]
        self.ui.lbSelectedNode.setText(self.node.name)
        node_class = self.node.__class__

        if node_class != self.node_class:
            # re-fill
            props = self.scene.give_properties_for_node(self.node,
                                                settable=self.settable, single_settable=self.single_settable, single_numeric=self.single_numeric)

            self.node_class = node_class

            self.ui.lwProperties.clear()
            self.ui.lwProperties.addItems(props)

    def prop_selected(self, *args):
        if not self.ui.lwProperties.selectedItems():
            return

        item = self.ui.lwProperties.selectedItems()[0]
        self.prop = item.text()

        self.new_selection()

    def new_selection(self):

        self.ui.lbSelectedProperty.setText(self.prop)
        doc = self.scene.give_documentation(self.node, self.prop)
        self.ui.ptDoc.setPlainText(doc.doc_long)

        value = getattr(self.node, self.prop, '')
        self.ui.lbValue.setText(str(value))

        # enable OK button
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)



if __name__ == '__main__':

    from DAVE import *

    app = QApplication.instance()
    s = Scene()
    s.import_scene("res: cheetah.DAVE")
    ex = SelectNodePropDialog(None, s, node="Cheetah", prop="tilt_x")
    result = ex.exec()

    if result:
        print(ex.node.name, ex.prop)


    print(result)