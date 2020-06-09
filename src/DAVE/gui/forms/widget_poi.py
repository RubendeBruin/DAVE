# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_poi.ui',
# licensing of 'widget_poi.ui' applies.
#
# Created: Tue Jun  9 08:30:22 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Poi(object):
    def setupUi(self, Poi):
        Poi.setObjectName("Poi")
        Poi.resize(400, 361)
        self.verticalLayout = QtWidgets.QVBoxLayout(Poi)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(Poi)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_7.setAutoFillBackground(False)
        self.label_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.frame_2 = QtWidgets.QFrame(Poi)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(-1e+18)
        self.doubleSpinBox_2.setMaximum(999999999999.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.gridLayout.addWidget(self.doubleSpinBox_2, 6, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setMinimum(-1e+18)
        self.doubleSpinBox_3.setMaximum(999999999999.0)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.gridLayout.addWidget(self.doubleSpinBox_3, 7, 1, 1, 1)
        self.doubleSpinBox_1 = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_1.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-1e+18)
        self.doubleSpinBox_1.setMaximum(999999999999.0)
        self.doubleSpinBox_1.setObjectName("doubleSpinBox_1")
        self.gridLayout.addWidget(self.doubleSpinBox_1, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Poi)
        QtCore.QMetaObject.connectSlotsByName(Poi)
        Poi.setTabOrder(self.doubleSpinBox_1, self.doubleSpinBox_2)
        Poi.setTabOrder(self.doubleSpinBox_2, self.doubleSpinBox_3)

    def retranslateUi(self, Poi):
        Poi.setWindowTitle(QtWidgets.QApplication.translate("Poi", "Form", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("Poi", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Position on parent</span></p></body></html>", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Poi", "Z - position", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Poi", "X - position", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Poi", "Y - position", None, -1))

