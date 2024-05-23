from PySide6.QtCore import QTimer
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QLabel, QApplication, QWidget, QMenu


class InfoMessage:
    def __init__(self, message):
        # get cursor position

        cursor = QCursor()
        pos = cursor.pos()

        self.menu = QMenu()
        self.menu.addAction(message)
        self.menu.setStyleSheet(
            "QMenu{background-color: rgb(231,200,100); color: black;}"
        )
        self.menu.exec(pos)


if __name__ == "__main__":
    app = QApplication.instance() or QApplication()

    widget = QWidget()
    widget.show()

    InfoMessage("This is a test message")

    app.exec()
