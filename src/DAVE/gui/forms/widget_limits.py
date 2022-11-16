# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_limits.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_DockLimits(object):
    def setupUi(self, DockLimits):
        if not DockLimits.objectName():
            DockLimits.setObjectName(u"DockLimits")
        DockLimits.resize(412, 655)
        self.verticalLayout = QVBoxLayout(DockLimits)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(DockLimits)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(400, 0))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lbNodeClass = QLabel(self.widget)
        self.lbNodeClass.setObjectName(u"lbNodeClass")

        self.gridLayout.addWidget(self.lbNodeClass, 2, 1, 1, 1)

        self.cbNode = QComboBox(self.widget)
        self.cbNode.setObjectName(u"cbNode")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbNode.sizePolicy().hasHeightForWidth())
        self.cbNode.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.cbNode, 1, 1, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.lblError = QLabel(self.widget)
        self.lblError.setObjectName(u"lblError")
        self.lblError.setStyleSheet(u"background: yellow; \n"
"color: rgb(255, 0, 0);")

        self.gridLayout.addWidget(self.lblError, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.widget)

        self.widgetLimitEdit = QWidget(DockLimits)
        self.widgetLimitEdit.setObjectName(u"widgetLimitEdit")
        self.gridLayout_2 = QGridLayout(self.widgetLimitEdit)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(self.widgetLimitEdit)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.cbProperty = QComboBox(self.widgetLimitEdit)
        self.cbProperty.setObjectName(u"cbProperty")

        self.gridLayout_2.addWidget(self.cbProperty, 0, 1, 1, 1)

        self.lbPropHelp = QLabel(self.widgetLimitEdit)
        self.lbPropHelp.setObjectName(u"lbPropHelp")
        self.lbPropHelp.setToolTipDuration(0)
        self.lbPropHelp.setWordWrap(True)

        self.gridLayout_2.addWidget(self.lbPropHelp, 1, 1, 1, 1)

        self.label_4 = QLabel(self.widgetLimitEdit)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)

        self.lineEdit = QLineEdit(self.widgetLimitEdit)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setToolTipDuration(-1)
        self.lineEdit.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.lineEdit, 2, 1, 1, 1)

        self.lbResult = QLabel(self.widgetLimitEdit)
        self.lbResult.setObjectName(u"lbResult")
        self.lbResult.setWordWrap(True)

        self.gridLayout_2.addWidget(self.lbResult, 3, 1, 1, 1)

        self.widget_2 = QWidget(self.widgetLimitEdit)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.pbApply = QPushButton(self.widget_2)
        self.pbApply.setObjectName(u"pbApply")

        self.horizontalLayout.addWidget(self.pbApply)

        self.pbRemove = QPushButton(self.widget_2)
        self.pbRemove.setObjectName(u"pbRemove")

        self.horizontalLayout.addWidget(self.pbRemove)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_2.addWidget(self.widget_2, 4, 1, 1, 1)


        self.verticalLayout.addWidget(self.widgetLimitEdit)

        self.label_5 = QLabel(DockLimits)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.table = QTableWidget(DockLimits)
        self.table.setObjectName(u"table")
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.verticalLayout.addWidget(self.table)


        self.retranslateUi(DockLimits)

        QMetaObject.connectSlotsByName(DockLimits)
    # setupUi

    def retranslateUi(self, DockLimits):
        DockLimits.setWindowTitle(QCoreApplication.translate("DockLimits", u"Form", None))
        self.lbNodeClass.setText(QCoreApplication.translate("DockLimits", u"node_class", None))
        self.label.setText(QCoreApplication.translate("DockLimits", u"Node", None))
        self.lblError.setText(QCoreApplication.translate("DockLimits", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("DockLimits", u"Property", None))
        self.lbPropHelp.setText(QCoreApplication.translate("DockLimits", u"hoover here for property help", None))
        self.label_4.setText(QCoreApplication.translate("DockLimits", u"Limit", None))
#if QT_CONFIG(tooltip)
        self.lineEdit.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lineEdit.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.lineEdit.setPlaceholderText("")
        self.lbResult.setText(QCoreApplication.translate("DockLimits", u"[UC]", None))
        self.pbApply.setText(QCoreApplication.translate("DockLimits", u"Apply", None))
        self.pbRemove.setText(QCoreApplication.translate("DockLimits", u"Remove", None))
        self.label_5.setText(QCoreApplication.translate("DockLimits", u"Defined limits:", None))
    # retranslateUi

