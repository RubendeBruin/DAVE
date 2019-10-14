# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_name.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NameWidget(object):
    def setupUi(self, NameWidget):
        NameWidget.setObjectName("NameWidget")
        NameWidget.resize(503, 68)
        self.horizontalLayout = QtWidgets.QHBoxLayout(NameWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(NameWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.tbName = QtWidgets.QLineEdit(NameWidget)
        self.tbName.setObjectName("tbName")
        self.horizontalLayout.addWidget(self.tbName)

        self.retranslateUi(NameWidget)
        QtCore.QMetaObject.connectSlotsByName(NameWidget)

    def retranslateUi(self, NameWidget):
        _translate = QtCore.QCoreApplication.translate
        NameWidget.setWindowTitle(_translate("NameWidget", "Form"))
        self.label.setText(_translate("NameWidget", "Name [unique]"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NameWidget = QtWidgets.QWidget()
    ui = Ui_NameWidget()
    ui.setupUi(NameWidget)
    NameWidget.show()
    sys.exit(app.exec_())

