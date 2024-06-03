"""Creates a context manager for a QT Dialog that blocks the main GUI,
re-enables the main gui and closes the dialog when the context is exited."""
from datetime import datetime
from time import sleep

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
)

from DAVE.gui import Gui


# define the dialog
class BlockingDialog(QDialog):
    def __init__(self, gui):
        self.gui = gui
        self.main_window = gui.MainWindow
        self.app = gui.app
        self.done = False

        self.wants_to_cancel = False

        super().__init__()
        self.setModal(True)

        # # disable the close button
        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)  # <-- captured by closeEvent

        self.setWindowIcon(self.main_window.windowIcon())
        self.setWindowTitle("Working...")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # add a label and a button
        self.label = QLabel(self)
        layout.addWidget(self.label)
        self.button = QPushButton(self)
        self.button.setText("Cancel")
        layout.addWidget(self.button)
        self.button.pressed.connect(self.cancel_button_pressed)

        # register the start-time
        self.start_time = datetime.now()

    def user_wants_to_terminate(self):
        return self.wants_to_cancel

    def closeEvent(self, event):

        if self.done:
            event.accept()
            return

        self.wants_to_cancel = True
        self.button.setEnabled(False)
        self.button.setText("Cancelling...")
        self.app.processEvents()
        event.ignore()

    def processEventsIfSufficientTimeElapsed(self, min_seconds_passed=0.5):
        """Process events if more than min_time_passed has passed since the last update"""
        if (datetime.now() - self.start_time).total_seconds() > min_seconds_passed:
            self.app.processEvents()
            self.start_time = datetime.now()

    def cancel_button_pressed(self):
        self.wants_to_cancel = True
        self.button.setEnabled(False)
        self.button.setText("Cancelling...")
        self.app.processEvents()

    def feedback(self, text):
        self.label.setText(text)
        self.processEventsIfSufficientTimeElapsed()

    def __enter__(self):
        self.main_window.setEnabled(False)
        self.show()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.done = True
        self.close()
        self.main_window.setEnabled(True)
        return False

# example use:

if __name__ == '__main__':
    from DAVE import *

    s = Scene()
    gui = Gui(s, block = False)

    with BlockingDialog(gui) as dialog:
        for i in range(100):
            dialog.feedback(f"Processing {i}/100")
            dialog.processEventsIfSufficientTimeElapsed()
            if dialog.wants_to_cancel:
                break

            sleep(0.1)

    gui.app.exec()