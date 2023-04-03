# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'solverdialog_threaded.ui',
# licensing of 'solverdialog_threaded.ui' applies.
#
# Created: Fri Mar 31 20:10:03 2023
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SolverDialogThreaded(object):
    def setupUi(self, SolverDialogThreaded):
        SolverDialogThreaded.setObjectName("SolverDialogThreaded")
        SolverDialogThreaded.resize(569, 532)
        SolverDialogThreaded.setWindowOpacity(0.01)
        self.gridLayout_2 = QtWidgets.QGridLayout(SolverDialogThreaded)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pbTerminate = QtWidgets.QPushButton(SolverDialogThreaded)
        self.pbTerminate.setDefault(True)
        self.pbTerminate.setObjectName("pbTerminate")
        self.gridLayout_2.addWidget(self.pbTerminate, 5, 1, 1, 1)
        self.label = QtWidgets.QLabel(SolverDialogThreaded)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(SolverDialogThreaded)
        self.frame.setEnabled(True)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setStyleSheet("color: rgb(45, 165, 79);")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 1, 1, 1)
        self.mobilitySlider = QtWidgets.QSlider(self.frame)
        self.mobilitySlider.setOrientation(QtCore.Qt.Horizontal)
        self.mobilitySlider.setObjectName("mobilitySlider")
        self.gridLayout.addWidget(self.mobilitySlider, 4, 0, 1, 3)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setStyleSheet("color: rgb(255, 150, 2);")
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 3)
        self.pbReset = QtWidgets.QPushButton(self.frame)
        self.pbReset.setObjectName("pbReset")
        self.gridLayout.addWidget(self.pbReset, 7, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setStyleSheet("color: rgb(85, 0, 255);")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.lbMobility = QtWidgets.QLabel(self.frame)
        self.lbMobility.setAlignment(QtCore.Qt.AlignCenter)
        self.lbMobility.setObjectName("lbMobility")
        self.gridLayout.addWidget(self.lbMobility, 5, 1, 1, 1)
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 3)
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 3)
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 3)
        self.gridLayout_2.addWidget(self.frame, 3, 0, 1, 2)
        self.lbInfo = QtWidgets.QLabel(SolverDialogThreaded)
        self.lbInfo.setObjectName("lbInfo")
        self.gridLayout_2.addWidget(self.lbInfo, 1, 0, 1, 2)
        self.pbShowControls = QtWidgets.QPushButton(SolverDialogThreaded)
        self.pbShowControls.setStyleSheet("color: rgb(0, 0, 255);\n"
"text-decoration: underline;")
        self.pbShowControls.setFlat(True)
        self.pbShowControls.setObjectName("pbShowControls")
        self.gridLayout_2.addWidget(self.pbShowControls, 2, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(SolverDialogThreaded)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 2)
        self.pbAccept = QtWidgets.QPushButton(SolverDialogThreaded)
        self.pbAccept.setObjectName("pbAccept")
        self.gridLayout_2.addWidget(self.pbAccept, 5, 0, 1, 1)

        self.retranslateUi(SolverDialogThreaded)
        QtCore.QMetaObject.connectSlotsByName(SolverDialogThreaded)
        SolverDialogThreaded.setTabOrder(self.pbAccept, self.pbTerminate)
        SolverDialogThreaded.setTabOrder(self.pbTerminate, self.pbShowControls)
        SolverDialogThreaded.setTabOrder(self.pbShowControls, self.mobilitySlider)
        SolverDialogThreaded.setTabOrder(self.mobilitySlider, self.pbReset)

    def retranslateUi(self, SolverDialogThreaded):
        SolverDialogThreaded.setWindowTitle(QtWidgets.QApplication.translate("SolverDialogThreaded", "Finding equilibrium state", None, -1))
        self.pbTerminate.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Cancel", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Details of actual state:", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Usual sweet spot", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Fast but Funky", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Press \"reset\" to restart the solver from its initial position with its current settings.", None, -1))
        self.pbReset.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Reset solver to initial state", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Slow and Steady", None, -1))
        self.lbMobility.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "TextLabel", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Slow and Steady (low exploration rate)\n"
"+ Good when looking for an equilibrium position with low stability\n"
"+ Looks very thoroughly for a solution before going to the next location\n"
"- can converge slowly when set to extreme conditions. \n"
"\n"
"Move the handle this way if the solver converges to an equilibrium position too far away from the start position or when it keeps jumping around.", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Fast and Funky (high exploration rate)\n"
"+ can be useful for highly coupled systems with stiff interaction between degrees of freedom.\n"
"- can cause the solver to converge to an equilibrium position further away from the start position.\n"
"- can converge slowly or not at all when set to extreme conditions.\n"
"\n"
"Move the handle this way if the solver moves very slowly towards its equilibrium position.", None, -1))
        self.label_10.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "These settings are applied instantly when the slider is moved.", None, -1))
        self.label_9.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Use the slider to adjust the mobility of the solver.", None, -1))
        self.lbInfo.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "ABS\n"
"NORM\n"
"WHERE", None, -1))
        self.pbShowControls.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Show solver controls", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "This window automatically closes when solving is complete.", None, -1))
        self.pbAccept.setText(QtWidgets.QApplication.translate("SolverDialogThreaded", "Accept current state", None, -1))

