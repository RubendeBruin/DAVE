from pathlib import Path

from PySide2.QtCore import QSettings
from PySide2.QtGui import QIcon
from PySide2 import QtWidgets

from DAVE.gui.forms.dlg_export_to_blender import Ui_Dialog
from DAVE.io.blender import create_blend_and_open
from DAVE.settings import BLENDER_EXEC, BLENDER_BASE_SCENE


class ExportToBlenderDialog():

    def __init__(self):

        dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()

        self.ui = ui
        self.dialog = dialog


        ui.setupUi(dialog)

        self.settings = QSettings("rdbr", "DAVE")

        blender_executable = self.settings.value(f"blender_executable")
        if blender_executable is None:
            blender_executable = BLENDER_EXEC

        self.blender_templates = self.settings.value(f"blender_templates")
        if self.blender_templates is None:
            self.blender_templates = str(BLENDER_BASE_SCENE)
        self.blender_templates = self.blender_templates.split(';')

        ui.teExecutable.textChanged.connect(self.check_path)
        ui.cbBaseScene.currentTextChanged.connect(self.check_template_path)

        ui.teExecutable.setText(blender_executable)
        ui.cbBaseScene.addItems(self.blender_templates)

        self.ui.btnOK.pressed.connect(self.export)
        self.ui.btnCancel.pressed.connect(self.dialog.close)

    def check_path(self, *args):
        path = self.ui.teExecutable.text()
        if Path(path).exists():
            self.ui.teExecutable.setStyleSheet('color: rgb(0,100,0)')
        else:
            self.ui.teExecutable.setStyleSheet('color: rgb(200,0,25)')

    def check_template_path(self, *args):
        path = self.ui.cbBaseScene.currentText()
        if Path(path).exists():
            self.ui.cbBaseScene.setStyleSheet('color: rgb(0,100,0)')
        else:
            self.ui.cbBaseScene.setStyleSheet('color: rgb(200,0,25)')

    def export(self, *args):

        self.ui.btnOK.setText("Working")
        QtWidgets.QApplication.processEvents()

        template = self.ui.cbBaseScene.currentText()
        executable = self.ui.teExecutable.text()

        # save settings
        templates = self.blender_templates  # list
        if template in templates:
            templates.remove(template)
        templates.insert(0,template)

        self.settings.setValue('blender_templates', ';'.join(templates))
        self.settings.setValue('blender_executable', executable)

        # execute blender
        create_blend_and_open(
            self.scene, animation_dofs=self.animation_dofs, wavefield=self.wavefield,
            blender_base_file=template, blender_exe_path=executable
        )

        # and close
        self.dialog.close()


    def show(self, scene, animation_dofs=None, wavefield=None):
        self.ui.btnOK.setText("Export")
        self.scene = scene
        self.animation_dofs = animation_dofs
        self.wavefield = wavefield
        self.dialog.exec_()


if __name__ == '__main__':

    app = QtWidgets.QApplication()
    etb = ExportToBlenderDialog()
    etb.show(None)

