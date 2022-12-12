# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menu_nodetypes.ui'
##
## Created by: Qt User Interface Compiler version 5.15.6
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

# import resources_rc

class Ui_MenuNodes(object):
    def setupUi(self, MenuNodes):
        if not MenuNodes.objectName():
            MenuNodes.setObjectName(u"MenuNodes")
        MenuNodes.resize(446, 266)
        self.gridLayout = QGridLayout(MenuNodes)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget_2 = QWidget(MenuNodes)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_2.setFont(font)

        self.verticalLayout_2.addWidget(self.label_2)

        self.pbForce = QPushButton(self.widget_2)
        self.pbForce.setObjectName(u"pbForce")
        icon = QIcon()
        icon.addFile(u":/icons/force.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbForce.setIcon(icon)
        self.pbForce.setFlat(True)

        self.verticalLayout_2.addWidget(self.pbForce)

        self.pbWindArea = QPushButton(self.widget_2)
        self.pbWindArea.setObjectName(u"pbWindArea")
        self.pbWindArea.setStyleSheet(u"text-align:left")
        icon1 = QIcon()
        icon1.addFile(u":/icons/wind.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbWindArea.setIcon(icon1)
        self.pbWindArea.setFlat(True)

        self.verticalLayout_2.addWidget(self.pbWindArea)

        self.pbCurrentArea = QPushButton(self.widget_2)
        self.pbCurrentArea.setObjectName(u"pbCurrentArea")
        self.pbCurrentArea.setStyleSheet(u"text-align:left")
        icon2 = QIcon()
        icon2.addFile(u":/icons/current.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbCurrentArea.setIcon(icon2)
        self.pbCurrentArea.setFlat(True)

        self.verticalLayout_2.addWidget(self.pbCurrentArea)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)


        self.gridLayout.addWidget(self.widget_2, 0, 4, 1, 1)

        self.widget = QWidget(MenuNodes)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.pbAxis = QPushButton(self.widget)
        self.pbAxis.setObjectName(u"pbAxis")
        icon3 = QIcon()
        icon3.addFile(u":/icons/axis_blue.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbAxis.setIcon(icon3)
        self.pbAxis.setFlat(True)

        self.verticalLayout.addWidget(self.pbAxis)

        self.pbPoint = QPushButton(self.widget)
        self.pbPoint.setObjectName(u"pbPoint")
        icon4 = QIcon()
        icon4.addFile(u":/icons/point_blue.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbPoint.setIcon(icon4)
        self.pbPoint.setFlat(True)

        self.verticalLayout.addWidget(self.pbPoint)

        self.pbCircle = QPushButton(self.widget)
        self.pbCircle.setObjectName(u"pbCircle")
        icon5 = QIcon()
        icon5.addFile(u":/icons/circle_blue.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbCircle.setIcon(icon5)
        self.pbCircle.setFlat(True)

        self.verticalLayout.addWidget(self.pbCircle)

        self.pbBody = QPushButton(self.widget)
        self.pbBody.setObjectName(u"pbBody")
        icon6 = QIcon()
        icon6.addFile(u":/icons/cube.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbBody.setIcon(icon6)
        self.pbBody.setFlat(True)

        self.verticalLayout.addWidget(self.pbBody)

        self.pbGeometricContact = QPushButton(self.widget)
        self.pbGeometricContact.setObjectName(u"pbGeometricContact")
        icon7 = QIcon()
        icon7.addFile(u":/icons/pin_hole.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbGeometricContact.setIcon(icon7)
        self.pbGeometricContact.setFlat(True)

        self.verticalLayout.addWidget(self.pbGeometricContact)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.widget_5 = QWidget(MenuNodes)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_5 = QVBoxLayout(self.widget_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_5 = QLabel(self.widget_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.verticalLayout_5.addWidget(self.label_5)

        self.pbContactShape = QPushButton(self.widget_5)
        self.pbContactShape.setObjectName(u"pbContactShape")
        self.pbContactShape.setStyleSheet(u"text-align:left")
        icon8 = QIcon()
        icon8.addFile(u":/icons/trimesh.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbContactShape.setIcon(icon8)
        self.pbContactShape.setFlat(True)

        self.verticalLayout_5.addWidget(self.pbContactShape)

        self.pbContactBall = QPushButton(self.widget_5)
        self.pbContactBall.setObjectName(u"pbContactBall")
        icon9 = QIcon()
        icon9.addFile(u":/icons/contactball.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbContactBall.setIcon(icon9)
        self.pbContactBall.setFlat(True)

        self.verticalLayout_5.addWidget(self.pbContactBall)

        self.pbSPMT = QPushButton(self.widget_5)
        self.pbSPMT.setObjectName(u"pbSPMT")
        icon10 = QIcon()
        icon10.addFile(u":/icons/spmt.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbSPMT.setIcon(icon10)
        self.pbSPMT.setFlat(True)

        self.verticalLayout_5.addWidget(self.pbSPMT)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)


        self.gridLayout.addWidget(self.widget_5, 0, 6, 1, 1)

        self.widget_4 = QWidget(MenuNodes)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_4 = QVBoxLayout(self.widget_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.widget_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.verticalLayout_4.addWidget(self.label_4)

        self.pbTank = QPushButton(self.widget_4)
        self.pbTank.setObjectName(u"pbTank")
        self.pbTank.setStyleSheet(u"text-align:left")
        icon11 = QIcon()
        icon11.addFile(u":/icons/tank.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbTank.setIcon(icon11)
        self.pbTank.setFlat(True)

        self.verticalLayout_4.addWidget(self.pbTank)

        self.pbBuoyancyShape = QPushButton(self.widget_4)
        self.pbBuoyancyShape.setObjectName(u"pbBuoyancyShape")
        icon12 = QIcon()
        icon12.addFile(u":/icons/buoy_mesh.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbBuoyancyShape.setIcon(icon12)
        self.pbBuoyancyShape.setFlat(True)

        self.verticalLayout_4.addWidget(self.pbBuoyancyShape)

        self.pbLinearBuoyancy = QPushButton(self.widget_4)
        self.pbLinearBuoyancy.setObjectName(u"pbLinearBuoyancy")
        icon13 = QIcon()
        icon13.addFile(u":/icons/linhyd.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbLinearBuoyancy.setIcon(icon13)
        self.pbLinearBuoyancy.setFlat(True)

        self.verticalLayout_4.addWidget(self.pbLinearBuoyancy)

        self.pbWaveInteraction = QPushButton(self.widget_4)
        self.pbWaveInteraction.setObjectName(u"pbWaveInteraction")
        icon14 = QIcon()
        icon14.addFile(u":/icons/waveinteraction.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbWaveInteraction.setIcon(icon14)
        self.pbWaveInteraction.setFlat(True)

        self.verticalLayout_4.addWidget(self.pbWaveInteraction)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_6)


        self.gridLayout.addWidget(self.widget_4, 1, 0, 1, 1)

        self.widget_3 = QWidget(MenuNodes)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_3 = QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_3.addWidget(self.label_3)

        self.pbCable = QPushButton(self.widget_3)
        self.pbCable.setObjectName(u"pbCable")
        icon15 = QIcon()
        icon15.addFile(u":/icons/cable.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbCable.setIcon(icon15)
        self.pbCable.setFlat(True)

        self.verticalLayout_3.addWidget(self.pbCable)

        self.pbBeam = QPushButton(self.widget_3)
        self.pbBeam.setObjectName(u"pbBeam")
        icon16 = QIcon()
        icon16.addFile(u":/icons/beam.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbBeam.setIcon(icon16)
        self.pbBeam.setFlat(True)

        self.verticalLayout_3.addWidget(self.pbBeam)

        self.pbSling = QPushButton(self.widget_3)
        self.pbSling.setObjectName(u"pbSling")
        icon17 = QIcon()
        icon17.addFile(u":/icons/sling.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbSling.setIcon(icon17)
        self.pbSling.setFlat(True)

        self.verticalLayout_3.addWidget(self.pbSling)

        self.pbShackle = QPushButton(self.widget_3)
        self.pbShackle.setObjectName(u"pbShackle")
        icon18 = QIcon()
        icon18.addFile(u":/icons/circle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbShackle.setIcon(icon18)
        self.pbShackle.setFlat(True)

        self.verticalLayout_3.addWidget(self.pbShackle)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_7)


        self.gridLayout.addWidget(self.widget_3, 1, 1, 1, 1)

        self.widget_6 = QWidget(MenuNodes)
        self.widget_6.setObjectName(u"widget_6")
        self.verticalLayout_6 = QVBoxLayout(self.widget_6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_6 = QLabel(self.widget_6)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.verticalLayout_6.addWidget(self.label_6)

        self.pbSpring2D = QPushButton(self.widget_6)
        self.pbSpring2D.setObjectName(u"pbSpring2D")
        self.pbSpring2D.setStyleSheet(u"text-align:left")
        icon19 = QIcon()
        icon19.addFile(u":/icons/con2d.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbSpring2D.setIcon(icon19)
        self.pbSpring2D.setFlat(True)

        self.verticalLayout_6.addWidget(self.pbSpring2D)

        self.pbSpring6D = QPushButton(self.widget_6)
        self.pbSpring6D.setObjectName(u"pbSpring6D")
        icon20 = QIcon()
        icon20.addFile(u":/icons/lincon6.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbSpring6D.setIcon(icon20)
        self.pbSpring6D.setFlat(True)

        self.verticalLayout_6.addWidget(self.pbSpring6D)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)


        self.gridLayout.addWidget(self.widget_6, 0, 1, 1, 1)

        self.widget_8 = QWidget(MenuNodes)
        self.widget_8.setObjectName(u"widget_8")
        self.verticalLayout_8 = QVBoxLayout(self.widget_8)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_8 = QLabel(self.widget_8)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.verticalLayout_8.addWidget(self.label_8)

        self.pbComponent = QPushButton(self.widget_8)
        self.pbComponent.setObjectName(u"pbComponent")
        icon21 = QIcon()
        icon21.addFile(u":/icons/component.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbComponent.setIcon(icon21)
        self.pbComponent.setFlat(True)

        self.verticalLayout_8.addWidget(self.pbComponent)

        self.verticalSpacer_8 = QSpacerItem(20, 63, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_8)


        self.gridLayout.addWidget(self.widget_8, 1, 6, 1, 1)

        self.widget_7 = QWidget(MenuNodes)
        self.widget_7.setObjectName(u"widget_7")
        self.verticalLayout_7 = QVBoxLayout(self.widget_7)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_7 = QLabel(self.widget_7)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.verticalLayout_7.addWidget(self.label_7)

        self.pbVisual = QPushButton(self.widget_7)
        self.pbVisual.setObjectName(u"pbVisual")
        self.pbVisual.setStyleSheet(u"text-align:left")
        icon22 = QIcon()
        icon22.addFile(u":/icons/visual.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pbVisual.setIcon(icon22)
        self.pbVisual.setFlat(True)

        self.verticalLayout_7.addWidget(self.pbVisual)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_5)


        self.gridLayout.addWidget(self.widget_7, 1, 4, 1, 1)


        self.retranslateUi(MenuNodes)

        self.pbAxis.setDefault(True)


        QMetaObject.connectSlotsByName(MenuNodes)
    # setupUi

    def retranslateUi(self, MenuNodes):
        MenuNodes.setWindowTitle(QCoreApplication.translate("MenuNodes", u"Form", None))
        self.widget_2.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_2.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_2.setText(QCoreApplication.translate("MenuNodes", u"Loads", None))
        self.pbForce.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbForce.setText(QCoreApplication.translate("MenuNodes", u"Force", None))
        self.pbWindArea.setText(QCoreApplication.translate("MenuNodes", u"Wind area", None))
        self.pbCurrentArea.setText(QCoreApplication.translate("MenuNodes", u"Current area", None))
        self.widget.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label.setText(QCoreApplication.translate("MenuNodes", u"Geometry", None))
        self.pbAxis.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbAxis.setText(QCoreApplication.translate("MenuNodes", u"Frame", None))
        self.pbPoint.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbPoint.setText(QCoreApplication.translate("MenuNodes", u"&Point", None))
        self.pbCircle.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbCircle.setText(QCoreApplication.translate("MenuNodes", u"&Circle", None))
        self.pbBody.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbBody.setText(QCoreApplication.translate("MenuNodes", u"&Body", None))
        self.pbGeometricContact.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbGeometricContact.setText(QCoreApplication.translate("MenuNodes", u"G&eometric contact", None))
        self.widget_5.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_5.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_5.setText(QCoreApplication.translate("MenuNodes", u"Elastic Contact", None))
        self.pbContactShape.setText(QCoreApplication.translate("MenuNodes", u"Contact Shape", None))
        self.pbContactBall.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbContactBall.setText(QCoreApplication.translate("MenuNodes", u"Contact Ball", None))
        self.pbSPMT.setText(QCoreApplication.translate("MenuNodes", u"SPMT susp. group", None))
        self.widget_4.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_4.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_4.setText(QCoreApplication.translate("MenuNodes", u"Fluid", None))
        self.pbTank.setText(QCoreApplication.translate("MenuNodes", u"Tank", None))
        self.pbBuoyancyShape.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbBuoyancyShape.setText(QCoreApplication.translate("MenuNodes", u"Buoyancy shape", None))
        self.pbLinearBuoyancy.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbLinearBuoyancy.setText(QCoreApplication.translate("MenuNodes", u"Linear buoyancy", None))
        self.pbWaveInteraction.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbWaveInteraction.setText(QCoreApplication.translate("MenuNodes", u"Wave interaction", None))
        self.widget_3.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_3.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_3.setText(QCoreApplication.translate("MenuNodes", u"Steel", None))
        self.pbCable.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbCable.setText(QCoreApplication.translate("MenuNodes", u"Cable", None))
        self.pbBeam.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbBeam.setText(QCoreApplication.translate("MenuNodes", u"Beam", None))
        self.pbSling.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbSling.setText(QCoreApplication.translate("MenuNodes", u"Sling", None))
        self.pbShackle.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbShackle.setText(QCoreApplication.translate("MenuNodes", u"Shackle", None))
        self.widget_6.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_6.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_6.setText(QCoreApplication.translate("MenuNodes", u"Springs", None))
        self.pbSpring2D.setText(QCoreApplication.translate("MenuNodes", u"&2D spring", None))
        self.pbSpring6D.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbSpring6D.setText(QCoreApplication.translate("MenuNodes", u"&6D spring", None))
        self.label_8.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_8.setText(QCoreApplication.translate("MenuNodes", u"Assets", None))
        self.pbComponent.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.pbComponent.setText(QCoreApplication.translate("MenuNodes", u"Component", None))
        self.widget_7.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_7.setStyleSheet(QCoreApplication.translate("MenuNodes", u"text-align:left", None))
        self.label_7.setText(QCoreApplication.translate("MenuNodes", u"Beauty", None))
        self.pbVisual.setText(QCoreApplication.translate("MenuNodes", u"Visual", None))
    # retranslateUi

