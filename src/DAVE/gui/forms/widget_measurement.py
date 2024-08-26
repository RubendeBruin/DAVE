# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_measurement.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QLabel, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QWidget)

from DAVE.gui.helpers.qnodepicker import QNodePicker

class Ui_MeasurementWidget(object):
    def setupUi(self, MeasurementWidget):
        if not MeasurementWidget.objectName():
            MeasurementWidget.setObjectName(u"MeasurementWidget")
        MeasurementWidget.resize(258, 525)
        self.gridLayout_2 = QGridLayout(MeasurementWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_4 = QLabel(MeasurementWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)

        self.rbDistance = QRadioButton(MeasurementWidget)
        self.rbDistance.setObjectName(u"rbDistance")

        self.gridLayout_2.addWidget(self.rbDistance, 0, 1, 1, 1)

        self.rbAngle = QRadioButton(MeasurementWidget)
        self.rbAngle.setObjectName(u"rbAngle")

        self.gridLayout_2.addWidget(self.rbAngle, 1, 1, 1, 1)

        self.label_2 = QLabel(MeasurementWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.npPoint1 = QNodePicker(MeasurementWidget)
        self.npPoint1.setObjectName(u"npPoint1")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.npPoint1.sizePolicy().hasHeightForWidth())
        self.npPoint1.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.npPoint1, 2, 1, 1, 1)

        self.label_3 = QLabel(MeasurementWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)

        self.npPoint2 = QNodePicker(MeasurementWidget)
        self.npPoint2.setObjectName(u"npPoint2")
        sizePolicy.setHeightForWidth(self.npPoint2.sizePolicy().hasHeightForWidth())
        self.npPoint2.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.npPoint2, 3, 1, 1, 1)

        self.label = QLabel(MeasurementWidget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)

        self.cbDirection = QComboBox(MeasurementWidget)
        self.cbDirection.setObjectName(u"cbDirection")

        self.gridLayout_2.addWidget(self.cbDirection, 4, 1, 1, 1)

        self.label_5 = QLabel(MeasurementWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_5, 5, 0, 1, 1)

        self.npFrame = QNodePicker(MeasurementWidget)
        self.npFrame.setObjectName(u"npFrame")
        sizePolicy.setHeightForWidth(self.npFrame.sizePolicy().hasHeightForWidth())
        self.npFrame.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.npFrame, 5, 1, 1, 1)

        self.widget_advanced = QWidget(MeasurementWidget)
        self.widget_advanced.setObjectName(u"widget_advanced")
        self.gridLayout = QGridLayout(self.widget_advanced)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pbUpdateInverted = QPushButton(self.widget_advanced)
        self.pbUpdateInverted.setObjectName(u"pbUpdateInverted")

        self.gridLayout.addWidget(self.pbUpdateInverted, 3, 1, 1, 1)

        self.pbUpdatePos = QPushButton(self.widget_advanced)
        self.pbUpdatePos.setObjectName(u"pbUpdatePos")

        self.gridLayout.addWidget(self.pbUpdatePos, 2, 1, 1, 1)

        self.cbFlipAngleDirection = QCheckBox(self.widget_advanced)
        self.cbFlipAngleDirection.setObjectName(u"cbFlipAngleDirection")

        self.gridLayout.addWidget(self.cbFlipAngleDirection, 1, 1, 1, 1)

        self.label_6 = QLabel(self.widget_advanced)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.label_6, 1, 0, 3, 1)


        self.gridLayout_2.addWidget(self.widget_advanced, 6, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(161, 255, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 7, 1, 1, 1)

        QWidget.setTabOrder(self.rbDistance, self.rbAngle)
        QWidget.setTabOrder(self.rbAngle, self.cbDirection)
        QWidget.setTabOrder(self.cbDirection, self.pbUpdatePos)

        self.retranslateUi(MeasurementWidget)

        QMetaObject.connectSlotsByName(MeasurementWidget)
    # setupUi

    def retranslateUi(self, MeasurementWidget):
        MeasurementWidget.setWindowTitle(QCoreApplication.translate("MeasurementWidget", u"Form", None))
        self.label_4.setText(QCoreApplication.translate("MeasurementWidget", u"Measure", None))
        self.rbDistance.setText(QCoreApplication.translate("MeasurementWidget", u"Distance [m]", None))
        self.rbAngle.setText(QCoreApplication.translate("MeasurementWidget", u"Angle [deg]", None))
        self.label_2.setText(QCoreApplication.translate("MeasurementWidget", u"Location 1", None))
        self.label_3.setText(QCoreApplication.translate("MeasurementWidget", u"Location 2", None))
        self.label.setText(QCoreApplication.translate("MeasurementWidget", u"Along", None))
        self.label_5.setText(QCoreApplication.translate("MeasurementWidget", u"of", None))
        self.pbUpdateInverted.setText(QCoreApplication.translate("MeasurementWidget", u"Update current direction as -", None))
        self.pbUpdatePos.setText(QCoreApplication.translate("MeasurementWidget", u"Update current direction as +", None))
        self.cbFlipAngleDirection.setText(QCoreApplication.translate("MeasurementWidget", u"Flip angle sign", None))
        self.label_6.setText(QCoreApplication.translate("MeasurementWidget", u"Optional\n"
"Tweaking:", None))
    # retranslateUi

