# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_node_prop_select.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QFrame, QLabel, QListWidget,
    QListWidgetItem, QPlainTextEdit, QSizePolicy, QSplitter,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(884, 442)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: bold;")

        self.verticalLayout_2.addWidget(self.label)

        self.lwNodes = QListWidget(self.widget)
        self.lwNodes.setObjectName(u"lwNodes")
        self.lwNodes.setFrameShape(QFrame.StyledPanel)
        self.lwNodes.setFrameShadow(QFrame.Plain)
        self.lwNodes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lwNodes.setSortingEnabled(True)

        self.verticalLayout_2.addWidget(self.lwNodes)

        self.splitter.addWidget(self.widget)
        self.widget_2 = QWidget(self.splitter)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font: bold;")

        self.verticalLayout_3.addWidget(self.label_2)

        self.lwProperties = QListWidget(self.widget_2)
        self.lwProperties.setObjectName(u"lwProperties")
        self.lwProperties.setFrameShape(QFrame.StyledPanel)
        self.lwProperties.setFrameShadow(QFrame.Plain)
        self.lwProperties.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lwProperties.setSortingEnabled(True)

        self.verticalLayout_3.addWidget(self.lwProperties)

        self.splitter.addWidget(self.widget_2)
        self.widget_3 = QWidget(self.splitter)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_4 = QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.lbName = QLabel(self.widget_3)
        self.lbName.setObjectName(u"lbName")
        self.lbName.setStyleSheet(u"font: bold;")

        self.verticalLayout_4.addWidget(self.lbName)

        self.lbSelectedNode = QLabel(self.widget_3)
        self.lbSelectedNode.setObjectName(u"lbSelectedNode")

        self.verticalLayout_4.addWidget(self.lbSelectedNode)

        self.lbSelectedProperty = QLabel(self.widget_3)
        self.lbSelectedProperty.setObjectName(u"lbSelectedProperty")

        self.verticalLayout_4.addWidget(self.lbSelectedProperty)

        self.lbValue = QLabel(self.widget_3)
        self.lbValue.setObjectName(u"lbValue")

        self.verticalLayout_4.addWidget(self.lbValue)

        self.ptDoc = QPlainTextEdit(self.widget_3)
        self.ptDoc.setObjectName(u"ptDoc")
        self.ptDoc.setFrameShape(QFrame.NoFrame)
        self.ptDoc.setFrameShadow(QFrame.Plain)
        self.ptDoc.setReadOnly(True)

        self.verticalLayout_4.addWidget(self.ptDoc)

        self.splitter.addWidget(self.widget_3)

        self.verticalLayout.addWidget(self.splitter)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.lwNodes, self.lwProperties)
        QWidget.setTabOrder(self.lwProperties, self.ptDoc)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Select property", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Node", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Property", None))
        self.lbName.setText(QCoreApplication.translate("Dialog", u"Selected", None))
        self.lbSelectedNode.setText(QCoreApplication.translate("Dialog", u"Select node", None))
        self.lbSelectedProperty.setText(QCoreApplication.translate("Dialog", u"Select property", None))
        self.lbValue.setText(QCoreApplication.translate("Dialog", u"Value", None))
    # retranslateUi

