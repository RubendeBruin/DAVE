from PySide2 import QtCore, QtGui, QtWidgets
from DAVE.scene import Scene

from DAVE.gui2.forms.main_form import Ui_MainWindow
from DAVE.visual import Viewport
from DAVE.gui2 import new_node_dialog

from IPython.utils.capture import capture_output
import datetime

# All guiDockWidgets
from DAVE.gui2.dockwidget import *
from DAVE.gui2.widget_nodetree import WidgetNodeTree
from DAVE.gui2.widget_derivedproperties import WidgetDerivedProperties
from DAVE.gui2.widget_nodeprops import WidgetNodeProps

# resources

import DAVE.forms.resources_rc as resources_rc


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

        # private properties
        self._codelog = []

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
        self.visual.mouseLeftEvent = self.view3d_select_element

        self.MainWindow.setCentralWidget(self.ui.frame3d)
        self.visual.show_embedded(self.ui.frame3d)
        self.visual.update_visibility()

        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver('TimerEvent', self.timerEvent)

        # Docks
        self.guiWidgets = dict()
        """Dictionary of all created guiWidgets (dock-widgets)"""


        # Workspace buttons
        self.btnConstruct = QtWidgets.QPushButton()
        self.btnConstruct.setText('Construct')
        self.ui.toolBar.addWidget(self.btnConstruct)
        self.btnConstruct.clicked.connect(lambda : self.activate_workspace("CONSTRUCT"))

        self.activate_workspace('CONSTRUCT')

        # Finalize
        splash.finish(self.MainWindow)
        self.MainWindow.show()
        self.app.exec_()

    def activate_workspace(self, name):

        self.btnConstruct.setChecked(False)

        if name == 'CONSTRUCT':
            self.show_guiWidget('NodeTree', WidgetNodeTree)
            self.show_guiWidget('DerivedProperties', WidgetDerivedProperties)
            self.show_guiWidget('WidgetNodeProps', WidgetNodeProps)
            self.btnConstruct.setChecked(True)


    def timerEvent(self):
        pass

    def onClose(self):
        self.visual.shutdown_qt()
        # self._logfile.close()
        print('closing')


    def run_code(self, code, event):

        s = self.scene

        self.ui.teFeedback.setStyleSheet("background-color: yellow;")
        self.ui.teFeedback.setText("Running:")
        self.ui.teFeedback.append(code)
        self.ui.teFeedback.update()

        with capture_output() as c:

            try:
                exec(code)

                self.ui.teFeedback.setStyleSheet("background-color: white;")
                if c.stdout:
                    self.ui.teFeedback.append(c.stdout)
                    self.ui.teFeedback.append(str(datetime.datetime.now()))
                else:
                    self.ui.teFeedback.append("Succes at " + str(datetime.datetime.now()))

                self._codelog.append(code)

                if event is not None:
                    self.guiEmitEvent(event)

                # See if selected nodes are still valid and identical to the ones
                to_be_removed = []
                for node in self.selected_nodes:
                    if node not in self.scene._nodes:
                        to_be_removed.append(node)

                for node in to_be_removed:
                    self.selected_nodes.remove(node)

                if to_be_removed:
                    self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED)

            except Exception as E:
                self.ui.teFeedback.setText(c.stdout + '\n' + str(E) + '\n\nWhen running: \n\n' + code)
                self.ui.teFeedback.setStyleSheet("background-color: red;")
                return

    def openContextMenyAt(self, node_name, globLoc):
        menu = QtWidgets.QMenu()

        if node_name is not None:


            def delete():
                self.set_code('s.delete("{}")'.format(node_name))

            def dissolve():
                self.set_code('s.dissolve("{}")'.format(node_name))

            def edit():
                self.select_node(node_name)

            menu.addAction("Delete {}".format(node_name), delete)
            menu.addAction("Dissolve (Evaporate) {}".format(node_name), dissolve)
            menu.addAction("Edit {}".format(node_name), edit)

            menu.addSeparator()

            def copy_python_code():
                code = self.scene[node_name].give_python_code()
                print(code)
                self.app.clipboard().setText(code)

            menu.addAction("Copy python code", copy_python_code)
            menu.addSeparator()

            def duplicate():
                name = node_name
                name_of_duplicate = self.scene.available_name_like(name)

                node = self.scene[node_name]
                node.name = name_of_duplicate
                code = node.give_python_code()
                node.name = name
                self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

                self.select_node(name_of_duplicate)


            menu.addAction("Duplicate", duplicate)
            menu.addSeparator()

        menu.addAction("New Axis", self.new_axis)
        menu.addAction("New RigidBody", self.new_body)
        menu.addAction("New Poi", self.new_poi)
        menu.addAction("New Sheave", self.new_sheave)
        menu.addAction("New Cable", self.new_cable)
        menu.addAction("New Force", self.new_force)
        menu.addAction("New Beam", self.new_beam)
        menu.addAction("New 2d Connector", self.new_connector2d)
        menu.addAction("New 6d Connector", self.new_linear_connector)
        menu.addAction("New Linear Hydrostatics", self.new_linear_hydrostatics)
        menu.addAction("New Visual", self.new_visual)
        menu.addAction("New Buoyancy mesh", self.new_buoyancy_mesh)

        menu.exec_(globLoc)

    def new_axis(self):
        self.new_something(new_node_dialog.add_axis)

    def new_body(self):
        self.new_something(new_node_dialog.add_body)

    def new_poi(self):
        self.new_something(new_node_dialog.add_poi)

    def new_cable(self):
        self.new_something(new_node_dialog.add_cable)

    def new_force(self):
        self.new_something(new_node_dialog.add_force)

    def new_sheave(self):
        self.new_something(new_node_dialog.add_sheave)

    def new_linear_connector(self):
        self.new_something(new_node_dialog.add_linear_connector)

    def new_connector2d(self):
        self.new_something(new_node_dialog.add_connector2d)

    def new_beam(self):
        self.new_something(new_node_dialog.add_beam_connector)

    def new_linear_hydrostatics(self):
        self.new_something(new_node_dialog.add_linear_hydrostatics)

    def new_visual(self):
        self.new_something(new_node_dialog.add_visual)

    def new_buoyancy_mesh(self):
        self.new_something(new_node_dialog.add_buoyancy)

    def new_something(self, what):
        r = what(self.scene, self.selected_nodes)
        if r:
            self.run_code("s." + r, guiEventType.MODEL_STRUCTURE_CHANGED)

# ================= viewer code ===================

    def view3d_select_element(self, vtkactor):

        # info is an Actor
        #
        # we need to find the corresponding node
        node = self.visual.node_from_vtk_actor(vtkactor)

        if node is None:
            print('Could not find node for this actor')
            self.selected_nodes.clear()
            self.guiEmitEvent(guiEventType.SELECTION_CHANGED)


        _node = node
        if node in self.selected_nodes:
            # if the is already selected, then select something different

            # cycle between node and its parent
            try:
                node = node.parent
            except:
                try:
                    node = node.master
                except:
                    try:
                        node = node.slave
                    except:
                        try:
                            node = node._pois[0]
                        except:
                            pass

        if node is None:  # in case the parent or something was none
            node = _node
        self.guiSelectNode(node.name)

    def visual_update_selection(self):
        for v in self.visual.visuals:
            if v.node in self.selected_nodes:
                if v.node is not None:
                    print('selecting {}'.format(v.node.name))
                v.select()
            else:
                if v.node is not None:
                    print('deselecting {}'.format(v.node.name))
                v.deselect()




# ================= guiWidget codes

    def guiEmitEvent(self, event, sender=None):
        for widget in self.guiWidgets.values():
            if not (widget is sender):
                widget.guiEvent(event)


        # update the visual as well
        if event == guiEventType.SELECTION_CHANGED:
            self.visual_update_selection()
            self.visual.refresh_embeded_view()
        if event == guiEventType.MODEL_STATE_CHANGED:
            self.visual.position_visuals()
            self.visual.refresh_embeded_view()
        if event in [guiEventType.SELECTED_NODE_MODIFIED,
                     guiEventType.MODEL_STRUCTURE_CHANGED,
                     guiEventType.FULL_UPDATE]:
            self.visual.add_new_actors_to_screen()
            self.visual.position_visuals()
            self.visual.refresh_embeded_view()





    def guiSelectNode(self, node_name):
        print('selecting a node with name {}'.format(node_name))

        old_selection = self.selected_nodes.copy()

        if not (self.app.keyboardModifiers() and QtCore.Qt.KeyboardModifier.ControlModifier):
            self.selected_nodes.clear()


        node = self.scene[node_name]
        if node not in self.selected_nodes:
            self.selected_nodes.append(node)

        print(self.selected_nodes)

        if old_selection != self.selected_nodes:
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
            d.gui = self

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
a = s.new_rigidbody('test3', position=(0,0,3))

g = Gui(s)