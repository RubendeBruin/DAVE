# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frm_animation.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AnimationWindow(object):
    def setupUi(self, AnimationWindow):
        AnimationWindow.setObjectName("AnimationWindow")
        AnimationWindow.resize(1689, 1060)
        self.centralwidget = QtWidgets.QWidget(AnimationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame3d = QtWidgets.QFrame(self.centralwidget)
        self.frame3d.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame3d.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame3d.setObjectName("frame3d")
        self.horizontalLayout.addWidget(self.frame3d)
        AnimationWindow.setCentralWidget(self.centralwidget)
        self.dockWidget = QtWidgets.QDockWidget(AnimationWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblInfo = QtWidgets.QLabel(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblInfo.setFont(font)
        self.lblInfo.setObjectName("lblInfo")
        self.verticalLayout.addWidget(self.lblInfo)
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalSlider = QtWidgets.QSlider(self.dockWidgetContents)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout.addWidget(self.horizontalSlider)
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.dockWidgetContents)
        self.horizontalSlider_2.setMinimum(1)
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setProperty("value", 10)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.verticalLayout.addWidget(self.horizontalSlider_2)
        spacerItem = QtWidgets.QSpacerItem(20, 839, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.dockWidget.setWidget(self.dockWidgetContents)
        AnimationWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)

        self.retranslateUi(AnimationWindow)
        QtCore.QMetaObject.connectSlotsByName(AnimationWindow)

    def retranslateUi(self, AnimationWindow):
        _translate = QtCore.QCoreApplication.translate
        AnimationWindow.setWindowTitle(_translate("AnimationWindow", "MainWindow"))
        self.lblInfo.setText(_translate("AnimationWindow", "0.1 rad/s | 62 s"))
        self.label.setText(_translate("AnimationWindow", "Mode-shape"))
        self.label_2.setText(_translate("AnimationWindow", "Scale"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AnimationWindow = QtWidgets.QMainWindow()
    ui = Ui_AnimationWindow()
    ui.setupUi(AnimationWindow)
    AnimationWindow.show()
    sys.exit(app.exec_())

