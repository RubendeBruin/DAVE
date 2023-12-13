"""Creates a logger for the GUI.

The logger stores the messaged in memory only. They can be saved to a file if requested.

A global logger DAVE_GUI_LOGGER is created and used by the GUI.

"""
import traceback


class DaveGuiLogger():
    def __init__(self, scene = None):
        self._log = []
        self._logged_code = []
        self.scene = scene

    def log_exception(self, exception):
        """Append an exception to the log."""

        self.log(str(exception))
        notes = getattr(exception, '__notes__', [])
        for note in notes:
            self.log(note)
        self.log(traceback.format_exc())

    def log(self, msg):
        """Append a message to the log."""

        # treat repeated messages differently
        if self._log:
            if self._log[-1].startswith(msg): # repeated message
                if self._log[-1].endswith('(repeated)'):
                    return
                else:
                    msg += ' (repeated)'
        self._log.append(msg)

    def log_code(self, code):
        """Append a code to the log."""
        self._logged_code.append(code)

    def get_log(self):
        """Return the log as a string."""
        log = '\n'.join(self._log)
        log += '\n\n\n--ACTIONS--\n'
        log += '\n'.join(self._logged_code)
        log += '\n\n\n--SCENE--\n'
        try:
            log += '\n' + str(self.scene.give_python_code())
        except Exception as M:
            log += '\n' + str(M)
        return log

DAVE_GUI_LOGGER = DaveGuiLogger()
