# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'resource_browser.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QScrollBar, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ResourceBrowser(object):
    def setupUi(self, ResourceBrowser):
        if not ResourceBrowser.objectName():
            ResourceBrowser.setObjectName(u"ResourceBrowser")
        ResourceBrowser.resize(1142, 712)
        self.gridLayout_2 = QGridLayout(ResourceBrowser)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.widget_RES = QWidget(ResourceBrowser)
        self.widget_RES.setObjectName(u"widget_RES")
        self.verticalLayout = QVBoxLayout(self.widget_RES)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.widget_RES)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.lwResourcePaths = QListWidget(self.widget_RES)
        QListWidgetItem(self.lwResourcePaths)
        QListWidgetItem(self.lwResourcePaths)
        QListWidgetItem(self.lwResourcePaths)
        self.lwResourcePaths.setObjectName(u"lwResourcePaths")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lwResourcePaths.sizePolicy().hasHeightForWidth())
        self.lwResourcePaths.setSizePolicy(sizePolicy)
        self.lwResourcePaths.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout.addWidget(self.lwResourcePaths)


        self.gridLayout_2.addWidget(self.widget_RES, 2, 0, 1, 1)

        self.lwWhere = QListWidget(ResourceBrowser)
        QListWidgetItem(self.lwWhere)
        QListWidgetItem(self.lwWhere)
        QListWidgetItem(self.lwWhere)
        self.lwWhere.setObjectName(u"lwWhere")
        sizePolicy.setHeightForWidth(self.lwWhere.sizePolicy().hasHeightForWidth())
        self.lwWhere.setSizePolicy(sizePolicy)
        self.lwWhere.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.gridLayout_2.addWidget(self.lwWhere, 1, 0, 1, 1)

        self.widget_2 = QWidget(ResourceBrowser)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.widget_2)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.widget_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.gridLayout_2.addWidget(self.widget_2, 4, 0, 1, 2)

        self.label_4 = QLabel(ResourceBrowser)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)

        self.widget = QWidget(ResourceBrowser)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.teFilter = QLineEdit(self.widget)
        self.teFilter.setObjectName(u"teFilter")

        self.gridLayout.addWidget(self.teFilter, 0, 3, 1, 1)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.hsZoom = QScrollBar(self.widget)
        self.hsZoom.setObjectName(u"hsZoom")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.hsZoom.sizePolicy().hasHeightForWidth())
        self.hsZoom.setSizePolicy(sizePolicy4)
        self.hsZoom.setMinimum(1)
        self.hsZoom.setMaximum(400)
        self.hsZoom.setValue(100)
        self.hsZoom.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.hsZoom, 0, 1, 1, 1)

        self.TumbnailArea = QWidget(self.widget)
        self.TumbnailArea.setObjectName(u"TumbnailArea")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.TumbnailArea.sizePolicy().hasHeightForWidth())
        self.TumbnailArea.setSizePolicy(sizePolicy5)

        self.gridLayout.addWidget(self.TumbnailArea, 3, 0, 1, 6)


        self.gridLayout_2.addWidget(self.widget, 0, 1, 4, 1)


        self.retranslateUi(ResourceBrowser)

        QMetaObject.connectSlotsByName(ResourceBrowser)
    # setupUi

    def retranslateUi(self, ResourceBrowser):
        ResourceBrowser.setWindowTitle(QCoreApplication.translate("ResourceBrowser", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("ResourceBrowser", u"Resource system location:", None))

        __sortingEnabled = self.lwResourcePaths.isSortingEnabled()
        self.lwResourcePaths.setSortingEnabled(False)
        ___qlistwidgetitem = self.lwResourcePaths.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("ResourceBrowser", u"SHOW ALL RESOURCES", None));
        ___qlistwidgetitem1 = self.lwResourcePaths.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("ResourceBrowser", u"DAVE_models", None));
        ___qlistwidgetitem2 = self.lwResourcePaths.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("ResourceBrowser", u"synced folder", None));
        self.lwResourcePaths.setSortingEnabled(__sortingEnabled)


        __sortingEnabled1 = self.lwWhere.isSortingEnabled()
        self.lwWhere.setSortingEnabled(False)
        ___qlistwidgetitem3 = self.lwWhere.item(0)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("ResourceBrowser", u"Resource system (res:)", None));
        ___qlistwidgetitem4 = self.lwWhere.item(1)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("ResourceBrowser", u"Model folder (cd: )", None));
        ___qlistwidgetitem5 = self.lwWhere.item(2)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("ResourceBrowser", u"Local file", None));
        self.lwWhere.setSortingEnabled(__sortingEnabled1)

        self.pushButton.setText(QCoreApplication.translate("ResourceBrowser", u"Ok", None))
        self.pushButton_2.setText(QCoreApplication.translate("ResourceBrowser", u"Cancel", None))
        self.label_4.setText(QCoreApplication.translate("ResourceBrowser", u"Find resource in:", None))
        self.label.setText(QCoreApplication.translate("ResourceBrowser", u"Zoom:", None))
        self.label_3.setText(QCoreApplication.translate("ResourceBrowser", u"Search", None))
    # retranslateUi

