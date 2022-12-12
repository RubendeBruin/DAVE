# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_area.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_frmArea(object):
    def setupUi(self, frmArea):
        if not frmArea.objectName():
            frmArea.setObjectName(u"frmArea")
        frmArea.resize(165, 340)
        self.gridLayout_3 = QGridLayout(frmArea)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.widget_3 = QWidget(frmArea)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout = QHBoxLayout(self.widget_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_13 = QLabel(self.widget_3)
        self.label_13.setObjectName(u"label_13")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_13)

        self.widgetParent = QNodePicker(self.widget_3)
        self.widgetParent.setObjectName(u"widgetParent")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widgetParent.sizePolicy().hasHeightForWidth())
        self.widgetParent.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.widgetParent)


        self.gridLayout_3.addWidget(self.widget_3, 0, 0, 1, 3)

        self.label = QLabel(frmArea)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 2, 0, 1, 1)

        self.Cd = QDoubleSpinBox(frmArea)
        self.Cd.setObjectName(u"Cd")
        self.Cd.setLocale(QLocale(QLocale.English, QLocale.World))
        self.Cd.setMaximum(100.000000000000000)

        self.gridLayout_3.addWidget(self.Cd, 2, 1, 1, 1)

        self.label_2 = QLabel(frmArea)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 2, 2, 1, 1)

        self.label_3 = QLabel(frmArea)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)

        self.Area = QDoubleSpinBox(frmArea)
        self.Area.setObjectName(u"Area")
        self.Area.setLocale(QLocale(QLocale.English, QLocale.World))
        self.Area.setMaximum(10000.000000000000000)

        self.gridLayout_3.addWidget(self.Area, 3, 1, 1, 1)

        self.label_4 = QLabel(frmArea)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 3, 2, 1, 1)

        self.rbNoOrientation = QRadioButton(frmArea)
        self.rbNoOrientation.setObjectName(u"rbNoOrientation")

        self.gridLayout_3.addWidget(self.rbNoOrientation, 4, 0, 1, 2)

        self.rbPlane = QRadioButton(frmArea)
        self.rbPlane.setObjectName(u"rbPlane")

        self.gridLayout_3.addWidget(self.rbPlane, 5, 0, 1, 2)

        self.rbCylinder = QRadioButton(frmArea)
        self.rbCylinder.setObjectName(u"rbCylinder")

        self.gridLayout_3.addWidget(self.rbCylinder, 7, 0, 1, 3)

        self.windcurrent = QLabel(frmArea)
        self.windcurrent.setObjectName(u"windcurrent")
        self.windcurrent.setStyleSheet(u"")
        self.windcurrent.setFrameShape(QFrame.Box)
        self.windcurrent.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.windcurrent, 1, 0, 1, 3)

        self.widget = QWidget(frmArea)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.Z = QDoubleSpinBox(self.widget)
        self.Z.setObjectName(u"Z")
        self.Z.setLocale(QLocale(QLocale.English, QLocale.World))
        self.Z.setMinimum(-10.000000000000000)
        self.Z.setMaximum(10.000000000000000)
        self.Z.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.Z, 5, 1, 1, 1)

        self.Y = QDoubleSpinBox(self.widget)
        self.Y.setObjectName(u"Y")
        self.Y.setLocale(QLocale(QLocale.English, QLocale.World))
        self.Y.setMinimum(-10.000000000000000)
        self.Y.setMaximum(10.000000000000000)
        self.Y.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.Y, 4, 1, 1, 1)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.X = QDoubleSpinBox(self.widget)
        self.X.setObjectName(u"X")
        self.X.setLocale(QLocale(QLocale.English, QLocale.World))
        self.X.setMinimum(-10.000000000000000)
        self.X.setMaximum(10.000000000000000)
        self.X.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.X, 2, 1, 1, 1)


        self.gridLayout_3.addWidget(self.widget, 6, 0, 1, 3)

        self.widget_2 = QWidget(frmArea)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_2 = QGridLayout(self.widget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_9 = QLabel(self.widget_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 5, 0, 1, 1)

        self.label_10 = QLabel(self.widget_2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 4, 0, 1, 1)

        self.Z_2 = QDoubleSpinBox(self.widget_2)
        self.Z_2.setObjectName(u"Z_2")
        self.Z_2.setLocale(QLocale(QLocale.English, QLocale.World))
        self.Z_2.setMinimum(-10.000000000000000)
        self.Z_2.setMaximum(10.000000000000000)
        self.Z_2.setSingleStep(0.100000000000000)

        self.gridLayout_2.addWidget(self.Z_2, 5, 1, 1, 1)

        self.Y_2 = QDoubleSpinBox(self.widget_2)
        self.Y_2.setObjectName(u"Y_2")
        self.Y_2.setLocale(QLocale(QLocale.English, QLocale.World))
        self.Y_2.setMinimum(-10.000000000000000)
        self.Y_2.setMaximum(10.000000000000000)
        self.Y_2.setSingleStep(0.100000000000000)

        self.gridLayout_2.addWidget(self.Y_2, 4, 1, 1, 1)

        self.label_11 = QLabel(self.widget_2)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 0, 0, 1, 1)

        self.label_12 = QLabel(self.widget_2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 2, 0, 1, 1)

        self.X_2 = QDoubleSpinBox(self.widget_2)
        self.X_2.setObjectName(u"X_2")
        self.X_2.setLocale(QLocale(QLocale.English, QLocale.World))
        self.X_2.setMinimum(-10.000000000000000)
        self.X_2.setMaximum(10.000000000000000)
        self.X_2.setSingleStep(0.100000000000000)

        self.gridLayout_2.addWidget(self.X_2, 2, 1, 1, 1)


        self.gridLayout_3.addWidget(self.widget_2, 8, 0, 1, 3)

        QWidget.setTabOrder(self.Cd, self.Area)
        QWidget.setTabOrder(self.Area, self.rbNoOrientation)
        QWidget.setTabOrder(self.rbNoOrientation, self.rbPlane)
        QWidget.setTabOrder(self.rbPlane, self.X)
        QWidget.setTabOrder(self.X, self.Y)
        QWidget.setTabOrder(self.Y, self.Z)
        QWidget.setTabOrder(self.Z, self.rbCylinder)
        QWidget.setTabOrder(self.rbCylinder, self.X_2)
        QWidget.setTabOrder(self.X_2, self.Y_2)
        QWidget.setTabOrder(self.Y_2, self.Z_2)

        self.retranslateUi(frmArea)

        QMetaObject.connectSlotsByName(frmArea)
    # setupUi

    def retranslateUi(self, frmArea):
        frmArea.setWindowTitle(QCoreApplication.translate("frmArea", u"Form", None))
        self.label_13.setText(QCoreApplication.translate("frmArea", u"Parent", None))
        self.label.setText(QCoreApplication.translate("frmArea", u"Cd", None))
        self.label_2.setText(QCoreApplication.translate("frmArea", u"[-]", None))
        self.label_3.setText(QCoreApplication.translate("frmArea", u"Area", None))
        self.label_4.setText(QCoreApplication.translate("frmArea", u"[m2]", None))
        self.rbNoOrientation.setText(QCoreApplication.translate("frmArea", u"No orientation", None))
        self.rbPlane.setText(QCoreApplication.translate("frmArea", u"Plane orientation", None))
        self.rbCylinder.setText(QCoreApplication.translate("frmArea", u"Cylindrical orientation", None))
        self.windcurrent.setText(QCoreApplication.translate("frmArea", u"TextLabel", None))
        self.label_7.setText(QCoreApplication.translate("frmArea", u"Z", None))
        self.label_6.setText(QCoreApplication.translate("frmArea", u"Y", None))
        self.label_8.setText(QCoreApplication.translate("frmArea", u"Plane normal:", None))
        self.label_5.setText(QCoreApplication.translate("frmArea", u"X", None))
        self.label_9.setText(QCoreApplication.translate("frmArea", u"Z", None))
        self.label_10.setText(QCoreApplication.translate("frmArea", u"Y", None))
        self.label_11.setText(QCoreApplication.translate("frmArea", u"Cylinder axis:", None))
        self.label_12.setText(QCoreApplication.translate("frmArea", u"X", None))
    # retranslateUi

