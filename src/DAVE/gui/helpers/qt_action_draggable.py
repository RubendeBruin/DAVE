"""This is a draggable QWidgetAction that can be used in a QMenu.

It is specifically designed to be used in the DAVE GUI in combination with selecting nodes.

Clicked will fire if a node is clicked.
The menu will be closed only if the shift or control key is NOT down.


"""
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import (
    QApplication,
    QMenu,
    QWidgetAction,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QLabel,
)
from PySide6.QtCore import Qt, QMimeData, Signal


# Class wrapping a menu item


class QDraggableNodeActionWidget(QWidgetAction):
    def __init__(self, text="", mime_text=None, right_text=None, icon = None):
        self.startPos = None

        QWidgetAction.__init__(self, None)
        self.text = text

        if mime_text is None:
            mime_text = text

        self.mime_text = mime_text

        self.widget = QWidget()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(9, 3, 3, 9)

        if icon:
            self.icon = QLabel()
            self.icon.setPixmap(icon.pixmap(12,12))
            self.layout.addWidget(self.icon)
            self.icon.setFixedWidth(16)

            self.icon.mouseMoveEvent = self.mouseMoveEvent
            self.icon.mousePressEvent = self.mousePressEvent
            self.icon.mouseReleaseEvent = self.mouseReleaseEvent

        self.label = QLabel()
        self.label.setText(self.text)
        # self.label.setAlignment(Qt.AlignRight)

        self.label.mouseMoveEvent = self.mouseMoveEvent
        self.label.mousePressEvent = self.mousePressEvent
        self.label.mouseReleaseEvent = self.mouseReleaseEvent


        self.widget.setLayout(self.layout)
        self.layout.addWidget(self.label)
        if right_text is not None:
            self.right_label = QLabel()
            self.right_label.setText(right_text)
            self.right_label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(self.right_label)
        self.setDefaultWidget(self.widget)

    @Signal
    def clicked(self):
        pass

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

        # if the shift or control key is NOT down, close the menu
        if not (
            event.modifiers() & Qt.ShiftModifier
            or event.modifiers() & Qt.ControlModifier
        ):
            self.triggered.emit()  # close the menu

    def mousePressEvent(self, event):
        self.startPos = event.position()

    def mouseMoveEvent(self, event):
        if self.startPos is None:
            return
        if event.buttons() != Qt.LeftButton:
            return
        if (
            event.position() - self.startPos
        ).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        data = QMimeData()
        data.setText(self.mime_text)
        drag.setMimeData(data)
        pixmap = self.icon.pixmap()
        drag.setPixmap(pixmap)
        result = drag.exec()

        if result != Qt.IgnoreAction:
            self.triggered.emit() # close the menu

    def setBold(self, bold):
        if bold:
            self.label.setStyleSheet("font-weight: bold")
        else:
            self.label.setStyleSheet("font-weight: normal")


if __name__ == "__main__":
    app = QApplication()
    menu = QMenu()
    demo = QDraggableNodeActionWidget("Drag me or click me", "mime_text")
    demo.clicked.connect(lambda: print("clicked"))

    a = menu.addAction("Other action")

    menu.addAction(demo)
    menu.exec()
