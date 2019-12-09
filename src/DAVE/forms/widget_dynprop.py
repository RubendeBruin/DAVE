# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_dynprop.ui',
# licensing of 'widget_dynprop.ui' applies.
#
# Created: Fri Nov 29 16:13:01 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_widget_dynprop(object):
    def setupUi(self, widget_dynprop):
        widget_dynprop.setObjectName("widget_dynprop")
        widget_dynprop.resize(1293, 1074)
        self.horizontalLayout = QtWidgets.QHBoxLayout(widget_dynprop)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(widget_dynprop)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lblChangeDynamicInfo = QtWidgets.QLabel(self.widget)
        self.lblChangeDynamicInfo.setObjectName("lblChangeDynamicInfo")
        self.verticalLayout_2.addWidget(self.lblChangeDynamicInfo)
        self.tableDynProp = QtWidgets.QTableWidget(self.widget)
        self.tableDynProp.setObjectName("tableDynProp")
        self.tableDynProp.setColumnCount(13)
        self.tableDynProp.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(12, item)
        self.tableDynProp.horizontalHeader().setMinimumSectionSize(20)
        self.tableDynProp.verticalHeader().setVisible(True)
        self.verticalLayout_2.addWidget(self.tableDynProp)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(widget_dynprop)
        QtCore.QMetaObject.connectSlotsByName(widget_dynprop)

    def retranslateUi(self, widget_dynprop):
        widget_dynprop.setWindowTitle(QtWidgets.QApplication.translate("widget_dynprop", "Form", None, -1))
        self.lblChangeDynamicInfo.setText(QtWidgets.QApplication.translate("widget_dynprop", "Note: For RigidBody type nodes the inertia properties are coupled to the weight properties.\n"
"Changing the intertia properties changes the weight properties as well", None, -1))
        self.tableDynProp.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("widget_dynprop", "F", None, -1))
        self.tableDynProp.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("widget_dynprop", "I", None, -1))
        self.tableDynProp.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("widget_dynprop", "X", None, -1))
        self.tableDynProp.horizontalHeaderItem(3).setText(QtWidgets.QApplication.translate("widget_dynprop", "E", None, -1))
        self.tableDynProp.horizontalHeaderItem(4).setText(QtWidgets.QApplication.translate("widget_dynprop", "D", None, -1))
        self.tableDynProp.horizontalHeaderItem(6).setText(QtWidgets.QApplication.translate("widget_dynprop", "Inertia (weight)", None, -1))
        self.tableDynProp.horizontalHeaderItem(7).setText(QtWidgets.QApplication.translate("widget_dynprop", "x (cog)", None, -1))
        self.tableDynProp.horizontalHeaderItem(8).setText(QtWidgets.QApplication.translate("widget_dynprop", "y (cog)", None, -1))
        self.tableDynProp.horizontalHeaderItem(9).setText(QtWidgets.QApplication.translate("widget_dynprop", " (cog)", None, -1))
        self.tableDynProp.horizontalHeaderItem(10).setText(QtWidgets.QApplication.translate("widget_dynprop", "rxx", None, -1))
        self.tableDynProp.horizontalHeaderItem(11).setText(QtWidgets.QApplication.translate("widget_dynprop", "ryy", None, -1))
        self.tableDynProp.horizontalHeaderItem(12).setText(QtWidgets.QApplication.translate("widget_dynprop", "rzz", None, -1))

