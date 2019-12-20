# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_airy.ui',
# licensing of 'widget_airy.ui' applies.
#
# Created: Thu Dec 19 14:22:27 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_frmAiryWave(object):
    def setupUi(self, frmAiryWave):
        frmAiryWave.setObjectName("frmAiryWave")
        frmAiryWave.resize(503, 439)
        frmAiryWave.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(frmAiryWave)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(frmAiryWave)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.pushButton = QtWidgets.QPushButton(frmAiryWave)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.label_5 = QtWidgets.QLabel(frmAiryWave)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.pushButton_2 = QtWidgets.QPushButton(frmAiryWave)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.label_6 = QtWidgets.QLabel(frmAiryWave)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.widget = QtWidgets.QWidget(frmAiryWave)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.amplitude = QtWidgets.QDoubleSpinBox(self.widget_2)
        self.amplitude.setSingleStep(0.5)
        self.amplitude.setProperty("value", 2.0)
        self.amplitude.setObjectName("amplitude")
        self.verticalLayout.addWidget(self.amplitude)
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.period = QtWidgets.QDoubleSpinBox(self.widget_2)
        self.period.setProperty("value", 7.0)
        self.period.setObjectName("period")
        self.verticalLayout.addWidget(self.period)
        self.gridLayout.addWidget(self.widget_2, 1, 2, 1, 1)
        self.heading = QtWidgets.QDial(self.widget)
        self.heading.setMaximum(360)
        self.heading.setPageStep(45)
        self.heading.setProperty("value", 0)
        self.heading.setOrientation(QtCore.Qt.Vertical)
        self.heading.setWrapping(True)
        self.heading.setNotchTarget(0.0)
        self.heading.setNotchesVisible(True)
        self.heading.setObjectName("heading")
        self.gridLayout.addWidget(self.heading, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.widget)
        spacerItem = QtWidgets.QSpacerItem(20, 8, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(frmAiryWave)
        QtCore.QMetaObject.connectSlotsByName(frmAiryWave)

    def retranslateUi(self, frmAiryWave):
        frmAiryWave.setWindowTitle(QtWidgets.QApplication.translate("frmAiryWave", "Form", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("frmAiryWave", "Model need to be prepared before responses can be calculated. This loads the hydrodynamic data", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("frmAiryWave", "Prepare model for hydrodynamic interaction", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("frmAiryWave", "RAO calculation, no linearization of quadratic damping", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("frmAiryWave", "Show RAOs", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("frmAiryWave", "Visualization", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("frmAiryWave", "<- Direction", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("frmAiryWave", "Amplitude [m]", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("frmAiryWave", "Period [s]", None, -1))

