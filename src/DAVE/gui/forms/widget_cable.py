# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_cable.ui',
# licensing of 'widget_cable.ui' applies.
#
# Created: Wed Mar  2 18:17:17 2022
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Cable_form(object):
    def setupUi(self, Cable_form):
        Cable_form.setObjectName("Cable_form")
        Cable_form.resize(289, 690)
        Cable_form.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout = QtWidgets.QVBoxLayout(Cable_form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(Cable_form)
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
        self.frame_2 = QtWidgets.QFrame(Cable_form)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.formLayout = QtWidgets.QFormLayout(self.frame_2)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.doubleSpinBox_1 = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_1.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-1e+18)
        self.doubleSpinBox_1.setMaximum(999999999999.0)
        self.doubleSpinBox_1.setObjectName("doubleSpinBox_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_1)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(0.0)
        self.doubleSpinBox_2.setMaximum(999999999999.0)
        self.doubleSpinBox_2.setSingleStep(1000.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_2)
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox.setSingleStep(0.001)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox)
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setSingleStep(0.001)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_3)
        self.label_9 = QtWidgets.QLabel(self.frame_2)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_4.setDecimals(3)
        self.doubleSpinBox_4.setMaximum(999999.0)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_4)
        self.verticalLayout.addWidget(self.frame_2)
        self.label_6 = QtWidgets.QLabel(Cable_form)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.frame = QtWidgets.QFrame(Cable_form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setWordWrap(True)
        self.label_3.setIndent(-1)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.cbPointsAndCircles = QtWidgets.QComboBox(self.frame)
        self.cbPointsAndCircles.setEditable(True)
        self.cbPointsAndCircles.setObjectName("cbPointsAndCircles")
        self.gridLayout.addWidget(self.cbPointsAndCircles, 1, 0, 1, 1)
        self.list = QtWidgets.QListWidget(self.frame)
        self.list.setObjectName("list")
        self.gridLayout.addWidget(self.list, 4, 0, 1, 2)
        self.pbRemoveSelected = QtWidgets.QPushButton(self.frame)
        self.pbRemoveSelected.setObjectName("pbRemoveSelected")
        self.gridLayout.addWidget(self.pbRemoveSelected, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.lbDirection = QtWidgets.QLabel(self.frame)
        self.lbDirection.setWordWrap(True)
        self.lbDirection.setObjectName("lbDirection")
        self.gridLayout.addWidget(self.lbDirection, 3, 0, 1, 2)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Cable_form)
        QtCore.QMetaObject.connectSlotsByName(Cable_form)
        Cable_form.setTabOrder(self.doubleSpinBox_1, self.doubleSpinBox_2)

    def retranslateUi(self, Cable_form):
        Cable_form.setWindowTitle(QtWidgets.QApplication.translate("Cable_form", "Form", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("Cable_form", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Cable properties</span></p></body></html>", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Cable_form", "Length at rest [m]", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Cable_form", "Stiffness EA [kN]", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Cable_form", "Diameter [m]", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Cable_form", "Mass per length [mT/m] *", None, -1))
        self.label_9.setText(QtWidgets.QApplication.translate("Cable_form", "Mass [mT]", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("Cable_form", "* Intended for lift-rigging calculations. Mass is only accurately accounted for when cable is tension exceeds its own weight. Mass is calculated from mass_per_length.", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Cable_form", "Add", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Cable_form", "A cable can run between and over points and circles. ", None, -1))
        self.pbRemoveSelected.setText(QtWidgets.QApplication.translate("Cable_form", "Remove selected point", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("Cable_form", "Drag items to change order. You can also drag items from the node-tree to add them", None, -1))
        self.lbDirection.setText(QtWidgets.QApplication.translate("Cable_form", "For circles the direction in which the cable runs over it is defined by the axis of the circle. Check the box to run over the circle in opposite direction.", None, -1))

