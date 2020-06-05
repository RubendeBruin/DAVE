# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_selection_actions.ui',
# licensing of 'widget_selection_actions.ui' applies.
#
# Created: Thu May 14 16:14:05 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SelectionActions(object):
    def setupUi(self, SelectionActions):
        SelectionActions.setObjectName("SelectionActions")
        SelectionActions.resize(1185, 324)
        self.verticalLayout = QtWidgets.QVBoxLayout(SelectionActions)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(SelectionActions)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.frame = QtWidgets.QFrame(SelectionActions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(SelectionActions)
        QtCore.QMetaObject.connectSlotsByName(SelectionActions)

    def retranslateUi(self, SelectionActions):
        SelectionActions.setWindowTitle(QtWidgets.QApplication.translate("SelectionActions", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("SelectionActions", "Selected elements", None, -1))

