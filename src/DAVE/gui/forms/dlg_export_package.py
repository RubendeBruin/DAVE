# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_export_package.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGridLayout,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ExportPackage(object):
    def setupUi(self, ExportPackage):
        if not ExportPackage.objectName():
            ExportPackage.setObjectName(u"ExportPackage")
        ExportPackage.resize(501, 631)
        ExportPackage.setSizeGripEnabled(True)
        self.verticalLayout = QVBoxLayout(ExportPackage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(ExportPackage)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label)

        self.cbStripVisuals = QCheckBox(self.widget)
        self.cbStripVisuals.setObjectName(u"cbStripVisuals")

        self.verticalLayout_2.addWidget(self.cbStripVisuals)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_3)

        self.cbFlatten = QCheckBox(self.widget)
        self.cbFlatten.setObjectName(u"cbFlatten")

        self.verticalLayout_2.addWidget(self.cbFlatten)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_4)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.pbBrowse = QPushButton(self.widget_2)
        self.pbBrowse.setObjectName(u"pbBrowse")

        self.gridLayout.addWidget(self.pbBrowse, 0, 3, 1, 1)

        self.tbFile = QLineEdit(self.widget_2)
        self.tbFile.setObjectName(u"tbFile")

        self.gridLayout.addWidget(self.tbFile, 0, 2, 1, 1)

        self.pbExport = QPushButton(self.widget_2)
        self.pbExport.setObjectName(u"pbExport")

        self.gridLayout.addWidget(self.pbExport, 1, 2, 1, 1)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.lblInfo = QLabel(self.widget)
        self.lblInfo.setObjectName(u"lblInfo")

        self.verticalLayout_2.addWidget(self.lblInfo)

        self.teLog = QPlainTextEdit(self.widget)
        self.teLog.setObjectName(u"teLog")
        self.teLog.setAutoFillBackground(True)
        self.teLog.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.teLog)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(ExportPackage)

        QMetaObject.connectSlotsByName(ExportPackage)
    # setupUi

    def retranslateUi(self, ExportPackage):
        ExportPackage.setWindowTitle(QCoreApplication.translate("ExportPackage", u"Export self-contained package", None))
        self.label.setText(QCoreApplication.translate("ExportPackage", u"<html><head/><body><p><span style=\" font-weight:700;\">Export DAVE model to self-contained package.</span></p><p>The export option exports the current DAVE model including all the resources that it needs.", None))
        self.cbStripVisuals.setText(QCoreApplication.translate("ExportPackage", u"Strip visuals", None))
        self.label_3.setText(QCoreApplication.translate("ExportPackage", u"<html><head/><body><p>Strip visuals removes all visuals from the model before exporting.</p></body></html>", None))
        self.cbFlatten.setText(QCoreApplication.translate("ExportPackage", u"Flatten", None))
        self.label_4.setText(QCoreApplication.translate("ExportPackage", u"<html><head/><body><p>Flatten will recursively dissolve all nodes to bring the model to its most basic state. Doing so makes it more likely that a basic version of DAVE can open the file.</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("ExportPackage", u"Export location (folder)", None))
        self.label_5.setText(QCoreApplication.translate("ExportPackage", u"Save as:", None))
        self.pbBrowse.setText(QCoreApplication.translate("ExportPackage", u"...", None))
        self.pbExport.setText(QCoreApplication.translate("ExportPackage", u"EXPORT", None))
        self.lblInfo.setText(QCoreApplication.translate("ExportPackage", u"Log:", None))
        self.teLog.setPlainText(QCoreApplication.translate("ExportPackage", u"Click EXPORT to start export", None))
    # retranslateUi

