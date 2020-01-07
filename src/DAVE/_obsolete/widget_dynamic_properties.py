import DAVE.gui.forms.widget_dynprop
from PySide2 import QtWidgets
from PySide2.QtWidgets import QMainWindow, QApplication, QCheckBox
from DAVE.scene import Axis, Scene

class DynamicProperties:

    def __init__(self, scene, ui_target, run_code_func = None):
        """

        Args:
            scene : Scene
            ui_target : widget to create ui in
            run_code_func : callback function for running code
        """

        self.scene = scene
        self.run_code_func = run_code_func

        self.ui = DAVE.gui.forms.widget_dynprop.Ui_widget_dynprop()
        self.ui.setupUi(ui_target)

        self.fill_nodes_table()
        self.ui.tableDynProp.itemChanged.connect(self.node_table_cell_edit_done)

    def fill_nodes_table(self):

        # bodies = self.scene.nodes_of_type(RigidBody)
        axes = self.scene.nodes_of_type(Axis)
        self._filling_node_table = True

        for row, b in enumerate(axes):
            self.ui.tableDynProp.setRowCount(row+1)
            self.ui.tableDynProp.setVerticalHeaderItem(row,QtWidgets.QTableWidgetItem(b.name))

            cbs = list()
            for i in range(6):
                cbs.append(QCheckBox())
                self.ui.tableDynProp.setCellWidget(row,i,cbs[i])
                cbs[i].setChecked(b.fixed[i])
                self.ui.tableDynProp.setColumnWidth(i,24)
                cbs[i].node = b
                cbs[i].stateChanged.connect(self.node_table_cell_change_checkbox)
            b._checkboxes = cbs

            self.ui.tableDynProp.setItem(row, 6, QtWidgets.QTableWidgetItem(str(b.inertia)))

            for i in range(3):
                self.ui.tableDynProp.setItem(row, 7+i, QtWidgets.QTableWidgetItem(str(b.inertia_position[i])))
                self.ui.tableDynProp.setItem(row, 10+i, QtWidgets.QTableWidgetItem(str(b.inertia_radii[i])))

        self.ui.tableDynProp.resizeColumnsToContents()

        self._filling_node_table = False

    def node_table_cell_change_checkbox(self):
        if self._filling_node_table:
            return

        row = self.ui.tableDynProp.currentRow()
        name = self.ui.tableDynProp.verticalHeaderItem(row).text()
        node = self.scene[name]

        fixed = [cb.isChecked() for cb in node._checkboxes]

        # self._pause = True
        # self.scene._vfc.set_dofs(self.d0)
        code = 's["{}"].fixed = ({},{},{},{},{},{})'.format(name, *fixed)

        self.run_code_func(code)

    def node_table_cell_edit_done(self, data):
        if self._filling_node_table:
            return

        value = data.text()

        row = data.row()
        col = data.column()

        name = self.ui.tableDynProp.verticalHeaderItem(row).text()
        node = self.scene[name]

        code = ''

        if col == 6:  # inertia
            try:
                node.mass
                code = 's["{}"].mass = {}'.format(name, value)
                print('test')
            except:
                code = 's["{}"].inertia = {}'.format(name, value)
                print('test2')

        elif col in (7,8,9): # cog

            pos = [self.ui.tableDynProp.item(row,7).text(),
                   self.ui.tableDynProp.item(row,8).text(),
                   self.ui.tableDynProp.item(row,9).text()]

            try:
                node.mass
                code = 's["{}"].cog = ({},{},{})'.format(name, *pos)
            except:
                code = 's["{}"].inertia_position = ({},{},{})'.format(name, *pos)

        elif col in (10,11,12):  # cog

            pos = [self.ui.tableDynProp.item(row, 10).text(),
                   self.ui.tableDynProp.item(row, 11).text(),
                   self.ui.tableDynProp.item(row, 12).text()]

            code = 's["{}"].inertia_radii = ({},{},{})'.format(name, *pos)

        else:
            print('This column is not supposed to be edited')

        self.run_code_func(code)




# ====== main code - for testing and demonstration ======

if __name__ == '__main__':

    scene = Scene()
    scene.new_axis('test')

    app = QApplication()
    window = QMainWindow()
    p = DynamicProperties(scene=scene, ui_target=window, run_code_func=print)
    window.setCentralWidget(p.ui.widget)
    window.show()
    app.exec_()

