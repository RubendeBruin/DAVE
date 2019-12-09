from DAVE.gui2.dockwidget import *
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide2.QtCore import QMimeData, Qt, QItemSelectionModel
from PySide2.QtWidgets import QTreeWidgetItem
import DAVE.scene as nodes
import DAVE.settings as ds

class WidgetDerivedProperties(guiDockWidget):

    def guiCreate(self):

        self.dispPropTree = QtWidgets.QTreeWidget(self.contents)
        self.dispPropTree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dispPropTree.setAlternatingRowColors(True)
        self.dispPropTree.setRootIsDecorated(False)
        self.dispPropTree.setObjectName("dispPropTree")
        item_0 = QtWidgets.QTreeWidgetItem(self.dispPropTree)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.dispPropTree.header().setVisible(False)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.dispPropTree)
        self.contents.setLayout(layout)

    def guiProcessEvent(self, event):

        if event in [guiEventType.SELECTION_CHANGED,
                     guiEventType.FULL_UPDATE,
                     guiEventType.MODEL_STATE_CHANGED,
                     guiEventType.SELECTED_NODE_MODIFIED]:
            self.display_node_properties()

    def guiDefaultLocation(self):
        return QtCore.Qt.DockWidgetArea.RightDockWidgetArea


    # ======= custom

    def display_node_properties(self):

        self.dispPropTree.clear()
        # get first selected item
        if self.guiSelection:
            node = self.guiSelection[0]
        else:
            return


        props = []
        props.extend(ds.PROPS_NODE)
        if isinstance(node, nodes.Axis):
            props.extend(ds.PROPS_AXIS)
        if isinstance(node, nodes.RigidBody):
            props.extend(ds.PROPS_BODY)
        if isinstance(node, nodes.Poi):
            props.extend(ds.PROPS_POI)
        if isinstance(node, nodes.Cable):
            props.extend(ds.PROPS_CABLE)
        if isinstance(node, nodes.Connector2d):
            props.extend(ds.PROPS_CON2D)
        if isinstance(node, nodes.Buoyancy):
            props.extend(ds.PROPS_BUOY_MESH)

        # evaluate properties
        for p in props:
            code = "node.{}".format(p)
            try:
                result = eval(code)

                result = fancy_format(result)

            except:
                result = 'Error evaluating {}'.format(code)

            pa = QtWidgets.QTreeWidgetItem(self.dispPropTree)
            v = QtWidgets.QTreeWidgetItem(pa)
            pa.setText(0, '.' + p)
            v.setText(0, str(result))

        self.dispPropTree.expandAll()

def fancy_format(text):
    # do some formatting
    try:
        a = float(text)
        result = '{:.3f}'.format(a)
        return result

    except:
        pass


    if len(text) > 0:

        try:
            float(text[0])
        except:
            return text

        a = []
        for e in text:
            try:
                r = float(e)
                a.append('{:.3f}'.format(r))
            except:
                a.append(e)

        result = '('
        for e in a:
            result += e
            result += ', '
        result = result[:-2]
        result += ' )'
        return result


    return text

