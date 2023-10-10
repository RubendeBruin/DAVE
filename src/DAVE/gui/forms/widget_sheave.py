# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_sheave.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from DAVE.gui.helpers.qnodepicker import QNodePicker

class Ui_widget_sheave(object):
    def setupUi(self, widget_sheave):
        if not widget_sheave.objectName():
            widget_sheave.setObjectName(u"widget_sheave")
        widget_sheave.resize(323, 813)
        widget_sheave.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widget_sheave)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(widget_sheave)
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

        self.label_9 = QLabel(widget_sheave)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_9)

        self.sbRadius = QDoubleSpinBox(widget_sheave)
        self.sbRadius.setObjectName(u"sbRadius")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sbRadius.sizePolicy().hasHeightForWidth())
        self.sbRadius.setSizePolicy(sizePolicy2)
        self.sbRadius.setDecimals(3)
        self.sbRadius.setMinimum(-999999999999.000000000000000)
        self.sbRadius.setMaximum(99999999999999.000000000000000)

        self.verticalLayout.addWidget(self.sbRadius)

        self.label_7 = QLabel(widget_sheave)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_7)

        self.frame = QFrame(widget_sheave)
        self.frame.setObjectName(u"frame")
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.sbAX = QDoubleSpinBox(self.frame)
        self.sbAX.setObjectName(u"sbAX")
        sizePolicy2.setHeightForWidth(self.sbAX.sizePolicy().hasHeightForWidth())
        self.sbAX.setSizePolicy(sizePolicy2)
        self.sbAX.setDecimals(3)
        self.sbAX.setMinimum(-999999999999.000000000000000)
        self.sbAX.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sbAX)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.sbAY = QDoubleSpinBox(self.frame)
        self.sbAY.setObjectName(u"sbAY")
        sizePolicy2.setHeightForWidth(self.sbAY.sizePolicy().hasHeightForWidth())
        self.sbAY.setSizePolicy(sizePolicy2)
        self.sbAY.setDecimals(3)
        self.sbAY.setMinimum(-999999999999.000000000000000)
        self.sbAY.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sbAY)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.sbAZ = QDoubleSpinBox(self.frame)
        self.sbAZ.setObjectName(u"sbAZ")
        sizePolicy2.setHeightForWidth(self.sbAZ.sizePolicy().hasHeightForWidth())
        self.sbAZ.setSizePolicy(sizePolicy2)
        self.sbAZ.setDecimals(3)
        self.sbAZ.setMinimum(-999999999999.000000000000000)
        self.sbAZ.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.sbAZ)


        self.verticalLayout.addWidget(self.frame)

        self.cbIsRoundBar = QCheckBox(widget_sheave)
        self.cbIsRoundBar.setObjectName(u"cbIsRoundBar")

        self.verticalLayout.addWidget(self.cbIsRoundBar)

        self.rbWidget = QWidget(widget_sheave)
        self.rbWidget.setObjectName(u"rbWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.rbWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.rbWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.sbStart = QDoubleSpinBox(self.rbWidget)
        self.sbStart.setObjectName(u"sbStart")
        self.sbStart.setDecimals(3)
        self.sbStart.setMinimum(-999999.000000000000000)
        self.sbStart.setMaximum(999999.000000000000000)
        self.sbStart.setValue(-1.000000000000000)

        self.horizontalLayout_2.addWidget(self.sbStart)

        self.label_5 = QLabel(self.rbWidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_5)

        self.sbStop = QDoubleSpinBox(self.rbWidget)
        self.sbStop.setObjectName(u"sbStop")
        self.sbStop.setDecimals(3)
        self.sbStop.setMinimum(-999999.000000000000000)
        self.sbStop.setMaximum(999999.000000000000000)
        self.sbStop.setValue(1.000000000000000)

        self.horizontalLayout_2.addWidget(self.sbStop)


        self.verticalLayout.addWidget(self.rbWidget)

        self.label_8 = QLabel(widget_sheave)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.sbRadius, self.sbAX)
        QWidget.setTabOrder(self.sbAX, self.sbAY)
        QWidget.setTabOrder(self.sbAY, self.sbAZ)
        QWidget.setTabOrder(self.sbAZ, self.cbIsRoundBar)
        QWidget.setTabOrder(self.cbIsRoundBar, self.sbStart)
        QWidget.setTabOrder(self.sbStart, self.sbStop)

        self.retranslateUi(widget_sheave)

        QMetaObject.connectSlotsByName(widget_sheave)
    # setupUi

    def retranslateUi(self, widget_sheave):
        widget_sheave.setWindowTitle(QCoreApplication.translate("widget_sheave", u"Form", None))
        self.label_10.setText(QCoreApplication.translate("widget_sheave", u"Parent", None))
        self.label_9.setText(QCoreApplication.translate("widget_sheave", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Circle radius</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("widget_sheave", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Axis direction</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("widget_sheave", u"X", None))
        self.label_2.setText(QCoreApplication.translate("widget_sheave", u"Y", None))
        self.label_3.setText(QCoreApplication.translate("widget_sheave", u"Z", None))
        self.cbIsRoundBar.setText(QCoreApplication.translate("widget_sheave", u"Is a round-bar", None))
        self.label_4.setText(QCoreApplication.translate("widget_sheave", u"show visual between", None))
        self.label_5.setText(QCoreApplication.translate("widget_sheave", u"and", None))
        self.label_8.setText(QCoreApplication.translate("widget_sheave", u"<html><head/><body><p>Axis direction is defined in parent axis system.</p><p>Wire runs over the circle in positive direction (apply right hand rule on axis direction).</p></body></html>", None))
    # retranslateUi

