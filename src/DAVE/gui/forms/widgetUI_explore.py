# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_explore.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

class Ui_widgetExplore11(object):
    def setupUi(self, widgetExplore11):
        if not widgetExplore11.objectName():
            widgetExplore11.setObjectName(u"widgetExplore11")
        widgetExplore11.resize(593, 576)
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
        self.editResult.setReadOnly(True)

        self.gridLayout.addWidget(self.editResult, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.widget)

        self.groupBox = QGroupBox(widgetExplore11)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.editTarget = QDoubleSpinBox(self.groupBox)
        self.editTarget.setObjectName(u"editTarget")
        self.editTarget.setDecimals(3)
        self.editTarget.setMinimum(-100000000000000000.000000000000000)
        self.editTarget.setMaximum(99999999999999991611392.000000000000000)

        self.gridLayout_3.addWidget(self.editTarget, 0, 1, 1, 1)

        self.btnGoalSeek = QPushButton(self.groupBox)
        self.btnGoalSeek.setObjectName(u"btnGoalSeek")

        self.gridLayout_3.addWidget(self.btnGoalSeek, 0, 0, 1, 1)

        self.wigetHistory = QWidget(self.groupBox)
        self.wigetHistory.setObjectName(u"wigetHistory")

        self.gridLayout_3.addWidget(self.wigetHistory, 3, 0, 1, 2)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(widgetExplore11)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)

        self.editFrom = QDoubleSpinBox(self.groupBox_2)
        self.editFrom.setObjectName(u"editFrom")
        self.editFrom.setDecimals(3)
        self.editFrom.setMinimum(-100000000000000000.000000000000000)
        self.editFrom.setMaximum(99999999999999991611392.000000000000000)

        self.gridLayout_2.addWidget(self.editFrom, 0, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)

        self.editTo = QDoubleSpinBox(self.groupBox_2)
        self.editTo.setObjectName(u"editTo")
        self.editTo.setDecimals(3)
        self.editTo.setMinimum(-100000000000000000.000000000000000)
        self.editTo.setMaximum(99999999999999991611392.000000000000000)
        self.editTo.setValue(20.000000000000000)

        self.gridLayout_2.addWidget(self.editTo, 1, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)

        self.editSteps = QSpinBox(self.groupBox_2)
        self.editSteps.setObjectName(u"editSteps")
        self.editSteps.setMaximum(100)
        self.editSteps.setValue(10)

        self.gridLayout_2.addWidget(self.editSteps, 2, 1, 1, 1)

        self.btnGraph = QPushButton(self.groupBox_2)
        self.btnGraph.setObjectName(u"btnGraph")

        self.gridLayout_2.addWidget(self.btnGraph, 3, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        QWidget.setTabOrder(self.editSet, self.editEvaluate)
        QWidget.setTabOrder(self.editEvaluate, self.editResult)

        self.retranslateUi(widgetExplore11)

        QMetaObject.connectSlotsByName(widgetExplore11)
    # setupUi

    def retranslateUi(self, widgetExplore11):
        widgetExplore11.setWindowTitle(QCoreApplication.translate("widgetExplore11", u"Form", None))
        self.label.setText(QCoreApplication.translate("widgetExplore11", u"<html><head/><body><p>Plotting or goal-seek</p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("widgetExplore11", u"Current value", None))
        self.label_2.setText(QCoreApplication.translate("widgetExplore11", u"Adjust:", None))
        self.editSet.setPlaceholderText(QCoreApplication.translate("widgetExplore11", u"(Hint, drag from \"derived properties (the looking glass) and drop here.", None))
        self.label_3.setText(QCoreApplication.translate("widgetExplore11", u"Find:", None))
        self.editEvaluate.setPlaceholderText(QCoreApplication.translate("widgetExplore11", u"(Hint, drag from \"derived properties (the looking glass) and drop here.", None))
        self.editResult.setPlaceholderText(QCoreApplication.translate("widgetExplore11", u"The result of \"Find\" will appear here", None))
        self.groupBox.setTitle(QCoreApplication.translate("widgetExplore11", u"Goal-seek", None))
        self.btnGoalSeek.setText(QCoreApplication.translate("widgetExplore11", u"Goal-seek (find) to", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("widgetExplore11", u"Graph", None))
        self.label_4.setText(QCoreApplication.translate("widgetExplore11", u"From value", None))
        self.label_5.setText(QCoreApplication.translate("widgetExplore11", u"To value", None))
        self.label_6.setText(QCoreApplication.translate("widgetExplore11", u"number of steps", None))
        self.btnGraph.setText(QCoreApplication.translate("widgetExplore11", u"produce graph", None))
    # retranslateUi

