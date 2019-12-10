"""

   This is the root module for the graphical user interface.

   The GUI is build using QT / PySide2 and is set-up to be easily to extent.

   The main module (this file) provides the main screen with:
     - A 3D viewer with interaction
     - A method to modify the scene by running python code
     - Opening and saving of models or actions
     - The library browser
     - A timer and animation mechanism
     - A method to switch between workspaces
     - An event system for communication between dock-widgets
     - An data-source for teh dock-widgets

    The interface is extended by dockwidgets. These are gui elements (widgets) that can be shown inside the main window.
    Some of the dock-widgets are:
    - the node-tree
    - the node-properties (editor)
    - the node-derived-properties (inspector)



    Dockwidgets can be created by:

    -  creating a new class derived from the guiDockWidget (dockwidget.py)
    -  implement the abstract methods
        - guiCreate : creates the content of the widget
        - guiProcessEvent : is called when the model is changed. The widget should update itself accordingly.
             See guiEventType enum for details.
        - guiDefaultLocation : returns the location where the widget should be shown [optional]
    - Provided interaction with the main module by sending python-code to guiRunCodeCallback()

    EXAMPLE: widget_template_example.py

    -  import the class in this file
    -  implement the activation of the widget in the activate_workspace method of the Gui class


    Animation structure

    The 3D viewer can be animated. This is done on basis of degrees of freedom of the scene.
    Animations can continue as long as the model structure is unchanged.

    Animations can be a "single-run" animation or can be a loop.

    animation
    - current time (time in seconds, reset by start)
    - dof interpolation object
    - final dofs (array)

    - is loop     (bool)
    - start()     (terminates the current animation, if any, and starts a new animation)
    - terminate() (terminates the current animation, if and)





"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""




from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QDialog,QFileDialog
from DAVE.scene import Scene

from DAVE.gui2.forms.main_form import Ui_MainWindow
from DAVE.visual import Viewport
from DAVE.gui2 import new_node_dialog
import DAVE.standard_assets
from DAVE.forms.dlg_solver import Ui_Dialog
import DAVE.settings

from IPython.utils.capture import capture_output
import datetime
import time
import scipy.interpolate

# All guiDockWidgets
from DAVE.gui2.dockwidget import *
from DAVE.gui2.widget_nodetree import WidgetNodeTree
from DAVE.gui2.widget_derivedproperties import WidgetDerivedProperties
from DAVE.gui2.widget_nodeprops import WidgetNodeProps
from DAVE.gui2.widget_dynamic_properties import WidgetDynamicProperties
from DAVE.gui2.widget_modeshapes import WidgetModeShapes
from DAVE.gui2.widget_ballastconfiguration import WidgetBallastConfiguration
from DAVE.gui2.widget_ballastsolver import WidgetBallastSolver
from DAVE.gui2.widget_ballastsystemselect import WidgetBallastSystemSelect

# Imports available in script
import numpy as np
from DAVE.solvers.ballast import force_vessel_to_evenkeel_and_draft, BallastSystemSolver

# resources

import DAVE.forms.resources_rc as resources_rc

class SolverDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(SolverDialog, self).__init__(parent)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/icons/cube.png"))

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

        # ============== private properties ================
        self._codelog = []

        self._animation_start_time = time.time()
        """Time at start of the simulation in seconds (system-time)"""

        self._animation_length = 0
        """The length of the animation in seconds"""

        self._animation_loop = False
        """Animation is a loop"""

        self._animation_final_dofs = None
        """DOFS at termination of the animation"""

        self._animation_keyframe_interpolation_object = None
        """Object that can be called with a time and yields the dofs at that time. t should be [0..._animation_length] """


        # ================= Create globally available properties =======
        self.selected_nodes = []
        """A list of selected nodes (if any)"""

        self.scene = scene
        """Reference to a scene"""

        # ======================== Create 3D viewpower ====================
        self.visual = Viewport(scene)
        """Reference to a viewport"""


        self.visual.create_visuals(recreate=True)
        self.visual.position_visuals()
        self.visual.mouseLeftEvent = self.view3d_select_element

        self.MainWindow.setCentralWidget(self.ui.frame3d)
        self.visual.show_embedded(self.ui.frame3d)
        self.visual.update_visibility()

        self._timerid = None
        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver('TimerEvent', self.timerEvent)

        # ======================== Main Menu entries :: visuals ======

        self.ui.actionNew.triggered.connect(self.clear)
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave_scene.triggered.connect(self.menu_save)
        self.ui.actionImport_sub_scene.triggered.connect(self.menu_import)
        self.ui.actionImport_browser.triggered.connect(self.import_browser)

        # --- buttons
        self.ui.pbExecute.pressed.connect(self.run_code_in_teCode)
        self.ui.pbCopyFeedback.pressed.connect(self.feedback_copy)
        self.ui.pbGenerateSceneCode.pressed.connect(self.generate_scene_code)

        # -- visuals
        self.ui.actionShow_water_plane.triggered.connect(self.toggle_show_global)
        self.ui.actionShow_visuals.triggered.connect(self.toggle_show_visuals)
        self.ui.actionShow_Geometry_elements.triggered.connect(self.toggle_show_geometry)
        self.ui.actionShow_force_applyting_element.triggered.connect(self.toggle_show_force)

        self.ui.actionHorizontal_camera.triggered.connect(self.visual.level_camera)
        self.ui.actionAdd_light.triggered.connect(self.visual.make_lighter)
        self.ui.actionDark_mode.triggered.connect(self.visual.make_darker)
        self.ui.action2D_mode.triggered.connect(self.visual.toggle_2D)

        def normalize_force():
            self.run_code('self.visual.force_do_normalize = not self.visual.force_do_normalize',guiEventType.VIEWER_SETTINGS_UPDATE)

        self.ui.actionShow_all_forces_at_same_size.triggered.connect(normalize_force)

        def increase_force_size():
            self.run_code('self.visual.force_scale = 1.1*self.visual.force_scale',guiEventType.VIEWER_SETTINGS_UPDATE)

        self.ui.actionIncrease_force_size.triggered.connect(increase_force_size)

        def decrease_force_size():
            self.run_code('self.visual.force_scale = 0.9*self.visual.force_scale',guiEventType.VIEWER_SETTINGS_UPDATE)

        self.ui.actionDecrease_force_size.triggered.connect(decrease_force_size)

        def increase_geo_size():
            self.run_code('self.visual.geometry_scale = 1.1*self.visual.geometry_scale',guiEventType.VIEWER_SETTINGS_UPDATE)

        self.ui.actionIncrease_Geometry_size.triggered.connect(increase_geo_size)

        def decrease_geo_size():
            self.run_code('self.visual.geometry_scale = 0.9*self.visual.geometry_scale',guiEventType.VIEWER_SETTINGS_UPDATE)

        self.ui.actionDecrease_Geometry_size.triggered.connect(decrease_geo_size)

        # ======================== Docks ====================
        self.guiWidgets = dict()
        """Dictionary of all created guiWidgets (dock-widgets)"""


        # Workspace buttons

        self.btnSolve = QtWidgets.QPushButton()
        self.btnSolve.setText('Solve &statics')
        self.ui.toolBar.addWidget(self.btnSolve)
        self.btnSolve.clicked.connect(self.solve_statics)

        self.btnUndoSolve = QtWidgets.QPushButton()
        self.btnUndoSolve.setText('undo solve')
        self.ui.toolBar.addWidget(self.btnUndoSolve)
        self.btnUndoSolve.clicked.connect(self.undo_solve_statics)

        self.btnLibrary = QtWidgets.QPushButton()
        self.btnLibrary.setText('Library')
        self.ui.toolBar.addWidget(self.btnLibrary)
        self.btnLibrary.clicked.connect(self.import_browser)

        space = QtWidgets.QWidget()
        space.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.ui.toolBar.addWidget(space)

        lbl = QtWidgets.QLabel()
        lbl.setText("Workspace:  ")
        self.ui.toolBar.addWidget(lbl)

        self.btnConstruct = QtWidgets.QPushButton()
        self.btnConstruct.setText('Construct')
        self.ui.toolBar.addWidget(self.btnConstruct)
        self.btnConstruct.clicked.connect(lambda : self.activate_workspace("CONSTRUCT"))

        self.btnConstruct = QtWidgets.QPushButton()
        self.btnConstruct.setText('Dynamics')
        self.ui.toolBar.addWidget(self.btnConstruct)
        self.btnConstruct.clicked.connect(lambda : self.activate_workspace("DYNAMICS"))

        self.btnConstruct = QtWidgets.QPushButton()
        self.btnConstruct.setText('Ballast')
        self.ui.toolBar.addWidget(self.btnConstruct)
        self.btnConstruct.clicked.connect(lambda: self.activate_workspace("BALLAST"))

        space = QtWidgets.QWidget()
        space.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.ui.toolBar.addWidget(space)

        self.activate_workspace('CONSTRUCT')

        # ======================== Finalize ========================
        splash.finish(self.MainWindow)
        self.MainWindow.show()
        self.app.exec_()

    def activate_workspace(self, name):

        self.animation_terminate()

        for g in self.guiWidgets.values():
            g.close()

        if name == 'CONSTRUCT':
            self.show_guiWidget('NodeTree', WidgetNodeTree)
            self.show_guiWidget('DerivedProperties', WidgetDerivedProperties)
            self.show_guiWidget('WidgetNodeProps', WidgetNodeProps)
            # self.btnConstruct.setChecked(True)

        if name == 'DYNAMICS':
            # self.show_guiWidget('NodeTree', WidgetNodeTree)
            # self.show_guiWidget('DerivedProperties', WidgetDerivedProperties)
            self.show_guiWidget('WidgetDynamicProperties', WidgetDynamicProperties)
            self.show_guiWidget('WidgetModeShapes', WidgetModeShapes)

        if name == 'BALLAST':
            self.show_guiWidget('WidgetBallastSystemSelect', WidgetBallastSystemSelect)
            self.show_guiWidget('WidgetBallastConfiguration', WidgetBallastConfiguration)
            self.show_guiWidget('WidgetBallastSolver', WidgetBallastSolver)


    def import_browser(self):
        G = DAVE.standard_assets.Gui()
        r = G.showModal()

        if r is not None:
            file = r[0]
            container = r[1]
            prefix = r[2]
            code = 's.import_scene(s.get_resource_path("{}"), containerize={}, prefix="{}")'.format(file,container,prefix)
            self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)


    def animation_running(self):
        """Returns true is an animation is running"""
        return self._timerid is not None

    def timerEvent(self,a,b):

        if self._timerid is None:  # timer is going to be destroyed
            return

        t = time.time() - self._animation_start_time  # time since start of animation in [s]

        if self._animation_loop:
            t = np.mod(t, self._animation_length)
        else:
            if t>self._animation_length:
                self.animation_terminate()
                return

        dofs = self._animation_keyframe_interpolation_object(t)
        self.scene._vfc.set_dofs(dofs)
        self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)

    def animation_terminate(self, no_reset_dofs = False):

        if not self.animation_running():
            return # nothing to destroy

        print('Destroying timer')
        to_be_destroyed = self._timerid
        self._timerid = None
        iren = self.visual.renwin.GetInteractor()
        iren.DestroyTimer(to_be_destroyed)

        if not no_reset_dofs:
            self.scene._vfc.set_dofs(self._animation_final_dofs)
            self.visual.quick_updates_only = False
            self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)
        self.visual.quick_updates_only = False


    def animation_start(self, t, dofs, is_loop, final_dofs = None, do_not_reset_time=False):
        """Start an new animation

        Args:
            t:    List of times at keyframes
            dofs: List of dofs at keyframes
            is_loop: Should animation be played in a loop (bool)
            final_dofs : [optional] DOFS to be set when animation is finished or terminated. Defaults to last keyframe
            do_not_reset_time : do not reset the time when starting the animation, this means the loop continues where it was.


        """
        self.animation_terminate(no_reset_dofs=True) # end old animation, if any

        if len(dofs) != len(t):
            raise ValueError("dofs and t should have the same length (list or tuple)")

        self._animation_length = np.max(t)
        self._animation_keyframe_interpolation_object = scipy.interpolate.interp1d(t, dofs,axis=0)
        self._animation_loop = is_loop

        if final_dofs is None:
            final_dofs = dofs[-1]

        self._animation_final_dofs = final_dofs
        if not do_not_reset_time:
            self._animation_start_time = time.time()

        self.visual.quick_updates_only = True

        iren = self.visual.renwin.GetInteractor()
        if self._timerid is None:
            self._timerid = iren.CreateRepeatingTimer(round(1000 / DAVE.settings.GUI_ANIMATION_FPS))
        else:
            raise Exception("could not create new timer, old timer is still active")




    def onClose(self):
        self.visual.shutdown_qt()
        # self._logfile.close()
        print('closing')


    def run_code(self, code, event):

        s = self.scene

        self.ui.teCode.append('# ------------------')
        self.ui.pbExecute.setStyleSheet("background-color: yellow;")
        self.ui.teFeedback.setStyleSheet("")
        self.ui.teFeedback.update()
        self.ui.teCode.append(code)
        self.ui.teCode.append('\n')
        self.ui.teCode.verticalScrollBar().setValue(
            self.ui.teCode.verticalScrollBar().maximum())  # scroll down all the way
        self.ui.teCode.update()

        # self.app.processEvents()

        with capture_output() as c:

            try:
                exec(code)

                if c.stdout:
                    self.ui.teFeedback.append(c.stdout)
                    self.ui.teFeedback.append(str(datetime.datetime.now()))
                else:
                    self.ui.teFeedback.append("Succes at " + str(datetime.datetime.now()))

                self._codelog.append(code)

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

            self.ui.pbExecute.setStyleSheet("")
            self.ui.pbExecute.update()
            self.ui.teFeedback.verticalScrollBar().setValue(self.ui.teFeedback.verticalScrollBar().maximum()) # scroll down all the way

            if event is not None:
                self.guiEmitEvent(event)



    def stop_solving(self):
        self._terminate = True

    def solve_statics(self):
        self.scene._vfc.state_update()
        old_dofs = self.scene._vfc.get_dofs()

        if len(old_dofs) == 0:  # no degrees of freedom
            print('No dofs')
            return

        self._dofs = old_dofs.copy()

        long_wait = False
        dialog = None

        self._terminate = False

        # solve with time-out
        count = 0
        while True:
            status = self.scene._vfc.state_solve_statics_with_timeout(0.5, True)

            if self._terminate:
                print('Terminating')
                break

            if status == 0:
                if count == 0:
                    break
                else:
                    long_wait = True

                    self.visual.position_visuals()
                    self.visual.refresh_embeded_view()
                    break

            if dialog is None:
                dialog = SolverDialog()
                dialog.btnTerminate.clicked.connect(self.stop_solving)
                dialog.show()

            count += 1
            dialog.label_2.setText('Maximum error = {}'.format(self.scene._vfc.Emaxabs))
            dialog.update()

            self.visual.position_visuals()
            self.visual.refresh_embeded_view()
            self.app.processEvents()

        if dialog is not None:
            dialog.close()

        if DAVE.settings.GUI_DO_ANIMATE and not long_wait:
            new_dofs = self.scene._vfc.get_dofs()
            self.animate_change(old_dofs, new_dofs, 10)

        self._codelog.append('s.solve_statics()')

    def animate_change(self, old_dof, new_dof, n_steps):
        """Animates from old_dof to new_dofs in n_steps"""

        dt = DAVE.settings.GUI_SOLVER_ANIMATION_DURATION / n_steps

        t = []
        dofs = []

        old_dof = np.array(old_dof)
        new_dof = np.array(new_dof)

        for i in range(n_steps+1):

            factor = i/n_steps
            old = 0.5 + 0.5 * np.cos(3.14159 * factor)

            t.append(dt*i)
            dofs.append((1 - old) * new_dof + old * old_dof)

        self.animation_start(t,dofs,is_loop=False)

    def toggle_show_force(self):
        self.visual.show_force = self.ui.actionShow_force_applyting_element.isChecked()
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def toggle_show_geometry(self):
        self.visual.show_geometry = self.ui.actionShow_Geometry_elements.isChecked()
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def toggle_show_global(self):
        self.visual.show_global = self.ui.actionShow_water_plane.isChecked()
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def toggle_show_visuals(self):
        self.visual.show_visual = self.ui.actionShow_visuals.isChecked()
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def undo_solve_statics(self):
        if self._dofs is not None:
            self.run_code('s._vfc.set_dofs(self._dofs) # UNDO SOLVE STATICS', guiEventType.MODEL_STATE_CHANGED)

    def clear(self):
        self.run_code('s.clear()', guiEventType.FULL_UPDATE)

    def open(self):
        filename, _ = QFileDialog.getOpenFileName(filter="*.dave", caption="Assets")
        if filename:
            code = 's.clear()\ns.load_scene(r"{}")'.format(filename)
            self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

    def menu_import(self):
        filename, _ = QFileDialog.getOpenFileName(filter="*.dave", caption="Assets")
        if filename:
            code = 's.import_scene(r"{}")'.format(filename)
            self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

    def menu_save(self):
        filename, _ = QFileDialog.getSaveFileName(filter="*.dave", caption="Scene files",directory=self.scene.resources_paths[0])
        if filename:
            code = 's.save_scene(r"{}")'.format(filename)
            self.run_code(code, guiEventType.NOTHING)

    def feedback_copy(self):
        self.app.clipboard().setText(self.ui.teFeedback.toPlainText())

    def generate_scene_code(self):
        self.ui.teFeedback.setText(self.scene.give_python_code())

    def run_code_in_teCode(self):
        code = self.ui.teCode.toPlainText()
        self.run_code(code,guiEventType.FULL_UPDATE)

    def openContextMenyAt(self, node_name, globLoc):
        menu = QtWidgets.QMenu()

        if node_name is not None:


            def delete():
                self.run_code('s.delete("{}")'.format(node_name), guiEventType.MODEL_STRUCTURE_CHANGED)

            def dissolve():
                self.run_code('s.dissolve("{}")'.format(node_name), guiEventType.MODEL_STRUCTURE_CHANGED)

            def edit():
                self.selected_nodes.clear()
                self.guiSelectNode(node_name)

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

        if node is None: # sea or something
            self.selected_nodes.clear()
        else:
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

        for v in self.visual.visuals:
            try:
                parent = v.node.parent
            except:
                continue

            if parent in self.selected_nodes:
                v.make_transparent()
            else:
                v.reset_opacity()



    # ================= guiWidget codes

    def guiEmitEvent(self, event, sender=None):
        for widget in self.guiWidgets.values():
            if not (widget is sender):
                widget.guiEvent(event)


        # update the visual as well
        if event == guiEventType.SELECTION_CHANGED:
            self.visual_update_selection()
            self.refresh_3dview()
            return
        if event == guiEventType.SELECTED_NODE_MODIFIED:
            self.visual.add_new_actors_to_screen()
            self.visual.position_visuals()
            self.refresh_3dview()
            return

        if event == guiEventType.VIEWER_SETTINGS_UPDATE:
            self.visual.update_visibility()
            self.refresh_3dview()


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
            location = d.guiDefaultLocation()
            if location is None:
                d.setFloating(True)
            else:
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

# ====== main code ======

if __name__ == '__main__':

    from DAVE.solvers.ballast import Tank, BallastSystemSolver

    s = Scene()

    s.import_scene('barge with linear hydrostatics.dave_asset')

    # make four tanks
    t1 = Tank()
    t1.position = np.array((10.,10.,0))
    t1.max = 50000


    t2 = Tank()
    t2.position = np.array((10., -10., 0))
    t2.max = 50000

    t3 = Tank()
    t3.position = np.array((-10., -10., 0))
    t3.max = 50000

    t4 = Tank()
    t4.position = np.array((-10., 10., 0))
    t4.max = 50000

    t5 = Tank()
    t5.position = np.array((40., 10., 5))
    t5.max = 50000

    t6 = Tank()
    t6.position = np.array((40., -10., 5))
    t6.max = 50000

    t7 = Tank()
    t7.position = np.array((-40., -10., 5))
    t7.max = 50000

    t8 = Tank()
    t8.position = np.array((-40., 10., 5))
    t8.max = 50000

    t1.name = 't1'
    t2.name = 't2'
    t3.name = 't3'
    t4.name = 't4'
    t5.name = 't5'
    t6.name = 't6'
    t7.name = 't7'
    t8.name = 't8'

    s['Barge'].parent = None
    s['Barge'].fixed = False
    s['Barge'].mass = 0.0


    # force_vessel_to_evenkeel_and_draft(s, s['Barge'], -4)
    #
    bs = s.new_ballastsystem('bs',parent=s['Barge'], position = (50,0,0))

    bs.tanks.extend([t1,t2,t3,t4,t5,t6,t7,t8])

    bso = BallastSystemSolver(bs)

    s["bs"].empty_all_usable_tanks()
    s.required_ballast = force_vessel_to_evenkeel_and_draft(scene=s, vessel="Barge", z=-7.25)
    bss = BallastSystemSolver(s["bs"])
    bso.ballast_to(cogx=s.required_ballast[1], cogy=s.required_ballast[2], weight=-s.required_ballast[0])

    g = Gui(s)