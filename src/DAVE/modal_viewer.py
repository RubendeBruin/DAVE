from DAVE.scene import Scene
from DAVE.visual import Viewport
from DAVE.forms.frm_animation import Ui_AnimationWindow
import sys
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
app = QtWidgets.QApplication(sys.argv)
AnimationWindow = QtWidgets.QMainWindow()
ui = Ui_AnimationWindow()
ui.setupUi(AnimationWindow)

class ModalViewer:

    def __init__(self, scene, shapes, omegas):
        
        self.shapes = shapes
        self.omega = omegas
        self._pause = False
        self.n_frames = 240
        self.time = 0
        self.dt = 1
        self.endTime = 240
        self.n_shapes = len(omegas)
        
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

        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui.setupUi(self.MainWindow)

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

        self.generateModeShape(0,1)

        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver('TimerEvent', self.timerEvent)
        iren.CreateRepeatingTimer(round(100))

        self.MainWindow.show()
        self.app.aboutToQuit.connect(self.onClose)

        while True:
            try:
                self.app.exec_()
                break
            except Exception as E:
                print(E)

    def onClose(self):
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



