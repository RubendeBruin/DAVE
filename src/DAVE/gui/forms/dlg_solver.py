# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlg_solver.ui',
# licensing of 'dlg_solver.ui' applies.
#
# Created: Fri Nov  1 11:11:55 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(336, 142)
        Dialog.setWindowOpacity(1.0)
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        Dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.btnTerminate = QtWidgets.QPushButton(Dialog)
        self.btnTerminate.setObjectName("btnTerminate")
        self.verticalLayout.addWidget(self.btnTerminate)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Working", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Doing what you told me to do.", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "< Info >", None, -1))
        self.btnTerminate.setText(QtWidgets.QApplication.translate("Dialog", "Terminate solver", None, -1))

