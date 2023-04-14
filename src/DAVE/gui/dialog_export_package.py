from pathlib import Path

from PySide2.QtCore import QSettings
from PySide2.QtGui import QIcon
from PySide2 import QtWidgets
from PySide2.QtWidgets import QFileDialog

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

        self.ui.tbFolder.textChanged.connect(self.folder_changed)

    def folder_changed(self, *args):
        folder = self.ui.tbFolder.text()

        try:
            folder = Path(folder)
            if not folder.parent.exists():
                raise ValueError('parent folder does not exist')
            self.ui.tbFolder.setStyleSheet('')
            self.ui.pbExport.setEnabled(True)
        except:
            self.ui.tbFolder.setStyleSheet('background: pink')
            self.ui.pbExport.setEnabled(False)


    def browse(self, *args):
        folder = QFileDialog.getExistingDirectory(dir = self.ui.tbFolder.text())
        if folder:
            self.ui.tbFolder.setText(folder)


    def export(self, *args):
        log = self.scene.create_standalone_copy(target_dir=self.ui.tbFolder.text(),
                         filename = 'exported.dave',
                         include_visuals=not self.ui.cbStripVisuals.isChecked(),
                         zip=self.ui.cbZip.isChecked(),
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
                os.startfile(self.ui.tbFolder.text())


        self.ui.teLog.verticalScrollBar().setValue(
            self.ui.teLog.verticalScrollBar().maximum()
        )  # scroll down all the way


    def show(self, scene, folder=None):
        self.scene = scene
        if folder is None:
            folder = r'c:\data\DAVE'
        self.ui.tbFolder.setText(folder)
        self.ui.teLog.clear()
        self.dialog.exec_()


if __name__ == '__main__':

    app = QtWidgets.QApplication()
    etb = ExportAsPackageDialog()

    class dummy:
        def create_standalone_copy(self, *args, **kwargs):
            return ['FAILED']


    etb.show(dummy())

