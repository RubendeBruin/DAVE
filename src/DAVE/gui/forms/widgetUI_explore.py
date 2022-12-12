# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_explore.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_widgetExplore11(object):
    def setupUi(self, widgetExplore11):
        if not widgetExplore11.objectName():
            widgetExplore11.setObjectName(u"widgetExplore11")
        widgetExplore11.resize(593, 1102)
        widgetExplore11.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widgetExplore11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(widgetExplore11)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.widget = QWidget(widgetExplore11)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.editSet = QLineEdit(self.widget)
        self.editSet.setObjectName(u"editSet")

        self.gridLayout.addWidget(self.editSet, 0, 1, 1, 1)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.editEvaluate = QPlainTextEdit(self.widget)
        self.editEvaluate.setObjectName(u"editEvaluate")
        self.editEvaluate.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        self.gridLayout.addWidget(self.editEvaluate, 1, 1, 1, 1)

        self.editResult = QPlainTextEdit(self.widget)
        self.editResult.setObjectName(u"editResult")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editResult.sizePolicy().hasHeightForWidth())
        self.editResult.setSizePolicy(sizePolicy)
        self.editResult.setMaximumSize(QSize(16777215, 40))

        self.gridLayout.addWidget(self.editResult, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.widget)

        self.toolBox = QToolBox(widgetExplore11)
        self.toolBox.setObjectName(u"toolBox")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 567, 416))
        self.formLayout = QFormLayout(self.page)
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(self.page)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.editFrom = QDoubleSpinBox(self.page)
        self.editFrom.setObjectName(u"editFrom")
        self.editFrom.setDecimals(3)
        self.editFrom.setMinimum(-100000000000000000.000000000000000)
        self.editFrom.setMaximum(99999999999999991611392.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.editFrom)

        self.label_5 = QLabel(self.page)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.editTo = QDoubleSpinBox(self.page)
        self.editTo.setObjectName(u"editTo")
        self.editTo.setDecimals(3)
        self.editTo.setMinimum(-100000000000000000.000000000000000)
        self.editTo.setMaximum(99999999999999991611392.000000000000000)
        self.editTo.setValue(20.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.editTo)

        self.label_6 = QLabel(self.page)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.editSteps = QSpinBox(self.page)
        self.editSteps.setObjectName(u"editSteps")
        self.editSteps.setMaximum(100)
        self.editSteps.setValue(10)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.editSteps)

        self.btnGraph = QPushButton(self.page)
        self.btnGraph.setObjectName(u"btnGraph")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.btnGraph)

        self.toolBox.addItem(self.page, u"Graph")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 567, 401))
        self.formLayout_2 = QFormLayout(self.page_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_7 = QLabel(self.page_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_7)

        self.editTarget = QDoubleSpinBox(self.page_2)
        self.editTarget.setObjectName(u"editTarget")
        self.editTarget.setDecimals(3)
        self.editTarget.setMinimum(-100000000000000000.000000000000000)
        self.editTarget.setMaximum(99999999999999991611392.000000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.editTarget)

        self.btnGoalSeek = QPushButton(self.page_2)
        self.btnGoalSeek.setObjectName(u"btnGoalSeek")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.btnGoalSeek)

        self.toolBox.addItem(self.page_2, u"Goal-seek")

        self.verticalLayout.addWidget(self.toolBox)

        QWidget.setTabOrder(self.editSet, self.editEvaluate)
        QWidget.setTabOrder(self.editEvaluate, self.editFrom)
        QWidget.setTabOrder(self.editFrom, self.editTo)
        QWidget.setTabOrder(self.editTo, self.editSteps)
        QWidget.setTabOrder(self.editSteps, self.btnGraph)
        QWidget.setTabOrder(self.btnGraph, self.editTarget)
        QWidget.setTabOrder(self.editTarget, self.btnGoalSeek)
        QWidget.setTabOrder(self.btnGoalSeek, self.editResult)

        self.retranslateUi(widgetExplore11)

        self.toolBox.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(widgetExplore11)
    # setupUi

    def retranslateUi(self, widgetExplore11):
        widgetExplore11.setWindowTitle(QCoreApplication.translate("widgetExplore11", u"Form", None))
        self.label.setText(QCoreApplication.translate("widgetExplore11", u"<html><head/><body><p><span style=\" text-decoration: underline;\">Explore or solve 1-to-1 relations</span></p><p>Set any settable scalar property in the scene, for example s['cable'].length</p><p>Solve statics</p><p>Evaluate another property of the scene (scalar) or python expression</p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("widgetExplore11", u"Evaluation result", None))
        self.label_2.setText(QCoreApplication.translate("widgetExplore11", u"Set", None))
        self.editSet.setPlaceholderText(QCoreApplication.translate("widgetExplore11", u" (Hint, drag and drop this from the \"derived properties\" widget).", None))
        self.label_3.setText(QCoreApplication.translate("widgetExplore11", u"Evaluate", None))
        self.editEvaluate.setPlaceholderText(QCoreApplication.translate("widgetExplore11", u"(Hint, drag and drop this from the \"derived properties\" widget).", None))
        self.editResult.setPlaceholderText(QCoreApplication.translate("widgetExplore11", u"The result of the evaluation will appear here", None))
        self.label_4.setText(QCoreApplication.translate("widgetExplore11", u"From value", None))
        self.label_5.setText(QCoreApplication.translate("widgetExplore11", u"To value", None))
        self.label_6.setText(QCoreApplication.translate("widgetExplore11", u"number of steps", None))
        self.btnGraph.setText(QCoreApplication.translate("widgetExplore11", u"produce graph", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QCoreApplication.translate("widgetExplore11", u"Graph", None))
        self.label_7.setText(QCoreApplication.translate("widgetExplore11", u"Target value:", None))
        self.btnGoalSeek.setText(QCoreApplication.translate("widgetExplore11", u"Goal-seek", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("widgetExplore11", u"Goal-seek", None))
    # retranslateUi

