"""
GUI

The GUI can be created from a scene



"""

import DAVE.visual as dv
import DAVE.scene as ds
import DAVE.constants as dc

import DAVE.frm_standard_assets

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import QMimeData, Qt
from PyQt5 import QtCore

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QFileDialog

class window_with_close_event(DAVE.frm_standard_assets.Ui_MainWindow):

    def closeEvent(self):
        self.visual.shutdown_qt()



class Gui:

    def __init__(self):
        self.scene = ds.Scene()
        """Reference to a scene"""
        self.visual = dv.Viewport(self.scene)
        """Reference to a viewport"""

        self.ui = window_with_close_event()
        """Reference to the ui"""
        self.ui.visual = self.visual # pass a reference

        self._selected = None
        self._result = None

        # self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QDialog()
        self.ui.setupUi(self.MainWindow)

        txt = "Resources from:\n"
        for p in self.scene.resources_paths:
            txt += '\n' + p
        self.ui.lblInfo.setText(txt)

        res = self.scene.get_resource_list('.pscene')

        for r in res:
            self.ui.listWidget.addItem(r)

        self.ui.listWidget.itemSelectionChanged.connect(self.changed)
            #(self.select)
        self.ui.listWidget.itemDoubleClicked.connect(self.dblclick)

        self.visual.show_embedded(self.ui.frame3d)

        self.ui.btnImport.clicked.connect(self.clickImport)


    def changed(self):
        self.select(self.ui.listWidget.currentItem())

    def select(self, data):
        file = data.text()
        self._selected = file
        self.ui.btnImport.setText("Import {}".format(file[:-7])) # remove the .pscene part

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

# ====== main code ======

if __name__ == '__main__':

    G = Gui().show()
