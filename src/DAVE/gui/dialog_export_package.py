from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog

from DAVE.gui.forms.dlg_export_package import Ui_ExportPackage



class ExportAsPackageDialog():

    def __init__(self):

        dialog = QtWidgets.QDialog()
        ui = Ui_ExportPackage()

        self.ui = ui
        self.dialog = dialog

        ui.setupUi(dialog)

        self.ui.pbExport.clicked.connect(self.export)
        self.ui.pbBrowse.clicked.connect(self.browse)


    def browse(self, *args):

        # open a file save-as dialog to get a .zip file
        # and set the text of the line edit to the selected file
        # if the user cancels, do nothing
        fileName = QFileDialog.getSaveFileName(None, "Save File",
                                                     "",
                                                     "DAVE package (*.zip)")

        if fileName[0]:
            self.ui.tbFile.setText(fileName[0])



    def export(self, *args):

        if self.ui.tbFile.text() == '':
            self.browse()
            if self.ui.tbFile.text() == '':
                self.ui.teLog.setPlainText('No file selected')
                return

        log = ["Exporting package..."]
        name = self.ui.tbFile.text()

        parts = Path(name)
        folder = parts.parent
        name = parts.stem

        filename, log = self.scene.create_standalone_copy(target_dir=folder,
                             filename = f"{name}.dave",
                             include_visuals=not self.ui.cbStripVisuals.isChecked(),
                             flatten=self.ui.cbFlatten.isChecked())


        text = '\n'.join(log)

        self.ui.teLog.setPlainText(text)

        if 'FAILED' in text:
            self.ui.teLog.setStyleSheet('color: red')
        else:
            self.ui.teLog.setStyleSheet('color: green')

            import platform
            if platform.system() == "Windows":
                import os
                os.startfile(folder)


        self.ui.teLog.verticalScrollBar().setValue(
            self.ui.teLog.verticalScrollBar().maximum()
        )  # scroll down all the way


    def show(self, scene, folder=None):
        self.scene = scene
        self.ui.teLog.clear()
        self.dialog.exec()


if __name__ == '__main__':

    # app = QtWidgets.QApplication()
    etb = ExportAsPackageDialog()

    class dummy:
        def create_standalone_copy(self, *args, **kwargs):
            return ['FAILED']


    etb.show(dummy())

