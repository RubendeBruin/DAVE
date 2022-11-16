# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addnode_form.ui'
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
        Dialog.resize(459, 522)
        Dialog.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(80, 0))
        self.label.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_2.addWidget(self.label)

        self.tbName = QLineEdit(self.frame_2)
        self.tbName.setObjectName(u"tbName")

        self.horizontalLayout_2.addWidget(self.tbName)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(60, 0))
        self.label_2.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_2.addWidget(self.label_2)


        self.verticalLayout.addWidget(self.frame_2)

        self.errUniqueName = QLabel(Dialog)
        self.errUniqueName.setObjectName(u"errUniqueName")

        self.verticalLayout.addWidget(self.errUniqueName)

        self.frmParent = QFrame(Dialog)
        self.frmParent.setObjectName(u"frmParent")
        self.frmParent.setFrameShape(QFrame.StyledPanel)
        self.frmParent.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frmParent)
        self.gridLayout.setObjectName(u"gridLayout")
        self.cbParentAxis = QComboBox(self.frmParent)
        self.cbParentAxis.setObjectName(u"cbParentAxis")

        self.gridLayout.addWidget(self.cbParentAxis, 0, 1, 1, 1)

        self.label_3 = QLabel(self.frmParent)
        self.label_3.setObjectName(u"label_3")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(80, 0))
        self.label_3.setMaximumSize(QSize(80, 16777215))

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_4 = QLabel(self.frmParent)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(60, 0))
        self.label_4.setMaximumSize(QSize(60, 16777215))

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)


        self.verticalLayout.addWidget(self.frmParent)

        self.frmParentPoi = QFrame(Dialog)
        self.frmParentPoi.setObjectName(u"frmParentPoi")
        self.frmParentPoi.setFrameShape(QFrame.StyledPanel)
        self.frmParentPoi.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frmParentPoi)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.cbParentPoi = QComboBox(self.frmParentPoi)
        self.cbParentPoi.setObjectName(u"cbParentPoi")

        self.gridLayout_4.addWidget(self.cbParentPoi, 0, 1, 1, 1)

        self.label_13 = QLabel(self.frmParentPoi)
        self.label_13.setObjectName(u"label_13")
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QSize(80, 0))
        self.label_13.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_4.addWidget(self.label_13, 0, 0, 1, 1)

        self.label_14 = QLabel(self.frmParentPoi)
        self.label_14.setObjectName(u"label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setMinimumSize(QSize(60, 0))
        self.label_14.setMaximumSize(QSize(60, 16777215))

        self.gridLayout_4.addWidget(self.label_14, 0, 2, 1, 1)


        self.verticalLayout.addWidget(self.frmParentPoi)

        self.frmMasterSlave = QFrame(Dialog)
        self.frmMasterSlave.setObjectName(u"frmMasterSlave")
        self.frmMasterSlave.setFrameShape(QFrame.StyledPanel)
        self.frmMasterSlave.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frmMasterSlave)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_6 = QLabel(self.frmMasterSlave)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(80, 0))
        self.label_6.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.cbMasterAxis = QComboBox(self.frmMasterSlave)
        self.cbMasterAxis.setObjectName(u"cbMasterAxis")

        self.gridLayout_2.addWidget(self.cbMasterAxis, 0, 1, 1, 1)

        self.label_5 = QLabel(self.frmMasterSlave)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(60, 0))
        self.label_5.setMaximumSize(QSize(60, 16777215))

        self.gridLayout_2.addWidget(self.label_5, 0, 2, 1, 1)

        self.label_8 = QLabel(self.frmMasterSlave)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(80, 0))
        self.label_8.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)

        self.cbSlaveAxis = QComboBox(self.frmMasterSlave)
        self.cbSlaveAxis.setObjectName(u"cbSlaveAxis")

        self.gridLayout_2.addWidget(self.cbSlaveAxis, 1, 1, 1, 1)

        self.label_7 = QLabel(self.frmMasterSlave)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QSize(60, 0))
        self.label_7.setMaximumSize(QSize(60, 16777215))

        self.gridLayout_2.addWidget(self.label_7, 1, 2, 1, 1)


        self.verticalLayout.addWidget(self.frmMasterSlave)

        self.frmPoints = QFrame(Dialog)
        self.frmPoints.setObjectName(u"frmPoints")
        self.frmPoints.setFrameShape(QFrame.StyledPanel)
        self.frmPoints.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frmPoints)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_10 = QLabel(self.frmPoints)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QSize(80, 0))
        self.label_10.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_3.addWidget(self.label_10, 0, 0, 1, 1)

        self.cbPoiA = QComboBox(self.frmPoints)
        self.cbPoiA.setObjectName(u"cbPoiA")

        self.gridLayout_3.addWidget(self.cbPoiA, 0, 1, 1, 1)

        self.label_9 = QLabel(self.frmPoints)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(60, 0))
        self.label_9.setMaximumSize(QSize(60, 16777215))

        self.gridLayout_3.addWidget(self.label_9, 0, 2, 1, 1)

        self.label_12 = QLabel(self.frmPoints)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QSize(80, 0))
        self.label_12.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_3.addWidget(self.label_12, 1, 0, 1, 1)

        self.cbPoiB = QComboBox(self.frmPoints)
        self.cbPoiB.setObjectName(u"cbPoiB")

        self.gridLayout_3.addWidget(self.cbPoiB, 1, 1, 1, 1)

        self.label_11 = QLabel(self.frmPoints)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QSize(60, 0))
        self.label_11.setMaximumSize(QSize(60, 16777215))

        self.gridLayout_3.addWidget(self.label_11, 1, 2, 1, 1)


        self.verticalLayout.addWidget(self.frmPoints)

        self.errPois = QLabel(Dialog)
        self.errPois.setObjectName(u"errPois")

        self.verticalLayout.addWidget(self.errPois)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(218, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnOk = QPushButton(self.frame)
        self.btnOk.setObjectName(u"btnOk")
        self.btnOk.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.btnOk)

        self.buttonBox = QDialogButtonBox(self.frame)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Dialog)

        self.btnOk.setDefault(True)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"New Node", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Name", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"[unique]", None))
        self.errUniqueName.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:600; color:#aa0000;\">Pick a unique name !</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Parent", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"[Frame]", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Parent", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"[point]", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Main", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"[Frame]", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Secondary", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"[Frame]", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"point 1", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"[Point]", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"point 2", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"[Point]", None))
        self.errPois.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:600; color:#aa0000;\">Select two distinct nodes</span></p></body></html>", None))
        self.btnOk.setText(QCoreApplication.translate("Dialog", u"  Ok  ", None))
    # retranslateUi

