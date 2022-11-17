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
import subprocess
from copy import deepcopy
import logging

from DAVE.gui.helpers.my_qt_helpers import DeleteEventFilter
from DAVE.visual_helpers.vtkBlenderLikeInteractionStyle import DragInfo
from DAVE.gui.widget_BendingMoment import WidgetBendingMoment
from DAVE.gui.widget_footprints import WidgetFootprints
from DAVE.gui.widget_limits import WidgetLimits
from DAVE.gui.widget_painter import WidgetPainters
from DAVE.gui.widget_tags import WidgetTags

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

import DAVE.auto_download

from PySide2.QtCore import Qt
from PySide2.QtCore import QSettings
from PySide2.QtGui import QIcon, QPixmap, QFont, QFontMetricsF, QCursor
from PySide2.QtWidgets import (
    QDialog,
    QFileDialog,
    QMessageBox,
    QMenu,
    QWidgetAction,
    QAction, QStatusBar,
)
from DAVE.scene import Scene

from DAVE.gui.forms.main_form import Ui_MainWindow
from DAVE.visual import Viewport, ActorType, DelayRenderingTillDone
from DAVE.gui import new_node_dialog
import DAVE.gui.standard_assets
from DAVE.gui.forms.dlg_solver import Ui_Dialog
from DAVE.gui.forms.dlg_settingsr import Ui_frmSettings
import DAVE.settings
from DAVE.settings_visuals import PAINTERS

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
from DAVE.gui.widget_rigg_it_right import WidgetQuickActions
from DAVE.gui.widget_environment import WidgetEnvironment

import numpy as np

# resources
import DAVE.gui.forms.resources_rc

# ========================================================
#   Settings for customization of the GUI
# ========================================================
#
# List with of tupple with (Button text, WORKSPACE_ID)
#
# These buttons are created in the tool-bar.
# Clicking a button will call activate_workspace with WORKSPACE_ID
DAVE_GUI_WORKSPACE_BUTTONS = [
    ("Construct", "CONSTRUCT"),
    ("Explore", "EXPLORE"),
    ("Ballast", "BALLAST"),
    ("Shear and Bending", "MOMENTS"),
    ("Environment", "ENVIRONMENT"),
    ("Stability", "STABILITY"),
    ("Limits", "LIMITS"),
    ("Tags", "TAGS"),
    ("Mode shapes [beta]", "DYNAMICS"),
    ("Airy [beta]", "AIRY"),
]

DAVE_GUI_PLUGINS_INIT=[]
DAVE_GUI_PLUGINS_WORKSPACE=[]
DAVE_GUI_PLUGINS_CONTEXT=[]
DAVE_GUI_PLUGINS_EDITOR=[]

# ====================================================

class UndoType(Enum):
    CLEAR_AND_RUN_CODE = 1
    RUN_CODE = 2
    SET_DOFS = 3


class SolverDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(SolverDialog, self).__init__(parent)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/icons/cube.png"))


class SettingsDialog(QDialog, Ui_frmSettings):
    def __init__(self, scene, gui, parent=None):
        super(SettingsDialog, self).__init__(parent)
        Ui_frmSettings.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/icons/cube.png"))

        paths_str = ['- ' + str(p) for p in scene.resources_paths if p not in gui.additional_user_resource_paths]
        self.label_4.setText('\n'.join(paths_str))

        paths_str = [str(p) for p in gui.additional_user_resource_paths]
        self.plainTextEdit.setPlainText('\n'.join(paths_str))


class Gui:
    def __init__(
        self,
        scene=None,
        splash=None,
        app=None,
        geometry_scale=-1,
        cog_scale=0.25,
        block=True,
        workspace=None,
        painters=None,
    ):
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
            workspace (string) : open the workspace with this name
            plugins_init [ () ] : iterable of functions that are to be called at the end of the __init__ function
            painters: [None] (str) painters to activate

        """

        self.plugins_workspace = DAVE_GUI_PLUGINS_WORKSPACE
        self.plugins_context = DAVE_GUI_PLUGINS_CONTEXT
        self.plugins_editor = DAVE_GUI_PLUGINS_EDITOR

        if app is None:

            if QtWidgets.QApplication.instance() is not None:
                self.app = QtWidgets.QApplication.instance()
            else:
                self.app = QtWidgets.QApplication()
        else:
            self.app = app


        self.app.aboutToQuit.connect(self.onCloseApplication)

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
        self.MainWindow.closeEvent = self.closeEvent

        self.statusbar = QStatusBar()
        self.MainWindow.setStatusBar(self.statusbar)
        self.statusbar.mousePressEvent = self.show_python_console

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
        self.selected_nodes: [Node] = []
        """A list of selected nodes (if any)"""

        self.scene = scene
        """Reference to a scene"""
        self.scene.gui_solve_func = self.solve_statics_using_gui_on_scene

        self.modelfilename = None
        """Open file"""

        self._model_has_changed = False
        """User"""

        self.additional_user_resource_paths = []
        """User-defined additional resource paths, stored on user machine - settings dialog"""

        settings = QSettings("rdbr", "DAVE")
        paths_str = settings.value(f"additional_paths")
        if paths_str:
            for p in paths_str.split(';'):
                if p:
                    self.additional_user_resource_paths.append(Path(p))
                    self.scene.resources_paths.append(Path(p))

        self.update_resources_paths()

        # ======================== Modify dock layout options ============

        self.MainWindow.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.MainWindow.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.MainWindow.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)
        self.MainWindow.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)

        # ======================== Create 3D viewport ====================
        self.visual = Viewport(scene)
        """Reference to a viewport"""

        if painters is None:
            painters = "Construction"  # use as default

        self.visual.settings.painter_settings = PAINTERS[painters]

        self.ui.cbPainerSelect.addItems([str(k) for k in PAINTERS.keys()])
        self.ui.cbPainerSelect.currentIndexChanged.connect(self.change_paintset)

        if cog_scale >= 0:
            self.visual.cog_scale = cog_scale

        if geometry_scale >= 0:
            self.visual.geometry_scale = geometry_scale

        self.visual.create_node_visuals(recreate=True)
        self.visual.show_embedded(self.ui.frame3d)

        self.visual.position_visuals()
        self.visual.update_visibility()  # apply paint
        self.visual.add_new_node_actors_to_screen()

        self.visual.Style.callbackSelect = self.view3d_select_element
        self.visual.focus_on_selected_object = self.focus_on_selected_object

        # right-click event for
        self.ui.frame3d.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.frame3d.customContextMenuRequested.connect(self.rightClickViewport)

        self._timerid = None
        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver("TimerEvent", self.timerEvent)

        # ------ key-presses -----

        self.visual.Style.callbackEscapeKey = self.escPressed
        self.visual.Style.callbackDeleteKey = self.delete_key
        self.visual.Style.callbackFocusKey = self.focus_on_selected_object
        self.visual.Style.callbackStartDrag = self.start_node_drag
        self.visual.Style.callbackEndDrag = self.node_dragged
        self.visual.Style.callbackMeasure = self.measured_in_viewport

        # ------ viewport buttons ------

        # right
        self.ui.btnWater.clicked.connect(self.toggle_show_global)
        self.ui.pbUC.clicked.connect(self.toggle_show_UC)
        self.ui.btnBlender.clicked.connect(self.to_blender)
        self.ui.pbCopyViewCode.clicked.connect(self.copy_screenshot_code)
        self.ui.btnSSAO.clicked.connect(self.toggle_SSAO)
        self.ui.btnZoomFit.clicked.connect(self.camera_reset)

        # left
        self.ui.pbUpdate.clicked.connect(
            lambda: self.guiEmitEvent(guiEventType.FULL_UPDATE)
        )
        self.ui.btnSolveStatics.clicked.connect(self.solve_statics)
        # self.ui.btnUndoStatics.clicked.connect(self.undo_solve_statics)

        # bottom
        self.ui.pbExecute.clicked.connect(self.run_code_in_teCode)
        self.ui.pbCopyOutput.clicked.connect(self.feedback_copy)
        self.ui.pbCopyHistory.clicked.connect(self.history_copy)
        self.ui.pbGenerateSceneCode.clicked.connect(self.generate_scene_code)
        self.ui.pbClearCode.clicked.connect(self.clear_code)
        self.ui.tbTidyHistory.clicked.connect(self.tidy_history)

        # ------ animation buttons ------
        self.ui.frameAni.setVisible(False)
        self.ui.btnStopAnimation.clicked.connect(
            lambda: self.animation_terminate(False)
        )
        self.ui.btnPauseAnimation.clicked.connect(
            self.animation_pause_or_continue_click
        )
        self.ui.aniSlider.valueChanged.connect(self.animation_change_time)
        self.ui.sbPlaybackspeed.valueChanged.connect(self.animation_speed_change)

        # ======================== Main Menu entries  ======

        self.ui.actionNew.triggered.connect(self.clear)
        self.ui.actionReload_components.triggered.connect(self.refresh_model)
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.menu_save_model)
        self.ui.actionSave.setEnabled(False)
        self.ui.actionSave_scene.triggered.connect(self.menu_save_model_as)
        self.ui.actionSettings.triggered.connect(self.show_settings)
        self.ui.actionSave_actions_as.triggered.connect(self.menu_save_actions)
        self.ui.actionImport_sub_scene.triggered.connect(self.menu_import)
        self.ui.actionImport_browser.triggered.connect(self.import_browser)
        self.ui.actionOrcaflex.triggered.connect(self.menu_export_orcaflex_yml)
        self.ui.actionOrcaflex_package.triggered.connect(
            self.menu_export_orcaflex_package
        )
        self.ui.actionBlender.triggered.connect(self.to_blender)

        # --- recent files ---

        self.recent_files = []
        self.ui.menuSolve_Statics.addSeparator()
        for i in range(8):
            action = QAction("none")
            action.triggered.connect(lambda *args, a=i: self.open_recent(a))
            self.recent_files.append(action)
            self.ui.menuSolve_Statics.addAction(action)
        self.update_recent_file_menu()

        # -- drag drop files into DAVE --

        self.ui.frame3d.dropEvent = self.drop
        self.ui.frame3d.dragEnterEvent = self.drag_enter

        # -- visuals --
        self.ui.actionShow_water_plane.triggered.connect(
            self.toggle_show_global_from_menu
        )
        self.ui.actionShow_force_applying_element.triggered.connect(
            self.toggle_show_force_applying_elements
        )

        self.ui.sliderGeometrySize = MenuSlider("Geometry size")
        self.ui.sliderGeometrySize.setMin(0)
        self.ui.sliderGeometrySize.slider.setValue(20)

        def set_geo_size(value):
            if value < 1:
                self.visual.show_geometry = False
                self.run_code(
                    "self.visual.settings.geometry_scale = 0",
                    guiEventType.VIEWER_SETTINGS_UPDATE,
                )
                # self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)
            else:
                self.visual.show_geometry = True
                self.run_code(
                    f"self.visual.settings.geometry_scale = {value**(1.8)/100 : .2f}",
                    guiEventType.VIEWER_SETTINGS_UPDATE,
                )

        self.ui.sliderGeometrySize.connectvalueChanged(set_geo_size)
        self.ui.menuView.addAction(self.ui.sliderGeometrySize)

        # force size
        self.ui.menuView.addSeparator()

        def normalize_force():
            self.run_code(
                "self.visual.settings.force_do_normalize = not self.visual.settings.force_do_normalize",
                guiEventType.VIEWER_SETTINGS_UPDATE,
            )

        forcenormalize = self.ui.menuView.addAction("View all forces at same size")
        forcenormalize.setCheckable(True)
        forcenormalize.setChecked(True)
        forcenormalize.triggered.connect(normalize_force)
        self.ui.forcenormalize = forcenormalize

        self.ui.sliderForceSize = MenuSlider("Force size")
        self.ui.sliderForceSize.setMin(0)
        self.ui.sliderForceSize.slider.setValue(20.0)

        def set_force_size(value):
            if value < 1:
                self.visual.show_force = False
                self.run_code(
                    "self.visual.settings.force_scale = 0",
                    guiEventType.VIEWER_SETTINGS_UPDATE,
                )
                self.visual.refresh_embeded_view()
            else:
                self.visual.show_force = True
                self.run_code(
                    f"self.visual.settings.force_scale = {value ** (2) / 10 : .2f}",
                    guiEventType.VIEWER_SETTINGS_UPDATE,
                )

        self.ui.sliderForceSize.connectvalueChanged(set_force_size)
        self.ui.menuView.addAction(self.ui.sliderForceSize)

        # labels
        self.ui.actionShow_labels.triggered.connect(self.labels_show_hide)

        # cog size
        self.ui.menuView.addSeparator()

        def normalize_cog():
            self.run_code(
                "self.visual.settings.cog_do_normalize = not self.visual.settings.cog_do_normalize",
                guiEventType.VIEWER_SETTINGS_UPDATE,
            )

        cognormalize = self.ui.menuView.addAction("View all CoGs at same size")
        cognormalize.setCheckable(True)
        cognormalize.setChecked(False)
        cognormalize.triggered.connect(normalize_cog)
        self.ui.cognormalize = cognormalize

        self.ui.sliderCoGSize = MenuSlider("CoG size")
        self.ui.sliderCoGSize.setMin(0)
        self.ui.sliderCoGSize.slider.setValue(20.0)

        def set_cog_size(value):
            if value < 1:
                self.visual.show_cog = False
                self.run_code(
                    f"self.visual.settings.cog_scale = 0",
                    guiEventType.VIEWER_SETTINGS_UPDATE,
                )
                self.visual.refresh_embeded_view()
            else:
                self.visual.show_cog = True
                self.run_code(
                    f"self.visual.settings.cog_scale = {value ** (1.3) / 100}",
                    guiEventType.VIEWER_SETTINGS_UPDATE,
                )

        self.ui.sliderCoGSize.connectvalueChanged(set_cog_size)
        self.ui.menuView.addAction(self.ui.sliderCoGSize)

        self.ui.action2D_mode.triggered.connect(self.toggle_2D)
        self.ui.actionX.triggered.connect(lambda: self.camera_set_direction((1, 0, 0)))
        self.ui.action_x.triggered.connect(
            lambda: self.camera_set_direction((-1, 0, 0))
        )
        self.ui.actionY.triggered.connect(lambda: self.camera_set_direction((0, 1, 0)))
        self.ui.action_Y.triggered.connect(
            lambda: self.camera_set_direction((0, -1, 0))
        )
        self.ui.actionZ.triggered.connect(lambda: self.camera_set_direction((0, 0, -1)))
        self.ui.action_Z.triggered.connect(lambda: self.camera_set_direction((0, 0, 1)))
        self.ui.actionCamera_reset.triggered.connect(self.camera_reset)
        #

        self.ui.pbTop.clicked.connect(self.visual.Style.SetViewZ)
        self.ui.pbFront.clicked.connect(self.visual.Style.SetViewY)
        self.ui.pbSide.clicked.connect(self.visual.Style.SetViewX)
        self.ui.pb3D.clicked.connect(self.toggle_2D)

        # the python console
        self.ui.dockWidget_2.setVisible(False)

        self.ui.actionPython_console_2.triggered.connect(self.show_python_console)




        self.ui.actionVersion.setText(f"Version {DAVE.__version__}")
        self.ui.actionOnline_help.triggered.connect(
            lambda: subprocess.Popen("explorer https://davedocs.online")
        )

        # ======================= Code-highlighter ==============

        font = QFont()
        font.setPointSize(10)
        font.setFamily("Consolas")
        self.ui.teCode.setFont(font)
        self.ui.teCode.setTabStopDistance(
            QFontMetricsF(self.ui.teCode.font()).width(" ") * 4
        )

        self.highlight = PythonHighlighter(self.ui.teCode.document())

        self.teCode_eventFilter = ShiftEnterKeyPressFilter()
        self.teCode_eventFilter.callback = self.run_code_in_teCode
        self.ui.teCode.installEventFilter(self.teCode_eventFilter)

        # self.delete_eventFilter = DeleteEventFilter()
        # self.delete_eventFilter.callback = self.delete_key
        # self.MainWindow.installEventFilter(self.delete_eventFilter)

        # ======================== Docks ====================
        self.guiWidgets = dict()
        """Dictionary of all created guiWidgets (dock-widgets)"""

        # def set_pb_style(pb):
        #     pb.setFlat(True)
        #     pb.setCheckable(True)
        #     pb.setAutoExclusive(True)
        #     pb.setStyleSheet("text-decoration: underline;")
        #     self.ui.toolBar.addWidget(pb)

        # Workspace buttons
        btnConstruct = QtWidgets.QPushButton()
        btnConstruct.setText("&0. Library")
        btnConstruct.clicked.connect(self.import_browser)
        btnConstruct.setFlat(True)
        self.ui.toolBar.addWidget(btnConstruct)

        for i, button in enumerate(DAVE_GUI_WORKSPACE_BUTTONS):
            name = button[0]
            workspace_id = button[1]

            btn = QtWidgets.QPushButton()
            if i<9:
                btn.setText(f'&{i+1} {name}')
            else:
                btn.setText(f'{i + 1} {name}')
            btn.pressed.connect(lambda *args, wsid=workspace_id : self.activate_workspace(wsid))

            # btn.setFlat(True)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            # btn.setStyleSheet("text-decoration: underline;")
            self.ui.toolBar.addWidget(btn)
            self.ui.toolBar.setMinimumHeight(btn.minimumSizeHint().height())

        # self.ui.toolBar.layout().setContentsMargins(-2, 0, 0, 0)
        self.ui.toolBar.setStyleSheet("QToolBar{spacing:0px;}")
        # self.ui.toolBar

        space = QtWidgets.QWidget()
        space.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self.ui.toolBar.addWidget(space)

        self._active_workspace = None

        # call plugin(s)

        for plugin_init in DAVE_GUI_PLUGINS_INIT:
            plugin_init(self)

        # ---------- activate workspace (if any)

        if workspace is None:
            self.activate_workspace("CONSTRUCT")
        else:
            self.activate_workspace(workspace)

        # ========== undo log =======

        self._undo_log = []
        self._undo_index = 0

        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)

        # ======================== Finalize ========================
        splash.finish(self.MainWindow)
        self.MainWindow.show()

        self.MainWindow.setMinimumWidth(1400)

        if block:
            self.ui.pbUpdate.setVisible(False)
            self.ui.pbCopyViewCode.setVisible(False)
            self.app.exec_()

    def show_python_console(self, *args):
        self.ui.dockWidget_2.show()

    def new_scene(self):
        self.scene.clear()
        self.guiEmitEvent(guiEventType.FULL_UPDATE)

    def show_settings(self):
        dlg = SettingsDialog(scene=self.scene, gui=self)
        result = dlg.exec_()
        if result > 0:

            text = dlg.plainTextEdit.toPlainText()
            paths = text.split('\n')

            self.additional_user_resource_paths.clear()
            for p in paths:
                if p:
                    self.additional_user_resource_paths.append(Path(p))
                settings = QSettings("rdbr", "DAVE")
                paths_str = ';'.join([str(p) for p in self.additional_user_resource_paths])
                settings.setValue(f"additional_paths", paths_str)

    def update_resources_paths(self):
        """Updates the global settings.DAVE_RESOURCES_PATHS to include the user-defined dirs

        Note: removing paths required a program restart
        """

        for p in self.additional_user_resource_paths:
            if p not in DAVE.settings.RESOURCE_PATH:
                DAVE.settings.RESOURCE_PATH.append(p)

    def labels_show_hide(self):
        if self.visual.settings.label_scale > 0:
            self.visual.settings.label_scale = 0
        else:
            self.visual.settings.label_scale = 1.0
        self.ui.actionShow_labels.setChecked(self.visual.settings.label_scale > 0)
        self.visual.update_visibility()
        self.visual.refresh_embeded_view()

    def toggle_2D(self):
        flat = self.visual.toggle_2D()
        self.ui.pb3D.setChecked(flat)
        self.ui.action2D_mode.setChecked(flat)
        self.visual.refresh_embeded_view()

    def refresh_model(self):
        """Full model refresh to reload components"""
        code = self.scene.give_python_code()
        self.scene.clear()
        self.scene.run_code(code)
        self.guiEmitEvent(guiEventType.FULL_UPDATE)

    def delete_key(self):
        """Delete key pressed in either main-form or viewport"""

        names = [node.name for node in self.selected_nodes]

        need_refresh = False
        for name in names:

            # does the node still exist?
            if self.scene.node_exists(name):
                need_refresh = True
                self.run_code(
                    f"s.delete('{name}')", event=None
                )  # send event once after all nodes have been deleted

        if need_refresh:
            self.guiEmitEvent(guiEventType.MODEL_STRUCTURE_CHANGED)
            self.select_none()

    def change_paintset(self):
        """Updates the paintset of the viewport to the value of cbPainterSelect"""

        with DelayRenderingTillDone(self.visual):

            # Clear selection to make sure that the paint is updated for all actors
            selected_node_names = [node.name for node in self.selected_nodes]
            self.select_none()

            current_set = self.ui.cbPainerSelect.currentText()
            self.visual.settings.painter_settings = PAINTERS[current_set]
            self.visual.update_visibility()

            # and restore the selection afterwards
            if selected_node_names:
                self.guiSelectNode(selected_node_names[0])

    def activate_paintset(self, name):
        """Sets the current text of the combobox to the given paint-set name. This triggers activation
        of the new paint set.

        This action is not executed if the currently active paint-set name contains "custom"
        """

        cb = self.ui.cbPainerSelect  # alias

        if "custom" not in cb.currentText():  # do not change if set to custom
            items = [cb.itemText(i) for i in range(cb.count())]
            if name in items:
                self.ui.cbPainerSelect.setCurrentText(
                    name
                )  # this triggers the change_paintset event
            else:
                print(items)
                raise ValueError(
                    f"No paint-set with name {name}. Available names are printed above"
                )

    def copy_screenshot_code(self):

        sea = self.visual.settings.show_global
        camera_pos = self.visual.screen.camera.GetPosition()
        lookat = self.visual.screen.camera.GetFocalPoint()

        code = f"show(s, camera_pos = ({camera_pos[0]:.3},{camera_pos[1]:.3},{camera_pos[2]:.3}), "

        if self.visual.screen.camera.GetParallelProjection():
            code += f"\n     projection = '2d',"
            code += f"\n     scale = {self.visual.screen.camera.GetParallelScale()},"

            direction = np.array(lookat) - np.array(camera_pos)
            norm = np.linalg.norm(direction)
            if norm > 1e-9:
                direction = direction / norm
            direction = np.round(direction, 2)
            t = 0.98

            if direction[0] > t:
                lookat = "x"
            elif direction[1] > t:
                lookat = "y"
            elif direction[2] > t:
                lookat = "z"
            if direction[0] < -t:
                lookat = "-x"
            elif direction[1] < -t:
                lookat = "-y"
            elif direction[2] < -t:
                lookat = "-z"

        if isinstance(lookat, str):
            code += f"\n     lookat = '{lookat}',"
        else:
            code += f"\n     lookat = ({lookat[0]:.3},{lookat[1]:.3},{lookat[2]:.3}),"

        settings = self.visual.settings  # alias
        defaults = DAVE.settings_visuals.ViewportSettings()

        for key, value in settings.__dict__.items():
            if key == "painter_settings":
                continue

            if value != getattr(defaults, key):
                code += f"\n     {key} = {value},"

        code += f"\n     painters = '{self.ui.cbPainerSelect.currentText()}',"
        code += f"\n     zoom_fit = False)"

        print(code)
        self.app.clipboard().setText(code)

    def escPressed(self):
        self.animation_terminate()  # terminate any running animations
        self.select_none()

    def select_none(self):
        if self.selected_nodes:
            self.selected_nodes.clear()
            if "Properties" in self.guiWidgets:
                if self.guiWidgets["Properties"].node_picker is None:
                    self.guiWidgets["Properties"].setVisible(False)
            self.guiEmitEvent(guiEventType.SELECTION_CHANGED)

    def focus_on_selected_object(self):
        """Moves the viewport view to the selected object"""

        if self.selected_nodes:
            node = self.selected_nodes[0]
            visual = self.visual.actor_from_node(node)

            if visual is not None:
                position = visual.center_position
                print(f"focusing camera to {node.name} at {position}")
                self.visual.focus_on(position)

                self.refresh_3dview()

    def savepoint_restore(self):

        if self.scene._savepoint is not None:
            self.animation_terminate(keep_current_dofs=True)

        if self.scene.savepoint_restore():
            self.select_none()
            self.guiEmitEvent(guiEventType.MODEL_STRUCTURE_CHANGED)

    def close_all_open_docks(self):
        for g in self.guiWidgets.values():
            g.close()


    def activate_workspace(self, name):

        self._active_workspace = name

        self.animation_terminate()
        self.savepoint_restore()

        #
        # self.visual.set_alpha(1.0)
        # self.visual.hide_actors_of_type([ActorType.BALLASTTANK])
        # self.visual.update_outlines()
        self.activate_paintset("Construction")

        if name == "PAINTERS":
            self.show_guiWidget("vanGogh", WidgetPainters)

        if name == "CONSTRUCT":
            self.close_all_open_docks()
            self.show_guiWidget("Node Tree", WidgetNodeTree)
            # self.show_guiWidget("Derived Properties", WidgetDerivedProperties)
            self.show_guiWidget("Properties", WidgetNodeProps)
            self.show_guiWidget("Quick actions", WidgetQuickActions)

        if name == "EXPLORE":
            self.close_all_open_docks()
            self.show_guiWidget("Derived Properties", WidgetDerivedProperties)
            self.show_guiWidget("Explore 1-to-1", WidgetExplore)

        if name == "DYNAMICS":
            self.close_all_open_docks()
            self.show_guiWidget("Properties - dynamic", WidgetDynamicProperties)
            self.show_guiWidget("Mode-shapes", WidgetModeShapes)

        if name == "BALLAST":
            self.close_all_open_docks()
            self.show_guiWidget("Ballast system", WidgetBallastSystemSelect)
            self.show_guiWidget("Tanks", WidgetBallastConfiguration)
            self.show_guiWidget("Solver", WidgetBallastSolver)
            self.show_guiWidget("Tank order", WidgetTankOrder)
            if self.visual.settings.label_scale == 0:
                self.labels_show_hide()
            self.activate_paintset("Ballast")

            # self.visual.show_actors_of_type([ActorType.BALLASTTANK])

        if name == "ENVIRONMENT":
            self.show_guiWidget("Environment", WidgetEnvironment)

        if name == "STABILITY":
            self.close_all_open_docks()
            self.show_guiWidget("Stability", WidgetDisplacedStability)

        if name == "LIMITS":
            self.close_all_open_docks()
            self.show_guiWidget("Limits and UCs", WidgetLimits)
            if not self.visual.settings.paint_uc:
                self.toggle_show_UC()

        if name == "TAGS":
            self.show_guiWidget("Tags", WidgetTags)

        if name == "MOMENTS":
            self.close_all_open_docks()
            self.show_guiWidget("Footprints", WidgetFootprints)
            self.show_guiWidget("Graph", WidgetBendingMoment)
            self.activate_paintset("Footprints")

        if name == "AIRY":
            self.scene.savepoint_make()
            self.close_all_open_docks()
            code = "from DAVE.frequency_domain import prepare_for_fd\nprepare_for_fd(s)"
            self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)
            self.show_guiWidget("Airy waves", WidgetAiry)

        for plugin in self.plugins_workspace:
            plugin(self, name)

        self.visual.update_visibility()

    def import_browser(self):

        G = DAVE.gui.standard_assets.Gui()
        r = G.showModal()

        if r is not None:
            file = r[0]
            container = r[1]
            prefix = r[2]
            code = 's.import_scene("{}", containerize={}, prefix="{}")'.format(
                file, container, prefix
            )
            self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

            self.activate_workspace("CONSTRUCT")

    # ============== File open / recent / drag-drop functions ===========

    def drag_enter(self, event):
        if event.mimeData().hasText():
            event.accept()

    def drop(self, event):
        filename = event.mimeData().text()

        from pathlib import Path
        from urllib.parse import urlparse

        filename = urlparse(filename)[2]
        filename = filename[1:]
        p = Path(filename)

        if p.exists():
            try:
                self.open_file(p)
            except:
                raise ValueError(f"Could not open file {filename}")
        else:
            raise ValueError(f"Could not open file {filename}")

    def get_recent(self):
        settings = QSettings("rdbr", "DAVE")
        files = []
        for i in range(8):
            files.append(settings.value(f"recent{i}", ""))
        return files

    def add_to_recent_file_menu(self, filename):
        settings = QSettings("rdbr", "DAVE")

        files = self.get_recent()

        if filename in files:
            files.remove(filename)

        files = [filename, *files]
        for i in range(8):
            files.append(settings.setValue(f"recent{i}", files[i]))

        self.update_recent_file_menu()

    def update_recent_file_menu(self):
        files = self.get_recent()
        for i in range(8):
            if files[i]:
                self.recent_files[i].setText(f"&{i+1} " + str(files[i]))
            else:
                self.recent_files[i].setText("recent files will appear here")

    def open_recent(self, i):
        filename = self.recent_files[i].text()
        if filename == "recent files will appear here":
            return
        filename = filename[3:]

        self.open_file(filename)

    # ============== Animation functions =============

    def animation_running(self):
        """Returns true is an animation is running"""
        return self._timerid is not None

    def timerEvent(self, a, b):

        if self._timerid is None:  # timer is going to be destroyed
            return

        t = (
            time.time() - self._animation_start_time
        )  # time since start of animation in [s]

        t *= self._animation_speed

        if self._animation_loop:
            t = np.mod(t, self._animation_length)
        else:
            if t > self._animation_length:
                self.animation_terminate()
                return

        self.animation_activate_time(t)

        self.ui.aniSlider.setValue(t * 1000)

    def animation_speed_change(self):
        self._animation_speed = self.ui.sbPlaybackspeed.value()

    def animation_activate_time(self, t):
        dofs = self._animation_keyframe_interpolation_object(t)
        self.scene._vfc.set_dofs(dofs)
        self.visual.update_dynamic_waveplane(t)
        self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)

    def animation_terminate(self, keep_current_dofs=False):

        # if not self.animation_running():
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

    def animation_start(
        self,
        t,
        dofs,
        is_loop,
        final_dofs=None,
        do_not_reset_time=False,
        show_animation_bar=True,
    ):
        """Start an new animation

        Args:
            t:    List of times at keyframes
            dofs: List of dofs at keyframes
            is_loop: Should animation be played in a loop (bool)
            final_dofs : [optional] DOFS to be set when animation is finished or terminated. Defaults to last keyframe
            do_not_reset_time : do not reset the time when starting the animation, this means the loop continues where it was.


        """
        self.animation_terminate(keep_current_dofs=True)  # end old animation, if any

        if len(dofs) != len(t):
            raise ValueError("dofs and t should have the same length (list or tuple)")

        self._animation_length = np.max(t)
        self._animation_keyframe_interpolation_object = scipy.interpolate.interp1d(
            t, dofs, axis=0
        )
        self._animation_loop = is_loop

        if final_dofs is None:
            final_dofs = dofs[-1]

        self._animation_final_dofs = final_dofs
        if not do_not_reset_time:
            self._animation_start_time = time.time()

        self.visual.quick_updates_only = True

        self.ui.aniSlider.setMaximum(1000 * self._animation_length)
        self.ui.frameAni.setVisible(show_animation_bar)

        self._animation_available = True

        if not show_animation_bar:  # override pause for short animations
            self.ui.btnPauseAnimation.setChecked(False)
            self._animation_paused = False

        if not self._animation_paused:

            iren = self.visual.renwin.GetInteractor()
            if self._timerid is None:
                self._timerid = iren.CreateRepeatingTimer(
                    round(1000 / DAVE.settings.GUI_ANIMATION_FPS)
                )

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
                self._timerid = iren.CreateRepeatingTimer(
                    round(1000 / DAVE.settings.GUI_ANIMATION_FPS)
                )

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

        with DelayRenderingTillDone(self.visual):
            remember = self.visual.quick_updates_only
            self.visual.quick_updates_only = False
            self.animation_activate_time(t)
            self.visual.quick_updates_only = remember

    # =================================================== end of animation functions ==================

    # ==== undo functions ====

    def undo(self):
        self._undo_index -= 1
        if self._undo_index < 0:
            QMessageBox.information(
                self.ui.widget, "Undo", "Can not undo any further", QMessageBox.Ok
            )

            self._undo_index = 0
            return

        if self._undo_index == len(self._undo_log) - 1:
            # Make an undo point for the current state
            self._undo_log.append((UndoType.CLEAR_AND_RUN_CODE, self.scene.give_python_code()))

        self.activate_undo_index(self._undo_index)

    def redo(self):
        self._undo_index += 1
        if self._undo_index > len(self._undo_log) - 1:
            QMessageBox.information(
                self.ui.widget, "Redo", "Can not redo any further", QMessageBox.Ok
            )
            self._undo_index = len(self._undo_log) - 1
            return

        self.activate_undo_index(self._undo_index)

    def activate_undo_index(self, index):

        print(f"Activating undo index {index} of {len(self._undo_log)-1}")

        undo_type, undo_contents = self._undo_log[index]  # unpack

        if undo_type == UndoType.CLEAR_AND_RUN_CODE or undo_type == UndoType.RUN_CODE:

            # capture selected node names before deleting the scene
            selected_names = [node.name for node in self.selected_nodes]

            if undo_type == UndoType.CLEAR_AND_RUN_CODE:
                self.scene.clear()

            self.scene.run_code(undo_contents)

            try:
                nodes = [
                    self.scene[node] for node in selected_names
                ]  # selected nodes may not exist anymore
            except:
                nodes = []

            self.selected_nodes.clear()  # do not re-assign, docks keep a reference to this list
            self.selected_nodes.extend(nodes)

            self.guiEmitEvent(guiEventType.FULL_UPDATE)
            self.give_feedback(f"Activating undo index {index} of {len(self._undo_log)-1}")

        elif undo_type == UndoType.SET_DOFS:
            if undo_contents is not None:
                self.scene._vfc.set_dofs(undo_contents) # UNDO SOLVE STATICS"
                self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)
                self.give_feedback(f"Activating undo index {index} of {len(self._undo_log)} - Solve-statics reverted")


    def add_undo_point(self, undo_type = UndoType.CLEAR_AND_RUN_CODE, code = ''):

        logging.info(f"Creating undo point with type {undo_type}")

        if undo_type == UndoType.CLEAR_AND_RUN_CODE:

            """Adds the current model to the undo-list"""
            if len(self._undo_log) > self._undo_index:
                self._undo_log = self._undo_log[: self._undo_index]
            self._undo_log.append((UndoType.CLEAR_AND_RUN_CODE, self.scene.give_python_code()))

        elif undo_type == UndoType.RUN_CODE:
            self._undo_log.append((UndoType.RUN_CODE, code))

        elif undo_type == UndoType.SET_DOFS:
            self._undo_log.append((UndoType.SET_DOFS, self.scene._vfc.get_dofs()))

        else:
            raise Exception('Unsupported undo type')

        self._undo_index = len(self._undo_log)
        logging.info(f"current log index = number of points = {self._undo_index}")

    # / undo functions

    def closeEvent(self, event):
        """This is the on-close for the main window"""
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def onCloseApplication(self):
        """This is the on-close for the Application"""

        self.visual.shutdown_qt()
        print(
            "-- closing the gui : these were the actions you performed while the gui was open --"
        )
        print(self.give_clean_history())


    def measured_in_viewport(self, distance):
        self.give_feedback(f'View-plane distance = {distance:.3f}m\n (does not measure depth)')

    def show_exception(self, e):
        self.give_feedback(e, style=1)

    def give_feedback(self, what, style = 0):
        self.ui.teFeedback.setText(str(what))
        if style == 0:
            self.ui.teFeedback.setStyleSheet("background-color: white;")
        elif style == 1:
            self.ui.teFeedback.setStyleSheet("background-color: pink;")

        self.statusbar.showMessage(str(what))

        if not self.ui.dockWidget_2.isVisible() and style==1:

            tool_long = len(what) > 1000 or len(what.split('\n')) > 30

            short = what[-1000:]
            short = '\n'.join(short.split('\n')[-30:])

            if tool_long:
                print(what)
                QMessageBox.warning(self.ui.widget, "error", short + '\n\n !!! first part omitted,\n see (python) console for full error message', QMessageBox.Ok)
            else:
                QMessageBox.warning(self.ui.widget, "error", what, QMessageBox.Ok)


    def run_code(self, code, event, store_undo=True, sender=None):
        """Runs the provided code

        If successful, add code to history and create an undo point
        If not, set code as current code

        Args:
            - event : the event to send after running the code
            - store_undo : store undo information AFTER running code

        """

        start_time = datetime.datetime.now()
        self._model_has_changed = True

        before = self.scene._nodes.copy()

        s = self.scene

        self.ui.pbExecute.setStyleSheet("background-color: yellow;")
        if not self.ui.teCode.hasFocus():
            self.ui.teCode.setPlainText(
                code
            )  # do not replace if we are currently editing

        self.app.processEvents()

        if store_undo:
            self.add_undo_point()

        self.ui.teFeedback.setStyleSheet("")
        self.ui.teFeedback.clear()

        select_node_name_edit_field = False

        with capture_output() as c:

            try:

                glob_vars = globals()
                glob_vars.update(DAVE.settings.DAVE_ADDITIONAL_RUNTIME_MODULES)
                glob_vars["s"] = self.scene
                glob_vars["self"] = self

                exec(code, glob_vars)

                if c.stdout:
                    self.give_feedback(c.stdout, style=0)
                else:
                    self.give_feedback(code, style=0)

                self._codelog.append(code)
                self.ui.teHistory.append(code)
                self.tidy_history()

                self.ui.teHistory.verticalScrollBar().setValue(
                    self.ui.teHistory.verticalScrollBar().maximum()
                )  # scroll down all the way

                # See if selected nodes are still valid and identical to the ones
                to_be_removed = []
                for node in self.selected_nodes:
                    if node not in self.scene._nodes:
                        to_be_removed.append(node)

                for node in to_be_removed:
                    self.selected_nodes.remove(node)

                # if we created something new, then select it (or its manager)
                emitted = False
                for node in self.scene._nodes:
                    if node not in before:

                        logging.info(f"New node detected: {node.name}")

                        self.selected_nodes.clear()

                        if node.manager is not None:
                            self.guiSelectNode(node.manager)
                            select_node_name_edit_field = True
                        else:
                            self.guiSelectNode(node)
                            select_node_name_edit_field = True

                        emitted = True
                        break

                if event is not None:
                    self.guiEmitEvent(event, sender=sender)

                if to_be_removed and not emitted:
                    self.guiEmitEvent(guiEventType.SELECTED_NODE_MODIFIED, sender=sender)

            except Exception as E:

                self.ui.teCode.clear()
                self.ui.teCode.append(code)

                self.ui.teCode.update()
                self.ui.teCode.repaint()

                message = c.stdout + "\n" + str(E) + "\n\nWhen running: \n\n" + code
                self.show_exception(message)

                raise (E)

            self.ui.pbExecute.setStyleSheet("")
            self.ui.pbExecute.update()

            self.ui.teFeedback.verticalScrollBar().setValue(
                self.ui.teFeedback.verticalScrollBar().maximum()
            )  # scroll down all the way

            if select_node_name_edit_field:
                self.place_input_focus_on_name_of_node()

    def place_input_focus_on_name_of_node(self):
        """Places the input focus on the name of the node such that the user can directly change it if needed"""
        if 'Properties' in self.guiWidgets:
            props = self.guiWidgets['Properties']
            props._node_name_editor.ui.tbName.setFocus()
            props._node_name_editor.ui.tbName.selectAll()


    def stop_solving(self):
        self._terminate = True

    def solve_statics(self, timeout_s=0.5, called_by_user=True):

        self.scene.solve_activity_desc = "Solving static equilibrium"

        self.solve_statics_using_gui_on_scene(
            scene_to_solve=self.scene,
            timeout_s=timeout_s,
            called_by_user=called_by_user,
        )

        self.give_feedback(f"Solved statics - remaining error = {self.scene._vfc.Emaxabs} kN or kNm")

    def solve_statics_using_gui_on_scene(
        self, scene_to_solve, timeout_s=0.5, called_by_user=True
    ):
        scene_to_solve.update()

        if called_by_user:
            self.add_undo_point(undo_type=UndoType.SET_DOFS)

        old_dofs = scene_to_solve._vfc.get_dofs()

        if len(old_dofs) == 0:  # no degrees of freedom
            if called_by_user:
                msgBox = QMessageBox()
                msgBox.setText("No degrees of freedom - nothing to solve")
                msgBox.setWindowTitle("DAVE")
                msgBox.exec_()

                print("No dofs")

            return True

        self._dialog = None

        # define the terminate control
        self._terminate = False

        def should_we_stop():
            return self._terminate

        # define the feedback control
        self._feedbackcounter = 0

        def feedback(message):

            self._feedbackcounter += 1  # skip the first
            if self._feedbackcounter < 2:
                return

            if self._dialog is None:
                self._dialog = SolverDialog()
                self._dialog.btnTerminate.clicked.connect(self.stop_solving)
                self._dialog.label.setText(self.scene.solve_activity_desc)
                self._dialog.show()

            self._dialog.label_2.setText(message)

            self._dialog.update()

            self.visual.position_visuals()
            self.visual.refresh_embeded_view()
            self.app.processEvents()

        # execute the solver
        result = scene_to_solve._solve_statics_with_optional_control(
            feedback_func=feedback,
            do_terminate_func=should_we_stop,
            timeout_s=timeout_s,
        )

        # close the dialog.
        # if this was a short solve,
        if self._dialog is not None:
            self._dialog.close()

        else:  # animate the change
            if DAVE.settings.GUI_DO_ANIMATE and called_by_user:
                new_dofs = scene_to_solve._vfc.get_dofs()
                self.animate_change(old_dofs, new_dofs, 10)

        if called_by_user:
            self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)
            self._codelog.append("s.solve_statics()")

        return result

    def animate_change(self, old_dof, new_dof, n_steps):
        """Animates from old_dof to new_dofs in n_steps"""

        if len(old_dof) != len(new_dof):
            return

        dt = DAVE.settings.GUI_SOLVER_ANIMATION_DURATION / n_steps

        t = []
        dofs = []

        old_dof = np.array(old_dof)
        new_dof = np.array(new_dof)

        for i in range(n_steps + 1):

            factor = i / n_steps
            old = 0.5 + 0.5 * np.cos(3.14159 * factor)

            t.append(dt * i)
            dofs.append((1 - old) * new_dof + old * old_dof)

        self.animation_start(t, dofs, is_loop=False, show_animation_bar=False)

    def to_blender(self):

        from DAVE.io.blender import create_blend_and_open

        if self.animation_running():
            dofs = []

            n_frames = np.round(self._animation_length * DAVE.settings.BLENDER_FPS)
            for t in np.linspace(0, self._animation_length, int(n_frames)):
                dofs.append(self._animation_keyframe_interpolation_object(t))

        else:
            dofs = None

        create_blend_and_open(
            self.scene, animation_dofs=dofs, wavefield=self.visual._wavefield
        )

    def toggle_show_global(self):
        # TODO: fix
        self.ui.actionShow_water_plane.setChecked(
            not self.ui.actionShow_water_plane.isChecked()
        )
        self.toggle_show_global_from_menu()

    def toggle_show_UC(self):
        self.visual.settings.paint_uc = not self.visual.settings.paint_uc

        self.ui.pbUC.setChecked(self.visual.settings.paint_uc)
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def toggle_show_global_from_menu(self):
        self.visual.settings.show_global = self.ui.actionShow_water_plane.isChecked()
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def toggle_show_force_applying_elements(self):
        self.visual.show_meshes = self.ui.actionShow_force_applying_element.isChecked()
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def camera_set_direction(self, vector):
        self.visual.Style.SetCameraPlaneDirection(vector)
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def camera_reset(self):
        self.visual.zoom_all() # this function takes care of ignoring the sea-plane
        # self.visual.Style.ZoomFit()
        # self.visual.refresh_embeded_view()

    def toggle_SSAO(self):
        if self.ui.btnSSAO.isChecked():
            self.visual.EnableSSAO()
        else:
            self.visual.DisableSSAO()
        self.visual.refresh_embeded_view()


    def clear(self):
        self.run_code("s.clear()", guiEventType.FULL_UPDATE)
        self._model_has_changed = False
        self.modelfilename = None
        self.MainWindow.setWindowTitle(f'DAVE [unnamed scene]')
        self.ui.actionSave.setEnabled(False)

    def open_file(self, filename):
        code = 's.clear()\ns.load_scene(r"{}")'.format(filename)
        self.run_code(code, guiEventType.FULL_UPDATE)
        self.modelfilename = filename

        self._model_has_changed = False
        self.MainWindow.setWindowTitle(f'DAVE [{self.modelfilename}]')
        self.ui.actionSave.setEnabled(True)
        self.add_to_recent_file_menu(filename)
        self.visual.zoom_all()

    def _get_filename_using_dialog(self):
        if self.modelfilename is None:
            folder = self.scene.resources_paths[-2]  # get the lowest one
            filename, _ = QFileDialog.getOpenFileName(
                filter="*.dave", caption="Assets", dir=str(folder)
            )
        else:
            filename, _ = QFileDialog.getOpenFileName(filter="*.dave", caption="Assets")
        return filename

    def open(self):
        filename = self._get_filename_using_dialog()
        if filename:
            self.open_file(filename)

    def menu_import(self):
        filename = self._get_filename_using_dialog()

        if filename:
            code = 's.import_scene(r"{}")'.format(filename)
            self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)
            self.visual.update_visibility()

    def menu_save_model(self):
        code = 's.save_scene(r"{}")'.format(self.modelfilename)
        self.run_code(code, guiEventType.NOTHING)
        self._model_has_changed = False

    def menu_save_model_as(self):

        if self.modelfilename is not None:
            dir = str(Path(self.modelfilename).parent)
        else:
            dir = str(self.scene.resources_paths[-2])  # most typical work-path

        filename, _ = QFileDialog.getSaveFileName(
            filter="*.dave",
            caption="Scene files",
            dir=dir,
        )
        if filename:
            code = 's.save_scene(r"{}")'.format(filename)
            self.run_code(code, guiEventType.NOTHING)

            self._model_has_changed = False
            self.modelfilename = filename
            self.MainWindow.setWindowTitle(f'DAVE [{self.modelfilename}]')

            self.ui.actionSave.setEnabled(True)
            self.add_to_recent_file_menu(filename)

    def maybeSave(self):
        if not self._model_has_changed:
            return True

        ret = QMessageBox.question(self.MainWindow, "Message",
                "<h4><p>The scene has unsaved changes.</p>\n" 
                "<p>Do you want to save changes?</p></h4>",
                QMessageBox.Yes | QMessageBox.Discard | QMessageBox.Cancel)

        if ret == QMessageBox.Yes:
            if self.modelfilename is None:
                self.menu_save_model_as()
                return False
            else:
                self.menu_save_model()
                return True

        if ret == QMessageBox.Cancel:
            return False

        return True

    def menu_export_orcaflex_yml(self):
        filename, _ = QFileDialog.getSaveFileName(
            filter="*.yml",
            caption="Orcaflex .yml file",
            directory=self.scene.resources_paths[0],
        )
        if filename:
            code = 'from DAVE.io.orcaflex import export_ofx_yml\nexport_ofx_yml(s,r"{}")'.format(
                filename
            )
            self.run_code(code, guiEventType.NOTHING)

    def menu_export_orcaflex_package(self):
        filename, _ = QFileDialog.getSaveFileName(
            filter="*.py",
            caption="Python files",
            directory=self.scene.resources_paths[0],
        )
        if filename:
            python_file = filename
            ofx_file = python_file + ".yml"
            code = 'from DAVE.io.orcaflex import export_ofx_yml, write_ofx_run_and_collect_script\nexport_ofx_yml(s,r"{}")'.format(
                ofx_file
            )
            code += '\nwrite_ofx_run_and_collect_script(r"{}", r"{}")'.format(
                python_file, ofx_file
            )
            self.run_code(code, guiEventType.NOTHING)

    def tidy_history(self):
        self.ui.teHistory.setText(self.give_clean_history())

    def give_clean_history(self):
        prev_line = ""

        f = []
        for s in self._codelog:

            # filter repeated assignments to same target
            if s.split("=")[0] == prev_line.split("=")[0]:
                prev_line = s
                continue

            f.append(prev_line)
            prev_line = s

        f.append(prev_line)

        return "\n".join(f)

    def menu_save_actions(self):
        filename, _ = QFileDialog.getSaveFileName(
            filter="*.dave",
            caption="Scene files",
            directory=self.scene.resources_paths[0],
        )
        if filename:

            prev_line = ""

            f = open(filename, "w+")
            for s in self._codelog:

                # filter repeated assignments to same target
                if s.split("=")[0] == prev_line.split("=")[0]:
                    prev_line = s
                    continue

                f.write(prev_line + "\n")
                prev_line = s

            f.write(prev_line + "\n")
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
        self.run_code(code, guiEventType.FULL_UPDATE)

    def rightClickViewport(self, point):
        globLoc = self.ui.frame3d.mapToGlobal(point)
        name = None
        try:
            name = self.selected_nodes[0].name
        except:
            pass

        self.openContextMenyAt(name, globLoc)

    def selected_nodes_of_instance(self, req_class):
        """Returns a list of nodes that are selected and are an instance of the requested class"""
        return [node for node in self.selected_nodes if isinstance(node, req_class)]

    def openContextMenyAt(self, node_name, globLoc):
        menu = QtWidgets.QMenu()

        if node_name is not None:

            node = self.scene[node_name]

            if node._manager is None:

                def edit():
                    self.selected_nodes.clear()
                    self.guiSelectNode(node_name)
                    self.show_guiWidget(
                        "Properties", WidgetNodeProps
                    )  # people often close this one

                menu.addAction("Edit {}".format(node_name), edit)

                showhide = menu.addAction("Visible")
                showhide.setCheckable(True)

                showhide.setChecked(node.visible)

                if node.visible:
                    showhide.triggered.connect(
                        lambda: self.run_code(
                            f"s['{node_name}'].visible = False",
                            guiEventType.VIEWER_SETTINGS_UPDATE,
                        )
                    )
                else:
                    showhide.triggered.connect(
                        lambda: self.run_code(
                            f"s['{node_name}'].visible = True",
                            guiEventType.VIEWER_SETTINGS_UPDATE,
                        )
                    )

                def delete():
                    self.run_code(
                        's.delete("{}")'.format(node_name),
                        guiEventType.MODEL_STRUCTURE_CHANGED,
                    )

                def dissolve():
                    self.run_code(
                        's.dissolve("{}")'.format(node_name),
                        guiEventType.MODEL_STRUCTURE_CHANGED,
                    )

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
                    code = f"s.duplicate_node('{node_name}')"
                    self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

                def duplicate_branch():
                    code = f"s.duplicate_branch('{node_name}')"
                    self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

                    # self.guiSelectNode(name_of_duplicate)

                if isinstance(node, (Frame, Point)):
                    if self.scene.nodes_with_parent(node):
                        menu.addAction("Duplicate", duplicate_branch)

                if isinstance(node, Cable):
                    menu.addAction("Convert Cable --> Sling", lambda *args: self.run_code(f"s.to_sling(s['{node.name}'])", guiEventType.MODEL_STRUCTURE_CHANGED))

                if isinstance(node, Sling):
                    menu.addAction("Convert Sling --> Cable", lambda *args: self.run_code(f"s.to_cable(s['{node.name}'])", guiEventType.MODEL_STRUCTURE_CHANGED))

                if type(node) == RigidBody:
                    menu.addAction("Downgrade Body --> Frame", lambda *args: self.run_code(f"s.to_frame(s['{node.name}'])", guiEventType.MODEL_STRUCTURE_CHANGED))

                if type(node) == Frame:
                    menu.addAction("Upgrade Frame --> Body", lambda *args: self.run_code(f"s.to_rigidbody(s['{node.name}'])", guiEventType.MODEL_STRUCTURE_CHANGED))


                menu.addAction("Duplicate node", duplicate)

                menu.addSeparator()
                menu.addSeparator()

        wa = QtWidgets.QWidgetAction(None)

        ui = Ui_MenuNodes()
        widget = QtWidgets.QWidget()
        ui.setupUi(widget)
        wa.setDefaultWidget(widget)

        ui.pbPoint.clicked.connect(self.new_point)
        ui.pbCircle.clicked.connect(self.new_circle)
        ui.pbAxis.clicked.connect(self.new_frame)
        ui.pbBody.clicked.connect(self.new_body)
        ui.pbGeometricContact.clicked.connect(self.new_geometric_contact)

        ui.pbSpring2D.clicked.connect(self.new_connector2d)
        ui.pbSpring6D.clicked.connect(self.new_linear_connector)

        ui.pbForce.clicked.connect(self.new_force)
        ui.pbWindArea.pressed.connect(self.new_windarea)
        ui.pbCurrentArea.pressed.connect(self.new_currentarea)

        ui.pbContactShape.clicked.connect(self.new_contactmesh)
        ui.pbContactBall.clicked.connect(self.new_contactball)
        ui.pbSPMT.clicked.connect(self.new_spmt)

        ui.pbTank.clicked.connect(self.new_tank)
        ui.pbBuoyancyShape.clicked.connect(self.new_buoyancy_mesh)
        ui.pbLinearBuoyancy.clicked.connect(self.new_linear_hydrostatics)
        ui.pbWaveInteraction.clicked.connect(self.new_waveinteraction)

        ui.pbCable.clicked.connect(self.new_cable)
        ui.pbSling.clicked.connect(self.new_sling)
        ui.pbShackle.clicked.connect(self.new_shackle)
        ui.pbBeam.clicked.connect(self.new_beam)

        ui.pbVisual.clicked.connect(self.new_visual)
        ui.pbComponent.clicked.connect(self.new_component)

        menu.addAction(wa)

        for plugin in self.plugins_context:
            plugin(menu, node_name, self)

        menu.exec_(globLoc)

    def new_frame(self):
        self.new_something(new_node_dialog.add_frame)

    def new_body(self):
        self.new_something(new_node_dialog.add_body)

    def new_point(self):
        self.new_something(new_node_dialog.add_poi)

    def new_cable(self):
        self.new_something(new_node_dialog.add_cable)

    def new_force(self):
        self.new_something(new_node_dialog.add_force)

    def new_windarea(self):
        self.new_something(new_node_dialog.add_windarea)

    def new_currentarea(self):
        self.new_something(new_node_dialog.add_currentarea)

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

    def new_component(self):
        self.new_something(new_node_dialog.add_component)

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

    def new_spmt(self):
        self.new_something(new_node_dialog.add_spmt)

    def new_geometric_contact(self):
        msgBox = QMessageBox()
        msgBox.setText(
            "To create a Geometric Contact:\n\nDrag a circle onto another circle (in the node-tree)"
        )
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

    def view3d_select_element(self, props):

        # info is a list of props
        # at least a single prop is present
        #
        # we need to find the corresponding node

        node = self.visual.node_from_vtk_actor(props[0])

        if node is None:
            print("Could not find node for this actor")
            self.selected_nodes.clear()
            self.guiEmitEvent(guiEventType.SELECTION_CHANGED)

        # find the higest manager of this node
        manager = node.manager
        if manager is not None:
            while manager.manager is not None:
                manager = manager.manager

            if manager in self.selected_nodes:
                self.selected_nodes.remove(manager)
                self.guiSelectNode(node)
            else:
                if node in self.selected_nodes:
                    self.selected_nodes.remove(node)
                self.guiSelectNode(manager)

            return

        else:

            _node = node
            if node in self.selected_nodes:
                # if the is already selected, then select something different

                self.selected_nodes.remove(node)

                # # if node has a manager, then select the manager
                # if node.manager is not None:
                #     self.guiSelectNode(node.manager)
                #     return

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

        if node is None:  # sea or something
            self.selected_nodes.clear()
        else:
            self.guiSelectNode(node.name)

    def visual_update_selection(self):
        """Updates the _is_selected and _is_sub_selected properties of the visuals, then re-applies paint"""

        visually_selected_nodes = self.selected_nodes.copy()

        for node in self.selected_nodes:
            if isinstance(node, Manager):
                visually_selected_nodes.extend(self.scene.nodes_managed_by(node))

        # loop over visuals, and set _is_selected or _is_sub_selected based on the referenced node

        for v in self.visual.node_visuals:
            if v.node in visually_selected_nodes:
                v._is_selected = True
            else:
                v._is_selected = False

        # check sub-selection - but only for nodes that are not yet selected

        for v in self.visual.node_visuals:
            try:
                parent = v.node.parent
            except:
                continue

            if parent in visually_selected_nodes:
                if not v._is_selected:
                    v._is_sub_selected = (
                        True  # can not be sub-selected if already selected
                    )
            else:
                v._is_sub_selected = False

        self.visual.update_visibility()  # update paint

    # ================= guiWidget codes

    def guiEmitEvent(self, event, sender=None):

        with DelayRenderingTillDone(
            self.visual
        ):  # temporary freezes rendering and calls update afterwards

            for widget in self.guiWidgets.values():
                if not (widget is sender):
                    if widget.isVisible():
                        widget.guiEvent(event)

            # update the visual as well
            if event == guiEventType.SELECTION_CHANGED:
                self.visual_update_selection()
                return

            if event == guiEventType.SELECTED_NODE_MODIFIED:
                self.visual.add_new_node_actors_to_screen()
                if self.visual.settings.paint_uc:
                    self.visual.update_visibility()
                self.visual.position_visuals()
                return

            if event == guiEventType.MODEL_STATE_CHANGED:
                if self.visual.settings.paint_uc:
                    self.visual.update_visibility()
                self.visual.position_visuals()
                return

            if event == guiEventType.ENVIRONMENT_CHANGED:
                self.visual.position_visuals()
                return

            if event == guiEventType.VIEWER_SETTINGS_UPDATE:
                self.visual.update_visibility()
                self.visual.position_visuals()
                return

            if event == guiEventType.MODEL_STEP_ACTIVATED:
                if self.visual.settings.paint_uc:
                    self.visual.update_visibility()
                self.visual.position_visuals()
                return

            self.visual.create_node_visuals()
            self.visual.add_new_node_actors_to_screen()
            self.visual.position_visuals()
            self.visual_update_selection()

    def guiSelectNode(self, node_name):
        # Select a node with name, pass None to deselect all

        old_selection = self.selected_nodes.copy()

        if not (
            self.app.keyboardModifiers() and QtCore.Qt.KeyboardModifier.ControlModifier
        ):
            self.selected_nodes.clear()

        node = None
        if node_name is not None:
            node = self.scene._node_from_node_or_str(node_name)
            if node not in self.selected_nodes:
                self.selected_nodes.append(node)

        if self.selected_nodes:
            if self._active_workspace in ["CONSTRUCT", "TimeLine"]:
                if "Properties" in self.guiWidgets:
                    if not self.guiWidgets["Properties"].isVisible():
                        self.guiWidgets["Properties"].setVisible(True)
                        self.guiEmitEvent(
                            guiEventType.SELECTION_CHANGED
                        )  # force update

        # Get the screen position of the just selected visual
        #
        if node is not None:
            if self.visual.vtkWidget.hasFocus():
                self.move_floating_widgets_away_from_cursor()

        if old_selection != self.selected_nodes:
            self.guiEmitEvent(guiEventType.SELECTION_CHANGED)

    def move_floating_widgets_away_from_cursor(self):
        for w in self.guiWidgets.values():
            w.move_away_from_cursor()

    def show_guiWidget(self, name, widgetClass=None):

        if widgetClass is None:
            widgetClass = DAVE_GUI_DOCKS[
                name
            ]  # TODO, make this the default and remove the widgetClass argument

        if name in self.guiWidgets:
            d = self.guiWidgets[name]
        else:
            print("Creating {}".format(name))

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
            d.guiPressSolveButton = self.solve_statics
            d.gui = self

            if widgetClass == WidgetQuickActions:
                self.MainWindow.resizeDocks([d], [6], Qt.Horizontal)

        d.show()
        d._active = True
        d.guiEvent(guiEventType.FULL_UPDATE)



    # =============================

    def refresh_3dview(self):
        self.visual.refresh_embeded_view()

    # --- dragging actors ---

    def start_node_drag(self):
        """Start node drag in viewport
        Actual selection shall be a single node
        That single node shall be movable (extends Frame, Point, Visual)
        """

        # only works on one node
        if len(self.selected_nodes) != 1:
            self.give_feedback(f"Can not start drag - number of selected nodes should be exactly 1 but is {len(self.selected_nodes)}", style=1)
            return

        node = self.selected_nodes[0]

        nodes = [node]

        while True:
            if isinstance(node, (Frame, Point)):
                self._dragged_node = node
                logging.info(f"Starting drag on {node.name}")
                self.visual.initialize_node_drag(nodes)
                break

            parent = getattr(node, 'parent', None)

            if parent is None:
                break

            node = node.parent
            nodes.append(node)

    def node_dragged(self, info : DragInfo):  # callback from self.visual.Style
        """Apply the translation of the dragged node"""

        node = self._dragged_node
        old_position = np.array(node.global_position)
        new_position = old_position + info.delta

        code = f"s['{node.name}'].global_position = ({new_position[0]:.3f},{new_position[1]:.3f},{new_position[2]:.3f})"
        self.run_code(code,guiEventType.MODEL_STATE_CHANGED, store_undo=True)


# ======================================

if __name__ == "__main__":
    from DAVE import *

    s = Scene()
    Gui(s)
