from PySide2 import QtCore, QtGui, QtWidgets
from DAVE.scene import Scene

from DAVE.gui2.forms.main_form import Ui_MainWindow
from DAVE.visual import Viewport

from IPython.utils.capture import capture_output
import datetime

# All guiDockWidgets
from DAVE.gui2.dockwidget import *
from DAVE.gui2.widget_nodetree import WidgetNodeTree



class Gui():

    def __init__(self, scene):

        self.app = QtWidgets.QApplication()
        self.app.aboutToQuit.connect(self.onClose)

        splash = QtWidgets.QSplashScreen()
        splash.showMessage("Starting GUI")
        splash.show()

        # Main Window
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        # Create globally available properties

        self.selected_nodes = []
        """A list of selected nodes (if any)"""

        self.scene = scene
        """Reference to a scene"""

        # Create 3D viewpower

        self.visual = Viewport(scene)
        """Reference to a viewport"""

        # populate
        self.visual.create_visuals(recreate=True)
        self.visual.position_visuals()

        self.MainWindow.setCentralWidget(self.ui.frame3d)
        self.visual.show_embedded(self.ui.frame3d)
        self.visual.update_visibility()

        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver('TimerEvent', self.timerEvent)

        # Docks
        self.guiWidgets = dict()
        """Dictionary of all created guiWidgets (dock-widgets)"""

        self.show_guiWidget('NodeTree',WidgetNodeTree)

        # Finalize
        splash.finish(self.MainWindow)
        self.MainWindow.show()
        self.app.exec_()

    def timerEvent(self):
        pass

    def onClose(self):
        self.visual.shutdown_qt()
        # self._logfile.close()
        print('closing')


    def run_code(self, code, event):

        s = self.scene

        self.ui.teFeedback.setStyleSheet("background-color: yellow;")
        self.ui.teFeedback.setText("Running...")
        self.ui.teFeedback.update()

        with capture_output() as c:

            try:
                exec(code)

                self.ui.teFeedback.setStyleSheet("background-color: white;")
                if c.stdout:
                    self.ui.teFeedback.setText(c.stdout)
                else:
                    self.ui.teFeedback.append("...Done")

                self.ui.teFeedback.append(str(datetime.datetime.now()))

                # TODO log code
                # TODO check if selected node is still present
                # TODO fire event

            except Exception as E:
                self.ui.teFeedback.setText(c.stdout + '\n' + str(E) + '\n\nWhen running: \n\n' + code)
                self.ui.teFeedback.setStyleSheet("background-color: red;")
                return



# ================= guiWidget codes

    def guiEmitEvent(self, event, sender=None):
        for widget in self.guiWidgets.values():
            if not (widget is sender):
                widget.guiEvent(event)

    def guiSelectNode(self, node_name):
        print('selecting a node with name {}'.format(node_name))

        if not (self.app.keyboardModifiers() and QtCore.Qt.KeyboardModifier.ControlModifier):
            self.selected_nodes.clear()


        node = self.scene[node_name]
        if node not in self.selected_nodes:
            self.selected_nodes.append(node)

        print(self.selected_nodes)
        self.guiEmitEvent(guiEventType.SELECTION_CHANGED)


    def show_guiWidget(self, name, widgetClass):
        if name in self.guiWidgets:
            d = self.guiWidgets[name]
        else:
            print('Creating {}'.format(name))

            d = widgetClass(self.MainWindow)
            d.setWindowTitle(name)
            self.MainWindow.addDockWidget(d.guiDefaultLocation(), d)
            self.guiWidgets[name] = d

            d.guiScene = self.scene
            d.guiEmitEvent = self.guiEmitEvent
            d.guiRunCodeCallback = self.run_code
            d.guiSelectNode = self.guiSelectNode
            d.guiSelection = self.selected_nodes

        d.show()
        d._active = True
        d.guiEvent(guiEventType.FULL_UPDATE)

# =============================

    def refresh_3dview(self):
        self.visual.refresh_embeded_view()


# ======================================

s = Scene()
a = s.new_rigidbody('test')
a = s.new_rigidbody('test2', parent=a)
a = s.new_rigidbody('test3')

g = Gui(s)