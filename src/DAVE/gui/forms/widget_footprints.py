# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_footprints.ui',
# licensing of 'widget_footprints.ui' applies.
#
# Created: Sat Jun 19 08:06:59 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_FootprintForm(object):
    def setupUi(self, FootprintForm):
        FootprintForm.setObjectName("FootprintForm")
        FootprintForm.resize(506, 739)
        self.verticalLayout = QtWidgets.QVBoxLayout(FootprintForm)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(FootprintForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.verticalLayout.addWidget(self.widget_2)
        self.splitter = QtWidgets.QSplitter(FootprintForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.treeView = QtWidgets.QTreeWidget(self.splitter)
        self.treeView.setColumnCount(1)
        self.treeView.setObjectName("treeView")
        self.treeView.headerItem().setText(0, "1")
        self.treeView.header().setVisible(False)
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(FootprintForm)
        QtCore.QMetaObject.connectSlotsByName(FootprintForm)

    def retranslateUi(self, FootprintForm):
        FootprintForm.setWindowTitle(QtWidgets.QApplication.translate("FootprintForm", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("FootprintForm", "Footprints define over which length a force or weight is introduced.", None, -1))

