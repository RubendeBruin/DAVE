"""
- Basic mode: Select nodes based on GUI selection
- Add buttons to select all nodes to the same type or use node-selector to filter
- Nodes vertically, Properties horizontally
- Only display single-settable properties that exist in ALL of the active nodes
- First column to be used for "ALL" of the selection. Changing the value here changes the property for all the selected nodes.
- This column shows "VAR" if values are different.

"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget

from DAVE import Scene
from DAVE.gui.helpers.my_qt_helpers import BlockSigs
from DAVE.visual_helpers.constants import ERROR_COLOR_BACKGROUND


class GriddedNodeEditor(QTableWidget):

    def __init__(self, parent=None, scene : Scene = None, execute_func = None):
        super().__init__(parent)

        if scene is None:
            raise ValueError("Need to provide a scene")
        if execute_func is None:
            raise ValueError("Need to provide an execute function")

        self.execute = execute_func
        self.nodes = []
        self.common = False
        self._scene = scene
        self.itemChanged.connect(self.item_changed)

    def set_nodes(self, nodes):
        self.nodes = nodes
        self.fill()

    def set_common(self, common):
        self.common = common

    def _get_settable_properties(self):
        covered = dict()
        props = None

        for n in self.nodes:
            if type(n) in covered:
                continue
            covered[type(n)] = True

            prop_for_this_node_type = set(self._scene.give_properties_for_node(n,single_settable=True, single_numeric=True))

            if props is None:
                props = prop_for_this_node_type
            else:
                if self.common:
                    props = props.intersection(prop_for_this_node_type)
                else:
                    props = props.union(prop_for_this_node_type)



        props = list(props)
        props.sort()
        return props



    def fill(self):
        # loop over all the node types and get the settable properties
        # try to keep the same input position

        curindex = self.currentIndex()

        with BlockSigs(self):
            props = self._get_settable_properties()

            n_props = len(props)
            n_nodes = len(self.nodes)

            self.clear()
            self.setRowCount(n_nodes + 1)
            self.setColumnCount(n_props)

            self.setHorizontalHeaderLabels(props)
            self.setVerticalHeaderLabels(['ALL'] + [node.name for node in self.nodes])

            for j, prop in enumerate(props):

                values = []

                for i, node in enumerate(self.nodes):

                    doc = self._scene.give_documentation(node, prop)

                    if doc:
                        value = getattr(node, prop)
                        fmt = "{:.3g}"
                        if abs(value) > 1e5:
                            fmt = "{:.0f}"
                        elif abs(value) > 1e3:
                            fmt = "{:.1f}"
                        if value == 0:
                            fmt = "{:.0f}"


                        self.setItem(i+1,j, QTableWidgetItem(fmt.format(value)))

                        editable = doc.is_single_settable and doc.is_single_numeric

                    else:
                        self.setItem(i + 1, j, QTableWidgetItem(''))
                        editable = False

                    # cell can also be read-only if the node manager does not allow it
                    if editable:
                        if node.manager:
                            editable = node.manager.is_property_change_allowed(node, prop)

                    if editable:
                        values.append(value)
                    else:
                        # make cell un-editable
                        self.item(i+1, j).setFlags(self.item(i+1, j).flags() & ~Qt.ItemIsEditable)
                        self.item(i+1, j).setBackground(QBrush(QColor(200,200,200)))

                if len(set(values)) == 1:
                    self.setItem(0, j, QTableWidgetItem(str(values[0])))
                else:
                    self.setItem(0, j, QTableWidgetItem("var"))

            self.resizeColumnsToContents()
            self.resizeRowsToContents()

            if curindex.row() < self.rowCount():
                if curindex.column() < self.columnCount():
                    self.setCurrentIndex(curindex)



    def item_changed(self, item):
        print(item.row(), item.column(), item.text())

        try:
            value = float(item.text())
            item.setBackground(QBrush(QColor(255,255,255)))
        except:
            # mark the cell as invalid
            item.setBackground(QBrush(QColor(*ERROR_COLOR_BACKGROUND)))
            return

        if item.row() == 0:
            rows = range(1, self.rowCount())
        else:
            rows = [item.row()]

        codes = []
        for row in rows:
            node_name = self.nodes[row-1]
            prop_name = self.horizontalHeaderItem(item.column()).text()

            # see if cell is editable
            if not self.item(row, item.column()).flags() & Qt.ItemIsEditable:
                continue

            # see if the value is different from what we had, if that is the case then no need to change it
            if getattr(self.nodes[row-1], prop_name) == value:
                continue

            codes.append(f's["{node_name}"].{prop_name} = {value}')

        code = '\n'.join(codes)

        self.execute(code)






if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(sys.argv)

    s = Scene()


    for i in range(10):
        s.new_point(f"Point {i}", position = (i, i, i))

    s.new_rigidbody('Rigid', position = (10, 10, 10))

    for i in range(10):
        s.new_frame(f"Frame {i}")

    # s['Frame 4'].manager = s['Frame 3']
    def ex(code):
        print(len(code.split('\n')))
        print(code)

    win = GriddedNodeEditor(scene = s, execute_func = ex)

    nodes = s.nodes()

    print(nodes)

    win.set_nodes(nodes)



    win.show()
    sys.exit(app.exec())