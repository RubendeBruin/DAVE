# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_environment.ui',
# licensing of 'widget_environment.ui' applies.
#
# Created: Wed Sep  1 10:31:35 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_frmEnvironment(object):
    def setupUi(self, frmEnvironment):
        frmEnvironment.setObjectName("frmEnvironment")
        frmEnvironment.resize(208, 541)
        self.verticalLayout = QtWidgets.QVBoxLayout(frmEnvironment)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(frmEnvironment)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 10, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.widget)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 13, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.widget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 1, 2, 1, 1)
        self.waterlevel = QtWidgets.QDoubleSpinBox(self.widget)
        self.waterlevel.setEnabled(False)
        self.waterlevel.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.World))
        self.waterlevel.setObjectName("waterlevel")
        self.gridLayout.addWidget(self.waterlevel, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.current_velocity = QtWidgets.QDoubleSpinBox(self.widget)
        self.current_velocity.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.World))
        self.current_velocity.setMaximum(100.0)
        self.current_velocity.setSingleStep(0.1)
        self.current_velocity.setObjectName("current_velocity")
        self.gridLayout.addWidget(self.current_velocity, 14, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 13, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 14, 0, 1, 1)
        self.rho_air = QtWidgets.QDoubleSpinBox(self.widget)
        self.rho_air.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.World))
        self.rho_air.setDecimals(7)
        self.rho_air.setObjectName("rho_air")
        self.gridLayout.addWidget(self.rho_air, 6, 1, 1, 1)
        self.wind_velocity = QtWidgets.QDoubleSpinBox(self.widget)
        self.wind_velocity.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.World))
        self.wind_velocity.setMaximum(100.0)
        self.wind_velocity.setObjectName("wind_velocity")
        self.gridLayout.addWidget(self.wind_velocity, 10, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.current_direction = QtWidgets.QDoubleSpinBox(self.widget)
        self.current_direction.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.World))
        self.current_direction.setMinimum(-360.0)
        self.current_direction.setMaximum(720.0)
        self.current_direction.setObjectName("current_direction")
        self.gridLayout.addWidget(self.current_direction, 13, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.g = QtWidgets.QDoubleSpinBox(self.widget)
        self.g.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.World))
        self.g.setDecimals(5)
        self.g.setObjectName("g")
        self.gridLayout.addWidget(self.g, 1, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.widget)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 8, 2, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.widget)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 6, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.widget)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 10, 2, 1, 1)
        self.wind_direction = QtWidgets.QDoubleSpinBox(self.widget)
        self.wind_direction.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.World))
        self.wind_direction.setMinimum(-360.0)
        self.wind_direction.setMaximum(720.0)
        self.wind_direction.setObjectName("wind_direction")
        self.gridLayout.addWidget(self.wind_direction, 8, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 12, 0, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.widget)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 14, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 1)
        self.rho_water = QtWidgets.QDoubleSpinBox(self.widget)
        self.rho_water.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.World))
        self.rho_water.setDecimals(5)
        self.rho_water.setObjectName("rho_water")
        self.gridLayout.addWidget(self.rho_water, 5, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 5, 2, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        spacerItem = QtWidgets.QSpacerItem(20, 288, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(frmEnvironment)
        QtCore.QMetaObject.connectSlotsByName(frmEnvironment)
        frmEnvironment.setTabOrder(self.g, self.waterlevel)
        frmEnvironment.setTabOrder(self.waterlevel, self.rho_water)
        frmEnvironment.setTabOrder(self.rho_water, self.rho_air)
        frmEnvironment.setTabOrder(self.rho_air, self.wind_direction)
        frmEnvironment.setTabOrder(self.wind_direction, self.wind_velocity)
        frmEnvironment.setTabOrder(self.wind_velocity, self.current_direction)
        frmEnvironment.setTabOrder(self.current_direction, self.current_velocity)

    def retranslateUi(self, frmEnvironment):
        frmEnvironment.setWindowTitle(QtWidgets.QApplication.translate("frmEnvironment", "Form", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("frmEnvironment", "Velocity", None, -1))
        self.label_17.setText(QtWidgets.QApplication.translate("frmEnvironment", "[deg]", None, -1))
        self.label_12.setText(QtWidgets.QApplication.translate("frmEnvironment", "m/s2", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("frmEnvironment", "water-level", None, -1))
        self.label_10.setText(QtWidgets.QApplication.translate("frmEnvironment", "Going to", None, -1))
        self.label_11.setText(QtWidgets.QApplication.translate("frmEnvironment", "Velocity", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("frmEnvironment", "Air density", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("frmEnvironment", "General", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("frmEnvironment", "g", None, -1))
        self.label_15.setText(QtWidgets.QApplication.translate("frmEnvironment", "[deg]", None, -1))
        self.label_14.setText(QtWidgets.QApplication.translate("frmEnvironment", "mT/m3", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("frmEnvironment", "Wind", None, -1))
        self.label_16.setText(QtWidgets.QApplication.translate("frmEnvironment", "[m/s]", None, -1))
        self.label_9.setText(QtWidgets.QApplication.translate("frmEnvironment", "Current", None, -1))
        self.label_18.setText(QtWidgets.QApplication.translate("frmEnvironment", "[m/s]", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("frmEnvironment", "Going to", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("frmEnvironment", "water density", None, -1))
        self.label_13.setText(QtWidgets.QApplication.translate("frmEnvironment", "mT/m3", None, -1))

