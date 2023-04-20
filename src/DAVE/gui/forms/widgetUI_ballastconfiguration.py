# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_ballastconfiguration.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QHBoxLayout,
    QHeaderView, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_widget_ballastsystem(object):
    def setupUi(self, widget_ballastsystem):
        if not widget_ballastsystem.objectName():
            widget_ballastsystem.setObjectName(u"widget_ballastsystem")
        widget_ballastsystem.resize(441, 1214)
        widget_ballastsystem.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widget_ballastsystem)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(widget_ballastsystem)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pbFillAll = QPushButton(self.widget_2)
        self.pbFillAll.setObjectName(u"pbFillAll")

        self.horizontalLayout_2.addWidget(self.pbFillAll)

        self.pbEmptyAll = QPushButton(self.widget_2)
        self.pbEmptyAll.setObjectName(u"pbEmptyAll")

        self.horizontalLayout_2.addWidget(self.pbEmptyAll)

        self.pbToggleFreeze = QPushButton(self.widget_2)
        self.pbToggleFreeze.setObjectName(u"pbToggleFreeze")

        self.horizontalLayout_2.addWidget(self.pbToggleFreeze)

        self.pbUnfreezeAll = QPushButton(self.widget_2)
        self.pbUnfreezeAll.setObjectName(u"pbUnfreezeAll")

        self.horizontalLayout_2.addWidget(self.pbUnfreezeAll)

        self.pbFreezeAll = QPushButton(self.widget_2)
        self.pbFreezeAll.setObjectName(u"pbFreezeAll")

        self.horizontalLayout_2.addWidget(self.pbFreezeAll)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget = QWidget(widget_ballastsystem)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pgGoEvenKeel = QPushButton(self.widget)
        self.pgGoEvenKeel.setObjectName(u"pgGoEvenKeel")

        self.horizontalLayout.addWidget(self.pgGoEvenKeel)

        self.rbUp = QRadioButton(self.widget)
        self.rbUp.setObjectName(u"rbUp")

        self.horizontalLayout.addWidget(self.rbUp)

        self.rbDown = QRadioButton(self.widget)
        self.rbDown.setObjectName(u"rbDown")
        self.rbDown.setChecked(True)

        self.horizontalLayout.addWidget(self.rbDown)

        self.cbPassive = QCheckBox(self.widget)
        self.cbPassive.setObjectName(u"cbPassive")

        self.horizontalLayout.addWidget(self.cbPassive)


        self.verticalLayout.addWidget(self.widget)

        self.tableWidget = QTableWidget(widget_ballastsystem)
        if (self.tableWidget.columnCount() < 6):
            self.tableWidget.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        if (self.tableWidget.rowCount() < 2):
            self.tableWidget.setRowCount(2)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem7)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setDragEnabled(True)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setDragDropMode(QAbstractItemView.InternalMove)

        self.verticalLayout.addWidget(self.tableWidget)

        self.pbGenerate = QPushButton(widget_ballastsystem)
        self.pbGenerate.setObjectName(u"pbGenerate")

        self.verticalLayout.addWidget(self.pbGenerate)

        QWidget.setTabOrder(self.tableWidget, self.pbFillAll)
        QWidget.setTabOrder(self.pbFillAll, self.pbEmptyAll)
        QWidget.setTabOrder(self.pbEmptyAll, self.pbToggleFreeze)
        QWidget.setTabOrder(self.pbToggleFreeze, self.pbUnfreezeAll)
        QWidget.setTabOrder(self.pbUnfreezeAll, self.pbFreezeAll)

        self.retranslateUi(widget_ballastsystem)

        QMetaObject.connectSlotsByName(widget_ballastsystem)
    # setupUi

    def retranslateUi(self, widget_ballastsystem):
        widget_ballastsystem.setWindowTitle(QCoreApplication.translate("widget_ballastsystem", u"Form", None))
        self.pbFillAll.setText(QCoreApplication.translate("widget_ballastsystem", u"Fill all", None))
        self.pbEmptyAll.setText(QCoreApplication.translate("widget_ballastsystem", u"Empty all", None))
        self.pbToggleFreeze.setText(QCoreApplication.translate("widget_ballastsystem", u"Toggle freeze", None))
        self.pbUnfreezeAll.setText(QCoreApplication.translate("widget_ballastsystem", u"Unfreeze all", None))
        self.pbFreezeAll.setText(QCoreApplication.translate("widget_ballastsystem", u"Freeze all", None))
        self.pgGoEvenKeel.setText(QCoreApplication.translate("widget_ballastsystem", u"Go even keel", None))
        self.rbUp.setText(QCoreApplication.translate("widget_ballastsystem", u"Up", None))
        self.rbDown.setText(QCoreApplication.translate("widget_ballastsystem", u"Down", None))
#if QT_CONFIG(tooltip)
        self.cbPassive.setToolTip(QCoreApplication.translate("widget_ballastsystem", u"Only fill tanks using natural flow (no pumps). Tanks are filled to maximum the outside waterline", None))
#endif // QT_CONFIG(tooltip)
        self.cbPassive.setText(QCoreApplication.translate("widget_ballastsystem", u"Passive only", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("widget_ballastsystem", u"Capacity [m3]", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("widget_ballastsystem", u"Fill [%]", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("widget_ballastsystem", u"Frozen", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("widget_ballastsystem", u"X [m]", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("widget_ballastsystem", u"Y [m]", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("widget_ballastsystem", u"Z [m]", None));
        ___qtablewidgetitem6 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("widget_ballastsystem", u"Tank1", None));
        ___qtablewidgetitem7 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("widget_ballastsystem", u"Tank2", None));
        self.pbGenerate.setText(QCoreApplication.translate("widget_ballastsystem", u"Generate tank-fill python code", None))
    # retranslateUi

