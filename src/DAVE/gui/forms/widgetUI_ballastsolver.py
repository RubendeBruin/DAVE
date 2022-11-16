# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_ballastsolver.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_BallastSolver(object):
    def setupUi(self, BallastSolver):
        if not BallastSolver.objectName():
            BallastSolver.setObjectName(u"BallastSolver")
        BallastSolver.resize(219, 598)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BallastSolver.sizePolicy().hasHeightForWidth())
        BallastSolver.setSizePolicy(sizePolicy)
        BallastSolver.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(BallastSolver)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(BallastSolver)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(BallastSolver)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_4)

        self.label_2 = QLabel(BallastSolver)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.doubleSpinBox = QDoubleSpinBox(BallastSolver)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setMinimum(-99999999999999.000000000000000)
        self.doubleSpinBox.setMaximum(99999999999999.000000000000000)
        self.doubleSpinBox.setSingleStep(0.250000000000000)
        self.doubleSpinBox.setValue(-5.000000000000000)

        self.verticalLayout.addWidget(self.doubleSpinBox)

        self.pushButton = QPushButton(BallastSolver)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.tableWidget = QTableWidget(BallastSolver)
        if (self.tableWidget.columnCount() < 1):
            self.tableWidget.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.tableWidget.rowCount() < 3):
            self.tableWidget.setRowCount(3)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem3)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)
        self.tableWidget.setMaximumSize(QSize(16777215, 174))
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setProperty("showDropIndicator", True)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(0)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tableWidget)

        self.widget = QWidget(BallastSolver)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cbUseCurrentFills = QCheckBox(self.widget_2)
        self.cbUseCurrentFills.setObjectName(u"cbUseCurrentFills")

        self.verticalLayout_2.addWidget(self.cbUseCurrentFills)

        self.pushButton_2 = QPushButton(self.widget_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.widget_2)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_2.addWidget(self.pushButton_3)


        self.gridLayout.addWidget(self.widget_2, 1, 0, 1, 2)


        self.verticalLayout.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(BallastSolver)

        QMetaObject.connectSlotsByName(BallastSolver)
    # setupUi

    def retranslateUi(self, BallastSolver):
        BallastSolver.setWindowTitle(QCoreApplication.translate("BallastSolver", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("BallastSolver", u"Ballast", None))
        self.label_4.setText(QCoreApplication.translate("BallastSolver", u"VESSEL", None))
        self.label_2.setText(QCoreApplication.translate("BallastSolver", u"to an even-keel conditions at vertical position of:", None))
        self.pushButton.setText(QCoreApplication.translate("BallastSolver", u"Determine required ballast weight and position", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("BallastSolver", u"Value", None));
        ___qtablewidgetitem1 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("BallastSolver", u"Volume", None));
        ___qtablewidgetitem2 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("BallastSolver", u"X", None));
        ___qtablewidgetitem3 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("BallastSolver", u"Y", None));
        self.cbUseCurrentFills.setText(QCoreApplication.translate("BallastSolver", u"Use current tank-fills as start point for solution", None))
        self.pushButton_2.setText(QCoreApplication.translate("BallastSolver", u"Solve tank fillings", None))
        self.pushButton_3.setText(QCoreApplication.translate("BallastSolver", u"Solve tank fillings (alt. method)", None))
    # retranslateUi

