from DAVE.gui.dock_system.dockwidget import *
from PySide6.QtGui import QDrag, QBrush
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel, QLineEdit, QCheckBox

from DAVE.tools import fancy_format
from DAVE.visual_helpers.constants import BLUE_LIGHT, YELLOW_LIGHT


class TreeWithDragOut(QtWidgets.QTreeWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.last_selected_item_row = None

    def mouseMoveEvent(self, event):

        # we should have only a single item selected
        items = self.selectedItems()
        if len(items) < 1:
            return

        texts = []
        for item in items:

        # if item.parent() is not None:
        #     item  = item.parent()

            text = item.text(0)
            if text[0]=='.':
                text = "{}{}".format(self.nodename, text)
            texts.append(text)


        drag = QDrag(self)
        mime = QtCore.QMimeData()

        mime.setText('\n'.join(texts))
        drag.setMimeData(mime)
        drag.exec(QtCore.Qt.MoveAction)


    def mousePressEvent(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        current_item = self.itemAt(event.pos())

        if modifiers == QtCore.Qt.ShiftModifier and self.last_selected_item_row:
            current_row = self.indexFromItem(current_item).row()
            last_row = self.last_selected_item_row

            if last_row > self.topLevelItemCount():  # if the last selected item is out of bounds becuse the content has changed
                last_row = self.topLevelItemCount() - 1

            start, end = sorted([current_row, last_row])

            for row in range(start, end + 1):
                item = self.topLevelItem(row)
                item.setSelected(True)
            self.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        else:
            if event.button() == QtCore.Qt.LeftButton:
                self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
                self.last_selected_item_row = self.indexFromItem(current_item).row()

            super().mousePressEvent(event)

class WidgetDerivedProperties(guiDockWidget):

    def guiCreate(self):

        self._nodename = None

        self.label = QLabel()
        self.filterbox = QLineEdit()
        self.filterbox.textChanged.connect(self.display_node_properties)

        self.cd_show_all = QCheckBox('Show all properties')
        self.cd_show_all.stateChanged.connect(self.display_node_properties)


        self.dispPropTree = TreeWithDragOut(self.contents)
        self.dispPropTree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dispPropTree.setAlternatingRowColors(False)
        self.dispPropTree.setRootIsDecorated(False)
        self.dispPropTree.setObjectName("dispPropTree")
        self.dispPropTree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.dispPropTree.setColumnCount(4)
        self.dispPropTree.setHeaderLabels(('Property', 'Value','Unit','Description'))

        self.dispPropTree.header().setVisible(True)
        self.dispPropTree.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)

        self.dispPropTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dispPropTree.customContextMenuRequested.connect(self.rightClickTreeview)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.filterbox)
        layout.addWidget(self.dispPropTree)
        layout.addWidget(self.cd_show_all)
        self.contents.setLayout(layout)

        # let the property tree accept drops and assign a callback
        self.dispPropTree.setAcceptDrops(True)
        self.dispPropTree.dragEnterEvent = self.dragEnterEvent
        self.dispPropTree.dragMoveEvent = self.dragEnterEvent
        self.dispPropTree.dropEvent = self.dropEvent

        # assign a callback to the delete-key event of the property tree
        self.dispPropTree.keyPressEvent = self.delete_key_pressed

    def delete_key_pressed(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_selected_watches()
        else:
            super().keyPressEvent(event)


    def guiProcessEvent(self, event):

        if event in [guiEventType.SELECTION_CHANGED,
                     guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STATE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED,
                     guiEventType.WATCHES_CHANGED,
                     guiEventType.MODEL_STEP_ACTIVATED]:
            self.display_node_properties()

    def guiDefaultLocation(self):
        return PySide6QtAds.DockWidgetArea.RightDockWidgetArea

    def dragEnterEvent(self, event):
        try:
            text = event.mimeData().text()
            if '.' not in text:
                return
        except:
            return

        event.accept()

    def dropEvent(self, event):
        # get the text from the mime data
        #
        # the text should be in the form of s['nodename'].property
        text = event.mimeData().text()

        if '.' in text:

            codes = []

            for row in text.split('\n'):
                node_name = row.split('.')[0]
                prop = row.split('.')[1]
                codes.append(f's.try_add_watch("{node_name}", "{prop}")')

            code = '\n'.join(codes)
            self.guiRunCodeCallback(code, guiEventType.WATCHES_CHANGED)
            event.accept()

    # ======= custom

    def delete_selected_watches(self):
        """Deletes the watches of the selected properties."""

        codes = []
        if self.dispPropTree.selectedItems():
            for item in self.dispPropTree.selectedItems():
                text = item.text(0)
                if '.' in text:
                    node = text.split('.')[0]
                    prop = text.split('.')[1]

                    codes.append(f's.try_delete_watch("{node}", "{prop}")')

            self.guiRunCodeCallback('\n'.join(codes), guiEventType.WATCHES_CHANGED)

    def display_node_properties(self, *args):
        self.dispPropTree.clear()

        do_show_all = self.cd_show_all.isChecked()

        s = self.guiScene

        # watches
        node, prop, value, docs = s.evaluate_watches()

        for n, p, v, d in zip(node, prop, value, docs):

            w = f'{n.name}.{p}'
            try:
                result = f'{v:.3f}'
            except:
                result = str(v)  # for None

            pa = QtWidgets.QTreeWidgetItem(self.dispPropTree)
            pa.setBackground(0,QBrush(QColor(*YELLOW_LIGHT)))
            pa.setBackground(1, QBrush(QColor(*YELLOW_LIGHT)))
            pa.setBackground(2, QBrush(QColor(*YELLOW_LIGHT)))

            pa.setText(0, w)
            pa.setText(1, str(result))
            pa.setText(2, d.units)
            pa.setText(3, d.doc_short_with_remarks)

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

            doc = self.guiScene.give_documentation(node, p)

            if not do_show_all:
                if doc.is_single_numeric is False:
                    continue

            code = "node.{}".format(p)
            try:
                result = eval(code)
                result = fancy_format(result)

            except:
                result = 'Error evaluating {}'.format(code)

            pa = QtWidgets.QTreeWidgetItem(self.dispPropTree)
            pa.setText(0, '.' + p)
            pa.setText(1, str(result))
            pa.setText(2, doc.units)
            pa.setText(3, doc.doc_short_with_remarks)

            pa.setToolTip(0, doc.doc_long)


        self.dispPropTree.expandAll()

    def rightClickTreeview(self, point):

        if self._nodename is None:
            return

        if self.dispPropTree.selectedItems():
            globLoc = self.dispPropTree.mapToGlobal(point)
            self.openContextMenyAt(globLoc)

    def openContextMenyAt(self, globLoc):

        menu = QtWidgets.QMenu()

        def add_watch():
            # self.guiScene.try_add_watch(node_name, node_prop)
            # self.display_node_properties()

            codes = []
            for item in self.dispPropTree.selectedItems():
                text = item.text(0)

                node = text.split('.')[0]
                prop = text.split('.')[1]

                if node == '':
                    node = self._nodename
                codes.append(f's.try_add_watch("{node}", "{prop}")')

            code = '\n'.join(codes)
            self.guiRunCodeCallback(code, guiEventType.WATCHES_CHANGED)

            if 'Watches' in self.gui.guiWidgets:
                self.gui.guiWidgets['Watches'].fill()

        menu.addAction("Add watch", add_watch)

        menu.addSeparator()

        menu.exec_(globLoc)






