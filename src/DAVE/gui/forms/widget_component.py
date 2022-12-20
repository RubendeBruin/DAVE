# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_component.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_component(object):
    def setupUi(self, component):
        if not component.objectName():
            component.setObjectName(u"component")
        component.resize(326, 57)
        component.setStyleSheet(u"")
        self.gridLayout = QGridLayout(component)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.cbPath = QComboBox(component)
        self.cbPath.setObjectName(u"cbPath")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbPath.sizePolicy().hasHeightForWidth())
        self.cbPath.setSizePolicy(sizePolicy)
        self.cbPath.setEditable(True)

        self.gridLayout.addWidget(self.cbPath, 1, 1, 1, 1)

        self.label = QLabel(component)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.pbReScan = QPushButton(component)
        self.pbReScan.setObjectName(u"pbReScan")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pbReScan.sizePolicy().hasHeightForWidth())
        self.pbReScan.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.pbReScan, 1, 2, 1, 1)

        self.pbEditExposedProperties = QPushButton(component)
        self.pbEditExposedProperties.setObjectName(u"pbEditExposedProperties")

        self.gridLayout.addWidget(self.pbEditExposedProperties, 2, 1, 1, 1)


        self.retranslateUi(component)

        QMetaObject.connectSlotsByName(component)
    # setupUi

    def retranslateUi(self, component):
        component.setWindowTitle(QCoreApplication.translate("component", u"Form", None))
        self.label.setText(QCoreApplication.translate("component", u"File:", None))
        self.pbReScan.setText(QCoreApplication.translate("component", u"Rescan", None))
        self.pbEditExposedProperties.setText(QCoreApplication.translate("component", u"Edit exposed properties", None))
    # retranslateUi

