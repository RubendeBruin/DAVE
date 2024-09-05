# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_supportpoint.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
    QSizePolicy, QSpacerItem, QWidget)

from DAVE.gui.helpers.qnodepicker import QNodePicker

class Ui_SupportPointWidget(object):
    def setupUi(self, SupportPointWidget):
        if not SupportPointWidget.objectName():
            SupportPointWidget.setObjectName(u"SupportPointWidget")
        SupportPointWidget.resize(258, 525)
        self.gridLayout_2 = QGridLayout(SupportPointWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(SupportPointWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(161, 255, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.npFrame = QNodePicker(SupportPointWidget)
        self.npFrame.setObjectName(u"npFrame")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.npFrame.sizePolicy().hasHeightForWidth())
        self.npFrame.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.npFrame, 0, 1, 1, 1)

        self.label_3 = QLabel(SupportPointWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.npPoint = QNodePicker(SupportPointWidget)
        self.npPoint.setObjectName(u"npPoint")
        sizePolicy.setHeightForWidth(self.npPoint.sizePolicy().hasHeightForWidth())
        self.npPoint.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.npPoint, 1, 1, 1, 1)

        self.widget_advanced = QWidget(SupportPointWidget)
        self.widget_advanced.setObjectName(u"widget_advanced")
        self.gridLayout = QGridLayout(self.widget_advanced)
        self.gridLayout.setObjectName(u"gridLayout")
        self.dsKx = QDoubleSpinBox(self.widget_advanced)
        self.dsKx.setObjectName(u"dsKx")
        self.dsKx.setMaximum(1000.000000000000000)
        self.dsKx.setSingleStep(0.500000000000000)

        self.gridLayout.addWidget(self.dsKx, 6, 1, 1, 1)

        self.dsDeltaZ = QDoubleSpinBox(self.widget_advanced)
        self.dsDeltaZ.setObjectName(u"dsDeltaZ")
        self.dsDeltaZ.setDecimals(3)
        self.dsDeltaZ.setMinimum(-101.000000000000000)
        self.dsDeltaZ.setMaximum(101.000000000000000)
        self.dsDeltaZ.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.dsDeltaZ, 4, 1, 1, 1)

        self.label_17 = QLabel(self.widget_advanced)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setWordWrap(True)

        self.gridLayout.addWidget(self.label_17, 5, 0, 1, 3)

        self.label_5 = QLabel(self.widget_advanced)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.dsKz = QDoubleSpinBox(self.widget_advanced)
        self.dsKz.setObjectName(u"dsKz")
        self.dsKz.setMaximum(10000000.000000000000000)
        self.dsKz.setSingleStep(100.000000000000000)

        self.gridLayout.addWidget(self.dsKz, 2, 1, 1, 1)

        self.label_6 = QLabel(self.widget_advanced)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)

        self.label_13 = QLabel(self.widget_advanced)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 4, 2, 1, 1)

        self.label_16 = QLabel(self.widget_advanced)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setWordWrap(True)

        self.gridLayout.addWidget(self.label_16, 3, 0, 1, 3)

        self.label_4 = QLabel(self.widget_advanced)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)

        self.dsKy = QDoubleSpinBox(self.widget_advanced)
        self.dsKy.setObjectName(u"dsKy")
        self.dsKy.setMaximum(1000.000000000000000)
        self.dsKy.setSingleStep(0.500000000000000)

        self.gridLayout.addWidget(self.dsKy, 7, 1, 1, 1)

        self.label = QLabel(self.widget_advanced)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.label_15 = QLabel(self.widget_advanced)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 7, 2, 1, 1)

        self.label_14 = QLabel(self.widget_advanced)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 6, 2, 1, 1)

        self.label_7 = QLabel(self.widget_advanced)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)

        self.label_18 = QLabel(self.widget_advanced)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setWordWrap(True)

        self.gridLayout.addWidget(self.label_18, 1, 0, 1, 3)


        self.gridLayout_2.addWidget(self.widget_advanced, 2, 0, 1, 2)

        QWidget.setTabOrder(self.dsKz, self.dsDeltaZ)
        QWidget.setTabOrder(self.dsDeltaZ, self.dsKx)
        QWidget.setTabOrder(self.dsKx, self.dsKy)

        self.retranslateUi(SupportPointWidget)

        QMetaObject.connectSlotsByName(SupportPointWidget)
    # setupUi

    def retranslateUi(self, SupportPointWidget):
        SupportPointWidget.setWindowTitle(QCoreApplication.translate("SupportPointWidget", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("SupportPointWidget", u"Frame", None))
        self.label_3.setText(QCoreApplication.translate("SupportPointWidget", u"Point", None))
        self.label_17.setText(QCoreApplication.translate("SupportPointWidget", u"Fx and Fy are multiplied by Fz. This makes them 0 if there is no contact.", None))
        self.label_5.setText(QCoreApplication.translate("SupportPointWidget", u"Z", None))
        self.label_6.setText(QCoreApplication.translate("SupportPointWidget", u"kx", None))
        self.label_13.setText(QCoreApplication.translate("SupportPointWidget", u"m", None))
        self.label_16.setText(QCoreApplication.translate("SupportPointWidget", u"Contact starts when Z location of \"Point\" relative to Frame is less than Z", None))
        self.label_4.setText(QCoreApplication.translate("SupportPointWidget", u"kN/m", None))
        self.label.setText(QCoreApplication.translate("SupportPointWidget", u"kz", None))
        self.label_15.setText(QCoreApplication.translate("SupportPointWidget", u"kN/m / Fz", None))
        self.label_14.setText(QCoreApplication.translate("SupportPointWidget", u"kN/m  / Fz", None))
        self.label_7.setText(QCoreApplication.translate("SupportPointWidget", u"ky", None))
        self.label_18.setText(QCoreApplication.translate("SupportPointWidget", u"Stiffness when \"Point\" contact \"Frame\"", None))
    # retranslateUi

