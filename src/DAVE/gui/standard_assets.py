"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


    This is the asset-browser dialog.

"""

import DAVE.scene as ds

import DAVE.gui.forms.frm_standard_assets

from PySide6 import QtWidgets

from DAVE.settings_visuals import PAINTERS
from DAVE.visual_helpers.qt_embedded_renderer import QtEmbeddedSceneRenderer


class DialogWithCloseEvent(QtWidgets.QDialog):
    def closeEvent(self, other):
        print("closing qt interactor of import window")
        self.visual.shutdown_qt()


class Gui:
    def __init__(self):
        self.scene = ds.Scene()




        self.ui = DAVE.gui.forms.frm_standard_assets.Ui_MainWindow()

        self._selected = None
        self._result = None

        self.MainWindow = DialogWithCloseEvent()  # QtWidgets.QDialog()
        self.ui.setupUi(self.MainWindow)

        """Reference to a scene"""
        self.visual = QtEmbeddedSceneRenderer(self.scene, self.ui.frame3d)
        self.visual.settings.show_sea = False
        self.visual.settings.painter_settings = PAINTERS["Visual"]

        txt = "Resources from:\n"
        for p in self.scene.resource_provider.resources_paths:
            txt += "\n" + str(p)
        self.ui.lblInfo.setText(txt)

        res = self.scene.get_resource_list(".dave")

        for r in res:
            self.ui.listWidget.addItem(str(r))

        self.ui.listWidget.itemSelectionChanged.connect(self.changed)
        self.ui.listWidget.itemDoubleClicked.connect(self.dblclick)
        self.ui.btnImport.clicked.connect(self.clickImport)

        self.MainWindow.visual = self.visual  # pass reference of onCloseApplication

        self.ui.lineEdit.textChanged.connect(self.filter)
        self.ui.pbCancel.pressed.connect(self.cancel)

    def changed(self):
        self.select(self.ui.listWidget.currentItem())

    def select(self, data):
        file = data.text()
        self._selected = file
        self.ui.btnImport.setText(
            "Import {}".format(file[:-5])
        )  # remove the .dave part

        file = data.text()
        self.scene.clear()
        try:
            self.scene.load_scene(self.scene.get_resource_path(file))
            self.ui.lbInfo.setText("Loaded: {}".format(file))
        except Exception as M:
            print(M)
            self.ui.lbInfo.setText("Error when loading file {}".format(file))
            return

        self.visual.create_node_visuals()
        self.visual.add_new_node_actors_to_screen()
        self.visual.position_visuals()
        self.visual.update_visibility()
        self.visual.zoom_all()
        self.visual.refresh_embeded_view()

    def dblclick(self, data):
        self.select(data)
        self.clickImport()

    def clickImport(self):
        if self._selected is None:
            self._result = None
        else:
            self._result = (
                self._selected,
                self.ui.checkBox.isChecked(),
                self.ui.txtPrefix.text(),
            )
        self.MainWindow.close()

    def cancel(self):
        self._result = None
        self.MainWindow.close()

    def showModal(self):
        self.MainWindow.exec_()
        return self._result

    def filter(self):
        look_for = self.ui.lineEdit.text()
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            item.setHidden(not look_for in item.text())



if __name__ == "__main__":

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    G = Gui()
    G.showModal()
