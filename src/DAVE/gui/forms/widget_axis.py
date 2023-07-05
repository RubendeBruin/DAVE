# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_axis.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)

from DAVE.gui.helpers.qnodepicker import QNodePicker

class Ui_widget_axis(object):
    def setupUi(self, widget_axis):
        if not widget_axis.objectName():
            widget_axis.setObjectName(u"widget_axis")
        widget_axis.resize(427, 637)
        widget_axis.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout = QVBoxLayout(widget_axis)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_7 = QLabel(widget_axis)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_7)

        self.frame = QFrame(widget_axis)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.doubleSpinBox_2 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy)
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_2.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_2, 1, 2, 1, 2)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.checkBox_3 = QCheckBox(self.frame)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout.addWidget(self.checkBox_3, 2, 1, 1, 1)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_3.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_3.setSizePolicy(sizePolicy)
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_3.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_3, 2, 2, 1, 2)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_4.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_4.setSizePolicy(sizePolicy)
        self.doubleSpinBox_4.setDecimals(3)
        self.doubleSpinBox_4.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_4.setMaximum(99999999999999.000000000000000)
        self.doubleSpinBox_4.setSingleStep(5.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_4, 5, 2, 1, 2)

        self.pbToggleAllFixes = QPushButton(self.frame)
        self.pbToggleAllFixes.setObjectName(u"pbToggleAllFixes")

        self.gridLayout.addWidget(self.pbToggleAllFixes, 9, 1, 1, 1)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.HLine)
        self.frame_2.setFrameShadow(QFrame.Plain)

        self.gridLayout.addWidget(self.frame_2, 3, 0, 1, 1)

        self.doubleSpinBox_5 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_5.setObjectName(u"doubleSpinBox_5")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_5.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_5.setSizePolicy(sizePolicy)
        self.doubleSpinBox_5.setDecimals(3)
        self.doubleSpinBox_5.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_5.setMaximum(99999999999999.000000000000000)
        self.doubleSpinBox_5.setSingleStep(5.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_5, 6, 2, 1, 2)

        self.checkBox_4 = QCheckBox(self.frame)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.gridLayout.addWidget(self.checkBox_4, 5, 1, 1, 1)

        self.checkBox_5 = QCheckBox(self.frame)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.gridLayout.addWidget(self.checkBox_5, 6, 1, 1, 1)

        self.checkBox_6 = QCheckBox(self.frame)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.gridLayout.addWidget(self.checkBox_6, 7, 1, 1, 1)

        self.doubleSpinBox_1 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_1.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_1.setSizePolicy(sizePolicy)
        self.doubleSpinBox_1.setDecimals(3)
        self.doubleSpinBox_1.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_1.setMaximum(99999999999999.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_1, 0, 2, 1, 2)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.toolButton = QToolButton(self.frame)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setLayoutDirection(Qt.RightToLeft)
        self.toolButton.setToolButtonStyle(Qt.ToolButtonTextOnly)

        self.gridLayout.addWidget(self.toolButton, 9, 2, 1, 2)

        self.checkBox_1 = QCheckBox(self.frame)
        self.checkBox_1.setObjectName(u"checkBox_1")

        self.gridLayout.addWidget(self.checkBox_1, 0, 1, 1, 1)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)

        self.doubleSpinBox_6 = QDoubleSpinBox(self.frame)
        self.doubleSpinBox_6.setObjectName(u"doubleSpinBox_6")
        sizePolicy.setHeightForWidth(self.doubleSpinBox_6.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_6.setSizePolicy(sizePolicy)
        self.doubleSpinBox_6.setDecimals(3)
        self.doubleSpinBox_6.setMinimum(-999999999999.000000000000000)
        self.doubleSpinBox_6.setMaximum(99999999999999.000000000000000)
        self.doubleSpinBox_6.setSingleStep(5.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_6, 7, 2, 1, 2)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.checkBox_2 = QCheckBox(self.frame)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout.addWidget(self.checkBox_2, 1, 1, 1, 1)

        self.lblRotationsWarning = QLabel(self.frame)
        self.lblRotationsWarning.setObjectName(u"lblRotationsWarning")
        self.lblRotationsWarning.setStyleSheet(u"background-color: rgb(255, 238, 220);")
        self.lblRotationsWarning.setLocale(QLocale(QLocale.English, QLocale.Uganda))
        self.lblRotationsWarning.setFrameShape(QFrame.NoFrame)
        self.lblRotationsWarning.setFrameShadow(QFrame.Plain)
        self.lblRotationsWarning.setLineWidth(3)
        self.lblRotationsWarning.setWordWrap(True)
        self.lblRotationsWarning.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.lblRotationsWarning, 4, 0, 1, 4)


        self.verticalLayout.addWidget(self.frame)

        self.label_9 = QLabel(widget_axis)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_9)

        self.widget = QWidget(widget_axis)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.label_8)

        self.widgetParent = QNodePicker(self.widget)
        self.widgetParent.setObjectName(u"widgetParent")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widgetParent.sizePolicy().hasHeightForWidth())
        self.widgetParent.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.widgetParent)


        self.verticalLayout.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.checkBox_1, self.doubleSpinBox_1)
        QWidget.setTabOrder(self.doubleSpinBox_1, self.checkBox_2)
        QWidget.setTabOrder(self.checkBox_2, self.doubleSpinBox_2)
        QWidget.setTabOrder(self.doubleSpinBox_2, self.checkBox_3)
        QWidget.setTabOrder(self.checkBox_3, self.doubleSpinBox_3)
        QWidget.setTabOrder(self.doubleSpinBox_3, self.checkBox_4)
        QWidget.setTabOrder(self.checkBox_4, self.doubleSpinBox_4)
        QWidget.setTabOrder(self.doubleSpinBox_4, self.checkBox_5)
        QWidget.setTabOrder(self.checkBox_5, self.doubleSpinBox_5)
        QWidget.setTabOrder(self.doubleSpinBox_5, self.checkBox_6)
        QWidget.setTabOrder(self.checkBox_6, self.doubleSpinBox_6)
        QWidget.setTabOrder(self.doubleSpinBox_6, self.pbToggleAllFixes)

        self.retranslateUi(widget_axis)

        QMetaObject.connectSlotsByName(widget_axis)
    # setupUi

    def retranslateUi(self, widget_axis):
        widget_axis.setWindowTitle(QCoreApplication.translate("widget_axis", u"Form", None))
        self.label_7.setText(QCoreApplication.translate("widget_axis", u"<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">Set position and rotation.</span></p><p>Modes that are &quot;<span style=\" font-weight:600;\">fixed</span>&quot; will not move when solving statics</p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("widget_axis", u"X-rotation [deg]", None))
        self.checkBox_3.setText(QCoreApplication.translate("widget_axis", u"Fixed", None))
        self.label_6.setText(QCoreApplication.translate("widget_axis", u"Z-rotation [deg]", None))
        self.label_3.setText(QCoreApplication.translate("widget_axis", u"Z - translation [m]", None))
        self.pbToggleAllFixes.setText(QCoreApplication.translate("widget_axis", u"toggle all", None))
        self.checkBox_4.setText(QCoreApplication.translate("widget_axis", u"Fixed", None))
        self.checkBox_5.setText(QCoreApplication.translate("widget_axis", u"Fixed", None))
        self.checkBox_6.setText(QCoreApplication.translate("widget_axis", u"Fixed", None))
        self.label_2.setText(QCoreApplication.translate("widget_axis", u"Y - translation [m]", None))
#if QT_CONFIG(tooltip)
        self.toolButton.setToolTip(QCoreApplication.translate("widget_axis", u"<html><head/><body><p><span style=\" font-weight:600;\">Definition:</span></p><p>Rotation is defined as a rotation about a single axis.</p><p>- The axis of rotation is defined by the X,Y and Z components of the rotation.</p><p>- The angle or rotation is defined by the length of the rotation vector.</p><p><span style=\" font-weight:600;\"><br/>Examples:</span></p><p>x=0, y=0, z=90 ---&gt; 90 degees Rotation about Z-axis</p><p>x=10, y= 10, z= 0 --&gt; Axis of rotation is (1,1,0) and rotation angle |(10,10,0)| = sqrt(200)</p><p>x=Free, y =0, z= 0 --&gt; Axis system is free to rotate about the x-axis</p><p>x=Free, y = Free, z=0 --&gt; Axis system is free to rotate about any axis with z=0. The effect of this is hard to visualize.</p><p><br/></p><p><span style=\" font-weight:600;\">Tips:</span></p><p>To define subsequent rotations about different axis it is often more convenient to stack axis-nodes on top of eachother. For example to model a rotation of 20 degrees about the z-axis (yaw) and rotation of 5 degrees abo"
                        "ut the y-axis (pitch) simply consider the following:</p><p>1. Create an axis system for the yaw. Set the rotation to (0,0,20)</p><p>2. Create a second axis system and place it under yaw. Set the rotation of this axis system to (0,5,0).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton.setText(QCoreApplication.translate("widget_axis", u"help on rotations ", None))
        self.checkBox_1.setText(QCoreApplication.translate("widget_axis", u"Fixed", None))
        self.label_5.setText(QCoreApplication.translate("widget_axis", u"Y-rotation [deg]", None))
        self.label.setText(QCoreApplication.translate("widget_axis", u"X - translation [m]", None))
        self.checkBox_2.setText(QCoreApplication.translate("widget_axis", u"Fixed", None))
        self.lblRotationsWarning.setText(QCoreApplication.translate("widget_axis", u"<html><head/><body><p><span style=\" font-weight:700;\">WARNING</span></p><p>This combination of rotations is not recommended. <a href=\"https://usedave.nl/rotations_in_3d.html\"><span style=\" text-decoration: underline; color:#0000ff;\">Click here for more information.</span></a></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("widget_axis", u"These rotations and positions are defined relative to the parent. If parent is empty then the global axis system is used.", None))
        self.label_8.setText(QCoreApplication.translate("widget_axis", u"Parent", None))
    # retranslateUi

