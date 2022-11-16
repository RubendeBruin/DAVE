# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_modeshapes.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_ModeShapesWidget(object):
    def setupUi(self, ModeShapesWidget):
        if not ModeShapesWidget.objectName():
            ModeShapesWidget.setObjectName(u"ModeShapesWidget")
        ModeShapesWidget.resize(1333, 385)
        self.gridLayout = QGridLayout(ModeShapesWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(ModeShapesWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget = QTableWidget(self.frame)
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
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setSortingEnabled(False)

        self.verticalLayout.addWidget(self.tableWidget)


        self.gridLayout.addWidget(self.frame, 3, 2, 1, 4)

        self.line = QFrame(ModeShapesWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 0, 1, 1, 1)

        self.line_2 = QFrame(ModeShapesWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 0, 3, 1, 1)

        self.line_3 = QFrame(ModeShapesWidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_3, 1, 3, 1, 1)

        self.line_4 = QFrame(ModeShapesWidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_4, 1, 1, 1, 1)

        self.frame_2 = QFrame(ModeShapesWidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.pushButton_2 = QPushButton(self.frame_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.gridLayout.addWidget(self.frame_2, 3, 0, 1, 1)

        self.btnCalc = QPushButton(ModeShapesWidget)
        self.btnCalc.setObjectName(u"btnCalc")
        self.btnCalc.setCheckable(False)
        self.btnCalc.setChecked(False)

        self.gridLayout.addWidget(self.btnCalc, 0, 0, 1, 1)

        self.label = QLabel(ModeShapesWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 4, 1, 1)

        self.lblPeriod = QLabel(ModeShapesWidget)
        self.lblPeriod.setObjectName(u"lblPeriod")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblPeriod.setFont(font)

        self.gridLayout.addWidget(self.lblPeriod, 0, 2, 1, 1)

        self.label_2 = QLabel(ModeShapesWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 4, 1, 1)

        self.sliderSize = QSlider(ModeShapesWidget)
        self.sliderSize.setObjectName(u"sliderSize")
        self.sliderSize.setMinimum(1)
        self.sliderSize.setMaximum(100)
        self.sliderSize.setValue(10)
        self.sliderSize.setOrientation(Qt.Horizontal)
        self.sliderSize.setTickPosition(QSlider.NoTicks)

        self.gridLayout.addWidget(self.sliderSize, 1, 5, 1, 1)

        self.horizontalSlider = QSlider(ModeShapesWidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QSlider.TicksAbove)

        self.gridLayout.addWidget(self.horizontalSlider, 0, 5, 1, 1)

        self.lblRads = QLabel(ModeShapesWidget)
        self.lblRads.setObjectName(u"lblRads")
        self.lblRads.setFont(font)

        self.gridLayout.addWidget(self.lblRads, 1, 2, 1, 1)

        self.lblError = QLabel(ModeShapesWidget)
        self.lblError.setObjectName(u"lblError")
        self.lblError.setFont(font)
        self.lblError.setStyleSheet(u"color:rgb(200, 0, 0)")
        self.lblError.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.lblError.setTextFormat(Qt.AutoText)

        self.gridLayout.addWidget(self.lblError, 1, 0, 1, 1)


        self.retranslateUi(ModeShapesWidget)

        QMetaObject.connectSlotsByName(ModeShapesWidget)
    # setupUi

    def retranslateUi(self, ModeShapesWidget):
        ModeShapesWidget.setWindowTitle(QCoreApplication.translate("ModeShapesWidget", u"Form", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ModeShapesWidget", u"Exitation", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ModeShapesWidget", u"Linear Inertia", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ModeShapesWidget", u"Radius", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("ModeShapesWidget", u"Total inc. children", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("ModeShapesWidget", u"Stiffness", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("ModeShapesWidget", u"unconstrained", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("ModeShapesWidget", u"no-inertia", None));
        self.pushButton_2.setText(QCoreApplication.translate("ModeShapesWidget", u"Quick-fix model", None))
        self.btnCalc.setText(QCoreApplication.translate("ModeShapesWidget", u"Calculate Modeshapes", None))
        self.label.setText(QCoreApplication.translate("ModeShapesWidget", u"Mode-shape", None))
        self.lblPeriod.setText(QCoreApplication.translate("ModeShapesWidget", u"Period", None))
        self.label_2.setText(QCoreApplication.translate("ModeShapesWidget", u"Scale", None))
        self.lblRads.setText(QCoreApplication.translate("ModeShapesWidget", u"Frequency", None))
        self.lblError.setText(QCoreApplication.translate("ModeShapesWidget", u"warning/error", None))
    # retranslateUi

