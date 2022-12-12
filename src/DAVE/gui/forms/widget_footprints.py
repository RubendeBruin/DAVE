# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_footprints.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_FootprintForm(object):
    def setupUi(self, FootprintForm):
        if not FootprintForm.objectName():
            FootprintForm.setObjectName(u"FootprintForm")
        FootprintForm.resize(506, 739)
        self.verticalLayout = QVBoxLayout(FootprintForm)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(FootprintForm)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)


        self.verticalLayout.addWidget(self.widget_2)

        self.splitter = QSplitter(FootprintForm)
        self.splitter.setObjectName(u"splitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy1)
        self.splitter.setOrientation(Qt.Horizontal)
        self.treeView = QTreeWidget(self.splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeView.setHeaderItem(__qtreewidgetitem)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setColumnCount(1)
        self.splitter.addWidget(self.treeView)
        self.treeView.header().setVisible(False)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.splitter.addWidget(self.widget)

        self.verticalLayout.addWidget(self.splitter)


        self.retranslateUi(FootprintForm)

        QMetaObject.connectSlotsByName(FootprintForm)
    # setupUi

    def retranslateUi(self, FootprintForm):
        FootprintForm.setWindowTitle(QCoreApplication.translate("FootprintForm", u"Form", None))
        self.label.setText(QCoreApplication.translate("FootprintForm", u"Footprints define over which length a force or weight is introduced.", None))
    # retranslateUi

