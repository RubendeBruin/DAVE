"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2019
"""
from PySide2.QtGui import QIcon

"""
The purpose of this widget is to give the user a quick way to do things. A bit like clippy used to be. But then
one that actually works.

How does it work
Depending on the selected nodes (may be none) the agent makes and presents a list of logical next actions.
It does this by calling all registered functions after any selection change.

The functions get called with the current selection as argument and return a list or tuple of QtWidgets (usually buttons).
The list may be empty. 

"""
from DAVE.nodes import *
from DAVE.gui.dockwidget import *
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import QPoint
import DAVE.scene as nodes
import DAVE.settings as ds
from DAVE.gui.forms.widget_selection_actions import Ui_SelectionActions
from DAVE.gui.helpers.flow_layout import FlowLayout
from DAVE.gui.helpers.popup_textbox import get_text

from DAVE.settings import QUICK_ACTION_REGISTER

def nodes_of_type(node_list, types):
    return [node for node in node_list if isinstance(node, types)]

def get_parent_code(selection):
    frames = nodes_of_type(selection, Frame)
    if frames:
        return f", parent = '{frames[0].name}'"
    else:

        for node in selection:
            current = node
            while True:
                parent = getattr(current,'parent',None)
                if parent is None:
                    break
                else:
                    if isinstance(parent, Frame):
                        return f", parent = '{parent.name}'"
                    current = parent

        return ''

def find_nodes(nodes, types):
    """Returns nodes of given types. Only the first node per given type is returned and no duplicates.

    Returns None if not all types could be found
    """
    r = []
    source = nodes.copy()

    for t in types:
        for s in source:
            if isinstance(s, t):
                r.append(s)
                source.remove(s)
                break

    if len(r) == len(types):
        return r
    else:
        return None

def point(scene, selection, *args):
    code = f"s.new_point(name = '{scene.available_name_like('Point')}' {get_parent_code(selection)})"
    btn = QPushButton('+ &Point')
    btn.setIcon(QIcon(":/icons/poi.png"))
    return [(btn, code)]
QUICK_ACTION_REGISTER.append(point)

def frame(scene, selection, *args):
    code = f"s.new_frame(name = '{scene.available_name_like('Frame')}' {get_parent_code(selection)})"
    btn = QPushButton('+ &Frame')
    btn.setIcon(QIcon(":/icons/axis.png"))
    return [(btn, code)]
QUICK_ACTION_REGISTER.append(frame)

def rigidbody(scene, selection, *args):
    code = f"s.new_rigidbody(name = '{scene.available_name_like('Body')}' {get_parent_code(selection)})"
    btn = QPushButton('+ Rigid&Body')
    btn.setIcon(QIcon(":/icons/cube.png"))
    return [(btn, code)]
QUICK_ACTION_REGISTER.append(rigidbody)

def circle(scene, selection, *args):
    nodes = nodes_of_type(selection,Point)
    if nodes:
        code = f"s.new_circle(name = '{scene.available_name_like('Circle')}', parent = '{nodes[0].name}', axis = (0,1,0), radius = 1)"
        btn = QPushButton('+ &Circle')
        btn.setIcon(QIcon(":/icons/circle.png"))
        return [(btn, code)]

    code = f"point = s.new_point(name = '{scene.available_name_like('Point')}' {get_parent_code(selection)})"
    code += f"\ns.new_circle(name = '{scene.available_name_like('Circle')}', parent = point, axis = (0,1,0), radius = 1)"
    btn = QPushButton('+ Point && &Circle')
    btn.setIcon(QIcon(":/icons/circle.png"))
    return [(btn, code)]

QUICK_ACTION_REGISTER.append(circle)

def actions_on_circles(scene, selection, *args):
    # At least two sheaves selected
    style_warning = "color: darkred"

    actions = []
    p2 = find_nodes(selection, [nodes.Circle, nodes.Circle])

    if p2:


        p0 = p2[0]
        p1 = p2[1]

        # Grommet
        button = QPushButton('+ &Grommet')
        button.setIcon(QIcon(":/icons/circle.png"))
        name = scene.available_name_like("Grommet")
        code = f's.new_cable("{name}", endA="{p0.name}", endB = "{p0.name}", sheaves = ["{p1.name}"])'

        actions.append((button, code))

        # Geometric contact between p0 -> p1
        if p0.parent.parent is not None:

            button = QPushButton(f'Connect using {p0.name} to {p1.name}')
            button.setIcon(QIcon(':/icons/pin_hole.png'))
            name = scene.available_name_like("Contact")
            code = f's.new_geometriccontact("{name}", "{p0.name}", "{p1.name}")'

            #  sheave poi   axis
            if p0.parent.parent.parent is not None:
                button.setStyleSheet(style_warning)
                button.setToolTip(f"Warning: {p0.parent.parent.parent.name} will be disconnected from its parent")

            actions.append((button, code))

        # Geometric contact between p1 -> p0
        if p1.parent.parent is not None:

            button = QPushButton(f'Connect using {p1.name} to {p0.name}')
            button.setIcon(QIcon(':/icons/pin_hole.png'))
            name = scene.available_name_like("Contact")
            code = f's.new_geometriccontact("{name}", "{p1.name}", "{p0.name}")'

            #  sheave poi   axis
            if p1.parent.parent.parent is not None:
                button.setStyleSheet(style_warning)
                button.setToolTip(
                    f"Warning: {p1.parent.parent.parent.name} will be disconnected from its parent")

            actions.append((button, code))

    return actions

QUICK_ACTION_REGISTER.append(actions_on_circles)

def cables_slings_and_grommets(scene, selection, *args):

    # Multiple points/sheaves selected
    actions = []
    poi_and_sheave = nodes_of_type(selection, (Point, Circle))
    if poi_and_sheave:

        # check for length
        #
        # If all points are at the same location, then length can not be determined and an error is raised
        # check that in advance

        pos = [n.global_position for n in poi_and_sheave]
        L = 0
        for i in range(len(pos)-1):
            L += np.linalg.norm(np.array(pos[i]) - pos[i+1])
        if L == 0:
            length_code = ', length = 1'
        else:
            length_code = ''

        # Cable
        if len(poi_and_sheave) > 1:
            button = QPushButton('+ &Cable')
            button.setIcon(QIcon(':/icons/cable.png'))

            if len(poi_and_sheave) > 2:
                names = ''.join([f'"{e.name}",' for e in poi_and_sheave[1:-1]])
                sheaves = f', sheaves = [{names[:-1]}]'
            else:
                sheaves = ''

            name = scene.available_name_like("Cable")
            cable_code = f's.new_cable("{name}", endA="{poi_and_sheave[0].name}", endB = "{poi_and_sheave[-1].name}"{sheaves}{length_code})'

            actions.append((button, cable_code))

        # Sling
        if len(poi_and_sheave) > 1:
            button = QPushButton('+ &Sling')
            button.setIcon(QIcon(':/icons/sling.png'))

            if len(poi_and_sheave) > 2:
                names = ''.join([f'"{e.name}",' for e in poi_and_sheave[1:-1]])
                sheaves = f', sheaves = [{names[:-1]}]'
            else:
                sheaves = ''

            name = scene.available_name_like("Sling")
            cable_code = f's.new_sling("{name}", endA="{poi_and_sheave[0].name}", endB = "{poi_and_sheave[-1].name}"{sheaves}{length_code})'

            actions.append((button, cable_code))
    return actions

QUICK_ACTION_REGISTER.append(cables_slings_and_grommets)

def shackles(scene, selection, *args):

    circles = nodes_of_type(selection,Circle)
    actions = []

    # a single circle is selected
    if circles:
        sheave = circles[0]

        name = scene.available_name_like('Shackle')
        code = f"shackle = s.new_shackle(name = '{name}')"
        code += f'\ns.new_geometriccontact("{name}" + "_connection", "{name}_pin", "{sheave.name}", inside=True)'
        btn = QPushButton('Insert Shackle')
        btn.setIcon(QIcon(":/icons/shackle.png"))
        actions.append((btn, code))

    else:
        name = scene.available_name_like('Shackle')
        code = f"s.new_shackle(name = '{name}')"
        btn = QPushButton('+ Shackle')
        btn.setIcon(QIcon(":/icons/shackle.png"))
        actions.append((btn, code))

    return actions

QUICK_ACTION_REGISTER.append(shackles)


def con6d(scene, selection, *args):
    frames = nodes_of_type(selection, Frame)
    if len(frames) > 1:
        f1 = frames[0]
        f2 = frames[1]
        name = scene.available_name_like(f'Con6d_{f1.name}_to_{f2.name}')
        code = f"s.new_linear_connector_6d(name = '{name}', main = '{f2.name}', secondary = '{f1.name}')"

        button = QPushButton('Connect with 6d connector')
        button.setIcon(QIcon(':/icons/lincon6.png'))
        return [(button, code)]
    return []


def connectors(scene, selection, *args):

    actions = []
    frames = nodes_of_type(selection, Frame)
    if len(frames) > 1:
        f1 = frames[0]
        f2 = frames[1]

        # Beam
        name = scene.available_name_like(f'Beam')
        code = f"s.new_beam(name = '{name}', nodeA = '{f1.name}', nodeB = '{f2.name}')"

        button = QPushButton('Connect with beam')
        button.setIcon(QIcon(':/icons/beam.png'))

        actions.append((button, code))

        # 2D
        name = scene.available_name_like(f'Con2d_{f1.name}_to_{f2.name}')
        code = f"s.new_connector2d(name = '{name}', nodeA = '{f2.name}', nodeB = '{f1.name}')"

        button = QPushButton('Connect with 2d connector')
        button.setIcon(QIcon(':/icons/con2d.png'))

        actions.append((button, code))

        # 6D
        name = scene.available_name_like(f'Con6d_{f1.name}_to_{f2.name}')
        code = f"s.new_linear_connector_6d(name = '{name}', main = '{f2.name}', secondary = '{f1.name}')"

        button = QPushButton('Connect with 6d connector')
        button.setIcon(QIcon(':/icons/lincon6.png'))
        actions.append((button, code))

    return actions

QUICK_ACTION_REGISTER.append(connectors)

def visual(scene, selection, *args):
    parent = get_parent_code(selection)
    if parent:
        name = scene.available_name_like(f'Visual')
        code = f"s.new_visual(name = '{name}' {parent}, path = 'res: cube_with_bevel.obj')"

        button = QPushButton('+ &Visual')
        button.setIcon(QIcon(':/icons/visual.png'))
        return [(button, code)]
    return []

QUICK_ACTION_REGISTER.append(visual)

def other_frame_additions(scene, selection, *args):
    parent = get_parent_code(selection)
    actions = []
    if parent:
        name = scene.available_name_like(f'Buoyancy')
        code = f"s.new_buoyancy(name = '{name}' {parent}).trimesh.load_file('res: cube.obj')"

        button = QPushButton('+ Buoyancy')
        button.setIcon(QIcon(':/icons/buoy_mesh.png'))
        actions.append((button, code))

        name = scene.available_name_like(f'Tank')
        code = f"s.new_tank(name = '{name}' {parent}).trimesh.load_file('res: cube.obj')"

        button = QPushButton('+ &Tank')
        button.setIcon(QIcon(':/icons/tank.png'))
        actions.append((button, code))

    return actions

QUICK_ACTION_REGISTER.append(other_frame_additions)





class WidgetQuickActions(guiDockWidget):

    def guiCreate(self):
        """
        Add gui components to self.contents

        Do not fill the controls with actual values here. This is executed
        upon creation and guiScene etc are not yet available.

        """
        self.flow_layout = FlowLayout()
        self.contents.setLayout(self.flow_layout)
        self.buttons = []




    def guiProcessEvent(self, event):
        """
        Add processing that needs to be done.

        After creation of the widget this event is called with guiEventType.FULL_UPDATE
        """

        # selection changed: obviously
        # model structure: parent of select nodes may have changed
        # selected_node_modified: name of the selected node may have changed meaning that the parent has changed

        if event in [guiEventType.SELECTION_CHANGED, guiEventType.FULL_UPDATE, guiEventType.MODEL_STRUCTURE_CHANGED, guiEventType.SELECTED_NODE_MODIFIED]:
            self.fill()

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.BottomDockWidgetArea # QtCore.Qt.DockWidgetArea.RightDockWidgetArea

    # ======

    def find_nodes(self, types):
        """Returns nodes of given types. Only the first node per given type is returned and no duplicates.

        Returns None if not all types could be found
        """

        return find_nodes(self.guiSelection, types)


    def all_of_type(self, types):
        source = self.guiSelection.copy()

        types = tuple(types)

        if np.all( [isinstance(e, types) for e in source] ):
            return source
        else:
            return None




    def fill(self):

        # Remove everything
        self.contents.setUpdatesEnabled(False)

        for button in self.buttons:
            self.flow_layout.removeWidget(button)
            button.deleteLater()

        self.buttons.clear()

        # Scan for new buttons

        for qa in QUICK_ACTION_REGISTER:
            actions = qa(self.guiScene, self.guiSelection)
            for action in actions:
                btn = action[0]
                code = action[1]
                self.buttons.append(btn)
                btn.pressed.connect(lambda c=code, *args: self.guiRunCodeCallback(c, guiEventType.MODEL_STRUCTURE_CHANGED))

        # add all buttons to the layout

        for button in self.buttons:
            self.flow_layout.addWidget(button)

        self.contents.setUpdatesEnabled(True)
