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
        AnimationWindow.resize(1341, 891)
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
        self.dockWidget.setWidget(self.dockWidgetContents)
        AnimationWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)

        self.retranslateUi(AnimationWindow)
        QtCore.QMetaObject.connectSlotsByName(AnimationWindow)

    def retranslateUi(self, AnimationWindow):
        _translate = QtCore.QCoreApplication.translate
        AnimationWindow.setWindowTitle(_translate("AnimationWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AnimationWindow = QtWidgets.QMainWindow()
    ui = Ui_AnimationWindow()
    ui.setupUi(AnimationWindow)
    AnimationWindow.show()
    sys.exit(app.exec_())

