# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_connections.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

from DAVE.gui.helpers.qnodepicker import QNodePicker

class Ui_ConnectionForm(object):
    def setupUi(self, ConnectionForm):
        if not ConnectionForm.objectName():
            ConnectionForm.setObjectName(u"ConnectionForm")
        ConnectionForm.resize(500, 418)
        self.verticalLayout = QVBoxLayout(ConnectionForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(ConnectionForm)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)
        self.label_3.setIndent(-1)

        self.verticalLayout.addWidget(self.label_3)

        self.frame = QFrame(ConnectionForm)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pbSetShortestRoute = QPushButton(self.frame)
        self.pbSetShortestRoute.setObjectName(u"pbSetShortestRoute")

        self.gridLayout.addWidget(self.pbSetShortestRoute, 5, 3, 1, 1)

        self.widgetPicker = QNodePicker(self.frame)
        self.widgetPicker.setObjectName(u"widgetPicker")

        self.gridLayout.addWidget(self.widgetPicker, 11, 2, 1, 2)

        self.pbRemoveSelected = QPushButton(self.frame)
        self.pbRemoveSelected.setObjectName(u"pbRemoveSelected")

        self.gridLayout.addWidget(self.pbRemoveSelected, 4, 3, 1, 1)

        self.cbGeometryTweaking = QCheckBox(self.frame)
        self.cbGeometryTweaking.setObjectName(u"cbGeometryTweaking")

        self.gridLayout.addWidget(self.cbGeometryTweaking, 7, 2, 1, 2)

        self.lblError = QLabel(self.frame)
        self.lblError.setObjectName(u"lblError")
        self.lblError.setStyleSheet(u"background-color: rgb(255, 229, 255);")
        self.lblError.setFrameShape(QFrame.Box)
        self.lblError.setWordWrap(True)

        self.gridLayout.addWidget(self.lblError, 10, 1, 1, 3)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 11, 1, 1, 1)

        self.tree = QTreeWidget(self.frame)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree.setHeaderItem(__qtreewidgetitem)
        self.tree.setObjectName(u"tree")

        self.gridLayout.addWidget(self.tree, 9, 1, 1, 3)

        self.checkBox = QCheckBox(self.frame)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout.addWidget(self.checkBox, 7, 1, 1, 1)

        self.label_8 = QLabel(self.frame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setWordWrap(True)

        self.gridLayout.addWidget(self.label_8, 4, 1, 1, 2)

        self.pbPinLocations = QPushButton(self.frame)
        self.pbPinLocations.setObjectName(u"pbPinLocations")

        self.gridLayout.addWidget(self.pbPinLocations, 6, 3, 1, 1)

        self.lbDirection = QLabel(self.frame)
        self.lbDirection.setObjectName(u"lbDirection")
        self.lbDirection.setWordWrap(True)

        self.gridLayout.addWidget(self.lbDirection, 5, 1, 2, 2)


        self.verticalLayout.addWidget(self.frame)

        QWidget.setTabOrder(self.pbRemoveSelected, self.pbSetShortestRoute)
        QWidget.setTabOrder(self.pbSetShortestRoute, self.pbPinLocations)
        QWidget.setTabOrder(self.pbPinLocations, self.checkBox)
        QWidget.setTabOrder(self.checkBox, self.cbGeometryTweaking)
        QWidget.setTabOrder(self.cbGeometryTweaking, self.tree)
        QWidget.setTabOrder(self.tree, self.pushButton)

        self.retranslateUi(ConnectionForm)

        QMetaObject.connectSlotsByName(ConnectionForm)
    # setupUi

    def retranslateUi(self, ConnectionForm):
        ConnectionForm.setWindowTitle(QCoreApplication.translate("ConnectionForm", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("ConnectionForm", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Connections (Points/Circles)</span></p></body></html>", None))
        self.pbSetShortestRoute.setText(QCoreApplication.translate("ConnectionForm", u"Set to shortest route", None))
        self.pbRemoveSelected.setText(QCoreApplication.translate("ConnectionForm", u"Remove selected connection", None))
        self.cbGeometryTweaking.setText(QCoreApplication.translate("ConnectionForm", u"Show geometry tweaking options", None))
        self.lblError.setText(QCoreApplication.translate("ConnectionForm", u"Error if any", None))
        self.pushButton.setText(QCoreApplication.translate("ConnectionForm", u"Add", None))
        self.checkBox.setText(QCoreApplication.translate("ConnectionForm", u"Show Friction options", None))
        self.label_8.setText(QCoreApplication.translate("ConnectionForm", u"Drag/drop items to change order, add or remove.", None))
        self.pbPinLocations.setText(QCoreApplication.translate("ConnectionForm", u"Set Pin Locations", None))
        self.lbDirection.setText(QCoreApplication.translate("ConnectionForm", u"For circles the direction in which the cable runs over it is defined by the axis of the circle. Check the box below \u2b6e/\u2b6f to run over the circle in opposite direction.", None))
    # retranslateUi

