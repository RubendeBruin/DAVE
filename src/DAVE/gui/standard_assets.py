"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019


    This is the asset-browser dialog.

"""

import DAVE.visual as dv
import DAVE.scene as ds

import DAVE.gui.forms.frm_standard_assets

from PySide2 import QtWidgets


class DialogWithCloseEvent(QtWidgets.QDialog):

    def closeEvent(self, other):
        print('closing qt interactor of import window')
        self.visual.shutdown_qt()



class Gui:

    def __init__(self):
        self.scene = ds.Scene()
        """Reference to a scene"""
        self.visual = dv.Viewport(self.scene)
        """Reference to a viewport"""

        self.ui = DAVE.gui.forms.frm_standard_assets.Ui_MainWindow()
        """Reference to the ui"""
        self.ui.visual = self.visual # pass a reference

        self._selected = None
        self._result = None

        # self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = DialogWithCloseEvent() # QtWidgets.QDialog()
        self.ui.setupUi(self.MainWindow)

        txt = "Resources from:\n"
        for p in self.scene.resources_paths:
            txt += '\n' + str(p)
        self.ui.lblInfo.setText(txt)

        res = self.scene.get_resource_list('.dave')

        for r in res:
            self.ui.listWidget.addItem(str(r))

        self.ui.listWidget.itemSelectionChanged.connect(self.changed)
        self.ui.listWidget.itemDoubleClicked.connect(self.dblclick)
        self.visual.show_embedded(self.ui.frame3d)
        self.ui.btnImport.clicked.connect(self.clickImport)

        self.MainWindow.visual = self.visual # pass reference of onClose


    def changed(self):
        self.select(self.ui.listWidget.currentItem())

    def select(self, data):
        file = data.text()
        self._selected = file
        self.ui.btnImport.setText("Import {}".format(file[:-5])) # remove the .dave part

    def dblclick(self, data):
        self.select(data)
        file = data.text()
        self.scene.clear()
        try:
            self.scene.load_scene(self.scene.get_resource_path(file))
        except Exception as M:
            print(M)
            print('Error when loading file {}'.format(file))
            return

        self.visual.create_visuals()
        self.visual.add_new_actors_to_screen()
        self.visual.position_visuals()
        self.visual.update_visibility()
        self.visual.zoom_all()
        self.visual.refresh_embeded_view()


    def clickImport(self):
        if self._selected is None:
            self._result = None
        else:
            self._result =  (self._selected, self.ui.checkBox.isChecked(), self.ui.txtPrefix.text())
        self.MainWindow.close()

    def showModal(self):
        self.MainWindow.exec_()
        return self._result

# ====== nodeA code ======

if __name__ == '__main__':

    G = Gui().show()
