# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_limits.ui',
# licensing of 'widget_limits.ui' applies.
#
# Created: Tue Oct  5 14:10:39 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DockLimits(object):
    def setupUi(self, DockLimits):
        DockLimits.setObjectName("DockLimits")
        DockLimits.resize(312, 655)
        self.verticalLayout = QtWidgets.QVBoxLayout(DockLimits)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(DockLimits)
        self.widget.setMinimumSize(QtCore.QSize(400, 0))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lbPropHelp = QtWidgets.QLabel(self.widget)
        self.lbPropHelp.setToolTipDuration(0)
        self.lbPropHelp.setWordWrap(True)
        self.lbPropHelp.setObjectName("lbPropHelp")
        self.gridLayout.addWidget(self.lbPropHelp, 3, 2, 1, 1)
        self.lbNodeClass = QtWidgets.QLabel(self.widget)
        self.lbNodeClass.setObjectName("lbNodeClass")
        self.gridLayout.addWidget(self.lbNodeClass, 1, 2, 1, 1)
        self.cbProperty = QtWidgets.QComboBox(self.widget)
        self.cbProperty.setObjectName("cbProperty")
        self.gridLayout.addWidget(self.cbProperty, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setToolTip("")
        self.lineEdit.setToolTipDuration(-1)
        self.lineEdit.setStatusTip("")
        self.lineEdit.setPlaceholderText("")
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 4, 2, 1, 1)
        self.cbNode = QtWidgets.QComboBox(self.widget)
        self.cbNode.setObjectName("cbNode")
        self.gridLayout.addWidget(self.cbNode, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lbResult = QtWidgets.QLabel(self.widget)
        self.lbResult.setWordWrap(True)
        self.lbResult.setObjectName("lbResult")
        self.gridLayout.addWidget(self.lbResult, 5, 2, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbApply = QtWidgets.QPushButton(self.widget_2)
        self.pbApply.setObjectName("pbApply")
        self.horizontalLayout.addWidget(self.pbApply)
        self.pbRemove = QtWidgets.QPushButton(self.widget_2)
        self.pbRemove.setObjectName("pbRemove")
        self.horizontalLayout.addWidget(self.pbRemove)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.widget_2, 6, 2, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        self.label_5 = QtWidgets.QLabel(DockLimits)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.table = QtWidgets.QTableWidget(DockLimits)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(DockLimits)
        QtCore.QMetaObject.connectSlotsByName(DockLimits)

    def retranslateUi(self, DockLimits):
        DockLimits.setWindowTitle(QtWidgets.QApplication.translate("DockLimits", "Form", None, -1))
        self.lbPropHelp.setText(QtWidgets.QApplication.translate("DockLimits", "hoover here for property help", None, -1))
        self.lbNodeClass.setText(QtWidgets.QApplication.translate("DockLimits", "node_class", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("DockLimits", "Limit", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("DockLimits", "Node", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("DockLimits", "Property", None, -1))
        self.lbResult.setText(QtWidgets.QApplication.translate("DockLimits", "[UC]", None, -1))
        self.pbApply.setText(QtWidgets.QApplication.translate("DockLimits", "Apply", None, -1))
        self.pbRemove.setText(QtWidgets.QApplication.translate("DockLimits", "Remove", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("DockLimits", "Defined limits:", None, -1))

