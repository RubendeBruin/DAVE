# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_ballastconfiguration.ui',
# licensing of 'widget_ballastconfiguration.ui' applies.
#
# Created: Tue Dec 10 15:08:57 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_widget_ballastsystem(object):
    def setupUi(self, widget_ballastsystem):
        widget_ballastsystem.setObjectName("widget_ballastsystem")
        widget_ballastsystem.resize(828, 1412)
        self.verticalLayout = QtWidgets.QVBoxLayout(widget_ballastsystem)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(widget_ballastsystem)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.widget = QtWidgets.QWidget(widget_ballastsystem)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widget)
        self.tableWidget = QtWidgets.QTableWidget(widget_ballastsystem)
        self.tableWidget.setDragEnabled(True)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(widget_ballastsystem)
        QtCore.QMetaObject.connectSlotsByName(widget_ballastsystem)

    def retranslateUi(self, widget_ballastsystem):
        widget_ballastsystem.setWindowTitle(QtWidgets.QApplication.translate("widget_ballastsystem", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("widget_ballastsystem", "The order of the tanks in the table determines how eager the auto-ballast algorithm is to fill that tank. Tanks higher on the list are more likely to be filled than tanks lower on the list.  The order of the list can be changed by using one of the buttons or by dragging the tanks up or down in the list by selecting their name.", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("widget_ballastsystem", "Order by elevation", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("widget_ballastsystem", "Minimize radii of gyration", None, -1))
        self.pushButton_3.setText(QtWidgets.QApplication.translate("widget_ballastsystem", "Maximize radii of gyration", None, -1))
        self.tableWidget.verticalHeaderItem(0).setText(QtWidgets.QApplication.translate("widget_ballastsystem", "Tank1", None, -1))
        self.tableWidget.verticalHeaderItem(1).setText(QtWidgets.QApplication.translate("widget_ballastsystem", "Tank2", None, -1))
        self.tableWidget.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("widget_ballastsystem", "Capacity", None, -1))
        self.tableWidget.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("widget_ballastsystem", "Fill", None, -1))
        self.tableWidget.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("widget_ballastsystem", "X", None, -1))
        self.tableWidget.horizontalHeaderItem(3).setText(QtWidgets.QApplication.translate("widget_ballastsystem", "Y", None, -1))
        self.tableWidget.horizontalHeaderItem(4).setText(QtWidgets.QApplication.translate("widget_ballastsystem", "Z", None, -1))

