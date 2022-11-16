# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_animation.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_AnimationWindow(object):
    def setupUi(self, AnimationWindow):
        if not AnimationWindow.objectName():
            AnimationWindow.setObjectName(u"AnimationWindow")
        AnimationWindow.resize(1408, 1191)
        AnimationWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.centralwidget = QWidget(AnimationWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame3d = QFrame(self.centralwidget)
        self.frame3d.setObjectName(u"frame3d")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.frame3d.sizePolicy().hasHeightForWidth())
        self.frame3d.setSizePolicy(sizePolicy)
        self.frame3d.setSizeIncrement(QSize(8, 8))
        self.frame3d.setFrameShape(QFrame.StyledPanel)
        self.frame3d.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.frame3d)

        AnimationWindow.setCentralWidget(self.centralwidget)
        self.dockWidget = QDockWidget(AnimationWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dockWidget.sizePolicy().hasHeightForWidth())
        self.dockWidget.setSizePolicy(sizePolicy1)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        sizePolicy1.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.dockWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)

        self.horizontalSlider_2 = QSlider(self.dockWidgetContents)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setMinimum(1)
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setValue(10)
        self.horizontalSlider_2.setOrientation(Qt.Vertical)

        self.gridLayout.addWidget(self.horizontalSlider_2, 3, 1, 1, 1)

        self.label = QLabel(self.dockWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.horizontalSlider = QSlider(self.dockWidgetContents)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Vertical)

        self.gridLayout.addWidget(self.horizontalSlider, 3, 0, 1, 1)

        self.lblRads = QLabel(self.dockWidgetContents)
        self.lblRads.setObjectName(u"lblRads")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblRads.setFont(font)

        self.gridLayout.addWidget(self.lblRads, 1, 0, 1, 1)

        self.lblPeriod = QLabel(self.dockWidgetContents)
        self.lblPeriod.setObjectName(u"lblPeriod")
        self.lblPeriod.setFont(font)

        self.gridLayout.addWidget(self.lblPeriod, 0, 0, 1, 1)

        self.dockWidget.setWidget(self.dockWidgetContents)
        AnimationWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        self.dockWidget_2 = QDockWidget(AnimationWindow)
        self.dockWidget_2.setObjectName(u"dockWidget_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.dockWidget_2.sizePolicy().hasHeightForWidth())
        self.dockWidget_2.setSizePolicy(sizePolicy2)
        self.dockWidget_2.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.dockWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents_2.setSizePolicy(sizePolicy3)
        self.horizontalLayout_2 = QHBoxLayout(self.dockWidgetContents_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tableWidget = QTableWidget(self.dockWidgetContents_2)
        if (self.tableWidget.columnCount() < 7):
            self.tableWidget.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy2.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy2)
        self.tableWidget.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.tableWidget.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_2.addWidget(self.tableWidget)

        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        AnimationWindow.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget_2)
        self.dockWidget_3 = QDockWidget(AnimationWindow)
        self.dockWidget_3.setObjectName(u"dockWidget_3")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.dockWidget_3.sizePolicy().hasHeightForWidth())
        self.dockWidget_3.setSizePolicy(sizePolicy4)
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btnStatics = QPushButton(self.dockWidgetContents_3)
        self.btnStatics.setObjectName(u"btnStatics")

        self.verticalLayout.addWidget(self.btnStatics)

        self.pushButton = QPushButton(self.dockWidgetContents_3)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.dockWidgetContents_3)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.dockWidget_3.setWidget(self.dockWidgetContents_3)
        AnimationWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget_3)
        self.dockWidget_4 = QDockWidget(AnimationWindow)
        self.dockWidget_4.setObjectName(u"dockWidget_4")
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName(u"dockWidgetContents_4")
        self.dockWidget_4.setWidget(self.dockWidgetContents_4)
        AnimationWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_4)

        self.retranslateUi(AnimationWindow)

        QMetaObject.connectSlotsByName(AnimationWindow)
    # setupUi

    def retranslateUi(self, AnimationWindow):
        AnimationWindow.setWindowTitle(QCoreApplication.translate("AnimationWindow", u"MainWindow", None))
        self.dockWidget.setWindowTitle(QCoreApplication.translate("AnimationWindow", u"View", None))
        self.label_2.setText(QCoreApplication.translate("AnimationWindow", u"Scale", None))
        self.label.setText(QCoreApplication.translate("AnimationWindow", u"Mode-shape", None))
        self.lblRads.setText(QCoreApplication.translate("AnimationWindow", u"Frequency", None))
        self.lblPeriod.setText(QCoreApplication.translate("AnimationWindow", u"Period", None))
        self.dockWidget_2.setWindowTitle(QCoreApplication.translate("AnimationWindow", u"DOF summary", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("AnimationWindow", u"Exitation", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("AnimationWindow", u"Linear Inertia", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("AnimationWindow", u"Radius", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("AnimationWindow", u"Total inc. children", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("AnimationWindow", u"Stiffness", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("AnimationWindow", u"unconstrained", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("AnimationWindow", u"no-inertia", None));
        self.dockWidget_3.setWindowTitle(QCoreApplication.translate("AnimationWindow", u"Actions", None))
        self.btnStatics.setText(QCoreApplication.translate("AnimationWindow", u"Solve statics", None))
        self.pushButton.setText(QCoreApplication.translate("AnimationWindow", u"Update model", None))
        self.pushButton_2.setText(QCoreApplication.translate("AnimationWindow", u"Quick-fix model", None))
        self.dockWidget_4.setWindowTitle(QCoreApplication.translate("AnimationWindow", u"Dynamic properties", None))
    # retranslateUi

