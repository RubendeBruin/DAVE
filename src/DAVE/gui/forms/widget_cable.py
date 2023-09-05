# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_cable.ui'
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
    QVBoxLayout, QWidget)

class Ui_Cable_form(object):
    def setupUi(self, Cable_form):
        if not Cable_form.objectName():
            Cable_form.setObjectName(u"Cable_form")
        Cable_form.resize(293, 237)
        Cable_form.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(Cable_form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_7 = QLabel(Cable_form)
        self.label_7.setObjectName(u"label_7")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMaximumSize(QSize(16777215, 30))
        self.label_7.setAutoFillBackground(False)
        self.label_7.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.label_7)

        self.frame_2 = QFrame(Cable_form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame_2)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        self.doubleSpinBox_1.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-1000000000000000000.000000000000000)
        self.doubleSpinBox_1.setMaximum(999999999999.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBox_1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(0.000000000000000)
        self.doubleSpinBox_2.setMaximum(999999999999.000000000000000)
        self.doubleSpinBox_2.setSingleStep(1000.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.doubleSpinBox_2)

        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.doubleSpinBox = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox.setSingleStep(0.001000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.doubleSpinBox)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_9)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        self.doubleSpinBox_4.setDecimals(3)
        self.doubleSpinBox_4.setMaximum(999999.000000000000000)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.doubleSpinBox_4)

        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.frame_2)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setSingleStep(0.001000000000000)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.doubleSpinBox_3)

        self.widget = QWidget(self.frame_2)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.cbSolveSegmentLengths = QCheckBox(self.widget)
        self.cbSolveSegmentLengths.setObjectName(u"cbSolveSegmentLengths")

        self.horizontalLayout.addWidget(self.cbSolveSegmentLengths)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setWordWrap(True)

        self.horizontalLayout.addWidget(self.label_3)


        self.formLayout.setWidget(5, QFormLayout.SpanningRole, self.widget)


        self.verticalLayout.addWidget(self.frame_2)

        QWidget.setTabOrder(self.doubleSpinBox_1, self.doubleSpinBox_2)
        QWidget.setTabOrder(self.doubleSpinBox_2, self.doubleSpinBox)
        QWidget.setTabOrder(self.doubleSpinBox, self.doubleSpinBox_4)

        self.retranslateUi(Cable_form)

        QMetaObject.connectSlotsByName(Cable_form)
    # setupUi

    def retranslateUi(self, Cable_form):
        Cable_form.setWindowTitle(QCoreApplication.translate("Cable_form", u"Form", None))
        self.label_7.setText(QCoreApplication.translate("Cable_form", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Cable properties</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Cable_form", u"Length at rest [m]", None))
        self.label_2.setText(QCoreApplication.translate("Cable_form", u"Stiffness EA [kN]", None))
        self.label_4.setText(QCoreApplication.translate("Cable_form", u"Diameter [m]", None))
        self.label_9.setText(QCoreApplication.translate("Cable_form", u"Mass [mT]", None))
        self.label_5.setText(QCoreApplication.translate("Cable_form", u"Mass per length [mT/m] ", None))
        self.cbSolveSegmentLengths.setText("")
        self.label_3.setText(QCoreApplication.translate("Cable_form", u"[Experimental!] Solve cable length re-distribution due to cable weight", None))
    # retranslateUi

