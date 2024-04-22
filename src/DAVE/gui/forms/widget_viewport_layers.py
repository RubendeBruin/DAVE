# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_viewport_layers.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSlider,
    QSpinBox, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(336, 412)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Widget.sizePolicy().hasHeightForWidth())
        Widget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)

        self.label_6 = QLabel(Widget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 8, 2, 1, 1)

        self.padBottom = QSpinBox(Widget)
        self.padBottom.setObjectName(u"padBottom")

        self.gridLayout.addWidget(self.padBottom, 7, 3, 1, 1)

        self.padTop = QSpinBox(Widget)
        self.padTop.setObjectName(u"padTop")

        self.gridLayout.addWidget(self.padTop, 7, 1, 1, 1)

        self.label_5 = QLabel(Widget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 6, 2, 1, 1)

        self.pbBorderOpacity = QSpinBox(Widget)
        self.pbBorderOpacity.setObjectName(u"pbBorderOpacity")
        self.pbBorderOpacity.setMaximum(255)

        self.gridLayout.addWidget(self.pbBorderOpacity, 6, 3, 1, 1)

        self.pbBorderColor = QPushButton(Widget)
        self.pbBorderColor.setObjectName(u"pbBorderColor")

        self.gridLayout.addWidget(self.pbBorderColor, 6, 1, 1, 1)

        self.sbBackgroundOpacity = QSpinBox(Widget)
        self.sbBackgroundOpacity.setObjectName(u"sbBackgroundOpacity")
        self.sbBackgroundOpacity.setMaximum(255)

        self.gridLayout.addWidget(self.sbBackgroundOpacity, 8, 3, 1, 1)

        self.sbBorderWidth = QSpinBox(Widget)
        self.sbBorderWidth.setObjectName(u"sbBorderWidth")

        self.gridLayout.addWidget(self.sbBorderWidth, 5, 1, 1, 1)

        self.label_7 = QLabel(Widget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 1)

        self.pbBackgroundColor = QPushButton(Widget)
        self.pbBackgroundColor.setObjectName(u"pbBackgroundColor")

        self.gridLayout.addWidget(self.pbBackgroundColor, 8, 1, 1, 1)

        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.padLeft = QSpinBox(Widget)
        self.padLeft.setObjectName(u"padLeft")

        self.gridLayout.addWidget(self.padLeft, 7, 4, 1, 1)

        self.label_4 = QLabel(Widget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)

        self.padRight = QSpinBox(Widget)
        self.padRight.setObjectName(u"padRight")

        self.gridLayout.addWidget(self.padRight, 7, 2, 1, 1)

        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)

        self.label_9 = QLabel(Widget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 1, 0, 1, 1)

        self.layerList = QListWidget(Widget)
        self.layerList.setObjectName(u"layerList")

        self.gridLayout.addWidget(self.layerList, 3, 0, 1, 5)

        self.fontSize = QSlider(Widget)
        self.fontSize.setObjectName(u"fontSize")
        self.fontSize.setMinimum(5)
        self.fontSize.setMaximum(120)
        self.fontSize.setValue(16)
        self.fontSize.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.fontSize, 4, 1, 1, 4)

        QWidget.setTabOrder(self.layerList, self.fontSize)
        QWidget.setTabOrder(self.fontSize, self.sbBorderWidth)
        QWidget.setTabOrder(self.sbBorderWidth, self.pbBorderColor)
        QWidget.setTabOrder(self.pbBorderColor, self.pbBorderOpacity)
        QWidget.setTabOrder(self.pbBorderOpacity, self.padTop)
        QWidget.setTabOrder(self.padTop, self.padRight)
        QWidget.setTabOrder(self.padRight, self.padBottom)
        QWidget.setTabOrder(self.padBottom, self.padLeft)
        QWidget.setTabOrder(self.padLeft, self.pbBackgroundColor)
        QWidget.setTabOrder(self.pbBackgroundColor, self.sbBackgroundOpacity)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Border width", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"opacity", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"opacity", None))
        self.pbBorderColor.setText("")
        self.label_7.setText(QCoreApplication.translate("Widget", u"Background color", None))
        self.pbBackgroundColor.setText("")
        self.label_3.setText(QCoreApplication.translate("Widget", u"Padding (TRBL)", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Border color", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Font size", None))
        self.label_9.setText(QCoreApplication.translate("Widget", u"Visible layers:", None))
    # retranslateUi

