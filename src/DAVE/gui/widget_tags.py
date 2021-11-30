from DAVE.gui.dockwidget import *
import PySide2
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon, QDrag, QColor
from PySide2.QtCore import QMimeData, Qt, QItemSelectionModel, QPoint
from PySide2.QtWidgets import (
    QTreeWidgetItem,
    QCheckBox,
    QListWidget,
    QAbstractScrollArea, QApplication, QMenu, QMainWindow,
)
import DAVE.scene as ds
from DAVE.gui.helpers.my_qt_helpers import EnterKeyPressFilter

class EnterKeyPressFilter(PySide2.QtCore.QObject):

    def eventFilter(self, obj, event):
        if isinstance(event, PySide2.QtGui.QKeyEvent):
            if (event.key() == Qt.Key_Return):
                self.callback(obj, event)
                event.setAccepted(True)
                return True

        return False


class WidgetTags(guiDockWidget):
    def guiCreate(self):

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

        self.resize(800,800)

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
        node = self.guiScene[item.text(0)]
        # walk the columns
        tags = self.guiScene.tags

        code = None
        for i,tag in enumerate(tags):
            cb = self.treeView.itemWidget(item, i+2)
            has = node.has_tag(tag)
            need = cb.isChecked()

            if has and not need:
                code = f"s['{node.name}'].delete_tag('{tag}')"
                break
            if need and not has:
                code = f"s['{node.name}'].add_tag('{tag}')"
                break

        if code is None:
            raise ValueError('Event called but nothing to update')

        self.guiRunCodeCallback(code, guiEventType.TAGS_CHANGED)

        # change the columns if last tag is removed
        if len(tags) != len(self.guiScene.tags):
            self.update_node_data_and_tree()



    def update_node_data_and_tree(self):
        """
        Updates the tree and assembles the node-data

        This data is obtained from scene.nodes

        """

        self.items = dict()

        # # store the open/closed state of the current tree - based on Name
        closed_items = []

        def walk_node(item, store_here):
            for i in range(item.childCount()):
                child = item.child(i)
                if child.childCount() > 0:
                    if not child.isExpanded():
                        store_here.append(child.text(0))
                    walk_node(child, store_here)

        walk_node(self.treeView.invisibleRootItem(), closed_items)

        self.guiScene.sort_nodes_by_parent()

        # store the current scroll position
        vertical_position = self.treeView.verticalScrollBar().sliderPosition()


        self.treeView.clear()


        tags = self.guiScene.tags
        self.treeView.setColumnCount(len(tags)+1)
        self.treeView.setHeaderLabels(['Node','Add tag ', *tags])
        self.treeView.header().setVisible(True)

        show_managed_nodes = self.checkbox.isChecked()

        for node in self.guiScene._nodes:

            # create a tree item
            text = node.name
            item = QTreeWidgetItem()
            item.setText(0, text)

            # if we have a parent, then put the items under the parent,
            # else put it under the root

            item.setIcon(0, QIcon(":/icons/redball.png"))
            if isinstance(node, ds.Component):
                item.setIcon(0, QIcon(":/icons/component.png"))
            elif isinstance(node, ds.RigidBody):
                item.setIcon(0, QIcon(":/icons/cube.png"))
            elif isinstance(node, ds.Frame):
                item.setIcon(0, QIcon(":/icons/axis_blue.png"))
            elif isinstance(node, ds.Point):
                item.setIcon(0, QIcon(":/icons/point_blue.png"))
            elif isinstance(node, ds.Cable):
                item.setIcon(0, QIcon(":/icons/cable.png"))
            elif isinstance(node, ds.Visual):
                item.setIcon(0, QIcon(":/icons/visual.png"))
            elif isinstance(node, ds.LC6d):
                item.setIcon(0, QIcon(":/icons/lincon6.png"))
            elif isinstance(node, ds.Connector2d):
                item.setIcon(0, QIcon(":/icons/con2d.png"))
            elif isinstance(node, ds.Beam):
                item.setIcon(0, QIcon(":/icons/beam.png"))
            elif isinstance(node, ds.HydSpring):
                item.setIcon(0, QIcon(":/icons/linhyd.png"))
            elif isinstance(node, ds.Force):
                item.setIcon(0, QIcon(":/icons/force.png"))
            elif isinstance(node, ds.Circle):
                item.setIcon(0, QIcon(":/icons/circle_blue.png"))
            elif isinstance(node, ds.Buoyancy):
                item.setIcon(0, QIcon(":/icons/trimesh.png"))
            elif isinstance(node, ds.WaveInteraction1):
                item.setIcon(0, QIcon(":/icons/waveinteraction.png"))
            elif isinstance(node, ds.ContactBall):
                item.setIcon(0, QIcon(":/icons/contactball.png"))
            elif isinstance(node, ds.ContactMesh):
                item.setIcon(0, QIcon(":/icons/contactmesh.png"))
            elif isinstance(node, ds.GeometricContact):
                item.setIcon(0, QIcon(":/icons/pin_hole.png"))
            elif isinstance(node, ds.Sling):
                item.setIcon(0, QIcon(":/icons/sling.png"))
            elif isinstance(node, ds.Tank):
                item.setIcon(0, QIcon(":/icons/tank.png"))
            elif isinstance(node, ds.WindArea):
                item.setIcon(0, QIcon(":/icons/wind.png"))
            elif isinstance(node, ds.CurrentArea):
                item.setIcon(0, QIcon(":/icons/current.png"))



            try:
                parent = node.parent
            except:
                parent = None

            # node is managed by a manager
            show_managed_node = show_managed_nodes

            # custom work-around for showing the "out-frame" for managed geometric connectors
            if isinstance(node._manager, GeometricContact):
                if node == node._manager._child_circle_parent_parent:
                    show_managed_node = True

            # custom work-around for showing the "circles" for managed shackles
            if isinstance(node._manager, Shackle):
                if (
                    node == node._manager.pin
                    or node == node._manager.bow
                    or node == node._manager.inside
                ):
                    show_managed_node = True

            if node._manager:

                # are we showing managed nodes?
                if show_managed_node:

                    # item.setTextColor(0, Qt.gray)
                    item.setTextColor(0, QColor(0, 150, 0))

                    # if the item does not have a parent, then show it under the manager
                    if parent is None:
                        parent = node._manager

                    if parent.name not in self.items:
                        parent = node._manager

                    self.items[node.name] = item
                    self.items[parent.name].addChild(item)

            else:
                self.items[node.name] = item

                if parent is None:
                    self.treeView.invisibleRootItem().addChild(item)
                else:
                    if parent.name in self.items:
                        self.items[parent.name].addChild(item)
                    else:  # if the parent is not there, then it must be a managed node
                        self.items[parent._manager.name].addChild(item)

            for i,tag in enumerate(tags):
                cbx = QtWidgets.QCheckBox()
                cbx.setChecked(node.has_tag(tag))
                cbx.toggled.connect(self.checkbox_toggeled)
                self.treeView.setItemWidget(item, 2+i, cbx)

            # add new-tag textbox
            edb = QtWidgets.QLineEdit()
            edb.setFrame(False)
            edb.setFixedWidth(110)
            edb.setToolTip('Press enter to accept')
            edb.setPlaceholderText('new tag')
            edb.returnPressed.connect(lambda sender = edb, node_name = node.name : self.tag_added(sender, node_name))
            self.treeView.setItemWidget(item, 1, edb)

        header = self.treeView.header()

        for i in range(len(tags)):
            header.setSectionResizeMode(i+1, QtWidgets.QHeaderView.ResizeToContents) # https://doc.qt.io/qt-5/qheaderview.html#details



        self.treeView.expandAll()

        # restore closed nodes state
        def close_nodes(item, closed):
            for i in range(item.childCount()):
                child = item.child(i)
                if child.text(0) in closed_items:
                    child.setExpanded(False)
                if child.childCount() > 0:
                    close_nodes(child, closed)

        close_nodes(self.treeView.invisibleRootItem(), closed_items)

        # restore vertical position
        self.treeView.verticalScrollBar().setSliderPosition(vertical_position)

    def tag_added(self, sender, node_name):
        tag = sender.text()
        self.guiRunCodeCallback(f"s['{node_name}'].add_tag('{tag}')", guiEventType.NOTHING)
        self.update_node_data_and_tree()

    def header_clicked(self, col):
        header = self.treeView.header()
        x = header.sectionPosition(col)

        if col<2:
            return

        tag = self.guiScene.tags[col-2]

        pos = self.treeView.mapToGlobal(QPoint(x, 5))

        def delete():
            self.guiRunCodeCallback(f"s.delete_tag('{tag}')", guiEventType.NOTHING)
            self.update_node_data_and_tree()

        menu = QMenu()
        menu.addAction(f'Delete {tag} tag', delete)
        menu.addAction('Cancel')
        menu.exec_(pos)

if __name__ == '__main__':
    app = QApplication()

    m = QMainWindow()


    s = Scene()
    p = s.new_point("point")
    a = s.new_frame('Frame')
    p = s.new_point("point2", parent=a)
    p.add_tags(('demo','tag2'))

    widget = WidgetTags()

    def run_code(code, void):
        print(code)
        exec(code)

    widget.guiScene = s
    widget.guiRunCodeCallback = run_code

    widget.guiProcessEvent(guiEventType.FULL_UPDATE)

    m.addDockWidget(PySide2.QtCore.Qt.LeftDockWidgetArea, widget)

    m.show()

    print('showing')

    app.exec_()
