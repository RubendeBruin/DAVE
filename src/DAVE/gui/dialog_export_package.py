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

        self.ui.tbFolder.textChanged.connect(self.folder_changed)
        self.ui.tbName.textChanged.connect(self.folder_changed)

    def folder_changed(self, *args):
        folder = self.ui.tbFolder.text()

        self.ui.lblInfo.setStyleSheet('')

        try:
            folder = Path(folder)
            if not folder.parent.exists():
                raise ValueError('parent folder does not exist')
            self.ui.tbFolder.setStyleSheet('')


            folder = Path(self.ui.tbFolder.text()) / self.ui.tbName.text()
            if folder.exists():
                self.ui.tbName.setStyleSheet('background: pink')
                self.ui.pbExport.setEnabled(False)
                self.ui.lblInfo.setText(f"{folder} already exists, please choose another name or folder")
                self.ui.lblInfo.setStyleSheet('background: pink')
                raise ValueError('folder already exists')
            else:
                self.ui.tbName.setStyleSheet('')

            self.ui.pbExport.setEnabled(True)
            self.ui.lblInfo.setText(f"Export to {folder}")

        except:
            self.ui.tbFolder.setStyleSheet('background: pink')
            self.ui.pbExport.setEnabled(False)

            self.ui.tbName.setStyleSheet('background: pink')
            self.ui.pbExport.setEnabled(False)




    def browse(self, *args):
        folder = QFileDialog.getExistingDirectory(dir = self.ui.tbFolder.text())
        if folder:
            self.ui.tbFolder.setText(folder)


    def export(self, *args):

        log = ["Exporting package..."]
        name = self.ui.tbName.text()

        # create folder
        try:
            folder = Path(self.ui.tbFolder.text()) / name
            folder.mkdir(exist_ok=False)



            log.append(f"Created folder {folder}")

            log.extend(self.scene.create_standalone_copy(target_dir=folder,
                             filename = f"{name}.dave",
                             include_visuals=not self.ui.cbStripVisuals.isChecked(),
                             zip=self.ui.cbZip.isChecked(),
                             flatten=self.ui.cbFlatten.isChecked()))
        except Exception as e:
            log.extend([f'FAILED with {e}'])

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
            folder = r'c:\data'
        self.ui.tbFolder.setText(folder)
        self.ui.tbName.setText("demo")
        self.ui.teLog.clear()
        self.dialog.exec()


if __name__ == '__main__':

    app = QtWidgets.QApplication()
    etb = ExportAsPackageDialog()

    class dummy:
        def create_standalone_copy(self, *args, **kwargs):
            return ['FAILED']


    etb.show(dummy())

