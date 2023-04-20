# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_shackle.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QSizePolicy, QWidget)

class Ui_widgetShackle(object):
    def setupUi(self, widgetShackle):
        if not widgetShackle.objectName():
            widgetShackle.setObjectName(u"widgetShackle")
        widgetShackle.resize(400, 57)
        self.gridLayout = QGridLayout(widgetShackle)
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBox = QComboBox(widgetShackle)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)

        self.label = QLabel(widgetShackle)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.lbInfo = QLabel(widgetShackle)
        self.lbInfo.setObjectName(u"lbInfo")

        self.gridLayout.addWidget(self.lbInfo, 2, 0, 1, 2)


        self.retranslateUi(widgetShackle)

        QMetaObject.connectSlotsByName(widgetShackle)
    # setupUi

    def retranslateUi(self, widgetShackle):
        widgetShackle.setWindowTitle(QCoreApplication.translate("widgetShackle", u"Form", None))
        self.label.setText(QCoreApplication.translate("widgetShackle", u"Shackle type:", None))
        self.lbInfo.setText(QCoreApplication.translate("widgetShackle", u"Info about selected shackle", None))
    # retranslateUi

