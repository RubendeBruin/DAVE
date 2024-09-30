# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_missing_item.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_MissingItemDialog(object):
    def setupUi(self, MissingItemDialog):
        if not MissingItemDialog.objectName():
            MissingItemDialog.setObjectName(u"MissingItemDialog")
        MissingItemDialog.resize(672, 367)
        MissingItemDialog.setSizeGripEnabled(True)
        MissingItemDialog.setModal(True)
        self.gridLayout_2 = QGridLayout(MissingItemDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.cbReplacement = QComboBox(MissingItemDialog)
        self.cbReplacement.setObjectName(u"cbReplacement")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbReplacement.sizePolicy().hasHeightForWidth())
        self.cbReplacement.setSizePolicy(sizePolicy)
        self.cbReplacement.setEditable(True)

        self.gridLayout_2.addWidget(self.cbReplacement, 5, 0, 1, 1)

        self.lbItemName = QLabel(MissingItemDialog)
        self.lbItemName.setObjectName(u"lbItemName")
        font = QFont()
        font.setBold(True)
        self.lbItemName.setFont(font)
        self.lbItemName.setFrameShape(QFrame.NoFrame)
        self.lbItemName.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lbItemName, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 2, 0, 1, 1)

        self.label_2 = QLabel(MissingItemDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 4, 0, 1, 1)

        self.label = QLabel(MissingItemDialog)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.pbBrowse = QPushButton(MissingItemDialog)
        self.pbBrowse.setObjectName(u"pbBrowse")

        self.gridLayout_2.addWidget(self.pbBrowse, 5, 1, 1, 1)

        self.widget = QWidget(MissingItemDialog)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.cbAcceptAll = QCheckBox(self.widget)
        self.cbAcceptAll.setObjectName(u"cbAcceptAll")

        self.gridLayout.addWidget(self.cbAcceptAll, 0, 0, 1, 1)

        self.pbNo = QPushButton(self.widget)
        self.pbNo.setObjectName(u"pbNo")

        self.gridLayout.addWidget(self.pbNo, 1, 1, 1, 1)

        self.pbYes = QPushButton(self.widget)
        self.pbYes.setObjectName(u"pbYes")

        self.gridLayout.addWidget(self.pbYes, 1, 0, 1, 1)

        self.pbNever = QPushButton(self.widget)
        self.pbNever.setObjectName(u"pbNever")

        self.gridLayout.addWidget(self.pbNever, 1, 2, 1, 1)


        self.gridLayout_2.addWidget(self.widget, 7, 0, 1, 2)

        QWidget.setTabOrder(self.cbReplacement, self.pbYes)
        QWidget.setTabOrder(self.pbYes, self.cbAcceptAll)
        QWidget.setTabOrder(self.cbAcceptAll, self.pbNo)
        QWidget.setTabOrder(self.pbNo, self.pbNever)

        self.retranslateUi(MissingItemDialog)

        QMetaObject.connectSlotsByName(MissingItemDialog)
    # setupUi

    def retranslateUi(self, MissingItemDialog):
        MissingItemDialog.setWindowTitle(QCoreApplication.translate("MissingItemDialog", u"Dialog", None))
        self.lbItemName.setText(QCoreApplication.translate("MissingItemDialog", u"Node name", None))
        self.label_2.setText(QCoreApplication.translate("MissingItemDialog", u"Use the following node instead:", None))
        self.label.setText(QCoreApplication.translate("MissingItemDialog", u"A node with this name could not be found:", None))
        self.pbBrowse.setText(QCoreApplication.translate("MissingItemDialog", u"...", None))
        self.cbAcceptAll.setText(QCoreApplication.translate("MissingItemDialog", u"Stop asking and automatically accept\n"
"suggested replacements", None))
        self.pbNo.setText(QCoreApplication.translate("MissingItemDialog", u"No", None))
        self.pbYes.setText(QCoreApplication.translate("MissingItemDialog", u"Accept replacement", None))
        self.pbNever.setText(QCoreApplication.translate("MissingItemDialog", u"Never", None))
    # retranslateUi

