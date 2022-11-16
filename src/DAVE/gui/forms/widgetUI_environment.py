# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_environment.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_frmEnvironment(object):
    def setupUi(self, frmEnvironment):
        if not frmEnvironment.objectName():
            frmEnvironment.setObjectName(u"frmEnvironment")
        frmEnvironment.resize(208, 541)
        self.verticalLayout = QVBoxLayout(frmEnvironment)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(frmEnvironment)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 10, 0, 1, 1)

        self.label_17 = QLabel(self.widget)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout.addWidget(self.label_17, 13, 2, 1, 1)

        self.label_12 = QLabel(self.widget)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 1, 2, 1, 1)

        self.waterlevel = QDoubleSpinBox(self.widget)
        self.waterlevel.setObjectName(u"waterlevel")
        self.waterlevel.setEnabled(False)
        self.waterlevel.setLocale(QLocale(QLocale.English, QLocale.World))

        self.gridLayout.addWidget(self.waterlevel, 2, 1, 1, 1)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.current_velocity = QDoubleSpinBox(self.widget)
        self.current_velocity.setObjectName(u"current_velocity")
        self.current_velocity.setLocale(QLocale(QLocale.English, QLocale.World))
        self.current_velocity.setMaximum(100.000000000000000)
        self.current_velocity.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.current_velocity, 14, 1, 1, 1)

        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 13, 0, 1, 1)

        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 14, 0, 1, 1)

        self.rho_air = QDoubleSpinBox(self.widget)
        self.rho_air.setObjectName(u"rho_air")
        self.rho_air.setLocale(QLocale(QLocale.English, QLocale.World))
        self.rho_air.setDecimals(7)

        self.gridLayout.addWidget(self.rho_air, 6, 1, 1, 1)

        self.wind_velocity = QDoubleSpinBox(self.widget)
        self.wind_velocity.setObjectName(u"wind_velocity")
        self.wind_velocity.setLocale(QLocale(QLocale.English, QLocale.World))
        self.wind_velocity.setMaximum(100.000000000000000)

        self.gridLayout.addWidget(self.wind_velocity, 10, 1, 1, 1)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)

        self.current_direction = QDoubleSpinBox(self.widget)
        self.current_direction.setObjectName(u"current_direction")
        self.current_direction.setLocale(QLocale(QLocale.English, QLocale.World))
        self.current_direction.setMinimum(-360.000000000000000)
        self.current_direction.setMaximum(720.000000000000000)

        self.gridLayout.addWidget(self.current_direction, 13, 1, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.g = QDoubleSpinBox(self.widget)
        self.g.setObjectName(u"g")
        self.g.setLocale(QLocale(QLocale.English, QLocale.World))
        self.g.setDecimals(5)

        self.gridLayout.addWidget(self.g, 1, 1, 1, 1)

        self.label_15 = QLabel(self.widget)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 8, 2, 1, 1)

        self.label_14 = QLabel(self.widget)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 6, 2, 1, 1)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 1)

        self.label_16 = QLabel(self.widget)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 10, 2, 1, 1)

        self.wind_direction = QDoubleSpinBox(self.widget)
        self.wind_direction.setObjectName(u"wind_direction")
        self.wind_direction.setLocale(QLocale(QLocale.English, QLocale.World))
        self.wind_direction.setMinimum(-360.000000000000000)
        self.wind_direction.setMaximum(720.000000000000000)

        self.gridLayout.addWidget(self.wind_direction, 8, 1, 1, 1)

        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 12, 0, 1, 1)

        self.label_18 = QLabel(self.widget)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout.addWidget(self.label_18, 14, 2, 1, 1)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 1)

        self.rho_water = QDoubleSpinBox(self.widget)
        self.rho_water.setObjectName(u"rho_water")
        self.rho_water.setLocale(QLocale(QLocale.English, QLocale.World))
        self.rho_water.setDecimals(5)

        self.gridLayout.addWidget(self.rho_water, 5, 1, 1, 1)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.label_13 = QLabel(self.widget)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 5, 2, 1, 1)

        self.current_knots = QLabel(self.widget)
        self.current_knots.setObjectName(u"current_knots")

        self.gridLayout.addWidget(self.current_knots, 15, 1, 1, 1)

        self.wind_knots = QLabel(self.widget)
        self.wind_knots.setObjectName(u"wind_knots")

        self.gridLayout.addWidget(self.wind_knots, 11, 1, 1, 1)


        self.verticalLayout.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 260, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.g, self.waterlevel)
        QWidget.setTabOrder(self.waterlevel, self.rho_water)
        QWidget.setTabOrder(self.rho_water, self.rho_air)
        QWidget.setTabOrder(self.rho_air, self.wind_direction)
        QWidget.setTabOrder(self.wind_direction, self.wind_velocity)
        QWidget.setTabOrder(self.wind_velocity, self.current_direction)
        QWidget.setTabOrder(self.current_direction, self.current_velocity)

        self.retranslateUi(frmEnvironment)

        QMetaObject.connectSlotsByName(frmEnvironment)
    # setupUi

    def retranslateUi(self, frmEnvironment):
        frmEnvironment.setWindowTitle(QCoreApplication.translate("frmEnvironment", u"Form", None))
        self.label_8.setText(QCoreApplication.translate("frmEnvironment", u"Velocity", None))
        self.label_17.setText(QCoreApplication.translate("frmEnvironment", u"[deg]", None))
        self.label_12.setText(QCoreApplication.translate("frmEnvironment", u"m/s2", None))
        self.label_3.setText(QCoreApplication.translate("frmEnvironment", u"water-level", None))
        self.label_10.setText(QCoreApplication.translate("frmEnvironment", u"Going to", None))
        self.label_11.setText(QCoreApplication.translate("frmEnvironment", u"Velocity", None))
        self.label_5.setText(QCoreApplication.translate("frmEnvironment", u"Air density", None))
        self.label.setText(QCoreApplication.translate("frmEnvironment", u"General", None))
        self.label_2.setText(QCoreApplication.translate("frmEnvironment", u"g", None))
        self.label_15.setText(QCoreApplication.translate("frmEnvironment", u"[deg]", None))
        self.label_14.setText(QCoreApplication.translate("frmEnvironment", u"mT/m3", None))
        self.label_6.setText(QCoreApplication.translate("frmEnvironment", u"Wind", None))
        self.label_16.setText(QCoreApplication.translate("frmEnvironment", u"[m/s]", None))
        self.label_9.setText(QCoreApplication.translate("frmEnvironment", u"Current", None))
        self.label_18.setText(QCoreApplication.translate("frmEnvironment", u"[m/s]", None))
        self.label_7.setText(QCoreApplication.translate("frmEnvironment", u"Going to", None))
        self.label_4.setText(QCoreApplication.translate("frmEnvironment", u"water density", None))
        self.label_13.setText(QCoreApplication.translate("frmEnvironment", u"mT/m3", None))
        self.current_knots.setText(QCoreApplication.translate("frmEnvironment", u"(knots)", None))
        self.wind_knots.setText(QCoreApplication.translate("frmEnvironment", u"(knots)", None))
    # retranslateUi

