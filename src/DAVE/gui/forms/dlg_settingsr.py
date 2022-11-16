# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_settings.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_frmSettings(object):
    def setupUi(self, frmSettings):
        if not frmSettings.objectName():
            frmSettings.setObjectName(u"frmSettings")
        frmSettings.resize(473, 294)
        self.verticalLayout = QVBoxLayout(frmSettings)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(frmSettings)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(frmSettings)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.label_4)

        self.label_2 = QLabel(frmSettings)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_2.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.label_2)

        self.label = QLabel(frmSettings)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.plainTextEdit = QPlainTextEdit(frmSettings)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.verticalLayout.addWidget(self.plainTextEdit)

        self.buttonBox = QDialogButtonBox(frmSettings)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(frmSettings)
        self.buttonBox.accepted.connect(frmSettings.accept)
        self.buttonBox.rejected.connect(frmSettings.reject)

        QMetaObject.connectSlotsByName(frmSettings)
    # setupUi

    def retranslateUi(self, frmSettings):
        frmSettings.setWindowTitle(QCoreApplication.translate("frmSettings", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("frmSettings", u"Standard resource paths:", None))
        self.label_4.setText(QCoreApplication.translate("frmSettings", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("frmSettings", u"<html><head/><body><p>Additional info see: <a href=\"https://davedocs.online/assets_and_resources.html\"><span style=\" text-decoration: underline; color:#0000ff;\">https://davedocs.online/assets_and_resources.html</span></a></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("frmSettings", u"Additional asset paths:", None))
    # retranslateUi

