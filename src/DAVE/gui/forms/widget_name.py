# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_name.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_NameWidget(object):
    def setupUi(self, NameWidget):
        if not NameWidget.objectName():
            NameWidget.setObjectName(u"NameWidget")
        NameWidget.resize(599, 95)
        NameWidget.setMinimumSize(QSize(0, 0))
        self.gridLayout_2 = QGridLayout(NameWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pbEditAll = QPushButton(NameWidget)
        self.pbEditAll.setObjectName(u"pbEditAll")
        font = QFont()
        font.setBold(True)
        font.setUnderline(True)
        self.pbEditAll.setFont(font)
        self.pbEditAll.setStyleSheet(u"color: rgb(85, 170, 255);")
        self.pbEditAll.setFlat(True)

        self.gridLayout_2.addWidget(self.pbEditAll, 0, 0, 1, 1)

        self.widget = QWidget(NameWidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.cbVisible = QCheckBox(self.widget)
        self.cbVisible.setObjectName(u"cbVisible")

        self.gridLayout.addWidget(self.cbVisible, 1, 1, 1, 1)

        self.label2 = QLabel(self.widget)
        self.label2.setObjectName(u"label2")
        self.label2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label2, 1, 2, 1, 1)

        self.lbColor = QLabel(self.widget)
        self.lbColor.setObjectName(u"lbColor")
        self.lbColor.setStyleSheet(u"background-color: rgb(255, 170, 0);")
        self.lbColor.setFrameShape(QFrame.NoFrame)

        self.gridLayout.addWidget(self.lbColor, 1, 3, 1, 1)

        self.tbName = QLineEdit(self.widget)
        self.tbName.setObjectName(u"tbName")

        self.gridLayout.addWidget(self.tbName, 0, 1, 1, 3)


        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.retranslateUi(NameWidget)

        QMetaObject.connectSlotsByName(NameWidget)
    # setupUi

    def retranslateUi(self, NameWidget):
        NameWidget.setWindowTitle(QCoreApplication.translate("NameWidget", u"Form", None))
        self.pbEditAll.setText(QCoreApplication.translate("NameWidget", u"Edit all", None))
        self.label.setText(QCoreApplication.translate("NameWidget", u"Name [unique]", None))
        self.cbVisible.setText(QCoreApplication.translate("NameWidget", u"Visual visible", None))
        self.label2.setText(QCoreApplication.translate("NameWidget", u"Color:", None))
#if QT_CONFIG(tooltip)
        self.lbColor.setToolTip(QCoreApplication.translate("NameWidget", u"click to change, right-click to reset", None))
#endif // QT_CONFIG(tooltip)
        self.lbColor.setText(QCoreApplication.translate("NameWidget", u"default", None))
    # retranslateUi

