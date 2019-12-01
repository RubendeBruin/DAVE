"""
    GUI

    The GUI can be created from a scene via

    s = Scene()
    ...
    G = Gui(s)
    G.show()


    Or by running this file as main

"""

"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""

import DAVE.visual as vfv
import DAVE.scene as vfs
import DAVE.constants as vfc
import DAVE.standard_assets
import DAVE.forms.resources_rc as resources_rc
from DAVE.forms.viewer_form import Ui_MainWindow
from DAVE.forms.dlg_solver import Ui_Dialog
import numpy as np
import math
import DAVE.element_widgets as element_widgets

import sys
from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtWidgets import QMenu, QMainWindow, QDialog
from PySide2.QtCore import QMimeData, Qt
from PySide2 import QtCore

from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide2.QtWidgets import QFileDialog

from IPython.utils.capture import capture_output
import datetime

class NodeData:
    data = list()

    def clear(self):
        self.data.clear()

    def add(self, node, visual, tree):
        self.data.append({'node':node, 'visual':visual, 'tree':tree})

    def get_node(self, node):
        for d in self.data:
            if d['node']==node:
                return d
        return None

    def get_visual(self, visual):
        for d in self.data:
            if d['visual']==visual:
                return d
        return None

    def get_tree(self, tree):
        for d in self.data:
            if d['tree'] == tree:
                return d
        return None

    def get_name(self, name):
        for d in self.data:
            if d['node'].name == name:
                return d
        return None

    def get_actor(self, actor):
        for d in self.data:
            for a in d['visual'].actors:
                if a == actor:
                    return d
        return None


class SceneTreeModel(QStandardItemModel):

    def mimeData(self, indexes):
        QStandardItemModel.mimeData(self, indexes)
        name = indexes[0].data()
        print('called mimeData on ' + name)
        mimedata = QMimeData()
        mimedata.setText(name)
        return mimedata

    def supportedDropActions(self):
        return QtCore.Qt.MoveAction

    def canDropMimeData(self, data, action, row, column, parent):
        print('can drop called on')
        print(parent.data())
        return True

    def dropMimeData(self, data, action, row, column, parent):
        parent_name = parent.data()
        node_name = data.text()
        print("Dropped {} onto {}".format(node_name, parent_name))

        if parent_name is None:
            code = "s['{}'].change_parent_to(None)".format(node_name)
        else:
            code = "s['{}'].change_parent_to(s['{}'])".format(node_name, parent_name)
        print(code)

        self._scene.run_code(code)

        return False

class SolverDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(SolverDialog, self).__init__(parent)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/icons/cube.png"))


class Gui:

    def __init__(self, scene):
        self.scene = scene
        """Reference to a scene"""
        self.visual = vfv.Viewport(scene)
        """Reference to a viewport"""

        self.ui = DAVE.forms.viewer_form.Ui_MainWindow()
        """Reference to the ui"""

        self.app = QtWidgets.QApplication(sys.argv)

        self.MainWindow = QMainWindow()
        self.ui.setupUi(self.MainWindow)

        self.node_data = NodeData()
        """Holds a list of node_data"""

        self.selected_node = None
        """Data of selected node, if any"""

        self._open_edit_widgets = list()
        """Active edit widgets"""

        self._node_editors = list()
        """Not-used list of node-editor objects, required to keep them from being deleted which also removes the signals"""

        self._dofs = None
        """Values of dofs before last solve command"""

        self.visual.create_visuals(recreate=True)
        self.visual.position_visuals()

        self.update_node_data_and_tree()

        try:
            self._logfile = open(vfc.LOGFILE, mode = 'w+')
        except Exception as E:
            print('Can not create logfile due to the following error: ')
            print(E)
            exit(1)

        #---- register events ----

        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave_scene.triggered.connect(self.menu_save)
        self.ui.actionImport_sub_scene.triggered.connect(self.menu_import)
        self.ui.actionImport_browser.triggered.connect(self.import_browser)
        self.ui.actionRender_current_view.triggered.connect(self.render_in_blender)

        self.ui.treeView.activated.connect(self.tree_select_node)  # fires when a user presses [enter]
        # self.ui.treeView.pressed.connect(self.tree_select_node)
        self.ui.treeView.doubleClicked.connect(self.tree_select_node)

        self.ui.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeView.customContextMenuRequested.connect(self.rightClickTreeview)

        self.ui.frame3d.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.frame3d.customContextMenuRequested.connect(self.rightClickViewport)

        self.ui.teCode.textChanged.connect(self.code_change)

        self.visual.mouseLeftEvent = self.view3d_select_element

        self.ui.pbRunCode.clicked.connect(self.run_code_in_teCode)
        self.ui.pbCopyFeedback.clicked.connect(self.feedback_copy)
        self.ui.pbCopyHistory.clicked.connect(self.history_copy)
        self.ui.pbGenerateSceneCode.clicked.connect(self.generate_scene_code)
        self.ui.pbStartOver.clicked.connect(self.start_over)
        self.ui.btnGoalSeek.clicked.connect(self.goal_seek_go)
        self.ui.stability_go.clicked.connect(self.stability_curve_go)

        # ------- make action buttons

        a = self.ui.toolBar.addAction("Solve Statics [alt+s]", self.solve_statics)
        a.setShortcut("Alt+s")

        a = self.ui.toolBar.addAction("Undo solve [alt+z]", self.undo_solve_statics)
        a.setShortcut("Alt+z")

        a = self.ui.toolBar.addAction("New Axis [alt+a]", self.new_axis)
        a.setShortcut("Alt+a")

        a = self.ui.toolBar.addAction("New Poi [alt+p]", self.new_poi)
        a.setShortcut("Alt+p")

        a = self.ui.toolBar.addAction("New RigidBody [alt+b]", self.new_body)
        a.setShortcut("Alt+b")

        a = self.ui.toolBar.addAction("New Cable [alt+c]", self.new_cable)
        a.setShortcut("Alt+c")

        a = self.ui.toolBar.addAction("New Force [alt+f]", self.new_force)
        a.setShortcut("Alt+f")

        a = self.ui.toolBar.addAction("New 6d Connector [alt+6]", self.new_linear_connector)
        a.setShortcut("Alt+6")

        a = self.ui.toolBar.addAction("New 2d Connector [alt+2]", self.new_connector2d)
        a.setShortcut("Alt+2")

        a = self.ui.toolBar.addAction("New Linear Hydrostatics [alt+h]", self.new_linear_hydrostatics)
        a.setShortcut("Alt+h")

        a = self.ui.toolBar.addAction("New Visual [alt+v]", self.new_visual)
        a.setShortcut("Alt+v")

        a = self.ui.toolBar.addAction("New Buoyancy mesh [alt+b]", self.new_buoyancy_mesh)
        a.setShortcut("Alt+b")

        # -------------- menu

        self.ui.actionNew.triggered.connect(self.clear)
        self.ui.actionShow_water_plane.triggered.connect(self.toggle_show_global)
        self.ui.actionShow_visuals.triggered.connect(self.toggle_show_visuals)
        self.ui.actionShow_Geometry_elements.triggered.connect(self.toggle_show_geometry)
        self.ui.actionShow_force_applyting_element.triggered.connect(self.toggle_show_force)

        self.ui.actionHorizontal_camera.triggered.connect(self.level_camera)
        self.ui.actionAdd_light.triggered.connect(self.visual.make_lighter)
        self.ui.actionDark_mode.triggered.connect(self.visual.make_darker)
        self.ui.action2D_mode.triggered.connect(self.visual.toggle_2D)

        def normalize_force():
            self.run_code('self.visual.force_do_normalize = not self.visual.force_do_normalize')

        self.ui.actionShow_all_forces_at_same_size.triggered.connect(normalize_force)

        def increase_force_size():
            self.run_code('self.visual.force_scale = 1.1*self.visual.force_scale')

        self.ui.actionIncrease_force_size.triggered.connect(increase_force_size)

        def decrease_force_size():
            self.run_code('self.visual.force_scale = 0.9*self.visual.force_scale')

        self.ui.actionDecrease_force_size.triggered.connect(decrease_force_size)

        def increase_geo_size():
            self.run_code('self.visual.geometry_scale = 1.1*self.visual.geometry_scale')

        self.ui.actionIncrease_Geometry_size.triggered.connect(increase_geo_size)

        def decrease_geo_size():
            self.run_code('self.visual.geometry_scale = 0.9*self.visual.geometry_scale')

        self.ui.actionDecrease_Geometry_size.triggered.connect(decrease_geo_size)

        # docking windows

        def show_python_dock():
            self.ui.pythonDockWidget.setVisible(True)
        self.ui.pythonDockWidget.setVisible(False)
        self.ui.actionPython_console.triggered.connect(show_python_dock)

        # -- goal-seek

        def show_goalseek_dock():
            self.ui.goalseekDockWidget.setVisible(True)

        self.ui.goalseekDockWidget.setVisible(False)
        self.ui.actionGoal_seek.triggered.connect(show_goalseek_dock)

        # -- stability

        def show_stability_dock():
            self.ui.stabilityDockWidget.setVisible(True)

        self.ui.stabilityDockWidget.setVisible(False)
        self.ui.actionStability_curve.triggered.connect(show_stability_dock)


        # -------------- Create the 3d view

        self.MainWindow.setCentralWidget(self.ui.frame3d)
        self.visual.show_embedded(self.ui.frame3d)
        self.visual.update_visibility()

        iren = self.visual.renwin.GetInteractor()
        iren.AddObserver('TimerEvent', self.set_state)


    def clear(self):
        self.run_code('s.clear()')

    def open(self):
        filename, _ = QFileDialog.getOpenFileName(filter="*.dave_asset", caption="Assets")
        if filename:
            code = 's.clear()\ns.load_scene(r"{}")'.format(filename)
            self.run_code(code)

    def menu_import(self):
        filename, _ = QFileDialog.getOpenFileName(filter="*.dave_asset", caption="Assets")
        if filename:
            code = 's.import_scene(r"{}")'.format(filename)
            self.run_code(code)

    def import_browser(self):
        G = DAVE.standard_assets.Gui()
        r = G.showModal()

        if r is not None:
            file = r[0]
            container = r[1]
            prefix = r[2]
            code = 's.import_scene(s.get_resource_path("{}"), containerize={}, prefix="{}")'.format(file,container,prefix)
            self.run_code(code)

    def render_in_blender(self):

        pos = self.visual.screen.camera.GetPosition()
        dir = self.visual.screen.camera.GetDirectionOfProjection()

        code = 'import DAVE.io.blender'
        code += "\ncamera = {{'position':({},{},{}), 'direction':({},{},{})}}".format(*pos,*dir)
        code += '\nblender_base = r"{}"'.format(vfc.BLENDER_BASE_SCENE)
        code += '\nblender_result = r"{}"'.format(Path(vfc.PATH_TEMP) / 'current_render.blend')
        code += '\nDAVE.io.blender.create_blend_and_open(s, blender_base_file=blender_base, blender_result_file=blender_result, camera=camera)'
        code += '\nprint("Opening blender, close blender to continue.")'
        code += '\nprint("In blender, press F12 to go to rendered camera view.")'
        self.run_code(code)

    def menu_save(self):
        filename, _ = QFileDialog.getSaveFileName(filter="*.dave_scene", caption="Scene files",directory=self.scene.resources_paths[0])
        if filename:
            code = 's.save_scene(r"{}")'.format(filename)
            self.run_code(code)

    def level_camera(self):
        self.visual.level_camera()

    def history_copy(self):
        self.app.clipboard().setText(self.ui.teHistory.toPlainText())

    def feedback_copy(self):
        self.app.clipboard().setText(self.ui.teFeedback.toPlainText())

    def generate_scene_code(self):
        self.ui.teFeedback.setText(self.scene.give_python_code())

    def start_over(self):
        self.ui.teCode.setPlainText(self.ui.teHistory.toPlainText())
        self.ui.teHistory.clear()
        self.clear()

    def rightClickViewport(self, point):
        node = self.tree_selected_node()
        globLoc = self.ui.frame3d.mapToGlobal(point)
        self.openContextMenyAt(node, globLoc)

    def rightClickTreeview(self, point):
        node = self.tree_selected_node()
        globLoc = self.ui.treeView.mapToGlobal(point)
        self.openContextMenyAt(node, globLoc)

    def goal_seek_go(self):
        # def goal_seek(self, set_node, set_property, target, change_node, change_property, bracket=None, tol=1e-3):
        code = 's.goal_seek(set_property="{}",\nset_node="{}",\ntarget={},\nchange_property="{}",\nchange_node="{}")'.format(
            self.ui.gsSetProp.text(),
            self.ui.gsSetNode.text(),
            self.ui.gsValue.text(),
            self.ui.gsChangeProp.text(),
            self.ui.gsChangeNode.text())
        self.set_code(code)

    def stability_curve_go(self):
        # def goal_seek(self, set_node, set_property, target, change_node, change_property, bracket=None, tol=1e-3):
        code = 'from DAVE.marine import GZcurve_DisplacementDriven\n'
        code += """GZcurve_DisplacementDriven(scene = s,
            vessel_node = "{}",
            displacement_kN={},
            minimum_heel= {},
            maximum_heel={},
            steps={},
            teardown={},
            allow_surge={},
            allow_sway={},
            allow_yaw={},
            allow_trim={})""".format(self.ui.stability_node_name.text(),
                                     self.ui.stability_displacement.value(),
                                     self.ui.stability_heel_start.value(),
                                     self.ui.stability_heel_max.value(),
                                     self.ui.stability_n_steps.value(),
                                     self.ui.stability_do_teardown.isChecked(),
                                     self.ui.stability_surge.isChecked(),
                                     self.ui.stability_sway.isChecked(),
                                     self.ui.stability_yaw.isChecked(),
                                     self.ui.stability_trim.isChecked())

        self.set_code(code)

    def openContextMenyAt(self, node, globLoc):
        menu = QMenu()

        if node is not None:

            node = node[0]
            node_name = node.name
            node_data = self.node_data.get_node(node)

            def delete():
                self.set_code('s.delete("{}")'.format(node_name))

            def dissolve():
                self.set_code('s.dissolve("{}")'.format(node_name))

            def edit():
                self.select_node(node_data)

            menu.addAction("Delete {}".format(node_name), delete)
            menu.addAction("Dissolve (Evaporate) {}".format(node_name), dissolve)
            menu.addAction("Edit {}".format(node_name), edit)

            menu.addSeparator()

            def copy_python_code():
                code = node.give_python_code()
                print(code)
                self.app.clipboard().setText(code)

            menu.addAction("Copy python code", copy_python_code)
            menu.addSeparator()

            def duplicate():
                name = node.name
                name_of_duplicate = self.scene.available_name_like(name)
                node.name = name_of_duplicate
                code = node.give_python_code()
                node.name = name
                self.run_code(code)

                data = self.node_data.get_name(name_of_duplicate)
                self.select_node(data)


            menu.addAction("Duplicate", duplicate)
            menu.addSeparator()



        menu.addAction("New Axis", self.new_axis)
        menu.addAction("New RigidBody", self.new_body)
        menu.addAction("New Poi", self.new_poi)
        menu.addAction("New Sheave", self.new_sheave)
        menu.addAction("New Cable", self.new_cable)
        menu.addAction("New Force", self.new_force)
        menu.addAction("New Beam", self.new_beam)
        menu.addAction("New 2d Connector", self.new_connector2d)
        menu.addAction("New 6d Connector", self.new_linear_connector)
        menu.addAction("New Linear Hydrostatics", self.new_linear_hydrostatics)
        menu.addAction("New Visual", self.new_visual)
        menu.addAction("New Buoyancy mesh", self.new_buoyancy_mesh)

        menu.exec_(globLoc)


    def toggle_show_force(self):
        self.visual.show_force = self.ui.actionShow_force_applyting_element.isChecked()
        self.visual.update_visibility()

    def toggle_show_geometry(self):
        self.visual.show_geometry = self.ui.actionShow_Geometry_elements.isChecked()
        self.visual.update_visibility()

    def toggle_show_global(self):
        self.visual.show_global = self.ui.actionShow_water_plane.isChecked()
        self.visual.update_visibility()

    def toggle_show_visuals(self):
        self.visual.show_visual = self.ui.actionShow_visuals.isChecked()
        self.visual.update_visibility()

    def actionDelete(self):
        print('delete')

    def stop_solving(self):
        self._terminate = True

    def solve_statics(self):
        self.scene._vfc.state_update()
        old_dofs = self.scene._vfc.get_dofs()
        self._dofs = old_dofs.copy()

        long_wait = False
        dialog = None

        self._terminate = False



        # solve with time-out
        count = 0
        while True:
            status = self.scene._vfc.state_solve_statics_with_timeout(0.5, True)

            if self._terminate:
                print('Terminating')
                break

            if status == 0:
                if count == 0:
                    break
                else:
                    long_wait = True

                    self.visual.position_visuals()
                    self.visual.refresh_embeded_view()
                    break

            if dialog is None:
                dialog = SolverDialog()
                dialog.btnTerminate.clicked.connect(self.stop_solving)
                dialog.show()

            count += 1
            dialog.label_2.setText('Maximum error = {}'.format(self.scene._vfc.Emaxabs))
            dialog.update()

            self.visual.position_visuals()
            self.visual.refresh_embeded_view()
            self.app.processEvents()

        if dialog is not None:
            dialog.close()

        if DAVE.constants.GUI_DO_ANIMATE and not long_wait:
            new_dofs = self.scene._vfc.get_dofs()
            self.animate(old_dofs, new_dofs, vfc.GUI_ANIMATION_NSTEPS)

        self.ui.teHistory.setPlainText(self.ui.teHistory.toPlainText() + '\n#---\ns.solve_statics()')

    def undo_solve_statics(self):
        if self._dofs is not None:
            self.run_code('s._vfc.set_dofs(self._dofs)')


    def onClose(self):
        self.visual.shutdown_qt()
        self._logfile.close()
        print('closing')

    def show(self):

        self.MainWindow.show()
        self.app.aboutToQuit.connect(self.onClose)

        while True:
            try:
                self.app.exec_()
                break
            except Exception as E:
                print(E)


    def refresh_3dview(self):
        self.visual.refresh_embeded_view()

    def update_node_data_and_tree(self):
        """
        Updates the tree and assembles the node-data

        This data is obtained from scene.nodes and assumes that
        each of the nodes has a visual assigned to it.

        """
        model = SceneTreeModel()
        model._scene = self
        self.scene.sort_nodes_by_dependency()

        self.node_data.clear()

        for node in self.scene.nodes:

            # create a tree item
            text = node.name
            item = QStandardItem(text)

            # if we have a parent, then put the items under the parent,
            # else put it under the root

            item.setIcon(QIcon(":/icons/redball.png"))
            if isinstance(node, vfs.Axis):
                item.setIcon(QIcon(":/icons/axis.png"))
            if isinstance(node, vfs.RigidBody):
                item.setIcon(QIcon(":/icons/cube.png"))
            if isinstance(node, vfs.Poi):
                item.setIcon(QIcon(":/icons/poi.png"))
            if isinstance(node, vfs.Cable):
                item.setIcon(QIcon(":/icons/cable.png"))
            if isinstance(node, vfs.Visual):
                item.setIcon(QIcon(":/icons/visual.png"))
            if isinstance(node, vfs.LC6d):
                item.setIcon(QIcon(":/icons/lincon6.png"))
            if isinstance(node, vfs.Connector2d):
                item.setIcon(QIcon(":/icons/con2d.png"))
            if isinstance(node, vfs.LinearBeam):
                item.setIcon(QIcon(":/icons/beam.png"))
            if isinstance(node, vfs.HydSpring):
                item.setIcon(QIcon(":/icons/linhyd.png"))
            if isinstance(node, vfs.Force):
                item.setIcon(QIcon(":/icons/force.png"))
            if isinstance(node, vfs.Sheave):
                item.setIcon(QIcon(":/icons/sheave.png"))
            if isinstance(node, vfs.Buoyancy):
                item.setIcon(QIcon(":/icons/trimesh.png"))


            try:
                parent = node.parent
            except:
                parent = None

            if parent is not None:
                data = self.node_data.get_node(parent)
                if data is None:
                    raise Exception('Parent of {} does not exist'.format(text))
                data['tree'].appendRow(item)
            else:
                model.invisibleRootItem().appendRow(item)

            # store in the lookup database

            self.node_data.add(node,node.visual,item)

        self.ui.treeView.setModel(model)
        self.ui.treeView.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.ui.treeView.expandAll()

    def node_name_changed(self):
        """Triggered by changing the text in the node-name widget"""
        node = self._node_name_editor.node
        element = "\ns['{}']".format(node.name)

        new_name = self._node_name_editor.ui.tbName.text()
        if not new_name == node.name:
            code = element + ".name = '{}'".format(new_name)
            self.run_code(code)


    def deselect_all(self):
        # self.visual.set_alpha(1, 1)
        self.visual.deselect_all()
        self.ui.dockWidget_3.setVisible(False)


    def select_node(self, data):
        """Select a node

        Arguments:
            - data : NodeData object
        """


        if data is None:  # selected None
            self.deselect_all()
            return

        node = data['node']

        if self.selected_node is not None:
            self.selected_node['visual'].deselect()

        visual = data['visual']
        visual.select()

        # see if there are any visuals attached to the selected object

        deps = self.scene.nodes_of_type(vfs.Visual)

        for dep in deps:
            if dep.parent == node:
                dep.visual.make_transparent()
            else:
                dep.visual.reset_opacity()



        self.selected_node = data
        self.refresh_3dview()



        # Select the node in the tree-view as well
        print('Selecting node in tree-view')
        twi = data['tree']
        index = self.ui.treeView.model().indexFromItem(twi)
        self.ui.treeView.setCurrentIndex(index)

        for widget in self._open_edit_widgets:
            self.ui.widgetLayout.removeWidget(widget)
            widget.setVisible(False)

        self._node_editors.clear()
        self._open_edit_widgets.clear()

        try:
            self._node_name_editor
            self._node_name_editor.node = node
            self._node_name_editor.create_widget()
        except:
            self._node_name_editor = element_widgets.EditNode(node, self.node_name_changed, self.scene)
            self._node_name_editor.create_widget()
            self.ui.widgetLayout.addWidget(self._node_name_editor.ui._widget)

        if isinstance(node, vfs.Visual):
            # self.visual.set_alpha(1, 1)
            self._node_editors.append(element_widgets.EditVisual(node, self.node_property_changed, self.scene))

        if isinstance(node, vfs.Axis):
            self._node_editors.append(element_widgets.EditAxis(node, self.node_property_changed, self.scene))

        if isinstance(node, vfs.RigidBody):
            self._node_editors.append(element_widgets.EditBody(node, self.node_property_changed, self.scene))

        if isinstance(node, vfs.Poi):
            self._node_editors.append(element_widgets.EditPoi(node, self.node_property_changed, self.scene))

        if isinstance(node, vfs.Cable):
            self._node_editors.append(element_widgets.EditCable(node, self.node_property_changed, self.scene))

        if isinstance(node, vfs.Force):
            self._node_editors.append(element_widgets.EditForce(node, self.node_property_changed, self.scene))

        if isinstance(node, vfs.Sheave):
            self._node_editors.append(element_widgets.EditSheave(node, self.node_property_changed, self.scene))


        if isinstance(node, vfs.HydSpring):
            self._node_editors.append(element_widgets.EditHydSpring(node, self.node_property_changed, self.scene))

        if isinstance(node, vfs.LC6d):
            self._node_editors.append(element_widgets.EditLC6d(node, self.node_property_changed, self.scene))

        if isinstance(node, vfs.Connector2d):
            self._node_editors.append(element_widgets.EditConnector2d(node, self.node_property_changed, self.scene))


        if isinstance(node, vfs.LinearBeam):
            self._node_editors.append(element_widgets.EditBeam(node, self.node_property_changed, self.scene))

        if isinstance(node, vfs.Buoyancy):
            self._node_editors.append(element_widgets.EditBuoyancy(node, self.node_property_changed, self.scene))

        for editor in self._node_editors:
            widget = editor.create_widget()
            widget.setVisible(True)
            self.ui.widgetLayout.addWidget(widget)
            self._open_edit_widgets.append(widget)

        self.ui.dockWidget_3.setVisible(True)
        self.ui.dockWidgetContents_3.resize(0, 0)  # set the size of the floating dock widget to its minimum size
        self.ui.dockWidget_3.resize(0, 0)

        # ---- display node properties
        self.display_node_properties(node)

    def display_node_properties(self, node):

        props = []
        props.extend(vfc.PROPS_NODE)
        if isinstance(node, vfs.Axis):
            props.extend(vfc.PROPS_AXIS)
        if isinstance(node, vfs.RigidBody):
            props.extend(vfc.PROPS_BODY)
        if isinstance(node, vfs.Poi):
            props.extend(vfc.PROPS_POI)
        if isinstance(node, vfs.Cable):
            props.extend(vfc.PROPS_CABLE)
        if isinstance(node, vfs.Connector2d):
            props.extend(vfc.PROPS_CON2D)
        if isinstance(node, vfs.Buoyancy):
            props.extend(vfc.PROPS_BUOY_MESH)

        # evaluate properties
        self.ui.dispPropTree.clear()
        for p in props:
            code = "node.{}".format(p)
            try:
                result = eval(code)
            except:
                result = 'Error evaluating {}'.format(code)

            pa = QtWidgets.QTreeWidgetItem(self.ui.dispPropTree)
            v = QtWidgets.QTreeWidgetItem(pa)
            pa.setText(0,'.' + p)
            v.setText(0,str(result))

        self.ui.dispPropTree.expandAll()






    # events

    def tree_select_node(self, index):
        node_name = index.data()
        data = self.node_data.get_name(node_name)
        self.select_node(data)

    def view3d_select_element(self, info):
        data = self.node_data.get_actor(info)

        if data is not None:
            # # if a visual is clicked, then select the parent of this visual instead
            # node = data['node']
            # if isinstance(node, vfs.Visual):
            #     if node.parent is not None:
            #         data = self.node_data.get_node(node.parent)

            # if the node is already selected, then select something different
            if self.selected_node is not None:

                # cycle between node and its parent
                if self.selected_node['node'] == data['node']:
                    node = data['node']
                    try:
                        node = node.parent
                        data = self.node_data.get_node(node)
                    except:
                        pass

                # cycle between node and its master
                if self.selected_node['node'] == data['node']:
                    node = data['node']
                    try:
                        node = node.master
                        data = self.node_data.get_node(node)
                    except:
                        pass

                # cycle between node and its poiA
                if self.selected_node['node'] == data['node']:
                    node = data['node']
                    try:
                        node = node._pois[0]
                        data = self.node_data.get_node(node)
                    except:
                        pass




        self.select_node(data)

    def node_property_changed(self):

        code = ""
        for editor in self._node_editors:
            code += editor.generate_code()

        self.ui.teCode.setText(code)

    def code_change(self):
        if self.ui.cbAutoExecute.isChecked():

            before = self.scene.nodes.copy()
            self.run_code_in_teCode()

            # if we created something new, then select it
            for node in self.scene.nodes:
                if node not in before:
                    data = self.node_data.get_node(node)
                    self.select_node(data)
                    break



            if self.ui.cbAutoStatics.isChecked():
                # self.solve_statics()
                self.run_code('s.solve_statics()')

    def set_code(self, code):
        self.ui.teCode.setText(code)

    def run_code(self, code):

        s = self.scene

        self.ui.teFeedback.setStyleSheet("background-color: yellow;")
        self.ui.teFeedback.setText("Running...")
        self.ui.teFeedback.update()

        with capture_output() as c:

            try:
                exec(code)

                self.ui.teFeedback.setStyleSheet("background-color: white;")
                if c.stdout:
                    self.ui.teFeedback.setText(c.stdout)
                else:
                    self.ui.teFeedback.append("...Done")

                self.ui.teFeedback.append(str(datetime.datetime.now()))

                self._logfile.write(code)
                self._logfile.write('\n')
                self._logfile.flush()

                self.ui.teHistory.setPlainText(self.ui.teHistory.toPlainText() + '\n#---\n' + code)
                self.ui.teHistory.verticalScrollBar().setValue(self.ui.teHistory.verticalScrollBar().maximum()) # scroll down all the way
            except Exception as E:
                self.ui.teFeedback.setText(c.stdout + '\n' + str(E) + '\n\nWhen running: \n\n' + code)
                self.ui.teFeedback.setStyleSheet("background-color: red;")
                return


            self.scene._vfc.state_update()
            self.visual.create_visuals()
            self.visual.add_new_actors_to_screen()
            self.update_node_data_and_tree()
            self.visual.position_visuals()
            self.visual.update_visibility()
            self.refresh_3dview()

            if self.selected_node is not None:

                # check if selected node is still present
                if self.selected_node['node'] in self.scene.nodes:
                    self.display_node_properties(self.selected_node['node'])
                else:
                    self.selected_node = None
                    self.ui.dockWidget_3.setVisible(False)


    def run_code_in_teCode(self):
        code = self.ui.teCode.toPlainText()
        self.run_code(code)

    def new_something(self, what):
        r = what(self.scene, self.tree_selected_node())
        if r:
            self.set_code("s." + r)

    def tree_selected_node(self):

        if self.ui.treeView.selectedIndexes():

            nodes = list()
            for index in self.ui.treeView.selectedIndexes():
                node_name = index.data()
                node = self.node_data.get_name(node_name)
                nodes.append(node['node'])
            return nodes
        else:
            return None


    def new_axis(self):
        self.new_something(DAVE.element_widgets.add_axis)

    def new_body(self):
        self.new_something(DAVE.element_widgets.add_body)

    def new_poi(self):
        self.new_something(DAVE.element_widgets.add_poi)

    def new_cable(self):
        self.new_something(DAVE.element_widgets.add_cable)

    def new_force(self):
        self.new_something(DAVE.element_widgets.add_force)

    def new_sheave(self):
        self.new_something(DAVE.element_widgets.add_sheave)

    def new_linear_connector(self):
        self.new_something(DAVE.element_widgets.add_linear_connector)

    def new_connector2d(self):
        self.new_something(DAVE.element_widgets.add_connector2d)

    def new_beam(self):
        self.new_something(DAVE.element_widgets.add_beam_connector)

    def new_linear_hydrostatics(self):
        self.new_something(DAVE.element_widgets.add_linear_hydrostatics)

    def new_visual(self):
        self.new_something(DAVE.element_widgets.add_visual)

    def new_buoyancy_mesh(self):
        self.new_something(DAVE.element_widgets.add_buoyancy)

    def set_state(self, a, b):

        try:
            if self._timerid is None:
                print('timer not assigned')
                return

            self._iAnimation += 1
            factor = self._iAnimation / self._steps

            if factor >= 1:
                print('Destroying timer')
                to_be_destroyed = self._timerid
                self._timerid = None
                iren = self.visual.renwin.GetInteractor()
                iren.DestroyTimer(to_be_destroyed)

                self.visual.quick_updates_only = False
                self.scene._vfc.set_dofs(self._new_dof)
                self.visual.position_visuals()
                self.visual.update_outlines()
                self.visual.refresh_embeded_view()
                return


            old = 0.5 + 0.5 * math.cos(3.14159 * factor)
            dofs = (1 - old) * self._new_dof + old * self._old_dof
            # print(a,b)
            self.scene._vfc.set_dofs(dofs)
            self.visual.position_visuals()
            self.visual.update_outlines()
            self.visual.refresh_embeded_view()
        except:
            print('An error occurred during the animate-event')


    def animate(self, old_dof, new_dof, steps):

        print('Old dof: {}'.format(len(old_dof)))
        print('New dof: {}'.format(len(new_dof)))

        print('starting animation')
        self.visual.quick_updates_only = True

        self._old_dof = np.array(old_dof)
        self._new_dof = np.array(new_dof)
        self._steps = steps

        self._timerid = None

        print('creating timer')
        iren = self.visual.renwin.GetInteractor()
        self._iAnimation = 0

        # iren.AddObserver('TimerEvent', self.set_state)
        self._timerid = iren.CreateRepeatingTimer(round(1000/vfc.GUI_ANIMATION_FPS))


# ====== main code ======

if __name__ == '__main__':



    s = DAVE.scene.Scene()
    #
    # s.new_poi('b', position = (10,0,15))
    # s.new_sheave('sb', 'b', (0, 1, 0), 0.5)
    #
    # n = s.import_scene('liftme')
    # n.fixed = False
    #
    #
    # n = s.import_scene(s.get_resource_path("crane block 4p.dave_asset"), containerize=True, prefix="")
    # n.z = 30
    # s.dissolve(n)
    #
    # from DAVE.rigging import *
    #
    # create_sling(s,'sling3',Ltotal=30, LeyeA=4, LeyeB=5, LspliceA=2, LspliceB=3, diameter = 0.3, EA = 1e6, mass = 3, endA='lp3bow', endB='prong4_sheave')
    # create_sling(s, 'sling4', Ltotal=30, LeyeA=4, LeyeB=5, LspliceA=2, LspliceB=3, diameter=0.3, EA=1e6, mass=3,
    #              endA='lp4bow', endB='prong3_sheave')
    #
    # # doubled sling in two parts
    # n = s.import_scene(s.get_resource_path("GP800.dave_asset"), containerize=True, prefix="sh01_")
    # n.fixed = False
    #
    # create_sling(s, 'sling1_part1', Ltotal=40, LeyeA=4, LeyeB=5, LspliceA=2, LspliceB=3, diameter=0.3, EA=1e6, mass=3,
    #              endA='lp1lp2', endB='sh01_bow', sheave='prong2_sheave')
    #
    # create_sling(s, 'sling1_part2', Ltotal=20, LeyeA=4, LeyeB=5, LspliceA=2, LspliceB=3, diameter=0.3, EA=1e6, mass=3,
    #              endA='lp1lp1', endB='sh01_pin')
    #
    #
    # # doubled sling
    # create_sling(s, 'sling2', Ltotal=60, LeyeA=4, LeyeB=5, LspliceA=2, LspliceB=3, diameter=0.3, EA=1e6, mass=3,
    #              endA='lp2lp2', endB='lp2lp1', sheave='prong1_sheave')
    #
    #
    #
    # s.solve_statics()

    from DAVE.io.blender import *


    s.resources_paths.append(r"C:\data\Dave\Public\Blender visuals")
    s.resources_paths.append(r"C:\data\3d models\shackles")

    Gui(s).show()

    create_blend_and_open(s)