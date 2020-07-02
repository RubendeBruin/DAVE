# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_contactball.ui',
# licensing of 'widget_contactball.ui' applies.
#
# Created: Thu Jul  2 20:34:21 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_widget_contactball(object):
    def setupUi(self, widget_contactball):
        widget_contactball.setObjectName("widget_contactball")
        widget_contactball.resize(396, 442)
        widget_contactball.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.gridLayout = QtWidgets.QGridLayout(widget_contactball)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(widget_contactball)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(widget_contactball)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.sbR = QtWidgets.QDoubleSpinBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbR.sizePolicy().hasHeightForWidth())
        self.sbR.setSizePolicy(sizePolicy)
        self.sbR.setDecimals(3)
        self.sbR.setMinimum(0.0)
        self.sbR.setMaximum(99999999999999.0)
        self.sbR.setObjectName("sbR")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.sbR)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.sbK = QtWidgets.QDoubleSpinBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbK.sizePolicy().hasHeightForWidth())
        self.sbK.setSizePolicy(sizePolicy)
        self.sbK.setDecimals(3)
        self.sbK.setMinimum(0.0)
        self.sbK.setMaximum(99999999999999.0)
        self.sbK.setSingleStep(100.0)
        self.sbK.setObjectName("sbK")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sbK)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 2)
        self.label_9 = QtWidgets.QLabel(widget_contactball)
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 2)
        self.lwMeshes = QtWidgets.QListWidget(widget_contactball)
        self.lwMeshes.setAcceptDrops(True)
        self.lwMeshes.setObjectName("lwMeshes")
        self.gridLayout.addWidget(self.lwMeshes, 3, 0, 1, 2)
        self.pbRemoveSelected = QtWidgets.QPushButton(widget_contactball)
        self.pbRemoveSelected.setObjectName("pbRemoveSelected")
        self.gridLayout.addWidget(self.pbRemoveSelected, 4, 1, 1, 1)

        self.retranslateUi(widget_contactball)
        QtCore.QMetaObject.connectSlotsByName(widget_contactball)
        widget_contactball.setTabOrder(self.sbR, self.sbK)

    def retranslateUi(self, widget_contactball):
        widget_contactball.setWindowTitle(QtWidgets.QApplication.translate("widget_contactball", "Form", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("widget_contactball", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Ball</span></p></body></html>", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("widget_contactball", "Radius [m]", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("widget_contactball", "Stiffness [kN/m]", None, -1))
        self.label_9.setText(QtWidgets.QApplication.translate("widget_contactball", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Meshes</span></p><p>Meshes that this ball can make contact with need to be listed here explicitly</p><p>To add meshes, drag and drop them from the node-tree</p><p><br/></p></body></html>", None, -1))
        self.pbRemoveSelected.setText(QtWidgets.QApplication.translate("widget_contactball", "remove selected point", None, -1))

