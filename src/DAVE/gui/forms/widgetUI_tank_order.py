# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_tank_order.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_widget_tank_order(object):
    def setupUi(self, widget_tank_order):
        if not widget_tank_order.objectName():
            widget_tank_order.setObjectName(u"widget_tank_order")
        widget_tank_order.resize(378, 703)
        widget_tank_order.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widget_tank_order)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(widget_tank_order)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.pbElevation = QPushButton(widget_tank_order)
        self.pbElevation.setObjectName(u"pbElevation")

        self.verticalLayout.addWidget(self.pbElevation)

        self.pbMinimizeRadii = QPushButton(widget_tank_order)
        self.pbMinimizeRadii.setObjectName(u"pbMinimizeRadii")

        self.verticalLayout.addWidget(self.pbMinimizeRadii)

        self.pbMaximizeRadii = QPushButton(widget_tank_order)
        self.pbMaximizeRadii.setObjectName(u"pbMaximizeRadii")

        self.verticalLayout.addWidget(self.pbMaximizeRadii)

        self.widget_3 = QWidget(widget_tank_order)
        self.widget_3.setObjectName(u"widget_3")
        self.gridLayout = QGridLayout(self.widget_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.dsX = QDoubleSpinBox(self.widget_3)
        self.dsX.setObjectName(u"dsX")
        self.dsX.setMinimum(-999.000000000000000)
        self.dsX.setMaximum(999.000000000000000)
        self.dsX.setSingleStep(10.000000000000000)

        self.gridLayout.addWidget(self.dsX, 1, 1, 1, 1)

        self.dsX_2 = QDoubleSpinBox(self.widget_3)
        self.dsX_2.setObjectName(u"dsX_2")
        self.dsX_2.setMinimum(-999.000000000000000)
        self.dsX_2.setMaximum(999.000000000000000)
        self.dsX_2.setSingleStep(10.000000000000000)

        self.gridLayout.addWidget(self.dsX_2, 2, 1, 1, 1)

        self.dsX_3 = QDoubleSpinBox(self.widget_3)
        self.dsX_3.setObjectName(u"dsX_3")
        self.dsX_3.setMinimum(-999.000000000000000)
        self.dsX_3.setMaximum(999.000000000000000)
        self.dsX_3.setSingleStep(10.000000000000000)

        self.gridLayout.addWidget(self.dsX_3, 3, 1, 1, 1)

        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)


        self.verticalLayout.addWidget(self.widget_3)

        self.pbNearest = QPushButton(widget_tank_order)
        self.pbNearest.setObjectName(u"pbNearest")

        self.verticalLayout.addWidget(self.pbNearest)

        self.pbFurthest = QPushButton(widget_tank_order)
        self.pbFurthest.setObjectName(u"pbFurthest")

        self.verticalLayout.addWidget(self.pbFurthest)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.pbElevation, self.pbMinimizeRadii)
        QWidget.setTabOrder(self.pbMinimizeRadii, self.pbMaximizeRadii)
        QWidget.setTabOrder(self.pbMaximizeRadii, self.dsX)
        QWidget.setTabOrder(self.dsX, self.dsX_2)
        QWidget.setTabOrder(self.dsX_2, self.dsX_3)
        QWidget.setTabOrder(self.dsX_3, self.pbNearest)
        QWidget.setTabOrder(self.pbNearest, self.pbFurthest)

        self.retranslateUi(widget_tank_order)

        QMetaObject.connectSlotsByName(widget_tank_order)
    # setupUi

    def retranslateUi(self, widget_tank_order):
        widget_tank_order.setWindowTitle(QCoreApplication.translate("widget_tank_order", u"Form", None))
        self.label.setText(QCoreApplication.translate("widget_tank_order", u"<html><head/><body><p>The order of the tanks in the table determines how eager the auto-ballast algorithm is to fill that tank.</p><p>Tanks higher on the list are more likely to be filled than tanks lower on the list.</p><p>The order of the list can be changed by using one of the buttons or by dragging the tanks up or down in the list by selecting their name.</p></body></html>", None))
        self.pbElevation.setText(QCoreApplication.translate("widget_tank_order", u"Order by elevation", None))
        self.pbMinimizeRadii.setText(QCoreApplication.translate("widget_tank_order", u"Minimize radii of gyration", None))
        self.pbMaximizeRadii.setText(QCoreApplication.translate("widget_tank_order", u"Maximize radii of gyration", None))
        self.label_2.setText(QCoreApplication.translate("widget_tank_order", u"X", None))
        self.label_3.setText(QCoreApplication.translate("widget_tank_order", u"Y", None))
        self.label_4.setText(QCoreApplication.translate("widget_tank_order", u"Z", None))
        self.pbNearest.setText(QCoreApplication.translate("widget_tank_order", u"Nearest to point", None))
        self.pbFurthest.setText(QCoreApplication.translate("widget_tank_order", u"Furthest from point", None))
    # retranslateUi

