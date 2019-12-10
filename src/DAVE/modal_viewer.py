from DAVE.scene import Scene, RigidBody, Axis
from DAVE.visual import Viewport
from DAVE.forms.frm_animation import Ui_AnimationWindow
import DAVE.frequency_domain
# from dynamics.frequency_domain import PointMass
import sys
import numpy as np
from scipy.linalg import eig
from PySide2.QtGui import QBrush, QColor

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QCheckBox

from IPython.utils.capture import capture_output

from DAVE.widget_dynamic_properties import DynamicProperties

class MainWindowWithCloseEvent(QtWidgets.QMainWindow):

    def closeEvent(self, other):
        print('closing qt interactor and timer of modal_viewer window')
        iren = self.visual.renwin.GetInteractor()
        iren.DestroyTimer(self.timerid)
        self.visual.shutdown_qt()


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
            self.MainWindow = QtWidgets.QMainWindow()
        else:
            self.app = app
            self.MainWindow = MainWindowWithCloseEvent() # QtWidgets.QDialog()

        self.ui.setupUi(self.MainWindow)

        self.visual.quick_updates_only = True
        self.visual.create_visuals(recreate=True)
        self.visual.position_visuals()

        self.MainWindow.visual = self.visual # reference for the close event

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

        # ui = DAVE.forms.widget_dynprop.Ui_widget_dynprop()
        # ui.setupUi(self.ui.dockWidgetContents_4)
        # self.ui.dockWidgetContents_4.layout().addWidget(ui.widget)
        # self.ui.tableDynProp = ui.tableDynProp
        # self.ui.tableDynProp.itemChanged.connect(self.node_table_cell_edit_done)

        def dyn_table_run_code(code):
            self._pause = True
            self.scene._vfc.set_dofs(self.d0)
            self._runcode(code)
            self.d0 = self.scene._vfc.get_dofs()
            self.calculate_modeshapes()
            self.fill_result_table()

        self.dynprop = DynamicProperties(scene=self.scene, ui_target=self.ui.dockWidgetContents_4, run_code_func=dyn_table_run_code)

        #
        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver('TimerEvent', self.timerEvent)
        self.timerid = iren.CreateRepeatingTimer(round(100))
        self.MainWindow.timerid = self.timerid # for close event

        self.fill_result_table()
        self.dynprop.fill_nodes_table()
        self.calculate_modeshapes()

        if self.n_shapes > 0:
            self.generateModeShape(0, 1)
        else:
            self.ui.label_3.setText("No mode-shapes found")

        self.ui.pushButton.clicked.connect(self.recalc)
        self.ui.pushButton_2.clicked.connect(self.quickfix)
        self.ui.btnStatics.clicked.connect(self.solvestatics)

        if app is not None:
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
        self.calculate_modeshapes()
        self.fill_results_table_with(summary)
        self.dynprop.fill_nodes_table()
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

            self.ui.tableWidget.setItem(rows, 3, QtWidgets.QTableWidgetItem('{:.3e}'.format(b['total_inertia'])))
            self.ui.tableWidget.setItem(rows, 4, QtWidgets.QTableWidgetItem('{:.3e}'.format(b['stiffness'])))
            self.ui.tableWidget.setItem(rows, 5, QtWidgets.QTableWidgetItem(b['unconstrained']))
            self.ui.tableWidget.setItem(rows, 6, QtWidgets.QTableWidgetItem(b['noinertia']))





        self._filling_table = False

    def calculate_modeshapes(self):

        # V,D = dynamics.frequency_domain.mode_shapes(self.scene)
        #
        # if V is not None:
        #     self.shapes = D
        #     self.omega = np.real(np.sqrt(V))
        #     self.n_shapes = len(V)
        # else:
        #     self.n_shapes = 0
        #
        # self.ui.horizontalSlider.setMaximum(self.n_shapes-1)

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
            if m>0 and abs(d)>0:
                factor = 0.5 + 0.5*abs(d) / m
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
    s.import_scene(s.get_resource_path("pendulum.dave_asset"), containerize=False, prefix="")
    # s.import_scene(s.get_resource_path("cheetah with crane.dave_asset"), containerize=False, prefix="")
    # s.import_scene(s.get_resource_path("cheetah.dave_asset"), containerize=False, prefix="")

    s.solve_statics()
    window = ModalViewer(s)