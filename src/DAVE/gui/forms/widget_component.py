# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_component.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

from DAVE.gui.helpers.resource_selector import QResourceSelector

class Ui_component(object):
    def setupUi(self, component):
        if not component.objectName():
            component.setObjectName(u"component")
        component.resize(326, 72)
        component.setStyleSheet(u"")
        self.formLayout = QFormLayout(component)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(component)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.resource_selector = QResourceSelector(component)
        self.resource_selector.setObjectName(u"resource_selector")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.resource_selector)

        self.pbEditExposedProperties = QPushButton(component)
        self.pbEditExposedProperties.setObjectName(u"pbEditExposedProperties")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.pbEditExposedProperties)


        self.retranslateUi(component)

        QMetaObject.connectSlotsByName(component)
    # setupUi

    def retranslateUi(self, component):
        component.setWindowTitle(QCoreApplication.translate("component", u"Form", None))
        self.label.setText(QCoreApplication.translate("component", u"File:", None))
        self.pbEditExposedProperties.setText(QCoreApplication.translate("component", u"Edit exposed properties", None))
    # retranslateUi

