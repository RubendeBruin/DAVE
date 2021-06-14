"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019



  Interface between the gui and and the element-widgets


"""



import DAVE.gui.forms.addnode_form

import DAVE.scene as vfs
from PySide2.QtGui import QIcon

from PySide2 import QtWidgets


def fill_dropdown_boxes(ui, scene, selection=None):
    a = list()
    p = list()
    for e in scene.nodes_of_type(vfs.Axis):
        a.append(e.name)
    for e in scene.nodes_of_type((vfs.Point, vfs.Circle)):
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

    # see if we can do something with the selection
    if selection:
        node = selection[0]
        if isinstance(node, (vfs.Point, vfs.Circle)):
            ui.cbPoiA.setCurrentText(node.name)
            ui.cbParentPoi.setCurrentText(node.name)
        if isinstance(node, vfs.Axis):
            ui.cbMasterAxis.setCurrentText(node.name)
            ui.cbParentAxis.setCurrentText(node.name)

        if len(selection) > 1:
            node = selection[1]
            if isinstance(node, (vfs.Point, vfs.Circle)):
                ui.cbPoiB.setCurrentText(node.name)
                ui.cbParentPoi.setCurrentText(node.name)
            if isinstance(node, vfs.Axis):
                ui.cbSlaveAxis.setCurrentText(node.name)
                ui.cbParentAxis.setCurrentText(node.name)




def add_node(scene, selection = None):
    AddNode = QtWidgets.QDialog()
    ui = DAVE.gui.forms.addnode_form.Ui_Dialog()
    ui.setupUi(AddNode)

    ui.frmMasterSlave.setVisible(False)
    ui.frmPoints.setVisible(False)
    ui.frmParent.setVisible(False)
    ui.frmParentPoi.setVisible(False)

    fill_dropdown_boxes(ui, scene, selection)

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


def add_axis(scene, selection=None):

    ui, AddNode = add_node(scene, selection)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/axis.png"))


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

def add_body(scene, selection=None):

    ui, AddNode = add_node(scene,selection)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/rigidbody.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Body'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()
        if parent:
            return "new_rigidbody('{}', parent = '{}')".format(name, parent)
        else:
            return "new_rigidbody('{}')".format(name)
    else:
        return None

def add_poi(scene, selection=None):

    ui, AddNode = add_node(scene, selection)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/poi.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Point'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()
        if parent:
            return "new_point('{}', parent = '{}')".format(name, parent)
        else:
            return "new_point('{}')".format(name)
    else:
        return None


def add_cable(scene, selection=None):

    ui, AddNode = add_node(scene,selection)

    ui.frmPoints.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/cable.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Cable'))



    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        endA = ui.cbPoiA.currentText()
        endB = ui.cbPoiB.currentText()
        name = ui.tbName.text()

        return "new_cable('{}', endA = '{}', endB= '{}')".format(name, endA, endB)

    else:
        return None

def add_force(scene, selection=None):

    ui, AddNode = add_node(scene,selection)

    ui.frmParentPoi.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/force.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Force'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        poi = ui.cbParentPoi.currentText()
        name = ui.tbName.text()

        return "new_force('{}', parent = '{}')".format(name, poi)

    else:
        return None


def add_contactball(scene, selection=None):

    ui, AddNode = add_node(scene,selection)

    ui.frmParentPoi.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/contactball.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Contactball'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        poi = ui.cbParentPoi.currentText()
        name = ui.tbName.text()

        return "new_contactball('{}', parent = '{}')".format(name, poi)

    else:
        return None



def add_sheave(scene, selection=None):

    ui, AddNode = add_node(scene,selection)

    ui.frmParentPoi.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/sheave.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Circle'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        poi = ui.cbParentPoi.currentText()
        name = ui.tbName.text()

        return "new_circle('{}', parent = '{}', axis = (0,1,0))".format(name, poi)

    else:
        return None

def add_linear_connector(scene, selection=None):

    ui, AddNode = add_node(scene, selection)

    ui.frmMasterSlave.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/lincon6.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('LinCon6d'))


    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        master = ui.cbMasterAxis.currentText()
        slave = ui.cbSlaveAxis.currentText()
        name = ui.tbName.text()

        return "new_linear_connector_6d('{}', main = '{}', secondary = '{}')".format(name, slave, master)

    else:
        return None


def add_connector2d(scene, selection=None):

    ui, AddNode = add_node(scene,selection)

    ui.frmMasterSlave.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/con2d.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Connector2d'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        master = ui.cbMasterAxis.currentText()
        slave = ui.cbSlaveAxis.currentText()
        name = ui.tbName.text()

        return "new_connector2d('{}', nodeB = '{}', nodeA = '{}')".format(name, slave, master)

    else:
        return None

def add_beam_connector(scene, selection=None):

    ui, AddNode = add_node(scene,selection)

    ui.frmMasterSlave.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/beam.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Beam'))


    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        master = ui.cbMasterAxis.currentText()
        slave = ui.cbSlaveAxis.currentText()
        name = ui.tbName.text()

        return "new_beam('{}', nodeB = '{}', nodeA = '{}')".format(name, slave, master)

    else:
        return None


def add_linear_hydrostatics(scene, selection=None):

    ui, AddNode = add_node(scene,selection)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/linhyd.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Hydrostatics'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()

        return "new_hydspring('{}', parent = '{}', cob = (0,0,0), BMT=0, BML=0, COFX=0, COFY=0, kHeave=0, waterline=0, displacement_kN=0)".format(name, parent)

    else:
        return None

def add_visual(scene, selection=None):
    ui, AddNode = add_node(scene,selection)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/visual.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Visual'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()

        return "new_visual('{}', parent = '{}', path = r'wirecube.obj')".format(
            name, parent)

    else:
        return None

def add_buoyancy(scene, selection=None):
    ui, AddNode = add_node(scene,selection)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/buoy_mesh.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Buoyancy mesh'))



    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()

        return "new_buoyancy('{}', parent = '{}')".format(name, parent)

    else:
        return None

def add_tank(scene, selection=None):
    ui, AddNode = add_node(scene,selection)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/tank.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Tank'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()

        return "new_tank('{}', parent = '{}')".format(name, parent)

    else:
        return None


def add_contactmesh(scene, selection=None):
    ui, AddNode = add_node(scene,selection)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/contact_mesh.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Contactmesh'))



    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()

        if parent:
            return "new_contactmesh('{}', parent = '{}')".format(name, parent)
        else:
            return "new_contactmesh('{}')".format(name)


    else:
        return None


def add_waveinteraction(scene, selection=None):
    ui, AddNode = add_node(scene,selection)

    ui.frmParent.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/waveinteraction.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('WaveInteraction'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        parent = ui.cbParentAxis.currentText()
        name = ui.tbName.text()

        return "new_waveinteraction('{}', parent = '{}', path = '')".format(
            name, parent)

    else:
        return None

def add_shackle(scene, selection=None):
    ui, AddNode = add_node(scene,selection)
    ui.btnOk.setIcon(QIcon(":/icons/shackle.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Shackle'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        name = ui.tbName.text()
        return f"new_shackle('{name}')"

    else:
        return None


def add_sling(scene, selection=None):

    ui, AddNode = add_node(scene,selection)

    ui.frmPoints.setVisible(True)
    ui.btnOk.setIcon(QIcon(":/icons/sling.png"))

    def ok():
        AddNode.accept()

    ui.btnOk.clicked.connect(ok)
    ui.tbName.setText(scene.available_name_like('Sling'))

    if (AddNode.exec() == QtWidgets.QDialog.Accepted):
        endA = ui.cbPoiA.currentText()
        endB = ui.cbPoiB.currentText()
        name = ui.tbName.text()

        return "new_sling('{}', endA = '{}', endB= '{}')".format(name, endA, endB)

    else:
        return None

