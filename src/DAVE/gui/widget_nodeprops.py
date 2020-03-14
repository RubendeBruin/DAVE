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

import numpy as np

from PySide2.QtWidgets import QListWidgetItem


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
        raise Exception('Show() method not defined in derived class')


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
        except:
            pass # no connections yet

        ui.tbName.setText(self.node.name)

        ui.tbName.textChanged.connect(self.callback)

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

        try:
            ui.checkBox_1.stateChanged.disconnect()
            ui.checkBox_2.stateChanged.disconnect()
            ui.checkBox_3.stateChanged.disconnect()
            ui.checkBox_4.stateChanged.disconnect()
            ui.checkBox_5.stateChanged.disconnect()
            ui.checkBox_6.stateChanged.disconnect()

            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox_3.valueChanged.disconnect()
            ui.doubleSpinBox_4.valueChanged.disconnect()
            ui.doubleSpinBox_5.valueChanged.disconnect()
            ui.doubleSpinBox_6.valueChanged.disconnect()
        except:
            pass # no connections yet

        ui.doubleSpinBox_1.setValue(self.node.position[0])
        ui.doubleSpinBox_2.setValue(self.node.position[1])
        ui.doubleSpinBox_3.setValue(self.node.position[2])

        ui.doubleSpinBox_4.setValue(self.node.rotation[0])
        ui.doubleSpinBox_5.setValue(self.node.rotation[1])
        ui.doubleSpinBox_6.setValue(self.node.rotation[2])

        ui.checkBox_1.setChecked(self.node.fixed[0])
        ui.checkBox_2.setChecked(self.node.fixed[1])
        ui.checkBox_3.setChecked(self.node.fixed[2])
        ui.checkBox_4.setChecked(self.node.fixed[3])
        ui.checkBox_5.setChecked(self.node.fixed[4])
        ui.checkBox_6.setChecked(self.node.fixed[5])

        ui.checkBox_1.stateChanged.connect(self.callback)
        ui.checkBox_2.stateChanged.connect(self.callback)
        ui.checkBox_3.stateChanged.connect(self.callback)
        ui.checkBox_4.stateChanged.connect(self.callback)
        ui.checkBox_5.stateChanged.connect(self.callback)
        ui.checkBox_6.stateChanged.connect(self.callback)

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

        new_position = np.array((self.ui.doubleSpinBox_1.value(), self.ui.doubleSpinBox_2.value(),self.ui.doubleSpinBox_3.value()))
        new_rotation = np.array((self.ui.doubleSpinBox_4.value(), self.ui.doubleSpinBox_5.value(),self.ui.doubleSpinBox_6.value()))
        new_fixed = np.array((self.ui.checkBox_1.isChecked(),
                              self.ui.checkBox_2.isChecked(),
                              self.ui.checkBox_3.isChecked(),
                              self.ui.checkBox_4.isChecked(),
                              self.ui.checkBox_5.isChecked(),
                              self.ui.checkBox_6.isChecked()))

        if not np.all(new_position == self.node.position):
            code += element + '.position = ({}, {}, {})'.format(*new_position)

        if not np.all(new_rotation == self.node.rotation):
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
        ui.comboBox.addItems(self.scene.get_resource_list('obj'))

        ui.comboBox.setCurrentText(self.node.path)

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

            ui.comboBox.editTextChanged.disconnect()
        except:
            pass # no connections yet

        # ui.doubleSpinBox_1.setValue(self.node.offset[0])
        # ui.doubleSpinBox_2.setValue(self.node.offset[1])
        # ui.doubleSpinBox_3.setValue(self.node.offset[2])
        #
        # ui.doubleSpinBox_4.setValue(self.node.rotation[0])
        # ui.doubleSpinBox_5.setValue(self.node.rotation[1])
        # ui.doubleSpinBox_6.setValue(self.node.rotation[2])
        #
        # ui.doubleSpinBox_7.setValue(self.node.scale[0])
        # ui.doubleSpinBox_8.setValue(self.node.scale[1])
        # ui.doubleSpinBox_9.setValue(self.node.scale[2])



        ui.comboBox.clear()
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

        self.ui = ui

        return ui._widget

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        offset = np.array((self.ui.doubleSpinBox_1.value(), self.ui.doubleSpinBox_2.value(),self.ui.doubleSpinBox_3.value()))
        rotation = np.array((self.ui.doubleSpinBox_4.value(), self.ui.doubleSpinBox_5.value(),self.ui.doubleSpinBox_6.value()))
        scale = np.array((self.ui.doubleSpinBox_7.value(), self.ui.doubleSpinBox_8.value(),self.ui.doubleSpinBox_9.value()))

        try:
            new_path = self.scene.get_resource_path(self.ui.comboBox.currentText())
        except:
            new_path = "FILE DOES NOT EXIST"

        # load_obj(self, filename, offset = None, rotation = None, scale = None)
        code = element + ".trimesh.load_obj(r'{}', scale = ({},{},{}), rotation = ({},{},{}), offset = ({},{},{}))".format(new_path, *scale, *rotation, *offset)

        return code




class EditBody(EditAxis):

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

        self.plist = [""]

        for poi in self.scene.nodes_of_type(vfs.Sheave):
            self.plist.append(poi.name)

        for poi in self.scene.nodes_of_type(vfs.Poi):
            self.plist.append(poi.name)

        try:
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox.valueChanged.disconnect()
            ui.comboBox_2.currentIndexChanged.disconnect()
            ui.comboBox.currentIndexChanged.disconnect()

        except:
            pass # no connections yet

        for ddb in ui.additional_pois:
            ui.poiLayout.removeWidget(ddb)
            ddb.deleteLater()

        ui.additional_pois.clear()

        ui.comboBox.clear()

        ui.comboBox.addItems(self.plist)

        ui.comboBox_2.clear()
        ui.comboBox_2.addItems(self.plist)

        ui.doubleSpinBox_1.setValue(self.node.length)
        ui.doubleSpinBox_2.setValue(self.node.EA)
        ui.doubleSpinBox.setValue(self.node.diameter)

        self.ui = ui  # needs to be done here as self.add_poi_dropdown modifies this

        # Add as many drop-down boxes as needed
        poi_names = self.node.give_poi_names()
        for i in range(len(poi_names)-2):
            self.add_poi_dropdown()

        self.ui.comboBox.setCurrentText(poi_names[0])
        self.ui.comboBox_2.setCurrentText(poi_names[1])

        for i,name in enumerate(poi_names[2:]):
            self.ui.additional_pois[i].setCurrentText(name)
            # self.ui.additional_pois[i].currentIndexChanged.connect(self.callback)

        # Set events
        ui.btnAdd.clicked.connect(self.add_poi_dropdown)
        ui.btnRemove.clicked.connect(self.delete_poi_dropdown)

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox.valueChanged.connect(self.callback)

        ui.comboBox.currentIndexChanged.connect(self.callback)
        ui.comboBox_2.currentIndexChanged.connect(self.callback)
        for cbx in self.ui.additional_pois:
            cbx.currentIndexChanged.connect(self.callback)

        return ui._widget

    def add_poi_dropdown(self):
        cbx = QtWidgets.QComboBox(self.ui.frame)
        self.ui.poiLayout.addWidget(cbx)
        cbx.addItems(self.plist)

        self.ui.additional_pois.append(cbx)


    def delete_poi_dropdown(self):
        if self.ui.additional_pois:
            last_item = self.ui.additional_pois.pop()
            self.ui.poiLayout.removeWidget(last_item)
            last_item.deleteLater()
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
        for cbx in [self.ui.comboBox, self.ui.comboBox_2, *self.ui.additional_pois]:
            ct = cbx.currentText()
            if ct: # skip empty
                new_names.append(ct)

        if not (new_names == self.node.give_poi_names):
            code += element + '.clear_connections()'
            for name in new_names:
                code += element + ".add_connection(s['{}'])".format(name)

        code += '\n' + element + ".check_endpoints()"

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

        ui.cbMasterAxis.setCurrentText(self.node.master.name)
        ui.cbSlaveAxis.setCurrentText(self.node.slave.name)

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

        if not new_master == self.node.master.name:
            code += element + '.master = s["{}"]'.format(new_master)

        if not new_slave == self.node.slave.name:
            code += element + '.slave = s["{}"]'.format(new_slave)


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

        ui.cbMasterAxis.setCurrentText(self.node.master.name)
        ui.cbSlaveAxis.setCurrentText(self.node.slave.name)

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

        if not new_master == self.node.master.name:
            code += element + '.master = s["{}"]'.format(new_master)

        if not new_slave == self.node.slave.name:
            code += element + '.slave = s["{}"]'.format(new_slave)

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
            ui.doubleSpinBox_1.valueChanged.disconnect()
            ui.doubleSpinBox_2.valueChanged.disconnect()
            ui.doubleSpinBox_3.valueChanged.disconnect()
            ui.doubleSpinBox_4.valueChanged.disconnect()
            ui.doubleSpinBox_5.valueChanged.disconnect()

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

        ui.cbMasterAxis.setCurrentText(self.node.master.name)
        ui.cbSlaveAxis.setCurrentText(self.node.slave.name)

        ui.doubleSpinBox_1.setValue(self.node.L)
        ui.doubleSpinBox_2.setValue(self.node.EIy)
        ui.doubleSpinBox_3.setValue(self.node.EIz)

        ui.doubleSpinBox_4.setValue(self.node.GIp)
        ui.doubleSpinBox_5.setValue(self.node.EA)

        ui.doubleSpinBox_1.valueChanged.connect(self.callback)
        ui.doubleSpinBox_2.valueChanged.connect(self.callback)
        ui.doubleSpinBox_3.valueChanged.connect(self.callback)
        ui.doubleSpinBox_4.valueChanged.connect(self.callback)
        ui.doubleSpinBox_5.valueChanged.connect(self.callback)

        ui.cbMasterAxis.currentIndexChanged.connect(self.callback)
        ui.cbSlaveAxis.currentIndexChanged.connect(self.callback)

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

        if not new_master == self.node.master.name:
            code += element + '.master = s["{}"]'.format(new_master)

        if not new_slave == self.node.slave.name:
            code += element + '.slave = s["{}"]'.format(new_slave)

        return code

class EditContactBall(NodeEditor):

    _ui = None

    def create_widget(self):

        # Prevents the ui from being created more than once
        if EditContactBall._ui is None:

            widget = QtWidgets.QWidget()
            ui = DAVE.gui.forms.widget_contactball.Ui_widget_contactball()
            ui.setupUi(widget)
            EditForce._ui = ui
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
        event.accept()


    def onDrop(self,  event):

        try:
            dragged_name = event.mimeData().text()
        except:
            event.ignore()
            return

        code = "\ns['{}'].add_contactmesh('{}')".format(self.node.name,dragged_name)
        self.run_code(code)

        # update the contents of this widget
        self.update_meshes_list()

    def update_meshes_list(self):
        self.ui.lwMeshes.clear()
        for name in self.node.meshes_names:
            self.ui.lwMeshes.addItem(QListWidgetItem(name) )



        

    def generate_code(self):

        code = ""
        element = "\ns['{}']".format(self.node.name)

        new_r = self.ui.sbR.value()
        new_k = self.ui.sbK.value()

        if new_r != self.node.radius:
            code += element + '.radius = {}'.format(new_r)
        if new_k != self.node.k:
            code += element + '.k = {}'.format(new_k)

        return code


# ===========================================

class WidgetNodeProps(guiDockWidget):

    def guiDefaultLocation(self):
        return None # QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    def guiCreate(self):
        self.setVisible(False)

        self._open_edit_widgets = list()
        self._node_editors = list()
        
        self.layout = QtWidgets.QVBoxLayout()
        self.contents.setLayout(self.layout)

    def guiProcessEvent(self, event):

        if event in [guiEventType.SELECTION_CHANGED,guiEventType.FULL_UPDATE]:
            # check if we have a selection
            if self.guiSelection:
                self.select_node(self.guiSelection[0])

        if self._open_edit_widgets:
            self.setVisible(True)
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

    def node_property_changed(self):
        code = ""
        for editor in self._node_editors:
            code += editor.generate_code()

        self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)

    def run_code(self, code):
        self.guiRunCodeCallback(code, guiEventType.SELECTED_NODE_MODIFIED)


    def select_node(self, node):
        
        # for widget in self._open_edit_widgets:
        #     self.layout.removeWidget(widget)
        #     widget.setVisible(False)

        to_be_removed = self._open_edit_widgets.copy()


        #for item in to_be_removed:
        #    print('to be removed: ' + str(type(item)))

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

        if isinstance(node, vfs.RigidBody):
            self._node_editors.append(EditBody(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Poi):
            self._node_editors.append(EditPoi(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Cable):
            self._node_editors.append(EditCable(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Force):
            self._node_editors.append(EditForce(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Sheave):
            self._node_editors.append(EditSheave(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.HydSpring):
            self._node_editors.append(EditHydSpring(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.LC6d):
            self._node_editors.append(EditLC6d(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.Connector2d):
            self._node_editors.append(EditConnector2d(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.LinearBeam):
            self._node_editors.append(EditBeam(node, self.node_property_changed, self.guiScene, self.run_code))

        if isinstance(node, vfs.ContactBall):
            self._node_editors.append(EditContactBall(node, self.node_property_changed, self.guiScene, self.run_code))


        if isinstance(node, vfs.Buoyancy) or isinstance(node, vfs.ContactMesh):
            self._node_editors.append(EditBuoyancyOrContactMesh(node, self.node_property_changed, self.guiScene, self.run_code))

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
            widget.setVisible(True)
            self.layout.addWidget(widget)
            self._open_edit_widgets.append(widget)

        self.resize(0, 0)  # set the size of the floating dock widget to its minimum size
