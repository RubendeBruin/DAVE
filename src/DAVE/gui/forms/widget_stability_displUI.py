# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_stability_displ.ui',
# licensing of 'widget_stability_displ.ui' applies.
#
# Created: Mon Sep 20 11:25:05 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_WidgetDispDrivenStability(object):
    def setupUi(self, WidgetDispDrivenStability):
        WidgetDispDrivenStability.setObjectName("WidgetDispDrivenStability")
        WidgetDispDrivenStability.resize(540, 765)
        WidgetDispDrivenStability.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout = QtWidgets.QVBoxLayout(WidgetDispDrivenStability)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(WidgetDispDrivenStability)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.widget = QtWidgets.QWidget(WidgetDispDrivenStability)
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.node_name = QtWidgets.QComboBox(self.widget)
        self.node_name.setObjectName("node_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.node_name)
        self.label_16 = QtWidgets.QLabel(self.widget)
        self.label_16.setObjectName("label_16")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.stability_displacement = QtWidgets.QDoubleSpinBox(self.widget)
        self.stability_displacement.setMaximum(999999999999999.0)
        self.stability_displacement.setProperty("value", 1.0)
        self.stability_displacement.setObjectName("stability_displacement")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.stability_displacement)
        self.label_12 = QtWidgets.QLabel(self.widget)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.stability_heel_start = QtWidgets.QSpinBox(self.widget)
        self.stability_heel_start.setMinimum(-180)
        self.stability_heel_start.setMaximum(20)
        self.stability_heel_start.setObjectName("stability_heel_start")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.stability_heel_start)
        self.label_14 = QtWidgets.QLabel(self.widget)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.stability_heel_max = QtWidgets.QSpinBox(self.widget)
        self.stability_heel_max.setMaximum(180)
        self.stability_heel_max.setProperty("value", 40)
        self.stability_heel_max.setObjectName("stability_heel_max")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.stability_heel_max)
        self.label_18 = QtWidgets.QLabel(self.widget)
        self.label_18.setObjectName("label_18")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.stability_n_steps = QtWidgets.QSpinBox(self.widget)
        self.stability_n_steps.setMaximum(1000)
        self.stability_n_steps.setProperty("value", 40)
        self.stability_n_steps.setObjectName("stability_n_steps")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.stability_n_steps)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.stability_surge = QtWidgets.QCheckBox(self.widget)
        self.stability_surge.setObjectName("stability_surge")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.stability_surge)
        self.stability_sway = QtWidgets.QCheckBox(self.widget)
        self.stability_sway.setObjectName("stability_sway")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.stability_sway)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.label_2)
        self.stability_trim = QtWidgets.QCheckBox(self.widget)
        self.stability_trim.setChecked(False)
        self.stability_trim.setObjectName("stability_trim")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.stability_trim)
        self.stability_yaw = QtWidgets.QCheckBox(self.widget)
        self.stability_yaw.setObjectName("stability_yaw")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.stability_yaw)
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.stability_do_teardown = QtWidgets.QCheckBox(self.widget)
        self.stability_do_teardown.setChecked(True)
        self.stability_do_teardown.setObjectName("stability_do_teardown")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.stability_do_teardown)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.sbWindVelocity = QtWidgets.QDoubleSpinBox(self.widget)
        self.sbWindVelocity.setMaximum(200.0)
        self.sbWindVelocity.setProperty("value", 36.0)
        self.sbWindVelocity.setObjectName("sbWindVelocity")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sbWindVelocity)
        self.verticalLayout.addWidget(self.widget)
        self.stability_go = QtWidgets.QPushButton(WidgetDispDrivenStability)
        self.stability_go.setObjectName("stability_go")
        self.verticalLayout.addWidget(self.stability_go)
        self.pushButton = QtWidgets.QPushButton(WidgetDispDrivenStability)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(20, 151, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(WidgetDispDrivenStability)
        QtCore.QMetaObject.connectSlotsByName(WidgetDispDrivenStability)
        WidgetDispDrivenStability.setTabOrder(self.node_name, self.stability_displacement)
        WidgetDispDrivenStability.setTabOrder(self.stability_displacement, self.stability_heel_start)
        WidgetDispDrivenStability.setTabOrder(self.stability_heel_start, self.stability_heel_max)
        WidgetDispDrivenStability.setTabOrder(self.stability_heel_max, self.stability_n_steps)
        WidgetDispDrivenStability.setTabOrder(self.stability_n_steps, self.stability_surge)
        WidgetDispDrivenStability.setTabOrder(self.stability_surge, self.stability_sway)
        WidgetDispDrivenStability.setTabOrder(self.stability_sway, self.stability_yaw)
        WidgetDispDrivenStability.setTabOrder(self.stability_yaw, self.stability_trim)
        WidgetDispDrivenStability.setTabOrder(self.stability_trim, self.stability_do_teardown)

    def retranslateUi(self, WidgetDispDrivenStability):
        WidgetDispDrivenStability.setWindowTitle(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Form", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "<html><head/><body><p>Calculate the heeling moment curve or GZ-curve.</p><p>This is done by iteratively imposing a heel angle, solving statics and evaluating the moment on the node that is used to impose the heel.</p></body></html>", None, -1))
        self.label_11.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Node", None, -1))
        self.label_16.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Displacement [kN]", None, -1))
        self.label_12.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Minimum heel [deg]", None, -1))
        self.label_14.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Maximum heel [deg]", None, -1))
        self.label_18.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Steps [-]", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Freedom", None, -1))
        self.stability_surge.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Allow Surge", None, -1))
        self.stability_sway.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Allow Sway", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "[X] Allow Heave", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "[X] Impose Roll", None, -1))
        self.stability_trim.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Allow Trim", None, -1))
        self.stability_yaw.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Allow Yaw", None, -1))
        self.label_13.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Tear-down", None, -1))
        self.stability_do_teardown.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Delete temporary nodes", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Wind-velicity [m/s]", None, -1))
        self.stability_go.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Displacement driven curve", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("WidgetDispDrivenStability", "Visualize", None, -1))

