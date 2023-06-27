# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_airy.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_frmAiryWave(object):
    def setupUi(self, frmAiryWave):
        if not frmAiryWave.objectName():
            frmAiryWave.setObjectName(u"frmAiryWave")
        frmAiryWave.resize(503, 357)
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
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.sbHeading = QSpinBox(self.widget_2)
        self.sbHeading.setObjectName(u"sbHeading")
        self.sbHeading.setMaximum(360)
        self.sbHeading.setSingleStep(5)

        self.verticalLayout.addWidget(self.sbHeading)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.amplitude = QDoubleSpinBox(self.widget_2)
        self.amplitude.setObjectName(u"amplitude")
        self.amplitude.setSingleStep(0.250000000000000)
        self.amplitude.setValue(2.000000000000000)

        self.verticalLayout.addWidget(self.amplitude)

        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.period = QDoubleSpinBox(self.widget_2)
        self.period.setObjectName(u"period")
        self.period.setValue(7.000000000000000)

        self.verticalLayout.addWidget(self.period)

        self.pushButton = QPushButton(self.widget_2)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.lblInfo = QLabel(self.widget_2)
        self.lblInfo.setObjectName(u"lblInfo")
        font = QFont()
        font.setPointSize(16)
        self.lblInfo.setFont(font)

        self.verticalLayout.addWidget(self.lblInfo)


        self.gridLayout.addWidget(self.widget_2, 1, 1, 1, 1)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)


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
        self.label.setText(QCoreApplication.translate("frmAiryWave", u"Wave heading", None))
        self.label_2.setText(QCoreApplication.translate("frmAiryWave", u"Amplitude [m]", None))
        self.label_3.setText(QCoreApplication.translate("frmAiryWave", u"Period [s]", None))
        self.pushButton.setText(QCoreApplication.translate("frmAiryWave", u"Show", None))
        self.lblInfo.setText(QCoreApplication.translate("frmAiryWave", u"press show to activate animation", None))
        self.label_4.setText(QCoreApplication.translate("frmAiryWave", u"Airy wave", None))
    # retranslateUi

