# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_name.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_NameWidget(object):
    def setupUi(self, NameWidget):
        if not NameWidget.objectName():
            NameWidget.setObjectName(u"NameWidget")
        NameWidget.resize(254, 61)
        NameWidget.setMinimumSize(QSize(0, 0))
        self.gridLayout = QGridLayout(NameWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label2 = QLabel(NameWidget)
        self.label2.setObjectName(u"label2")
        self.label2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label2, 2, 2, 1, 1)

        self.cbVisible = QCheckBox(NameWidget)
        self.cbVisible.setObjectName(u"cbVisible")

        self.gridLayout.addWidget(self.cbVisible, 2, 1, 1, 1)

        self.label = QLabel(NameWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lbColor = QLabel(NameWidget)
        self.lbColor.setObjectName(u"lbColor")
        self.lbColor.setStyleSheet(u"background-color: rgb(255, 170, 0);")
        self.lbColor.setFrameShape(QFrame.NoFrame)

        self.gridLayout.addWidget(self.lbColor, 2, 3, 1, 1)

        self.tbName = QLineEdit(NameWidget)
        self.tbName.setObjectName(u"tbName")

        self.gridLayout.addWidget(self.tbName, 0, 1, 1, 3)

        self.lblInfo = QLabel(NameWidget)
        self.lblInfo.setObjectName(u"lblInfo")
        self.lblInfo.setStyleSheet(u"color: rgb(200, 100, 0)")

        self.gridLayout.addWidget(self.lblInfo, 1, 1, 1, 3)


        self.retranslateUi(NameWidget)

        QMetaObject.connectSlotsByName(NameWidget)
    # setupUi

    def retranslateUi(self, NameWidget):
        NameWidget.setWindowTitle(QCoreApplication.translate("NameWidget", u"Form", None))
        self.label2.setText(QCoreApplication.translate("NameWidget", u"Color:", None))
        self.cbVisible.setText(QCoreApplication.translate("NameWidget", u"Visual visible", None))
        self.label.setText(QCoreApplication.translate("NameWidget", u"Name [unique]", None))
#if QT_CONFIG(tooltip)
        self.lbColor.setToolTip(QCoreApplication.translate("NameWidget", u"click to change, right-click to reset", None))
#endif // QT_CONFIG(tooltip)
        self.lbColor.setText(QCoreApplication.translate("NameWidget", u"default", None))
        self.lblInfo.setText(QCoreApplication.translate("NameWidget", u"TextLabel", None))
    # retranslateUi

