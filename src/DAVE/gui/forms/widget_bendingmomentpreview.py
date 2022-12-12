# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_bendingmomentpreview.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_WidgetBendingMomentPreview(object):
    def setupUi(self, WidgetBendingMomentPreview):
        if not WidgetBendingMomentPreview.objectName():
            WidgetBendingMomentPreview.setObjectName(u"WidgetBendingMomentPreview")
        WidgetBendingMomentPreview.resize(318, 256)
        self.formLayout = QFormLayout(WidgetBendingMomentPreview)
        self.formLayout.setObjectName(u"formLayout")
        self.label_5 = QLabel(WidgetBendingMomentPreview)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setWordWrap(True)

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.label_5)

        self.label_6 = QLabel(WidgetBendingMomentPreview)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setWordWrap(True)

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.label_6)

        self.label = QLabel(WidgetBendingMomentPreview)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label)

        self.cbAxis = QComboBox(WidgetBendingMomentPreview)
        self.cbAxis.setObjectName(u"cbAxis")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.cbAxis)

        self.label_2 = QLabel(WidgetBendingMomentPreview)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_2)

        self.cbOrientation = QComboBox(WidgetBendingMomentPreview)
        self.cbOrientation.setObjectName(u"cbOrientation")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.cbOrientation)

        self.label_3 = QLabel(WidgetBendingMomentPreview)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_3)

        self.label_4 = QLabel(WidgetBendingMomentPreview)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_4)

        self.sbScale = QDoubleSpinBox(WidgetBendingMomentPreview)
        self.sbScale.setObjectName(u"sbScale")
        self.sbScale.setMaximum(100.000000000000000)
        self.sbScale.setValue(2.000000000000000)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.sbScale)

        self.pbShear = QPushButton(WidgetBendingMomentPreview)
        self.pbShear.setObjectName(u"pbShear")

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.pbShear)

        self.pbBending = QPushButton(WidgetBendingMomentPreview)
        self.pbBending.setObjectName(u"pbBending")

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.pbBending)

        self.pbReport = QPushButton(WidgetBendingMomentPreview)
        self.pbReport.setObjectName(u"pbReport")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.pbReport)


        self.retranslateUi(WidgetBendingMomentPreview)

        QMetaObject.connectSlotsByName(WidgetBendingMomentPreview)
    # setupUi

    def retranslateUi(self, WidgetBendingMomentPreview):
        WidgetBendingMomentPreview.setWindowTitle(QCoreApplication.translate("WidgetBendingMomentPreview", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("WidgetBendingMomentPreview", u"Load / Shear / Modem analysis can be performed for any body or frame.", None))
        self.label_6.setText(QCoreApplication.translate("WidgetBendingMomentPreview", u"Select the frame or body for which the analysis shall be performed from the list below.\n"
"", None))
        self.label.setText(QCoreApplication.translate("WidgetBendingMomentPreview", u"Report for:", None))
        self.label_2.setText(QCoreApplication.translate("WidgetBendingMomentPreview", u"Using orientation from:", None))
#if QT_CONFIG(tooltip)
        self.cbOrientation.setToolTip(QCoreApplication.translate("WidgetBendingMomentPreview", u"<html><head/><body><p>By default the analysis will be performed for the local X-axis.</p><p>If any other axis is required then select any other system from this drop-down box.</p><p>The calculation will then be performed using the local x-axis of that node.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("WidgetBendingMomentPreview", u"Preview", None))
        self.label_4.setText(QCoreApplication.translate("WidgetBendingMomentPreview", u"Scale max to [m]", None))
        self.pbShear.setText(QCoreApplication.translate("WidgetBendingMomentPreview", u"Show Shear", None))
        self.pbBending.setText(QCoreApplication.translate("WidgetBendingMomentPreview", u"Show Bending", None))
        self.pbReport.setText(QCoreApplication.translate("WidgetBendingMomentPreview", u"Write report", None))
    # retranslateUi

