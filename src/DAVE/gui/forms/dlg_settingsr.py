# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlg_settings.ui',
# licensing of 'dlg_settings.ui' applies.
#
# Created: Sun May 15 10:28:59 2022
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_frmSettings(object):
    def setupUi(self, frmSettings):
        frmSettings.setObjectName("frmSettings")
        frmSettings.resize(473, 294)
        self.verticalLayout = QtWidgets.QVBoxLayout(frmSettings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(frmSettings)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(frmSettings)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label = QtWidgets.QLabel(frmSettings)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(frmSettings)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(frmSettings)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(frmSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(frmSettings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), frmSettings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), frmSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(frmSettings)

    def retranslateUi(self, frmSettings):
        frmSettings.setWindowTitle(QtWidgets.QApplication.translate("frmSettings", "Dialog", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("frmSettings", "Standard resource paths:", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("frmSettings", "TextLabel", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("frmSettings", "Additional asset paths:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("frmSettings", "<html><head/><body><p>Additional info see: <a href=\"https://davedocs.online/assets_and_resources.html\"><span style=\" text-decoration: underline; color:#0000ff;\">https://davedocs.online/assets_and_resources.html</span></a></p></body></html>", None, -1))

