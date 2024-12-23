# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_visual.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from DAVE.gui.helpers.qnodepicker import QNodePicker
from DAVE.gui.helpers.resource_selector import QResourceSelector

class Ui_widget_axis(object):
    def setupUi(self, widget_axis):
        if not widget_axis.objectName():
            widget_axis.setObjectName(u"widget_axis")
        widget_axis.resize(325, 642)
        widget_axis.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widget_axis)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_18 = QLabel(widget_axis)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_18)

        self.widget_2 = QWidget(widget_axis)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_13 = QLabel(self.widget_2)
        self.label_13.setObjectName(u"label_13")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_13)

        self.widgetParent = QNodePicker(self.widget_2)
        self.widgetParent.setObjectName(u"widgetParent")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widgetParent.sizePolicy().hasHeightForWidth())
        self.widgetParent.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.widgetParent)


        self.verticalLayout.addWidget(self.widget_2)

        self.label_12 = QLabel(widget_axis)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_12)

        self.widget = QWidget(widget_axis)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.widget)

        self.resource_selector = QResourceSelector(widget_axis)
        self.resource_selector.setObjectName(u"resource_selector")

        self.verticalLayout.addWidget(self.resource_selector)

        self.label_17 = QLabel(widget_axis)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_17)

        self.cbInvertNormals = QCheckBox(widget_axis)
        self.cbInvertNormals.setObjectName(u"cbInvertNormals")

        self.verticalLayout.addWidget(self.cbInvertNormals)

        self.frame = QFrame(widget_axis)
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
        self.formLayout.setContentsMargins(9, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label)

        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_1.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_1.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_1.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.doubleSpinBox_1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_2)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_2.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.doubleSpinBox_2)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_3)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_3.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_3.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_3.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.doubleSpinBox_3)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.HLine)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.frame_2)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.label_4)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_4.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_4.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_4.setDecimals(3)
        self.doubleSpinBox_4.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_4.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(11, QFormLayout.FieldRole, self.doubleSpinBox_4)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(12, QFormLayout.LabelRole, self.label_5)

        self.doubleSpinBox_5 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_5.setObjectName(u"doubleSpinBox_5")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_5.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_5.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_5.setDecimals(3)
        self.doubleSpinBox_5.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_5.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(12, QFormLayout.FieldRole, self.doubleSpinBox_5)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(13, QFormLayout.LabelRole, self.label_6)

        self.doubleSpinBox_6 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_6.setObjectName(u"doubleSpinBox_6")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_6.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_6.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_6.setDecimals(3)
        self.doubleSpinBox_6.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_6.setMaximum(99999999999999.000000000000000)

        self.formLayout.setWidget(13, QFormLayout.FieldRole, self.doubleSpinBox_6)

        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.HLine)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.formLayout.setWidget(14, QFormLayout.LabelRole, self.frame_6)

        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_11)

        self.doubleSpinBox_8 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_8.setObjectName(u"doubleSpinBox_8")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_8.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_8.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_8.setDecimals(3)
        self.doubleSpinBox_8.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_8.setMaximum(99999999999999.000000000000000)
        self.doubleSpinBox_8.setValue(1.000000000000000)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.doubleSpinBox_8)

        self.label_10 = QLabel(self.frame)
        self.label_10.setObjectName(u"label_10")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_10)

        self.doubleSpinBox_9 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_9.setObjectName(u"doubleSpinBox_9")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_9.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_9.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_9.setDecimals(3)
        self.doubleSpinBox_9.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_9.setMaximum(99999999999999.000000000000000)
        self.doubleSpinBox_9.setValue(1.000000000000000)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.doubleSpinBox_9)

        self.label_16 = QLabel(self.frame)
        self.label_16.setObjectName(u"label_16")

        self.formLayout.setWidget(10, QFormLayout.SpanningRole, self.label_16)

        self.label_14 = QLabel(self.frame)
        self.label_14.setObjectName(u"label_14")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.label_14)

        self.label_15 = QLabel(self.frame)
        self.label_15.setObjectName(u"label_15")

        self.formLayout.setWidget(5, QFormLayout.SpanningRole, self.label_15)

        self.doubleSpinBox_7 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_7.setObjectName(u"doubleSpinBox_7")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox_7.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_7.setSizePolicy(sizePolicy2)
        self.doubleSpinBox_7.setDecimals(3)
        self.doubleSpinBox_7.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_7.setMaximum(99999999999999.000000000000000)
        self.doubleSpinBox_7.setValue(1.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.doubleSpinBox_7)

        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_9)


        self.verticalLayout.addWidget(self.frame)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.doubleSpinBox_8, self.doubleSpinBox_9)
        QWidget.setTabOrder(self.doubleSpinBox_9, self.doubleSpinBox_1)
        QWidget.setTabOrder(self.doubleSpinBox_1, self.doubleSpinBox_2)
        QWidget.setTabOrder(self.doubleSpinBox_2, self.doubleSpinBox_3)
        QWidget.setTabOrder(self.doubleSpinBox_3, self.doubleSpinBox_4)
        QWidget.setTabOrder(self.doubleSpinBox_4, self.doubleSpinBox_5)
        QWidget.setTabOrder(self.doubleSpinBox_5, self.doubleSpinBox_6)

        self.retranslateUi(widget_axis)

        QMetaObject.connectSlotsByName(widget_axis)
    # setupUi

    def retranslateUi(self, widget_axis):
        widget_axis.setWindowTitle(QCoreApplication.translate("widget_axis", u"Form", None))
        self.label_18.setText(QCoreApplication.translate("widget_axis", u"<html><head/><body><p><span style=\" font-weight:600;\">Shape attached to</span></p></body></html>", None))
        self.label_13.setText(QCoreApplication.translate("widget_axis", u"Parent", None))
        self.label_12.setText(QCoreApplication.translate("widget_axis", u"<html><head/><body><p><span style=\" font-weight:600;\">Shape (file)</span></p></body></html>", None))
        self.label_17.setText(QCoreApplication.translate("widget_axis", u"<html><head/><body><p><span style=\" font-weight:600;\">Shape modification</span></p></body></html>", None))
        self.cbInvertNormals.setText(QCoreApplication.translate("widget_axis", u"Invert normals", None))
        self.label.setText(QCoreApplication.translate("widget_axis", u"X", None))
        self.label_2.setText(QCoreApplication.translate("widget_axis", u"Y", None))
        self.label_3.setText(QCoreApplication.translate("widget_axis", u"Z", None))
        self.label_4.setText(QCoreApplication.translate("widget_axis", u"X", None))
        self.label_5.setText(QCoreApplication.translate("widget_axis", u"Y", None))
        self.label_6.setText(QCoreApplication.translate("widget_axis", u"Z", None))
        self.label_11.setText(QCoreApplication.translate("widget_axis", u"Y", None))
        self.label_10.setText(QCoreApplication.translate("widget_axis", u"Z", None))
        self.label_16.setText(QCoreApplication.translate("widget_axis", u"Apply rotation vector", None))
        self.label_14.setText(QCoreApplication.translate("widget_axis", u"Apply scale", None))
        self.label_15.setText(QCoreApplication.translate("widget_axis", u"Apply offset", None))
        self.label_9.setText(QCoreApplication.translate("widget_axis", u"X", None))
    # retranslateUi

