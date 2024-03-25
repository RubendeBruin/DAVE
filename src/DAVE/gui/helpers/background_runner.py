"""Displays a dialog while running one or more tasks in the background.
Done in a separate thread to avoid blocking the GUI.
"""
import subprocess
import time
from threading import Thread

from PySide6 import QtWidgets
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import Signal, Slot, QObject

class SignalWrapper(
    QObject):  # slots need to be defined inside a class derived from QObject (ref: https://wiki.qt.io/Qt_for_Python_Signals_and_Slots)
    # Signals are runtime objects owned by instances, they are not class attributes:
    action = Signal(str)

class BackgroundRunnerGui:
    """Runs tasks in the background and displays a dialog while running them.
    """

    def __init__(self, commands: list[list[str]], title = "Running external commands..."):
        """Constructor"""
        assert QApplication.instance() is not None, "QApplication must be created before creating a BackgroundRunner"
        application = QApplication.instance()

        self.active_command = "Starting..."

        self.commands = commands

        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle(title)
        dialog.setWindowIcon(QIcon(":/icons/Dave_icon.png"))

        layout = QtWidgets.QVBoxLayout()
        dialog.setLayout(layout)

        label = QtWidgets.QLabel("Starting...")
        layout.addWidget(label)

        button = QtWidgets.QPushButton("Stop")
        layout.addWidget(button)

        # disable close button
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowCloseButtonHint)


        @Slot(str)
        def update_text(text: str):
            label.setText(text)

        # create communication signals for inter-thread communication
        self.feedback = SignalWrapper()
        self.feedback.action.connect(update_text)

        @Slot(str)
        def on_done_func(error_message: str):
            if error_message:
                label.setText(error_message)
            else:
                dialog.close()


        self.on_done = SignalWrapper()
        self.on_done.action.connect(on_done_func)

        self.do_terminate = False

        new_thread = Thread(target = self.run_commands)
        new_thread.start()

        def terminate():
            self.do_terminate = True
            new_thread.join()
            self.on_done.action.emit("")

        button.clicked.connect(terminate)

        dialog.show()

    def run_commands(self):
        for command in self.commands:

            self.feedback.action.emit(f"Running command: {command}")
            print(f"Running command: {command}")

            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except:
                self.on_done.action.emit(f"Error running {command}")
                return

            while True:
                time.sleep(0.1)

                retcode = process.poll()

                print(retcode)

                if retcode is not None:
                    if retcode == 0:
                        break
                    self.on_done.action.emit(f"Error running {command}")
                    return

                if self.do_terminate:
                    self.feedback.action.emit(f"Terminating")
                    process.terminate()
                    break

            if self.do_terminate:
                break

            print("Done running command")

        self.feedback.action.emit(f"Finished!")
        self.on_done.action.emit("")


if __name__ == '__main__':

    app = QApplication([])
    commands = [["ping", "8.8.8.8", "-n","4"],   # hello google
                ["ping", "1.2.3.4", "-n", "4"],  # this one times out
                ]
    BackgroundRunnerGui(commands)
    app.exec()










