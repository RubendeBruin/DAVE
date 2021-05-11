"""

   This is the root module for the graphical user interface.

   The GUI is build using QT / PySide2 and is set-up to be easy to extent.

   The nodeA module (this file) provides the nodeA screen with:
     - A 3D viewer with interaction
     - A method to modify the scene by running python code
     - Opening and saving of models or actions
     - The library browser
     - A timer and animation mechanism
     - A method to switch between workspaces
     - An event system for communication between dock-widgets
     - A data-source for the dock-widgets

    The interface is extended by dockwidgets. These are gui elements (widgets) that can be shown inside the nodeA window.
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
    - Provided interaction with the nodeA module by sending python-code to guiRunCodeCallback()

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
    - wavefield (WaveField object)

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

import DAVE.auto_download

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QPixmap, QFont, QFontMetricsF, QCursor
from PySide2.QtWidgets import QDialog, QFileDialog, QMessageBox, QMenu, QWidgetAction
from DAVE.scene import Scene

from DAVE.gui.forms.main_form import Ui_MainWindow
from DAVE.visual import Viewport, ActorType
from DAVE.gui import new_node_dialog
import DAVE.gui.standard_assets
from DAVE.gui.forms.dlg_solver import Ui_Dialog
import DAVE.settings

from DAVE.gui.helpers.highlighter import PythonHighlighter
from DAVE.gui.helpers.ctrl_enter import ShiftEnterKeyPressFilter
from DAVE.gui.helpers.qmenu import MenuSlider
from DAVE.gui.forms.menu_nodetypes import Ui_MenuNodes

from IPython.utils.capture import capture_output
import datetime
import time
import scipy.interpolate

# All guiDockWidgets
from DAVE.gui.dockwidget import *
from DAVE.gui.widget_nodetree import WidgetNodeTree
from DAVE.gui.widget_derivedproperties import WidgetDerivedProperties
from DAVE.gui.widget_nodeprops import WidgetNodeProps
from DAVE.gui.widget_dynamic_properties import WidgetDynamicProperties
from DAVE.gui.widget_modeshapes import WidgetModeShapes
from DAVE.gui.widget_ballastconfiguration import WidgetBallastConfiguration
from DAVE.gui.widget_ballastsolver import WidgetBallastSolver
from DAVE.gui.widget_ballastsystemselect import WidgetBallastSystemSelect
from DAVE.gui.widget_airy import WidgetAiry
from DAVE.gui.widget_stability_disp import WidgetDisplacedStability
from DAVE.gui.widget_explore import WidgetExplore
from DAVE.gui.widget_tank_order import WidgetTankOrder
from DAVE.gui.widget_rigg_it_right import WidgetRiggItRight

import numpy as np

# resources
import DAVE.gui.forms.resources_rc

class SolverDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(SolverDialog, self).__init__(parent)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/icons/cube.png"))

class Gui():

    def __init__(self, scene=None, splash=None, app=None, geometry_scale = -1, cog_scale = 0.25, block=True):
        """
        Starts the Gui on scene "scene".

        Normal use:

            Gui(s)

        When stating from jupyter or ipython use:

            %gui qt
            Gui(scene=s, block=False)

        to create a non-blocking ui.

        Args:
            scene:  [None] Scene to view. None creates a new scene
            splash: [None] qt splash screen instance to close
            app:    [None] qt application instance to use. None creates a new instance.
            block:  [True] qt application _exec(). Set to False when using %gui qt in IPython/jupyter
            geometry_scale: geometry scale (visual)
            cog_scale: cog scale (visual)
        """

        if app is None:

            if QtWidgets.QApplication.instance() is not None:
                self.app = QtWidgets.QApplication.instance()
            else:
                self.app = QtWidgets.QApplication()
        else:
            self.app = app
        self.app.aboutToQuit.connect(self.onClose)

        if splash is None:
            splash = QtWidgets.QSplashScreen()
            splash.setPixmap(QPixmap(":/icons/splashscreen.png"))
            splash.show()

        if scene is None:
            scene = Scene()

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

        self._animation_paused = False
        """Animation paused"""

        self._animation_available = False
        """Animation available"""

        self._animation_speed = 1.0


        # ================= Create globally available properties =======
        self.selected_nodes = []
        """A list of selected nodes (if any)"""

        self.scene = scene
        """Reference to a scene"""

        # ======================== Create 3D viewport ====================
        self.visual = Viewport(scene)
        """Reference to a viewport"""

        if cog_scale >= 0:
            self.visual.cog_scale = cog_scale

        if geometry_scale >= 0:
            self.visual.geometry_scale = geometry_scale


        self.visual.create_visuals(recreate=True)
        self.visual.show_embedded(self.ui.frame3d)

        self.visual.position_visuals()
        self.visual.update_visibility()

        self.visual.mouseLeftEvent = self.view3d_select_element


        # right-click event for
        self.ui.frame3d.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.frame3d.customContextMenuRequested.connect(self.rightClickViewport)

        self._timerid = None
        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver('TimerEvent', self.timerEvent)

        # ------ key-presses -----

        self.visual.onEscapeKey = self.escPressed

        # ------ viewport buttons ------

        # right
        self.ui.btnWater.clicked.connect(self.toggle_show_global)
        self.ui.btnBlender.clicked.connect(self.to_blender)
        self.ui.pbCopyViewCode.clicked.connect(self.copy_screenshot_code)
        self.ui.pbLabels.clicked.connect(self.show_labels_menu)

        self.labels_menu = QMenu()
        items = ('Tank','Point','Cable')

        self.ui.label_menu_actions = []
        for name in items:

            lb = QWidgetAction(None)
            lb.setCheckable(True)
            lb.setChecked(True)
            lb.setText(name)
            lb.setData(name)
            lb.toggled.connect(self.show_label_toggled)
            self.ui.label_menu_actions.append(lb)
            self.labels_menu.addAction(lb)


        # left
        self.ui.pbUpdate.clicked.connect(lambda: self.guiEmitEvent(guiEventType.FULL_UPDATE))
        self.ui.btnSolveStatics.clicked.connect(self.solve_statics)
        self.ui.btnUndoStatics.clicked.connect(self.undo_solve_statics)

        # bottom
        self.ui.pbExecute.clicked.connect(self.run_code_in_teCode)
        self.ui.pbCopyOutput.clicked.connect(self.feedback_copy)
        self.ui.pbCopyHistory.clicked.connect(self.history_copy)
        self.ui.pbGenerateSceneCode.clicked.connect(self.generate_scene_code)
        self.ui.pbClearCode.clicked.connect(self.clear_code)
        self.ui.tbTidyHistory.clicked.connect(self.tidy_history)

        # ------ animation buttons ------
        self.ui.frameAni.setVisible(False)
        self.ui.btnStopAnimation.clicked.connect(lambda :self.animation_terminate(False))
        self.ui.btnPauseAnimation.clicked.connect(self.animation_pause_or_continue_click)
        self.ui.aniSlider.valueChanged.connect(self.animation_change_time)
        self.ui.sbPlaybackspeed.valueChanged.connect(self.animation_speed_change)



        # ======================== Main Menu entries  ======

        self.ui.actionNew.triggered.connect(self.clear)
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave_scene.triggered.connect(self.menu_save)
        self.ui.actionSave_actions_as.triggered.connect(self.menu_save_actions)
        self.ui.actionImport_sub_scene.triggered.connect(self.menu_import)
        self.ui.actionImport_browser.triggered.connect(self.import_browser)
        self.ui.actionOrcaflex.triggered.connect(self.menu_export_orcaflex_yml)
        self.ui.actionOrcaflex_package.triggered.connect(self.menu_export_orcaflex_package)
        self.ui.actionBlender.triggered.connect(self.to_blender)


        # -- visuals --
        self.ui.actionShow_water_plane.triggered.connect(self.toggle_show_global_from_menu)
        self.ui.actionShow_force_applying_element.triggered.connect(self.toggle_show_force_applying_elements)


        self.ui.sliderGeometrySize = MenuSlider('Geometry size')
        self.ui.sliderGeometrySize.setMin(0)
        self.ui.sliderGeometrySize.slider.setValue(20)
        def set_geo_size(value):
            if value < 1:
                self.visual.show_geometry = False
                self.run_code('self.visual.geometry_scale = 0',guiEventType.VIEWER_SETTINGS_UPDATE)
                self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)
            else:
                self.visual.show_geometry = True
                self.run_code(f'self.visual.geometry_scale = {value**(1.3)/100 : .2f}',guiEventType.VIEWER_SETTINGS_UPDATE)

        self.ui.sliderGeometrySize.connectvalueChanged(set_geo_size)
        self.ui.menuView.addAction(self.ui.sliderGeometrySize)

        # force size
        self.ui.menuView.addSeparator()

        def normalize_force():
            self.run_code('self.visual.force_do_normalize = not self.visual.force_do_normalize',guiEventType.VIEWER_SETTINGS_UPDATE)

        forcenormalize= self.ui.menuView.addAction("View all forces at same size")
        forcenormalize.setCheckable(True)
        forcenormalize.setChecked(True)
        forcenormalize.triggered.connect(normalize_force)

        self.ui.sliderForceSize = MenuSlider('Force size')
        self.ui.sliderForceSize.setMin(0)
        self.ui.sliderForceSize.slider.setValue(20.0)

        def set_force_size(value):
            if value < 1:
                self.visual.show_force = False
                self.run_code('self.visual.force_scale = 0', guiEventType.VIEWER_SETTINGS_UPDATE)
                self.visual.refresh_embeded_view()
            else:
                self.visual.show_force = True
                self.run_code(f'self.visual.force_scale = {value ** (2) / 10 : .2f}', guiEventType.VIEWER_SETTINGS_UPDATE)

        self.ui.sliderForceSize.connectvalueChanged(set_force_size)
        self.ui.menuView.addAction(self.ui.sliderForceSize)

        # cog size
        self.ui.menuView.addSeparator()

        def normalize_cog():
            self.run_code('self.visual.cog_do_normalize = not self.visual.cog_do_normalize',
                          guiEventType.VIEWER_SETTINGS_UPDATE)

        cognormalize = self.ui.menuView.addAction("View all CoGs at same size")
        cognormalize.setCheckable(True)
        cognormalize.setChecked(False)
        cognormalize.triggered.connect(normalize_cog)

        self.ui.sliderCoGSize = MenuSlider('CoG size')
        self.ui.sliderCoGSize.setMin(0)
        self.ui.sliderCoGSize.slider.setValue(20.0)

        def set_cog_size(value):
            if value < 1:
                self.visual.show_cog = False
                self.run_code(f'self.visual.cog_scale = 0', guiEventType.VIEWER_SETTINGS_UPDATE)
                self.visual.refresh_embeded_view()
            else:
                self.visual.show_cog = True
                self.run_code(f'self.visual.cog_scale = {value ** (1.3) / 100}', guiEventType.VIEWER_SETTINGS_UPDATE)

        self.ui.sliderCoGSize.connectvalueChanged(set_cog_size)
        self.ui.menuView.addAction(self.ui.sliderCoGSize)

        # visual opacity
        self.ui.sliderVisualAlpha = MenuSlider('Visual transparency')
        self.ui.sliderVisualAlpha.setMin(0)
        self.ui.sliderVisualAlpha.slider.setValue(100.0)

        def set_visualalpha(value):
            self.visual.visual_alpha = value / 100
            self.visual.update_visibility()
            self.visual.refresh_embeded_view()

        self.ui.sliderVisualAlpha.connectvalueChanged(set_visualalpha)
        self.ui.menuView.addAction(self.ui.sliderVisualAlpha)

        # light
        self.ui.sliderBrightness = MenuSlider('Sunshine')
        self.ui.sliderBrightness.setMin(0)
        self.ui.sliderBrightness.slider.setValue(20.0)
        def set_brightness(value):
            self.visual.light.SetIntensity(value/100)
            self.visual.refresh_embeded_view()
        self.ui.sliderBrightness.connectvalueChanged(set_brightness)
        self.ui.menuView.addAction(self.ui.sliderBrightness)

        self.ui.actionHorizontal_camera.triggered.connect(self.visual.level_camera)
        self.ui.action2D_mode.triggered.connect(self.visual.toggle_2D)

        self.ui.actionX.triggered.connect(lambda : self.camera_set_direction((1,0,0)))
        self.ui.action_x.triggered.connect(lambda : self.camera_set_direction((-1,0,0)))
        self.ui.actionY.triggered.connect(lambda : self.camera_set_direction((0,1,0)))
        self.ui.action_Y.triggered.connect(lambda : self.camera_set_direction((0,-1,0)))
        self.ui.actionZ.triggered.connect(lambda : self.camera_set_direction((0,0,-1)))
        self.ui.action_Z.triggered.connect(lambda : self.camera_set_direction((0,0,1)))
        self.ui.actionCamera_reset.triggered.connect(self.camera_reset)
        #




        # ======================= Code-highlighter ==============

        font = QFont()
        font.setPointSize(10)
        font.setFamily('Consolas')
        self.ui.teCode.setFont(font)
        self.ui.teCode.setTabStopDistance(QFontMetricsF(self.ui.teCode.font()).width(' ') * 4)

        self.highlight = PythonHighlighter(self.ui.teCode.document())

        self.eventFilter = ShiftEnterKeyPressFilter()
        self.eventFilter.callback = self.run_code_in_teCode
        self.ui.teCode.installEventFilter(self.eventFilter)

        # ======================== Docks ====================
        self.guiWidgets = dict()
        """Dictionary of all created guiWidgets (dock-widgets)"""

        def set_pb_style(pb):
            pb.setFlat(True)
            pb.setCheckable(True)
            pb.setAutoExclusive(True)
            self.ui.toolBar.addWidget(pb)

        # Workspace buttons
        btnConstruct= QtWidgets.QPushButton()
        btnConstruct.setText('&0. Library')
        btnConstruct.clicked.connect(self.import_browser)
        btnConstruct.setFlat(True)
        self.ui.toolBar.addWidget(btnConstruct)

        btnConstruct = QtWidgets.QPushButton()
        btnConstruct.setText('&1. Construct')
        btnConstruct.clicked.connect(lambda: self.activate_workspace("CONSTRUCT"))
        set_pb_style(btnConstruct)
        btnConstruct.setChecked(True)

        btnConstruct = QtWidgets.QPushButton()
        btnConstruct.setText('&2. Explore')
        btnConstruct.clicked.connect(lambda: self.activate_workspace("EXPLORE"))
        set_pb_style(btnConstruct)

        btnConstruct = QtWidgets.QPushButton()
        btnConstruct.setText('&3. Ballast')
        btnConstruct.clicked.connect(lambda: self.activate_workspace("BALLAST"))
        set_pb_style(btnConstruct)

        btnConstruct = QtWidgets.QPushButton()
        btnConstruct.setText('&4. Stability')
        btnConstruct.clicked.connect(lambda: self.activate_workspace("STABILITY"))
        set_pb_style(btnConstruct)

        btnConstruct = QtWidgets.QPushButton()
        btnConstruct.setText('&5. Mode Shapes [beta]')
        btnConstruct.clicked.connect(lambda: self.activate_workspace("DYNAMICS"))
        set_pb_style(btnConstruct)

        btnConstruct = QtWidgets.QPushButton()
        btnConstruct.setText('&6. Airy [beta]')
        btnConstruct.clicked.connect(lambda: self.activate_workspace("AIRY"))
        set_pb_style(btnConstruct)

        space = QtWidgets.QWidget()
        space.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.ui.toolBar.addWidget(space)

        self._active_workspace = None
        self.activate_workspace('CONSTRUCT')

        # ======================== Finalize ========================
        splash.finish(self.MainWindow)
        self.MainWindow.show()

        if block:
            self.ui.pbUpdate.setVisible(False)
            self.app.exec_()

    def show_labels_menu(self):
        self.labels_menu.exec_(QCursor.pos())

    def show_label_toggled(self):
        types = []
        for item in self.ui.label_menu_actions:
            if item.isChecked():
                name = item.data()
                if name == 'Point':
                    types.append(Point)
                elif name == 'Cable':
                    types.append(Cable)
                elif name == 'Tank':
                    types.append(Tank)
                else:
                    raise ValueError(name)

        if types:
            self.visual.show_only_labels_of_nodes_type(tuple(types))
        else:
            self.visual.show_only_labels_of_nodes_type(None)


    def copy_screenshot_code(self):

        sea = self.visual.show_global
        camera_pos = self.visual.screen.camera.GetPosition()
        lookat = self.visual.screen.camera.GetFocalPoint()

        code = f'show(s, sea = {sea}, camera_pos = {camera_pos}, lookat = {lookat}'
        if self.visual.visual_alpha < 1.0:
            code += f',visual_alpha = {self.visual.visual_alpha}'
        if not self.visual.show_meshes:
            code += ',do_meshes = False'
        if self.visual.geometry_scale != 1:
            code += f', geometry_size = {self.visual.geometry_scale}'
        if self.visual.force_do_normalize:
            code += ', force_normalize = True'
        if self.visual.force_scale != 1:
            code += f', force_scale = {self.visual.force_scale}'
        if self.visual.cog_do_normalize:
            code += ', cog_normalize = True'
        if self.visual.cog_scale != 1:
            code += f', cog_scale = {self.visual.cog_scale}'
        code += ')'

        print(code)
        self.app.clipboard().setText(code)


    def escPressed(self):
        self.animation_terminate()  # terminate any running animations
        self.select_none()

    def select_none(self):
        if self.selected_nodes:
            self.selected_nodes.clear()
            if 'Properties' in self.guiWidgets:
                self.guiWidgets['Properties'].setVisible(False)
            self.guiEmitEvent(guiEventType.SELECTION_CHANGED)



    def savepoint_restore(self):

        if self.scene._savepoint is not None:
            self.animation_terminate(keep_current_dofs=True)

        if self.scene.savepoint_restore():
            self.select_none()
            self.guiEmitEvent(guiEventType.MODEL_STRUCTURE_CHANGED)


    def activate_workspace(self, name):

        self._active_workspace = name

        self.animation_terminate()
        self.savepoint_restore()


        self.visual.set_alpha(1.0)
        self.visual.hide_actors_of_type([ActorType.BALLASTTANK])
        self.visual.update_outlines()

        for g in self.guiWidgets.values():
            g.close()

        if name == 'CONSTRUCT':
            self.show_guiWidget('Node Tree', WidgetNodeTree)
            self.show_guiWidget('Derived Properties', WidgetDerivedProperties)
            self.show_guiWidget('Properties', WidgetNodeProps)
            self.show_guiWidget('Rigg-it-Right', WidgetRiggItRight)

        if name == 'EXPLORE':
            self.show_guiWidget('Derived Properties', WidgetDerivedProperties)
            self.show_guiWidget('Explore 1-to-1', WidgetExplore)

        if name == 'DYNAMICS':
            self.show_guiWidget('Properties - dynamic', WidgetDynamicProperties)
            self.show_guiWidget('Mode-shapes', WidgetModeShapes)

        if name == 'BALLAST':
            self.show_guiWidget('Ballast system', WidgetBallastSystemSelect)
            self.show_guiWidget('Tanks', WidgetBallastConfiguration)
            self.show_guiWidget('Solver', WidgetBallastSolver)
            self.show_guiWidget('Tank order', WidgetTankOrder)
            self.visual.show_actors_of_type([ActorType.BALLASTTANK])

        if name == 'STABILITY':
            self.show_guiWidget('Stability', WidgetDisplacedStability)

        if name == 'AIRY':
            self.scene.savepoint_make()
            code = "from DAVE.frequency_domain import prepare_for_fd\nprepare_for_fd(s)"
            self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)
            self.show_guiWidget('Airy waves', WidgetAiry)



    def import_browser(self):

        G = DAVE.gui.standard_assets.Gui()
        r = G.showModal()

        if r is not None:
            file = r[0]
            container = r[1]
            prefix = r[2]
            code = 's.import_scene(s.get_resource_path("{}"), containerize={}, prefix="{}")'.format(file,container,prefix)
            self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

            self.activate_workspace('CONSTRUCT')


    # ============== Animation functions =============


    def animation_running(self):
        """Returns true is an animation is running"""
        return self._timerid is not None

    def timerEvent(self,a,b):

        if self._timerid is None:  # timer is going to be destroyed
            return

        t = time.time() - self._animation_start_time  # time since start of animation in [s]

        t *= self._animation_speed

        if self._animation_loop:
            t = np.mod(t, self._animation_length)
        else:
            if t>self._animation_length:
                self.animation_terminate()
                return

        self.animation_activate_time(t)

        self.ui.aniSlider.setValue(t*1000)

    def animation_speed_change(self):
        self._animation_speed = self.ui.sbPlaybackspeed.value()

    def animation_activate_time(self,t):
        dofs = self._animation_keyframe_interpolation_object(t)
        self.scene._vfc.set_dofs(dofs)
        self.visual.update_dynamic_waveplane(t)
        self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)


    def animation_terminate(self, keep_current_dofs = False):

        #if not self.animation_running():
        #    return # nothing to destroy
        if not self._animation_available:
            return

        self.ui.frameAni.setVisible(False)

        # print('Destroying timer')
        if self._timerid is not None:
            to_be_destroyed = self._timerid
            self._timerid = None
            iren = self.visual.renwin.GetInteractor()
            iren.DestroyTimer(to_be_destroyed)

        self._animation_available = False
        self.visual.remove_dynamic_wave_plane()

        # restore DOFs
        if not keep_current_dofs:
            self.scene._vfc.set_dofs(self._animation_final_dofs)
            self.visual.quick_updates_only = False
            self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)
        self.visual.quick_updates_only = False


    def animation_start(self, t, dofs, is_loop, final_dofs = None, do_not_reset_time=False, show_animation_bar = True):
        """Start an new animation

        Args:
            t:    List of times at keyframes
            dofs: List of dofs at keyframes
            is_loop: Should animation be played in a loop (bool)
            final_dofs : [optional] DOFS to be set when animation is finished or terminated. Defaults to last keyframe
            do_not_reset_time : do not reset the time when starting the animation, this means the loop continues where it was.


        """
        self.animation_terminate(keep_current_dofs=True) # end old animation, if any

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

        self.ui.aniSlider.setMaximum(1000*self._animation_length)
        self.ui.frameAni.setVisible(show_animation_bar)

        self._animation_available = True

        if not show_animation_bar:          # override pause for short animations
            self.ui.btnPauseAnimation.setChecked(False)
            self._animation_paused = False

        if not self._animation_paused:

            iren = self.visual.renwin.GetInteractor()
            if self._timerid is None:
                self._timerid = iren.CreateRepeatingTimer(round(1000 / DAVE.settings.GUI_ANIMATION_FPS))

            else:
                raise Exception("could not create new timer, old timer is still active")


    def animation_pause(self):
        """Pauses a running animation"""

        if self._animation_paused:
            return

        if self._timerid is not None:
            to_be_destroyed = self._timerid
            self._timerid = None
            iren = self.visual.renwin.GetInteractor()
            iren.DestroyTimer(to_be_destroyed)

        self._animation_paused = True

    def animation_continue(self):

        if not self._animation_paused:
            return

        if self._animation_available:
            if self._timerid is None:
                iren = self.visual.renwin.GetInteractor()
                self._timerid = iren.CreateRepeatingTimer(round(1000 / DAVE.settings.GUI_ANIMATION_FPS))

        self._animation_paused = False

    def animation_pause_or_continue_click(self):
        """Pauses or continues the animation"""
        if self.ui.btnPauseAnimation.isChecked():
            self.animation_continue()
        else:
            self.animation_pause()
            remember = self.visual.quick_updates_only
            self.visual.quick_updates_only = False
            self.animation_activate_time(self.ui.aniSlider.value() / 1000)
            self.visual.quick_updates_only = remember


    def animation_change_time(self):

        # only works if animation is paused
        if not self._animation_paused:
            return

        t = self.ui.aniSlider.value() / 1000
        remember = self.visual.quick_updates_only
        self.visual.quick_updates_only = False
        self.animation_activate_time(t)
        self.visual.quick_updates_only = remember

    # =================================================== end of animation functions ==================


    def onClose(self):
        self.visual.shutdown_qt()
        print('-- closing the gui : these were the actions you performed while the gui was open --')
        print(self.give_clean_history())


    def show_exception(self, e):
        self.ui.teFeedback.setText(str(e))
        self.ui.teFeedback.setStyleSheet("background-color: pink;")



    def run_code(self, code, event):
        """Runs the provided code

        If succesful, add code to history
        If not, set code as current code
        """

        before = self.scene._nodes.copy()

        s = self.scene

        self.ui.pbExecute.setStyleSheet("background-color: yellow;")

        self.ui.teFeedback.setStyleSheet("")
        self.ui.teFeedback.clear()




        with capture_output() as c:

            try:
                exec(code)

                if c.stdout:
                    self.ui.teFeedback.append(c.stdout)
                    self.ui.teFeedback.append(str(datetime.datetime.now()))
                else:
                    self.ui.teFeedback.append("Succes at " + str(datetime.datetime.now()))

                self._codelog.append(code)
                self.ui.teHistory.append(code)

                self.ui.teHistory.verticalScrollBar().setValue(
                    self.ui.teHistory.verticalScrollBar().maximum())  # scroll down all the way

                # See if selected nodes are still valid and identical to the ones
                to_be_removed = []
                for node in self.selected_nodes:
                    if node not in self.scene._nodes:
                        to_be_removed.append(node)

                for node in to_be_removed:
                    self.selected_nodes.remove(node)



                # if we created something new, then select it
                emitted = False
                for node in self.scene._nodes:
                    if node not in before:
                        self.selected_nodes.clear()
                        # self.selected_nodes.append(node)
                        # self.guiEmitEvent(guiEventType.SELECTION_CHANGED)
                        self.guiSelectNode(node)
                        emitted = True
                        break

                if event is not None:
                    self.guiEmitEvent(event)

                if to_be_removed and not emitted:
                    self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED)



            except Exception as E:

                self.ui.teCode.clear()
                self.ui.teCode.append(code)

                self.ui.teCode.update()
                self.ui.teCode.repaint()

                self.ui.teFeedback.setText(c.stdout + '\n' + str(E) + '\n\nWhen running: \n\n' + code)
                self.ui.teFeedback.setStyleSheet("background-color: pink;")

            self.ui.pbExecute.setStyleSheet("")
            self.ui.pbExecute.update()
            self.ui.teFeedback.verticalScrollBar().setValue(self.ui.teFeedback.verticalScrollBar().maximum()) # scroll down all the way





    def stop_solving(self):
        self._terminate = True

    def solve_statics(self):
        self.scene.update()
        old_dofs = self.scene._vfc.get_dofs()

        if len(old_dofs) == 0:  # no degrees of freedom

            self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)  # update the gui to reflect the scene.update

            msgBox = QMessageBox()
            msgBox.setText("No degrees of freedom - nothing to solve")
            msgBox.setWindowTitle("DAVE")
            msgBox.exec_()

            print('No dofs')
            return

        self._dofs = old_dofs.copy()

        long_wait = False
        dialog = None

        self._terminate = False

        original_dofs = self.scene._fix_vessel_heel_trim()

        while True:

            # Returns
            # -2  done, unstable solution for unable to converge to another one
            # -1  done, unstable solution
            # 0   done, stable equilibrium (if checked) or unknonwn equilibrium (if not checked)
            #
            # 1   time-out or fail during linear-dof solve   - state not in equilibrium
            # 2   time-out or fail during full-dof solve     - state not in equilibrium
            #
            # Positive (1,2) return argument can be passed as input (phases_completed) to continue where we timed-out.
            #
            # */
            # int Scene::stateSolve(bool doStabilityCheck, double timeout,
            # 	bool do_prepare_state,
            # 	bool solve_linear_dofs_first,
            # 	double stability_check_delta)

            timeout = 0.5
            do_stability_check = True
            do_prepare_state = True
            solve_linear_dofs_first = True
            delta = 0 # default

            status = self.scene._vfc.state_solve_statics_with_timeout(do_stability_check,
                                                                      timeout,
                                                                      do_prepare_state,
                                                                      solve_linear_dofs_first,
                                                                      delta)

            message = 'Maximum error = {}'.format(self.scene._vfc.Emaxabs)

            if self._terminate:
                print('Terminating')
                self.scene._restore_original_fixes(original_dofs)
                break

            if (status == 0) or (status==-2):  # solving done

                # solving exited with succes

                if original_dofs:  # reset original dofs and go to phase 2
                    self.scene._restore_original_fixes(original_dofs)
                    original_dofs = None
                    # continue
                else: # done

                    # see if all geometric contacts are ok
                    # if not then continue
                    changed, msg = self.scene._check_and_fix_geometric_contact_orientations()
                    message += '\n' + msg
                    if not changed:
                        # we are done!
                        break

            if dialog is None:
                dialog = SolverDialog()
                dialog.btnTerminate.clicked.connect(self.stop_solving)
                dialog.show()
                long_wait = True

            dialog.label_2.setText(message)

            dialog.update()

            self.visual.position_visuals()
            self.visual.refresh_embeded_view()
            self.app.processEvents()

        if dialog is not None:
            dialog.close()

        try:
            # See if we can get the debug-log
            dofs = self.scene._vfc.get_solve_dofs_log()
            n_steps = len(dofs)
            if n_steps <= 2:
                new_dofs = self.scene._vfc.get_dofs()
                self.animate_change(old_dofs, new_dofs, 10)
                return # nothing to animate

            ts = np.linspace(0,10,num=n_steps)
            self.animation_start(t=ts, dofs=dofs, is_loop=True)
        except AttributeError:
            if DAVE.settings.GUI_DO_ANIMATE and not long_wait:
                new_dofs = self.scene._vfc.get_dofs()
                self.animate_change(old_dofs, new_dofs, 10)


        self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)
        self._codelog.append('s.solve_statics()')

    def animate_change(self, old_dof, new_dof, n_steps):
        """Animates from old_dof to new_dofs in n_steps"""

        if len(old_dof) != len(new_dof):
            return

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

        self.animation_start(t,dofs,is_loop=False, show_animation_bar=False)


    def to_blender(self):

        from DAVE.io.blender import create_blend_and_open

        if self.animation_running():
            dofs = []

            n_frames = np.round(self._animation_length * DAVE.settings.BLENDER_FPS)
            for t in np.linspace(0,self._animation_length, int(n_frames)):
                dofs.append(self._animation_keyframe_interpolation_object(t))

        else:
            dofs = None

        create_blend_and_open(self.scene, animation_dofs=dofs, wavefield=self.visual._wavefield)

    def toggle_show_global(self):
        self.ui.actionShow_water_plane.setChecked(not self.ui.actionShow_water_plane.isChecked())
        self.toggle_show_global_from_menu()

    def toggle_show_global_from_menu(self):
        self.visual.show_global = self.ui.actionShow_water_plane.isChecked()
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def toggle_show_force_applying_elements(self):
        self.visual.show_meshes = self.ui.actionShow_force_applying_element.isChecked()
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def camera_set_direction(self,vector):
        self.visual.set_camera_direction(vector)
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def camera_reset(self):
        self.visual.camera_reset()


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

    def menu_export_orcaflex_yml(self):
        filename, _ = QFileDialog.getSaveFileName(filter="*.yml", caption="Orcaflex .yml file",directory=self.scene.resources_paths[0])
        if filename:
            code = 'from DAVE.io.orcaflex import export_ofx_yml\nexport_ofx_yml(s,r"{}")'.format(filename)
            self.run_code(code, guiEventType.NOTHING)

    def menu_export_orcaflex_package(self):
        filename, _ = QFileDialog.getSaveFileName(filter="*.py", caption="Python files",directory=self.scene.resources_paths[0])
        if filename:
            python_file = filename
            ofx_file = python_file + '.yml'
            code = 'from DAVE.io.orcaflex import export_ofx_yml, write_ofx_run_and_collect_script\nexport_ofx_yml(s,r"{}")'.format(ofx_file)
            code+= '\nwrite_ofx_run_and_collect_script(r"{}", r"{}")'.format(python_file, ofx_file)
            self.run_code(code, guiEventType.NOTHING)


    def tidy_history(self):
        self.ui.teHistory.setText(self.give_clean_history())

    def give_clean_history(self):
        prev_line = ''

        f = []
        for s in self._codelog:

            # filter repeated assignments to same target
            if s.split('=')[0] == prev_line.split('=')[0]:
                prev_line = s
                continue

            f.append(prev_line)
            prev_line = s

        f.append(prev_line)

        return '\n'.join(f)


    def menu_save_actions(self):
        filename, _ = QFileDialog.getSaveFileName(filter="*.dave", caption="Scene files",directory=self.scene.resources_paths[0])
        if filename:

            prev_line = ''

            f = open(filename, 'w+')
            for s in self._codelog:

                # filter repeated assignments to same target
                if s.split('=')[0] == prev_line.split('=')[0]:
                    prev_line = s
                    continue

                f.write(prev_line + '\n')
                prev_line = s

            f.write(prev_line + '\n')
            f.close()

    def feedback_copy(self):
        self.app.clipboard().setText(self.ui.teFeedback.toPlainText())

    def history_copy(self):
        self.app.clipboard().setText(self.ui.teHistory.toPlainText())

    def clear_code(self):
        self.ui.teCode.clear()
        self.ui.teCode.setFocus()


    def generate_scene_code(self):
        self.ui.teFeedback.setText(self.scene.give_python_code())

    def run_code_in_teCode(self):
        code = self.ui.teCode.toPlainText()
        self.run_code(code,guiEventType.FULL_UPDATE)

    def rightClickViewport(self, point):
        globLoc = self.ui.frame3d.mapToGlobal(point)
        name = None
        try:
            name = self.selected_nodes[0].name
        except:
            pass

        self.openContextMenyAt(name, globLoc)


    def openContextMenyAt(self, node_name, globLoc):
        menu = QtWidgets.QMenu()

        if node_name is not None:

            node = self.scene[node_name]

            if node._manager is None:

                def edit():
                    self.selected_nodes.clear()
                    self.guiSelectNode(node_name)
                    self.show_guiWidget('Properties', WidgetNodeProps) # people often close this one

                menu.addAction("Edit {}".format(node_name), edit)

                showhide = menu.addAction("Visible")
                showhide.setCheckable(True)

                showhide.setChecked(node.visible)

                if node.visible:
                    showhide.triggered.connect(lambda: self.run_code(f"s['{node_name}'].visible = False",guiEventType.VIEWER_SETTINGS_UPDATE))
                else:
                    showhide.triggered.connect(lambda: self.run_code(f"s['{node_name}'].visible = True",guiEventType.VIEWER_SETTINGS_UPDATE))

                def delete():
                    self.run_code('s.delete("{}")'.format(node_name), guiEventType.MODEL_STRUCTURE_CHANGED)

                def dissolve():
                    self.run_code('s.dissolve("{}")'.format(node_name), guiEventType.MODEL_STRUCTURE_CHANGED)

                menu.addAction("Delete {}".format(node_name), delete)
                menu.addAction("Dissolve (Evaporate) {}".format(node_name), dissolve)


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

                    self.guiSelectNode(name_of_duplicate)


                menu.addAction("Duplicate", duplicate)
                menu.addSeparator()
                menu.addSeparator()


        wa = QtWidgets.QWidgetAction(None)

        ui = Ui_MenuNodes()
        widget = QtWidgets.QWidget()
        ui.setupUi(widget)
        wa.setDefaultWidget(widget)

        ui.pbPoint.clicked.connect(self.new_point)
        ui.pbCircle.clicked.connect(self.new_circle)
        ui.pbAxis.clicked.connect(self.new_axis)
        ui.pbBody.clicked.connect(self.new_body)
        ui.pbGeometricContact.clicked.connect(self.new_geometric_contact)

        ui.pbSpring2D.clicked.connect(self.new_connector2d)
        ui.pbSpring6D.clicked.connect(self.new_linear_connector)

        ui.pbForce.clicked.connect(self.new_force)

        ui.pbContactShape.clicked.connect(self.new_contactmesh)
        ui.pbContactBall.clicked.connect(self.new_contactball)

        ui.pbTank.clicked.connect(self.new_tank)
        ui.pbBuoyancyShape.clicked.connect(self.new_buoyancy_mesh)
        ui.pbLinearBuoyancy.clicked.connect(self.new_linear_hydrostatics)
        ui.pbWaveInteraction.clicked.connect(self.new_waveinteraction)

        ui.pbCable.clicked.connect(self.new_cable)
        ui.pbSling.clicked.connect(self.new_sling)
        ui.pbShackle.clicked.connect(self.new_shackle)
        ui.pbBeam.clicked.connect(self.new_beam)

        ui.pbVisual.clicked.connect(self.new_visual)



        menu.addAction(wa)

        menu.exec_(globLoc)


    def new_axis(self):
        self.new_something(new_node_dialog.add_axis)

    def new_body(self):
        self.new_something(new_node_dialog.add_body)

    def new_point(self):
        self.new_something(new_node_dialog.add_poi)

    def new_cable(self):
        self.new_something(new_node_dialog.add_cable)

    def new_force(self):
        self.new_something(new_node_dialog.add_force)

    def new_circle(self):
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

    def new_tank(self):
        self.new_something(new_node_dialog.add_tank)

    def new_contactmesh(self):
        self.new_something(new_node_dialog.add_contactmesh)

    def new_contactball(self):
        self.new_something(new_node_dialog.add_contactball)

    def new_waveinteraction(self):
        self.new_something(new_node_dialog.add_waveinteraction)

    def new_shackle(self):
        self.new_something(new_node_dialog.add_shackle)

    def new_sling(self):
        self.new_something(new_node_dialog.add_sling)

    def new_geometric_contact(self):
        msgBox = QMessageBox()
        msgBox.setText("To create a Geometric Contact:\n\nDrag a circle onto another circle (in the node-tree)")
        msgBox.setWindowTitle("Geometric contact")
        msgBox.exec_()


    def new_something(self, what):
        r = what(self.scene, self.selected_nodes)
        if r:
            self.run_code("s." + r, guiEventType.MODEL_STRUCTURE_CHANGED)
            # self.guiEmitEvent(guiEventType.SELECTION_CHANGED)
            # added_node = self.scene._nodes[-1]
            # self.guiSelectNode(added_node)


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

            self.selected_nodes.remove(node)

            # if node has a manager, then select the manager
            if node.manager is not None:
                self.guiSelectNode(node.manager)
                return


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

        visually_selected_nodes = self.selected_nodes.copy()

        for node in self.selected_nodes:
            if isinstance(node, Manager):
                visually_selected_nodes.extend(node.managed_nodes())

        for v in self.visual.visuals:
            if v.node in visually_selected_nodes:
                v.select()
            else:
                v.deselect()

        for v in self.visual.visuals:
            try:
                parent = v.node.parent
            except:
                continue

            if parent in visually_selected_nodes:
                v.make_transparent()
            else:
                v.reset_opacity()



    # ================= guiWidget codes

    def guiEmitEvent(self, event, sender=None):
        for widget in self.guiWidgets.values():
            if not (widget is sender):
                if widget.isVisible():
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

        if event== guiEventType.MODEL_STATE_CHANGED:
            self.visual.position_visuals()
            self.refresh_3dview()
            return

        if event == guiEventType.VIEWER_SETTINGS_UPDATE:
            self.visual.update_visibility()
            self.visual.position_visuals()
            self.refresh_3dview()
            return

        self.visual.create_visuals()
        self.visual.add_new_actors_to_screen()
        self.visual.position_visuals()
        self.visual_update_selection()
        self.refresh_3dview()

    def guiSelectNode(self, node_name):
        # print('selecting a node with name {}'.format(node_name))

        old_selection = self.selected_nodes.copy()

        if not (self.app.keyboardModifiers() and QtCore.Qt.KeyboardModifier.ControlModifier):
            self.selected_nodes.clear()


        node = self.scene._node_from_node_or_str(node_name)
        if node not in self.selected_nodes:
            self.selected_nodes.append(node)

        if self.selected_nodes:
            if self._active_workspace == 'CONSTRUCT':
                if 'Properties' in self.guiWidgets:
                    if not self.guiWidgets['Properties'].isVisible():
                        self.guiWidgets['Properties'].setVisible(True)
                        self.guiEmitEvent(guiEventType.SELECTION_CHANGED) # force update

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

# ====== nodeA code ======

if __name__ == '__main__':
    pass