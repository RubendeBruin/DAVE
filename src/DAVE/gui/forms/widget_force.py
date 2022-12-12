# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_force.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from DAVE.gui.helpers.qnodepicker import QNodePicker


class Ui_widget_force(object):
    def setupUi(self, widget_force):
        if not widget_force.objectName():
            widget_force.setObjectName(u"widget_force")
        widget_force.resize(315, 288)
        widget_force.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widget_force)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(widget_force)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_10)

        self.widgetParent = QNodePicker(self.widget)
        self.widgetParent.setObjectName(u"widgetParent")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widgetParent.sizePolicy().hasHeightForWidth())
        self.widgetParent.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.widgetParent)


        self.verticalLayout.addWidget(self.widget)

        self.label_7 = QLabel(widget_force)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_7)

        self.frame = QFrame(widget_force)
        self.frame.setObjectName(u"frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_1.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_1.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_1.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBox_1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_2.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.doubleSpinBox_2)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_3.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_3.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_3.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.doubleSpinBox_3)


        self.verticalLayout.addWidget(self.frame)

        self.label_9 = QLabel(widget_force)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_9)

        self.frame_2 = QFrame(widget_force)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy2.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy2)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.formLayout_2 = QFormLayout(self.frame_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.doubleSpinBox_5 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_5.setObjectName(u"doubleSpinBox_5")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_5.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_5.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_5.setDecimals(3)
        self.doubleSpinBox_5.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_5.setMaximum(99999999999999.000000000000000)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.doubleSpinBox_5)

        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.doubleSpinBox_6 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_6.setObjectName(u"doubleSpinBox_6")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_6.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_6.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_6.setDecimals(3)
        self.doubleSpinBox_6.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_6.setMaximum(99999999999999.000000000000000)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.doubleSpinBox_6)

        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_4.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_4.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_4.setDecimals(3)
        self.doubleSpinBox_4.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_4.setMaximum(99999999999999.000000000000000)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.doubleSpinBox_4)


        self.verticalLayout.addWidget(self.frame_2)

        self.label_8 = QLabel(widget_force)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.doubleSpinBox_1, self.doubleSpinBox_2)
        QWidget.setTabOrder(self.doubleSpinBox_2, self.doubleSpinBox_3)
        QWidget.setTabOrder(self.doubleSpinBox_3, self.doubleSpinBox_4)
        QWidget.setTabOrder(self.doubleSpinBox_4, self.doubleSpinBox_5)
        QWidget.setTabOrder(self.doubleSpinBox_5, self.doubleSpinBox_6)

        self.retranslateUi(widget_force)

        QMetaObject.connectSlotsByName(widget_force)
    # setupUi

    def retranslateUi(self, widget_force):
        widget_force.setWindowTitle(QCoreApplication.translate("widget_force", u"Form", None))
        self.label_10.setText(QCoreApplication.translate("widget_force", u"Parent", None))
        self.label_7.setText(QCoreApplication.translate("widget_force", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Force</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("widget_force", u"X", None))
        self.label_2.setText(QCoreApplication.translate("widget_force", u"Y", None))
        self.label_3.setText(QCoreApplication.translate("widget_force", u"Z", None))
        self.label_9.setText(QCoreApplication.translate("widget_force", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Moment</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("widget_force", u"Y", None))
        self.label_6.setText(QCoreApplication.translate("widget_force", u"Z", None))
        self.label_4.setText(QCoreApplication.translate("widget_force", u"X", None))
        self.label_8.setText(QCoreApplication.translate("widget_force", u"<html><head/><body><p>Force components are defined in global axis.</p></body></html>", None))
    # retranslateUi

