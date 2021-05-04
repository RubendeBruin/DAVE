"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Ruben de Bruin - 2020
"""
from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import sys

"""
GridEdit is a table editor for Qt based on the item-view table widget.

Its purpose is to edit uniform data in table format where each row represents an entity of something. Each column
can have a fixed type: int, float, string or bool. 

It implements some convenience functions such at copy-paste, value checking and adding/removing columns.

Data can be set using a list of similar objects or as just a table of values.

Objects (DataModel):
- the object properties are edited directly

Table values:
- Use setData / getData to set/get the raw data in the table.

Use:
- Define columns
- Assign callbacks (if any)
- Setup (activate_columns)
- SetData or SetDataModel



set column
apply columns
[assing callback]
set data[source] and [row-labels]


datatypes

type : bool ,str, float, int

Columns:
- when using a DataModel: 'id' should correspond to a gettable and settable property of the provided data items.

SetData sets the data. The data is not updated when a cell is changed

SetDataModel sets the data but keeps a reference to the source. The source is updated when a cell is changed.

The buttons to add and remove rows are only shown when a callback is assigned to onAddRow

"""
from PySide2.QtGui import QColor

ColorError = QColor(254, 128, 128)


class Table(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_expand_rows = False

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        # Copy
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):

            rows = [cell.row() for cell in self.selectedIndexes()]
            cols = [cell.column() for cell in self.selectedIndexes()]

            data = "\n".join(
                [
                    "\t".join([self.item(row, col).text() for col in set(cols)])
                    for row in set(rows)
                ]
            )

            print(data)
            QApplication.clipboard().setText(data)

            event.accept()
            return True

        # Paste
        elif event.key() == Qt.Key_V and (event.modifiers() & Qt.ControlModifier):
            row = self.currentRow()
            col = self.currentColumn()

            text = QApplication.clipboard().text()
            rows = text.split("\n")

            if self.auto_expand_rows:
                if self.rowCount() < row + len(rows):
                    self.setRowCount(row + len(rows))

            for i_row, row_text in enumerate(rows):
                cols = row_text.split("\t")
                for i_col, cell in enumerate(cols):
                    item = self.item(row + i_row, col + i_col)
                    if item is not None:
                        item.setText(cell)
                    else:
                        item = QTableWidgetItem(cell)
                        self.setItem(row + i_row, col + i_col, item)

            event.accept()
            return True

        # Delete
        elif event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            for item in self.selectedItems():
                item.setText("")
            event.accept()
            return True


class GridEdit(QWidget):
    def __init__(self, parent):

        super().__init__(parent=parent)

        self.grid = Table(self)
        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.grid)
        self.grid.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # ----- buttons

        self.buttonPlane = QWidget(self)
        self.deleteButton = QPushButton(self.buttonPlane)
        self.addButton = QPushButton(self.buttonPlane)

        self.deleteButton.setText("Delete selected")
        self.addButton.setText("Add")

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(4, 0, 0, 4)
        button_layout.addWidget(self.addButton)
        button_layout.addWidget(self.deleteButton)
        button_layout.addStretch(-1)
        self.buttonPlane.setLayout(button_layout)

        self.layout.addWidget(self.buttonPlane)

        self.addButton.clicked.connect(self.onAddButton)
        self.deleteButton.clicked.connect(self.onDeleteButton)
        self.grid.currentCellChanged.connect(self.onSelectionChanged)

        self.setLayout(self.layout)

        self._columns = []
        self.onEditCallback = None

        self.onAddRow = None
        self.onDeleteRow = None
        self.onRowSelected = None
        self.onChanged = (
            None  # fires if the contents have changed or rows have been added/removed
        )

    def clearColumns(self):
        self._columns = []

    def addColumn(self, id, kind, caption=None):
        """sets the data-types.

        name : description of the data in the column
        kind : data-types. for example str, bool, float, int
        header-text : text to be displayed in the header
        """

        if caption is None:
            caption = id
        self._columns.append({"id": id, "kind": kind, "caption": caption})

    def activateColumns(self):
        n = len(self._columns)
        self.grid.clear()
        self.grid.setColumnCount(n)
        self.grid.setHorizontalHeaderLabels([a["caption"] for a in self._columns])

    def setDataSource(self, datasource, rows=None):
        """Fills the table with given data, sets the datasource

        Data needs to be iterable.

        Each individual items shall
        - be not iterable, and have properties corresponding to the IDs of the columns

        """
        self._setData(datasource, rows)
        self._datasource = datasource

    # ------------------------------------------------------

    def setData(self, data, row_names=None, allow_add_or_remove_rows=True):
        """Fills the table with given data

        Data needs to be iterable.

        Each individual items shall
        - be iterable with the same length as the number of columns
        """

        self.grid.blockSignals(True)

        if allow_add_or_remove_rows:
            self.onAddRow = self.newRow
            self.onDeleteRow = self.deleteRow

        self._setData(data, row_names)
        self._datasource = None
        self.grid.auto_expand_rows = allow_add_or_remove_rows

        self.grid.blockSignals(False)

    def getData(self):
        """Returns the cell-contents as a list of rows

        Invalid entries are returned as None
        """
        data = []

        for i_row in range(self.grid.rowCount()):
            row = []
            for i_col, col in enumerate(self._columns):
                kind = col["kind"]
                value = self.getCellValue(i_row, i_col, kind)
                row.append(value)
            data.append(tuple(row))
        return tuple(data)

    def newRow(self, current_position):
        if current_position < 0:
            self.grid.insertRow(0)
        else:
            self.grid.insertRow(current_position)

    def deleteRow(self, current_position, void):
        self.grid.removeRow(current_position)

    # --------------------------------------------------

    def highlight_invalid_data(self):
        self.grid.blockSignals(True)
        for icol in range(self.grid.columnCount()):
            kind = self._columns[icol]["kind"]
            for irow in range(self.grid.rowCount()):
                if self.getCellValue(irow, icol, kind) is None:
                    self.grid.item(irow, icol).setBackground(ColorError)

        self.grid.blockSignals(False)
    def _setData(self, datasource, row_names):

        try:
            self.grid.itemChanged.disconnect()
        except:
            pass

        self.grid.clearContents()
        self.grid.setRowCount(len(datasource))

        def setItem(irow, icol, kind, value):
            if kind == bool:
                cb = QCheckBox()
                cb.setChecked(value)
                self.grid.setCellWidget(irow, icol, cb)
                cb.toggled.connect(self.onCellEdited)
            else:
                tg = QTableWidgetItem(str(value))
                self.grid.setItem(irow, icol, tg)

        for irow, row in enumerate(datasource):
            try:
                for icol, item in enumerate(row):
                    setItem(irow, icol, self._columns[icol]["kind"], item)
            except:

                for icol in range(len(self._columns)):  # iterate over columns
                    setItem(
                        irow,
                        icol,
                        self._columns[icol]["kind"],
                        getattr(row, self._columns[icol]["id"]),
                    )

        if row_names is not None:
            self.grid.setVerticalHeaderLabels(row_names)
            self.grid.verticalHeader().setVisible(True)
        else:
            self.grid.verticalHeader().setVisible(False)

        self.grid.itemChanged.connect(self.onCellEdited)

        self.buttonPlane.setVisible(self.onAddRow is not None)

    def _get_row_id(self, row):
        if self.grid.verticalHeader().isVisible():
            name = self.grid.verticalHeaderItem(row).text()
        else:
            name = row

        return name

    def _get_active_row_id(self):
        row = self.grid.currentRow()
        return self._get_row_id(row)

    def getCellValue(self, row, col, kind):
        try:
            if kind == bool:
                value = self.grid.cellWidget(row, col).isChecked()
            elif kind == float:
                value = float(self.grid.item(row, col).text())
            else:
                value = self.grid.item(row, col).text()

            return value
        except:
            return None

    def onCellEdited(self):

        self.grid.blockSignals(True)

        row = self.grid.currentRow()
        col = self.grid.currentColumn()

        kind = self._columns[col]["kind"]

        value = self.getCellValue(row, col, kind)
        if value is None:
            self.grid.item(row, col).setBackground(ColorError)
        else:
            if self.grid.item(row, col).backgroundColor() == QColor():
                pass
            else:
                self.grid.item(row, col).setData(QtCore.Qt.BackgroundRole, None)

        old_value = None

        # Apply the change to the element
        if self._datasource is not None:
            old_value = getattr(self._datasource[row], self._columns[col]["id"])
            setattr(self._datasource[row], self._columns[col]["id"], value)

        if self.onEditCallback is not None:
            property_id = self._columns[col]["id"]
            kind = self._columns[col]["kind"]

            if self._datasource is None:
                element = None
            else:
                element = self._datasource[row]

            self.onEditCallback(
                row,
                col,
                value,
                self._get_active_row_id(),
                element,
                property_id,
                kind,
                old_value,
            )

        self.grid.setCurrentCell(row, col)
        self.grid.setFocus()

        self.grid.blockSignals(False)

        if self.onChanged is not None:
            self.onChanged()

    def onSelectionChanged(self):
        if self.onRowSelected is not None:
            self.onRowSelected(self._get_active_row_id())

    def onDeleteButton(self):
        if self.onDeleteRow is not None:

            # see if we have a multiple selection
            selected_rows = [ind.row() for ind in self.grid.selectedIndexes()]
            if not selected_rows:
                selected_rows = [self.grid.currentRow()]

            for row in reversed(selected_rows):
                self.onDeleteRow(row, self._get_row_id(row))

            if self.onChanged is not None:
                self.onChanged()

    def onAddButton(self):
        if self.onAddRow is not None:
            self.onAddRow(self.grid.currentRow())
            if self.onChanged is not None:
                self.onChanged()


"""
========================================================================
    Examples start here 
========================================================================    

"""


class DemoElement:
    def __init__(self):
        self.name = "Name"
        self.value = 41
        self.cando = True


if __name__ == "__main__":

    qApp = QApplication(sys.argv)

    if True:  # Example with raw data

        ge = GridEdit(None)

        # # Example with raw data
        ge.addColumn("x", float)
        ge.addColumn("y", float)
        ge.addColumn("z", float)
        ge.activateColumns()

        ge.setData([[1, 2, 3], [4, 5, 6.789]], allow_add_or_remove_rows=True)

        def change(*x):
            print(ge.getData())

        ge.onChanged = change

        ge.show()
        code = qApp.exec_()

        print(ge.getData())

    else:  # example with model data

        ge = GridEdit(None)



        # Example with elements - These names correpond to properties of the objects
        ge.addColumn("name", str)
        ge.addColumn("value", int)
        ge.addColumn("cando", bool)

        e1 = DemoElement()
        e2 = DemoElement()
        e2.name = "Element2"
        e3 = DemoElement()

        collection = [e1, e2, e3]

        ge.activateColumns()

        def add(_):
            collection.append(DemoElement())
            ge.setDataSource(collection)

        ge.onAddRow = add
        ge.setDataSource(collection, ["These", "Are", "Objects"])

        def do_something(*varargin):
            print(varargin)

        ge.onEditCallback = do_something

        ge.show()
        code = qApp.exec_()

        print(collection)

    sys.exit(code)
