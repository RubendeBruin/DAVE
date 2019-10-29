from DAVE.scene import Scene, RigidBody
from DAVE.visual import Viewport
from DAVE.forms.frm_animation import Ui_AnimationWindow
import dynamics.frequency_domain
from dynamics.frequency_domain import PointMass
import sys
import numpy as np
from scipy.linalg import eig

from PyQt5 import QtCore, QtGui, QtWidgets
# app = QtWidgets.QApplication(sys.argv)
# AnimationWindow = QtWidgets.QMainWindow()
# ui = Ui_AnimationWindow()
# ui.setupUi(AnimationWindow)

class ModalViewer:

    def __init__(self, scene, app=None):
        

        self._pause = False
        self.n_frames = 240
        self.time = 0
        self.dt = 1
        self.endTime = 240

        
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
        self.ui.horizontalSlider.actionTriggered.connect(self.new_mode_shape)
        self.ui.horizontalSlider_2.setSliderPosition(10)
        self.ui.horizontalSlider_2.actionTriggered.connect(self.new_mode_shape)

        #

        self._pause = True
        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver('TimerEvent', self.timerEvent)
        self.timerid = iren.CreateRepeatingTimer(round(100))


        self.fill_table()
        self.update_point_masses()
        self.calculate_modeshapes()

        if self.n_shapes > 0:
            self.generateModeShape(0, 1)
        else:
            self.ui.label_3.setText("No mode-shapes found")

        self.ui.pushButton.clicked.connect(self.recalc)


        self.app.aboutToQuit.connect(self.onClose)
        self.MainWindow.show()

        while True:
            try:
                self.app.exec_()
                break
            except Exception as E:
                print(E)

    def recalc(self):
        self._pause = True
        self.update_point_masses()
        self.calculate_modeshapes()

    def fill_table(self):
        rows = -1
        for b in self.scene.nodes_of_type(RigidBody):
            rows += 1
            self.ui.tableWidget.setRowCount(rows+1)
            self.ui.tableWidget.setItem(rows,0, QtWidgets.QTableWidgetItem(b.name))
            self.ui.tableWidget.setItem(rows,1, QtWidgets.QTableWidgetItem(str(b.mass)))

            try:
                rs = b.radii_of_gyration
            except:
                rs = (0,0,0)

            self.ui.tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(rs[0])))
            self.ui.tableWidget.setItem(rows, 3, QtWidgets.QTableWidgetItem(str(rs[1])))
            self.ui.tableWidget.setItem(rows, 4, QtWidgets.QTableWidgetItem(str(rs[2])))

    def update_point_masses(self):

        self.ui.label_3.setText("")
        for node in list(self.scene.nodes):
            if isinstance(node, PointMass):
                self.scene.nodes.remove(node)

        for row in range(self.ui.tableWidget.rowCount()):
            name = self.ui.tableWidget.item(row,0).text()
            mass = float(self.ui.tableWidget.item(row,1).text())

            if mass <= 0:
                print('Zero mass encountered')
                continue

            rxx = float(self.ui.tableWidget.item(row,2).text())
            ryy = float(self.ui.tableWidget.item(row, 3).text())
            rzz = float(self.ui.tableWidget.item(row, 4).text())

            # deconstruct into six point masses

            Ixx = mass * rxx ** 2
            Iyy = mass * ryy ** 2
            Izz = mass * rzz ** 2

            rxx2 = (Ixx / mass)
            ryy2 = (Iyy / mass)
            rzz2 = (Izz / mass)

            # checks
            try:
                if rxx2 > ryy2 + rzz2:
                    raise Exception('Ixx should be < Iyy + Izz')
                if ryy2 > rxx2 + rzz2:
                    raise Exception('Iyy should be < Ixx + Izz')
                if rzz2 > rxx2 + rzz2:
                    raise Exception('Izz should be < Ixx + Iyy')
            except Exception as ME:
                self.ui.label_3.setText(str(ME))
                return

            x = np.sqrt(0.5 * (-rxx2 + ryy2 + rzz2)) * np.sqrt(3)
            y = np.sqrt(0.5 * (rxx2 - ryy2 + rzz2)) * np.sqrt(3)
            z = np.sqrt(0.5 * (rxx2 + ryy2 - rzz2)) * np.sqrt(3)

            m = mass / 6

            Ixxc = 2 * (y ** 2 + z ** 2) * m
            Iyyc = 2 * (x ** 2 + z ** 2) * m
            Izzc = 2 * (x ** 2 + y ** 2) * m

            print('{} =?= {}'.format(Ixx, Ixxc))
            print('{} =?= {}'.format(Iyy, Iyyc))
            print('{} =?= {}'.format(Izz, Izzc))

            # Add the point masses
            ps = list()
            ps.append([x,0,0])
            ps.append([-x, 0,0])
            ps.append([0, y, 0])
            ps.append([0, -y, 0])
            ps.append([0, 0, z])
            ps.append([0,0 , -z])

            for p in ps:
                pm = PointMass(self.scene)
                b = self.scene[name]
                pm.parent = b
                pm.mass = m
                pm.offset = (b.cogx + p[0], b.cogy + p[1], b.cogz + p[2])
                self.scene.nodes.append(pm)
                print('added pm of {} at {} {} {} on {}'.format(m, *pm.offset, b.name))

    def calculate_modeshapes(self):
        M = dynamics.frequency_domain.M(self.scene)
        print("Mass matrix")
        print(M)
        K = self.scene._vfc.K(0.1)
        K = -K
        print("Stiffness matrix")
        print(K)

        if K.size>0:
            V, D = eig(K, M)

            print("Values = ")
            print(V)
            print("Directions = ")
            print(D)

            self.shapes = D
            self.omega = V
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
        text = '{:.2f} rad/s | {:.2f} s'.format(omega, 2*np.pi / omega)

        self.ui.lblInfo.setText(text)
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
        self._pause = True
        self.animation_dofs = list()
        for i_frame in range(self.n_frames):
            d = np.array(self.d0)
            displ = self.shapes[:, i_shape]
            frame_dofs = d + np.sin(2 * 3.14159 * i_frame / self.n_frames) * displ * scale
            self.animation_dofs.append(frame_dofs)
        self._pause = False

# ====== main code ======

if __name__ == '__main__':
    s = Scene()

    # ---
    s.import_scene(s.get_resource_path("cheetah.pscene"), containerize=False, prefix="")

    s.solve_statics()

    window = ModalViewer(s)