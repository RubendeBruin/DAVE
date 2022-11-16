# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_solver.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(336, 142)
        Dialog.setWindowOpacity(1.000000000000000)
        Dialog.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        Dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.btnTerminate = QPushButton(Dialog)
        self.btnTerminate.setObjectName(u"btnTerminate")

        self.verticalLayout.addWidget(self.btnTerminate)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Working", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Doing what you told me to do.", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"< Info >", None))
        self.btnTerminate.setText(QCoreApplication.translate("Dialog", u"Terminate solver", None))
    # retranslateUi

