from DAVE.gui.dock_system.dockwidget import *
from PySide6.QtGui import QDrag, QBrush
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel, QLineEdit

from DAVE.tools import fancy_format


class TreeWithDragOut(QtWidgets.QTreeWidget):

    def mouseMoveEvent(self, event):

        # we should have only a single item selected
        item = self.selectedItems()
        if len(item) != 1:
            return

        item = item[0]

        # item should not have a parent (should not be a value)
        if item.parent() is not None:
            item  = item.parent()

        drag = QDrag(self)
        mime = QtCore.QMimeData()

        text = item.text(0)
        if text[0]=='.':
            text = "s['{}']{}".format(self.nodename, text)

        mime.setText(text)
        drag.setMimeData(mime)
        drag.exec(QtCore.Qt.MoveAction)


class WidgetDerivedProperties(guiDockWidget):

    def guiCreate(self):

        self._watches = []
        self._nodename = None

        self.label = QLabel()
        self.filterbox = QLineEdit()
        self.filterbox.textChanged.connect(self.display_node_properties)

        self.dispPropTree = TreeWithDragOut(self.contents)
        self.dispPropTree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dispPropTree.setAlternatingRowColors(True)
        self.dispPropTree.setRootIsDecorated(False)
        self.dispPropTree.setObjectName("dispPropTree")

        # self.dispPropTree.setColumnCount(3)
        # self.dispPropTree.setHeaderLabels(('Value','Limits','UC'))

        item_0 = QtWidgets.QTreeWidgetItem(self.dispPropTree)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.dispPropTree.header().setVisible(False)
        self.dispPropTree.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)

        self.dispPropTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dispPropTree.customContextMenuRequested.connect(self.rightClickTreeview)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.filterbox)
        layout.addWidget(self.dispPropTree)
        self.contents.setLayout(layout)

    def guiProcessEvent(self, event):

        if event in [guiEventType.SELECTION_CHANGED,
                     guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STATE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED,
                     guiEventType.MODEL_STEP_ACTIVATED]:
            self.display_node_properties()

    def guiDefaultLocation(self):
        return PySide6QtAds.DockWidgetArea.RightDockWidgetArea


    # ======= custom

    def display_node_properties(self, *args):
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
            pa.setForeground(0,QBrush(QColor(0,120,0)))

            v = QtWidgets.QTreeWidgetItem(pa)
            pa.setText(0, w)
            v.setText(0, str(result))

        # get first selected item
        if self.guiSelection:
            node = self.guiSelection[0]
            self._nodename = node.name
            self.dispPropTree.nodename = node.name
            self.label.setText(f"{node.name} [{node.class_name}]")
        else:
            return

        props = self.guiScene.give_properties_for_node(node)


        # evaluate properties
        filter = self.filterbox.text()

        for p in props:

            if filter not in p:
                continue

            code = "node.{}".format(p)
            try:
                result = eval(code)
                result = fancy_format(result)

            except:
                result = 'Error evaluating {}'.format(code)

            pa = QtWidgets.QTreeWidgetItem(self.dispPropTree)
            v = QtWidgets.QTreeWidgetItem(pa)
            pa.setText(0, '.' + p)

            text = str(result)
            v.setText(0, text)

            doc = self.guiScene.give_documentation(node, p).doc_long
            v.setToolTip(0, doc)

            # add limit node
            if p in node.limits:
                v = QtWidgets.QTreeWidgetItem(pa)
                limit = node.limits[p]
                uc = node.give_UC(p)
                text = f'UC = {uc:.2f} = ({text} / {limit})'
                v.setText(0, text)

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

            watch_name = f'{node_name}{node_prop}'
            watch_code = f'self{node_prop}'
            self.guiScene[node_name].watches[watch_name] = Watch(evaluate=watch_code)

            if 'Watches' in self.gui.guiWidgets:
                self.gui.guiWidgets['Watches'].fill()

        menu.addAction("Add watch", add_watch)

        menu.addSeparator()

        def delete_all():
            self._watches.clear()
            self.display_node_properties()

        menu.addAction("Delete all watches", delete_all)

        menu.exec_(globLoc)






