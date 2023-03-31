# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlg_export_to_blender.ui',
# licensing of 'dlg_export_to_blender.ui' applies.
#
# Created: Fri Mar 31 17:25:12 2023
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(482, 160)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.sbFrames_per_step = QtWidgets.QSpinBox(Dialog)
        self.sbFrames_per_step.setMinimum(1)
        self.sbFrames_per_step.setMaximum(9999)
        self.sbFrames_per_step.setProperty("value", 24)
        self.sbFrames_per_step.setObjectName("sbFrames_per_step")
        self.gridLayout.addWidget(self.sbFrames_per_step, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 3, 1, 1)
        self.teExecutable = QtWidgets.QLineEdit(Dialog)
        self.teExecutable.setObjectName("teExecutable")
        self.gridLayout.addWidget(self.teExecutable, 3, 1, 1, 2)
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout.addWidget(self.radioButton, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 3, 1, 1)
        self.cbBaseScene = QtWidgets.QComboBox(Dialog)
        self.cbBaseScene.setEditable(True)
        self.cbBaseScene.setObjectName("cbBaseScene")
        self.gridLayout.addWidget(self.cbBaseScene, 2, 1, 1, 2)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnOK = QtWidgets.QPushButton(self.frame)
        self.btnOK.setObjectName("btnOK")
        self.horizontalLayout.addWidget(self.btnOK)
        self.btnCancel = QtWidgets.QPushButton(self.frame)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.gridLayout.addWidget(self.frame, 4, 2, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("Dialog", ".blend file", None, -1))
        self.radioButton_2.setText(QtWidgets.QApplication.translate("Dialog", "All frames from timeline with", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Blender template file", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Blender executable:", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Dialog", "blender-launcher.exe", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "Export", None, -1))
        self.radioButton.setText(QtWidgets.QApplication.translate("Dialog", "Current view (image)", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Dialog", "frames per step", None, -1))
        self.btnOK.setText(QtWidgets.QApplication.translate("Dialog", "Export", None, -1))
        self.btnCancel.setText(QtWidgets.QApplication.translate("Dialog", "Cancel", None, -1))

