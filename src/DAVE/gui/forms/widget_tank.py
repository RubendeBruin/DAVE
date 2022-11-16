# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_tank.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(321, 303)
        Form.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.sbPermeability = QDoubleSpinBox(Form)
        self.sbPermeability.setObjectName(u"sbPermeability")
        self.sbPermeability.setDecimals(8)
        self.sbPermeability.setMaximum(2.000000000000000)
        self.sbPermeability.setSingleStep(0.000010000000000)
        self.sbPermeability.setValue(1.000000000000000)

        self.gridLayout_2.addWidget(self.sbPermeability, 0, 1, 1, 1)

        self.cbFreeFlooding = QCheckBox(Form)
        self.cbFreeFlooding.setObjectName(u"cbFreeFlooding")

        self.gridLayout_2.addWidget(self.cbFreeFlooding, 1, 0, 1, 1)

        self.widgetContents = QWidget(Form)
        self.widgetContents.setObjectName(u"widgetContents")
        self.gridLayout = QGridLayout(self.widgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.lblCapacity = QLabel(self.widgetContents)
        self.lblCapacity.setObjectName(u"lblCapacity")

        self.gridLayout.addWidget(self.lblCapacity, 1, 1, 1, 1)

        self.sbDenstiy = QDoubleSpinBox(self.widgetContents)
        self.sbDenstiy.setObjectName(u"sbDenstiy")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbDenstiy.sizePolicy().hasHeightForWidth())
        self.sbDenstiy.setSizePolicy(sizePolicy)
        self.sbDenstiy.setDecimals(3)
        self.sbDenstiy.setMinimum(-999999999999.000000000000000)
        self.sbDenstiy.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.sbDenstiy, 4, 1, 1, 1)

        self.sbPercentage = QDoubleSpinBox(self.widgetContents)
        self.sbPercentage.setObjectName(u"sbPercentage")
        sizePolicy.setHeightForWidth(self.sbPercentage.sizePolicy().hasHeightForWidth())
        self.sbPercentage.setSizePolicy(sizePolicy)
        self.sbPercentage.setDecimals(3)
        self.sbPercentage.setMinimum(0.000000000000000)
        self.sbPercentage.setMaximum(100.000000000000000)
        self.sbPercentage.setSingleStep(5.000000000000000)

        self.gridLayout.addWidget(self.sbPercentage, 8, 1, 1, 1)

        self.cbUseOutsideDensity = QCheckBox(self.widgetContents)
        self.cbUseOutsideDensity.setObjectName(u"cbUseOutsideDensity")

        self.gridLayout.addWidget(self.cbUseOutsideDensity, 3, 0, 1, 1)

        self.label_10 = QLabel(self.widgetContents)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setWordWrap(True)

        self.gridLayout.addWidget(self.label_10, 5, 0, 1, 1)

        self.label_2 = QLabel(self.widgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)

        self.label_5 = QLabel(self.widgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.sbElevation = QDoubleSpinBox(self.widgetContents)
        self.sbElevation.setObjectName(u"sbElevation")
        sizePolicy.setHeightForWidth(self.sbElevation.sizePolicy().hasHeightForWidth())
        self.sbElevation.setSizePolicy(sizePolicy)
        self.sbElevation.setDecimals(3)
        self.sbElevation.setMinimum(-999999999999.000000000000000)
        self.sbElevation.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.sbElevation, 9, 1, 1, 1)

        self.sbVolume = QDoubleSpinBox(self.widgetContents)
        self.sbVolume.setObjectName(u"sbVolume")
        sizePolicy.setHeightForWidth(self.sbVolume.sizePolicy().hasHeightForWidth())
        self.sbVolume.setSizePolicy(sizePolicy)
        self.sbVolume.setDecimals(3)
        self.sbVolume.setMinimum(-999999999999.000000000000000)
        self.sbVolume.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.sbVolume, 7, 1, 1, 1)

        self.label_8 = QLabel(self.widgetContents)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_8.setWordWrap(False)

        self.gridLayout.addWidget(self.label_8, 11, 1, 1, 1)

        self.label = QLabel(self.widgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)

        self.label_9 = QLabel(self.widgetContents)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setWordWrap(True)

        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_3 = QLabel(self.widgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 8, 0, 1, 1)

        self.label_4 = QLabel(self.widgetContents)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 9, 0, 1, 1)

        self.label_7 = QLabel(self.widgetContents)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 10, 0, 1, 1)

        self.lbUllage = QLabel(self.widgetContents)
        self.lbUllage.setObjectName(u"lbUllage")

        self.gridLayout.addWidget(self.lbUllage, 10, 1, 1, 1)


        self.gridLayout_2.addWidget(self.widgetContents, 2, 0, 1, 2)

        QWidget.setTabOrder(self.sbPermeability, self.cbFreeFlooding)
        QWidget.setTabOrder(self.cbFreeFlooding, self.cbUseOutsideDensity)
        QWidget.setTabOrder(self.cbUseOutsideDensity, self.sbDenstiy)
        QWidget.setTabOrder(self.sbDenstiy, self.sbVolume)
        QWidget.setTabOrder(self.sbVolume, self.sbPercentage)
        QWidget.setTabOrder(self.sbPercentage, self.sbElevation)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Permeability", None))
        self.cbFreeFlooding.setText(QCoreApplication.translate("Form", u"Free flooding (aka damaged)", None))
        self.lblCapacity.setText(QCoreApplication.translate("Form", u"Calculated", None))
        self.cbUseOutsideDensity.setText(QCoreApplication.translate("Form", u"Same as outside water", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Fill</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Volume [m3]", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Maximum capacity", None))
#if QT_CONFIG(tooltip)
        self.label_8.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Setting any of these values changes the amount of fluid in the tank. Global elevation may thus change if the vessel moves.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_8.setText(QCoreApplication.translate("Form", u"note (hoover to show)", None))
        self.label.setText(QCoreApplication.translate("Form", u"Contents density [mT/m3]", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Fluid density</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Fill percentage [%]", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Global Elevation [m]", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Ullage", None))
        self.lbUllage.setText(QCoreApplication.translate("Form", u"Calculated", None))
    # retranslateUi

