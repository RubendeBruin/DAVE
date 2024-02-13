from DAVE import ContactMesh
from DAVE.gui.dock_system.dockwidget import *
from PySide6.QtGui import QIcon, QDrag, QColor, QBrush
from PySide6.QtCore import QMimeData, Qt
from PySide6.QtWidgets import (
    QTreeWidgetItem,
    QCheckBox,
    QListWidget,
)
import DAVE.scene as ds
from DAVE.gui.helpers.my_qt_helpers import (
    DeleteEventFilter,
    update_combobox_items_with_completer,
)
from DAVE.helpers.node_trees import give_parent_item
from DAVE.settings import DAVE_NODEPROP_INFO

from DAVE.settings_visuals import ICONS


class HasNodeTreeMixin:
    """Mixin used by both WidgetNodeTree and WidgetTags"""

    def init(self):
        self._current_tree = None
        self.items = dict()

        self.show_managed_nodes = False

    def make_tree_item(self, node):
        print("Shall return a QTreeWidgetItem for the given node")
        raise NotImplementedError

    def _update_needed(self):
        """Determines if an update is needed"""
        # lets first see if anything has changed
        # to quickly check that, we compare the current parents and managers with the ones from the last update
        # Node --> Parent node, manager node

        if self.show_managed_nodes != self.checkbox.isChecked():
            return True

        if self._current_tree is None:
            return True

        if len(self._current_tree) != len(self.guiScene._nodes):
            return True

        for node in self.guiScene._nodes:
            if node.name not in self._current_tree.keys():
                return True

        for node in self.guiScene._nodes:
            if self._current_tree[node.name] != (
                getattr(node, "parent", None),
                node.manager,
                type(node),
            ):
                print("structure changed")
                return True

        return False

    def update_node_data_and_tree(self):
        """
        Updates the tree and assembles the node-data

        This data is obtained from scene.nodes and assumes that
        each of the nodes has a visual assigned to it.

        """

        structure_changed = self._update_needed()

        if not structure_changed:
            # we may still need to update the labels
            for node in self.guiScene._nodes:
                if (
                    node.name in self.items
                ):  # check if visible; twice as fast as try-except
                    item = self.items[node.name]
                    if item.text(0) != node.label:
                        item.setText(0, node.label)
            return  # no further updates needed

        # store new tree

        self._current_tree = dict()
        for node in self.guiScene._nodes:
            self._current_tree[node.name] = (
                getattr(node, "parent", None),
                node.manager,
                type(node),
            )

        # start the update

        self.guiScene.sort_nodes_by_parent()

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

        # store the current scroll position
        vertical_position = self.treeView.verticalScrollBar().sliderPosition()

        self.treeView.clear()
        self.treeView.guiScene = self.guiScene

        self.show_managed_nodes = self.checkbox.isChecked()

        def give_parent_tree_item(node):
            """Determines where to place the given item in the tree.
            Returns the parent node, which may be the invisible root node, to which the item of this node
            shall be a child
            """

            item = give_parent_item(node, self.items)
            if item is None:
                return self.treeView.invisibleRootItem()
            else:
                return item

        for node in self.guiScene._nodes:
            # create a tree item

            item = self.make_tree_item(node)

            # if we have a parent, then put the items under the parent,
            # else put it under the root

            if type(node) in ICONS:
                item.setIcon(0, ICONS[type(node)])
            else:
                item.setIcon(0, QIcon(":/icons/redball.png"))

            try:
                parent = node.parent
            except:
                parent = None

            # node is managed by a manager
            show_managed_node = self.show_managed_nodes

            # custom work-around for showing the "out-frame" for managed geometric connectors
            if isinstance(node._manager, GeometricContact):
                if node == node._manager._child_circle_parent_parent:
                    if (
                        node._manager.manager is None
                    ):  # but only if the manager itself is not also managed (and thus hidden)
                        show_managed_node = True

            if not show_managed_node:  # another override
                if hasattr(node, "_always_show_in_tree"):
                    show_managed_node = node._always_show_in_tree

            if node.manager and show_managed_node:  # are we showing managed nodes?
                item.setForeground(0, QBrush(QColor(0, 150, 0)))
                self.items[node.name] = item
                give_parent_tree_item(node).addChild(item)

            elif node.manager is None:
                self.items[node.name] = item
                give_parent_tree_item(node).addChild(item)

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
        drag.setPixmap(dragged.icon(0).pixmap(16))
        drag.exec(supportedActions=supportedActions)  # , defaultAction=Qt.MoveAction)


class WidgetNodeTree(guiDockWidget, HasNodeTreeMixin):
    DO_RECENT_ITEMS = False

    def guiCanShareLocation(self):
        return False  # Want all the space I can have

    def guiCreate(self):
        HasNodeTreeMixin.init(self)

        self.contents.setContentsMargins(0, 0, 0, 0)

        self.tbFilter = QtWidgets.QComboBox(self.contents)
        self.tbFilter.setEditable(True)
        self.tbFilter.lineEdit().setPlaceholderText("Filter")
        self.tbFilter.lineEdit().setClearButtonEnabled(True)

        filter_options = []

        for key in DAVE_NODEPROP_INFO.keys():
            filter_options.append(f"type:{key.__name__}")

        update_combobox_items_with_completer(self.tbFilter, filter_options)

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

        self.treeView.setStyleSheet(
            """
                                    QWidget {border: None}
                                    
                                    QTreeView::branch:has-siblings:!adjoins-item {
                                        border-image: url(:tree/tree/vline.svg) 0;
                                    }
                                    
                                    QTreeView::branch:has-siblings:adjoins-item {
                                        border-image: url(:tree/tree/Tline.svg) 0;
                                    }
                                    
                                    QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                                        border-image: url(:tree/tree/Lline.svg) 0;
                                    }
                                    
                                    QTreeView::branch:has-children:has-siblings:closed {
                                            image: url(:tree/tree/T_closed.svg);
                                    }
                                    
                                    QTreeView::branch:has-children:!has-siblings:closed {
                                            image: url(:tree/tree/L_closed.svg);
                                    }
                                    
                                    QTreeView::branch:has-children:has-siblings:open {
                                            image: url(:tree/tree/T_open.svg);
                                    }
                                    
                                    QTreeView::branch:has-children:!has-siblings:open {
                                            image: url(:tree/tree/L_open.svg);
                                    }"""
        )

        self.checkbox = QCheckBox(self.contents)
        self.checkbox.setText("show all managed nodes")
        self.checkbox.setChecked(False)
        self.checkbox.toggled.connect(self.update_node_data_and_tree)

        if self.DO_RECENT_ITEMS:
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
        layout.addWidget(self.tbFilter)
        layout.addWidget(self.treeView)
        layout.addWidget(self.checkbox)

        if self.DO_RECENT_ITEMS:
            layout.addWidget(
                self.listbox
            )  # No recent items for now, don't think anybody uses it

        self.contents.setLayout(layout)

        layout.setContentsMargins(4, 0, 0, 0)

        self.recent_items = list()

        self.delete_eventFilter = DeleteEventFilter()
        self.delete_eventFilter.callback = self.delete_key
        self.installEventFilter(self.delete_eventFilter)

        self.tbFilter.editTextChanged.connect(self.filter_changed)


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

    def make_tree_item(self, node):
        text = node.name
        item = QTreeWidgetItem()
        item.setToolTip(0, text)  # store the name in the tool-tip

        item.setText(0, node.label)

        return item

    # ======= custom

    def delete_key(self):
        self.gui.delete_key()

    def dragDropCallback(self, drop, onto, event):
        keep_local_position = event.keyboardModifiers() == Qt.ControlModifier

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
                code = f"s.new_geometriccontact('Geometric_connection of {drop} on {onto}','{drop}','{onto}')"

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
        if self.DO_RECENT_ITEMS:
            self.listbox.clear()
            self.listbox.addItems([node.name for node in self.recent_items])

    def filter_changed(self, *args):
        self.update_node_visibility()

    def update_node_visibility(self):
        """Updates the visibility of the nodes in the tree
        passes the filter and the visibility settings of the viewer"""

        filter_type = ""
        filter_name = ""

        filter = self.tbFilter.currentText()
        parts = filter.split(" ")
        parts = [part for part in parts if part != ""]
        for part in parts:
            part = part.lower()
            if part.startswith("type:"):
                filter_type = part[5:].lower()
            else:
                filter_name = part.lower()

        for name, item in self.items.items():
            # item not visible? then mark gray
            node = self.guiScene[name]
            #
            # process node visibility from node settings itself
            if not node.visible:
                item.setForeground(0, QBrush(QColor(124, 124, 124)))
            elif node.manager is not None:
                item.setForeground(0, QBrush(QColor(0, 150, 0)))
            else:
                item.setForeground(0, QBrush(QColor(0, 0, 0)))

            # process node visibility from filter
            # only set doHide to True if node should be hidden
            # actual hiding is done later because we need to check if children are visible
            hide = False
            if filter_type != "":
                if filter_type not in node.__class__.__name__.lower():
                    hide = True
            if filter_name != "":
                if filter_name not in name.lower():
                    hide = True

            item.doHide = hide

        def has_visible_children(item):
            for i in range(item.childCount()):
                child = item.child(i)
                if not child.doHide:
                    return True
                if has_visible_children(child):
                    return True
            return False

        for name, item in self.items.items():
            if item.doHide:
                if has_visible_children(item):
                    item.setForeground(0, QBrush(QColor(120, 120, 200)))
                    item.setHidden(False)
                else:
                    item.setHidden(True)
            else:
                item.setHidden(False)

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
