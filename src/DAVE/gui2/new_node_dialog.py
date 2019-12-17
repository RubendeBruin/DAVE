"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019



  Interface between the gui and and the element-widgets


"""



import DAVE.gui2.forms.addnode_form

import DAVE.scene as vfs
from PySide2.QtGui import QIcon

from PySide2 import QtWidgets


def fill_dropdown_boxes(ui, scene):
    a = list()
    p = list()
    for e in scene.nodes_of_type(vfs.Axis):
        a.append(e.name)
    for e in scene.nodes_of_type(vfs.Poi):
        p.append(e.name)

    ui.cbMasterAxis.addItems(a)
    ui.cbSlaveAxis.addItems(a)
    ui.cbPoiA.addItems(p)
    ui.cbPoiB.addItems(p)
    ui.cbParentPoi.addItems(p)
    if len(p) > 1:
        ui.cbPoiB.setCurrentText(p[1])

    ui.cbParentAxis.addItems([""])
    ui.cbParentAxis.addItems(a)


def add_node(scene):
    AddNode = QtWidgets.QDialog()
    ui = DAVE.gui2.forms.addnode_form.Ui_Dialog()
    ui.setupUi(AddNode)

    ui.frmMasterSlave.setVisible(False)
    ui.frmPoints.setVisible(False)
    ui.frmParent.setVisible(False)
    ui.frmParentPoi.setVisible(False)

    fill_dropdown_boxes(ui, scene)

    # AddNode.setFixedHeight(250)

    ui.errPois.setVisible(False)
    ui.errUniqueName.setVisible(False)

    def ok():
        if ui.frmPoints.isVisible():
            if ui.cbPoiA.currentText() == ui.cbPoiB.currentText():
                ui.errPois.setVisible(True)
            else:
                ui.errPois.setVisible(False)
        ui.btnOk.setEnabled((not ui.errPois.isVisible()) and (not ui.errUniqueName.isVisible()))

    def ok_name():
        ui.errUniqueName.setVisible(not scene.name_available(ui.tbName.text()))
        ui.btnOk.setEnabled((not ui.errPois.isVisible()) and (not ui.errUniqueName.isVisible()))

    ui.cbPoiA.currentTextChanged.connect(ok)
    ui.cbPoiB.currentTextChanged.connect(ok)
    ui.tbName.textChanged.connect(ok_name)

    def cancel():
        AddNode.reject()

    ui.buttonBox.clicked.connect(cancel)

    return ui, AddNode


def add_axis(scene, parent=None):

    ui, AddNode = add_node(scene)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/axis.png"))

    if parent:
        ui.cbParentAxis.setCurrentText(parent[0].name)

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Axis'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()
        if parent:
            return "new_axis('{}', parent = '{}')".format(name, parent)
        else:
            return "new_axis('{}')".format(name)
    else:
        return None

def add_body(scene, parent=None):

    ui, AddNode = add_node(scene)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/rigidbody.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Body'))

    if parent:
        ui.cbParentAxis.setCurrentText(parent[0].name)

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()
        if parent:
            return "new_rigidbody('{}', parent = '{}')".format(name, parent)
        else:
            return "new_rigidbody('{}')".format(name)
    else:
        return None

def add_poi(scene, parent = None):

    ui, AddNode = add_node(scene)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/poi.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Poi'))

    if parent:
        ui.cbParentAxis.setCurrentText(parent[0].name)

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()
        if parent:
            return "new_poi('{}', parent = '{}')".format(name, parent)
        else:
            return "new_poi('{}')".format(name)
    else:
        return None


def add_cable(scene, parent = None):

    ui, AddNode = add_node(scene)

    ui.frmPoints.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/cable.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Cable'))

    if parent:
        ui.cbPoiA.setCurrentText(parent[0].name)
        try:
            ui.cbPoiB.setCurrentText(parent[1].name)
        except:
            pass

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        poiA = ui.cbPoiA.currentText()
        poiB = ui.cbPoiB.currentText()
        name = ui.tbName.text()

        return "new_cable('{}', poiA = '{}', poiB= '{}')".format(name, poiA, poiB)

    else:
        return None

def add_force(scene, parent = None):

    ui, AddNode = add_node(scene)

    ui.frmParentPoi.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/force.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Force'))

    if parent:
        ui.cbParentAxis.setCurrentText(parent[0].name)

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        poi = ui.cbParentPoi.currentText()
        name = ui.tbName.text()

        return "new_force('{}', parent = '{}')".format(name, poi)

    else:
        return None
    
def add_sheave(scene, parent = None):

    ui, AddNode = add_node(scene)

    ui.frmParentPoi.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/sheave.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Sheave'))

    if parent:
        ui.cbParentAxis.setCurrentText(parent[0].name)

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        poi = ui.cbParentPoi.currentText()
        name = ui.tbName.text()

        return "new_sheave('{}', parent = '{}', axis = (0,1,0))".format(name, poi)

    else:
        return None

def add_linear_connector(scene, parent = None):

    ui, AddNode = add_node(scene)

    ui.frmMasterSlave.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/lincon6.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('LinCon6d'))

    if parent:
        ui.cbMasterAxis.setCurrentText(parent[0].name)
        try:
            ui.cbSlaveAxis.setCurrentText(parent[1].name)
        except:
            pass

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        master = ui.cbMasterAxis.currentText()
        slave = ui.cbSlaveAxis.currentText()
        name = ui.tbName.text()

        return "new_linear_connector_6d('{}', slave = '{}', master = '{}')".format(name, slave, master)

    else:
        return None


def add_connector2d(scene, parent = None):

    ui, AddNode = add_node(scene)

    ui.frmMasterSlave.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/con2d.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Connector2d'))

    if parent:
        ui.cbMasterAxis.setCurrentText(parent[0].name)
        try:
            ui.cbSlaveAxis.setCurrentText(parent[1].name)
        except:
            pass

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        master = ui.cbMasterAxis.currentText()
        slave = ui.cbSlaveAxis.currentText()
        name = ui.tbName.text()

        return "new_connector2d('{}', slave = '{}', master = '{}')".format(name, slave, master)

    else:
        return None

def add_beam_connector(scene, parent = None):

    ui, AddNode = add_node(scene)

    ui.frmMasterSlave.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/beam.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Beam'))

    if parent:
        ui.cbMasterAxis.setCurrentText(parent[0].name)
        try:
            ui.cbSlaveAxis.setCurrentText(parent[1].name)
        except:
            pass

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        master = ui.cbMasterAxis.currentText()
        slave = ui.cbSlaveAxis.currentText()
        name = ui.tbName.text()

        return "new_linear_beam('{}', slave = '{}', master = '{}')".format(name, slave, master)

    else:
        return None


def add_linear_hydrostatics(scene, parent = None):

    ui, AddNode = add_node(scene)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/linhyd.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Hydrostatics'))

    if parent:
        ui.cbParentAxis.setCurrentText(parent[0].name)

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()

        return "new_hydspring('{}', parent = '{}', cob = (0,0,0), BMT=0, BML=0, COFX=0, COFY=0, kHeave=0, waterline=0, displacement_kN=0)".format(name, parent)

    else:
        return None

def add_visual(scene, parent = None):
    ui, AddNode = add_node(scene)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/visual.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Visual'))

    if parent:
        ui.cbParentAxis.setCurrentText(parent[0].name)

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()

        return "new_visual('{}', parent = '{}', path = r'wirecube.obj')".format(
            name, parent)

    else:
        return None

def add_buoyancy(scene, parent = None):
    ui, AddNode = add_node(scene)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/buoy_mesh.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Buoyancy mesh'))

    if parent:
        ui.cbParentAxis.setCurrentText(parent[0].name)

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()

        return "new_buoyancy('{}', parent = '{}')".format(name, parent)

    else:
        return None



def add_waveinteraction(scene, parent = None):
    ui, AddNode = add_node(scene)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/waveinteraction.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('WaveInteraction'))

    if parent:
        ui.cbParentAxis.setCurrentText(parent[0].name)

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()

        return "new_waveinteraction('{}', parent = '{}', path = r'barge_100_30_5.dhyd')".format(
            name, parent)

    else:
        return None




