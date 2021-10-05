# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_form.ui',
# licensing of 'main_form.ui' applies.
#
# Created: Mon Oct  4 18:12:27 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1099, 819)
        MainWindow.setAcceptDrops(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/Dave_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QtCore.QSize(0, 24))
        self.widget_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pbUpdate = QtWidgets.QPushButton(self.widget_3)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/import.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbUpdate.setIcon(icon1)
        self.pbUpdate.setObjectName("pbUpdate")
        self.horizontalLayout_2.addWidget(self.pbUpdate)
        self.btnSolveStatics = QtWidgets.QPushButton(self.widget_3)
        self.btnSolveStatics.setIcon(icon)
        self.btnSolveStatics.setObjectName("btnSolveStatics")
        self.horizontalLayout_2.addWidget(self.btnSolveStatics)
        self.btnUndoStatics = QtWidgets.QPushButton(self.widget_3)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icon_undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnUndoStatics.setIcon(icon2)
        self.btnUndoStatics.setObjectName("btnUndoStatics")
        self.horizontalLayout_2.addWidget(self.btnUndoStatics)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pbCopyViewCode = QtWidgets.QPushButton(self.widget_3)
        self.pbCopyViewCode.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icon_copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbCopyViewCode.setIcon(icon3)
        self.pbCopyViewCode.setFlat(True)
        self.pbCopyViewCode.setObjectName("pbCopyViewCode")
        self.horizontalLayout_2.addWidget(self.pbCopyViewCode)
        self.pb3D = QtWidgets.QPushButton(self.widget_3)
        self.pb3D.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pb3D.setCheckable(True)
        self.pb3D.setFlat(True)
        self.pb3D.setObjectName("pb3D")
        self.horizontalLayout_2.addWidget(self.pb3D)
        self.pbSide = QtWidgets.QPushButton(self.widget_3)
        self.pbSide.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/side.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbSide.setIcon(icon4)
        self.pbSide.setFlat(True)
        self.pbSide.setObjectName("pbSide")
        self.horizontalLayout_2.addWidget(self.pbSide)
        self.pbFront = QtWidgets.QPushButton(self.widget_3)
        self.pbFront.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/front.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbFront.setIcon(icon5)
        self.pbFront.setFlat(True)
        self.pbFront.setObjectName("pbFront")
        self.horizontalLayout_2.addWidget(self.pbFront)
        self.pbTop = QtWidgets.QPushButton(self.widget_3)
        self.pbTop.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/top.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbTop.setIcon(icon6)
        self.pbTop.setCheckable(False)
        self.pbTop.setFlat(True)
        self.pbTop.setObjectName("pbTop")
        self.horizontalLayout_2.addWidget(self.pbTop)
        self.btnZoomFit = QtWidgets.QPushButton(self.widget_3)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/circle_blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnZoomFit.setIcon(icon7)
        self.btnZoomFit.setFlat(True)
        self.btnZoomFit.setObjectName("btnZoomFit")
        self.horizontalLayout_2.addWidget(self.btnZoomFit)
        self.cbPainerSelect = QtWidgets.QComboBox(self.widget_3)
        self.cbPainerSelect.setStyleSheet("")
        self.cbPainerSelect.setFrame(True)
        self.cbPainerSelect.setObjectName("cbPainerSelect")
        self.horizontalLayout_2.addWidget(self.cbPainerSelect)
        self.pbUC = QtWidgets.QPushButton(self.widget_3)
        self.pbUC.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/UC_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbUC.setIcon(icon8)
        self.pbUC.setCheckable(True)
        self.pbUC.setFlat(True)
        self.pbUC.setObjectName("pbUC")
        self.horizontalLayout_2.addWidget(self.pbUC)
        self.btnWater = QtWidgets.QPushButton(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnWater.sizePolicy().hasHeightForWidth())
        self.btnWater.setSizePolicy(sizePolicy)
        self.btnWater.setMinimumSize(QtCore.QSize(30, 0))
        self.btnWater.setMaximumSize(QtCore.QSize(60, 16777215))
        self.btnWater.setBaseSize(QtCore.QSize(30, 0))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/fish.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnWater.setIcon(icon9)
        self.btnWater.setCheckable(True)
        self.btnWater.setFlat(True)
        self.btnWater.setObjectName("btnWater")
        self.horizontalLayout_2.addWidget(self.btnWater)
        self.btnSSAO = QtWidgets.QPushButton(self.widget_3)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/cube.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSSAO.setIcon(icon10)
        self.btnSSAO.setCheckable(True)
        self.btnSSAO.setChecked(False)
        self.btnSSAO.setFlat(True)
        self.btnSSAO.setObjectName("btnSSAO")
        self.horizontalLayout_2.addWidget(self.btnSSAO)
        self.btnBlender = QtWidgets.QPushButton(self.widget_3)
        self.btnBlender.setMaximumSize(QtCore.QSize(100, 16777215))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/blender_icon_64x64.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnBlender.setIcon(icon11)
        self.btnBlender.setFlat(True)
        self.btnBlender.setObjectName("btnBlender")
        self.horizontalLayout_2.addWidget(self.btnBlender)
        self.verticalLayout_3.addWidget(self.widget_3)
        self.frame3d = QtWidgets.QFrame(self.centralwidget)
        self.frame3d.setAcceptDrops(False)
        self.frame3d.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame3d.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame3d.setLineWidth(0)
        self.frame3d.setObjectName("frame3d")
        self.verticalLayout_3.addWidget(self.frame3d)
        self.frameAni = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameAni.sizePolicy().hasHeightForWidth())
        self.frameAni.setSizePolicy(sizePolicy)
        self.frameAni.setMinimumSize(QtCore.QSize(0, 20))
        self.frameAni.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frameAni.setObjectName("frameAni")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frameAni)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_2 = QtWidgets.QWidget(self.frameAni)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.btnPauseAnimation = QtWidgets.QToolButton(self.widget_2)
        self.btnPauseAnimation.setCheckable(True)
        self.btnPauseAnimation.setObjectName("btnPauseAnimation")
        self.gridLayout.addWidget(self.btnPauseAnimation, 0, 1, 1, 1)
        self.btnStopAnimation = QtWidgets.QToolButton(self.widget_2)
        self.btnStopAnimation.setObjectName("btnStopAnimation")
        self.gridLayout.addWidget(self.btnStopAnimation, 0, 0, 1, 1)
        self.sbPlaybackspeed = QtWidgets.QDoubleSpinBox(self.widget_2)
        self.sbPlaybackspeed.setToolTip("")
        self.sbPlaybackspeed.setToolTipDuration(0)
        self.sbPlaybackspeed.setMinimum(0.1)
        self.sbPlaybackspeed.setMaximum(10.0)
        self.sbPlaybackspeed.setSingleStep(0.1)
        self.sbPlaybackspeed.setProperty("value", 1.0)
        self.sbPlaybackspeed.setObjectName("sbPlaybackspeed")
        self.gridLayout.addWidget(self.sbPlaybackspeed, 0, 2, 1, 1)
        self.horizontalLayout.addWidget(self.widget_2)
        self.aniSlider = QtWidgets.QSlider(self.frameAni)
        self.aniSlider.setOrientation(QtCore.Qt.Horizontal)
        self.aniSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.aniSlider.setObjectName("aniSlider")
        self.horizontalLayout.addWidget(self.aniSlider)
        self.verticalLayout_3.addWidget(self.frameAni)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1099, 18))
        self.menubar.setObjectName("menubar")
        self.menuSolve_Statics = QtWidgets.QMenu(self.menubar)
        self.menuSolve_Statics.setObjectName("menuSolve_Statics")
        self.menuExport = QtWidgets.QMenu(self.menuSolve_Statics)
        self.menuExport.setObjectName("menuExport")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuLook_towards = QtWidgets.QMenu(self.menuView)
        self.menuLook_towards.setObjectName("menuLook_towards")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.dockWidgetContents_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget_5 = QtWidgets.QWidget(self.dockWidgetContents_2)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_6 = QtWidgets.QWidget(self.widget_5)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget_6)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.pbClearCode = QtWidgets.QToolButton(self.widget_6)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/file_new.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pbClearCode.setIcon(icon12)
        self.pbClearCode.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.pbClearCode.setObjectName("pbClearCode")
        self.horizontalLayout_3.addWidget(self.pbClearCode)
        self.pbExecute = QtWidgets.QToolButton(self.widget_6)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/python logo klein.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbExecute.setIcon(icon13)
        self.pbExecute.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.pbExecute.setObjectName("pbExecute")
        self.horizontalLayout_3.addWidget(self.pbExecute)
        self.verticalLayout_4.addWidget(self.widget_6)
        self.teCode = QtWidgets.QTextEdit(self.widget_5)
        self.teCode.setObjectName("teCode")
        self.verticalLayout_4.addWidget(self.teCode)
        self.horizontalLayout_4.addWidget(self.widget_5)
        self.frame_3 = QtWidgets.QFrame(self.dockWidgetContents_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setContentsMargins(13, 0, 13, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_7 = QtWidgets.QWidget(self.frame_3)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.widget_7)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.pbGenerateSceneCode = QtWidgets.QToolButton(self.widget_7)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/cube.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pbGenerateSceneCode.setIcon(icon14)
        self.pbGenerateSceneCode.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.pbGenerateSceneCode.setObjectName("pbGenerateSceneCode")
        self.horizontalLayout_5.addWidget(self.pbGenerateSceneCode)
        self.pbCopyOutput = QtWidgets.QToolButton(self.widget_7)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icons/icon_copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pbCopyOutput.setIcon(icon15)
        self.pbCopyOutput.setObjectName("pbCopyOutput")
        self.horizontalLayout_5.addWidget(self.pbCopyOutput)
        self.verticalLayout.addWidget(self.widget_7)
        self.teFeedback = QtWidgets.QTextEdit(self.frame_3)
        self.teFeedback.setAutoFillBackground(False)
        self.teFeedback.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.teFeedback.setObjectName("teFeedback")
        self.verticalLayout.addWidget(self.teFeedback)
        self.horizontalLayout_4.addWidget(self.frame_3)
        self.widget_4 = QtWidgets.QWidget(self.dockWidgetContents_2)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget = QtWidgets.QWidget(self.widget_4)
        self.widget.setObjectName("widget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_6.setContentsMargins(-1, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.tbTidyHistory = QtWidgets.QToolButton(self.widget)
        self.tbTidyHistory.setObjectName("tbTidyHistory")
        self.horizontalLayout_6.addWidget(self.tbTidyHistory)
        self.pbCopyHistory = QtWidgets.QToolButton(self.widget)
        self.pbCopyHistory.setIcon(icon15)
        self.pbCopyHistory.setObjectName("pbCopyHistory")
        self.horizontalLayout_6.addWidget(self.pbCopyHistory)
        self.verticalLayout_5.addWidget(self.widget)
        self.teHistory = QtWidgets.QTextEdit(self.widget_4)
        self.teHistory.setObjectName("teHistory")
        self.verticalLayout_5.addWidget(self.teHistory)
        self.horizontalLayout_4.addWidget(self.widget_4)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_2)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSave_scene = QtWidgets.QAction(MainWindow)
        self.actionSave_scene.setObjectName("actionSave_scene")
        self.actionImport_sub_scene = QtWidgets.QAction(MainWindow)
        self.actionImport_sub_scene.setObjectName("actionImport_sub_scene")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionHorizontal_camera = QtWidgets.QAction(MainWindow)
        self.actionHorizontal_camera.setObjectName("actionHorizontal_camera")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action2D_mode = QtWidgets.QAction(MainWindow)
        self.action2D_mode.setCheckable(True)
        self.action2D_mode.setObjectName("action2D_mode")
        self.actionDark_mode = QtWidgets.QAction(MainWindow)
        self.actionDark_mode.setCheckable(False)
        self.actionDark_mode.setObjectName("actionDark_mode")
        self.actionShow_visuals = QtWidgets.QAction(MainWindow)
        self.actionShow_visuals.setCheckable(True)
        self.actionShow_visuals.setChecked(True)
        self.actionShow_visuals.setObjectName("actionShow_visuals")
        self.actionShow_Geometry_elements = QtWidgets.QAction(MainWindow)
        self.actionShow_Geometry_elements.setCheckable(True)
        self.actionShow_Geometry_elements.setChecked(True)
        self.actionShow_Geometry_elements.setObjectName("actionShow_Geometry_elements")
        self.actionShow_force_applying_element = QtWidgets.QAction(MainWindow)
        self.actionShow_force_applying_element.setCheckable(True)
        self.actionShow_force_applying_element.setChecked(True)
        self.actionShow_force_applying_element.setObjectName("actionShow_force_applying_element")
        self.actionSet_all_visible = QtWidgets.QAction(MainWindow)
        self.actionSet_all_visible.setObjectName("actionSet_all_visible")
        self.actionSet_all_hidden = QtWidgets.QAction(MainWindow)
        self.actionSet_all_hidden.setObjectName("actionSet_all_hidden")
        self.actionFull_refresh = QtWidgets.QAction(MainWindow)
        self.actionFull_refresh.setObjectName("actionFull_refresh")
        self.actionShow_water_plane = QtWidgets.QAction(MainWindow)
        self.actionShow_water_plane.setCheckable(True)
        self.actionShow_water_plane.setChecked(False)
        self.actionShow_water_plane.setObjectName("actionShow_water_plane")
        self.actionAdd_light = QtWidgets.QAction(MainWindow)
        self.actionAdd_light.setObjectName("actionAdd_light")
        self.actionShow_all_forces_at_same_size = QtWidgets.QAction(MainWindow)
        self.actionShow_all_forces_at_same_size.setCheckable(True)
        self.actionShow_all_forces_at_same_size.setChecked(True)
        self.actionShow_all_forces_at_same_size.setObjectName("actionShow_all_forces_at_same_size")
        self.actionIncrease_force_size = QtWidgets.QAction(MainWindow)
        self.actionIncrease_force_size.setObjectName("actionIncrease_force_size")
        self.actionDecrease_force_size = QtWidgets.QAction(MainWindow)
        self.actionDecrease_force_size.setObjectName("actionDecrease_force_size")
        self.actionIncrease_Geometry_size = QtWidgets.QAction(MainWindow)
        self.actionIncrease_Geometry_size.setObjectName("actionIncrease_Geometry_size")
        self.actionDecrease_Geometry_size = QtWidgets.QAction(MainWindow)
        self.actionDecrease_Geometry_size.setObjectName("actionDecrease_Geometry_size")
        self.actionPython_console = QtWidgets.QAction(MainWindow)
        self.actionPython_console.setObjectName("actionPython_console")
        self.actionGoal_seek = QtWidgets.QAction(MainWindow)
        self.actionGoal_seek.setObjectName("actionGoal_seek")
        self.actionStability_curve = QtWidgets.QAction(MainWindow)
        self.actionStability_curve.setObjectName("actionStability_curve")
        self.actionOptimize = QtWidgets.QAction(MainWindow)
        self.actionOptimize.setObjectName("actionOptimize")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionImport_browser = QtWidgets.QAction(MainWindow)
        self.actionImport_browser.setObjectName("actionImport_browser")
        self.actionRender_current_view = QtWidgets.QAction(MainWindow)
        self.actionRender_current_view.setObjectName("actionRender_current_view")
        self.actionModal_shapes = QtWidgets.QAction(MainWindow)
        self.actionModal_shapes.setObjectName("actionModal_shapes")
        self.actionInertia_properties = QtWidgets.QAction(MainWindow)
        self.actionInertia_properties.setObjectName("actionInertia_properties")
        self.actionSave_actions_as = QtWidgets.QAction(MainWindow)
        self.actionSave_actions_as.setObjectName("actionSave_actions_as")
        self.actionsee_open_ocean_org = QtWidgets.QAction(MainWindow)
        self.actionsee_open_ocean_org.setObjectName("actionsee_open_ocean_org")
        self.actionX = QtWidgets.QAction(MainWindow)
        self.actionX.setObjectName("actionX")
        self.action_x = QtWidgets.QAction(MainWindow)
        self.action_x.setObjectName("action_x")
        self.actionY = QtWidgets.QAction(MainWindow)
        self.actionY.setObjectName("actionY")
        self.action_Y = QtWidgets.QAction(MainWindow)
        self.action_Y.setObjectName("action_Y")
        self.actionZ = QtWidgets.QAction(MainWindow)
        self.actionZ.setObjectName("actionZ")
        self.action_Z = QtWidgets.QAction(MainWindow)
        self.action_Z.setObjectName("action_Z")
        self.actionLook_towards_center = QtWidgets.QAction(MainWindow)
        self.actionLook_towards_center.setObjectName("actionLook_towards_center")
        self.actionCamera_reset = QtWidgets.QAction(MainWindow)
        self.actionCamera_reset.setObjectName("actionCamera_reset")
        self.actionShow_CoG_positions = QtWidgets.QAction(MainWindow)
        self.actionShow_CoG_positions.setObjectName("actionShow_CoG_positions")
        self.actionBlender = QtWidgets.QAction(MainWindow)
        self.actionBlender.setObjectName("actionBlender")
        self.actionOrcaflex = QtWidgets.QAction(MainWindow)
        self.actionOrcaflex.setObjectName("actionOrcaflex")
        self.actionOrcaflex_package = QtWidgets.QAction(MainWindow)
        self.actionOrcaflex_package.setObjectName("actionOrcaflex_package")
        self.actionPython_console_2 = QtWidgets.QAction(MainWindow)
        self.actionPython_console_2.setObjectName("actionPython_console_2")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actionOnline_help = QtWidgets.QAction(MainWindow)
        self.actionOnline_help.setObjectName("actionOnline_help")
        self.menuExport.addAction(self.actionBlender)
        self.menuExport.addAction(self.actionOrcaflex)
        self.menuExport.addAction(self.actionOrcaflex_package)
        self.menuSolve_Statics.addAction(self.actionNew)
        self.menuSolve_Statics.addSeparator()
        self.menuSolve_Statics.addAction(self.actionOpen)
        self.menuSolve_Statics.addAction(self.actionImport_sub_scene)
        self.menuSolve_Statics.addAction(self.actionImport_browser)
        self.menuSolve_Statics.addSeparator()
        self.menuSolve_Statics.addAction(self.actionSave_scene)
        self.menuSolve_Statics.addAction(self.actionSave_actions_as)
        self.menuSolve_Statics.addSeparator()
        self.menuSolve_Statics.addAction(self.menuExport.menuAction())
        self.menuLook_towards.addAction(self.actionX)
        self.menuLook_towards.addAction(self.action_x)
        self.menuLook_towards.addAction(self.actionY)
        self.menuLook_towards.addAction(self.action_Y)
        self.menuLook_towards.addAction(self.actionZ)
        self.menuLook_towards.addAction(self.action_Z)
        self.menuView.addAction(self.action2D_mode)
        self.menuView.addAction(self.menuLook_towards.menuAction())
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionShow_force_applying_element)
        self.menuView.addAction(self.actionShow_water_plane)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionFull_refresh)
        self.menuView.addAction(self.actionCamera_reset)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionPython_console_2)
        self.menuView.addSeparator()
        self.menuHelp.addAction(self.actionVersion)
        self.menuHelp.addAction(self.actionOnline_help)
        self.menubar.addAction(self.menuSolve_Statics.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "DAVE", None, -1))
        self.pbUpdate.setText(QtWidgets.QApplication.translate("MainWindow", "Update", None, -1))
        self.btnSolveStatics.setText(QtWidgets.QApplication.translate("MainWindow", "Solve &statics", None, -1))
        self.btnUndoStatics.setText(QtWidgets.QApplication.translate("MainWindow", "Undo", None, -1))
        self.pbCopyViewCode.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Copy screenshot code", None, -1))
        self.pb3D.setText(QtWidgets.QApplication.translate("MainWindow", "2D", None, -1))
        self.btnZoomFit.setText(QtWidgets.QApplication.translate("MainWindow", "Zoom fit", None, -1))
        self.btnWater.setText(QtWidgets.QApplication.translate("MainWindow", "sea", None, -1))
        self.btnSSAO.setText(QtWidgets.QApplication.translate("MainWindow", "shadows", None, -1))
        self.btnBlender.setText(QtWidgets.QApplication.translate("MainWindow", "blender", None, -1))
        self.btnPauseAnimation.setText(QtWidgets.QApplication.translate("MainWindow", "||", None, -1))
        self.btnStopAnimation.setText(QtWidgets.QApplication.translate("MainWindow", "X", None, -1))
        self.menuSolve_Statics.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.menuExport.setTitle(QtWidgets.QApplication.translate("MainWindow", "Export", None, -1))
        self.menuView.setTitle(QtWidgets.QApplication.translate("MainWindow", "View", None, -1))
        self.menuLook_towards.setTitle(QtWidgets.QApplication.translate("MainWindow", "Look in direction", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("MainWindow", "Help", None, -1))
        self.dockWidget_2.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Python engine", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Code", None, -1))
        self.pbClearCode.setText(QtWidgets.QApplication.translate("MainWindow", "&Clear", None, -1))
        self.pbExecute.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Shift + Enter", None, -1))
        self.pbExecute.setText(QtWidgets.QApplication.translate("MainWindow", "Execute", None, -1))
        self.teCode.setHtml(QtWidgets.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">print(&quot;type python code here&quot;)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"># press shift+enter to execute</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"># press alt+c to clear and focus here</p></body></html>", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Output", None, -1))
        self.pbGenerateSceneCode.setText(QtWidgets.QApplication.translate("MainWindow", "Generate scene code", None, -1))
        self.pbCopyOutput.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Copy text below", None, -1))
        self.pbCopyOutput.setText(QtWidgets.QApplication.translate("MainWindow", "Copy", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "History (actions)", None, -1))
        self.tbTidyHistory.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Removes redundant code from history", None, -1))
        self.tbTidyHistory.setText(QtWidgets.QApplication.translate("MainWindow", "tidy", None, -1))
        self.pbCopyHistory.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Copy text below", None, -1))
        self.pbCopyHistory.setText(QtWidgets.QApplication.translate("MainWindow", "Copy", None, -1))
        self.toolBar.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "toolBar", None, -1))
        self.actionSave_scene.setText(QtWidgets.QApplication.translate("MainWindow", "Save as", None, -1))
        self.actionImport_sub_scene.setText(QtWidgets.QApplication.translate("MainWindow", "Import (file)", None, -1))
        self.actionNew.setText(QtWidgets.QApplication.translate("MainWindow", "New", None, -1))
        self.actionHorizontal_camera.setText(QtWidgets.QApplication.translate("MainWindow", "Level camera (make horizon horizontal)", None, -1))
        self.actionHorizontal_camera.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Alt+L", None, -1))
        self.action.setText(QtWidgets.QApplication.translate("MainWindow", "---", None, -1))
        self.action2D_mode.setText(QtWidgets.QApplication.translate("MainWindow", "2D mode", None, -1))
        self.actionDark_mode.setText(QtWidgets.QApplication.translate("MainWindow", "Make darker", None, -1))
        self.actionDark_mode.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Alt+-", None, -1))
        self.actionShow_visuals.setText(QtWidgets.QApplication.translate("MainWindow", "Show visuals", None, -1))
        self.actionShow_Geometry_elements.setText(QtWidgets.QApplication.translate("MainWindow", "Show Geometry elements", None, -1))
        self.actionShow_force_applying_element.setText(QtWidgets.QApplication.translate("MainWindow", "Show physics only elements (connectors, meshes)", None, -1))
        self.actionSet_all_visible.setText(QtWidgets.QApplication.translate("MainWindow", "Set all visible", None, -1))
        self.actionSet_all_hidden.setText(QtWidgets.QApplication.translate("MainWindow", "Set all hidden", None, -1))
        self.actionFull_refresh.setText(QtWidgets.QApplication.translate("MainWindow", "Full refresh", None, -1))
        self.actionShow_water_plane.setText(QtWidgets.QApplication.translate("MainWindow", "Show water-plane", None, -1))
        self.actionAdd_light.setText(QtWidgets.QApplication.translate("MainWindow", "Make lighter", None, -1))
        self.actionAdd_light.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Alt+=", None, -1))
        self.actionShow_all_forces_at_same_size.setText(QtWidgets.QApplication.translate("MainWindow", "Show all forces same size (normalize)", None, -1))
        self.actionIncrease_force_size.setText(QtWidgets.QApplication.translate("MainWindow", "Increase force size", None, -1))
        self.actionIncrease_force_size.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Alt+]", None, -1))
        self.actionDecrease_force_size.setText(QtWidgets.QApplication.translate("MainWindow", "Decrease force size", None, -1))
        self.actionDecrease_force_size.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Alt+[", None, -1))
        self.actionIncrease_Geometry_size.setText(QtWidgets.QApplication.translate("MainWindow", "Increase Geometry size (poi, axis)", None, -1))
        self.actionIncrease_Geometry_size.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Alt+Shift+]", None, -1))
        self.actionDecrease_Geometry_size.setText(QtWidgets.QApplication.translate("MainWindow", "Decrease Geometry size", None, -1))
        self.actionDecrease_Geometry_size.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Alt+Shift+[", None, -1))
        self.actionPython_console.setText(QtWidgets.QApplication.translate("MainWindow", "Python console", None, -1))
        self.actionGoal_seek.setText(QtWidgets.QApplication.translate("MainWindow", "Goal-seek (one variable)", None, -1))
        self.actionStability_curve.setText(QtWidgets.QApplication.translate("MainWindow", "Stability-curve", None, -1))
        self.actionOptimize.setText(QtWidgets.QApplication.translate("MainWindow", "TODO: Optimize (multiple variables)", None, -1))
        self.actionOpen.setText(QtWidgets.QApplication.translate("MainWindow", "Open", None, -1))
        self.actionImport_browser.setText(QtWidgets.QApplication.translate("MainWindow", "Import (browser)", None, -1))
        self.actionRender_current_view.setText(QtWidgets.QApplication.translate("MainWindow", "Render current view", None, -1))
        self.actionModal_shapes.setText(QtWidgets.QApplication.translate("MainWindow", "Modal shapes", None, -1))
        self.actionInertia_properties.setText(QtWidgets.QApplication.translate("MainWindow", "Inertia properties", None, -1))
        self.actionSave_actions_as.setText(QtWidgets.QApplication.translate("MainWindow", "Save actions as", None, -1))
        self.actionsee_open_ocean_org.setText(QtWidgets.QApplication.translate("MainWindow", "see open-ocean.org", None, -1))
        self.actionX.setText(QtWidgets.QApplication.translate("MainWindow", "X", None, -1))
        self.action_x.setText(QtWidgets.QApplication.translate("MainWindow", "-X", None, -1))
        self.actionY.setText(QtWidgets.QApplication.translate("MainWindow", "Y", None, -1))
        self.action_Y.setText(QtWidgets.QApplication.translate("MainWindow", "-Y", None, -1))
        self.actionZ.setText(QtWidgets.QApplication.translate("MainWindow", "From top", None, -1))
        self.action_Z.setText(QtWidgets.QApplication.translate("MainWindow", "From bottom", None, -1))
        self.actionLook_towards_center.setText(QtWidgets.QApplication.translate("MainWindow", "Look towards center", None, -1))
        self.actionCamera_reset.setText(QtWidgets.QApplication.translate("MainWindow", "Camera reset", None, -1))
        self.actionShow_CoG_positions.setText(QtWidgets.QApplication.translate("MainWindow", "Show CoGs", None, -1))
        self.actionBlender.setText(QtWidgets.QApplication.translate("MainWindow", "Blender", None, -1))
        self.actionOrcaflex.setText(QtWidgets.QApplication.translate("MainWindow", "Orcaflex .yml", None, -1))
        self.actionOrcaflex_package.setText(QtWidgets.QApplication.translate("MainWindow", "Orcaflex run and collect package", None, -1))
        self.actionPython_console_2.setText(QtWidgets.QApplication.translate("MainWindow", "Python console", None, -1))
        self.actionVersion.setText(QtWidgets.QApplication.translate("MainWindow", "Version", None, -1))
        self.actionOnline_help.setText(QtWidgets.QApplication.translate("MainWindow", "Online help", None, -1))

import DAVE.gui.forms.resources_rc
