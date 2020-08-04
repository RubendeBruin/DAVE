# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_shackle.ui',
# licensing of 'widget_shackle.ui' applies.
#
# Created: Mon Aug  3 20:56:04 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_widgetShackle(object):
    def setupUi(self, widgetShackle):
        widgetShackle.setObjectName("widgetShackle")
        widgetShackle.resize(400, 90)
        self.horizontalLayout = QtWidgets.QHBoxLayout(widgetShackle)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(widgetShackle)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(widgetShackle)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)

        self.retranslateUi(widgetShackle)
        QtCore.QMetaObject.connectSlotsByName(widgetShackle)

    def retranslateUi(self, widgetShackle):
        widgetShackle.setWindowTitle(QtWidgets.QApplication.translate("widgetShackle", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("widgetShackle", "Shackle type:", None, -1))

