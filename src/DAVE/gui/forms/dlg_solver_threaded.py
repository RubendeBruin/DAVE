# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'solverdialog_threaded.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSlider, QWidget)

class Ui_SolverDialogThreaded(object):
    def setupUi(self, SolverDialogThreaded):
        if not SolverDialogThreaded.objectName():
            SolverDialogThreaded.setObjectName(u"SolverDialogThreaded")
        SolverDialogThreaded.resize(569, 532)
        SolverDialogThreaded.setWindowOpacity(0.010000000000000)
        self.gridLayout_2 = QGridLayout(SolverDialogThreaded)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pbTerminate = QPushButton(SolverDialogThreaded)
        self.pbTerminate.setObjectName(u"pbTerminate")

        self.gridLayout_2.addWidget(self.pbTerminate, 5, 1, 1, 1)

        self.label = QLabel(SolverDialogThreaded)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.frame = QFrame(SolverDialogThreaded)
        self.frame.setObjectName(u"frame")
        self.frame.setEnabled(True)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Plain)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"color: rgb(45, 165, 79);")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_7, 3, 1, 1, 1)

        self.mobilitySlider = QSlider(self.frame)
        self.mobilitySlider.setObjectName(u"mobilitySlider")
        self.mobilitySlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.mobilitySlider, 4, 0, 1, 3)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"color: rgb(255, 150, 2);")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_6, 3, 2, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 3)

        self.pbReset = QPushButton(self.frame)
        self.pbReset.setObjectName(u"pbReset")

        self.gridLayout.addWidget(self.pbReset, 7, 0, 1, 1)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"color: rgb(85, 0, 255);")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.lbMobility = QLabel(self.frame)
        self.lbMobility.setObjectName(u"lbMobility")
        self.lbMobility.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lbMobility, 5, 1, 1, 1)

        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)

        self.horizontalLayout.addWidget(self.label_4)

        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setLineWidth(1)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setWordWrap(True)

        self.horizontalLayout.addWidget(self.label_8)


        self.gridLayout.addWidget(self.widget, 1, 0, 1, 3)

        self.label_10 = QLabel(self.frame)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 3)

        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 3)

        self.cbLinearFirst = QCheckBox(self.frame)
        self.cbLinearFirst.setObjectName(u"cbLinearFirst")

        self.gridLayout.addWidget(self.cbLinearFirst, 7, 1, 1, 2)


        self.gridLayout_2.addWidget(self.frame, 3, 0, 1, 2)

        self.lbInfo = QLabel(SolverDialogThreaded)
        self.lbInfo.setObjectName(u"lbInfo")

        self.gridLayout_2.addWidget(self.lbInfo, 1, 0, 1, 2)

        self.pbShowControls = QPushButton(SolverDialogThreaded)
        self.pbShowControls.setObjectName(u"pbShowControls")
        self.pbShowControls.setStyleSheet(u"color: rgb(0, 0, 255);\n"
"text-decoration: underline;")
        self.pbShowControls.setFlat(True)

        self.gridLayout_2.addWidget(self.pbShowControls, 2, 0, 1, 2)

        self.label_3 = QLabel(SolverDialogThreaded)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 2)

        self.pbAccept = QPushButton(SolverDialogThreaded)
        self.pbAccept.setObjectName(u"pbAccept")

        self.gridLayout_2.addWidget(self.pbAccept, 5, 0, 1, 1)

        QWidget.setTabOrder(self.pbAccept, self.pbTerminate)
        QWidget.setTabOrder(self.pbTerminate, self.pbShowControls)
        QWidget.setTabOrder(self.pbShowControls, self.mobilitySlider)
        QWidget.setTabOrder(self.mobilitySlider, self.pbReset)

        self.retranslateUi(SolverDialogThreaded)

        self.pbTerminate.setDefault(True)


        QMetaObject.connectSlotsByName(SolverDialogThreaded)
    # setupUi

    def retranslateUi(self, SolverDialogThreaded):
        SolverDialogThreaded.setWindowTitle(QCoreApplication.translate("SolverDialogThreaded", u"Finding equilibrium state", None))
        self.pbTerminate.setText(QCoreApplication.translate("SolverDialogThreaded", u"Cancel", None))
        self.label.setText(QCoreApplication.translate("SolverDialogThreaded", u"Details of actual state:", None))
        self.label_7.setText(QCoreApplication.translate("SolverDialogThreaded", u"Usual sweet spot", None))
        self.label_6.setText(QCoreApplication.translate("SolverDialogThreaded", u"Fast but Funky", None))
        self.label_2.setText(QCoreApplication.translate("SolverDialogThreaded", u"Press \"reset\" to restart the solver from its initial position with its current settings.", None))
        self.pbReset.setText(QCoreApplication.translate("SolverDialogThreaded", u"Reset solver to initial state", None))
        self.label_5.setText(QCoreApplication.translate("SolverDialogThreaded", u"Slow and Steady", None))
        self.lbMobility.setText(QCoreApplication.translate("SolverDialogThreaded", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("SolverDialogThreaded", u"Slow and Steady (low exploration rate)\n"
"+ Good when looking for an equilibrium position with low stability\n"
"+ Looks very thoroughly for a solution before going to the next location\n"
"- can converge slowly when set to extreme conditions. \n"
"\n"
"Move the handle this way if the solver converges to an equilibrium position too far away from the start position or when it keeps jumping around.", None))
        self.label_8.setText(QCoreApplication.translate("SolverDialogThreaded", u"Fast and Funky (high exploration rate)\n"
"+ can be useful for highly coupled systems with stiff interaction between degrees of freedom.\n"
"- can cause the solver to converge to an equilibrium position further away from the start position.\n"
"- can converge slowly or not at all when set to extreme conditions.\n"
"\n"
"Move the handle this way if the solver moves very slowly towards its equilibrium position.", None))
        self.label_10.setText(QCoreApplication.translate("SolverDialogThreaded", u"This setting is applied instantly when the slider is moved.", None))
        self.label_9.setText(QCoreApplication.translate("SolverDialogThreaded", u"Use the slider to adjust the mobility of the solver.", None))
#if QT_CONFIG(statustip)
        self.cbLinearFirst.setStatusTip(QCoreApplication.translate("SolverDialogThreaded", u"Takes effect after solver restart", None))
#endif // QT_CONFIG(statustip)
        self.cbLinearFirst.setText(QCoreApplication.translate("SolverDialogThreaded", u"Solve linear degrees of freedom before solving full model", None))
        self.lbInfo.setText(QCoreApplication.translate("SolverDialogThreaded", u"ABS\n"
"NORM\n"
"WHERE", None))
        self.pbShowControls.setText(QCoreApplication.translate("SolverDialogThreaded", u"Show solver controls", None))
        self.label_3.setText(QCoreApplication.translate("SolverDialogThreaded", u"This window automatically closes when solving is complete.", None))
        self.pbAccept.setText(QCoreApplication.translate("SolverDialogThreaded", u"Accept current state", None))
    # retranslateUi

