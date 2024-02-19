from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt

from DAVE.scene import Scene
from DAVE.nodes import Cable


class ConnectionsTreeWidget(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setHeaderLabels(["⟲", "Connection", "Offset", "Friction", "Max winding"])

        # Enable drag and drop reordering
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QTreeWidget.InternalMove)

    def connect(self, scene: Scene, node: Cable):
        self._scene = scene
        self._node = node

    def fill(self):
        # add items to the tree
        for i in range(len(self._node.connections)):
            item = QTreeWidgetItem(
                [
                    " ",
                    self._node.connections[i].label,
                    str(self._node.offsets[i]),
                    "friction",  # str(self._node.friction[i]),
                    str(self._node.max_winding_angles[i]),
                ]
            )
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)
            self.addTopLevelItem(item)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText() or event.source() == self:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.proposedAction() == Qt.MoveAction:
            moved_item = self.selectedItems()[0]
            to_item = self.itemAt(event.pos())

            print(moved_item)
            print(to_item)

        print(event.mimeData().text())
        if event.source() == self:
            event.accept()
