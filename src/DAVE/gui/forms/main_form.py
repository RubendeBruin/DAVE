# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDockWidget,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
import DAVE.gui.forms.resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1099, 819)
        MainWindow.setAcceptDrops(True)
        icon = QIcon()
        icon.addFile(":/icons/Dave_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.actionSave_scene = QAction(MainWindow)
        self.actionSave_scene.setObjectName("actionSave_scene")
        self.actionImport_sub_scene = QAction(MainWindow)
        self.actionImport_sub_scene.setObjectName("actionImport_sub_scene")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionHorizontal_camera = QAction(MainWindow)
        self.actionHorizontal_camera.setObjectName("actionHorizontal_camera")
        self.action = QAction(MainWindow)
        self.action.setObjectName("action")
        self.action2D_mode = QAction(MainWindow)
        self.action2D_mode.setObjectName("action2D_mode")
        self.action2D_mode.setCheckable(True)
        self.actionDark_mode = QAction(MainWindow)
        self.actionDark_mode.setObjectName("actionDark_mode")
        self.actionDark_mode.setCheckable(False)
        self.actionShow_visuals = QAction(MainWindow)
        self.actionShow_visuals.setObjectName("actionShow_visuals")
        self.actionShow_visuals.setCheckable(True)
        self.actionShow_visuals.setChecked(True)
        self.actionShow_Geometry_elements = QAction(MainWindow)
        self.actionShow_Geometry_elements.setObjectName("actionShow_Geometry_elements")
        self.actionShow_Geometry_elements.setCheckable(True)
        self.actionShow_Geometry_elements.setChecked(True)
        self.actionShow_force_applying_element = QAction(MainWindow)
        self.actionShow_force_applying_element.setObjectName(
            "actionShow_force_applying_element"
        )
        self.actionShow_force_applying_element.setCheckable(True)
        self.actionShow_force_applying_element.setChecked(True)
        self.actionSet_all_visible = QAction(MainWindow)
        self.actionSet_all_visible.setObjectName("actionSet_all_visible")
        self.actionSet_all_hidden = QAction(MainWindow)
        self.actionSet_all_hidden.setObjectName("actionSet_all_hidden")
        self.actionFull_refresh = QAction(MainWindow)
        self.actionFull_refresh.setObjectName("actionFull_refresh")
        self.actionShow_water_plane = QAction(MainWindow)
        self.actionShow_water_plane.setObjectName("actionShow_water_plane")
        self.actionShow_water_plane.setCheckable(True)
        self.actionShow_water_plane.setChecked(False)
        self.actionAdd_light = QAction(MainWindow)
        self.actionAdd_light.setObjectName("actionAdd_light")
        self.actionShow_all_forces_at_same_size = QAction(MainWindow)
        self.actionShow_all_forces_at_same_size.setObjectName(
            "actionShow_all_forces_at_same_size"
        )
        self.actionShow_all_forces_at_same_size.setCheckable(True)
        self.actionShow_all_forces_at_same_size.setChecked(True)
        self.actionIncrease_force_size = QAction(MainWindow)
        self.actionIncrease_force_size.setObjectName("actionIncrease_force_size")
        self.actionDecrease_force_size = QAction(MainWindow)
        self.actionDecrease_force_size.setObjectName("actionDecrease_force_size")
        self.actionIncrease_Geometry_size = QAction(MainWindow)
        self.actionIncrease_Geometry_size.setObjectName("actionIncrease_Geometry_size")
        self.actionDecrease_Geometry_size = QAction(MainWindow)
        self.actionDecrease_Geometry_size.setObjectName("actionDecrease_Geometry_size")
        self.actionPython_console = QAction(MainWindow)
        self.actionPython_console.setObjectName("actionPython_console")
        self.actionGoal_seek = QAction(MainWindow)
        self.actionGoal_seek.setObjectName("actionGoal_seek")
        self.actionStability_curve = QAction(MainWindow)
        self.actionStability_curve.setObjectName("actionStability_curve")
        self.actionOptimize = QAction(MainWindow)
        self.actionOptimize.setObjectName("actionOptimize")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionImport_browser = QAction(MainWindow)
        self.actionImport_browser.setObjectName("actionImport_browser")
        self.actionRender_current_view = QAction(MainWindow)
        self.actionRender_current_view.setObjectName("actionRender_current_view")
        self.actionModal_shapes = QAction(MainWindow)
        self.actionModal_shapes.setObjectName("actionModal_shapes")
        self.actionInertia_properties = QAction(MainWindow)
        self.actionInertia_properties.setObjectName("actionInertia_properties")
        self.actionSave_actions_as = QAction(MainWindow)
        self.actionSave_actions_as.setObjectName("actionSave_actions_as")
        self.actionsee_open_ocean_org = QAction(MainWindow)
        self.actionsee_open_ocean_org.setObjectName("actionsee_open_ocean_org")
        self.actionX = QAction(MainWindow)
        self.actionX.setObjectName("actionX")
        self.action_x = QAction(MainWindow)
        self.action_x.setObjectName("action_x")
        self.actionY = QAction(MainWindow)
        self.actionY.setObjectName("actionY")
        self.action_Y = QAction(MainWindow)
        self.action_Y.setObjectName("action_Y")
        self.actionZ = QAction(MainWindow)
        self.actionZ.setObjectName("actionZ")
        self.action_Z = QAction(MainWindow)
        self.action_Z.setObjectName("action_Z")
        self.actionLook_towards_center = QAction(MainWindow)
        self.actionLook_towards_center.setObjectName("actionLook_towards_center")
        self.actionCamera_reset = QAction(MainWindow)
        self.actionCamera_reset.setObjectName("actionCamera_reset")
        self.actionShow_CoG_positions = QAction(MainWindow)
        self.actionShow_CoG_positions.setObjectName("actionShow_CoG_positions")
        self.actionBlender = QAction(MainWindow)
        self.actionBlender.setObjectName("actionBlender")
        self.actionOrcaflex = QAction(MainWindow)
        self.actionOrcaflex.setObjectName("actionOrcaflex")
        self.actionOrcaflex_package = QAction(MainWindow)
        self.actionOrcaflex_package.setObjectName("actionOrcaflex_package")
        self.actionPython_console_2 = QAction(MainWindow)
        self.actionPython_console_2.setObjectName("actionPython_console_2")
        self.actionVersion = QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actionOnline_help = QAction(MainWindow)
        self.actionOnline_help.setObjectName("actionOnline_help")
        self.actionReload_components = QAction(MainWindow)
        self.actionReload_components.setObjectName("actionReload_components")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        icon1 = QIcon()
        icon1.addFile(":/v2/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave.setIcon(icon1)
        self.actionClear = QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionShow_labels = QAction(MainWindow)
        self.actionShow_labels.setObjectName("actionShow_labels")
        self.actionShow_labels.setCheckable(True)
        self.actionShow_labels.setChecked(True)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        icon2 = QIcon()
        icon2.addFile(":/v2/icons/gears.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSettings.setIcon(icon2)
        self.actionDegrees_of_Freedom_editor = QAction(MainWindow)
        self.actionDegrees_of_Freedom_editor.setObjectName(
            "actionDegrees_of_Freedom_editor"
        )
        self.actionSet_input_focus_to_viewport = QAction(MainWindow)
        self.actionSet_input_focus_to_viewport.setObjectName(
            "actionSet_input_focus_to_viewport"
        )
        self.actionSelf_contained_DAVE_package = QAction(MainWindow)
        self.actionSelf_contained_DAVE_package.setObjectName(
            "actionSelf_contained_DAVE_package"
        )
        self.actionShow_origin = QAction(MainWindow)
        self.actionShow_origin.setObjectName("actionShow_origin")
        self.actionShow_origin.setCheckable(True)
        self.actionShow_origin.setChecked(True)
        self.actionImport_package = QAction(MainWindow)
        self.actionImport_package.setObjectName("actionImport_package")
        self.actionCopy = QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionSend_bug_report = QAction(MainWindow)
        self.actionSend_bug_report.setObjectName("actionSend_bug_report")
        self.actionSolver_settings = QAction(MainWindow)
        self.actionSolver_settings.setObjectName("actionSolver_settings")
        self.actionSolver_settings.setIcon(icon2)
        self.action3D_points_to_csv = QAction(MainWindow)
        self.action3D_points_to_csv.setObjectName("action3D_points_to_csv")
        self.actionRun_automated_tests = QAction(MainWindow)
        self.actionRun_automated_tests.setObjectName("actionRun_automated_tests")
        self.actionRestore_right_side_docks = QAction(MainWindow)
        self.actionRestore_right_side_docks.setObjectName(
            "actionRestore_right_side_docks"
        )
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("border:none;")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QSize(0, 24))
        self.widget_3.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pbUpdate = QPushButton(self.widget_3)
        self.pbUpdate.setObjectName("pbUpdate")
        icon3 = QIcon()
        icon3.addFile(":/icons/import.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbUpdate.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.pbUpdate)

        self.cbPainerSelect = QComboBox(self.widget_3)
        self.cbPainerSelect.setObjectName("cbPainerSelect")
        self.cbPainerSelect.setStyleSheet("")
        self.cbPainerSelect.setFrame(True)

        self.horizontalLayout_2.addWidget(self.cbPainerSelect)

        self.pbLayers = QPushButton(self.widget_3)
        self.pbLayers.setObjectName("pbLayers")
        icon4 = QIcon()
        icon4.addFile(":/v2/icons/layer.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pbLayers.setIcon(icon4)
        self.pbLayers.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pbLayers)

        self.pbSide = QPushButton(self.widget_3)
        self.pbSide.setObjectName("pbSide")
        icon5 = QIcon()
        icon5.addFile(":/icons/side.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbSide.setIcon(icon5)
        self.pbSide.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pbSide)

        self.pbFront = QPushButton(self.widget_3)
        self.pbFront.setObjectName("pbFront")
        icon6 = QIcon()
        icon6.addFile(":/icons/front.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbFront.setIcon(icon6)
        self.pbFront.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pbFront)

        self.pbTop = QPushButton(self.widget_3)
        self.pbTop.setObjectName("pbTop")
        icon7 = QIcon()
        icon7.addFile(":/icons/top.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbTop.setIcon(icon7)
        self.pbTop.setCheckable(False)
        self.pbTop.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pbTop)

        self.btnZoomFit = QPushButton(self.widget_3)
        self.btnZoomFit.setObjectName("btnZoomFit")
        icon8 = QIcon()
        icon8.addFile(":/icons/cube_open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnZoomFit.setIcon(icon8)
        self.btnZoomFit.setFlat(True)

        self.horizontalLayout_2.addWidget(self.btnZoomFit)

        self.pb3D = QPushButton(self.widget_3)
        self.pb3D.setObjectName("pb3D")
        self.pb3D.setMaximumSize(QSize(30, 16777215))
        self.pb3D.setCheckable(True)
        self.pb3D.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pb3D)

        self.pbCopyViewCode = QPushButton(self.widget_3)
        self.pbCopyViewCode.setObjectName("pbCopyViewCode")
        icon9 = QIcon()
        icon9.addFile(":/icons/icon_copy.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbCopyViewCode.setIcon(icon9)
        self.pbCopyViewCode.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pbCopyViewCode)

        self.pbUC = QPushButton(self.widget_3)
        self.pbUC.setObjectName("pbUC")
        icon10 = QIcon()
        icon10.addFile(":/icons/UC_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbUC.setIcon(icon10)
        self.pbUC.setCheckable(True)
        self.pbUC.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pbUC)

        self.pbOrigin = QPushButton(self.widget_3)
        self.pbOrigin.setObjectName("pbOrigin")
        icon11 = QIcon()
        icon11.addFile(":/icons/axis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbOrigin.setIcon(icon11)
        self.pbOrigin.setCheckable(True)
        self.pbOrigin.setChecked(True)
        self.pbOrigin.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pbOrigin)

        self.btnWater = QPushButton(self.widget_3)
        self.btnWater.setObjectName("btnWater")
        self.btnWater.setBaseSize(QSize(0, 0))
        icon12 = QIcon()
        icon12.addFile(":/icons/fish.png", QSize(), QIcon.Normal, QIcon.On)
        self.btnWater.setIcon(icon12)
        self.btnWater.setCheckable(True)
        self.btnWater.setFlat(True)

        self.horizontalLayout_2.addWidget(self.btnWater)

        self.btnSSAO = QPushButton(self.widget_3)
        self.btnSSAO.setObjectName("btnSSAO")
        icon13 = QIcon()
        icon13.addFile(":/icons/cube_shaded.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnSSAO.setIcon(icon13)
        self.btnSSAO.setCheckable(True)
        self.btnSSAO.setChecked(False)
        self.btnSSAO.setFlat(True)

        self.horizontalLayout_2.addWidget(self.btnSSAO)

        self.btnBlender = QPushButton(self.widget_3)
        self.btnBlender.setObjectName("btnBlender")
        self.btnBlender.setMaximumSize(QSize(100, 16777215))
        icon14 = QIcon()
        icon14.addFile(
            ":/icons/blender_icon_64x64.png", QSize(), QIcon.Normal, QIcon.On
        )
        self.btnBlender.setIcon(icon14)
        self.btnBlender.setFlat(True)

        self.horizontalLayout_2.addWidget(self.btnBlender)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.verticalLayout_3.addWidget(self.widget_3)

        self.frame3d = QFrame(self.centralwidget)
        self.frame3d.setObjectName("frame3d")
        self.frame3d.setAcceptDrops(True)
        self.frame3d.setFrameShape(QFrame.NoFrame)
        self.frame3d.setFrameShadow(QFrame.Plain)
        self.frame3d.setLineWidth(0)

        self.verticalLayout_3.addWidget(self.frame3d)

        self.frameAni = QWidget(self.centralwidget)
        self.frameAni.setObjectName("frameAni")
        sizePolicy.setHeightForWidth(self.frameAni.sizePolicy().hasHeightForWidth())
        self.frameAni.setSizePolicy(sizePolicy)
        self.frameAni.setMinimumSize(QSize(0, 20))
        self.frameAni.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout = QHBoxLayout(self.frameAni)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.frameAni)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.btnPauseAnimation = QToolButton(self.widget_2)
        self.btnPauseAnimation.setObjectName("btnPauseAnimation")
        icon15 = QIcon()
        icon15.addFile(":/v2/icons/pause.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btnPauseAnimation.setIcon(icon15)
        self.btnPauseAnimation.setCheckable(False)

        self.gridLayout.addWidget(self.btnPauseAnimation, 0, 1, 1, 1)

        self.btnStopAnimation = QToolButton(self.widget_2)
        self.btnStopAnimation.setObjectName("btnStopAnimation")

        self.gridLayout.addWidget(self.btnStopAnimation, 0, 0, 1, 1)

        self.sbPlaybackspeed = QDoubleSpinBox(self.widget_2)
        self.sbPlaybackspeed.setObjectName("sbPlaybackspeed")
        self.sbPlaybackspeed.setToolTipDuration(0)
        self.sbPlaybackspeed.setMinimum(0.100000000000000)
        self.sbPlaybackspeed.setMaximum(10.000000000000000)
        self.sbPlaybackspeed.setSingleStep(0.100000000000000)
        self.sbPlaybackspeed.setValue(1.000000000000000)

        self.gridLayout.addWidget(self.sbPlaybackspeed, 0, 2, 1, 1)

        self.horizontalLayout.addWidget(self.widget_2)

        self.aniSlider = QSlider(self.frameAni)
        self.aniSlider.setObjectName("aniSlider")
        self.aniSlider.setOrientation(Qt.Horizontal)
        self.aniSlider.setTickPosition(QSlider.TicksAbove)

        self.horizontalLayout.addWidget(self.aniSlider)

        self.verticalLayout_3.addWidget(self.frameAni)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1099, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuExport = QMenu(self.menuFile)
        self.menuExport.setObjectName("menuExport")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuLook_towards = QMenu(self.menuView)
        self.menuLook_towards.setObjectName("menuLook_towards")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuScene = QMenu(self.menubar)
        self.menuScene.setObjectName("menuScene")
        MainWindow.setMenuBar(self.menubar)
        self.dockWidget_2 = QDockWidget(MainWindow)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.horizontalLayout_4 = QHBoxLayout(self.dockWidgetContents_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget_5 = QWidget(self.dockWidgetContents_2)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_4 = QVBoxLayout(self.widget_5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget_6 = QWidget(self.widget_5)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.widget_6)
        self.label_3.setObjectName("label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.pbClearCode = QToolButton(self.widget_6)
        self.pbClearCode.setObjectName("pbClearCode")
        icon16 = QIcon()
        icon16.addFile(":/icons/file_new.png", QSize(), QIcon.Normal, QIcon.On)
        self.pbClearCode.setIcon(icon16)
        self.pbClearCode.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_3.addWidget(self.pbClearCode)

        self.pbExecute = QToolButton(self.widget_6)
        self.pbExecute.setObjectName("pbExecute")
        icon17 = QIcon()
        icon17.addFile(
            ":/icons/python logo klein.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.pbExecute.setIcon(icon17)
        self.pbExecute.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_3.addWidget(self.pbExecute)

        self.verticalLayout_4.addWidget(self.widget_6)

        self.teCode = QTextEdit(self.widget_5)
        self.teCode.setObjectName("teCode")

        self.verticalLayout_4.addWidget(self.teCode)

        self.horizontalLayout_4.addWidget(self.widget_5)

        self.frame_3 = QFrame(self.dockWidgetContents_2)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(13, 0, 13, 0)
        self.widget_7 = QWidget(self.frame_3)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget_7)
        self.label_2.setObjectName("label_2")
        self.label_2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.horizontalLayout_5.addWidget(self.label_2)

        self.pbGenerateSceneCode = QToolButton(self.widget_7)
        self.pbGenerateSceneCode.setObjectName("pbGenerateSceneCode")
        icon18 = QIcon()
        icon18.addFile(":/icons/cube.png", QSize(), QIcon.Normal, QIcon.On)
        self.pbGenerateSceneCode.setIcon(icon18)
        self.pbGenerateSceneCode.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_5.addWidget(self.pbGenerateSceneCode)

        self.pbCopyOutput = QToolButton(self.widget_7)
        self.pbCopyOutput.setObjectName("pbCopyOutput")
        icon19 = QIcon()
        icon19.addFile(":/icons/icon_copy.png", QSize(), QIcon.Normal, QIcon.On)
        self.pbCopyOutput.setIcon(icon19)

        self.horizontalLayout_5.addWidget(self.pbCopyOutput)

        self.verticalLayout.addWidget(self.widget_7)

        self.teFeedback = QTextEdit(self.frame_3)
        self.teFeedback.setObjectName("teFeedback")
        self.teFeedback.setAutoFillBackground(False)
        self.teFeedback.setFrameShape(QFrame.StyledPanel)

        self.verticalLayout.addWidget(self.teFeedback)

        self.horizontalLayout_4.addWidget(self.frame_3)

        self.widget_4 = QWidget(self.dockWidgetContents_2)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_5 = QVBoxLayout(self.widget_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.widget_4)
        self.widget.setObjectName("widget")
        self.horizontalLayout_6 = QHBoxLayout(self.widget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.horizontalLayout_6.addWidget(self.label)

        self.tbTidyHistory = QToolButton(self.widget)
        self.tbTidyHistory.setObjectName("tbTidyHistory")

        self.horizontalLayout_6.addWidget(self.tbTidyHistory)

        self.pbCopyHistory = QToolButton(self.widget)
        self.pbCopyHistory.setObjectName("pbCopyHistory")
        self.pbCopyHistory.setIcon(icon19)

        self.horizontalLayout_6.addWidget(self.pbCopyHistory)

        self.verticalLayout_5.addWidget(self.widget)

        self.teHistory = QTextEdit(self.widget_4)
        self.teHistory.setObjectName("teHistory")

        self.verticalLayout_5.addWidget(self.teHistory)

        self.horizontalLayout_4.addWidget(self.widget_4)

        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget_2)
        self.infobar = QDockWidget(MainWindow)
        self.infobar.setObjectName("infobar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.infobar.sizePolicy().hasHeightForWidth())
        self.infobar.setSizePolicy(sizePolicy1)
        self.infobar.setMinimumSize(QSize(60, 40))
        self.infobar.setStyleSheet("background-color: rgb(200, 255, 100);")
        self.infobar.setFeatures(QDockWidget.DockWidgetClosable)
        self.infobar.setAllowedAreas(Qt.TopDockWidgetArea)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.infobar.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.TopDockWidgetArea, self.infobar)
        QWidget.setTabOrder(self.aniSlider, self.pbSide)
        QWidget.setTabOrder(self.pbSide, self.pbFront)
        QWidget.setTabOrder(self.pbFront, self.pbTop)
        QWidget.setTabOrder(self.pbTop, self.btnZoomFit)
        QWidget.setTabOrder(self.btnZoomFit, self.pbUpdate)
        QWidget.setTabOrder(self.pbUpdate, self.pbUC)
        QWidget.setTabOrder(self.pbUC, self.pbOrigin)
        QWidget.setTabOrder(self.pbOrigin, self.btnWater)
        QWidget.setTabOrder(self.btnWater, self.btnSSAO)
        QWidget.setTabOrder(self.btnSSAO, self.btnBlender)
        QWidget.setTabOrder(self.btnBlender, self.teCode)
        QWidget.setTabOrder(self.teCode, self.pbClearCode)
        QWidget.setTabOrder(self.pbClearCode, self.pbExecute)
        QWidget.setTabOrder(self.pbExecute, self.pbGenerateSceneCode)
        QWidget.setTabOrder(self.pbGenerateSceneCode, self.pbCopyOutput)
        QWidget.setTabOrder(self.pbCopyOutput, self.teFeedback)
        QWidget.setTabOrder(self.teFeedback, self.tbTidyHistory)
        QWidget.setTabOrder(self.tbTidyHistory, self.pbCopyHistory)
        QWidget.setTabOrder(self.pbCopyHistory, self.teHistory)
        QWidget.setTabOrder(self.teHistory, self.btnStopAnimation)
        QWidget.setTabOrder(self.btnStopAnimation, self.btnPauseAnimation)
        QWidget.setTabOrder(self.btnPauseAnimation, self.sbPlaybackspeed)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuScene.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionImport_sub_scene)
        self.menuFile.addAction(self.actionImport_browser)
        self.menuFile.addAction(self.actionImport_package)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_scene)
        self.menuFile.addAction(self.actionSave_actions_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuExport.addAction(self.actionBlender)
        self.menuExport.addAction(self.actionOrcaflex)
        self.menuExport.addAction(self.actionOrcaflex_package)
        self.menuExport.addAction(self.actionSelf_contained_DAVE_package)
        self.menuExport.addAction(self.action3D_points_to_csv)
        self.menuView.addAction(self.action2D_mode)
        self.menuView.addAction(self.menuLook_towards.menuAction())
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionShow_water_plane)
        self.menuView.addAction(self.actionShow_origin)
        self.menuView.addAction(self.actionShow_labels)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionFull_refresh)
        self.menuView.addAction(self.actionCamera_reset)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionPython_console_2)
        self.menuView.addAction(self.actionDegrees_of_Freedom_editor)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionSet_input_focus_to_viewport)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionRestore_right_side_docks)
        self.menuLook_towards.addAction(self.actionX)
        self.menuLook_towards.addAction(self.action_x)
        self.menuLook_towards.addAction(self.actionY)
        self.menuLook_towards.addAction(self.action_Y)
        self.menuLook_towards.addAction(self.actionZ)
        self.menuLook_towards.addAction(self.action_Z)
        self.menuHelp.addAction(self.actionVersion)
        self.menuHelp.addAction(self.actionOnline_help)
        self.menuHelp.addAction(self.actionSend_bug_report)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionRun_automated_tests)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionSolver_settings)
        self.menuScene.addSeparator()
        self.menuScene.addAction(self.actionReload_components)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "DAVE", None)
        )
        self.actionSave_scene.setText(
            QCoreApplication.translate("MainWindow", "Save as", None)
        )
        self.actionImport_sub_scene.setText(
            QCoreApplication.translate("MainWindow", "Import (file)", None)
        )
        self.actionNew.setText(QCoreApplication.translate("MainWindow", "New", None))
        self.actionHorizontal_camera.setText(
            QCoreApplication.translate(
                "MainWindow", "Level camera (make horizon horizontal)", None
            )
        )
        # if QT_CONFIG(shortcut)
        self.actionHorizontal_camera.setShortcut(
            QCoreApplication.translate("MainWindow", "Alt+L", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action.setText(QCoreApplication.translate("MainWindow", "---", None))
        self.action2D_mode.setText(
            QCoreApplication.translate("MainWindow", "2D mode", None)
        )
        self.actionDark_mode.setText(
            QCoreApplication.translate("MainWindow", "Make darker", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionDark_mode.setShortcut(
            QCoreApplication.translate("MainWindow", "Alt+-", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionShow_visuals.setText(
            QCoreApplication.translate("MainWindow", "Show visuals", None)
        )
        self.actionShow_Geometry_elements.setText(
            QCoreApplication.translate("MainWindow", "Show Geometry elements", None)
        )
        self.actionShow_force_applying_element.setText(
            QCoreApplication.translate(
                "MainWindow", "Show physics only elements (connectors, meshes)", None
            )
        )
        self.actionSet_all_visible.setText(
            QCoreApplication.translate("MainWindow", "Set all visible", None)
        )
        self.actionSet_all_hidden.setText(
            QCoreApplication.translate("MainWindow", "Set all hidden", None)
        )
        self.actionFull_refresh.setText(
            QCoreApplication.translate("MainWindow", "Full refresh", None)
        )
        self.actionShow_water_plane.setText(
            QCoreApplication.translate("MainWindow", "Show water-plane", None)
        )
        self.actionAdd_light.setText(
            QCoreApplication.translate("MainWindow", "Make lighter", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionAdd_light.setShortcut(
            QCoreApplication.translate("MainWindow", "Alt+=", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionShow_all_forces_at_same_size.setText(
            QCoreApplication.translate(
                "MainWindow", "Show all forces same size (normalize)", None
            )
        )
        self.actionIncrease_force_size.setText(
            QCoreApplication.translate("MainWindow", "Increase force size", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionIncrease_force_size.setShortcut(
            QCoreApplication.translate("MainWindow", "Alt+]", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionDecrease_force_size.setText(
            QCoreApplication.translate("MainWindow", "Decrease force size", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionDecrease_force_size.setShortcut(
            QCoreApplication.translate("MainWindow", "Alt+[", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionIncrease_Geometry_size.setText(
            QCoreApplication.translate(
                "MainWindow", "Increase Geometry size (poi, axis)", None
            )
        )
        # if QT_CONFIG(shortcut)
        self.actionIncrease_Geometry_size.setShortcut(
            QCoreApplication.translate("MainWindow", "Alt+Shift+]", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionDecrease_Geometry_size.setText(
            QCoreApplication.translate("MainWindow", "Decrease Geometry size", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionDecrease_Geometry_size.setShortcut(
            QCoreApplication.translate("MainWindow", "Alt+Shift+[", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionPython_console.setText(
            QCoreApplication.translate("MainWindow", "Python console", None)
        )
        self.actionGoal_seek.setText(
            QCoreApplication.translate("MainWindow", "Goal-seek (one variable)", None)
        )
        self.actionStability_curve.setText(
            QCoreApplication.translate("MainWindow", "Stability-curve", None)
        )
        self.actionOptimize.setText(
            QCoreApplication.translate(
                "MainWindow", "TODO: Optimize (multiple variables)", None
            )
        )
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", "Open", None))
        self.actionImport_browser.setText(
            QCoreApplication.translate("MainWindow", "Import (browser)", None)
        )
        self.actionRender_current_view.setText(
            QCoreApplication.translate("MainWindow", "Render current view", None)
        )
        self.actionModal_shapes.setText(
            QCoreApplication.translate("MainWindow", "Modal shapes", None)
        )
        self.actionInertia_properties.setText(
            QCoreApplication.translate("MainWindow", "Inertia properties", None)
        )
        self.actionSave_actions_as.setText(
            QCoreApplication.translate("MainWindow", "Save actions as", None)
        )
        self.actionsee_open_ocean_org.setText(
            QCoreApplication.translate("MainWindow", "see open-ocean.org", None)
        )
        self.actionX.setText(QCoreApplication.translate("MainWindow", "X", None))
        self.action_x.setText(QCoreApplication.translate("MainWindow", "-X", None))
        self.actionY.setText(QCoreApplication.translate("MainWindow", "Y", None))
        self.action_Y.setText(QCoreApplication.translate("MainWindow", "-Y", None))
        self.actionZ.setText(QCoreApplication.translate("MainWindow", "From top", None))
        self.action_Z.setText(
            QCoreApplication.translate("MainWindow", "From bottom", None)
        )
        self.actionLook_towards_center.setText(
            QCoreApplication.translate("MainWindow", "Look towards center", None)
        )
        self.actionCamera_reset.setText(
            QCoreApplication.translate("MainWindow", "Camera reset", None)
        )
        self.actionShow_CoG_positions.setText(
            QCoreApplication.translate("MainWindow", "Show CoGs", None)
        )
        self.actionBlender.setText(
            QCoreApplication.translate("MainWindow", "Blender", None)
        )
        self.actionOrcaflex.setText(
            QCoreApplication.translate("MainWindow", "Orcaflex .yml", None)
        )
        self.actionOrcaflex_package.setText(
            QCoreApplication.translate(
                "MainWindow", "Orcaflex run and collect package", None
            )
        )
        self.actionPython_console_2.setText(
            QCoreApplication.translate("MainWindow", "Python console", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionPython_console_2.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+P", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionVersion.setText(
            QCoreApplication.translate("MainWindow", "Version", None)
        )
        self.actionOnline_help.setText(
            QCoreApplication.translate("MainWindow", "Online help", None)
        )
        self.actionReload_components.setText(
            QCoreApplication.translate(
                "MainWindow", "Reload components from files", None
            )
        )
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", "Undo", None))
        # if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+Z", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", "Redo", None))
        # if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+Y", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", "Save", None))
        # if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+S", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionClear.setText(
            QCoreApplication.translate("MainWindow", "Remove al nodes", None)
        )
        self.actionShow_labels.setText(
            QCoreApplication.translate("MainWindow", "Show labels", None)
        )
        self.actionSettings.setText(
            QCoreApplication.translate("MainWindow", "Settings", None)
        )
        self.actionDegrees_of_Freedom_editor.setText(
            QCoreApplication.translate(
                "MainWindow", "Degrees of Freedom overview", None
            )
        )
        self.actionSet_input_focus_to_viewport.setText(
            QCoreApplication.translate(
                "MainWindow", "Set input focus to viewport", None
            )
        )
        # if QT_CONFIG(shortcut)
        self.actionSet_input_focus_to_viewport.setShortcut(
            QCoreApplication.translate("MainWindow", "Esc", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSelf_contained_DAVE_package.setText(
            QCoreApplication.translate(
                "MainWindow", "Self-contained DAVE package", None
            )
        )
        self.actionShow_origin.setText(
            QCoreApplication.translate("MainWindow", "Show origin", None)
        )
        self.actionImport_package.setText(
            QCoreApplication.translate(
                "MainWindow", "Import DAVE package (read-only)", None
            )
        )
        self.actionCopy.setText(QCoreApplication.translate("MainWindow", "Copy", None))
        # if QT_CONFIG(shortcut)
        self.actionCopy.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+C", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionPaste.setText(
            QCoreApplication.translate("MainWindow", "Paste", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionPaste.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+V", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSend_bug_report.setText(
            QCoreApplication.translate("MainWindow", "Send bug report", None)
        )
        self.actionSolver_settings.setText(
            QCoreApplication.translate("MainWindow", "Solver settings", None)
        )
        self.action3D_points_to_csv.setText(
            QCoreApplication.translate("MainWindow", "3D points to .csv", None)
        )
        self.actionRun_automated_tests.setText(
            QCoreApplication.translate("MainWindow", "Run automated tests", None)
        )
        self.actionRestore_right_side_docks.setText(
            QCoreApplication.translate(
                "MainWindow", "Restore right side docks -->", None
            )
        )
        self.pbUpdate.setText(QCoreApplication.translate("MainWindow", "Update", None))
        self.pbLayers.setText("")
        self.pbSide.setText("")
        self.pbFront.setText("")
        self.pbTop.setText("")
        self.btnZoomFit.setText("")
        self.pb3D.setText(QCoreApplication.translate("MainWindow", "2D", None))
        # if QT_CONFIG(tooltip)
        self.pbCopyViewCode.setToolTip(
            QCoreApplication.translate("MainWindow", "Copy screenshot code", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.pbCopyViewCode.setText("")
        self.pbUC.setText("")
        self.pbOrigin.setText("")
        self.btnWater.setText("")
        self.btnSSAO.setText("")
        self.btnBlender.setText("")
        self.btnPauseAnimation.setText("")
        self.btnStopAnimation.setText(
            QCoreApplication.translate("MainWindow", "X", None)
        )
        # if QT_CONFIG(tooltip)
        self.sbPlaybackspeed.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuExport.setTitle(
            QCoreApplication.translate("MainWindow", "Export", None)
        )
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", "View", None))
        self.menuLook_towards.setTitle(
            QCoreApplication.translate("MainWindow", "Look in direction", None)
        )
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", "Edit", None))
        self.menuScene.setTitle(QCoreApplication.translate("MainWindow", "Scene", None))
        self.dockWidget_2.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Python engine", None)
        )
        self.label_3.setText(QCoreApplication.translate("MainWindow", "Code", None))
        self.pbClearCode.setText(
            QCoreApplication.translate("MainWindow", "&Clear", None)
        )
        # if QT_CONFIG(tooltip)
        self.pbExecute.setToolTip(
            QCoreApplication.translate("MainWindow", "Shift + Enter", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.pbExecute.setText(
            QCoreApplication.translate("MainWindow", "Execute", None)
        )
        self.teCode.setHtml(
            QCoreApplication.translate(
                "MainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "hr { height: 1px; border-width: 0; }\n"
                'li.unchecked::marker { content: "\\2610"; }\n'
                'li.checked::marker { content: "\\2612"; }\n'
                "</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'MS Shell Dlg 2\'; font-size:8pt;">print(&quot;type python code here&quot;)</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'MS Shell Dlg 2\'; font-size:8pt;"># press shift+enter to execute</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-lef'
                't:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'MS Shell Dlg 2\'; font-size:8pt;"># press alt+c to clear and focus here</span></p></body></html>',
                None,
            )
        )
        self.label_2.setText(QCoreApplication.translate("MainWindow", "Output", None))
        self.pbGenerateSceneCode.setText(
            QCoreApplication.translate("MainWindow", "Generate scene code", None)
        )
        # if QT_CONFIG(tooltip)
        self.pbCopyOutput.setToolTip(
            QCoreApplication.translate("MainWindow", "Copy text below", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.pbCopyOutput.setText(
            QCoreApplication.translate("MainWindow", "Copy", None)
        )
        self.label.setText(
            QCoreApplication.translate("MainWindow", "History (actions)", None)
        )
        # if QT_CONFIG(tooltip)
        self.tbTidyHistory.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Removes redundant code from history", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.tbTidyHistory.setText(
            QCoreApplication.translate("MainWindow", "tidy", None)
        )
        # if QT_CONFIG(tooltip)
        self.pbCopyHistory.setToolTip(
            QCoreApplication.translate("MainWindow", "Copy text below", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.pbCopyHistory.setText(
            QCoreApplication.translate("MainWindow", "Copy", None)
        )
        self.infobar.setWindowTitle(
            QCoreApplication.translate("MainWindow", "THIS IS A READ-ONLY VIEW", None)
        )

    # retranslateUi
