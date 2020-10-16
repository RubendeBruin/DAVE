from DAVE.gui.dockwidget import *
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon, QDrag
from PySide2.QtCore import QMimeData, Qt, QItemSelectionModel
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QTreeWidgetItem
import DAVE.scene as nodes
import DAVE.settings as ds

from DAVE.tools import fancy_format


class TreeWithDragOut(QtWidgets.QTreeWidget):

    def mouseMoveEvent(self, event):

        # we should have only a single item selected
        item = self.selectedItems()
        if len(item) != 1:
            return

        item = item[0]

        # item should not have a parent (should not be a value)
        if item.parent() is None:
            drag = QDrag(self)
            mime = QtCore.QMimeData()

            text = item.text(0)
            if text[0]=='.':
                text = "s['{}']{}".format(self.nodename, text)

            mime.setText(text)
            drag.setMimeData(mime)
            drag.start(QtCore.Qt.MoveAction)


class WidgetDerivedProperties(guiDockWidget):

    def guiCreate(self):

        self._watches = []
        self._nodename = None

        self.dispPropTree = TreeWithDragOut(self.contents)
        self.dispPropTree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dispPropTree.setAlternatingRowColors(True)
        self.dispPropTree.setRootIsDecorated(False)
        self.dispPropTree.setObjectName("dispPropTree")
        item_0 = QtWidgets.QTreeWidgetItem(self.dispPropTree)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.dispPropTree.header().setVisible(False)
        self.dispPropTree.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)

        self.dispPropTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dispPropTree.customContextMenuRequested.connect(self.rightClickTreeview)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.dispPropTree)
        self.contents.setLayout(layout)

    def guiProcessEvent(self, event):

        if event in [guiEventType.SELECTION_CHANGED,
                     guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STATE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED]:
            self.display_node_properties()

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea


    # ======= custom

    def display_node_properties(self):
        self.dispPropTree.clear()


        s = self.guiScene

        # watches
        for w in self._watches:
            try:
                result = eval(w)
                result = fancy_format(result)
            except:
                result = 'Error evaluating {}'.format(w)
            pa = QtWidgets.QTreeWidgetItem(self.dispPropTree)
            pa.setTextColor(0,QColor(0,120,0))

            v = QtWidgets.QTreeWidgetItem(pa)
            pa.setText(0, w)
            v.setText(0, str(result))

        # get first selected item
        if self.guiSelection:
            node = self.guiSelection[0]
            self._nodename = node.name
            self.dispPropTree.nodename = node.name
        else:
            return


        props = []
        props.extend(ds.PROPS_NODE)
        if isinstance(node, nodes.Axis):
            props.extend(ds.PROPS_AXIS)
        if isinstance(node, nodes.RigidBody):
            props.extend(ds.PROPS_BODY)
        if isinstance(node, nodes.Point):
            props.extend(ds.PROPS_POI)
        if isinstance(node, nodes.Cable):
            props.extend(ds.PROPS_CABLE)
        if isinstance(node, nodes.Connector2d):
            props.extend(ds.PROPS_CON2D)
        if isinstance(node, nodes.Buoyancy):
            props.extend(ds.PROPS_BUOY_MESH)
        if isinstance(node, nodes.Beam):
            props.extend(ds.PROPS_BEAM)
        if isinstance(node, nodes.Force):
            props.extend(ds.PROPS_FORCE)
        if isinstance(node, nodes.ContactBall):
            props.extend(ds.PROPS_CONTACTBALL)

        # evaluate properties
        for p in props:
            code = "node.{}".format(p)
            try:
                result = eval(code)

                result = fancy_format(result)

            except:
                result = 'Error evaluating {}'.format(code)

            pa = QtWidgets.QTreeWidgetItem(self.dispPropTree)
            v = QtWidgets.QTreeWidgetItem(pa)
            pa.setText(0, '.' + p)
            v.setText(0, str(result))

        self.dispPropTree.expandAll()

    def rightClickTreeview(self, point):

        if self._nodename is None:
            return

        if self.dispPropTree.selectedItems():
            node_prop = self.dispPropTree.selectedItems()[0].text(0)
        else:
            return

        if node_prop[0] == '.':   # need to be a property, not a value
            globLoc = self.dispPropTree.mapToGlobal(point)
            self.openContextMenyAt(self._nodename, node_prop, globLoc)

    def openContextMenyAt(self, node_name, node_prop, globLoc):

        menu = QtWidgets.QMenu()

        def add_watch():
            self._watches.append("s['{}']{}".format(node_name, node_prop))
            self.display_node_properties()

        menu.addAction("Add watch", add_watch)

        menu.addSeparator()

        def delete_all():
            self._watches.clear()
            self.display_node_properties()

        menu.addAction("Delete all watches", delete_all)

        menu.exec_(globLoc)






