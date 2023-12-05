# Taken from: https://timlehr.com/2018/01/python-exception-hooks-with-qt-message-box/
# who in turn took from: https://github.com/ColinDuquesnoy/QCrash
#
# Both are MIT licensed
#
# Updated to PySide6

import sys
import traceback
import logging
from PySide6 import QtCore, QtWidgets

from DAVE.gui.helpers.gui_logger import DAVE_GUI_LOGGER

# basic logger functionality
log = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
log.addHandler(handler)

def show_exception_box(log_msg):
    """Checks if a QApplication instance is available and shows a messagebox with the exception message.
    If unavailable (non-console application), log an additional notice.
    """

    DAVE_GUI_LOGGER.log("Starting exception handling")
    DAVE_GUI_LOGGER.log(log_msg)

    if QtWidgets.QApplication.instance() is not None:


            errorbox = QtWidgets.QMessageBox()

            text = "Oops. An unexpected error occured:\n{0}".format(log_msg)
            text += "\n\nWould you like to report this error to the DAVE developers so that we can fix it?"

            errorbox.setText(text)
            errorbox.setWindowTitle("My fault, not yours. Sorry :-(")
            errorbox.setIcon(QtWidgets.QMessageBox.Critical)
            errorbox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            ret = errorbox.exec()

            if ret == QtWidgets.QMessageBox.Yes:
                # compile the log
                from DAVE.gui.helpers.crash_mailer import compile_and_mail
                compile_and_mail(info = log_msg)

    else:
        log.debug("No QApplication instance available.")

class UncaughtHook(QtCore.QObject):
    _exception_caught = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(UncaughtHook, self).__init__(*args, **kwargs)

        # this registers the exception_hook() function as hook with the Python interpreter
        sys.excepthook = self.exception_hook

        # connect signal to execute the message box function always on main thread
        self._exception_caught.connect(show_exception_box)

    def exception_hook(self, exc_type, exc_value, exc_traceback):
        """Function handling uncaught exceptions.
        It is triggered each time an uncaught exception occurs.
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # ignore keyboard interrupt to support console applications
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            exc_info = (exc_type, exc_value, exc_traceback)
            log_msg = '\n'.join([''.join(traceback.format_tb(exc_traceback)),
                                 '{0}: {1}'.format(exc_type.__name__, exc_value)])
            log.critical("Uncaught exception:\n {0}".format(log_msg), exc_info=exc_info)

            # trigger message box show
            self._exception_caught.emit(log_msg)

# create a global instance of our class to register the hook
qt_exception_hook = UncaughtHook()


