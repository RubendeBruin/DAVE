"""
Creates an autosave file for the current project.


"""

import os
import datetime
from DAVEcore import isProcessRunning
from DAVE.gui.settings import autosave_dir

class DaveAutoSave:
    def __init__(self):
        self.pid = os.getpid()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.autosave_file = autosave_dir / f"autosave_{timestamp}_{self.pid}.dave"

        print(f"Autosave file: {self.autosave_file}")

    def write(self, what):
        """Writes "what" to the autosave file"""

        with open(self.autosave_file, "w") as f:
            f.write(what)
        print('Saved autosave file: ', self.autosave_file)

    def cleanup(self):
        """Deletes the autosave file"""

        if self.autosave_file.exists():
            self.autosave_file.unlink()

    @classmethod
    def open_folder(cls):
        """Opens the autosave folder"""
        os.system(f"explorer {autosave_dir} &")

    @classmethod
    def scan(cls):
        """Returns a list of autosave files"""

        autosave_files = []
        for f in autosave_dir.iterdir():
            if f.name.startswith("autosave_"):

                # get the pid of the file
                pid = int(f.name.split("_")[-1].split(".")[0])
                if not isProcessRunning(pid):
                    autosave_files.append(f)
        return autosave_files

