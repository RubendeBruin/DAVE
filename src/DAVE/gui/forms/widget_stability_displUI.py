# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_stability_displ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_WidgetDispDrivenStability(object):
    def setupUi(self, WidgetDispDrivenStability):
        if not WidgetDispDrivenStability.objectName():
            WidgetDispDrivenStability.setObjectName(u"WidgetDispDrivenStability")
        WidgetDispDrivenStability.resize(540, 765)
        WidgetDispDrivenStability.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(WidgetDispDrivenStability)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = QLabel(WidgetDispDrivenStability)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_4)

        self.widget = QWidget(WidgetDispDrivenStability)
        self.widget.setObjectName(u"widget")
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName(u"label_11")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_11)

        self.node_name = QComboBox(self.widget)
        self.node_name.setObjectName(u"node_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.node_name)

        self.label_16 = QLabel(self.widget)
        self.label_16.setObjectName(u"label_16")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_16)

        self.stability_displacement = QDoubleSpinBox(self.widget)
        self.stability_displacement.setObjectName(u"stability_displacement")
        self.stability_displacement.setMaximum(999999999999999.000000000000000)
        self.stability_displacement.setValue(1.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.stability_displacement)

        self.label_12 = QLabel(self.widget)
        self.label_12.setObjectName(u"label_12")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_12)

        self.stability_heel_start = QSpinBox(self.widget)
        self.stability_heel_start.setObjectName(u"stability_heel_start")
        self.stability_heel_start.setMinimum(-180)
        self.stability_heel_start.setMaximum(20)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.stability_heel_start)

        self.label_14 = QLabel(self.widget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_14)

        self.stability_heel_max = QSpinBox(self.widget)
        self.stability_heel_max.setObjectName(u"stability_heel_max")
        self.stability_heel_max.setMaximum(180)
        self.stability_heel_max.setValue(40)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.stability_heel_max)

        self.label_18 = QLabel(self.widget)
        self.label_18.setObjectName(u"label_18")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_18)

        self.stability_n_steps = QSpinBox(self.widget)
        self.stability_n_steps.setObjectName(u"stability_n_steps")
        self.stability_n_steps.setMaximum(1000)
        self.stability_n_steps.setValue(40)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.stability_n_steps)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_3)

        self.stability_surge = QCheckBox(self.widget)
        self.stability_surge.setObjectName(u"stability_surge")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.stability_surge)

        self.stability_sway = QCheckBox(self.widget)
        self.stability_sway.setObjectName(u"stability_sway")

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.stability_sway)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.label)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.label_2)

        self.stability_trim = QCheckBox(self.widget)
        self.stability_trim.setObjectName(u"stability_trim")
        self.stability_trim.setChecked(False)

        self.formLayout.setWidget(11, QFormLayout.FieldRole, self.stability_trim)

        self.stability_yaw = QCheckBox(self.widget)
        self.stability_yaw.setObjectName(u"stability_yaw")

        self.formLayout.setWidget(12, QFormLayout.FieldRole, self.stability_yaw)

        self.label_13 = QLabel(self.widget)
        self.label_13.setObjectName(u"label_13")

        self.formLayout.setWidget(13, QFormLayout.LabelRole, self.label_13)

        self.stability_do_teardown = QCheckBox(self.widget)
        self.stability_do_teardown.setObjectName(u"stability_do_teardown")
        self.stability_do_teardown.setChecked(True)

        self.formLayout.setWidget(13, QFormLayout.FieldRole, self.stability_do_teardown)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.sbWindVelocity = QDoubleSpinBox(self.widget)
        self.sbWindVelocity.setObjectName(u"sbWindVelocity")
        self.sbWindVelocity.setMaximum(200.000000000000000)
        self.sbWindVelocity.setValue(36.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.sbWindVelocity)


        self.verticalLayout.addWidget(self.widget)

        self.stability_go = QPushButton(WidgetDispDrivenStability)
        self.stability_go.setObjectName(u"stability_go")

        self.verticalLayout.addWidget(self.stability_go)

        self.pushButton = QPushButton(WidgetDispDrivenStability)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.verticalSpacer = QSpacerItem(20, 151, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.node_name, self.stability_displacement)
        QWidget.setTabOrder(self.stability_displacement, self.stability_heel_start)
        QWidget.setTabOrder(self.stability_heel_start, self.stability_heel_max)
        QWidget.setTabOrder(self.stability_heel_max, self.stability_n_steps)
        QWidget.setTabOrder(self.stability_n_steps, self.stability_surge)
        QWidget.setTabOrder(self.stability_surge, self.stability_sway)
        QWidget.setTabOrder(self.stability_sway, self.stability_yaw)
        QWidget.setTabOrder(self.stability_yaw, self.stability_trim)
        QWidget.setTabOrder(self.stability_trim, self.stability_do_teardown)

        self.retranslateUi(WidgetDispDrivenStability)

        QMetaObject.connectSlotsByName(WidgetDispDrivenStability)
    # setupUi

    def retranslateUi(self, WidgetDispDrivenStability):
        WidgetDispDrivenStability.setWindowTitle(QCoreApplication.translate("WidgetDispDrivenStability", u"Form", None))
        self.label_4.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"<html><head/><body><p>Calculate the heeling moment curve or GZ-curve.</p><p>This is done by iteratively imposing a heel angle, solving statics and evaluating the moment on the node that is used to impose the heel.</p></body></html>", None))
        self.label_11.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Node", None))
        self.label_16.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Displacement [kN]", None))
        self.label_12.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Minimum heel [deg]", None))
        self.label_14.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Maximum heel [deg]", None))
        self.label_18.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Steps [-]", None))
        self.label_3.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Freedom", None))
        self.stability_surge.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Allow Surge", None))
        self.stability_sway.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Allow Sway", None))
        self.label.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"[X] Allow Heave", None))
        self.label_2.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"[X] Impose Roll", None))
        self.stability_trim.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Allow Trim", None))
        self.stability_yaw.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Allow Yaw", None))
        self.label_13.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Tear-down", None))
        self.stability_do_teardown.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Delete temporary nodes", None))
        self.label_5.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Wind-velicity [m/s]", None))
        self.stability_go.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Displacement driven curve", None))
        self.pushButton.setText(QCoreApplication.translate("WidgetDispDrivenStability", u"Visualize", None))
    # retranslateUi

