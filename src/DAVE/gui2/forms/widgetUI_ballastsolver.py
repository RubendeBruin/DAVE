# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_ballastsolver.ui',
# licensing of 'widget_ballastsolver.ui' applies.
#
# Created: Mon Dec  9 15:49:21 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_BallastSolver(object):
    def setupUi(self, BallastSolver):
        BallastSolver.setObjectName("BallastSolver")
        BallastSolver.resize(266, 556)
        BallastSolver.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout = QtWidgets.QVBoxLayout(BallastSolver)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(BallastSolver)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(BallastSolver)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.line = QtWidgets.QFrame(BallastSolver)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_3 = QtWidgets.QLabel(BallastSolver)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(BallastSolver)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_2 = QtWidgets.QLabel(BallastSolver)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(BallastSolver)
        self.doubleSpinBox.setMinimum(-99999999999999.0)
        self.doubleSpinBox.setMaximum(99999999999999.0)
        self.doubleSpinBox.setProperty("value", -5.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.verticalLayout.addWidget(self.doubleSpinBox)
        self.line_2 = QtWidgets.QFrame(BallastSolver)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.pushButton = QtWidgets.QPushButton(BallastSolver)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.tableWidget = QtWidgets.QTableWidget(BallastSolver)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.line_3 = QtWidgets.QFrame(BallastSolver)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.pushButton_2 = QtWidgets.QPushButton(BallastSolver)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.label_5 = QtWidgets.QLabel(BallastSolver)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)

        self.retranslateUi(BallastSolver)
        QtCore.QMetaObject.connectSlotsByName(BallastSolver)

    def retranslateUi(self, BallastSolver):
        BallastSolver.setWindowTitle(QtWidgets.QApplication.translate("BallastSolver", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("BallastSolver", "Ballast system:", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("BallastSolver", "Ballast", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("BallastSolver", "VESSEL", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("BallastSolver", "to an even-keel conditions at vertical position of:", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("BallastSolver", "1. Determine required ballast", None, -1))
        self.tableWidget.verticalHeaderItem(0).setText(QtWidgets.QApplication.translate("BallastSolver", "Volume", None, -1))
        self.tableWidget.verticalHeaderItem(1).setText(QtWidgets.QApplication.translate("BallastSolver", "X", None, -1))
        self.tableWidget.verticalHeaderItem(2).setText(QtWidgets.QApplication.translate("BallastSolver", "Y", None, -1))
        self.tableWidget.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("BallastSolver", "Value", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("BallastSolver", "2. Solve tank fillings", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("BallastSolver", "Result", None, -1))

