from DAVE.scene import Scene, RigidBody, Axis
from DAVE.visual import Viewport
from DAVE.forms.frm_animation import Ui_AnimationWindow
import dynamics.frequency_domain
# from dynamics.frequency_domain import PointMass
import sys
import numpy as np
from scipy.linalg import eig
from PySide2.QtGui import QBrush, QColor

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QCheckBox

from IPython.utils.capture import capture_output


# app = QtWidgets.QApplication(sys.argv)
# AnimationWindow = QtWidgets.QMainWindow()
# ui = Ui_AnimationWindow()
# ui.setupUi(AnimationWindow)

class ModalViewer:

    def __init__(self, scene, app=None):
        self._pause = True
        self._filling_table = True
        self._filling_node_table = True
        self.n_frames = 480
        self.time = 0
        self.dt = 1
        self.endTime = 480

        
        self.scene = scene
        """Reference to a scene"""
        self.visual = Viewport(scene)
        """Reference to a viewport"""
        
        self.eCore = scene._vfc
        self.eCore.state_update()
        self.d0 = self.eCore.get_dofs()
        self.n = len(self.d0)

        self.ui = Ui_AnimationWindow()
        """Reference to the ui"""

        if app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        else:
            self.app = app

        self.MainWindow = QtWidgets.QMainWindow()
        self.ui.setupUi(self.MainWindow)

        self.visual.quick_updates_only = True
        self.visual.create_visuals(recreate=True)
        self.visual.position_visuals()

        # -------------- Create the 3d view

        self.MainWindow.setCentralWidget(self.ui.frame3d)
        self.visual.show_embedded(self.ui.frame3d)
        self.visual.update_visibility()

        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver('TimerEvent', self.timerEvent)

        self.ui.horizontalSlider.setMaximum(self.n-1)
        self.ui.horizontalSlider.setMinimum(- 1)
        self.ui.horizontalSlider.actionTriggered.connect(self.new_mode_shape)
        self.ui.horizontalSlider_2.setSliderPosition(10)
        self.ui.horizontalSlider_2.actionTriggered.connect(self.new_mode_shape)

        self.ui.tableWidget.currentItemChanged.connect(self.cell_edit_start)
        self.ui.tableWidget.itemChanged.connect(self.cell_edit_done)

        self.ui.tableDynProp.itemChanged.connect(self.node_table_cell_edit_done)

        #
        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver('TimerEvent', self.timerEvent)
        self.timerid = iren.CreateRepeatingTimer(round(100))

        self.fill_result_table()
        self.fill_nodes_table()
        self.calculate_modeshapes()

        if self.n_shapes > 0:
            self.generateModeShape(0, 1)
        else:
            self.ui.label_3.setText("No mode-shapes found")

        self.ui.pushButton.clicked.connect(self.recalc)
        self.ui.pushButton_2.clicked.connect(self.quickfix)


        self.app.aboutToQuit.connect(self.onClose)
        self.MainWindow.show()

        while True:
            try:
                self.app.exec_()
                break
            except Exception as E:
                print(E)


    def _runcode(self, code):
        s = self.scene

        print('Running code:')
        print(code)

        with capture_output() as c:
            try:
                exec(code)
                if c.stdout:
                    print(c.stdout)
                else:
                    print('done')

                return True

            except Exception as E:
                print('ERROR')
                print(c.stdout + '\n' + str(E) + '\n\nWhen running: \n\n' + code)
                print('/ERROR')
                return False

    # ===================== Nodes table =============================

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

        self._pause = True
        self.scene._vfc.set_dofs(self.d0)
        code = 's["{}"].fixed = ({},{},{},{},{},{})'.format(name, *fixed)


        print(code)

        self._runcode(code)
        self.scene._vfc.state_update()
        self.d0 = self.scene._vfc.get_dofs()

        self.fill_result_table()


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

        if not self._runcode(code):
            print("there was an error running the code")

        self.fill_result_table()

    # ===================== results table ===========================

    def cell_edit_start(self, data):
        if self._filling_table:
            return
        try:
            self._celldata = data.text()
        except:
            pass



    def cell_edit_done(self, data):
        if self._filling_table:
            return

        row = data.row()
        col = data.column()

        # name = self.ui.tableWidget.item(row, 1).text()
        name = self.ui.tableWidget.verticalHeaderItem(row).text()
        node = self.scene[name]
        mode = int(self.ui.tableWidget.item(row, 1).text())

        if col == 2:  # inertia
            I = float(data.text())

            if isinstance(node, RigidBody):
                node.mass = I
            else:
                node.inertia = I

            self.fill_result_table()
            return

        elif col == 3: # radius
            r = float(data.text())
            if mode > 2:
                temp = node.inertia_radii
                temp[mode - 3] = r
                node.inertia_radii = temp
                self.fill_result_table()
                return

        data.setText(self._celldata)

    def recalc(self):
        self._pause = True
        self.fill_result_table()
        self.calculate_modeshapes()

    def quickfix(self):
        self._pause = True
        summary = dynamics.frequency_domain.dynamics_quickfix(self.scene)
        self.fill_results_table_with(summary)
        self.fill_nodes_table()
        self.calculate_modeshapes()
        self._pause = False


    def fill_result_table(self):
        self.scene._vfc.set_dofs(self.d0)
        summary = dynamics.frequency_domain.dynamics_summary_data(self.scene)
        self.fill_results_table_with(summary)

    def fill_results_table_with(self, summary):
        self._filling_table = True
        rows = -1
        factor = 0.3
        color = QColor.fromRgb(255 - 100 * factor, 255 - 100 * factor, 255)

        for b in summary:
            rows += 1

            mode = b['mode']
            name = b['node'] + ' mode:' + str(mode)
            node = self.scene[b['node']]

            self.ui.tableWidget.setRowCount(rows+1)
            self.ui.tableWidget.setVerticalHeaderItem(rows, QtWidgets.QTableWidgetItem(name))
            self.ui.tableWidget.setItem(rows, 1, QtWidgets.QTableWidgetItem('{:e}'.format(node.inertia)))

            if mode>2:
                self.ui.tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem('{:e}'.format(node.inertia_radii[mode-3])))
                self.ui.tableWidget.item(rows, 2).setBackground(QBrush(color))
            else:
                self.ui.tableWidget.item(rows, 1).setBackground(QBrush(color))
                self.ui.tableWidget.setItem(rows, 2,
                                            QtWidgets.QTableWidgetItem('n/a'))

            self.ui.tableWidget.setItem(rows, 3, QtWidgets.QTableWidgetItem('{:.3e}'.format(b['child_inertia'])))
            self.ui.tableWidget.setItem(rows, 4, QtWidgets.QTableWidgetItem('{:.3e}'.format(b['stiffness'])))
            self.ui.tableWidget.setItem(rows, 5, QtWidgets.QTableWidgetItem(b['unconstrained']))
            self.ui.tableWidget.setItem(rows, 6, QtWidgets.QTableWidgetItem(b['noinertia']))





        self._filling_table = False

    def calculate_modeshapes(self):

        V,D = dynamics.frequency_domain.mode_shapes(self.scene)

        if V is not None:
            self.shapes = D
            self.omega = np.real(np.sqrt(V))
            self.n_shapes = len(V)
        else:
            self.n_shapes = 0

    def onClose(self):
        iren = self.visual.renwin.GetInteractor()
        iren.DestroyTimer(self.timerid)
        self.visual.shutdown_qt()
        print('closing')

    def new_mode_shape(self):
        i = self.ui.horizontalSlider.sliderPosition()
        scale = self.ui.horizontalSlider_2.sliderPosition() + 1
        scale = 1.05**(scale-30)
        print('Activating mode-shape {} with scale {}'.format(i,scale))

        omega = self.omega[i]
        self.ui.lblPeriod.setText('{:.2f} s'.format(2*np.pi / omega))
        self.ui.lblRads.setText('{:.2f} rad/s'.format(omega))
        self.generateModeShape(i,scale)



    def timerEvent(self,a,b):
        if self._pause:
            return

        self.time += self.dt
        # print(self.time)
        
        low = round(self.time - 0.5)
        high = round(self.time + 0.5)
        
        if self.time > self.n_frames-1:
            self.time -= self.n_frames

        if high > self.n_frames-1:
            high -= self.n_frames
        if low > self.n_frames-1:
            low -= self.n_frames

        before = self.animation_dofs[low]
        after = self.animation_dofs[high]

        f1 = self.time - low
        f2 = 1 - f1
        dofs = f2 * before + f1 * after

        self.eCore.set_dofs(dofs)
        self.visual.position_visuals()
        self.visual.refresh_embeded_view()
    
    def generateModeShape(self,i_shape,scale):
        """An i_shape < 0 will generate the static position"""
        self._pause = True
        self._filling_table = True
        self.animation_dofs = list()

        d = np.array(self.d0)

        if i_shape>=0:
            displ = self.shapes[:, i_shape]
            # displ = np.real(displ)
        else:
            displ = 0*d # zero displacement


        # update exitation row in table
        for i,d in enumerate(displ):
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem('{:.2f}'.format(d)))
            cell = self.ui.tableWidget.item(i, 0)
            if cell is None:
                continue
            m = np.max(np.abs(displ))
            if m>0:
                factor = abs(d) / m
            else:
                factor=0
            color = QColor.fromRgb(255-100*factor,255-100*factor,255)
            cell.setBackground(QBrush(color))


        for i_frame in range(self.n_frames):

            change = np.sin(2 * 3.14159 * i_frame / self.n_frames) * displ * scale
            self.eCore.set_dofs(self.d0)

            t0 = self.eCore.get_dofs()
            # self.eCore.state_update()
            t1 = self.eCore.get_dofs()

            self.eCore.change_dofs(change)

            t2 = self.eCore.get_dofs()
            # self.eCore.state_update()
            t3 = self.eCore.get_dofs()

            d_d0 = np.array(t1)-np.array(t0)
            d_update = np.array(t2) - np.array(t3)

            if np.any(d_d0):
                print('difference in step0')
            if np.any(d_update):
                print('difference in update')


            self.animation_dofs.append(self.eCore.get_dofs())

        self._pause = False
        self._filling_table = False

# ====== main code ======

if __name__ == '__main__':
    s = Scene()

    # from DAVE.gui import Gui
    # s.import_scene(s.get_resource_path("pendulum.dave_asset"), containerize=False, prefix="")
    s.import_scene(s.get_resource_path("cheetah with crane.dave_asset"), containerize=False, prefix="")
    # Gui(s).show()

    s.solve_statics()
    window = ModalViewer(s)