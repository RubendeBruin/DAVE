from DAVE.gui.dockwidget import *
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon, QDrag, QColor
from PySide2.QtCore import QMimeData, Qt, QItemSelectionModel
from PySide2.QtWidgets import (
    QTreeWidgetItem,
    QCheckBox,
    QListWidget,
    QAbstractScrollArea, QApplication,
)
import DAVE.scene as ds
from DAVE.gui.helpers.my_qt_helpers import DeleteEventFilter

from DAVE.settings_visuals import ICONS


class NodeTreeWidget(QtWidgets.QTreeWidget):

    others = []

    def dragEnterEvent(self, event):
        if event.source() not in [self, *self.others]:
            # print("Not accepting external data")
            event.setDropAction(Qt.IgnoreAction)
            return
        else:
            event.accept()

    def dragMoveEvent(self, event):
        if event.source() not in [self, *self.others]:
            # print("Not accepting external data")
            event.setDropAction(Qt.IgnoreAction)
            return
        else:
            event.accept()

    def dropEvent(self, event):
        if event.source() not in [self, *self.others]:
            # print("Not accepting external data")
            event.setDropAction(Qt.IgnoreAction)
            return

        dragged_name = event.mimeData().text()

        # dropped onto
        point = event.pos()
        drop_onto = self.itemAt(point)

        if drop_onto is None:
            drop_onto_name = None
        else:
            drop_onto_name = drop_onto.toolTip(0)

        # print("dragged {} onto {}".format(dragged_name, drop_onto_name))
        event.setDropAction(Qt.IgnoreAction)

        self.parentcallback(dragged_name, drop_onto_name, event)

    def startDrag(self, supportedActions):

        dragged = self.selectedItems()[0]

        node_name = dragged.toolTip(0)
        node = self.guiScene[node_name]

        if (
            node._manager
        ):  # managed nodes can not be dragged, except points and circles and contact-meshes
            if not isinstance(node, (Circle, Point, ContactMesh)):
                return

        mimeData = QMimeData()
        mimeData.setText(node_name)

        drag = QDrag(self)
        drag.setMimeData(mimeData)

        drag.exec_(supportedActions=supportedActions) # , defaultAction=Qt.MoveAction)


class WidgetNodeTree(guiDockWidget):
    def guiCreate(self):

        self.treeView = NodeTreeWidget(self.contents)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView.setRootIsDecorated(True)
        self.treeView.setExpandsOnDoubleClick(False)
        self.treeView.setObjectName("treeView")
        self.treeView.setColumnCount(1)
        self.treeView.header().setVisible(False)
        self.treeView.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.treeView.activated.connect(
            self.tree_select_node
        )  # fires when a user presses [enter]
        self.treeView.doubleClicked.connect(self.tree_select_node)
        self.treeView.itemClicked.connect(self.item_clicked)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.rightClickTreeview)

        self.treeView.parentcallback = self.dragDropCallback

        self.checkbox = QCheckBox(self.contents)
        self.checkbox.setText("show all managed nodes")
        self.checkbox.setChecked(False)
        self.checkbox.toggled.connect(self.update_node_data_and_tree)

        self.listbox = QListWidget(self.contents)
        self.listbox.addItem("test")
        itemheight = self.listbox.sizeHintForRow(0)
        self.listbox.clear()
        self.listbox.setFixedHeight(4 * itemheight)
        self.listbox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listbox.setEditTriggers(QListWidget.NoEditTriggers)
        self.listbox.setDragEnabled(True)
        self.listbox.startDrag = self.listview_startDrag

        self.treeView.others.append(self.listbox)
        self.treeView.others.append(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.treeView)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.listbox)
        self.contents.setLayout(layout)

        self.recent_items = list()

        self.delete_eventFilter = DeleteEventFilter()
        self.delete_eventFilter.callback = self.delete_key
        self.installEventFilter(self.delete_eventFilter)

    def guiProcessEvent(self, event):
        if event in [
            guiEventType.MODEL_STRUCTURE_CHANGED,
            guiEventType.FULL_UPDATE,
            guiEventType.MODEL_STEP_ACTIVATED,
            guiEventType.SELECTED_NODE_MODIFIED,
        ]:
            self.update_node_data_and_tree()
            self.update_node_visibility()
            self._remove_removed_nodes_from_recent()
            self.update_listview()

        if event in [guiEventType.VIEWER_SETTINGS_UPDATE]:
            self.update_node_visibility()

        if event in [guiEventType.SELECTION_CHANGED]:
            self.update_selection()

    # ======= custom

    def delete_key(self):
        self.gui.delete_key()

    def dragDropCallback(self, drop, onto, event):

        keep_local_position = (event.keyboardModifiers() == Qt.ControlModifier)

        if onto is None:
            if keep_local_position:
                code = "s['{}'].parent = None".format(drop)
            else:
                code = "s['{}'].change_parent_to(None)".format(drop)
            self.guiRunCodeCallback(code, guiEventType.MODEL_STRUCTURE_CHANGED)

        else:

            node_drop = self.guiScene[drop]
            node_onto = self.guiScene[onto]

            # Sheave --> Sheave : create geometric contact
            if isinstance(node_drop, ds.Circle) and isinstance(node_onto, ds.Circle):
                code = f"s.new_geometriccontact('Geometric_connection of :{drop} on {onto}','{drop}','{onto}')"

            # Sheave --> GeometricContact : set child of geometric contact
            elif isinstance(node_drop, ds.Circle) and isinstance(
                node_onto, ds.GeometricContact
            ):
                code = f"s['{node_onto.name}'].child = '{node_drop.name}'"

            # GeometricContact --> Sheave : set parent of geometric contact
            elif isinstance(node_drop, ds.GeometricContact) and isinstance(
                node_onto, ds.Circle
            ):
                code = f"s['{node_drop.name}'].parent = '{node_onto.name}'"

            # Default
            else:
                if keep_local_position:
                    code = "s['{}'].parent = s['{}']".format(drop, onto)
                else:
                    code = "s['{}'].change_parent_to(s['{}'])".format(drop, onto)

            self.guiRunCodeCallback(code, guiEventType.MODEL_STRUCTURE_CHANGED)

    def tree_select_node(self, index):
        if index.column() == 0:
            node_name = index.data()
            self.guiSelectNode(node_name)

    def item_clicked(self, data):
        name = data.toolTip(0)
        self.guiSelectNode(name)

    def rightClickTreeview(self, point):
        if self.treeView.selectedItems():
            node_name = self.treeView.selectedItems()[0].toolTip(0)
        else:
            node_name = None
        globLoc = self.treeView.mapToGlobal(point)
        self.gui.openContextMenyAt(node_name, globLoc)

    def update_selection(self):

        selected_names = [node.name for node in self.guiSelection]
        for name in self.items.keys():

            if name in selected_names:
                self.items[name].setSelected(True)
                self.treeView.scrollToItem(self.items[name])
            else:
                self.items[name].setSelected(False)

        # update recent items
        self._remove_removed_nodes_from_recent()

        if len(self.guiSelection) > 4:
            self.recent_items = self.guiSelection[-4:]
        else:
            self.recent_items.extend(self.guiSelection)
            self.recent_items = remove_duplicates_from_list_keep_order(
                self.recent_items
            )
            self.recent_items = self.recent_items[-4:]

        self.update_listview()

    def _remove_removed_nodes_from_recent(self):
        """Removes items from recent-view if they do no longer exist in the scene"""
        new_recent = []
        for node in self.recent_items:
            if node in self.guiScene._nodes:
                new_recent.append(node)
        self.recent_items = new_recent

    def update_listview(self):
        self.listbox.clear()
        self.listbox.addItems([node.name for node in self.recent_items])


    def update_node_visibility(self):
        """Updates the visibility of the nodes in the tree"""
        for name, item in self.items.items():

            # item not visible? then mark gray
            node = self.guiScene[name]
            if not node.visible:
                item.setTextColor(0, QColor(124, 124, 124))
            elif node.manager is not None:
                item.setTextColor(0, QColor(0, 150, 0))
            else:
                item.setTextColor(0, QColor(0, 0, 0))

    def update_node_data_and_tree(self):
        """
        Updates the tree and assembles the node-data

        This data is obtained from scene.nodes and assumes that
        each of the nodes has a visual assigned to it.

        """

        self.items = dict()

        # # store the open/closed state of the current tree - based on Name
        closed_items = []

        def walk_node(item, store_here):
            for i in range(item.childCount()):
                child = item.child(i)
                if child.childCount() > 0:
                    if not child.isExpanded():
                        store_here.append(child.toolTip(0))
                    walk_node(child, store_here)

        walk_node(self.treeView.invisibleRootItem(), closed_items)

        self.guiScene.sort_nodes_by_parent()

        # store the current scroll position
        vertical_position = self.treeView.verticalScrollBar().sliderPosition()


        self.treeView.clear()
        self.treeView.guiScene = self.guiScene

        show_managed_nodes = self.checkbox.isChecked()

        for node in self.guiScene._nodes:

            # create a tree item
            text = node.name
            item = QTreeWidgetItem()

            item.setToolTip(0, text) # store the name in the tool-tip

            # shorten the name if it contains /-es

            item.setText(0, text.split('/')[-1])

            # if we have a parent, then put the items under the parent,
            # else put it under the root

            if type(node) in ICONS:
                item.setIcon(0,ICONS[type(node)])
            else:

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
                elif isinstance(node, ds.SPMT):
                    item.setIcon(0, QIcon(":/icons/spmt.png"))


            try:
                parent = node.parent
            except:
                parent = None

            # node is managed by a manager
            show_managed_node = show_managed_nodes

            # custom work-around for showing the "out-frame" for managed geometric connectors
            if isinstance(node._manager, GeometricContact):
                if node == node._manager._child_circle_parent_parent:
                    if node._manager.manager is None: # but only if the manager itself is not also managed (and thus hidden)
                        show_managed_node = True

            if not show_managed_node: # another override
                if hasattr(node, '_always_show_in_tree'):
                    show_managed_node = node._always_show_in_tree

            # custom work-around for showing the "circles" for managed shackles
            if isinstance(node._manager, Shackle):
                if (
                    node == node._manager.pin
                    or node == node._manager.bow
                    or node == node._manager.inside
                ):
                    if node._manager.manager is None: # but only if the manager itself is not also managed (and thus hidden)
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

        # self.treeView.resizeColumnToContents(0)
        self.treeView.expandAll()

        # restore closed nodes state
        def close_nodes(item, closed):
            for i in range(item.childCount()):
                child = item.child(i)
                if child.toolTip(0) in closed_items:
                    child.setExpanded(False)
                if child.childCount() > 0:
                    close_nodes(child, closed)

        close_nodes(self.treeView.invisibleRootItem(), closed_items)

        # restore vertical position
        self.treeView.verticalScrollBar().setSliderPosition(vertical_position)

    def listview_startDrag(self, supportedActions):

        dragged = self.listbox.selectedItems()[0]

        node_name = dragged.text()
        node = self.guiScene[node_name]

        if (
            node._manager
        ):  # managed nodes can not be dragged, except points and circles and contact-meshes
            if not isinstance(node, (Circle, Point, ContactMesh)):
                return

        mimeData = QMimeData()
        mimeData.setText(node_name)

        drag = QDrag(self)
        drag.setMimeData(mimeData)

        drag.exec_(supportedActions=supportedActions)
