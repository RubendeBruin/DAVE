# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_selection_actions.ui',
# licensing of 'widget_selection_actions.ui' applies.
#
# Created: Fri Jun 12 09:31:29 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SelectionActions(object):
    def setupUi(self, SelectionActions):
        SelectionActions.setObjectName("SelectionActions")
        SelectionActions.resize(1185, 829)
        self.verticalLayout = QtWidgets.QVBoxLayout(SelectionActions)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(SelectionActions)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.scrollArea = QtWidgets.QScrollArea(SelectionActions)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1185, 801))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2.addWidget(self.frame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(SelectionActions)
        QtCore.QMetaObject.connectSlotsByName(SelectionActions)

    def retranslateUi(self, SelectionActions):
        SelectionActions.setWindowTitle(QtWidgets.QApplication.translate("SelectionActions", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("SelectionActions", "Selected elements", None, -1))

