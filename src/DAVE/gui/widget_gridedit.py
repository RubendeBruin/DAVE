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

from DAVE import Scene, DG
from DAVE.gui.helpers.my_qt_helpers import BlockSigs
from DAVE.visual_helpers.constants import ERROR_COLOR_BACKGROUND


def smart_format(value: float):
    # convert to string with variable precision
    if value == 0:
        return "0"
    elif abs(value) > 1e6:
        return f"{value:.0f}"
    elif abs(value) > 1e3:
        return f"{value:.1f}"
    else:
        return f"{value:.3f}"


class GriddedNodeEditor(QTableWidget):

    def __init__(self, parent=None, scene: Scene = None, execute_func=None):
        super().__init__(parent)

        if scene is None:
            raise ValueError("Need to provide a scene")
        if execute_func is None:
            raise ValueError("Need to provide an execute function")

        self.execute = execute_func
        self.nodes = []
        self.common = False
        self.sorted = True
        self._scene = scene
        self.itemChanged.connect(self.item_changed)

    def set_nodes(self, nodes):
        # if self.nodes == nodes:
        #     return
        self.nodes = nodes
        self.fill()

    def set_common(self, common):
        if self.common == common:
            return
        self.common = common
        self.fill()

    def set_sorted(self, sorted):
        if self.sorted == sorted:
            return
        self.sorted = sorted
        self.fill()

    def _get_settable_properties(self):
        covered = dict()
        props = None

        for n in self.nodes:
            if type(n) in covered:
                continue
            covered[type(n)] = True

            prop_for_this_node_type = set(
                self._scene.give_properties_for_node(
                    n, single_settable=True, single_numeric=True
                )
            )

            if props is None:
                props = prop_for_this_node_type
            else:
                if self.common:
                    props = props.intersection(prop_for_this_node_type)
                else:
                    props = props.union(prop_for_this_node_type)

        if props is None:  # nothing selected
            return []

        props = list(props)
        props.sort()
        return props

    def _nodes_as_displayed(self):
        nodes = list(self.nodes)
        if self.sorted:
            nodes.sort(key=lambda x: x.name)
        return nodes

    def fill(self):
        # loop over all the node types and get the settable properties
        # try to keep the same input position

        curindex = self.currentIndex()

        with BlockSigs(self):

            props = self._get_settable_properties()

            nodes = self._nodes_as_displayed()

            n_props = len(props)
            n_nodes = len(self.nodes)

            self.clear()
            self.setRowCount(n_nodes + 1)
            self.setColumnCount(n_props)

            self.setHorizontalHeaderLabels(props)
            self.setVerticalHeaderLabels(["ALL"] + [node.name for node in nodes])

            for j, prop in enumerate(props):

                values = []

                for i, node in enumerate(nodes):

                    doc = self._scene.give_documentation(node, prop)

                    if doc:
                        value = getattr(node, prop)

                        self.setItem(i + 1, j, QTableWidgetItem(smart_format(value)))

                        editable = doc.is_single_settable and doc.is_single_numeric

                    else:
                        self.setItem(i + 1, j, QTableWidgetItem(""))
                        editable = False

                    # cell can also be read-only if the node manager does not allow it
                    if editable:
                        if node.manager:
                            editable = node.manager.is_property_change_allowed(
                                node, prop
                            )

                    if editable:
                        values.append(value)
                    else:
                        # make cell un-editable
                        self.item(i + 1, j).setFlags(
                            self.item(i + 1, j).flags() & ~Qt.ItemIsEditable
                        )
                        self.item(i + 1, j).setBackground(QBrush(QColor(200, 200, 200)))

                if len(set(values)) == 1:
                    self.setItem(0, j, QTableWidgetItem(smart_format(values[0])))
                else:
                    self.setItem(0, j, QTableWidgetItem("var"))

            self.resizeColumnsToContents()
            self.resizeRowsToContents()

            if curindex.row() < self.rowCount():
                if curindex.column() < self.columnCount():
                    self.setCurrentIndex(curindex)

    def item_changed(self, item):

        with BlockSigs(self):
            try:
                value = float(item.text())
                item.setBackground(QBrush(QColor(255, 255, 255)))
            except:
                # mark the cell as invalid
                item.setBackground(QBrush(QColor(*ERROR_COLOR_BACKGROUND)))
                return

        if item.row() == 0:
            rows = range(1, self.rowCount())
        else:
            rows = [item.row()]

        nodes = self._nodes_as_displayed()

        codes = []
        for row in rows:
            node_name = nodes[row - 1]
            prop_name = self.horizontalHeaderItem(item.column()).text()

            # see if cell is editable
            if not self.item(row, item.column()).flags() & Qt.ItemIsEditable:
                continue

            # see if the value is different from what we had, if that is the case then no need to change it
            if getattr(nodes[row - 1], prop_name) == value:
                continue

            codes.append(f's["{node_name}"].{prop_name} = {value}')

        code = "\n".join(codes)
        #
        if code:
            self.execute(code)
            self.fill()


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(sys.argv)

    s = Scene()

    for i in range(10):
        s.new_point(f"Point {i}", position=(i, i, i))

    s.new_rigidbody("Rigid", position=(10, 10, 10))

    for i in range(10):
        s.new_frame(f"Frame {i}")

    DG(s, autosave=False)
    #
    # # s['Frame 4'].manager = s['Frame 3']
    # def ex(code):
    #     print(len(code.split('\n')))
    #     print(code)
    #
    #
    # win = GriddedNodeEditor(scene = s, execute_func = ex)
    #
    # nodes = s.nodes()
    #
    # print(nodes)
    #
    # win.set_nodes(nodes)
    #
    #
    #
    # win.show()
    # sys.exit(app.exec())
