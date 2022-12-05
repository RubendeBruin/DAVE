# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_edit_watch.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_DialigEditWatch(object):
    def setupUi(self, DialigEditWatch):
        if not DialigEditWatch.objectName():
            DialigEditWatch.setObjectName(u"DialigEditWatch")
        DialigEditWatch.resize(521, 277)
        DialigEditWatch.setWindowOpacity(1.000000000000000)
        DialigEditWatch.setSizeGripEnabled(True)
        self.gridLayout = QGridLayout(DialigEditWatch)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_10 = QLabel(DialigEditWatch)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setStyleSheet(u"background-color: rgb(227, 227, 227);")

        self.gridLayout.addWidget(self.label_10, 3, 1, 1, 1)

        self.label_9 = QLabel(DialigEditWatch)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 6, 2, 1, 1)

        self.label_4 = QLabel(DialigEditWatch)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.label_4, 1, 2, 5, 1)

        self.label_5 = QLabel(DialigEditWatch)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)

        self.label = QLabel(DialigEditWatch)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(DialigEditWatch)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_3 = QLabel(DialigEditWatch)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)

        self.lblEvaluationResult = QLabel(DialigEditWatch)
        self.lblEvaluationResult.setObjectName(u"lblEvaluationResult")
        self.lblEvaluationResult.setStyleSheet(u"color: rgb(32, 84, 56);")
        self.lblEvaluationResult.setWordWrap(True)

        self.gridLayout.addWidget(self.lblEvaluationResult, 2, 1, 1, 1)

        self.tbCondition = QLineEdit(DialigEditWatch)
        self.tbCondition.setObjectName(u"tbCondition")
        self.tbCondition.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.tbCondition, 6, 1, 1, 1)

        self.label_11 = QLabel(DialigEditWatch)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"background-color: rgb(227, 227, 227);")

        self.gridLayout.addWidget(self.label_11, 8, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(DialigEditWatch)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 11, 0, 1, 2)

        self.tbName = QLineEdit(DialigEditWatch)
        self.tbName.setObjectName(u"tbName")

        self.gridLayout.addWidget(self.tbName, 0, 1, 1, 1)

        self.label_8 = QLabel(DialigEditWatch)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 5, 0, 1, 1)

        self.sbDecimals = QSpinBox(DialigEditWatch)
        self.sbDecimals.setObjectName(u"sbDecimals")

        self.gridLayout.addWidget(self.sbDecimals, 5, 1, 1, 1)

        self.lblConditionResult = QLabel(DialigEditWatch)
        self.lblConditionResult.setObjectName(u"lblConditionResult")
        self.lblConditionResult.setStyleSheet(u"color: rgb(32, 84, 56);")
        self.lblConditionResult.setWordWrap(True)

        self.gridLayout.addWidget(self.lblConditionResult, 7, 1, 1, 1)

        self.tbEvaluate = QLineEdit(DialigEditWatch)
        self.tbEvaluate.setObjectName(u"tbEvaluate")

        self.gridLayout.addWidget(self.tbEvaluate, 1, 1, 1, 1)

        QWidget.setTabOrder(self.tbName, self.tbEvaluate)
        QWidget.setTabOrder(self.tbEvaluate, self.sbDecimals)
        QWidget.setTabOrder(self.sbDecimals, self.tbCondition)

        self.retranslateUi(DialigEditWatch)
        self.buttonBox.accepted.connect(DialigEditWatch.accept)
        self.buttonBox.rejected.connect(DialigEditWatch.reject)

        QMetaObject.connectSlotsByName(DialigEditWatch)
    # setupUi

    def retranslateUi(self, DialigEditWatch):
        DialigEditWatch.setWindowTitle(QCoreApplication.translate("DialigEditWatch", u"Dialog", None))
        self.label_10.setText(QCoreApplication.translate("DialigEditWatch", u"Examples:\n"
" self.gx\n"
" self.heel\n"
" np.linalg.norm((self.tilt_x, self.tilt_y))\n"
" self.fx / s.g", None))
        self.label_9.setText(QCoreApplication.translate("DialigEditWatch", u"evaluation result available as 'value'", None))
        self.label_4.setText(QCoreApplication.translate("DialigEditWatch", u"node = self\n"
"scene = s\n"
"numpy=np", None))
        self.label_5.setText(QCoreApplication.translate("DialigEditWatch", u"Do not use \\ or '", None))
        self.label.setText(QCoreApplication.translate("DialigEditWatch", u"Watch name", None))
        self.label_2.setText(QCoreApplication.translate("DialigEditWatch", u"Evaluate", None))
        self.label_3.setText(QCoreApplication.translate("DialigEditWatch", u"Show only when", None))
        self.lblEvaluationResult.setText(QCoreApplication.translate("DialigEditWatch", u"TextLabel", None))
        self.label_11.setText(QCoreApplication.translate("DialigEditWatch", u"Example: abs(value) > 2", None))
        self.label_8.setText(QCoreApplication.translate("DialigEditWatch", u"Decimals", None))
        self.lblConditionResult.setText(QCoreApplication.translate("DialigEditWatch", u"TextLabel", None))
    # retranslateUi

