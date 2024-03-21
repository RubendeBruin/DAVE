"""Creates a context manager for a QT Dialog that blocks the main GUI,
re-enables the main gui and closes the dialog when the context is exited."""
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
)


# define the dialog
class BlockingDialog(QDialog):
    def __init__(self, gui):
        self.gui = gui
        self.main_window = gui.MainWindow
        self.app = gui.app

        self.wants_to_cancel = False

        super().__init__()
        self.setModal(True)

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

    def processEventsIfSufficientTimeElapsed(self, min_seconds_passed=0.5):
        """Process events if more than min_time_passed has passed since the last update"""
        if (datetime.now() - self.start_time).total_seconds() > min_seconds_passed:
            self.app.processEvents()
            self.start_time = datetime.now()

    def cancel_button_pressed(self):
        self.wants_to_cancel = True
        self.button.setEnabled(False)
        self.button.setText("Cancelling...")

    def feedback(self, text):
        self.label.setText(text)

    def __enter__(self):
        self.main_window.setEnabled(False)
        self.show()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.main_window.setEnabled(True)
        return False
