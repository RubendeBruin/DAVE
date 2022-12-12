# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_airy.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_frmAiryWave(object):
    def setupUi(self, frmAiryWave):
        if not frmAiryWave.objectName():
            frmAiryWave.setObjectName(u"frmAiryWave")
        frmAiryWave.resize(503, 321)
        frmAiryWave.setMaximumSize(QSize(16777215, 500))
        frmAiryWave.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout_2 = QVBoxLayout(frmAiryWave)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_5 = QLabel(frmAiryWave)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.pushButton_2 = QPushButton(frmAiryWave)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.label_6 = QLabel(frmAiryWave)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_6)

        self.widget = QWidget(frmAiryWave)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.amplitude = QDoubleSpinBox(self.widget_2)
        self.amplitude.setObjectName(u"amplitude")
        self.amplitude.setSingleStep(0.500000000000000)
        self.amplitude.setValue(2.000000000000000)

        self.verticalLayout.addWidget(self.amplitude)

        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.period = QDoubleSpinBox(self.widget_2)
        self.period.setObjectName(u"period")
        self.period.setValue(7.000000000000000)

        self.verticalLayout.addWidget(self.period)


        self.gridLayout.addWidget(self.widget_2, 1, 2, 1, 1)

        self.heading = QDial(self.widget)
        self.heading.setObjectName(u"heading")
        self.heading.setMaximum(360)
        self.heading.setPageStep(45)
        self.heading.setValue(0)
        self.heading.setOrientation(Qt.Vertical)
        self.heading.setWrapping(True)
        self.heading.setNotchTarget(0.000000000000000)
        self.heading.setNotchesVisible(True)

        self.gridLayout.addWidget(self.heading, 1, 1, 1, 1)

        self.lblHeading = QLabel(self.widget)
        self.lblHeading.setObjectName(u"lblHeading")
        self.lblHeading.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lblHeading, 2, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.retranslateUi(frmAiryWave)

        QMetaObject.connectSlotsByName(frmAiryWave)
    # setupUi

    def retranslateUi(self, frmAiryWave):
        frmAiryWave.setWindowTitle(QCoreApplication.translate("frmAiryWave", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("frmAiryWave", u"RAO calculation, no linearization of quadratic damping", None))
        self.pushButton_2.setText(QCoreApplication.translate("frmAiryWave", u"Show RAOs", None))
        self.label_6.setText(QCoreApplication.translate("frmAiryWave", u"Visualization", None))
        self.label_2.setText(QCoreApplication.translate("frmAiryWave", u"Amplitude [m]", None))
        self.label_3.setText(QCoreApplication.translate("frmAiryWave", u"Period [s]", None))
        self.lblHeading.setText(QCoreApplication.translate("frmAiryWave", u"heading", None))
    # retranslateUi

