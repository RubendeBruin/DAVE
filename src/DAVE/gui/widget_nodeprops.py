from DAVE.gui.dockwidget import *
import DAVE.scene as vfs

import DAVE.gui.forms.widget_axis
import DAVE.gui.forms.widget_body
import DAVE.gui.forms.widget_poi
import DAVE.gui.forms.widget_cable
import DAVE.gui.forms.widget_name
import DAVE.gui.forms.widget_visual
import DAVE.gui.forms.widget_force
import DAVE.gui.forms.widget_lincon6
import DAVE.gui.forms.widget_linhyd
import DAVE.gui.forms.widget_beam
import DAVE.gui.forms.widget_con2d
import DAVE.gui.forms.widget_sheave
import DAVE.gui.forms.widget_waveinteraction
import DAVE.gui.forms.widget_contactball
import DAVE.gui.forms.widget_geometricconnection
import DAVE.gui.forms.widget_sling
import DAVE.gui.forms.widget_tank
import DAVE.gui.forms.widget_buoyancy
import DAVE.gui.forms.widget_shackle

import numpy as np

from PySide2.QtWidgets import QListWidgetItem
from PySide2 import QtWidgets


class NodeEditor:
    """NodeEditor implements a "singleton" instance of NodeEditor-derived widget.

    This widget is shown in target_layout, which is a QtLayout

    properties:
    - node : the node being edited
    - callback : a callback function being called when python code need to be executed

    A create_widget() method shall be implemented. This function creates the widget and returns it. When th

    """


    def __init__(self, node, callback, scene, run_code):
        self.node = node
        self.callback = callback
        self.scene = scene
        self.run_code = run_code


    def create_widget(self):
        """Creates and returns the widget"""
        raise Exception('create_widget() method not defined in derived class')

    def post_update_event(self):
        """Is executed after running the generated code"""
        pass




class EditNode(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditNode._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_name.Ui_NameWidget()
            ui.setupUi(widget)
            EditNode._ui = ui
            ui._widget = widget

        else:
            ui = EditNode._ui

        try:
            ui.tbName.textChanged.disconnect()
            ui.cbVisible.toggled.disconnect()
        except:
            pass # no connections yet

        ui.tbName.setText(self.node.name)
        ui.cbVisible.setChecked(self.node.visible)

        ui.tbName.textChanged.connect(self.callback)
        ui.cbVisible.toggled.connect(self.callback)

        self.ui = ui

        return ui._widget



class EditAxis(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditAxis._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_axis.Ui_widget_axis()
            ui.setupUi(widget)
            EditAxis._ui = ui
            ui._widget = widget

        else:
            ui = EditAxis._ui

        self.ui = ui
        self.post_update_event()

        return ui._widget

    def post_update_event(self):
        try:
            self.ui.checkBox_1.stateChanged.disconnect()
            self.ui.checkBox_2.stateChanged.disconnect()
            self.ui.checkBox_3.stateChanged.disconnect()
            self.ui.checkBox_4.stateChanged.disconnect()
            self.ui.checkBox_5.stateChanged.disconnect()
            self.ui.checkBox_6.stateChanged.disconnect()

            self.ui.doubleSpinBox_1.valueChanged.disconnect()
            self.ui.doubleSpinBox_2.valueChanged.disconnect()
            self.ui.doubleSpinBox_3.valueChanged.disconnect()
            self.ui.doubleSpinBox_4.valueChanged.disconnect()
            self.ui.doubleSpinBox_5.valueChanged.disconnect()
            self.ui.doubleSpinBox_6.valueChanged.disconnect()
        except:
            pass # no connections yet

        self.ui.doubleSpinBox_1.setValue(self.node.position[0])
        self.ui.doubleSpinBox_2.setValue(self.node.position[1])
        self.ui.doubleSpinBox_3.setValue(self.node.position[2])

        self.ui.doubleSpinBox_4.setValue(self.node.rotation[0])
        self.ui.doubleSpinBox_5.setValue(self.node.rotation[1])
        self.ui.doubleSpinBox_6.setValue(self.node.rotation[2])

        self.ui.checkBox_1.setChecked(self.node.fixed[0])
        self.ui.checkBox_2.setChecked(self.node.fixed[1])
        self.ui.checkBox_3.setChecked(self.node.fixed[2])
        self.ui.checkBox_4.setChecked(self.node.fixed[3])
        self.ui.checkBox_5.setChecked(self.node.fixed[4])
        self.ui.checkBox_6.setChecked(self.node.fixed[5])

        self.ui.checkBox_1.stateChanged.connect(self.callback)
        self.ui.checkBox_2.stateChanged.connect(self.callback)
        self.ui.checkBox_3.stateChanged.connect(self.callback)
        self.ui.checkBox_4.stateChanged.connect(self.callback)
        self.ui.checkBox_5.stateChanged.connect(self.callback)
        self.ui.checkBox_6.stateChanged.connect(self.callback)

        self.ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        self.ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        self.ui.doubleSpinBox_3.valueChanged.connect(self.callback)
        self.ui.doubleSpinBox_4.valueChanged.connect(self.callback)
        self.ui.doubleSpinBox_5.valueChanged.connect(self.callback)
        self.ui.doubleSpinBox_6.valueChanged.connect(self.callback)

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_position = np.array((self.ui.doubleSpinBox_1.value(), self.ui.doubleSpinBox_2.value(),self.ui.doubleSpinBox_3.value()))
        new_rotation = np.array((self.ui.doubleSpinBox_4.value(), self.ui.doubleSpinBox_5.value(),self.ui.doubleSpinBox_6.value()))
        new_fixed = np.array((self.ui.checkBox_1.isChecked(),
                              self.ui.checkBox_2.isChecked(),
                              self.ui.checkBox_3.isChecked(),
                              self.ui.checkBox_4.isChecked(),
                              self.ui.checkBox_5.isChecked(),
                              self.ui.checkBox_6.isChecked()))

        if not np.all(round3d(new_position) == round3d(self.node.position)):
            code += element + '.position = ({}, {}, {})'.format(*new_position)

        if not np.all(round3d(new_rotation) == round3d(self.node.rotation)):
            code += element + '.rotation = ({}, {}, {})'.format(*new_rotation)

        if not np.all(new_fixed == self.node.fixed):
            code += element + '.fixed = ({}, {}, {}, {}, {}, {})'.format(*new_fixed)

        return code


class EditVisual(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditVisual._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_visual.Ui_widget_axis()
            ui.setupUi(widget)
            ui.cbInvertNormals.setVisible(False)
            EditVisual._ui = ui
            ui._widget = widget

        else:
            ui = EditVisual._ui

        try:
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox_3.valueChanged.disconnect()
            ui.doubleSpinBox_4.valueChanged.disconnect()
            ui.doubleSpinBox_5.valueChanged.disconnect()
            ui.doubleSpinBox_6.valueChanged.disconnect()
            ui.doubleSpinBox_7.valueChanged.disconnect()
            ui.doubleSpinBox_8.valueChanged.disconnect()
            ui.doubleSpinBox_9.valueChanged.disconnect()


            ui.comboBox.editTextChanged.disconnect()
        except:
            pass # no connections yet

        ui.doubleSpinBox_1.setValue(self.node.offset[0])
        ui.doubleSpinBox_2.setValue(self.node.offset[1])
        ui.doubleSpinBox_3.setValue(self.node.offset[2])

        ui.doubleSpinBox_4.setValue(self.node.rotation[0])
        ui.doubleSpinBox_5.setValue(self.node.rotation[1])
        ui.doubleSpinBox_6.setValue(self.node.rotation[2])

        ui.doubleSpinBox_7.setValue(self.node.scale[0])
        ui.doubleSpinBox_8.setValue(self.node.scale[1])
        ui.doubleSpinBox_9.setValue(self.node.scale[2])

        ui.comboBox.clear()
        ui.comboBox.addItems(self.scene.get_resource_list('stl'))
        ui.comboBox.addItems(self.scene.get_resource_list('obj'))

        ui.comboBox.setCurrentText(str(self.node.path))

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox_3.valueChanged.connect(self.callback)
        ui.doubleSpinBox_4.valueChanged.connect(self.callback)
        ui.doubleSpinBox_5.valueChanged.connect(self.callback)
        ui.doubleSpinBox_6.valueChanged.connect(self.callback)
        ui.doubleSpinBox_7.valueChanged.connect(self.callback)
        ui.doubleSpinBox_8.valueChanged.connect(self.callback)
        ui.doubleSpinBox_9.valueChanged.connect(self.callback)

        ui.comboBox.editTextChanged.connect(self.callback)


        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_position = np.array((self.ui.doubleSpinBox_1.value(), self.ui.doubleSpinBox_2.value(),self.ui.doubleSpinBox_3.value()))
        new_rotation = np.array((self.ui.doubleSpinBox_4.value(), self.ui.doubleSpinBox_5.value(),self.ui.doubleSpinBox_6.value()))
        new_scale = np.array((self.ui.doubleSpinBox_7.value(), self.ui.doubleSpinBox_8.value(),self.ui.doubleSpinBox_9.value()))

        new_path = self.ui.comboBox.currentText()

        if not new_path == self.node.path:
            code += element + ".path = r'{}'".format(new_path)

        if not np.all(new_position == self.node.offset):
            code += element + '.offset = ({}, {}, {})'.format(*new_position)

        if not np.all(new_rotation == self.node.rotation):
            code += element + '.rotation = ({}, {}, {})'.format(*new_rotation)

        if not np.all(new_scale == self.node.scale):
            code += element + '.scale = ({}, {}, {})'.format(*new_scale)

        return code

class EditWaveInteraction(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditWaveInteraction._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_waveinteraction.Ui_widget_waveinteraction()
            ui.setupUi(widget)
            EditWaveInteraction._ui = ui
            ui._widget = widget

        else:
            ui = EditWaveInteraction._ui

        try:
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox_3.valueChanged.disconnect()
            ui.comboBox.editTextChanged.disconnect()
        except:
            pass # no connections yet

        ui.doubleSpinBox_1.setValue(self.node.offset[0])
        ui.doubleSpinBox_2.setValue(self.node.offset[1])
        ui.doubleSpinBox_3.setValue(self.node.offset[2])

        ui.comboBox.clear()
        ui.comboBox.addItems(self.scene.get_resource_list('dhyd'))

        ui.comboBox.setCurrentText(self.node.path)

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox_3.valueChanged.connect(self.callback)
        ui.comboBox.editTextChanged.connect(self.callback)

        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_position = np.array((self.ui.doubleSpinBox_1.value(), self.ui.doubleSpinBox_2.value(),self.ui.doubleSpinBox_3.value()))
        new_path = self.ui.comboBox.currentText()

        if not new_path == self.node.path:
            code += element + ".path = r'{}'".format(new_path)

        if not np.all(new_position == self.node.offset):
            code += element + '.offset = ({}, {}, {})'.format(*new_position)


        return code


# ======================================

class EditTank(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditTank._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_tank.Ui_Form()
            ui.setupUi(widget)
            EditLC6d._ui = ui
            ui._widget = widget

        else:
            ui = EditTank._ui

        self.ui = ui
        self.post_update_event() # update values

        return ui._widget

    def generate_code(self):

        new_density = self.ui.sbDenstiy.value()
        new_volume = self.ui.sbVolume.value()
        new_pct = self.ui.sbPercentage.value()
        new_elev = self.ui.sbElevation.value()
        new_free_flooding = self.ui.cbFreeFlooding.isChecked()
        # new_ht_pct = self.ui.sbPercentage_ht.value()

        def add(name, value, ref, dec = 3):

            current = getattr(self.node, ref)

            if abs(value-current) > 10**(-dec):
                return f"\ns['{name}'].{ref} = {value}"
            else:
                return ''

        name = self.node.name
        code = ""

        code += add(name, new_free_flooding, 'free_flooding')
        code += add(name, new_density,'density')
        code += add(name, new_volume,'volume')
        code += add(name, new_pct,'fill_pct')
        code += add(name, new_elev,'level_global')
        # code += add(name, new_ht_pct, 'fill_ht_pct')

        return code

    def post_update_event(self):

        try:
            self.ui.sbDenstiy.valueChanged.disconnect()
            self.ui.sbVolume.valueChanged.disconnect()
            self.ui.sbPercentage.valueChanged.disconnect()
            self.ui.sbElevation.valueChanged.disconnect()
            self.ui.cbFreeFlooding.toggled.disconnect()
            # self.ui.sbPercentage_ht.valueChanged.disconnect()

        except:
            pass # no connections yet

        self.ui.sbDenstiy.setValue(self.node.density)
        self.ui.sbVolume.setValue(self.node.volume)
        self.ui.sbPercentage.setValue(self.node.fill_pct)
        self.ui.sbElevation.setValue(self.node.level_global)
        self.ui.cbFreeFlooding.setChecked(self.node.free_flooding)
        # self.ui.sbPercentage_ht.setValue(self.node.fill_ht_pct)

        self.ui.sbDenstiy.valueChanged.connect(self.callback)
        self.ui.sbVolume.valueChanged.connect(self.callback)
        self.ui.sbPercentage.valueChanged.connect(self.callback)
        self.ui.sbElevation.valueChanged.connect(self.callback)
        self.ui.cbFreeFlooding.toggled.connect(self.callback)
        # self.ui.sbPercentage_ht.valueChanged.connect(self.callback)

        self.ui.widgetContents.setEnabled(not self.node.free_flooding)

        self.ui.lblCapacity.setText(f"{self.node.capacity:.3f}")

class EditBuoyancyDensity(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditBuoyancyDensity._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_buoyancy.Ui_Form()
            ui.setupUi(widget)
            EditBuoyancyDensity._ui = ui
            ui._widget = widget

        else:
            ui = EditBuoyancyDensity._ui

        try:
            ui.sbDenstiy.valueChanged.disconnect()
        except:
            pass

        ui.sbDenstiy.setValue(self.node.density)
        ui.sbDenstiy.valueChanged.connect(self.callback)

        self.ui = ui
        return ui._widget

    def generate_code(self):

        code = ""

        if self.node.density != self.ui.sbDenstiy.value():
            element = "\ns['{}']".format(self.node.name)
            code = element + '.density = {}'.format(self.ui.sbDenstiy.value())

        return code

class EditBuoyancyOrContactMesh(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditBuoyancyOrContactMesh._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_visual.Ui_widget_axis() # same as visual widget!
            ui.setupUi(widget)
            EditBuoyancyOrContactMesh._ui = ui
            ui._widget = widget

        else:
            ui = EditBuoyancyOrContactMesh._ui

        try:
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox_3.valueChanged.disconnect()
            ui.doubleSpinBox_4.valueChanged.disconnect()
            ui.doubleSpinBox_5.valueChanged.disconnect()
            ui.doubleSpinBox_6.valueChanged.disconnect()
            ui.doubleSpinBox_7.valueChanged.disconnect()
            ui.doubleSpinBox_8.valueChanged.disconnect()
            ui.doubleSpinBox_9.valueChanged.disconnect()
            ui.cbInvertNormals.toggled.disconnect()
            ui.comboBox.editTextChanged.disconnect()
        except:
            pass # no connections yet

        ui.doubleSpinBox_1.setValue(self.node.trimesh._offset[0])
        ui.doubleSpinBox_2.setValue(self.node.trimesh._offset[1])
        ui.doubleSpinBox_3.setValue(self.node.trimesh._offset[2])

        ui.doubleSpinBox_4.setValue(self.node.trimesh._rotation[0])
        ui.doubleSpinBox_5.setValue(self.node.trimesh._rotation[1])
        ui.doubleSpinBox_6.setValue(self.node.trimesh._rotation[2])

        ui.doubleSpinBox_7.setValue(self.node.trimesh._scale[0])
        ui.doubleSpinBox_8.setValue(self.node.trimesh._scale[1])
        ui.doubleSpinBox_9.setValue(self.node.trimesh._scale[2])

        ui.cbInvertNormals.setChecked(self.node.trimesh._invert_normals)

        ui.comboBox.clear()
        ui.comboBox.addItems(self.scene.get_resource_list('stl'))
        ui.comboBox.addItems(self.scene.get_resource_list('obj'))

        ui.comboBox.setCurrentText(self.node.trimesh._path)

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox_3.valueChanged.connect(self.callback)
        ui.doubleSpinBox_4.valueChanged.connect(self.callback)
        ui.doubleSpinBox_5.valueChanged.connect(self.callback)
        ui.doubleSpinBox_6.valueChanged.connect(self.callback)
        ui.doubleSpinBox_7.valueChanged.connect(self.callback)
        ui.doubleSpinBox_8.valueChanged.connect(self.callback)
        ui.doubleSpinBox_9.valueChanged.connect(self.callback)

        ui.comboBox.editTextChanged.connect(self.callback)
        ui.cbInvertNormals.toggled.connect(self.callback)

        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        offset = np.array((self.ui.doubleSpinBox_1.value(), self.ui.doubleSpinBox_2.value(),self.ui.doubleSpinBox_3.value()))
        rotation = np.array((self.ui.doubleSpinBox_4.value(), self.ui.doubleSpinBox_5.value(),self.ui.doubleSpinBox_6.value()))
        scale = np.array((self.ui.doubleSpinBox_7.value(), self.ui.doubleSpinBox_8.value(),self.ui.doubleSpinBox_9.value()))
        invert_normals = self.ui.cbInvertNormals.isChecked()

        try:
            new_path = self.scene.get_resource_path(self.ui.comboBox.currentText())
        except:
            new_path = "FILE DOES NOT EXIST"

        # check if we need to reload the mesh
        if np.any(offset != self.node.trimesh._offset) or \
           np.any(rotation != self.node.trimesh._rotation) or \
           np.any(scale != self.node.trimesh._scale) or \
           invert_normals != self.node.trimesh._invert_normals or \
           self.node.trimesh._path !=  new_path :

            if invert_normals:
                code = element + ".trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}), invert_normals=True)".format(
                    new_path, *scale, *rotation, *offset)
            else:
                code = element + ".trimesh.load_file(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}))".format(new_path, *scale, *rotation, *offset)

        return code




class EditBody(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditBody._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_body.Ui_Form()
            ui.setupUi(widget)
            EditBody._ui = ui
            ui._widget = widget

        else:
            ui = EditBody._ui

        try:
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox_3.valueChanged.disconnect()
            ui.doubleSpinBox_mass.valueChanged.disconnect()
        except:
            pass # no connections yet

        ui.doubleSpinBox_1.setValue(self.node.cog[0])
        ui.doubleSpinBox_2.setValue(self.node.cog[1])
        ui.doubleSpinBox_3.setValue(self.node.cog[2])

        ui.doubleSpinBox_mass.setValue(self.node.mass)

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox_3.valueChanged.connect(self.callback)
        ui.doubleSpinBox_mass.valueChanged.connect(self.callback)

        self.ui = ui

        return ui._widget

    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_mass = self.ui.doubleSpinBox_mass.value()
        new_cog = np.array(
            (self.ui.doubleSpinBox_1.value(), self.ui.doubleSpinBox_2.value(), self.ui.doubleSpinBox_3.value()))

        if new_mass != self.node.mass:
            code += element + '.mass = {}'.format(new_mass)

        if not np.all(new_cog == self.node.cog):
            code += element + '.cog = ({}, {}, {})'.format(*new_cog)

        return code

class EditPoi(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditPoi._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_poi.Ui_Poi()
            ui.setupUi(widget)
            EditPoi._ui = ui
            ui._widget = widget

        else:
            ui = EditPoi._ui

        try:
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox_3.valueChanged.disconnect()
        except:
            pass # no connections yet

        ui.doubleSpinBox_1.setValue(self.node.position[0])
        ui.doubleSpinBox_2.setValue(self.node.position[1])
        ui.doubleSpinBox_3.setValue(self.node.position[2])

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox_3.valueChanged.connect(self.callback)

        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_position = np.array((self.ui.doubleSpinBox_1.value(), self.ui.doubleSpinBox_2.value(),self.ui.doubleSpinBox_3.value()))

        if not np.all(new_position == self.node.position):
            code += element + '.position = ({}, {}, {})'.format(*new_position)

        return code


class EditCable(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditCable._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_cable.Ui_Cable_form()
            ui.setupUi(widget)

            EditCable._ui = ui
            ui._widget = widget
            ui.additional_pois = list()

        else:
            ui = EditCable._ui

        try:
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox.valueChanged.disconnect()

        except:
            pass # no connections yet

        for ddb in ui.additional_pois:
            ui.poiLayout.removeWidget(ddb)
            ddb.deleteLater()

        ui.doubleSpinBox_1.setValue(self.node.length)
        ui.doubleSpinBox_2.setValue(self.node.EA)
        ui.doubleSpinBox.setValue(self.node.diameter)

        # Set events
        ui.pbRemoveSelected.clicked.connect(self.delete_selected)

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox.valueChanged.connect(self.callback)


        # ------- setup the drag-and-drop code ---------

        ui.list.dropEvent = self.dropEvent
        ui.list.dragEnterEvent = self.dragEnterEvent
        ui.list.dragMoveEvent = self.dragEnterEvent

        ui.list.setDragEnabled(True)
        ui.list.setAcceptDrops(True)
        ui.list.setDragEnabled(True)

        ui.list.clear()
        for item in self.node._give_poi_names():
            ui.list.addItem(item)

        self.ui = ui  # needs to be done here as self.add_poi_dropdown modifies this

        return ui._widget

    def dropEvent(self,event):

        list = self.ui.list

        # dropping onto something?
        point = event.pos()
        drop_onto = list.itemAt(point)

        if drop_onto:
            row = list.row(drop_onto)
        else:
            row = -1

        if event.source() == list:
            item = list.currentItem()
            name = item.text()
            delrow = list.row(item)
            list.takeItem(delrow)
        else:
            name = event.mimeData().text()

        if row >= 0:
            list.insertItem(row, name)
        else:
            list.addItem(name)

        self.callback()

    def dragEnterEvent(self, event):
        if event.source() == self.ui.list:
            event.accept()
        else:
            try:
                name = event.mimeData().text()
                node = self.scene[name]
                if isinstance(node, Circle) or isinstance(node, Point):
                    event.accept()
            except:
                return


    # def dragMoveEvent(self, event):
    #     event.accept()

    def delete_selected(self):
        row = self.ui.list.currentRow()
        if row > -1:
            self.ui.list.takeItem(row)
        self.callback()


    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_length = self.ui.doubleSpinBox_1.value()
        new_EA = self.ui.doubleSpinBox_2.value()
        new_diameter = self.ui.doubleSpinBox.value()

        if not new_length == self.node.length:
            code += element + '.length = {}'.format(new_length)

        if not new_EA == self.node.EA:
            code += element + '.EA = {}'.format(new_EA)

        if not new_diameter == self.node.diameter:
            code += element + '.diameter = {}'.format(new_diameter)

        # get the poi names
        # new_names = [self.ui.comboBox.currentText(),self.ui.comboBox_2.currentText()]
        new_names = []
        for i in range(self.ui.list.count()):
            new_names.append(self.ui.list.item(i).text())

        if not (new_names == self.node._give_poi_names):
            code += element + '.connections = ('
            for name in new_names:
                code += "'{}',".format(name)
            code = code[:-1] + ')'

        return code


class EditForce(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditForce._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_force.Ui_widget_force()
            ui.setupUi(widget)
            EditForce._ui = ui
            ui._widget = widget

        else:
            ui = EditForce._ui

        try:
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox_3.valueChanged.disconnect()
            ui.doubleSpinBox_4.valueChanged.disconnect()
            ui.doubleSpinBox_5.valueChanged.disconnect()
            ui.doubleSpinBox_6.valueChanged.disconnect()
        except:
            pass # no connections yet

        ui.doubleSpinBox_1.setValue(self.node.force[0])
        ui.doubleSpinBox_2.setValue(self.node.force[1])
        ui.doubleSpinBox_3.setValue(self.node.force[2])

        ui.doubleSpinBox_4.setValue(self.node.moment[0])
        ui.doubleSpinBox_5.setValue(self.node.moment[1])
        ui.doubleSpinBox_6.setValue(self.node.moment[2])

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox_3.valueChanged.connect(self.callback)

        ui.doubleSpinBox_4.valueChanged.connect(self.callback)
        ui.doubleSpinBox_5.valueChanged.connect(self.callback)
        ui.doubleSpinBox_6.valueChanged.connect(self.callback)

        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_force = np.array(
            (self.ui.doubleSpinBox_1.value(), self.ui.doubleSpinBox_2.value(),self.ui.doubleSpinBox_3.value()))
        new_moment = np.array(
            (self.ui.doubleSpinBox_4.value(), self.ui.doubleSpinBox_5.value(), self.ui.doubleSpinBox_6.value()))

        if not np.all(new_force == self.node.force):
            code += element + '.force = ({}, {}, {})'.format(*new_force)
        if not np.all(new_moment == self.node.moment):
            code += element + '.moment = ({}, {}, {})'.format(*new_moment)

        return code

class EditSheave(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditSheave._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_sheave.Ui_widget_sheave()
            ui.setupUi(widget)
            EditSheave._ui = ui
            ui._widget = widget

        else:
            ui = EditSheave._ui

        try:
            ui.sbAX.valueChanged.disconnect()
            ui.sbAY.valueChanged.disconnect()
            ui.sbAZ.valueChanged.disconnect()
            ui.sbRadius.valueChanged.disconnect()
        except:
            pass # no connections yet

        ui.sbAX.setValue(self.node.axis[0])
        ui.sbAY.setValue(self.node.axis[1])
        ui.sbAZ.setValue(self.node.axis[2])

        ui.sbRadius.setValue(self.node.radius)

        ui.sbAX.valueChanged.connect(self.callback)
        ui.sbAY.valueChanged.connect(self.callback)
        ui.sbAZ.valueChanged.connect(self.callback)

        ui.sbRadius.valueChanged.connect(self.callback)

        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_axis = np.array(
            (self.ui.sbAX.value(), self.ui.sbAY.value(),self.ui.sbAZ.value()))
        new_radius = self.ui.sbRadius.value()

        if not np.all(new_axis == self.node.axis):
            code += element + '.axis = ({}, {}, {})'.format(*new_axis)
        if not new_radius == self.node.radius:
            code += element + '.radius = {}'.format(new_radius)

        return code

class EditHydSpring(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditHydSpring._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_linhyd.Ui_widget_linhyd()
            ui.setupUi(widget)
            EditHydSpring._ui = ui
            ui._widget = widget

        else:
            ui = EditHydSpring._ui

        try:
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox_3.valueChanged.disconnect()
            ui.BMT.valueChanged.disconnect()
            ui.BML.valueChanged.disconnect()
            ui.COFX.valueChanged.disconnect()
            ui.COFY.valueChanged.disconnect()
            ui.kHeave.valueChanged.disconnect()
            ui.waterline.valueChanged.disconnect()
            ui.disp.valueChanged.disconnect()
        except:
            pass # no connections yet

        ui.doubleSpinBox_1.setValue(self.node.cob[0])
        ui.doubleSpinBox_2.setValue(self.node.cob[1])
        ui.doubleSpinBox_3.setValue(self.node.cob[2])
        ui.BMT.setValue(self.node.BMT)
        ui.BML.setValue(self.node.BML)
        ui.COFX.setValue(self.node.COFX)
        ui.COFY.setValue(self.node.COFY)
        ui.kHeave.setValue(self.node.kHeave)
        ui.waterline.setValue(self.node.waterline)
        ui.disp.setValue(self.node.displacement_kN)

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox_3.valueChanged.connect(self.callback)
        ui.BMT.valueChanged.connect(self.callback)
        ui.BML.valueChanged.connect(self.callback)
        ui.COFX.valueChanged.connect(self.callback)
        ui.COFY.valueChanged.connect(self.callback)
        ui.kHeave.valueChanged.connect(self.callback)
        ui.waterline.valueChanged.connect(self.callback)
        ui.disp.valueChanged.connect(self.callback)

        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_cob = np.array(
            (self.ui.doubleSpinBox_1.value(), self.ui.doubleSpinBox_2.value(),self.ui.doubleSpinBox_3.value()))
        new_bmt = self.ui.BMT.value()
        new_bml = self.ui.BML.value()
        new_cofx = self.ui.COFX.value()
        new_cofy = self.ui.COFY.value()
        new_kHeave = self.ui.kHeave.value()
        new_waterline = self.ui.waterline.value()
        new_dipl = self.ui.disp.value()

        if not np.all(new_cob == self.node.cob):
            code += element + '.cob = ({}, {}, {})'.format(*new_cob)

        if not new_bmt == self.node.BMT:
            code += element + '.BMT = {}'.format(new_bmt)

        if not new_bml == self.node.BML:
            code += element + '.BML = {}'.format(new_bml)

        if not new_cofx == self.node.COFX:
            code += element + '.COFX = {}'.format(new_cofx)

        if not new_cofy == self.node.COFY:
            code += element + '.COFY = {}'.format(new_cofy)

        if not new_kHeave == self.node.kHeave:
            code += element + '.kHeave = {}'.format(new_kHeave)

        if not new_waterline == self.node.waterline:
            code += element + '.waterline = {}'.format(new_waterline)

        if not new_dipl == self.node.displacement_kN:
            code += element + '.displacement_kN = {}'.format(new_dipl)

        return code

class EditLC6d(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditLC6d._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_lincon6.Ui_widget_lincon6()
            ui.setupUi(widget)
            EditLC6d._ui = ui
            ui._widget = widget

        else:
            ui = EditLC6d._ui

        try:
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox_3.valueChanged.disconnect()
            ui.doubleSpinBox_4.valueChanged.disconnect()
            ui.doubleSpinBox_5.valueChanged.disconnect()
            ui.doubleSpinBox_6.valueChanged.disconnect()

            ui.cbMasterAxis.currentIndexChanged.disconnect()
            ui.cbSlaveAxis.currentIndexChanged.disconnect()
        except:
            pass # no connections yet

        self.alist = list()
        for axis in self.scene.nodes_of_type(vfs.Axis):
            self.alist.append(axis.name)

        ui.cbMasterAxis.clear()
        ui.cbSlaveAxis.clear()

        ui.cbMasterAxis.addItems(self.alist)
        ui.cbSlaveAxis.addItems(self.alist)

        ui.cbMasterAxis.setCurrentText(self.node.main.name)
        ui.cbSlaveAxis.setCurrentText(self.node.secondary.name)

        ui.doubleSpinBox_1.setValue(self.node.stiffness[0])
        ui.doubleSpinBox_2.setValue(self.node.stiffness[1])
        ui.doubleSpinBox_3.setValue(self.node.stiffness[2])

        ui.doubleSpinBox_4.setValue(self.node.stiffness[3])
        ui.doubleSpinBox_5.setValue(self.node.stiffness[4])
        ui.doubleSpinBox_6.setValue(self.node.stiffness[5])

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox_3.valueChanged.connect(self.callback)
        ui.doubleSpinBox_4.valueChanged.connect(self.callback)
        ui.doubleSpinBox_5.valueChanged.connect(self.callback)
        ui.doubleSpinBox_6.valueChanged.connect(self.callback)

        ui.cbMasterAxis.currentIndexChanged.connect(self.callback)
        ui.cbSlaveAxis.currentIndexChanged.connect(self.callback)

        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_stiffness = np.array((self.ui.doubleSpinBox_1.value(),
                                  self.ui.doubleSpinBox_2.value(),
                                  self.ui.doubleSpinBox_3.value(),
                                  self.ui.doubleSpinBox_4.value(),
                                  self.ui.doubleSpinBox_5.value(),
                                  self.ui.doubleSpinBox_6.value()))

        new_master = self.ui.cbMasterAxis.currentText()
        new_slave = self.ui.cbSlaveAxis.currentText()

        if not np.all(new_stiffness == self.node.stiffness):
            code += element + '.stiffness = ({}, {}, {},'.format(*new_stiffness[:3])
            code += '                  {}, {}, {})'.format(*new_stiffness[3:])

        if not new_master == self.node.main.name:
            code += element + '.main = s["{}"]'.format(new_master)

        if not new_slave == self.node.secondary.name:
            code += element + '.secondary = s["{}"]'.format(new_slave)


        return code

class EditConnector2d(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditConnector2d._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_con2d.Ui_widget_con2d()
            ui.setupUi(widget)
            EditConnector2d._ui = ui
            ui._widget = widget

        else:
            ui = EditConnector2d._ui

        try:
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_4.valueChanged.disconnect()

            ui.cbMasterAxis.currentIndexChanged.disconnect()
            ui.cbSlaveAxis.currentIndexChanged.disconnect()
        except:
            pass # no connections yet

        self.alist = list()
        for axis in self.scene.nodes_of_type(vfs.Axis):
            self.alist.append(axis.name)

        ui.cbMasterAxis.clear()
        ui.cbSlaveAxis.clear()

        ui.cbMasterAxis.addItems(self.alist)
        ui.cbSlaveAxis.addItems(self.alist)

        ui.cbMasterAxis.setCurrentText(self.node.nodeA.name)
        ui.cbSlaveAxis.setCurrentText(self.node.nodeB.name)

        ui.doubleSpinBox_1.setValue(self.node.k_linear)
        ui.doubleSpinBox_4.setValue(self.node.k_angular)

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_4.valueChanged.connect(self.callback)

        ui.cbMasterAxis.currentIndexChanged.connect(self.callback)
        ui.cbSlaveAxis.currentIndexChanged.connect(self.callback)

        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_k_lin = self.ui.doubleSpinBox_1.value()
        new_k_ang = self.ui.doubleSpinBox_4.value()
        new_master = self.ui.cbMasterAxis.currentText()
        new_slave = self.ui.cbSlaveAxis.currentText()

        if not new_master == self.node.nodeA.name:
            code += element + '.nodeA = s["{}"]'.format(new_master)

        if not new_slave == self.node.nodeB.name:
            code += element + '.nodeB = s["{}"]'.format(new_slave)

        if not new_k_lin == self.node.k_linear:
            code += element + '.k_linear = {}'.format(new_k_lin)

        if not new_k_ang == self.node.k_angular:
            code += element + '.k_angular = {}'.format(new_k_ang)

        return code

class EditBeam(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditBeam._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_beam.Ui_widget_beam()
            ui.setupUi(widget)
            EditBeam._ui = ui
            ui._widget = widget

        else:
            ui = EditBeam._ui

        try:
            ui.sbnSegments.valueChanged.disconnect()
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox_3.valueChanged.disconnect()
            ui.doubleSpinBox_4.valueChanged.disconnect()
            ui.doubleSpinBox_5.valueChanged.disconnect()
            ui.sbMass.valueChanged.disconnect()
            ui.cbTensionOnly.stateChanged.disconnect()

            ui.cbMasterAxis.currentIndexChanged.disconnect()
            ui.cbSlaveAxis.currentIndexChanged.disconnect()
        except:
            pass # no connections yet

        self.alist = list()
        for axis in self.scene.nodes_of_type(vfs.Axis):
            self.alist.append(axis.name)

        ui.cbMasterAxis.clear()
        ui.cbSlaveAxis.clear()

        ui.cbMasterAxis.addItems(self.alist)
        ui.cbSlaveAxis.addItems(self.alist)

        ui.cbMasterAxis.setCurrentText(self.node.nodeA.name)
        ui.cbSlaveAxis.setCurrentText(self.node.nodeB.name)

        ui.sbnSegments.setValue(self.node.n_segments)

        ui.doubleSpinBox_1.setValue(self.node.L)
        ui.doubleSpinBox_2.setValue(self.node.EIy)
        ui.doubleSpinBox_3.setValue(self.node.EIz)

        ui.doubleSpinBox_4.setValue(self.node.GIp)
        ui.doubleSpinBox_5.setValue(self.node.EA)

        ui.cbTensionOnly.setChecked(self.node.tension_only)

        ui.sbMass.setValue(self.node.mass)

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox_3.valueChanged.connect(self.callback)
        ui.doubleSpinBox_4.valueChanged.connect(self.callback)
        ui.doubleSpinBox_5.valueChanged.connect(self.callback)
        ui.sbMass.valueChanged.connect(self.callback)
        ui.cbTensionOnly.stateChanged.connect(self.callback)

        ui.cbMasterAxis.currentIndexChanged.connect(self.callback)
        ui.cbSlaveAxis.currentIndexChanged.connect(self.callback)
        ui.sbnSegments.valueChanged.connect(self.callback)

        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_L = self.ui.doubleSpinBox_1.value()
        new_EIy = self.ui.doubleSpinBox_2.value()
        new_EIz = self.ui.doubleSpinBox_3.value()
        new_GIp = self.ui.doubleSpinBox_4.value()
        new_EA = self.ui.doubleSpinBox_5.value()
        new_mass = self.ui.sbMass.value()
        new_n = self.ui.sbnSegments.value()
        new_tensiononly = self.ui.cbTensionOnly.isChecked()

        new_master = self.ui.cbMasterAxis.currentText()
        new_slave = self.ui.cbSlaveAxis.currentText()

        if not new_L == self.node.L:
            code += element + '.L = {}'.format(new_L)

        if not new_EIy == self.node.EIy:
            code += element + '.EIy = {}'.format(new_EIy)

        if not new_EIz == self.node.EIz:
            code += element + '.EIz = {}'.format(new_EIz)

        if not new_GIp == self.node.GIp:
            code += element + '.GIp = {}'.format(new_GIp)

        if not new_EA == self.node.EA:
            code += element + '.EA = {}'.format(new_EA)

        if not new_mass == self.node.mass:
            code += element + '.mass = {}'.format(new_mass)

        if not new_master == self.node.nodeA.name:
            code += element + '.nodeA = s["{}"]'.format(new_master)

        if not new_slave == self.node.nodeB.name:
            code += element + '.nodeB = s["{}"]'.format(new_slave)

        if not new_n == self.node.n_segments:
            code += element + '.n_segments = {}'.format(new_n)

        if not new_tensiononly == self.node.tension_only:
            code += element + '.tension_only = {}'.format(new_tensiononly)

        return code

class EditGeometricContact(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditGeometricContact._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_geometricconnection.Ui_GeometricConnection()
            ui.setupUi(widget)
            EditGeometricContact._ui = ui
            ui._widget = widget

        else:
            ui = EditGeometricContact._ui
            ui.rbPinHole.toggled.connect(self.change_type)
            ui.rbPinHole.toggled.disconnect()
            # ui.rbPinPin.toggled.disconnect()

            ui.cbMFix.toggled.disconnect()
            ui.cbSFix.toggled.disconnect()
            ui.cbSwivelFix.toggled.disconnect()

            ui.sbMasterRotation.valueChanged.disconnect()
            ui.sbSlaveRotation.valueChanged.disconnect()
            ui.sbSwivel.valueChanged.disconnect()


        ui.lblParent.setText(self.node.parent.name)
        ui.lblChild.setText(self.node.child.name)

        ui.rbPinHole.setChecked(self.node.inside)
        ui.rbPinPin.setChecked(not self.node.inside)

        ui.cbMFix.setChecked(self.node.fixed_to_parent)
        ui.cbSFix.setChecked(self.node.child_fixed)
        ui.cbSwivelFix.setChecked(self.node.swivel_fixed)

        ui.sbMasterRotation.setValue(self.node.rotation_on_parent)
        ui.sbSlaveRotation.setValue(self.node.child_rotation)
        ui.sbSwivel.setValue(self.node.swivel)

        ui.rbPinHole.toggled.connect(self.change_type)
        # ui.rbPinPin.toggled.connect(self.callback) # only need to connect one of the group

        ui.cbMFix.toggled.connect(self.callback)
        ui.cbSFix.toggled.connect(self.callback)
        ui.cbSwivelFix.toggled.connect(self.callback)

        ui.sbMasterRotation.valueChanged.connect(self.callback)
        ui.sbSlaveRotation.valueChanged.connect(self.callback)
        ui.sbSwivel.valueChanged.connect(self.callback)

        ui.pbFlip.clicked.connect(self.flip)
        ui.pbChangeSide.clicked.connect(self.change_side)

        self.ui = ui

        return ui._widget

    def flip(self):
        code = "\ns['{}'].flip()".format(self.node.name)
        self.run_code(code)

        self.ui.sbSwivel.valueChanged.disconnect()
        self.ui.sbSwivel.setValue(self.node.swivel)
        self.ui.sbSwivel.valueChanged.connect(self.callback)

    def change_side(self):
        code = "\ns['{}'].change_side()".format(self.node.name)
        self.run_code(code)
        self.ui.sbSlaveRotation.valueChanged.disconnect()
        self.ui.sbMasterRotation.valueChanged.disconnect()
        self.ui.sbMasterRotation.setValue(self.node.rotation_on_parent)
        self.ui.sbSlaveRotation.setValue(self.node.child_rotation)
        self.ui.sbSlaveRotation.valueChanged.connect(self.callback)
        self.ui.sbMasterRotation.valueChanged.connect(self.callback)

    def change_type(self):
        new_inside = self.ui.rbPinHole.isChecked()
        if not new_inside == self.node.inside:
            code = "\ns['{}']".format(self.node.name) + '.inside = ' + str(new_inside)
            self.run_code(code)
            self.ui.sbSwivel.valueChanged.disconnect()
            self.ui.sbSwivel.setValue(self.node.swivel)
            self.ui.sbSwivel.valueChanged.connect(self.callback)


    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_swivel = self.ui.sbSwivel.value()
        new_master = self.ui.sbMasterRotation.value()
        new_slave = self.ui.sbSlaveRotation.value()

        new_swivel_fixed = self.ui.cbSwivelFix.isChecked()
        new_master_fixed = self.ui.cbMFix.isChecked()
        new_slave_fixed = self.ui.cbSFix.isChecked()



        if not new_swivel == self.node.swivel:
            code += element + '.swivel = ' + str(new_swivel)
        if not new_master == self.node.rotation_on_parent:
            code += element + '.rotation_on_parent = ' + str(new_master)
        if not new_slave == self.node.child_rotation:
            code += element + '.child_rotation = ' + str(new_slave)

        if not new_swivel_fixed == self.node.swivel_fixed:
            code += element + '.swivel_fixed = ' + str(new_swivel_fixed)
        if not new_master_fixed == self.node.fixed_to_parent:
            code += element + '.fixed_to_parent = ' + str(new_master_fixed)
        if not new_slave_fixed == self.node.child_fixed:
            code += element + '.child_fixed = ' + str(new_slave_fixed)

        # if not new_inside == self.node.inside:
        #     code += element + '.inside = ' + str(new_inside)

        return code

class EditContactBall(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditContactBall._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_contactball.Ui_widget_contactball()
            ui.setupUi(widget)
            EditContactBall._ui = ui
            ui._widget = widget

        else:
            ui = EditContactBall._ui

        try:
            ui.sbR.valueChanged.disconnect()
            ui.sbK.valueChanged.disconnect()

        except:
            pass # no connections yet

        ui.sbR.setValue(self.node.radius)
        ui.sbK.setValue(self.node.k)

        ui.pbRemoveSelected.clicked.connect(self.delete_selected)
        ui.sbR.valueChanged.connect(self.callback)
        ui.sbK.valueChanged.connect(self.callback)

        ui.lwMeshes.dropEvent = self.onDrop
        ui.lwMeshes.dragEnterEvent = self.dragEnter
        ui.lwMeshes.dragMoveEvent = self.dragEnter

        self.ui = ui
        self.update_meshes_list()

        return ui._widget

    def dragEnter(self, event):
        dragged_name = event.mimeData().text()

        try:
            a = self.scene[dragged_name]
            if isinstance(a, vfs.ContactMesh):
                event.accept()
        except:
            return


    def onDrop(self,  event):

        try:
            dragged_name = event.mimeData().text()
        except:
            event.ignore()
            return

        try:
            dropped_node = self.scene[dragged_name]
        except:
            dropped_node = None

        if not isinstance(dropped_node, ContactMesh):
            event.ignore()
            return

        self.ui.lwMeshes.addItem(QListWidgetItem(dragged_name))
        self.callback()

    def delete_selected(self):
        row = self.ui.lwMeshes.currentRow()
        if row > -1:
            self.ui.lwMeshes.takeItem(row)
        self.callback()

    def update_meshes_list(self):
        self.ui.lwMeshes.clear()
        for name in self.node.meshes_names:
            self.ui.lwMeshes.addItem(QListWidgetItem(name))


    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_r = self.ui.sbR.value()
        new_k = self.ui.sbK.value()

        if new_r != self.node.radius:
            code += element + '.radius = {}'.format(new_r)
        if new_k != self.node.k:
            code += element + '.k = {}'.format(new_k)

        new_names = []
        for i in range(self.ui.lwMeshes.count()):
            new_names.append(self.ui.lwMeshes.item(i).text())

        if not (new_names == self.node.meshes_names):

            if new_names:
                code += element + '.meshes = ['
                for name in new_names:
                    code += "'{}',".format(name)
                code = code[:-1] + ']'
            else:
                code += element + '.meshes = []'

        return code

class EditSling(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditSling._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_sling.Ui_Form()
            ui.setupUi(widget)

            EditSling._ui = ui
            ui._widget = widget
            ui.additional_pois = list()

        else:
            ui = EditSling._ui

        try:
            ui.sbLength.valueChanged.disconnect()
            ui.sbEA.valueChanged.disconnect()
            ui.sbDiameter.valueChanged.disconnect()
            ui.sbMass.valueChanged.disconnect()
            ui.sbLEyeA.valueChanged.disconnect()
            ui.sbLEyeB.valueChanged.disconnect()
            ui.sbLSpliceA.valueChanged.disconnect()
            ui.sbLSpliceB.valueChanged.disconnect()

        except:
            pass # no connections yet

        for ddb in ui.additional_pois:
            ui.poiLayout.removeWidget(ddb)
            ddb.deleteLater()

        ui.sbLength.setValue(self.node.length)
        ui.sbEA.setValue(self.node.EA)
        ui.sbDiameter.setValue(self.node.diameter)
        ui.sbMass.setValue(self.node.mass)
        ui.sbLEyeA.setValue(self.node.LeyeA)
        ui.sbLEyeB.setValue(self.node.LeyeB)
        ui.sbLSpliceA.setValue(self.node.LspliceA)
        ui.sbLSpliceB.setValue(self.node.LspliceB)


        # Set events
        ui.pbRemoveSelected.clicked.connect(self.delete_selected)

        ui.sbLength.valueChanged.connect(self.callback)
        ui.sbEA.valueChanged.connect(self.callback)
        ui.sbDiameter.valueChanged.connect(self.callback)
        ui.sbMass.valueChanged.connect(self.callback)
        ui.sbLEyeA.valueChanged.connect(self.callback)
        ui.sbLEyeB.valueChanged.connect(self.callback)
        ui.sbLSpliceA.valueChanged.connect(self.callback)
        ui.sbLSpliceB.valueChanged.connect(self.callback)


        # ------- setup the drag-and-drop code ---------

        ui.list.dropEvent = self.dropEvent
        ui.list.dragEnterEvent = self.dragEnterEvent
        ui.list.dragMoveEvent = self.dragEnterEvent

        ui.list.setDragEnabled(True)
        ui.list.setAcceptDrops(True)
        ui.list.setDragEnabled(True)

        ui.list.clear()

        if self.node.endA is not None:
            ui.list.addItem(self.node.endA.name)

        for s in self.node.sheaves:
            ui.list.addItem(s.name)

        if self.node.endB is not None:
            ui.list.addItem(self.node.endB.name)

        self.ui = ui  # needs to be done here as self.add_poi_dropdown modifies this

        return ui._widget

    def dropEvent(self,event):

        list = self.ui.list

        # dropping onto something?
        point = event.pos()
        drop_onto = list.itemAt(point)

        if drop_onto:
            row = list.row(drop_onto)
        else:
            row = -1

        if event.source() == list:
            item = list.currentItem()
            name = item.text()
            delrow = list.row(item)
            list.takeItem(delrow)
        else:
            name = event.mimeData().text()

        if row >= 0:
            list.insertItem(row, name)
        else:
            list.addItem(name)

        self.callback()

    def dragEnterEvent(self, event):
        if event.source() == self.ui.list:
            event.accept()
        else:
            try:
                name = event.mimeData().text()
                node = self.scene[name]
                if isinstance(node, Circle) or isinstance(node, Point):
                    event.accept()
            except:
                return


    # def dragMoveEvent(self, event):
    #     event.accept()

    def delete_selected(self):
        row = self.ui.list.currentRow()
        if row > -1:
            self.ui.list.takeItem(row)
        self.callback()


    def generate_code(self):
        code = ""
        element = "\ns['{}']".format(self.node.name)

        node = self.node

        new_length = self.ui.sbLength.value()
        new_EA = self.ui.sbEA.value()
        new_diameter = self.ui.sbDiameter.value()
        new_mass = self.ui.sbMass.value()
        new_LeyeA = self.ui.sbLEyeA.value()
        new_LeyeB = self.ui.sbLEyeB.value()
        new_LspliceA = self.ui.sbLSpliceA.value()
        new_LspliceB = self.ui.sbLSpliceB.value()


        if not new_EA == self.node.EA:
            code += element + '.EA = {}'.format(new_EA)

        if not new_diameter == self.node.diameter:
            code += element + '.diameter = {}'.format(new_diameter)

        if not new_mass == self.node.mass:
            code += element + '.mass = {}'.format(new_mass)

        if not new_LeyeA == self.node.LeyeA:
            code += element + '.LeyeA = {}'.format(new_LeyeA)

        if not new_LeyeB == self.node.LeyeB:
            code += element + '.LeyeB = {}'.format(new_LeyeB)

        if not new_LspliceA == self.node.LspliceA:
            code += element + '.LspliceA = {}'.format(new_LspliceA)

        if not new_LspliceB == self.node.LspliceB:
            code += element + '.LspliceB = {}'.format(new_LspliceB)

        if not new_length == self.node.length:
            code += element + '.length = {}'.format(new_length)


        # get the poi names
        new_names = []
        for i in range(self.ui.list.count()):
            new_names.append(self.ui.list.item(i).text())

        new_endA = None
        new_endB = None
        new_circles = []

        if len(new_names) > 0:
            new_endA = new_names[0]

        if len(new_names) > 1:
            new_endB = new_names[-1]

        if len(new_names) > 2:
            new_circles = new_names[1:-1]

        if node.endA is not None:
            if not node.endA.name == new_endA:
                code += element + '.endA = "{}"'.format(new_endA)
        else:
            code += element + '.endA = "{}"'.format(new_endA)

        if node.endB is not None:
            if not node.endB.name == new_endB:
                code += element + '.endB = "{}"'.format(new_endB)
        else:
            code += element + '.endB = "{}"'.format(new_endB)

        sheave_names = [n.name for n in node.sheaves]

        if not sheave_names == new_circles:

            if new_circles:
                code += element + '.sheaves = ['
                for s in new_circles:
                    code += f'"{s}", '
                code = code[:-2] + ']'
            else:
                code += element + '.sheaves = []'

        return code


class EditShackle(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditShackle._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_shackle.Ui_widgetShackle()
            ui.setupUi(widget)
            EditShackle._ui = ui
            ui._widget = widget

        else:
            ui = EditShackle._ui

        try:
            ui.comboBox.currentTextChanged.disconnect()

        except:
            pass # no connections yet

        ui.comboBox.clear()

        ui.comboBox.addItems(self.node.defined_kinds())

        ui.comboBox.setCurrentText(self.node.kind)
        ui.comboBox.currentTextChanged.connect(self.callback)

        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""

        kind = self.ui.comboBox.currentText()
        if kind != self.node.kind:
            element = "\ns['{}']".format(self.node.name)
            code = element + f".kind = '{kind}'"

        return code

# ===========================================

class WidgetNodeProps(guiDockWidget):

    def guiDefaultLocation(self):
        return None # QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    def guiCreate(self):
        self.setVisible(False)

        self._open_edit_widgets = list()
        self._node_editors = list()

        self.main_layout = QtWidgets.QVBoxLayout()

        self.manager_widget = QtWidgets.QWidget()
        self.manager_layout = QtWidgets.QVBoxLayout()
        self.manager_widget.setLayout(self.manager_layout)

        self.managed_label = QtWidgets.QLabel(self.manager_widget)
        self.managed_label.setWordWrap(True)
        self.managed_label.setFrameShape(QtWidgets.QFrame.Box)
        self.managed_label.setStyleSheet("background: gold;")
        self.manager_layout.addWidget(self.managed_label)

        self.manager_link_label = QtWidgets.QPushButton(self.contents)
        self.manager_link_label.setText("Select manager")
        self.manager_link_label.clicked.connect(self.select_manager)
        self.manager_layout.addWidget(self.manager_link_label)

        self.warning_label = QtWidgets.QLabel()
        self.warning_label.setFrameShape(QtWidgets.QFrame.Box)
        self.warning_label.setText("WARNING")
        self.warning_label.setStyleSheet("background-color: rgb(255, 255, 185);\ncolor: rgb(200, 0, 127);")

        self.props_widget = QtWidgets.QWidget()

        self.main_layout.addWidget(self.warning_label)
        self.main_layout.addWidget(self.manager_widget)
        self.main_layout.addWidget(self.props_widget)

        self.contents.setLayout(self.main_layout)


        self.layout = QtWidgets.QVBoxLayout()
        self.props_widget.setLayout(self.layout)

        self.positioned = False

    def select_manager(self):
        node = self.guiSelection[0]
        manager = node._manager
        self.guiSelectNode(manager)


    def guiProcessEvent(self, event):

        if event in [guiEventType.SELECTION_CHANGED,guiEventType.FULL_UPDATE]:
            # check if we have a selection
            if self.guiSelection:
                self.select_node(self.guiSelection[0])

        if self._open_edit_widgets:

            self.setVisible(True)

            # first time, position the widget at the upper-right corner of the 3d view
            if not self.positioned:
                point = QtCore.QPoint(self.gui.ui.frame3d.width() - self.width(), 0)
                point = self.gui.ui.frame3d.mapToGlobal(point)
                self.move(point)
                self.positioned = True

        else:
            self.setVisible(False)

        if event in [guiEventType.MODEL_STATE_CHANGED]:
            if self.guiSelection:
                self.select_node(self.guiSelection[0])



    # ======= custom

    def node_name_changed(self):
        """Triggered by changing the text in the node-name widget"""
        node = self._node_name_editor.node
        element = "\ns['{}']".format(node.name)

        new_name = self._node_name_editor.ui.tbName.text()
        if not new_name == node.name:
            code = element + ".name = '{}'".format(new_name)
            self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)

        new_visible = self._node_name_editor.ui.cbVisible.isChecked()
        if not new_visible == node.visible:
            code = element + ".visible = {}".format(new_visible)
            self.guiRunCodeCallback(code, guiEventType.VIEWER_SETTINGS_UPDATE)

    def node_property_changed(self):
        code = ""
        for editor in self._node_editors:
            code += editor.generate_code()

        self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)

        for editor in self._node_editors:
            editor.post_update_event()

        self.check_for_warnings()


    def run_code(self, code):
        self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)


    def check_for_warnings(self):
        """Controls the warning-label on top of the node-editor

        Args:
            node:

        Returns:

        """
        node = self._node

        self.warning_label.setVisible(False)
        if isinstance(node, (Buoyancy, Tank)):
            # check mesh
            messages = node.trimesh.check_shape()
            if messages:
                self.warning_label.setText('\n'.join(messages))
                self.warning_label.setVisible(True)



    def select_node(self, node):
        
        to_be_removed = self._open_edit_widgets.copy()

        if node._manager and not isinstance(node, vfs.Shackle):
            self.managed_label.setText(
                f"The properties of this node are managed by node '{node._manager.name}' and should not be changed manually")
            self.manager_widget.setVisible(True)
            self.props_widget.setEnabled(self.guiScene._godmode)
        else:
            self.manager_widget.setVisible(False)
            self.props_widget.setEnabled(True)


        self._node_editors.clear()
        self._open_edit_widgets.clear()

        try:
            self._node_name_editor
            self._node_name_editor.node = node
            self._node_name_editor.create_widget()
        except:
            self._node_name_editor = EditNode(node, self.node_name_changed, self.guiScene, self.run_code)
            self._node_name_editor.create_widget()
            self.layout.addWidget(self._node_name_editor.ui._widget)

        if isinstance(node, vfs.Visual):
            self._node_editors.append(EditVisual(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.WaveInteraction1):
            self._node_editors.append(EditWaveInteraction(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Axis):
            self._node_editors.append(EditAxis(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.RigidBody) and not isinstance(node, vfs.Shackle):
            self._node_editors.append(EditBody(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Point):
            self._node_editors.append(EditPoi(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Cable):
            self._node_editors.append(EditCable(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Force):
            self._node_editors.append(EditForce(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Circle):
            self._node_editors.append(EditSheave(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.HydSpring):
            self._node_editors.append(EditHydSpring(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.LC6d):
            self._node_editors.append(EditLC6d(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Connector2d):
            self._node_editors.append(EditConnector2d(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Beam):
            self._node_editors.append(EditBeam(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.ContactBall):
            self._node_editors.append(EditContactBall(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.GeometricContact):
            self._node_editors.append(EditGeometricContact(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Sling):
            self._node_editors.append(EditSling(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Buoyancy) or isinstance(node, vfs.ContactMesh) or isinstance(node, vfs.Tank):
            self._node_editors.append(EditBuoyancyOrContactMesh(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Buoyancy):
            self._node_editors.append(EditBuoyancyDensity(node, self.node_property_changed, self.guiScene, self.run_code))


        if isinstance(node, vfs.Tank):
            self._node_editors.append(EditTank(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Shackle):
            self._node_editors.append(EditShackle(node, self.node_property_changed, self.guiScene, self.run_code))


        to_be_added = []
        for editor in self._node_editors:
            to_be_added.append(editor.create_widget())

        #for item in to_be_added:
        #    print('to be added: ' + str(type(item)))

        for widget in to_be_removed:
            if widget in to_be_added:
                to_be_added.remove(widget)
                self._open_edit_widgets.append(widget)
            else:
                self.layout.removeWidget(widget)
                widget.setVisible(False)

        for widget in to_be_added:
            self.layout.addWidget(widget)
            self._open_edit_widgets.append(widget)
            widget.setVisible(True)

        # Check for warnings

        self._node = node
        self.check_for_warnings()


        self.resize(0, 0)  # set the size of the floating dock widget to its minimum size
        self.adjustSize()
