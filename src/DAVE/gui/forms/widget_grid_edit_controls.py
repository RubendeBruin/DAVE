# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_grid_edit_controls.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QLabel,
    QRadioButton, QSizePolicy, QWidget)

class Ui_widgetGridEditControls(object):
    def setupUi(self, widgetGridEditControls):
        if not widgetGridEditControls.objectName():
            widgetGridEditControls.setObjectName(u"widgetGridEditControls")
        widgetGridEditControls.resize(569, 108)
        self.gridLayout = QGridLayout(widgetGridEditControls)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(widgetGridEditControls)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.rbAll = QRadioButton(widgetGridEditControls)
        self.rbAll.setObjectName(u"rbAll")
        self.rbAll.setChecked(True)

        self.gridLayout.addWidget(self.rbAll, 1, 1, 1, 1)

        self.cbSortByName = QCheckBox(widgetGridEditControls)
        self.cbSortByName.setObjectName(u"cbSortByName")
        self.cbSortByName.setChecked(True)

        self.gridLayout.addWidget(self.cbSortByName, 2, 0, 1, 3)

        self.rbCommon = QRadioButton(widgetGridEditControls)
        self.rbCommon.setObjectName(u"rbCommon")

        self.gridLayout.addWidget(self.rbCommon, 1, 2, 1, 1)

        self.label_3 = QLabel(widgetGridEditControls)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        QWidget.setTabOrder(self.rbAll, self.rbCommon)
        QWidget.setTabOrder(self.rbCommon, self.cbSortByName)

        self.retranslateUi(widgetGridEditControls)

        QMetaObject.connectSlotsByName(widgetGridEditControls)
    # setupUi

    def retranslateUi(self, widgetGridEditControls):
        widgetGridEditControls.setWindowTitle(QCoreApplication.translate("widgetGridEditControls", u"Form", None))
        self.label.setText(QCoreApplication.translate("widgetGridEditControls", u"Editing multiple nodes", None))
        self.rbAll.setText(QCoreApplication.translate("widgetGridEditControls", u"All", None))
        self.cbSortByName.setText(QCoreApplication.translate("widgetGridEditControls", u"Sort nodes by name", None))
        self.rbCommon.setText(QCoreApplication.translate("widgetGridEditControls", u"Common", None))
        self.label_3.setText(QCoreApplication.translate("widgetGridEditControls", u"Properties:", None))
    # retranslateUi

