"""

   This is the root module for the graphical user interface.

   The GUI is build using QT / PySide6 and is set-up to be easy to extent.

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
import os
import subprocess
import sys
import textwrap
import traceback
import webbrowser
import zipfile
import logging

from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon, QFont, QFontMetricsF, QAction, QActionGroup
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QMessageBox,
    QStatusBar,
    QToolBar,
    QWidget,
    QDialogButtonBox,
)

from DAVE.gui.autosave import DaveAutoSave
from DAVE.gui.dialog_blender import ExportToBlenderDialog
from DAVE.gui.dialog_export_package import ExportAsPackageDialog
from DAVE.gui.dock_solver_settings import WidgetSolverSettings
from DAVE.gui.dock_system.ads_helpers import (
    create_dock_manager,
    dock_remove_from_gui,
    dock_show,
    set_as_central_widget,
    add_global_dock,
    get_all_active_docks,
)
from DAVE.gui.dock_system.gui_dock_groups import DaveDockGroup
from DAVE.gui.helpers.gui_logger import DAVE_GUI_LOGGER
from DAVE.gui.helpers.qt_action_draggable import QDraggableNodeActionWidget
from DAVE.gui.widget_watches import WidgetWatches
from DAVE.helpers.code_error_extract import get_code_error
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

from DAVE import ModelInvalidException

import DAVE.settings as vfc
import DAVE.gui.node_icons


from DAVE.gui.forms.main_form import Ui_MainWindow
from DAVE.visual import Viewport, DelayRenderingTillDone
from DAVE.gui import new_node_dialog
import DAVE.gui.standard_assets
from DAVE.gui.forms.dlg_solver import Ui_Dialog
from DAVE.gui.forms.dlg_settingsr import Ui_frmSettings
import DAVE.settings
from DAVE.settings_visuals import PAINTERS, ICONS

# from DAVE.gui.helpers.highlighter import PythonHighlighter
from DAVE.gui.helpers.ctrl_enter import ShiftEnterKeyPressFilter
from DAVE.gui.helpers.qmenu import MenuSlider
from DAVE.gui.forms.menu_nodetypes import Ui_MenuNodes

from IPython.utils.capture import capture_output
import time
import scipy.interpolate

# All guiDockWidgets
from DAVE.gui.dock_system.dockwidget import *
from DAVE.gui.widget_nodetree import WidgetNodeTree
from DAVE.gui.widget_derivedproperties import WidgetDerivedProperties
from DAVE.gui.widget_nodeprops import WidgetNodeProps
from DAVE.gui.widget_dynamic_properties import WidgetDynamicProperties
from DAVE.gui.widget_modeshapes import WidgetModeShapes
from DAVE.gui.widget_stability_disp import WidgetDisplacedStability
from DAVE.gui.widget_explore import WidgetExplore
from DAVE.gui.widget_rigg_it_right import WidgetQuickActions
from DAVE.gui.widget_environment import WidgetEnvironment
from DAVE.gui.widget_dof_edit import WidgetDOFEditor
import DAVE.gui.widget_ballastsolver
import DAVE.gui.widget_ballastconfiguration
import DAVE.gui.widget_tank_order
import DAVE.gui.widget_ballastsystemselect


from DAVE.gui.forms.dlg_solver_threaded import Ui_SolverDialogThreaded

import DAVE.gui.dock_system.default_dock_groups

import DAVEcore

# resources
import DAVE.gui.forms.resources_rc

from DAVE.gui.settings import (
    DAVE_GUI_DOCKS,
    DOCK_GROUPS,
    GUI_DO_ANIMATE,
    GUI_SOLVER_ANIMATION_DURATION,
    GUI_ANIMATION_FPS,
)

DAVE_GUI_DOCKS["Node Tree"] = WidgetNodeTree
DAVE_GUI_DOCKS["Properties"] = WidgetNodeProps
DAVE_GUI_DOCKS["Quick actions"] = WidgetQuickActions
DAVE_GUI_DOCKS["Derived Properties"] = WidgetDerivedProperties
DAVE_GUI_DOCKS["Properties - dynamic"] = WidgetDynamicProperties
DAVE_GUI_DOCKS["Mode-shapes"] = WidgetModeShapes
DAVE_GUI_DOCKS["Environment"] = WidgetEnvironment
DAVE_GUI_DOCKS["Stability"] = WidgetDisplacedStability
DAVE_GUI_DOCKS["Limits and UCs"] = WidgetLimits
DAVE_GUI_DOCKS["Tags"] = WidgetTags
DAVE_GUI_DOCKS["Footprints"] = WidgetFootprints
DAVE_GUI_DOCKS["Graph"] = WidgetBendingMoment
DAVE_GUI_DOCKS["vanGogh"] = WidgetPainters
DAVE_GUI_DOCKS["DOF editor"] = WidgetDOFEditor
DAVE_GUI_DOCKS["Explore 1-to-1"] = WidgetExplore
DAVE_GUI_DOCKS["Solver Settings"] = WidgetSolverSettings

# ========================================================
#   Settings for customization of the GUI
# ========================================================
#
# List with of tupple with (Button text, WORKSPACE_ID)
#
# These buttons are created in the tool-bar.
# Clicking a button will call activate_workspace with WORKSPACE_ID
# DAVE_GUI_WORKSPACE_BUTTONS = [
#     ("Construct", "CONSTRUCT"),
#     ("Watches", "WATCHES"),
#     ("Explore", "EXPLORE"),
#     ("Ballast", "BALLAST"),
#     ("Shear and Bending", "MOMENTS"),
#     ("Environment", "ENVIRONMENT"),
#     ("Stability", "STABILITY"),
#     ("Limits", "LIMITS"),
#     ("Tags", "TAGS"),
#     ("Mode shapes [beta]", "DYNAMICS"),
#     ("Airy [beta]", "AIRY"),
# ]

DAVE_GUI_PLUGINS_INIT = []
DAVE_GUI_PLUGINS_WORKSPACE = []
DAVE_GUI_PLUGINS_CONTEXT = []
DAVE_GUI_PLUGINS_EDITOR = []

# ====================================================


class UndoType(Enum):
    CLEAR_AND_RUN_CODE = 1
    RUN_CODE = 2
    SET_DOFS = 3


class SolverDialog_threaded(QDialog, Ui_SolverDialogThreaded):
    def __init__(self, parent=None):
        super(SolverDialog_threaded, self).__init__()
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/v2/icons/DAVE.svg"))

        # make stay-on-top
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)


class SettingsDialog(QDialog, Ui_frmSettings):
    def __init__(self, scene, gui, parent=None):
        super(SettingsDialog, self).__init__()
        Ui_frmSettings.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/icons/cube.png"))

        paths_str = [
            "- " + str(p)
            for p in scene.resource_provider.resources_paths
            if p not in gui.additional_user_resource_paths
        ]
        self.label_4.setText("\n".join(paths_str))

        paths_str = [str(p) for p in gui.additional_user_resource_paths]
        self.plainTextEdit.setPlainText("\n".join(paths_str))


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
        read_only_mode=False,
        filename=None,
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
        DAVE_GUI_LOGGER.log("Starting GUI")
        DAVE_GUI_LOGGER.log(f"Version {DAVE.__version__}")

        self._read_only_mode = read_only_mode

        self.plugins_workspace = DAVE_GUI_PLUGINS_WORKSPACE
        self.plugins_context = DAVE_GUI_PLUGINS_CONTEXT
        self.plugins_editor = DAVE_GUI_PLUGINS_EDITOR

        self._owns_the_application = False
        if app is None:
            if QtWidgets.QApplication.instance() is not None:
                self.app = QtWidgets.QApplication.instance()
            else:
                self.app = QtWidgets.QApplication()
                self._owns_the_application = True
        else:
            self.app = app

        # self.app.setStyle("Fusion")

        # pre-load icons
        for key, icon in ICONS.items():
            if isinstance(icon, str):
                ICONS[key] = QIcon(icon)

        if scene is None:
            scene = Scene()

        DAVE_GUI_LOGGER.log("Assigned Scene to logger")
        DAVE_GUI_LOGGER.scene = scene

        # Main Window
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self.MainWindow)
        self.MainWindow.closeEvent = self.closeEvent

        if not self._read_only_mode:
            self.ui.infobar.close()

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

        self._animation_current_time = None

        self._animation_speed = 1.0

        # ================= Create globally available properties =======
        self.selected_nodes: [Node] = []
        """A list of selected nodes (if any)"""

        self.scene = scene
        """Reference to a scene"""

        self.scene.gui_solve_func = self.solve_statics_using_gui_on_scene
        """Claim control of the solver for the gui"""

        self.modelfilename = None
        """Open file"""

        self._model_has_changed = False
        """User"""

        self.additional_user_resource_paths = []
        """User-defined additional resource paths, stored on user machine - settings dialog"""

        self._undo_log = []
        self._undo_index = 0
        """Undo log and history"""

        self._active_dockgroup = None
        """Dock-groups"""

        self.settings = QSettings("rdbr", "DAVE")
        paths_str = self.settings.value(f"additional_paths")
        if paths_str:
            for p in paths_str.split(";"):
                if p:
                    self.additional_user_resource_paths.append(Path(p))
                    self.scene.add_resources_paths(p)

        self.update_resources_paths()

        # # ======================== Modify dock layout options ============
        #
        # self.MainWindow.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        # self.MainWindow.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        # self.MainWindow.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)
        # self.MainWindow.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)

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

        # right
        self.ui.btnWater.clicked.connect(self.toggle_show_sea)
        self.ui.pbOrigin.clicked.connect(self.toggle_show_origin)
        self.ui.pbUC.clicked.connect(self.toggle_show_UC)
        self.ui.btnBlender.clicked.connect(self.to_blender)
        self.ui.pbCopyViewCode.clicked.connect(self.copy_screenshot_code)
        self.ui.btnSSAO.clicked.connect(self.toggle_SSAO)
        self.ui.btnZoomFit.clicked.connect(self.camera_reset)

        # left
        self.ui.pbUpdate.clicked.connect(
            lambda: self.guiEmitEvent(guiEventType.FULL_UPDATE)
        )
        # self.ui.btnSolveStatics.clicked.connect(self.solve_statics)
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
        self.ui.actionImport_package.triggered.connect(
            self.open_self_contained_DAVE_package_gui
        )
        self.ui.actionSave.triggered.connect(self.menu_save_model)
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
        self.ui.actionSelf_contained_DAVE_package.triggered.connect(
            self.menu_export_DAVE_package
        )
        self.ui.action3D_points_to_csv.triggered.connect(self.to_csv)

        self.ui.actionSend_bug_report.triggered.connect(self.bug_report)

        # --- recent files ---

        self.recent_files = []
        self.ui.menuFile.addSeparator()
        for i in range(8):
            action = QAction("none")
            action.triggered.connect(lambda *args, a=i: self.open_recent(a))
            self.recent_files.append(action)
            self.ui.menuFile.addAction(action)
        self.update_recent_file_menu()

        # -- drag drop files into DAVE --

        self.ui.frame3d.dropEvent = self.drop
        self.ui.frame3d.dragEnterEvent = self.drag_enter

        # -- visuals --
        self.ui.actionShow_origin.triggered.connect(self.toggle_show_origin)
        self.ui.actionShow_water_plane.triggered.connect(self.toggle_show_sea)
        self.ui.actionShow_force_applying_element.triggered.connect(
            self.toggle_show_force_applying_elements
        )

        # cog size
        self.ui.menuView.addSeparator()

        # --- label size
        self.ui.actionShow_labels.setChecked(self.visual.settings.label_scale > 0)

        self.ui.sliderLabelSize = MenuSlider("Label size")
        self.ui.sliderLabelSize.setMin(0)
        self.ui.sliderLabelSize.setMax(100)
        self.ui.sliderLabelSize.slider.setValue(10)

        def set_label_size(value):
            self.run_code(
                f"self.visual.settings.label_scale = {value / 10}",
                guiEventType.VIEWER_SETTINGS_UPDATE,
            )
            self.visual.refresh_embeded_view()

        self.ui.sliderLabelSize.connectvalueChanged(set_label_size)
        self.ui.menuView.addAction(self.ui.sliderLabelSize)

        # ---- label size

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
        self.ui.actionSet_input_focus_to_viewport.triggered.connect(
            self.focus_on_viewport
        )

        self.ui.pbTop.clicked.connect(self.visual.Style.SetViewZ)
        self.ui.pbFront.clicked.connect(self.visual.Style.SetViewY)
        self.ui.pbSide.clicked.connect(self.visual.Style.SetViewX)
        self.ui.pb3D.clicked.connect(self.toggle_2D)

        # the python console
        self.ui.dockWidget_2.setVisible(False)
        self.ui.actionPython_console_2.triggered.connect(self.show_python_console)

        # dof editor
        self.ui.actionDegrees_of_Freedom_editor.triggered.connect(
            lambda: self.show_dock("DOF Editor")
        )

        # solver settings
        self.ui.actionSolver_settings.triggered.connect(
            lambda: self.show_dock("Solver Settings")
        )

        self.ui.actionVersion.setText(f"Version {DAVE.__version__}")
        self.ui.actionOnline_help.triggered.connect(
            lambda: subprocess.Popen("explorer https://usedave.nl")
        )

        # ======================= Code-highlighter ==============

        font = QFont()
        font.setPointSize(10)
        font.setFamily("Consolas")
        self.ui.teCode.setFont(font)
        self.ui.teCode.setTabStopDistance(
            QFontMetricsF(self.ui.teCode.font()).horizontalAdvance(" ")
        )

        # self.highlight = PythonHighlighter(self.ui.teCode.document())

        self.teCode_eventFilter = ShiftEnterKeyPressFilter()
        self.teCode_eventFilter.callback = self.run_code_in_teCode
        self.ui.teCode.installEventFilter(self.teCode_eventFilter)

        # ======================== Docks ====================
        self.guiWidgets = dict()
        """Dictionary of all created guiWidgets (dock-widgets)"""

        for plugin_init in DAVE_GUI_PLUGINS_INIT:
            plugin_init(self)

        # ========== undo log =======

        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)

        # setup the docking system

        self.dock_manager = create_dock_manager(self.MainWindow, self.settings)

        # Set the main widget

        self.main_widget = QtWidgets.QWidget()

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.widget_3)
        layout.addWidget(self.ui.frame3d)
        layout.addWidget(self.ui.frameAni)
        self.main_widget.setLayout(layout)

        self.central_dock_widget = set_as_central_widget(
            self.dock_manager, self.main_widget
        )

        # Add the global docks
        add_global_dock(
            self.dock_manager, self.get_dock("Properties"), icon=":/v2/icons/pencil.svg"
        )

        add_global_dock(
            self.dock_manager,
            self.get_dock("Environment"),
            icon=":/v2/icons/environment.svg",
        )

        add_global_dock(
            self.dock_manager,
            self.get_dock("Derived Properties"),
            icon=":/v2/icons/magnifier90.svg",
        )
        add_global_dock(
            self.dock_manager, self.get_dock("Watches"), icon=":/v2/icons/glasses.svg"
        )
        add_global_dock(
            self.dock_manager, self.get_dock("Tags"), icon=":/v2/icons/tag.svg"
        )

        # ------ Add the permanent docks -------
        self.docks_permanent = [self.central_dock_widget]

        # -- tree
        self.dock_permanent_tree = self.get_dock("Node Tree")
        self.dock_manager.addDockWidget(
            PySide6QtAds.DockWidgetArea.LeftDockWidgetArea, self.dock_permanent_tree
        )
        self.docks_permanent.append(self.dock_permanent_tree)

        # self.dock_manager

        # --- timeline - if any

        try:
            self.dock_timeline = self.get_dock("TimeLine")
            area = self.dock_manager.addDockWidget(
                PySide6QtAds.DockWidgetArea.RightDockWidgetArea, self.dock_timeline
            )
            self.docks_permanent.append(self.dock_timeline)
            self.dock_timeline.toggleViewAction().trigger()  # closed by default

        except Exception as M:
            self.dock_timeline = None

        # Toolbar (top)
        self.toolbar_top = QToolBar("Top Toolbar")
        self.MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar_top)

        top_left_widget = QWidget(self.MainWindow)
        self.toolbar_top.addWidget(top_left_widget)

        # Add actions for permanent docks
        action = self.dock_permanent_tree.toggleViewAction()
        action.setIcon(QIcon(":v2/icons/tree.svg"))
        self.toolbar_top.addAction(action)

        if self.dock_timeline is not None:
            action = self.dock_timeline.toggleViewAction()
            action.setIcon(QIcon(":v2/icons/timeline.svg"))
            self.toolbar_top.addAction(action)

        self.top_bar_group_label = QtWidgets.QLabel(self.MainWindow)
        self.top_bar_group_label.setText("DAVE")
        self.top_bar_group_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: palette(midlight);"
        )
        self.toolbar_top.addWidget(self.top_bar_group_label)

        self.toolbar_top_right = QToolBar("Top Toolbar Right")
        self.MainWindow.addToolBar(
            Qt.ToolBarArea.TopToolBarArea, self.toolbar_top_right
        )

        self.toolbar_top_right.setMovable(False)

        # Left part of right toolbar

        self.save_perspective_action = QAction("Save perspective", self.MainWindow)
        self.save_perspective_action.triggered.connect(self.save_perspective)
        self.save_perspective_action.setIcon(QIcon(":/v2/icons/heart_empty_small.svg"))
        self.toolbar_top_right.addAction(self.save_perspective_action)

        # middle part of the top toolbar
        self.warnings_label = QAction(self.MainWindow)
        self.warnings_label.setText("Warnings")
        self.warnings_label.triggered.connect(self.show_warnings)
        self.warnings_label.setIcon(QIcon(":/v2/icons/warning.svg"))
        self.toolbar_top_right.addAction(self.warnings_label)

        # format the produced toolbutton
        button = self.toolbar_top_right.widgetForAction(self.warnings_label)
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.update_warnings()

        # spacer
        spacer_widget = QtWidgets.QWidget(self.MainWindow)
        spacer_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self.toolbar_top_right.addWidget(spacer_widget)

        # right part of right toolbar

        self.toolbar_top_right.addWidget(QtWidgets.QLabel("Solve:  "))
        self.solveAction = QAction("Solve", self.MainWindow)
        self.solveAction.setToolTip("Solve statics [Alt+S]")
        self.solveAction.triggered.connect(self.solve_statics)
        self.solveAction.setIcon(QIcon(":/v2/icons/DAVE.svg"))
        self.solveAction.setShortcut("Alt+S")
        self.toolbar_top_right.addAction(self.solveAction)

        # Toolbar (left)
        self.toolbar_left = QToolBar("Left Toolbar")
        self.MainWindow.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar_left)
        self.toolbar_left.setOrientation(Qt.Vertical)
        self.toolbar_left.setIconSize(QSize(32, 32))
        self.toolbar_left.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.create_dockgroups()

        # create all docks
        # self.pre_create_docks()

        # Makup
        self.toolbar_left.setContextMenuPolicy(
            Qt.CustomContextMenu
        )  # disable the default context menu
        self.toolbar_top.setContextMenuPolicy(Qt.CustomContextMenu)
        self.toolbar_top_right.setContextMenuPolicy(Qt.CustomContextMenu)

        self.toolbar_top.setMovable(False)
        self.toolbar_left.setMovable(False)

        backgroundcolor_str = "palette(midlight)"

        self.toolbar_top.setStyleSheet(
            "QToolBar { background : " + backgroundcolor_str + "; border: none; }\n"
            "QToolButton:checked{ background-color : " + backgroundcolor_str + "; }"
        )
        self.toolbar_left.setStyleSheet(
            "QToolBar { background : " + backgroundcolor_str + "; border: none; }\n"
            "QToolButton:checked{ background-color : "
            + backgroundcolor_str
            + "; border-width : 2px}"
        )
        top_left_widget.setStyleSheet(
            "background : " + backgroundcolor_str + "; border: none"
        )
        top_left_widget.setFixedWidth(self.toolbar_left.sizeHint().width())

        # Status-bar

        self.statusbar = QStatusBar()
        self.MainWindow.setStatusBar(self.statusbar)
        # self.statusbar.mousePressEvent = self.show_python_console

        # copy-paste
        self.ui.actionCopy.triggered.connect(self.clipboard_copy)
        self.ui.actionPaste.triggered.connect(self.clipboard_paste)

        # ======================== Finalize ========================

        self._requested_workspace = workspace

        if self._read_only_mode:
            self.ui.infobar.setWindowTitle(
                "This is a COPY of the model intended to view the results of an analysis. It may be re-organized, cleaned up or adapted otherwise."
            )
        #     self.ui.menuFile.setTitle("Read only mode")
        #     self.ui.menuFile.setEnabled(False)
        #     self.ui.menuScene.setEnabled(False)
        #     self.ui.menuEdit.setEnabled(False)

        self.MainWindow.show()

        # start autosave, but only if we are not running in read-only mode
        # or as part of a unit-test

        if "PYTEST_CURRENT_TEST" in os.environ or self._read_only_mode:
            self._autosave = None

        else:
            open_autosave = self.autosave_startup()

            if open_autosave:
                self.open_file(open_autosave)
            elif isinstance(filename, str):
                self.open_file(filename)

        if splash:
            splash.finish(self.MainWindow)

        if block:
            self.ui.pbUpdate.setVisible(False)
            self.ui.pbCopyViewCode.setVisible(False)

            # create a time to trigger after-startup events
            sst = QtCore.QTimer()
            sst.setSingleShot(True)
            sst.singleShot(0, self.after_startup)  # <-- 0 ms delay is ok

            self.app.exec()
        else:
            self.after_startup()  # execute directly

    def after_startup(self):
        """Executed after the gui has started up"""
        self.visual.zoom_all()
        self.visual.refresh_embeded_view()

        if self._requested_workspace is None:
            self.activate_dockgroup("Build", this_is_a_new_window=True)
        else:
            self.activate_dockgroup(
                self._requested_workspace, this_is_a_new_window=True
            )

    def logcode(self, code):
        self._codelog.append(code)
        self.ui.teHistory.append(code)

        self.tidy_history()

        self.ui.teHistory.verticalScrollBar().setValue(
            self.ui.teHistory.verticalScrollBar().maximum()
        )  # scroll down all the way

    def update_warnings(self):
        """Updates the warnings label"""
        warnings = self.scene.warnings

        if warnings:
            self.warnings_label.setVisible(True)
            # self.warnings_label.setEnabled(True)
            self.warnings_label.setText(f"Warnings: {len(warnings)}")
        else:
            self.warnings_label.setVisible(False)
            # self.warnings_label.setEnabled(False)
            self.warnings_label.setText("")

    def show_warnings_help(self):
        webbrowser.open("https://usedave.nl/scene/model_and_state_errors.html")

    def show_warnings(self):
        """Shows the warnings"""
        warnings = self.scene.warnings

        # create a dialog with a table
        dlg = QDialog()
        dlg.setWindowTitle("Warnings")
        dlg.setWindowIcon(QIcon(":/v2/icons/warning.svg"))
        dlg.setWindowFlag(Qt.WindowContextHelpButtonHint, True)

        layout = QtWidgets.QVBoxLayout()
        dlg.setLayout(layout)

        table = QtWidgets.QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Node", "Code", "Message"])
        table.setRowCount(len(warnings))

        for i, (node, message) in enumerate(warnings):
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(node.name))
            code = message.split(" ")[0]
            message = " ".join(message.split(" ")[1:])
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(code))
            table.setItem(i, 2, QtWidgets.QTableWidgetItem(message))

        layout.addWidget(table)

        # make the table stretch
        table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )

        # set the initial size of the dialog, but the user must still be able to resize it
        # to a smaller size
        dlg.resize(800, 400)

        # Add two buttons: ok and help
        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Help)
        buttonbox.accepted.connect(dlg.accept)
        buttonbox.helpRequested.connect(self.show_warnings_help)

        layout.addWidget(buttonbox)

        dlg.exec()

    def bug_report(self):
        """Creates a bug report email"""
        DAVE_GUI_LOGGER.log("creating bug report")
        from DAVE.gui.helpers.crash_mailer import compile_and_mail

        compile_and_mail()

    def show_dock(self, name):
        """Shows a dock by name"""
        dock = self.get_dock(name)
        dock_show(self.dock_manager, dock, True)

    def autosave_startup(self) -> str:
        # check for autosave files
        filename = None
        autosave_files = DaveAutoSave.scan()
        if autosave_files:
            autosave_file = autosave_files[-1]
            autosave_file = autosave_file.absolute()
            print(f"Autosave file found: {autosave_file}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                f"An autosave file was found:\n{autosave_file}\n\nDo you want to open it?"
            )
            msg.setWindowTitle("Autosave file found")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            retval = msg.exec()
            if retval == QMessageBox.Yes:
                filename = autosave_file
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(
                    f"Do you want to open the autosave folder (for example to manually delete the file if you do no longer need it)?"
                )
                msg.setWindowTitle("Open autosave folder?")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                retval = msg.exec()
                if retval == QMessageBox.Yes:
                    DaveAutoSave.open_folder()

        self._autosave = DaveAutoSave()

        # create a new autosave file
        self._autosave = DaveAutoSave()
        self._autosavetimer = QTimer()
        self._autosavetimer.timeout.connect(self._autosave_write)
        self._autosavetimer.start(1000 * DAVE.gui.settings.AUTOSAVE_INTERVAL_S)

        return filename

    def clipboard_copy(self):
        # get the selected nodes
        if self.selected_nodes:
            node = self.selected_nodes[0]

            code = vfc.DAVE_CLIPBOARD_HEADER + f's.duplicate_branch("{node.name}")'
            self.app.clipboard().setText(code)
            self.give_feedback(f"Duplicate node {node.name} copied to clipboard")

            DAVE_GUI_LOGGER.log("To Clipboard: " + code)

    def clipboard_paste(self):
        try:
            text = self.app.clipboard().text()
        except:
            self.give_feedback("Nothing to paste")
            return

        if text.strip():
            if text.startswith(vfc.DAVE_CLIPBOARD_HEADER):
                text = text[len(vfc.DAVE_CLIPBOARD_HEADER) :]
            else:
                # ask user if ok to run the code from the clipboard

                short_code = text
                if len(short_code) > 200:
                    short_code = short_code[:100] + "\n...\n" + short_code[-100:]

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"Do you want to run the following code?\n\n" + short_code)

                msg.setWindowTitle("Run code from clipboard?")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                retval = msg.exec()
                if retval == QMessageBox.No:
                    return

            DAVE_GUI_LOGGER.log("Executing code from clipboard")
            self.run_code(text, guiEventType.MODEL_STRUCTURE_CHANGED)
        else:
            self.give_feedback("Nothing to paste")

    def menu_export_DAVE_package(self, *args):
        d = ExportAsPackageDialog()
        d.show(self.scene, str(self.scene.current_directory))

    def focus_on_viewport(self, *args):
        # Executed when escape is pressed
        DAVE_GUI_LOGGER.log("Focus on viewport")
        if self.visual.vtkWidget.hasFocus():
            self.escPressed()
        else:
            self.visual.vtkWidget.setFocus()

    def show_python_console(self, *args):
        self.ui.dockWidget_2.show()

    def new_scene(self):
        DAVE_GUI_LOGGER.log("New scene")
        self.scene.clear()
        self.guiEmitEvent(guiEventType.FULL_UPDATE)

    def show_settings(self):
        dlg = SettingsDialog(scene=self.scene, gui=self)
        result = dlg.exec_()
        if result > 0:
            text = dlg.plainTextEdit.toPlainText()
            paths = text.split("\n")

            self.additional_user_resource_paths.clear()
            for p in paths:
                if p:
                    self.additional_user_resource_paths.append(Path(p))
                settings = QSettings("rdbr", "DAVE")
                paths_str = ";".join(
                    [str(p) for p in self.additional_user_resource_paths]
                )
                settings.setValue(f"additional_paths", paths_str)

        self.update_resources_paths()

    def update_resources_paths(self):
        """Updates the global settings.DAVE_RESOURCES_PATHS and current scene to include the user-defined dirs

        Note: removing paths requires a program restart
        """
        DAVE_GUI_LOGGER.log("Update resource paths")

        for p in self.additional_user_resource_paths:
            if p not in DAVE.settings.RESOURCE_PATH:
                DAVE.settings.RESOURCE_PATH.append(p)
                self.scene.add_resources_paths(p)

    def labels_show_hide(self):
        DAVE_GUI_LOGGER.log("Toggle labels")

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
        DAVE_GUI_LOGGER.log("Refresh model")
        code = self.scene.give_python_code()
        self.scene.clear()
        self.scene.run_code(code)
        self.guiEmitEvent(guiEventType.FULL_UPDATE)

    def delete_key(self):
        """Delete key pressed in either main-form or viewport"""
        DAVE_GUI_LOGGER.log("Delete key pressed")
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
        DAVE_GUI_LOGGER.log("Change paintset")

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
        DAVE_GUI_LOGGER.log("Activate paintset")

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
        DAVE_GUI_LOGGER.log("Copy screenshot code")

        sea = self.visual.settings.show_sea

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
        DAVE_GUI_LOGGER.log("Escape pressed")

        self.animation_terminate()  # terminate any running animations
        self.select_none()

    def select_none(self):
        DAVE_GUI_LOGGER.log("Select none")

        if self.selected_nodes:
            self.selected_nodes.clear()
            # if "Properties" in self.guiWidgets:
            #     if self.guiWidgets["Properties"].node_picker is None:
            #         self.guiWidgets["Properties"].setVisible(False)
            self.guiEmitEvent(guiEventType.SELECTION_CHANGED)

    def focus_on_selected_object(self):
        """Moves the viewport view to the selected object"""

        DAVE_GUI_LOGGER.log("Focus on selected object")

        if self.selected_nodes:
            node = self.selected_nodes[0]
            visual = self.visual.actor_from_node(node)

            if visual is not None:
                position = visual.center_position
                print(f"focusing camera to {node.name} at {position}")
                self.visual.focus_on(position)

                self.refresh_3dview()

    def close_all_open_docks(self):
        """Closes all open docks"""
        DAVE_GUI_LOGGER.log("Close all open docks")
        for g in self.guiWidgets.values():
            dock_remove_from_gui(self.dock_manager, g)

    def pre_create_docks(self):
        """Create all docks, then close them again"""

        DAVE_GUI_LOGGER.log("Pre-create docks")

        for k in DAVE_GUI_DOCKS.keys():
            if k in self.guiWidgets:
                continue

            d = self.get_dock(k)
            d.toggleViewAction().trigger()

    def create_dockgroups(self):
        """Creates the dockgroups for each workspace"""

        DAVE_GUI_LOGGER.log("Create dockgroups")

        tasks = QActionGroup(self.MainWindow)
        tasks.setExclusive(True)

        for d in DOCK_GROUPS:
            d: DaveDockGroup

            # manual word-wrap on the description
            word_wrapped_description = "\n".join(
                textwrap.wrap(d.description, width=10, break_long_words=False)
            )

            action = QAction(word_wrapped_description, self.MainWindow)  #
            tasks.addAction(action)

            d._action = action

            # action.setText(d.description)
            action.setCheckable(True)
            icon = d.icon
            if isinstance(icon, str):
                icon = QIcon(icon)
            action.setIcon(icon)
            action.triggered.connect(
                lambda *args, name=d.ID: self.activate_dockgroup(name)
            )
            self.toolbar_left.addAction(action)

    def save_perspective(self):
        """Saves the current perspective (dock layout)"""

        DAVE_GUI_LOGGER.log("Save perspective")

        if self._active_dockgroup is not None:
            perspective_name = self._active_dockgroup.ID
            self.dock_manager.addPerspective(perspective_name)
            self.dock_manager.savePerspectives(self.settings)
            print("Perspective saved")
            self.save_perspective_action.setIcon(
                QIcon(":/v2/icons/heart_full_small.svg")
            )

    def activate_dockgroup(self, name, this_is_a_new_window=False):
        DAVE_GUI_LOGGER.log(f"Activate dockgroup: {name}")

        names = [d.ID for d in DOCK_GROUPS]

        if name not in names:
            raise ValueError(
                f"Unknown dockgroup {name}, available dockgroups are {names}"
            )

        group: DaveDockGroup = DOCK_GROUPS[names.index(name)]

        # Make sure the action is checked even when not activated by user
        action = getattr(group, "_action", None)
        if action is not None:
            action.setChecked(True)

        if not this_is_a_new_window:
            if group.new_window:
                s = self.scene
                if group.new_window_copy:
                    s = s.copy()

                if group.init_actions:
                    try:
                        s.run_code(group.init_actions)
                    except Exception as E:
                        if not group.new_window_copy:
                            raise ModelInvalidException(
                                "Error when performing init actions for new window"
                                + str(E)
                            )
                        else:
                            raise E

                g = Gui(
                    s,
                    block=False,
                    read_only_mode=group.new_window_read_only,
                    workspace=name,
                )

                if group.new_window_no_workspaces:
                    g.toolbar_left.setVisible(False)

                return

        do_load_perspectives = True

        if self._active_dockgroup is not None:
            if self._active_dockgroup.ID == name:
                print("Dockgroup already active")

                # show a messagebox asking if the user wants to re-open the dockgroup (this will reset the dock layout)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setText(
                    f"Do you want to re-open the dockgroup {name} without applying the saved positions (if any) ?"
                )
                msg.setWindowTitle("Re-open dockgroup?")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                retval = msg.exec()

                if retval == QMessageBox.Yes:
                    do_load_perspectives = False
                else:
                    return

        self._active_dockgroup = group

        self.top_bar_group_label.setText(group.description)

        self.animation_terminate()
        # self.savepoint_restore()

        wanted_docks = [
            self.get_dock(name, send_full_update=False) for name in group.dock_widgets
        ]
        all_active_docks = get_all_active_docks(self.dock_manager)

        # Remove all non-needed
        for dock in all_active_docks:
            if dock in self.docks_permanent:
                continue

            if dock not in wanted_docks:
                dock_remove_from_gui(self.dock_manager, dock)
                self.toolbar_top.removeAction(dock.toggleViewAction())

        # Create all needed
        for dock in wanted_docks:
            dock_show(
                self.dock_manager, dock
            )  # does not do anything if dock is already visible, so safe to call

        # Add actions to the top-bar
        for dock in wanted_docks:
            action = dock.toggleViewAction()
            self.toolbar_top.addAction(action)

            if dock not in all_active_docks:
                dock.guiEvent(guiEventType.FULL_UPDATE)

        # (de)active the default docks
        def set_visible(dock, visible):
            if visible is not None:
                if (
                    visible
                    and not dock.isVisible()
                    or visible is False
                    and dock.isVisible()
                ):
                    dock.toggleViewAction().trigger()

        set_visible(self.dock_permanent_tree, group.show_tree)
        if self.dock_timeline is not None:
            set_visible(self.dock_timeline, group.show_timeline)

        # Set the active perspective
        if group.ID in self.dock_manager.perspectiveNames() and do_load_perspectives:
            print("Loading perspective", group.ID)

            #
            self.dock_manager.openPerspective(name)
            self.save_perspective_action.setIcon(
                QIcon(":/v2/icons/heart_full_small.svg")
            )

            # check if all docks are still ok
            for name, dock in self.guiWidgets.items():
                assert dock == self.dock_manager.dockWidgetsMap()[name]

        else:
            self.save_perspective_action.setIcon(
                QIcon(":/v2/icons/heart_empty_small.svg")
            )

        self.visual.update_visibility()

    def import_browser(self):
        DAVE_GUI_LOGGER.log("Import browser")

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

    # ============== File open / recent / drag-drop functions ===========

    def drag_enter(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def drop(self, event):
        DAVE_GUI_LOGGER.log("Drop event: ")

        filename = event.mimeData().text()

        DAVE_GUI_LOGGER.log(filename)

        from pathlib import Path
        from urllib.parse import urlparse

        filename = urlparse(filename)[2]
        filename = filename[1:]
        p = Path(filename)

        # show a messagebox asking if the user wants to open the file
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(f"Do you want to open the file {p.name}?")
        msg.setWindowTitle("Open file?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg.exec()

        if retval == QMessageBox.Yes:
            if p.exists():
                try:
                    self.open_file(p)
                except:
                    raise ValueError(f"Could not open file {filename}")
            else:
                raise ValueError(f"Could not open file {filename}")

    def get_recent(self):
        DAVE_GUI_LOGGER.log("Get recent files")
        settings = QSettings("rdbr", "DAVE")
        files = []
        for i in range(8):
            files.append(settings.value(f"recent{i}", ""))
        return files

    def add_to_recent_file_menu(self, filename):
        DAVE_GUI_LOGGER.log(f"Add to recent file menu: {filename}")
        settings = QSettings("rdbr", "DAVE")

        files = self.get_recent()

        if filename in files:
            files.remove(filename)

        files = [filename, *files]
        for i in range(8):
            files.append(settings.setValue(f"recent{i}", files[i]))

        self.update_recent_file_menu()

    def update_recent_file_menu(self):
        DAVE_GUI_LOGGER.log("Update recent file menu")
        files = self.get_recent()
        for i in range(8):
            if files[i]:
                self.recent_files[i].setText(f"&{i+1} " + str(files[i]))
            else:
                self.recent_files[i].setText("recent files will appear here")

    def open_recent(self, i):
        DAVE_GUI_LOGGER.log(f"Open recent file: {i}")
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
        DAVE_GUI_LOGGER.log("Animation speed change")
        self._animation_speed = self.ui.sbPlaybackspeed.value()

    def animation_activate_time(self, t):
        self._animation_current_time = t
        dofs = self._animation_keyframe_interpolation_object(t)
        self.scene._vfc.set_dofs(dofs)
        self.visual.update_dynamic_waveplane(t)
        self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)

    def animation_terminate(self, keep_current_dofs=False):
        DAVE_GUI_LOGGER.log(
            f"Terminate animation, keep_current_dofs = {keep_current_dofs}"
        )

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
        """Start a new animation

        Args:
            t:    List of times at keyframes
            dofs: List of dofs at keyframes
            is_loop: Should animation be played in a loop (bool)
            final_dofs : [optional] DOFS to be set when animation is finished or terminated. Defaults to last keyframe
            do_not_reset_time : do not reset the time when starting the animation, this means the loop continues where it was.


        """
        DAVE_GUI_LOGGER.log("Start animation...")
        self.animation_terminate(keep_current_dofs=False)  # end old animation, if any

        DAVE_GUI_LOGGER.log("Creating animation objects")

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
        DAVE_GUI_LOGGER.log("Animation available = True")

        if not show_animation_bar:  # override pause for short animations
            self.ui.btnPauseAnimation.setChecked(False)
            self._animation_paused = False

        if not self._animation_paused:
            iren = self.visual.renwin.GetInteractor()
            if self._timerid is None:
                self._timerid = iren.CreateRepeatingTimer(
                    round(1000 / GUI_ANIMATION_FPS)
                )

            else:
                raise Exception("could not create new timer, old timer is still active")

    def animation_pause(self):
        """Pauses a running animation"""

        DAVE_GUI_LOGGER.log("Pause animation")

        if self._animation_paused:
            return

        if self._timerid is not None:
            to_be_destroyed = self._timerid
            self._timerid = None
            iren = self.visual.renwin.GetInteractor()
            iren.DestroyTimer(to_be_destroyed)

        self._animation_paused = True

    def animation_continue(self):
        DAVE_GUI_LOGGER.log("Continue animation")

        if not self._animation_paused:
            return

        if self._animation_available:
            if self._timerid is None:
                iren = self.visual.renwin.GetInteractor()
                self._timerid = iren.CreateRepeatingTimer(
                    round(1000 / GUI_ANIMATION_FPS)
                )

        self._animation_paused = False

    def animation_pause_or_continue_click(self):
        """Pauses or continues the animation"""

        DAVE_GUI_LOGGER.log("Pause or continue animation")

        if self._animation_paused:
            self.ui.btnPauseAnimation.setIcon(QIcon(":/v2/icons/pause.svg"))
            self.animation_continue()
        else:
            self.animation_pause()
            self.ui.btnPauseAnimation.setIcon(QIcon(":/v2/icons/play.svg"))
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

    def _autosave_write(self):
        """Writes the autosave file"""
        DAVE_GUI_LOGGER.log("Autosave write")
        try:
            code = "# DAVE autosave file\n"
            code += f"# for: {self.modelfilename}\n#\n"

            curdir = self.scene.current_directory
            if curdir is not None:
                code += 's.current_directory = r"{}"\n'.format(curdir)

            code += self.scene.give_python_code()
            self._autosave.write(code)

            DAVE_GUI_LOGGER.log("Autosaved to {}".format(self._autosave.autosave_file))
        except Exception as e:
            self.show_exception(
                f"Could not save autosave file because {e} \n\n Advised to use the UNDO function to restore the model to a previous state, then save and restart"
            )

    # ==== undo functions ====

    def undo(self):
        DAVE_GUI_LOGGER.log("Undo")
        self._undo_index -= 1
        if self._undo_index < 0:
            QMessageBox.information(
                self.ui.widget, "Undo", "Can not undo any further", QMessageBox.Ok
            )

            self._undo_index = 0
            return

        if self._undo_index == len(self._undo_log) - 1:
            # Make an undo point for the current state
            self._undo_log.append(
                (UndoType.CLEAR_AND_RUN_CODE, self.scene.give_python_code())
            )

        self.activate_undo_index(self._undo_index)

    def redo(self):
        DAVE_GUI_LOGGER.log("Redo")
        self._undo_index += 1
        if self._undo_index > len(self._undo_log) - 1:
            QMessageBox.information(
                self.ui.widget, "Redo", "Can not redo any further", QMessageBox.Ok
            )
            self._undo_index = len(self._undo_log) - 1
            return

        self.activate_undo_index(self._undo_index)

    def activate_undo_index(self, index):
        """Activates the undo index"""
        DAVE_GUI_LOGGER.log(f"Activate undo index: {index}")
        print(f"Activating undo index {index} of {len(self._undo_log)-1}")

        undo_type, undo_contents = self._undo_log[index]  # unpack

        if undo_type == UndoType.CLEAR_AND_RUN_CODE or undo_type == UndoType.RUN_CODE:
            # capture selected node names before deleting the scene

            try:
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
                self.give_feedback(
                    f"Activating undo index {index} of {len(self._undo_log)-1}"
                )
            except:
                self.show_exception(
                    f"Could not activate undo index {index} of {len(self._undo_log)-1}"
                )

            self.guiEmitEvent(guiEventType.FULL_UPDATE)

        elif undo_type == UndoType.SET_DOFS:
            if undo_contents is not None:
                self.scene._vfc.set_dofs(undo_contents)  # UNDO SOLVE STATICS"
                self.give_feedback(
                    f"Activating undo index {index} of {len(self._undo_log)} - Solve-statics reverted"
                )

                self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)

    def add_undo_point(self, undo_type=UndoType.CLEAR_AND_RUN_CODE, code=""):
        logging.info(f"Creating undo point with type {undo_type}")
        DAVE_GUI_LOGGER.log(f"Add undo point, type = {undo_type}")

        if undo_type == UndoType.CLEAR_AND_RUN_CODE:
            """Adds the current model to the undo-list"""
            if len(self._undo_log) > self._undo_index:
                self._undo_log = self._undo_log[: self._undo_index]
            self._undo_log.append(
                (UndoType.CLEAR_AND_RUN_CODE, self.scene.give_python_code())
            )

        elif undo_type == UndoType.RUN_CODE:
            self._undo_log.append((UndoType.RUN_CODE, code))

        elif undo_type == UndoType.SET_DOFS:
            self._undo_log.append((UndoType.SET_DOFS, self.scene._vfc.get_dofs()))

        else:
            raise Exception("Unsupported undo type")

        self._undo_index = len(self._undo_log)
        logging.info(f"current log index = number of points = {self._undo_index}")

    # / undo functions

    def closeEvent(self, event):
        """This is the on-close for the main window"""

        DAVE_GUI_LOGGER.log("Close event")

        self.animation_terminate()

        if self.maybeSave():
            event.accept()

            if self._owns_the_application:
                DAVE_GUI_LOGGER.log("Closing dock manager")
                self.dock_manager.deleteLater()

            DAVE_GUI_LOGGER.log("Shutting down vtk interactor")
            self.visual.shutdown_qt()

            print("removing autosave files")
            DAVE_GUI_LOGGER.log("removing autosave files")
            if self._autosave is not None:
                self._autosave.cleanup()

            print(
                "-- closing the gui : these were the actions you performed while the gui was open --"
            )
            print(self.give_clean_history())
        else:
            event.ignore()

    # def onCloseApplication(self):
    #     """This is the on-close for the Application"""

    def measured_in_viewport(self, distance, angle):
        """Executed when a distance is measured in the viewport"""
        self.give_feedback(
            f"View-plane distance = {distance:.3f}m\n (does not measure depth), angle = {angle:.1f}deg"
        )

    def show_exception(self, e):
        self.give_feedback(e, style=1)

    def give_feedback(self, what, style=0):
        """Shows feedback in the feedback window and statusbar
        style 0 : normal
        style 1 : error
        """

        self.ui.teFeedback.setText(str(what))
        if style == 0:
            self.ui.teFeedback.setStyleSheet("background-color: white;")
            DAVE_GUI_LOGGER.log(f"Give feedback: {what}")
        elif style == 1:
            self.ui.teFeedback.setStyleSheet("background-color: pink;")
            DAVE_GUI_LOGGER.log(f"Give feedback error: {what}")

        self.statusbar.showMessage(str(what))

        if not self.ui.dockWidget_2.isVisible() and style == 1:
            tool_long = len(what) > 1000 or len(what.split("\n")) > 30

            short = what[-1000:]
            short = "\n".join(short.split("\n")[-30:])

            if tool_long:
                print(what)
                QMessageBox.warning(
                    self.ui.widget,
                    "error",
                    short
                    + "\n\n !!! first part omitted,\n see (python) console for full error message",
                    QMessageBox.Ok,
                )
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
        if isinstance(code, (list, tuple)):
            code = "\n".join(code)

        DAVE_GUI_LOGGER.log(f"Run code: {code}")

        self._model_has_changed = True

        before = self.scene._nodes.copy()

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

        DAVE_GUI_LOGGER.log_code(code)

        executed = False
        with capture_output() as c:
            try:
                glob_vars = globals()
                glob_vars.update(DAVE.settings.DAVE_ADDITIONAL_RUNTIME_MODULES)
                glob_vars["s"] = self.scene
                glob_vars["self"] = self

                exec(code, glob_vars)
                DAVE_GUI_LOGGER.log("Code executed successfully")
                executed = True

            except Exception as E:
                original_exception = E
                if isinstance(E, ModelInvalidException):
                    original_exception = E.args[0]

                if isinstance(original_exception, SyntaxError):
                    code_error = (
                        f"line {original_exception.lineno}: {original_exception.text}"
                    )

                else:
                    code_error = get_code_error(code)

                notes = getattr(original_exception, "__notes__", [])
                message = str(original_exception) + "\n".join(notes)
                if not message:
                    message = "Unknown error, traceback:\n" + traceback.format_exc()

                DAVE_GUI_LOGGER.log_exception(original_exception)

                DAVE_GUI_LOGGER.log_code("# Exception occurred: " + code_error)

                message = message + "\n\n" + code_error

                if isinstance(E, ModelInvalidException):  # It is serious
                    if store_undo:
                        QMessageBox.information(
                            self.ui.widget,
                            "Model invalid",
                            "The model state has become invalid due to an unrecoverable error. The error was:\n"
                            + message
                            + "\nWe will use the undo log to restore the model to the previous state.",
                            QMessageBox.Ok,
                        )
                        self.undo()
                    else:
                        # show an error box with error

                        # terminate the autosave, we do not want to be saving any invalid models

                        DAVE_GUI_LOGGER.log("Disabling autosave")
                        self._autosave = None  # no cleanup!

                        QMessageBox.warning(
                            self.ui.widget,
                            "terminal error",
                            "The model state has become invalid due to an unrecoverable error. The error was:\n"
                            + message
                            + "DO NOT SAVE. Advised to restart DAVE and continue with the latest auto-save file.",
                            QMessageBox.Ok,
                        )

                else:  # not so serious
                    self.show_exception(message)

            finally:
                self.ui.pbExecute.setStyleSheet("")
                self.ui.pbExecute.update()

            if executed:  # code ran as expected
                # Code was executed, so we can use the provided event and sender to
                # update the GUI

                if c.stdout:
                    self.give_feedback(c.stdout, style=0)
                else:
                    self.give_feedback(code, style=0)

                self.logcode(code)

                self.ui.teFeedback.verticalScrollBar().setValue(
                    self.ui.teFeedback.verticalScrollBar().maximum()
                )  # scroll down all the way

            # update selection

            # See if selected nodes are still valid and identical to the ones
            to_be_removed_from_selection = []
            for node in self.selected_nodes:
                if node not in self.scene._nodes:
                    to_be_removed_from_selection.append(node)

            for node in to_be_removed_from_selection:
                self.selected_nodes.remove(node)

            # if we created something new, then select it (or its manager)
            emitted = False
            for node in self.scene._nodes:
                if node not in before:
                    DAVE_GUI_LOGGER.log(f"New node detected: {node.name}")
                    logging.info(f"New node detected: {node.name}")

                    self.selected_nodes.clear()

                    node_to_be_selected = node
                    while node_to_be_selected.manager is not None:
                        node_to_be_selected = node_to_be_selected.manager

                    self.guiSelectNode(node_to_be_selected, new=True)
                    select_node_name_edit_field = True

                    emitted = True
                    break

            if event is not None:
                self.guiEmitEvent(event, sender=sender)

            if to_be_removed_from_selection and not emitted:
                self.guiEmitEvent(guiEventType.SELECTION_CHANGED, sender=sender)

            if select_node_name_edit_field:
                self.place_input_focus_on_name_of_node()

    def place_input_focus_on_name_of_node(self):
        """Places the input focus on the name of the node such that the user can directly change it if needed"""

        DAVE_GUI_LOGGER.log("Place input focus on name of node")

        if "Properties" in self.guiWidgets:
            props = self.guiWidgets["Properties"]
            props._node_name_editor.ui.tbName.setFocus()
            props._node_name_editor.ui.tbName.selectAll()

    def solve_statics(self, timeout_s=0.5, called_by_user=True):
        """Solves statics using the current scene"""
        DAVE_GUI_LOGGER.log("Solve statics")
        self.scene.solve_activity_desc = "Solving static equilibrium"

        self.solve_statics_using_gui_on_scene(
            scene_to_solve=self.scene,
            called_by_user=called_by_user,
        )

        if len(self.scene._vfc.get_dofs()) == 0:
            self.give_feedback("Solved statics - no degrees of freedom")
        else:
            self.give_feedback(
                f"Solved statics - remaining error = {self.scene._vfc.Emaxabs} kN or kNm"
            )

    def solve_statics_using_gui_on_scene(self, scene_to_solve, called_by_user=True):
        scene_to_solve.update()
        if scene_to_solve.verify_equilibrium():
            DAVE_GUI_LOGGER.log(
                "Solve statics using gui on scene - not solving, scene already converged"
            )
            if called_by_user:
                self.give_feedback(
                    f"Scene already converged with max(|E|) = {scene_to_solve._vfc.Emaxabs} kN or kNm"
                )
            return

        DAVE_GUI_LOGGER.log("Solve statics using gui on scene")

        if called_by_user:
            self.add_undo_point(undo_type=UndoType.SET_DOFS)

        old_dofs = scene_to_solve._vfc.get_dofs()

        if len(old_dofs) == 0:  # no degrees of freedom
            return True

        self._dialog = None

        start_time = datetime.datetime.now()

        D0 = self.scene._vfc.get_dofs()

        # Create the dialog and connect signals

        dialog = SolverDialog_threaded(parent=self.MainWindow)
        dialog.pbAccept.setEnabled(False)
        dialog.frame.setVisible(False)

        def show_settings(*args):
            dialog.frame.setVisible(True)

        dialog.pbShowControls.clicked.connect(show_settings)

        self.__solver_gui_do_terminate = False

        def terminate(*args):
            self.__solver_gui_do_terminate = True
            self.__BackgroundSolver.Stop()

            # restore original state
            self.scene._vfc.set_dofs(D0)
            self.visual.position_visuals()
            self.visual.refresh_embeded_view()

        def reset(*args):
            self.scene._vfc.set_dofs(D0)
            self.__BackgroundSolver.Stop()
            self.__BackgroundSolver = DAVEcore.BackgroundSolver(self.scene._vfc)
            self.scene.solver_settings.apply(self.__BackgroundSolver)
            self.__BackgroundSolver.Start()

        def accept(*args):
            dofs = self.__BackgroundSolver.DOFs
            self.__solver_gui_do_terminate = True
            self.__BackgroundSolver.Stop()
            if dofs:
                self.scene._vfc.set_dofs(dofs)

        def change_mobility(position, *args):
            self.__BackgroundSolver.mobility = position
            self.scene.solver_settings.mobility = position
            dialog.lbMobility.setText(f"{position}%")

        def change_do_linear_first(*args):
            self.scene.solver_settings.do_linear_first = (
                dialog.cbLinearFirst.isChecked()
            )

        # disable main window and prepare to start solving
        self.MainWindow.setEnabled(False)
        dialog_open = False

        # Start the solving sequence, continue until user cancels or we are done
        feedback_text_prefix = ""

        while True:  # keep trying after fixing orientations and such
            self.__BackgroundSolver = DAVEcore.BackgroundSolver(self.scene._vfc)

            self.scene.solver_settings.apply(self.__BackgroundSolver)

            running = self.__BackgroundSolver.Start()

            if running:
                while self.__BackgroundSolver.Running:
                    time_diff = datetime.datetime.now() - start_time
                    secs = time_diff.total_seconds()

                    dofs = self.__BackgroundSolver.DOFs
                    if dofs:
                        dialog.pbAccept.setEnabled(True)

                        text = feedback_text_prefix
                        if self.__BackgroundSolver.RunningLinear:
                            text = "Working on linear degrees of freedom only\n"
                        text += f"Error norm = {self.__BackgroundSolver.Enorm:.6e}\nError max-abs {self.__BackgroundSolver.Emaxabs:.6e}\nMaximum error at {self.__BackgroundSolver.Emaxabs_where}"
                        dialog.lbInfo.setText(text)

                        if secs > 0.5:  # else use animation
                            self.scene._vfc.set_dofs(dofs)
                            self.visual.position_visuals()
                            self.visual.refresh_embeded_view()

                    dialog.setWindowOpacity(
                        min(secs - 0.1, 1)
                    )  # fade in the window slowly

                    if secs > 0.1:  # and open only after 0.1 seconds
                        if not dialog_open:
                            # Connect signals/slots and show dialog

                            dialog.cbLinearFirst.setChecked(
                                self.scene.solver_settings.do_linear_first
                            )
                            dialog.cbLinearFirst.toggled.connect(change_do_linear_first)

                            dialog.mobilitySlider.valueChanged.connect(change_mobility)
                            dialog.mobilitySlider.setSliderPosition(
                                self.scene.solver_settings.mobility
                            )

                            dialog.pbReset.clicked.connect(reset)
                            dialog.pbAccept.clicked.connect(accept)

                            dialog.pbTerminate.clicked.connect(terminate)

                            dialog.show()
                            dialog_open = True

                    self.app.processEvents()

                if self.__BackgroundSolver.Converged:
                    dofs = self.__BackgroundSolver.DOFs
                    self.scene._vfc.set_dofs(dofs)
                    self.scene.update()
                    self.give_feedback(
                        f"Converged with Error norm = {self.__BackgroundSolver.Enorm} | max-abs {self.__BackgroundSolver.Emaxabs} in {self.__BackgroundSolver.Emaxabs_where}"
                    )

            if self.__solver_gui_do_terminate:
                result = False
                break  # <--- user exit

            # Check orientations
            (
                work_done,
                messages,
            ) = self.scene._check_and_fix_geometric_contact_orientations()

            if work_done:
                self.give_feedback(
                    f"Fixed {len(messages)} geometric contact orientations"
                )

                time_diff = datetime.datetime.now() - start_time
                secs = time_diff.total_seconds()

                # show in the dialog as well:
                if len(messages) > 3:
                    feedback_text_prefix = f"Fixed {len(messages)} geometric contact orientations at T = {secs:.1f}s\n"
                else:
                    temp = "\n".join(messages)
                    feedback_text_prefix = f"{temp}\n  at T = {secs:.1f}s\n"

                dialog.lbInfo.setText(feedback_text_prefix)

                dialog.setWindowOpacity(min(secs - 0.1, 1))  # fade in the window slowly

                if secs > 0.1:  # and open only after 0.1 seconds
                    if not dialog_open:
                        dialog.show()
                        dialog_open = True

                self.visual.position_visuals()
                self.visual.refresh_embeded_view()
                self.app.processEvents()

                if not dialog_open:
                    # Connect signals/slots and show dialog

                    dialog.cbLinearFirst.setChecked(
                        self.scene.solver_settings.do_linear_first
                    )
                    dialog.cbLinearFirst.toggled.connect(change_do_linear_first)

                    dialog.mobilitySlider.valueChanged.connect(change_mobility)
                    dialog.mobilitySlider.setSliderPosition(
                        self.scene.solver_settings.mobility
                    )

                    dialog.pbReset.clicked.connect(reset)
                    dialog.pbAccept.clicked.connect(accept)

                    dialog.pbTerminate.clicked.connect(terminate)

                    dialog.show()
                    dialog_open = True

            else:
                result = True  # <-- took the proper exit
                break

        if dialog_open:
            dialog.close()

        self.MainWindow.setEnabled(True)

        # Animate if little time has passed
        time_diff = datetime.datetime.now() - start_time
        secs = time_diff.total_seconds()
        if secs < 0.5:
            if GUI_DO_ANIMATE and called_by_user:
                new_dofs = scene_to_solve._vfc.get_dofs()
                self.animate_change(D0, new_dofs, 10)

        if called_by_user:
            self.guiEmitEvent(guiEventType.MODEL_STATE_CHANGED)
            self._codelog.append("s.solve_statics()")

        return result

    def animate_change(self, old_dof, new_dof, n_steps):
        """Animates from old_dof to new_dofs in n_steps"""

        DAVE_GUI_LOGGER.log("Animate change")

        if len(old_dof) != len(new_dof):
            return

        dt = GUI_SOLVER_ANIMATION_DURATION / n_steps

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

    def get_folder_for_dialogs(self) -> Path:
        """Returns a logical dir to save to, used as starting point for the dialogs"""
        if self.scene.current_directory is not None:
            return self.scene.current_directory

        if self.modelfilename is not None:
            return Path(self.modelfilename).parent

        try:
            if self.scene.resource_provider.resources_paths[-1]:
                return Path(self.scene.resource_provider.resources_paths[-1])
        except:
            pass

        return Path.cwd()

    def to_csv(self):
        """Exports the current model to csv"""
        DAVE_GUI_LOGGER.log("To csv")
        filename, _ = QFileDialog.getSaveFileName(
            filter="*.csv",
            caption="Export points to csv",
            dir=str(self.get_folder_for_dialogs()),
        )
        if filename:
            self.scene.export_points_to_csv(filename)

    def to_blender(self):
        """Exports the current model to blender"""
        DAVE_GUI_LOGGER.log("To blender")
        if self.animation_running():
            dofs = []

            n_frames = np.round(self._animation_length)
            for t in np.linspace(0, self._animation_length, int(n_frames)):
                dofs.append(self._animation_keyframe_interpolation_object(t))

        else:
            dofs = None
        #
        # create_blend_and_open(
        #     self.scene, animation_dofs=dofs, wavefield=self.visual._wavefield
        # )
        if getattr(self, "blender_dialog", None) is None:
            self.blender_dialog = ExportToBlenderDialog()

        self.blender_dialog.show(
            self.scene, animation_dofs=dofs, wavefield=self.visual._wavefield
        )

    def toggle_show_sea(self):
        """Toggles the visibility of the sea-plane"""
        DAVE_GUI_LOGGER.log("Toggle show sea")
        self.visual.settings.show_sea = not self.visual.settings.show_sea
        self.ui.actionShow_water_plane.setChecked(self.visual.settings.show_sea)
        self.ui.btnWater.setChecked(self.visual.settings.show_sea)
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def toggle_show_origin(self):
        """Toggles the visibility of the origin"""
        DAVE_GUI_LOGGER.log("Toggle show origin")
        self.visual.settings.show_origin = not self.visual.settings.show_origin
        self.ui.actionShow_origin.setChecked(self.visual.settings.show_origin)
        self.ui.pbOrigin.setChecked(self.visual.settings.show_origin)
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def toggle_show_UC(self):
        """Toggles the visibility of the UC colors"""
        DAVE_GUI_LOGGER.log("Toggle show UC")
        self.visual.settings.paint_uc = not self.visual.settings.paint_uc

        self.ui.pbUC.setChecked(self.visual.settings.paint_uc)
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def toggle_show_force_applying_elements(self):
        """Toggles the visibility of the force applying elements"""
        DAVE_GUI_LOGGER.log("Toggle show force applying elements")
        self.visual.show_meshes = self.ui.actionShow_force_applying_element.isChecked()
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def camera_set_direction(self, vector):
        """Sets the camera direction"""
        DAVE_GUI_LOGGER.log(f"Camera set direction {vector}")
        self.visual.Style.SetCameraPlaneDirection(vector)
        self.guiEmitEvent(guiEventType.VIEWER_SETTINGS_UPDATE)

    def camera_reset(self):
        """Resets the camera"""
        DAVE_GUI_LOGGER.log("Camera reset")
        self.visual.zoom_all()  # this function takes care of ignoring the sea-plane
        # self.visual.Style.ZoomFit()
        # self.visual.refresh_embeded_view()

    def toggle_SSAO(self):
        """Toggles SSAO"""
        DAVE_GUI_LOGGER.log("Toggle SSAO")
        if self.ui.btnSSAO.isChecked():
            self.visual.EnableSSAO()
        else:
            self.visual.DisableSSAO()
        self.visual.refresh_embeded_view()

    def clear(self):
        """Clears the scene"""
        DAVE_GUI_LOGGER.log("Clear")
        self.run_code("s.clear()", guiEventType.FULL_UPDATE, store_undo=False)
        self._model_has_changed = False
        self.modelfilename = None
        self.MainWindow.setWindowTitle(f"DAVE [unnamed scene]")

    def open_file(self, filename: str or Path):
        """Opens the provided file"""
        DAVE_GUI_LOGGER.log(f"Open file {filename}")

        if str(filename).endswith(".zip"):
            if self.open_self_contained_DAVE_package(filename=filename):
                return

        current_directory = Path(filename).parent
        code = f's.clear()\ns.current_directory = r"{current_directory}"\ns.load_scene(r"{filename}")'

        store = gui_globals.do_ask_user_for_unavailable_nodenames
        gui_globals.do_ask_user_for_unavailable_nodenames = True

        try:
            self.run_code(code, guiEventType.FULL_UPDATE)
        except:
            self._model_has_changed = False
            self.modelfilename = None
            self.MainWindow.setWindowTitle(
                f"DAVE - Error during load ; partially loaded model"
            )

            self.show_exception(
                "DAVE - Error during load ; partially loaded model - continue at own risk. Advised to undo or do file -> new"
            )
            self.guiEmitEvent(guiEventType.FULL_UPDATE)
        else:
            self.modelfilename = filename

            name_and_ext = str(Path(filename).name)

            self._model_has_changed = False
            self.MainWindow.setWindowTitle(
                f"DAVE [{str(self.scene.current_directory)}] - {name_and_ext} "
            )
            self.add_to_recent_file_menu(filename)

            self.visual.zoom_all()

        finally:
            gui_globals.do_ask_user_for_unavailable_nodenames = store

    def _get_filename_using_dialog(self):
        folder = self.get_folder_for_dialogs()
        filename, _ = QFileDialog.getOpenFileName(
            filter="*.dave", caption="DAVE models", dir=str(folder)
        )

        return filename

    def open_self_contained_DAVE_package_gui(self, *args):
        """Opens a self-contained DAVE package"""

        folder = self.get_folder_for_dialogs()
        filename, _ = QFileDialog.getOpenFileName(
            filter="*.zip", caption="DAVE model package", dir=str(folder)
        )

        if filename:
            self.open_self_contained_DAVE_package(filename)

    def open_self_contained_DAVE_package(self, filename=None):
        """Opens a self-contained DAVE package"""
        DAVE_GUI_LOGGER.log("Open self contained DAVE package")

        store = gui_globals.do_ask_user_for_unavailable_nodenames
        try:
            gui_globals.do_ask_user_for_unavailable_nodenames = True

            # extract the zip file (filename) to a temporary folder
            temp_folder = tempfile.mkdtemp()
            with zipfile.ZipFile(filename, "r") as zip_ref:
                zip_ref.extractall(temp_folder)

            name = Path(filename).stem
            name = str(name) + ".dave"

            model_file = Path(temp_folder) / name

            # check if the file exists
            if not model_file.exists():
                self.show_exception(
                    f"The DAVE zip package is expected to contain a file \n\n{name}\n\n (= the name of the .zip file without zip)\nHowever a file with this name not found.\n\nPlease check the contents of the zip and rename the package file if needed."
                )
                return

            self.scene.load_package(model_file)

        except Exception as e:
            self.show_exception(
                f"Could not load DAVE package because {e} - partial model load, continue at own risk"
            )

        else:
            self._model_has_changed = False
            self.MainWindow.setWindowTitle(
                f"DAVE [{str(self.scene.current_directory)}] - {filename} "
            )
            self.add_to_recent_file_menu(filename)

            self.guiEmitEvent(guiEventType.FULL_UPDATE)

            self.visual.zoom_all()
            return True
        finally:
            gui_globals.do_ask_user_for_unavailable_nodenames = store

    def open(self):
        """Opens a file"""
        DAVE_GUI_LOGGER.log("Open")
        filename = self._get_filename_using_dialog()
        if filename:
            self.open_file(filename)

    def menu_import(self):
        """Imports a file"""
        DAVE_GUI_LOGGER.log("Menu import")
        filename = self._get_filename_using_dialog()

        if filename:
            code = 's.import_scene(r"{}")'.format(filename)
            self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)
            self.visual.update_visibility()

    def menu_save_model(self):
        """Saves the model"""
        DAVE_GUI_LOGGER.log("Menu save model")
        if self.modelfilename is None:
            self.menu_save_model_as()
            return

        code = 's.save_scene(r"{}")'.format(self.modelfilename)
        self.run_code(code, guiEventType.NOTHING)
        self._model_has_changed = False
        self.give_feedback(f"File saved: [{self.modelfilename}]")

    def menu_save_model_as(self):
        """Saves the model as"""
        DAVE_GUI_LOGGER.log("Menu save model as")

        dir = str(self.get_folder_for_dialogs())

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
            self.MainWindow.setWindowTitle(f"DAVE [{self.modelfilename}]")

            self.add_to_recent_file_menu(filename)

    def maybeSave(self):
        """Asks the user if he wants to save the model"""
        DAVE_GUI_LOGGER.log("Maybe save")
        if not self._model_has_changed:
            return True

        ret = QMessageBox.question(
            self.MainWindow,
            "Message",
            "<h4><p>The scene has unsaved changes.</p>\n"
            "<p>Do you want to save changes?</p></h4>",
            QMessageBox.Yes | QMessageBox.Discard | QMessageBox.Cancel,
        )

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
        """Exports the model to an orcaflex .yml file"""
        DAVE_GUI_LOGGER.log("Menu export orcaflex yml")

        filename, _ = QFileDialog.getSaveFileName(
            filter="*.yml",
            caption="Orcaflex .yml file",
            dir=str(self.get_folder_for_dialogs()),
        )
        if filename:
            code = 'from DAVE.io.orcaflex import export_ofx_yml\nexport_ofx_yml(s,r"{}")'.format(
                filename
            )
            self.run_code(code, guiEventType.NOTHING)

    def menu_export_orcaflex_package(self):
        """Exports the model to an orcaflex package"""
        DAVE_GUI_LOGGER.log("Menu export orcaflex package")
        filename, _ = QFileDialog.getSaveFileName(
            filter="*.py",
            caption="Python files",
            dir=str(self.get_folder_for_dialogs()),
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
        """Tidies the history"""
        DAVE_GUI_LOGGER.log("Tidy history")
        self.ui.teHistory.setText(self.give_clean_history())

    def give_clean_history(self):
        """Returns a clean history"""
        DAVE_GUI_LOGGER.log("Give clean history")
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
        """Saves the actions"""
        DAVE_GUI_LOGGER.log("Menu save actions")
        filename, _ = QFileDialog.getSaveFileName(
            filter="*.dave",
            caption="Scene files",
            dir=str(self.get_folder_for_dialogs()),
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
        """Copies feedback to clipboard"""
        DAVE_GUI_LOGGER.log("Feedback copy")
        self.app.clipboard().setText(self.ui.teFeedback.toPlainText())

    def history_copy(self):
        """Copies history to clipboard"""
        DAVE_GUI_LOGGER.log("History copy")
        self.app.clipboard().setText(self.ui.teHistory.toPlainText())

    def clear_code(self):
        """Clears the code"""
        DAVE_GUI_LOGGER.log("Clear code and set-focus")
        self.ui.teCode.clear()
        self.ui.teCode.setFocus()

    def generate_scene_code(self):
        """Generates the scene code"""
        DAVE_GUI_LOGGER.log("Generate scene code")
        self.ui.teFeedback.setText(self.scene.give_python_code())

    def run_code_in_teCode(self):
        """Runs the code in the teCode"""
        DAVE_GUI_LOGGER.log("Run code in teCode")
        code = self.ui.teCode.toPlainText()
        self.run_code(code, guiEventType.FULL_UPDATE)

    def rightClickViewport(self, point):
        """Executed when the viewport is right-clicked"""
        DAVE_GUI_LOGGER.log("Right click viewport")
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
        """Opens the context menu at the provided location"""
        DAVE_GUI_LOGGER.log(f"Open context menu at {node_name} {globLoc}")
        main_window = self.MainWindow
        menu = QtWidgets.QMenu(main_window)

        if node_name is not None:
            node = self.scene[node_name]

            if node._manager is None:
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

                action = QAction("Delete {}".format(node_name), menu)
                action.triggered.connect(delete)
                action.setIcon(QIcon(":/v2/icons/delete.svg"))
                menu.addAction(action)

                action = QAction("Dissolve (Evaporate) {}".format(node_name), menu)
                action.triggered.connect(dissolve)
                action.setIcon(QIcon(":/v2/icons/explode.svg"))
                menu.addAction(action)

                menu.addSeparator()

                def copy_python_code():
                    code = self.scene[node_name].give_python_code()
                    print(code)
                    self.app.clipboard().setText(code)

                action = QAction("Copy python code", menu)
                action.triggered.connect(copy_python_code)
                action.setIcon(QIcon(":/v2/icons/python_code.svg"))
                menu.addAction(action)
                menu.addSeparator()

                def duplicate():
                    code = f"s.duplicate_node('{node_name}')"
                    self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

                def duplicate_branch():
                    code = f"s.duplicate_branch('{node_name}')"
                    self.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

                action = QAction("Duplicate node", menu)
                action.triggered.connect(duplicate)
                action.setIcon(QIcon(":/v2/icons/copy.svg"))
                menu.addAction(action)

                if isinstance(node, (Frame, Point)):
                    if self.scene.nodes_with_parent(node):
                        action = QAction("Duplicate branch", menu)
                        action.triggered.connect(duplicate_branch)
                        action.setIcon(QIcon(":/v2/icons/copy_branch.svg"))
                        menu.addAction(action)

                if type(node) == RigidBody:
                    action = QAction("Downgrade Body --> Frame", menu)
                    action.triggered.connect(
                        lambda *args: self.run_code(
                            f"s.to_frame(s['{node.name}'])",
                            guiEventType.MODEL_STRUCTURE_CHANGED,
                        ),
                    )
                    action.setIcon(QIcon(":/v2/icons/axis.svg"))
                    menu.addAction(action)

                if type(node) == Frame:
                    actionUpgrade = QAction("Upgrade Frame --> Body", menu)
                    actionUpgrade.triggered.connect(
                        lambda *args: self.run_code(
                            f"s.to_rigidbody(s['{node.name}'])",
                            guiEventType.MODEL_STRUCTURE_CHANGED,
                        )
                    )
                    menu.addAction(actionUpgrade)
                    actionUpgrade.setIcon(QIcon(":/v2/icons/box.svg"))

                if isinstance(node, Frame):
                    action = QAction("Insert Frame before", menu)
                    action.triggered.connect(
                        lambda *args: self.run_code(
                            f"s.insert_frame_before(s['{node.name}'])",
                            guiEventType.MODEL_STRUCTURE_CHANGED,
                        )
                    )
                    action.setIcon(QIcon(":/v2/icons/add_before.svg"))
                    menu.addAction(action)

                if isinstance(node, (Frame, Point)):
                    if node.parent is not None:
                        actionMakeGlobal = QAction("Make global (no parent)", menu)
                        actionMakeGlobal.triggered.connect(
                            lambda *args: self.run_code(
                                f"s['{node.name}'].change_parent_to(None)",
                                guiEventType.MODEL_STRUCTURE_CHANGED,
                            )
                        )
                        actionMakeGlobal.setIcon(QIcon(":/v2/icons/to_global.svg"))
                        menu.addAction(actionMakeGlobal)

                menu.addSeparator()

        wa = QtWidgets.QWidgetAction(menu)

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
        # ui.pbSling.clicked.connect(self.new_sling)
        ui.pbShackle.clicked.connect(self.new_shackle)
        ui.pbBeam.clicked.connect(self.new_beam)

        ui.pbVisual.clicked.connect(self.new_visual)
        ui.pbComponent.clicked.connect(self.new_component)

        menu.addAction(wa)

        for plugin in self.plugins_context:
            try:
                plugin(menu, node_name, self)
            except Exception as E:
                warnings.warn("Context menu plugin errored: {}".format(E))

        menu.exec(globLoc)

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
        """Creates something new"""
        DAVE_GUI_LOGGER.log(f"New something {what}")
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

        DAVE_GUI_LOGGER.log(f"View3d select element")

        # if self._read_only_mode:
        #     return

        nodes = [self.visual.node_from_vtk_actor(prop) for prop in props]
        nodes = [
            node for node in nodes if node is not None
        ]  # remove nones (not all actors have an associated node, for example the sea has none)
        nodes = list(set(nodes))  # make unique

        # find all managers (recursively)
        added = True
        while added:
            added = False
            for node in tuple(nodes):
                if node.manager is not None:
                    if node.manager not in nodes:
                        nodes.append(node.manager)
                        added = True

        added = True
        while added:
            added = False
            for node in tuple(nodes):
                parent = getattr(node, "parent", None)
                if parent:
                    if parent not in nodes:
                        nodes.append(parent)
                        added = True

        # We now have a list of all nodes that the user may want to select.
        # If we have a length 1 then it is easy
        # if more, then show a context-menu

        # Even with length 1, we may still want to show a context menu such that
        # the user can drag the selected node to somewhere.
        # Implement by checking if the SHIFT, ALT or CTRL keys are down
        # If so, show the context menu

        if self.app.keyboardModifiers() and (
            QtCore.Qt.KeyboardModifier.ControlModifier
            or QtCore.Qt.KeyboardModifier.AltModifier
            or QtCore.Qt.KeyboardModifier.ShiftModifier
        ):
            pass
        else:
            if len(nodes) == 1:
                self._user_clicked_node(nodes[0])
                return

        # order in some logical way
        # unmanaged nodes go first

        i = 0
        for _ in range(len(nodes)):
            if nodes[i].manager is not None:
                nodes.append(nodes.pop(i))  # move to end
            else:
                i += 1

        # group by node class

        # See if there are multiple nodes with the same class
        # if so, offer a menu option to select all of them
        # maintain order as in nodes

        class_names = []
        for node in nodes:
            if node.class_name not in class_names:
                class_names.append(node.class_name)

        menu = QtWidgets.QMenu()
        actions = []  # keep alive

        for class_name in class_names:
            print(f"{class_name}")
            nodes_with_class = tuple(
                [node for node in nodes if node.class_name == class_name]
            )

            try:
                icon = ICONS[type(nodes_with_class[0])]
            except KeyError:
                DAVE_GUI_LOGGER.log(
                    "ERROR: No icon found for {}".format(type(nodes_with_class[0]))
                )
                icon = QIcon(":/icons/redball.png")

            if len(nodes_with_class) > 1:
                action = menu.addAction(
                    f"------ {class_name}s ------",
                    lambda nodes=nodes_with_class, *args: self.guiSelectNodes(nodes),
                )
                action.setIcon(icon)

            for node in nodes_with_class:
                text = node.name

                if node.manager is None:
                    right_text = ""
                else:
                    right_text = f"{node.manager.name}"

                action = QDraggableNodeActionWidget(
                    text, mime_text=node.name, right_text=right_text, icon=icon
                )
                action.clicked.connect(
                    lambda n=node, *args: self._user_clicked_node(n, args)
                )

                actions.append(action)

                print(f"adding {text}")
                menu.addAction(action)

                if node.manager is None:
                    action.setBold(True)
                else:
                    if (
                        getattr(node, "_editor_widget_types_when_managed", None)
                        is not None
                        or getattr(node, "_always_show_in_tree", None) is not None
                    ):  # for partially managed nodes
                        action.setBold(True)

        menu.exec(QCursor.pos())

    def _user_clicked_node(self, node, event=None):
        DAVE_GUI_LOGGER.log(f"User clicked node {node}")

        if node is None:  # sea or something
            self.selected_nodes.clear()
            self.guiEmitEvent(guiEventType.SELECTION_CHANGED)
        elif node in self.selected_nodes:
            self.selected_nodes.remove(node)
            self.guiEmitEvent(guiEventType.SELECTION_CHANGED)
        else:
            self.guiSelectNode(node.name)

    def visual_update_selection(self):
        """Updates the _is_selected and _is_sub_selected properties of the visuals, then re-applies paint"""

        DAVE_GUI_LOGGER.log("Visual update selection")

        visually_selected_nodes = self.selected_nodes.copy()

        for node in self.selected_nodes:
            if isinstance(node, Manager):
                visually_selected_nodes.extend(
                    self.scene.nodes_managed_by(node, recursive=True)
                )

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

    def guiEmitEvent(self, event: guiEventType, sender=None, execute_now: bool = False):
        """Emits the given event to all widgets and the visual, and updates the visual as well.

        If sender is provided, then the event is not send to the sender.

        By default this is not executed directly but placed at the end of the event que.
        This prevents update from removing gui widgets that are still in use.
        (the nasty bug with the "reversed" checkboxes in the ConnectionsEditor widget)
        To execute directly, set execute_now to True.


        """
        if not execute_now:
            # make a single-shot timer to emit the event
            DAVE_GUI_LOGGER.log(f"Gui emit event {event} from {sender} placed in que")
            QTimer.singleShot(
                0, lambda: self.guiEmitEvent(event, sender, execute_now=True)
            )
            return

        DAVE_GUI_LOGGER.log(f"Gui emit event {event} from {sender}")

        # Bring the properties editor to front if needed
        if event in (guiEventType.SELECTION_CHANGED, guiEventType.NEW_NODE_ADDED):
            if self.selected_nodes:
                if self._active_dockgroup is not None:
                    if self._active_dockgroup.show_edit:
                        dock_show(
                            self.dock_manager,
                            self.guiWidgets["Properties"],
                            force_bring_to_front=(event == guiEventType.NEW_NODE_ADDED),
                        )

        # update warnings if needed
        if event in (
            guiEventType.FULL_UPDATE,
            guiEventType.MODEL_STRUCTURE_CHANGED,
            guiEventType.MODEL_STEP_ACTIVATED,
            guiEventType.NEW_NODE_ADDED,
            guiEventType.MODEL_STATE_CHANGED,
            guiEventType.SELECTED_NODE_MODIFIED,
        ):
            self.update_warnings()

        with DelayRenderingTillDone(
            self.visual
        ):  # temporary freezes rendering and calls update afterwards
            # update the model if needed - before updating the docks - so that the docks can use the updated model
            if event in (
                guiEventType.MODEL_STATE_CHANGED,
                guiEventType.FULL_UPDATE,
                guiEventType.MODEL_STRUCTURE_CHANGED,
                guiEventType.MODEL_STEP_ACTIVATED,
                guiEventType.SELECTED_NODE_MODIFIED,  # weight or shape has change
                guiEventType.ENVIRONMENT_CHANGED,
                guiEventType.NEW_NODE_ADDED,
            ):
                self.scene.update()

            if self.animation_running():
                self.visual.position_visuals()

                return  # do not update the widgets when an animation is running

            for widget in self.guiWidgets.values():
                if not (widget is sender):
                    if not widget.isClosed():
                        widget.guiEvent(event)

            # update the visual as well
            if event in (guiEventType.SELECTION_CHANGED, guiEventType.NEW_NODE_ADDED):
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

    def guiSelectNodes(self, nodes):
        """Replace or extend the current selection with the given nodes (depending on keyboard-modifiers). Nodes may be passed as strings or nodes, but must be an tuple or list."""

        DAVE_GUI_LOGGER.log(f"Gui select nodes {nodes}")

        assert isinstance(
            nodes, (tuple, list)
        ), f"Nodes must be an iterable, but is {type(nodes)}"

        nodes = [self.scene._node_from_node_or_str(node) for node in nodes]
        last_node = nodes[-1]
        first_nodes = nodes[:-1]

        if not (
            self.app.keyboardModifiers() and QtCore.Qt.KeyboardModifier.ControlModifier
        ):
            self.selected_nodes.clear()

        self.selected_nodes.extend(first_nodes)
        self.guiSelectNode(last_node, extend=True)

    def guiSelectNode(self, node_name, extend=False, new=False, execute_now=False):
        # Select a node with name, pass None to deselect all

        DAVE_GUI_LOGGER.log(f"Gui select node {node_name} extend {extend} new {new}")

        old_selection = self.selected_nodes.copy()

        if not (
            (
                self.app.keyboardModifiers()
                and QtCore.Qt.KeyboardModifier.ControlModifier
            )
            or extend
        ):
            self.selected_nodes.clear()

        node = None
        if node_name is not None:
            node = self.scene._node_from_node_or_str(node_name)
            if node not in self.selected_nodes:
                self.selected_nodes.append(node)

        if new:
            self.guiEmitEvent(guiEventType.NEW_NODE_ADDED, execute_now=execute_now)

        if old_selection != self.selected_nodes:
            self.guiEmitEvent(guiEventType.SELECTION_CHANGED, execute_now=execute_now)

    def get_dock(self, name, send_full_update=True):
        """Returns a reference to a dock instance,
        creates the instance if needed"""

        DAVE_GUI_LOGGER.log(f"Get dock {name}")

        if name not in DAVE_GUI_DOCKS:
            print(DAVE_GUI_DOCKS.keys())
            raise ValueError(
                f"Can not activate dock with name {name}, available names are {DAVE_GUI_DOCKS.keys()}"
            )

        widgetClass = DAVE_GUI_DOCKS[name]

        if name in self.guiWidgets:
            # dock already exists
            return self.guiWidgets[name]

        print("Creating {}".format(name))

        d = widgetClass(name=name, parent=self.MainWindow)
        d.guiScene = self.scene
        d.guiEmitEvent = self.guiEmitEvent
        d.guiRunCodeCallback = self.run_code
        d.guiSelectNode = self.guiSelectNode
        d.guiSelection = self.selected_nodes
        d.guiPressSolveButton = self.solve_statics
        d.gui = self

        self.guiWidgets[name] = d

        if send_full_update:
            d.guiProcessEvent(guiEventType.FULL_UPDATE)

        location = d.guiDefaultLocation()
        can_share_location = d.guiCanShareLocation()

        # Add floating
        if location is None:
            self.dock_manager.addDockWidget(
                PySide6QtAds.DockWidgetArea.LeftDockWidgetArea, d
            )
            d.setFloating()
            return d

        # Add docked
        #

        assert isinstance(
            location, PySide6QtAds.DockWidgetArea
        ), f"Wrong type of position returned by dock {name} - should be something like PySide6QtAds.DockWidgetArea.LeftDockWidgetArea"

        # Docks can be added to the left, right, top or bottom
        # but also to already existing docks.
        #
        # If a dock is wanted at the left, then there are two options:
        #  - above/below an already existing dock on the left
        #  - next to an already existing dock on the left
        #
        # Same for right

        if can_share_location:
            # For top or bottom, share with the central widget
            if location in (
                PySide6QtAds.DockWidgetArea.BottomDockWidgetArea,
                PySide6QtAds.DockWidgetArea.TopDockWidgetArea,
            ):
                self.dock_manager.addDockWidget(
                    location,
                    d,
                    self.dock_manager.centralWidget().dockAreaWidget(),
                )
                return d

            # see if there is already a dock in the same location
            # if so, add to that one
            for dock in self.dock_manager.dockWidgets():
                if not isinstance(dock, guiDockWidget):
                    continue

                if dock.guiDefaultLocation() == location and dock.guiCanShareLocation():
                    self.dock_manager.addDockWidget(
                        PySide6QtAds.DockWidgetArea.BottomDockWidgetArea,
                        d,
                        dock.dockAreaWidget(),
                    )

                    return d

        # if we get here, then we need to create a new dock area
        self.dock_manager.addDockWidget(location, d)

        return d

    def refresh_3dview(self):
        """Refreshes the 3d view"""
        DAVE_GUI_LOGGER.log("Refresh 3d view")
        self.visual.refresh_embeded_view()

    # --- dragging actors ---

    def start_node_drag(self):
        """Start node drag in viewport
        Actual selection shall be a single node
        That single node shall be movable (extends Frame, Point, Visual)
        """

        DAVE_GUI_LOGGER.log("Start node drag (grab)")

        # only works on one node
        if len(self.selected_nodes) != 1:
            self.give_feedback(
                f"Can not start drag - number of selected nodes should be exactly 1 but is {len(self.selected_nodes)}",
                style=1,
            )
            return

        node = self.selected_nodes[0]

        nodes = [node]

        while True:
            if isinstance(node, (Frame, Point)):
                self._dragged_node = node
                logging.info(f"Starting drag on {node.name}")

                # Find all nodes that are rigidly connected to this node
                # and add them to the drag list

                for n in self.scene.nodes_with_parent(node, recursive=True):
                    if n not in nodes:
                        nodes.append(n)

                self.visual.initialize_node_drag(
                    nodes, text_info=f"Moving node {node.name}"
                )
                break

            parent = getattr(node, "parent", None)

            if parent is None:
                break

            node = node.parent
            nodes.append(node)

    def node_dragged(self, info: DragInfo):  # callback from self.visual.Style
        """Apply the translation of the dragged node"""

        DAVE_GUI_LOGGER.log(f"Node dragged {info}")

        try:
            node = self._dragged_node
            old_position = np.array(node.global_position)
            new_position = old_position + info.delta
        except:
            self.show_exception("error during move - sorry")
            return

        code = f"s['{node.name}'].global_position = ({new_position[0]:.3f},{new_position[1]:.3f},{new_position[2]:.3f})"
        self.run_code(code, guiEventType.MODEL_STATE_CHANGED, store_undo=True)
