# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_dynprop.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_widget_dynprop(object):
    def setupUi(self, widget_dynprop):
        if not widget_dynprop.objectName():
            widget_dynprop.setObjectName(u"widget_dynprop")
        widget_dynprop.resize(1293, 1074)
        self.horizontalLayout = QHBoxLayout(widget_dynprop)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(widget_dynprop)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lblChangeDynamicInfo = QLabel(self.widget)
        self.lblChangeDynamicInfo.setObjectName(u"lblChangeDynamicInfo")

        self.verticalLayout_2.addWidget(self.lblChangeDynamicInfo)

        self.tableDynProp = QTableWidget(self.widget)
        if (self.tableDynProp.columnCount() < 13):
            self.tableDynProp.setColumnCount(13)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(11, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableDynProp.setHorizontalHeaderItem(12, __qtablewidgetitem12)
        self.tableDynProp.setObjectName(u"tableDynProp")
        self.tableDynProp.horizontalHeader().setMinimumSectionSize(20)
        self.tableDynProp.verticalHeader().setVisible(True)

        self.verticalLayout_2.addWidget(self.tableDynProp)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(widget_dynprop)

        QMetaObject.connectSlotsByName(widget_dynprop)
    # setupUi

    def retranslateUi(self, widget_dynprop):
        widget_dynprop.setWindowTitle(QCoreApplication.translate("widget_dynprop", u"Form", None))
        self.lblChangeDynamicInfo.setText(QCoreApplication.translate("widget_dynprop", u"Note: For RigidBody type nodes the inertia properties are coupled to the weight properties.\n"
"Changing the intertia properties changes the weight properties as well", None))
        ___qtablewidgetitem = self.tableDynProp.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("widget_dynprop", u"F", None));
        ___qtablewidgetitem1 = self.tableDynProp.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("widget_dynprop", u"I", None));
        ___qtablewidgetitem2 = self.tableDynProp.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("widget_dynprop", u"X", None));
        ___qtablewidgetitem3 = self.tableDynProp.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("widget_dynprop", u"E", None));
        ___qtablewidgetitem4 = self.tableDynProp.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("widget_dynprop", u"D", None));
        ___qtablewidgetitem5 = self.tableDynProp.horizontalHeaderItem(6)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("widget_dynprop", u"Inertia (weight)", None));
        ___qtablewidgetitem6 = self.tableDynProp.horizontalHeaderItem(7)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("widget_dynprop", u"x (cog)", None));
        ___qtablewidgetitem7 = self.tableDynProp.horizontalHeaderItem(8)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("widget_dynprop", u"y (cog)", None));
        ___qtablewidgetitem8 = self.tableDynProp.horizontalHeaderItem(9)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("widget_dynprop", u" (cog)", None));
        ___qtablewidgetitem9 = self.tableDynProp.horizontalHeaderItem(10)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("widget_dynprop", u"rxx", None));
        ___qtablewidgetitem10 = self.tableDynProp.horizontalHeaderItem(11)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("widget_dynprop", u"ryy", None));
        ___qtablewidgetitem11 = self.tableDynProp.horizontalHeaderItem(12)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("widget_dynprop", u"rzz", None));
    # retranslateUi

