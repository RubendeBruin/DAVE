from DAVE.gui2 import *
from PySide2 import QtCore, QtGui, QtWidgets
from DAVE.scene import Scene

from DAVE.gui2.forms.main_form import Ui_MainWindow
from DAVE.visual import Viewport

class Gui():

    def __init__(self, scene):

        app = QtWidgets.QApplication()
        app.aboutToQuit.connect(self.onClose)

        splash = QtWidgets.QSplashScreen()
        splash.showMessage("Starting GUI")
        splash.show()

        # Main Window
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)

        # Create globally available properties

        self.scene = scene
        """Reference to a scene"""

        # Create 3D viewpower

        self.visual = Viewport(scene)
        """Reference to a viewport"""

        # populate
        self.visual.create_visuals(recreate=True)
        self.visual.position_visuals()

        MainWindow.setCentralWidget(ui.frame3d)
        self.visual.show_embedded(ui.frame3d)
        self.visual.update_visibility()

        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver('TimerEvent', self.timerEvent)

        # Docks
        self.guiWidgets = dict()
        """Dictionary of all created guiWidgets (dock-widgets)"""

        # Finalize
        splash.finish(MainWindow)
        MainWindow.show()
        app.exec_()

    def timerEvent(self):
        pass

    def onClose(self):
        self.visual.shutdown_qt()
        # self._logfile.close()
        print('closing')


# ======================================

s = Scene()
a = s.new_rigidbody('test')
g = Gui(s)