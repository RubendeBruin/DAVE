# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_export_to_blender.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpinBox,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(629, 169)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.sbFrames_per_step = QSpinBox(Dialog)
        self.sbFrames_per_step.setObjectName(u"sbFrames_per_step")
        self.sbFrames_per_step.setMinimum(1)
        self.sbFrames_per_step.setMaximum(9999)
        self.sbFrames_per_step.setValue(24)

        self.gridLayout.addWidget(self.sbFrames_per_step, 1, 2, 1, 1)

        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 2, 3, 1, 1)

        self.teExecutable = QLineEdit(Dialog)
        self.teExecutable.setObjectName(u"teExecutable")

        self.gridLayout.addWidget(self.teExecutable, 3, 1, 1, 2)

        self.radioButton_2 = QRadioButton(Dialog)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout.addWidget(self.radioButton_2, 1, 1, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 3, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.radioButton = QRadioButton(Dialog)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)

        self.gridLayout.addWidget(self.radioButton, 0, 1, 1, 1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 3, 1, 1)

        self.cbBaseScene = QComboBox(Dialog)
        self.cbBaseScene.setObjectName(u"cbBaseScene")
        self.cbBaseScene.setEditable(True)

        self.gridLayout.addWidget(self.cbBaseScene, 2, 1, 1, 2)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnOK = QPushButton(self.frame)
        self.btnOK.setObjectName(u"btnOK")

        self.horizontalLayout.addWidget(self.btnOK)

        self.btnCancel = QPushButton(self.frame)
        self.btnCancel.setObjectName(u"btnCancel")

        self.horizontalLayout.addWidget(self.btnCancel)


        self.gridLayout.addWidget(self.frame, 4, 1, 1, 3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u".blend file", None))
        self.radioButton_2.setText(QCoreApplication.translate("Dialog", u"Animation using", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Blender template file", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Blender executable:", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"blender-launcher.exe", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Export", None))
        self.radioButton.setText(QCoreApplication.translate("Dialog", u"Current view (image)", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"frames per step or second", None))
        self.btnOK.setText(QCoreApplication.translate("Dialog", u"Export", None))
        self.btnCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

