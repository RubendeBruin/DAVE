from DAVE.gui.dockwidget import *
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon, QDrag
from PySide2.QtCore import QMimeData, Qt, QItemSelectionModel
from PySide2.QtWidgets import QTreeWidgetItem
from DAVE.rigging import sheave_connect_context_menu
import DAVE.scene as ds



class NodeTreeWidget(QtWidgets.QTreeWidget):

    def dragEnterEvent(self, event):
        if event.source() is not self:
            print("Not accepting external data")
            event.setDropAction(Qt.IgnoreAction)
            return
        else:
            event.accept()

    def dragMoveEvent(self, event):
        if event.source() is not self:
            print("Not accepting external data")
            event.setDropAction(Qt.IgnoreAction)
            return
        else:
            event.accept()

    def dropEvent(self, event):
        if event.source() is not self:
            print("Not accepting external data")
            event.setDropAction(Qt.IgnoreAction)
            return

        dragged_name = event.mimeData().text()

        # dropped onto
        point = event.pos()
        drop_onto = self.itemAt(point)

        if drop_onto is None:
            drop_onto_name = None
        else:
            drop_onto_name = drop_onto.text(0)

        print('dragged {} onto {}'.format(dragged_name,drop_onto_name))
        event.setDropAction(Qt.IgnoreAction)

        self.parentcallback(dragged_name, drop_onto_name, event)

    def startDrag(self, supportedActions):

        dragged = self.selectedItems()[0]
        mimeData = QMimeData()
        mimeData.setText(dragged.text(0))

        drag = QDrag(self)
        drag.setMimeData(mimeData)

        drag.exec_(supportedActions=supportedActions, defaultAction=Qt.MoveAction)





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

        self.treeView.activated.connect(self.tree_select_node)  # fires when a user presses [enter]
        self.treeView.doubleClicked.connect(self.tree_select_node)
        self.treeView.itemClicked.connect(self.item_clicked)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.rightClickTreeview)

        self.treeView.parentcallback = self.dragDropCallback

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.treeView)
        self.contents.setLayout(layout)

    def guiProcessEvent(self, event):
        if event in [guiEventType.MODEL_STRUCTURE_CHANGED,
                     guiEventType.FULL_UPDATE,
                     guiEventType.SELECTED_NODE_MODIFIED]:
            self.update_node_data_and_tree()

        if event in [guiEventType.SELECTION_CHANGED]:
            self.update_selection()

    # ======= custom

    def dragDropCallback(self, drop, onto, event):

        if onto is None:
            code = "s['{}'].change_parent_to(None)".format(drop)
            self.guiRunCodeCallback(code, guiEventType.MODEL_STRUCTURE_CHANGED)

        else:

            node_drop = self.guiScene[drop]
            node_onto = self.guiScene[onto]

            # are we dropping a sheave onto a sheave?

            if isinstance(node_drop, ds.Sheave) and isinstance(node_onto, ds.Sheave):

                # open an context menu

                sheave_connect_context_menu(node_drop, node_onto,
                                            lambda x : self.guiRunCodeCallback(x, guiEventType.MODEL_STRUCTURE_CHANGED),
                                            self.treeView.mapToGlobal(event.pos()))
            else:
                code = "s['{}'].change_parent_to(s['{}'])".format(drop, onto)
                self.guiRunCodeCallback(code, guiEventType.MODEL_STRUCTURE_CHANGED)


    def tree_select_node(self, index):
        if index.column() == 0:
            node_name = index.data()
            self.guiSelectNode(node_name)

    def item_clicked(self, data):
        name = data.text(0)
        self.guiSelectNode(name)

    def rightClickTreeview(self, point):
        if self.treeView.selectedItems():
            node_name = self.treeView.selectedItems()[0].text(0)
        else:
            node_name = None
        globLoc = self.treeView.mapToGlobal(point)
        self.gui.openContextMenyAt(node_name, globLoc)

    def update_selection(self):

        selected_names = [node.name for node in self.guiSelection]
        for name in self.items.keys():

            if name in selected_names:
                self.items[name].setSelected(True)
            else:
                self.items[name].setSelected(False)

    def update_node_data_and_tree(self):
        """
        Updates the tree and assembles the node-data

        This data is obtained from scene.nodes and assumes that
        each of the nodes has a visual assigned to it.

        """

        self.items = dict()

        self.guiScene.sort_nodes_by_dependency()
        self.treeView.clear()

        for node in self.guiScene._nodes:

            # create a tree item
            text = node.name
            item = QTreeWidgetItem()
            item.setText(0,text)

            # if we have a parent, then put the items under the parent,
            # else put it under the root

            item.setIcon(0, QIcon(":/icons/redball.png"))
            if isinstance(node, ds.Axis):
                item.setIcon(0, QIcon(":/icons/axis.png"))
            if isinstance(node, ds.RigidBody):
                item.setIcon(0, QIcon(":/icons/cube.png"))
            if isinstance(node, ds.Poi):
                item.setIcon(0,QIcon(":/icons/poi.png"))
            if isinstance(node, ds.Cable):
                item.setIcon(0,QIcon(":/icons/cable.png"))
            if isinstance(node, ds.Visual):
                item.setIcon(0,QIcon(":/icons/visual.png"))
            if isinstance(node, ds.LC6d):
                item.setIcon(0,QIcon(":/icons/lincon6.png"))
            if isinstance(node, ds.Connector2d):
                item.setIcon(0,QIcon(":/icons/con2d.png"))
            if isinstance(node, ds.LinearBeam):
                item.setIcon(0,QIcon(":/icons/beam.png"))
            if isinstance(node, ds.HydSpring):
                item.setIcon(0,QIcon(":/icons/linhyd.png"))
            if isinstance(node, ds.Force):
                item.setIcon(0,QIcon(":/icons/force.png"))
            if isinstance(node, ds.Sheave):
                item.setIcon(0,QIcon(":/icons/sheave.png"))
            if isinstance(node, ds.Buoyancy):
                item.setIcon(0,QIcon(":/icons/trimesh.png"))
            if isinstance(node, ds.WaveInteraction1):
                item.setIcon(0,QIcon(":/icons/waveinteraction.png"))
            if isinstance(node, ds.ContactBall):
                item.setIcon(0,QIcon(":/icons/contactball.png"))
            if isinstance(node, ds.ContactMesh):
                item.setIcon(0,QIcon(":/icons/contactmesh.png"))

            try:
                parent = node.parent
            except:
                parent = None

            self.items[node.name] = item

            if parent is not None:
                try:
                    self.items[node.parent.name].addChild(item)
                except:
                    print('stop here')
            else:
                self.treeView.invisibleRootItem().addChild(item)

        # self.treeView.resizeColumnToContents(0)
        self.treeView.expandAll()

