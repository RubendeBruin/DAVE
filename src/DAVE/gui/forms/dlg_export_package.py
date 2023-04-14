# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_export_package.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_ExportPackage(object):
    def setupUi(self, ExportPackage):
        if not ExportPackage.objectName():
            ExportPackage.setObjectName(u"ExportPackage")
        ExportPackage.resize(426, 313)
        ExportPackage.setSizeGripEnabled(True)
        self.verticalLayout = QVBoxLayout(ExportPackage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(ExportPackage)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.cbStripVisuals = QCheckBox(self.widget)
        self.cbStripVisuals.setObjectName(u"cbStripVisuals")

        self.verticalLayout_2.addWidget(self.cbStripVisuals)

        self.cbFlatten = QCheckBox(self.widget)
        self.cbFlatten.setObjectName(u"cbFlatten")

        self.verticalLayout_2.addWidget(self.cbFlatten)

        self.cbZip = QCheckBox(self.widget)
        self.cbZip.setObjectName(u"cbZip")
        self.cbZip.setChecked(True)

        self.verticalLayout_2.addWidget(self.cbZip)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, -1, 0, -1)
        self.tbFolder = QLineEdit(self.widget_2)
        self.tbFolder.setObjectName(u"tbFolder")

        self.horizontalLayout.addWidget(self.tbFolder)

        self.pbBrowse = QPushButton(self.widget_2)
        self.pbBrowse.setObjectName(u"pbBrowse")

        self.horizontalLayout.addWidget(self.pbBrowse)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.teLog = QPlainTextEdit(self.widget)
        self.teLog.setObjectName(u"teLog")
        self.teLog.setAutoFillBackground(True)
        self.teLog.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.teLog)

        self.pbExport = QPushButton(self.widget)
        self.pbExport.setObjectName(u"pbExport")

        self.verticalLayout_2.addWidget(self.pbExport)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(ExportPackage)

        QMetaObject.connectSlotsByName(ExportPackage)
    # setupUi

    def retranslateUi(self, ExportPackage):
        ExportPackage.setWindowTitle(QCoreApplication.translate("ExportPackage", u"Export self-contained package", None))
        self.label.setText(QCoreApplication.translate("ExportPackage", u"Export DAVE model to self-contained package.", None))
        self.cbStripVisuals.setText(QCoreApplication.translate("ExportPackage", u"Strip visuals", None))
        self.cbFlatten.setText(QCoreApplication.translate("ExportPackage", u"Flatten", None))
        self.cbZip.setText(QCoreApplication.translate("ExportPackage", u"Create .zip file", None))
        self.label_2.setText(QCoreApplication.translate("ExportPackage", u"Export location (folder)", None))
        self.pbBrowse.setText(QCoreApplication.translate("ExportPackage", u"...", None))
        self.teLog.setPlainText(QCoreApplication.translate("ExportPackage", u"Click EXPORT to start export", None))
        self.pbExport.setText(QCoreApplication.translate("ExportPackage", u"Export", None))
    # retranslateUi

