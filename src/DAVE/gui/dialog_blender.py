from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon
from PySide6 import QtWidgets

from DAVE.gui.forms.dlg_export_to_blender import Ui_Dialog
from DAVE.io.blender import create_blend_and_open
from DAVE.settings import BLENDER_BASE_SCENE, BLENDER_FPS

def try_get_blender_executable():

    import platform
    if platform.system().lower().startswith('win'):
        # on windows we can possibly get blender from the registry
        import winreg
        import os

        def find_blender_from_reg(where, key):
            try:
                pt = winreg.QueryValue(where, key)
                if pt:
                    if '%1' in pt:
                        pt = pt[1:-6]  # strip the %1

                    if os.path.exists(pt):
                        return pt
                    else:
                        pass
                        # print(f'Blender NOT found here {pt} as listed in {key}')
            except Exception as E:
                # print(f'Error when looking for blender here: {key} - {str(E)}')
                raise ValueError('Not found here')

        BLENDER_EXEC = None

        where_is_blender_in_the_registry = [
            (winreg.HKEY_CLASSES_ROOT, r'Applications\blender.exe\shell\open\command'),
            (winreg.HKEY_CLASSES_ROOT, r'Applications\blender-launcher.exe\shell\open\command'),
            (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Classes\Applications\blender-launcher.exe\shell\open\command'),
            (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Classes\Applications\blender-launcher.exe\shell\open\command'),
            (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Classes\blendfile\shell\open\command'),
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Classes\blendfile\shell\open\command')

        ]

        for possibility in where_is_blender_in_the_registry:
            try:
                BLENDER_EXEC = find_blender_from_reg(*possibility)
            except:
                pass

        # find it in a path
        # by default the windows-store version seems to be installed in a location which is in the path

        if BLENDER_EXEC == None:

            paths = os.environ['PATH'].split(';')
            for pth in paths:
                test = pth + r'\\blender-launcher.exe'
                if os.path.exists(test):
                    BLENDER_EXEC = test
                    break

        if BLENDER_EXEC:
            print("Blender found at: {}".format(BLENDER_EXEC))
        else:
            print("! Blender not found - Blender can be installed from the microsoft windows store."
                  "   if you have blender already and want to be able to use blender then please either:\n"
                  "   - configure windows to open .blend files with blender automatically \n"
                  "   - add the folder containing blender-launcher.exe to the PATH variable.")

            return "Blender can not be found automatically"

        # print('\nLoading DAVE...')
    else:  # assume we're on linux
        BLENDER_EXEC = 'blender'

    return BLENDER_EXEC

class ExportToBlenderDialog():

    def __init__(self):

        dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()

        self.ui = ui
        self.dialog = dialog


        ui.setupUi(dialog)

        self.ui.sbFrames_per_step.setValue(BLENDER_FPS)

        self.settings = QSettings("rdbr", "DAVE")

        blender_executable = self.settings.value(f"blender_executable")
        if blender_executable is None:
            blender_executable = try_get_blender_executable()

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

        self.ui.btnOK.setText("Working - background task is being prepared...")
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

        # do export animation?
        if self.ui.radioButton_2.isChecked():
            animation_dofs = self.animation_dofs
        else:
            animation_dofs = None

        # execute blender
        create_blend_and_open(
            self.scene, animation_dofs=self.animation_dofs, wavefield=self.wavefield,
            blender_base_file=template, blender_exe_path=executable, frames_per_step=self.ui.sbFrames_per_step.value()
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

    from DAVE.scene import Scene
    from DAVE.nodes import Frame, Visual

    s = Scene()
    s.new_frame('frame')
    s.new_visual('vis',path='res: cube.obj', parent='frame')

    etb.show(s)

