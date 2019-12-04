from DAVE.gui2.dockwidget import *
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide2.QtCore import QMimeData, Qt, QItemSelectionModel
import DAVE.scene as ds

class SceneTreeModel(QStandardItemModel):

    def mimeData(self, indexes):
        QStandardItemModel.mimeData(self, indexes)
        name = indexes[0].data()
        print('called mimeData on ' + name)
        mimedata = QMimeData()
        mimedata.setText(name)
        return mimedata

    def supportedDropActions(self):
        return QtCore.Qt.MoveAction

    def canDropMimeData(self, data, action, row, column, parent):
        print('can drop called on')
        print(parent.data())
        return True

    def dropMimeData(self, data, action, row, column, parent):
        parent_name = parent.data()
        node_name = data.text()
        print("Dropped {} onto {}".format(node_name, parent_name))

        if parent_name is None:
            code = "s['{}'].change_parent_to(None)".format(node_name)
        else:
            code = "s['{}'].change_parent_to(s['{}'])".format(node_name, parent_name)
        print(code)

        self._scene.run_code(code)

        return False

class WidgetNodeTree(guiDockWidget):

    def guiCreate(self):

        self.treeView = QtWidgets.QTreeView(self.contents)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView.setRootIsDecorated(True)
        self.treeView.setExpandsOnDoubleClick(False)
        self.treeView.setObjectName("treeView")
        self.treeView.header().setVisible(False)
        self.treeView.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.treeView.activated.connect(self.tree_select_node)  # fires when a user presses [enter]
        self.treeView.doubleClicked.connect(self.tree_select_node)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.rightClickTreeview)


        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.treeView)
        self.contents.setLayout(layout)

    def guiProcessEvent(self, event):
        if event in [guiEventType.MODEL_STRUCTURE_CHANGED, guiEventType.SELECTION_CHANGED, guiEventType.FULL_UPDATE]:
            self.update_node_data_and_tree()

        if event in [guiEventType.SELECTION_CHANGED]:
            self.update_selection()



    # ======= custom

    def tree_select_node(self, index):
        node_name = index.data()
        self.guiSelectNode(node_name)

    def rightClickTreeview(self):
        pass
        # TODO

    def update_selection(self):

        selected_names = [node.name for node in self.guiSelection]
        for name in self.items.keys():
            if name in selected_names:
                selected_indexes.append(self.items[name])

        self.treeView.selectionModel().select(selected_indexes[0], QItemSelectionModel.SelectionFlag(True))


    def update_node_data_and_tree(self):
        """
        Updates the tree and assembles the node-data

        This data is obtained from scene.nodes and assumes that
        each of the nodes has a visual assigned to it.

        """
        model = SceneTreeModel()
        self.items = dict()

        self.guiScene.sort_nodes_by_dependency()

        for node in self.guiScene.nodes:

            # create a tree item
            text = node.name
            item = QStandardItem()
            item.setText(text)

            # if we have a parent, then put the items under the parent,
            # else put it under the root

            item.setIcon(QIcon(":/icons/redball.png"))
            if isinstance(node, ds.Axis):
                item.setIcon(QIcon(":/icons/axis.png"))
            if isinstance(node, ds.RigidBody):
                item.setIcon(QIcon(":/icons/cube.png"))
            if isinstance(node, ds.Poi):
                item.setIcon(QIcon(":/icons/poi.png"))
            if isinstance(node, ds.Cable):
                item.setIcon(QIcon(":/icons/cable.png"))
            if isinstance(node, ds.Visual):
                item.setIcon(QIcon(":/icons/visual.png"))
            if isinstance(node, ds.LC6d):
                item.setIcon(QIcon(":/icons/lincon6.png"))
            if isinstance(node, ds.Connector2d):
                item.setIcon(QIcon(":/icons/con2d.png"))
            if isinstance(node, ds.LinearBeam):
                item.setIcon(QIcon(":/icons/beam.png"))
            if isinstance(node, ds.HydSpring):
                item.setIcon(QIcon(":/icons/linhyd.png"))
            if isinstance(node, ds.Force):
                item.setIcon(QIcon(":/icons/force.png"))
            if isinstance(node, ds.Sheave):
                item.setIcon(QIcon(":/icons/sheave.png"))
            if isinstance(node, ds.Buoyancy):
                item.setIcon(QIcon(":/icons/trimesh.png"))

            try:
                parent = node.parent
            except:
                parent = None

            self.items[node.name] = item

            if parent is not None:
                self.items[node.parent.name].appendRow(item)
            else:
                model.invisibleRootItem().appendRow(item)

        self.treeView.setModel(model)
        #
        self.treeView.expandAll()

