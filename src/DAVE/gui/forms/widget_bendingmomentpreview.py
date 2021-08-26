# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_bendingmomentpreview.ui',
# licensing of 'widget_bendingmomentpreview.ui' applies.
#
# Created: Thu Aug 26 08:41:34 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_WidgetBendingMomentPreview(object):
    def setupUi(self, WidgetBendingMomentPreview):
        WidgetBendingMomentPreview.setObjectName("WidgetBendingMomentPreview")
        WidgetBendingMomentPreview.resize(318, 256)
        self.formLayout = QtWidgets.QFormLayout(WidgetBendingMomentPreview)
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(WidgetBendingMomentPreview)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(WidgetBendingMomentPreview)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.label_6)
        self.label = QtWidgets.QLabel(WidgetBendingMomentPreview)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.cbAxis = QtWidgets.QComboBox(WidgetBendingMomentPreview)
        self.cbAxis.setObjectName("cbAxis")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cbAxis)
        self.label_2 = QtWidgets.QLabel(WidgetBendingMomentPreview)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.cbOrientation = QtWidgets.QComboBox(WidgetBendingMomentPreview)
        self.cbOrientation.setObjectName("cbOrientation")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.cbOrientation)
        self.label_3 = QtWidgets.QLabel(WidgetBendingMomentPreview)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(WidgetBendingMomentPreview)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.sbScale = QtWidgets.QDoubleSpinBox(WidgetBendingMomentPreview)
        self.sbScale.setMaximum(100.0)
        self.sbScale.setProperty("value", 2.0)
        self.sbScale.setObjectName("sbScale")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.sbScale)
        self.pbShear = QtWidgets.QPushButton(WidgetBendingMomentPreview)
        self.pbShear.setObjectName("pbShear")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.pbShear)
        self.pbBending = QtWidgets.QPushButton(WidgetBendingMomentPreview)
        self.pbBending.setObjectName("pbBending")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.pbBending)
        self.pbReport = QtWidgets.QPushButton(WidgetBendingMomentPreview)
        self.pbReport.setObjectName("pbReport")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.pbReport)

        self.retranslateUi(WidgetBendingMomentPreview)
        QtCore.QMetaObject.connectSlotsByName(WidgetBendingMomentPreview)

    def retranslateUi(self, WidgetBendingMomentPreview):
        WidgetBendingMomentPreview.setWindowTitle(QtWidgets.QApplication.translate("WidgetBendingMomentPreview", "Form", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("WidgetBendingMomentPreview", "Load / Shear / Modem analysis can be performed for any body or frame.", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("WidgetBendingMomentPreview", "Select the frame or body for which the analysis shall be performed from the list below.\n"
"", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("WidgetBendingMomentPreview", "Report for:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("WidgetBendingMomentPreview", "Using orientation from:", None, -1))
        self.cbOrientation.setToolTip(QtWidgets.QApplication.translate("WidgetBendingMomentPreview", "<html><head/><body><p>By default the analysis will be performed for the local X-axis.</p><p>If any other axis is required then select any other system from this drop-down box.</p><p>The calculation will then be performed using the local x-axis of that node.</p></body></html>", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("WidgetBendingMomentPreview", "Preview", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("WidgetBendingMomentPreview", "Scale max to [m]", None, -1))
        self.pbShear.setText(QtWidgets.QApplication.translate("WidgetBendingMomentPreview", "Show Shear", None, -1))
        self.pbBending.setText(QtWidgets.QApplication.translate("WidgetBendingMomentPreview", "Show Bending", None, -1))
        self.pbReport.setText(QtWidgets.QApplication.translate("WidgetBendingMomentPreview", "Write report", None, -1))

