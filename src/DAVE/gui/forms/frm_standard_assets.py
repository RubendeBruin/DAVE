# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_standard_assets.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

# import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.ApplicationModal)
        MainWindow.resize(1000, 800)
        MainWindow.setAcceptDrops(True)
        icon = QIcon()
        icon.addFile(u":/icons/Dave_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.actionSave_scene = QAction(MainWindow)
        self.actionSave_scene.setObjectName(u"actionSave_scene")
        self.actionImport_sub_scene = QAction(MainWindow)
        self.actionImport_sub_scene.setObjectName(u"actionImport_sub_scene")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionHorizontal_camera = QAction(MainWindow)
        self.actionHorizontal_camera.setObjectName(u"actionHorizontal_camera")
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action2D_mode = QAction(MainWindow)
        self.action2D_mode.setObjectName(u"action2D_mode")
        self.action2D_mode.setCheckable(True)
        self.actionDark_mode = QAction(MainWindow)
        self.actionDark_mode.setObjectName(u"actionDark_mode")
        self.actionDark_mode.setCheckable(False)
        self.actionShow_visuals = QAction(MainWindow)
        self.actionShow_visuals.setObjectName(u"actionShow_visuals")
        self.actionShow_visuals.setCheckable(True)
        self.actionShow_visuals.setChecked(True)
        self.actionShow_Geometry_elements = QAction(MainWindow)
        self.actionShow_Geometry_elements.setObjectName(u"actionShow_Geometry_elements")
        self.actionShow_Geometry_elements.setCheckable(True)
        self.actionShow_Geometry_elements.setChecked(True)
        self.actionShow_force_applyting_element = QAction(MainWindow)
        self.actionShow_force_applyting_element.setObjectName(u"actionShow_force_applyting_element")
        self.actionShow_force_applyting_element.setCheckable(True)
        self.actionShow_force_applyting_element.setChecked(True)
        self.actionSet_all_visible = QAction(MainWindow)
        self.actionSet_all_visible.setObjectName(u"actionSet_all_visible")
        self.actionSet_all_hidden = QAction(MainWindow)
        self.actionSet_all_hidden.setObjectName(u"actionSet_all_hidden")
        self.actionFull_refresh = QAction(MainWindow)
        self.actionFull_refresh.setObjectName(u"actionFull_refresh")
        self.actionShow_water_plane = QAction(MainWindow)
        self.actionShow_water_plane.setObjectName(u"actionShow_water_plane")
        self.actionShow_water_plane.setCheckable(True)
        self.actionShow_water_plane.setChecked(False)
        self.actionAdd_light = QAction(MainWindow)
        self.actionAdd_light.setObjectName(u"actionAdd_light")
        self.actionShow_all_forces_at_same_size = QAction(MainWindow)
        self.actionShow_all_forces_at_same_size.setObjectName(u"actionShow_all_forces_at_same_size")
        self.actionShow_all_forces_at_same_size.setCheckable(True)
        self.actionShow_all_forces_at_same_size.setChecked(True)
        self.actionIncrease_force_size = QAction(MainWindow)
        self.actionIncrease_force_size.setObjectName(u"actionIncrease_force_size")
        self.actionDecrease_force_size = QAction(MainWindow)
        self.actionDecrease_force_size.setObjectName(u"actionDecrease_force_size")
        self.actionIncrease_Geometry_size = QAction(MainWindow)
        self.actionIncrease_Geometry_size.setObjectName(u"actionIncrease_Geometry_size")
        self.actionDecrease_Geometry_size = QAction(MainWindow)
        self.actionDecrease_Geometry_size.setObjectName(u"actionDecrease_Geometry_size")
        self.actionPython_console = QAction(MainWindow)
        self.actionPython_console.setObjectName(u"actionPython_console")
        self.actionGoal_seek = QAction(MainWindow)
        self.actionGoal_seek.setObjectName(u"actionGoal_seek")
        self.actionStability_curve = QAction(MainWindow)
        self.actionStability_curve.setObjectName(u"actionStability_curve")
        self.actionOptimize = QAction(MainWindow)
        self.actionOptimize.setObjectName(u"actionOptimize")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.horizontalLayout = QHBoxLayout(MainWindow)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(MainWindow)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy1)
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame_4)
        self.formLayout.setObjectName(u"formLayout")
        self.checkBox = QCheckBox(self.frame_4)
        self.checkBox.setObjectName(u"checkBox")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.checkBox)

        self.btnImport = QPushButton(self.frame_4)
        self.btnImport.setObjectName(u"btnImport")

        self.formLayout.setWidget(5, QFormLayout.SpanningRole, self.btnImport)

        self.txtPrefix = QLineEdit(self.frame_4)
        self.txtPrefix.setObjectName(u"txtPrefix")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.txtPrefix)

        self.label_19 = QLabel(self.frame_4)
        self.label_19.setObjectName(u"label_19")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_19)


        self.verticalLayout.addWidget(self.frame_4)

        self.lblInfo = QLabel(self.frame)
        self.lblInfo.setObjectName(u"lblInfo")

        self.verticalLayout.addWidget(self.lblInfo)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.frame_5)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_5.addWidget(self.lineEdit)


        self.verticalLayout.addWidget(self.frame_5)

        self.listWidget = QListWidget(self.frame)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listWidget.setProperty("showDropIndicator", False)
        self.listWidget.setDefaultDropAction(Qt.IgnoreAction)
        self.listWidget.setAlternatingRowColors(True)

        self.verticalLayout.addWidget(self.listWidget)


        self.horizontalLayout.addWidget(self.frame)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame3d = QFrame(MainWindow)
        self.frame3d.setObjectName(u"frame3d")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame3d.sizePolicy().hasHeightForWidth())
        self.frame3d.setSizePolicy(sizePolicy2)
        self.frame3d.setAcceptDrops(False)
        self.frame3d.setFrameShape(QFrame.NoFrame)
        self.frame3d.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_2.addWidget(self.frame3d)


        self.horizontalLayout.addLayout(self.horizontalLayout_2)

        QWidget.setTabOrder(self.checkBox, self.btnImport)
        QWidget.setTabOrder(self.btnImport, self.lineEdit)

        self.retranslateUi(MainWindow)

        self.btnImport.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Standard assets", None))
        self.actionSave_scene.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
        self.actionImport_sub_scene.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionHorizontal_camera.setText(QCoreApplication.translate("MainWindow", u"Level camera (make horizon horizontal)", None))
#if QT_CONFIG(shortcut)
        self.actionHorizontal_camera.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+L", None))
#endif // QT_CONFIG(shortcut)
        self.action.setText(QCoreApplication.translate("MainWindow", u"---", None))
        self.action2D_mode.setText(QCoreApplication.translate("MainWindow", u"2D mode", None))
        self.actionDark_mode.setText(QCoreApplication.translate("MainWindow", u"Make darker", None))
#if QT_CONFIG(shortcut)
        self.actionDark_mode.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+-", None))
#endif // QT_CONFIG(shortcut)
        self.actionShow_visuals.setText(QCoreApplication.translate("MainWindow", u"Show visuals", None))
        self.actionShow_Geometry_elements.setText(QCoreApplication.translate("MainWindow", u"Show Geometry elements", None))
        self.actionShow_force_applyting_element.setText(QCoreApplication.translate("MainWindow", u"Show non-geometry elements", None))
        self.actionSet_all_visible.setText(QCoreApplication.translate("MainWindow", u"Set all visible", None))
        self.actionSet_all_hidden.setText(QCoreApplication.translate("MainWindow", u"Set all hidden", None))
        self.actionFull_refresh.setText(QCoreApplication.translate("MainWindow", u"Full refresh", None))
        self.actionShow_water_plane.setText(QCoreApplication.translate("MainWindow", u"Show water-plane", None))
        self.actionAdd_light.setText(QCoreApplication.translate("MainWindow", u"Make lighter", None))
#if QT_CONFIG(shortcut)
        self.actionAdd_light.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+=", None))
#endif // QT_CONFIG(shortcut)
        self.actionShow_all_forces_at_same_size.setText(QCoreApplication.translate("MainWindow", u"Show all forces same size (normalize)", None))
        self.actionIncrease_force_size.setText(QCoreApplication.translate("MainWindow", u"Increase force size", None))
#if QT_CONFIG(shortcut)
        self.actionIncrease_force_size.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+]", None))
#endif // QT_CONFIG(shortcut)
        self.actionDecrease_force_size.setText(QCoreApplication.translate("MainWindow", u"Decrease force size", None))
#if QT_CONFIG(shortcut)
        self.actionDecrease_force_size.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+[", None))
#endif // QT_CONFIG(shortcut)
        self.actionIncrease_Geometry_size.setText(QCoreApplication.translate("MainWindow", u"Increase Geometry size (poi, axis)", None))
#if QT_CONFIG(shortcut)
        self.actionIncrease_Geometry_size.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+Shift+]", None))
#endif // QT_CONFIG(shortcut)
        self.actionDecrease_Geometry_size.setText(QCoreApplication.translate("MainWindow", u"Decrease Geometry size", None))
#if QT_CONFIG(shortcut)
        self.actionDecrease_Geometry_size.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+Shift+[", None))
#endif // QT_CONFIG(shortcut)
        self.actionPython_console.setText(QCoreApplication.translate("MainWindow", u"Python console", None))
        self.actionGoal_seek.setText(QCoreApplication.translate("MainWindow", u"Goal-seek (one variable)", None))
        self.actionStability_curve.setText(QCoreApplication.translate("MainWindow", u"Stability-curve", None))
        self.actionOptimize.setText(QCoreApplication.translate("MainWindow", u"TODO: Optimize (multiple variables)", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Place imported asset in a container axis", None))
        self.btnImport.setText(QCoreApplication.translate("MainWindow", u"Import this asset", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Apply pre-fix to element names:", None))
        self.lblInfo.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
    # retranslateUi

