from DAVE.gui.dock_system.dockwidget import *
import PySide6
from PySide6.QtGui import QStandardItemModel, QIcon, QColor, QBrush
from PySide6.QtCore import QMimeData, Qt, QPoint
from PySide6.QtWidgets import (
    QTreeWidgetItem,
    QCheckBox,
    QApplication,
    QMenu,
    QMainWindow,
)
import DAVE.scene as ds
from DAVE.gui.widget_nodetree import HasNodeTreeMixin
from DAVE.settings_visuals import ICONS


class EnterKeyPressFilter(PySide6.QtCore.QObject):
    def eventFilter(self, obj, event):
        if isinstance(event, PySide6.QtGui.QKeyEvent):
            if event.key() == Qt.Key_Return:
                self.callback(obj, event)
                event.setAccepted(True)
                return True

        return False


class WidgetTags(guiDockWidget, HasNodeTreeMixin):
    def guiCreate(self):
        HasNodeTreeMixin.init(self)

        self.treeView = QtWidgets.QTreeWidget(self.contents)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView.setRootIsDecorated(True)
        self.treeView.setExpandsOnDoubleClick(False)
        self.treeView.setObjectName("treeView")

        header = self.treeView.header()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self.header_clicked)

        self.treeView.setAlternatingRowColors(True)

        self.checkbox = QCheckBox(self.contents)
        self.checkbox.setText("show all managed nodes")
        self.checkbox.setChecked(False)
        self.checkbox.toggled.connect(self.update_node_data_and_tree)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.treeView)
        layout.addWidget(self.checkbox)
        self.contents.setLayout(layout)

        self.resize(800, 800)

    def guiDefaultLocation(self):
        return None

    def guiProcessEvent(self, event):
        if event in [
            guiEventType.MODEL_STRUCTURE_CHANGED,
            guiEventType.FULL_UPDATE,
        ]:
            self.update_node_data_and_tree()

    def checkbox_toggeled(self):
        """Update the tags for the selected node"""
        item = self.treeView.selectedItems()[0]
        node = self.guiScene[item.toolTip(0)]  # name stored in tooltip
        # walk the columns
        tags = self.guiScene.tags

        code = None
        for i, tag in enumerate(tags):
            cb = self.treeView.itemWidget(item, i + 2)
            has = node.has_tag(tag)
            need = cb.isChecked()

            if has and not need:
                code = f"s['{node.name}'].delete_tag('{tag}')"
                break
            if need and not has:
                code = f"s['{node.name}'].add_tag('{tag}')"
                break

        if code is None:
            raise ValueError("Event called but nothing to update")

        self.guiRunCodeCallback(code, guiEventType.TAGS_CHANGED)

        # change the columns if last tag is removed
        if len(tags) != len(self.guiScene.tags):
            self.update_node_data_and_tree()

    def make_tree_item(self, node):
        text = node.name
        item = QTreeWidgetItem()
        item.setText(0, text)
        item.setToolTip(0, node.name)  # set tooltip to node name
        return item

    def update_node_data_and_tree(self):
        """
        Updates the tree and assembles the node-data

        This data is obtained from scene.nodes

        """

        HasNodeTreeMixin.update_node_data_and_tree(self)

        tags = self.guiScene.tags
        self.treeView.setColumnCount(len(tags) + 1)
        self.treeView.setHeaderLabels(["Node", "Add tag ", *tags])
        self.treeView.header().setVisible(True)

        for name, item in self.items.items():
            node = self.guiScene[name]
            for i, tag in enumerate(tags):
                cbx = QtWidgets.QCheckBox()
                cbx.setChecked(node.has_tag(tag))
                cbx.toggled.connect(self.checkbox_toggeled)
                self.treeView.setItemWidget(item, 2 + i, cbx)

            # add new-tag textbox
            edb = QtWidgets.QLineEdit()
            edb.setFrame(False)
            edb.setFixedWidth(110)
            edb.setToolTip("Press enter to accept")
            edb.setPlaceholderText("new tag")
            edb.returnPressed.connect(
                lambda sender=edb, node_name=node.name: self.tag_added(
                    sender, node_name
                )
            )
            self.treeView.setItemWidget(item, 1, edb)

        header = self.treeView.header()

        for i in range(len(tags)):
            header.setSectionResizeMode(
                i + 1, QtWidgets.QHeaderView.ResizeToContents
            )  # https://doc.qt.io/qt-5/qheaderview.html#details

    def tag_added(self, sender, node_name):
        tag = sender.text()
        self.guiRunCodeCallback(
            f"s['{node_name}'].add_tag('{tag}')", guiEventType.NOTHING
        )
        self.update_node_data_and_tree()

    def header_clicked(self, col):
        header = self.treeView.header()
        x = header.sectionPosition(col)

        if col < 2:
            return

        tag = self.guiScene.tags[col - 2]

        pos = self.treeView.mapToGlobal(QPoint(x, 5))

        def delete():
            self.guiRunCodeCallback(f"s.delete_tag('{tag}')", guiEventType.NOTHING)
            self.update_node_data_and_tree()

        menu = QMenu()
        menu.addAction(f"Delete {tag} tag", delete)
        menu.addAction("Cancel")
        menu.exec_(pos)


if __name__ == "__main__":
    app = QApplication()

    m = QMainWindow()

    s = Scene()
    p = s.new_point("point")
    a = s.new_frame("Frame")
    p = s.new_point("point2", parent=a)
    p.add_tags(("demo", "tag2"))

    widget = WidgetTags()

    def run_code(code, void):
        print(code)
        exec(code)

    widget.guiScene = s
    widget.guiRunCodeCallback = run_code

    widget.guiProcessEvent(guiEventType.FULL_UPDATE)

    m.addDockWidget(PySide6.QtCore.Qt.LeftDockWidgetArea, widget)

    m.show()

    print("showing")

    app.exec_()
