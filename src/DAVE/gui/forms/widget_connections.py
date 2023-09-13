# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_connections.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

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
        self.pbRemoveSelected = QPushButton(self.frame)
        self.pbRemoveSelected.setObjectName(u"pbRemoveSelected")

        self.gridLayout.addWidget(self.pbRemoveSelected, 4, 3, 1, 1)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 8, 1, 1, 1)

        self.list = QListWidget(self.frame)
        self.list.setObjectName(u"list")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list.sizePolicy().hasHeightForWidth())
        self.list.setSizePolicy(sizePolicy)
        self.list.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.list, 6, 1, 1, 3)

        self.pbSetShortestRoute = QPushButton(self.frame)
        self.pbSetShortestRoute.setObjectName(u"pbSetShortestRoute")

        self.gridLayout.addWidget(self.pbSetShortestRoute, 5, 3, 1, 1)

        self.label_8 = QLabel(self.frame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setWordWrap(True)

        self.gridLayout.addWidget(self.label_8, 4, 1, 1, 2)

        self.lbDirection = QLabel(self.frame)
        self.lbDirection.setObjectName(u"lbDirection")
        self.lbDirection.setWordWrap(True)

        self.gridLayout.addWidget(self.lbDirection, 5, 1, 1, 2)

        self.widgetPicker = QNodePicker(self.frame)
        self.widgetPicker.setObjectName(u"widgetPicker")

        self.gridLayout.addWidget(self.widgetPicker, 8, 2, 1, 2)


        self.verticalLayout.addWidget(self.frame)

        self.label = QLabel(ConnectionForm)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.pbAdvancedSettings = QPushButton(ConnectionForm)
        self.pbAdvancedSettings.setObjectName(u"pbAdvancedSettings")

        self.verticalLayout.addWidget(self.pbAdvancedSettings)

        QWidget.setTabOrder(self.pbRemoveSelected, self.pbSetShortestRoute)
        QWidget.setTabOrder(self.pbSetShortestRoute, self.list)
        QWidget.setTabOrder(self.list, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.pbAdvancedSettings)

        self.retranslateUi(ConnectionForm)

        QMetaObject.connectSlotsByName(ConnectionForm)
    # setupUi

    def retranslateUi(self, ConnectionForm):
        ConnectionForm.setWindowTitle(QCoreApplication.translate("ConnectionForm", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("ConnectionForm", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Connections (Points/Circles)</span></p></body></html>", None))
        self.pbRemoveSelected.setText(QCoreApplication.translate("ConnectionForm", u"Remove selected point", None))
        self.pushButton.setText(QCoreApplication.translate("ConnectionForm", u"Add", None))
        self.pbSetShortestRoute.setText(QCoreApplication.translate("ConnectionForm", u"Determine shortest route", None))
        self.label_8.setText(QCoreApplication.translate("ConnectionForm", u"Drag/drop items to change order, add or remove.", None))
        self.lbDirection.setText(QCoreApplication.translate("ConnectionForm", u"For circles the direction in which the cable runs over it is defined by the axis of the circle. Check the box to run over the circle in opposite direction.", None))
        self.label.setText(QCoreApplication.translate("ConnectionForm", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Friction and maximum winding angles</span></p></body></html>", None))
        self.pbAdvancedSettings.setText(QCoreApplication.translate("ConnectionForm", u"Open advanced settings", None))
    # retranslateUi

