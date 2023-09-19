from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QDialogButtonBox,
    QTableWidgetItem,
)

from PySide6.QtGui import QColor, QIcon

from DAVE import Scene, Cable

"""
Depending on what "cable" really is, the following settings are exposed:

endA friction
endA max winding angle
endB friction
endB max winding angle

                          Cable          Cable    SlingGrommet*     SlingGrommet          SlingGrommet
                          line           loop       sling           Grommet/circle        Grommet/line
                          
endA friction              no             yes        no              yes                       yes
endA max winding angle     no             yes        no              yes                       yes
endB friction              no             no         no              yes                       yes
endB max winding angle     no             no         no              yes                       yes


* SlingGrommet is a node from the Rigging extension

is_grommet_in_line_mode : In this case either the first or the last friction needs to be None. 

Max_winding_angle is defined for ALL connections
Friction is only defined for the connections where it is applicable

"""


class AdvancedCableSettings(QDialog):
    """
    Dialog to edit the advanced settings of a cable

    Code to apply the settings is generated and stored in self.code (string)
    """

    def __init__(self, cable: "Cable or SlingGrommet"):
        super().__init__()

        self.code = ""

        # store settings
        (
            self.endAFr,
            self.endAMaxWind,
            self.endBFr,
            self.endBMaxWind,
            self.is_grommet_in_line_mode,
        ) = cable._get_advanced_settings_dialog_settings()

        self.cable = cable

        self.setWindowIcon(QIcon(":/icons/cable.png"))

        # create the ui
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        title = f"Editing '{cable.name}'"
        self.setWindowTitle(title)

        self.label = QLabel(
            f"- Friction, if defined, shall be between -1 and 1\n- Max winding angle, if defined, shall be >180"
        )
        self.layout.addWidget(self.label)

        self.loop_label = QLabel(
            f"This is a looped cable, exactly one friction must be empty or all friction must be empty or zero"
        )
        self.loop_label.setWordWrap(True)
        self.layout.addWidget(self.loop_label)

        # make the table
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # make the code label
        self.code_label = QLabel()
        self.layout.addWidget(self.code_label)
        self.code_label.setWordWrap(True)

        # fill the table
        self.is_loop = cable._isloop
        N = len(cable.connections)

        self.table.setRowCount(N)
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(["Friction [-]", "Max winding [deg]"])
        self.table.horizontalHeader().setStretchLastSection(True)

        connection_names = [c.name for c in cable.connections]

        self.table.setVerticalHeaderLabels(connection_names)

        # fill the table with the current values
        if self.is_loop:
            self.loop_label.setVisible(True)
        else:
            self.loop_label.setVisible(False)

        # fill the table with the current values for max winding
        # max winding is defined for all connections

        for i_row in range(N):
            max_wind = cable.max_winding_angles[i_row]
            self.table.setItem(i_row, 1, QTableWidgetItem(max_wind))

        if not self.endAMaxWind:
            it = self.table.item(0, 1)
            it.setFlags(it.flags() & ~Qt.ItemIsEditable)

        if not self.endBMaxWind:
            it = self.table.item(N - 1, 1)
            it.setFlags(it.flags() & ~Qt.ItemIsEditable)

        # fill the table with the current values for friction
        # friction is only defined for the connections where it is applicable

        offset = 0 if self.endAFr else 1
        for i, friction in enumerate(cable.friction):
            if friction is not None:
                friction = str(friction)

            self.table.setItem(i + offset, 0, QTableWidgetItem(friction))

        if not self.endAFr:
            it = self.table.setItem(0, 0, QTableWidgetItem("-"))
            it = self.table.item(0, 0)
            it.setFlags(it.flags() & ~Qt.ItemIsEditable)

        if not self.endBFr:
            self.table.setItem(N - 1, 0, QTableWidgetItem("-"))
            it = self.table.item(N - 1, 0)
            it.setFlags(it.flags() & ~Qt.ItemIsEditable)

        self.buttons = QDialogButtonBox()
        self.buttons.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.table.itemChanged.connect(self.check_data)

        self.check_data()

    def check_data(self) -> bool:
        # all friction (column 0) should be between -1 and 1 or empty
        # all max wind (column 1) should be between 0 and 360 or empty

        N = self.table.rowCount()
        self.table.blockSignals(True)

        result = True

        # Set all backgrounds to "OK"
        for i_row in range(N):
            for i_col in range(2):
                item = self.table.item(i_row, i_col)
                if item is not None:
                    if item.flags() & Qt.ItemIsEditable:
                        item.setBackground(QColor.fromString("white"))
                    else:
                        item.setBackground(QColor.fromRgb(200, 200, 200, 255))

        None_supplied = False
        error = ""

        # friction values
        offset = 0 if self.endAFr else 1

        for i_row in range(len(self.cable.friction)):
            # frictions
            item = self.table.item(i_row + offset, 0)

            value = None
            if item is not None:
                value = item.text()
                if value == "":
                    value = None
                else:
                    try:
                        value = float(value)
                    except:
                        value = -99  # wrong

            if value is not None:
                if value < -1 or value > 1:
                    result = False
                    item.setBackground(QColor.fromRgb(255, 100, 100, 255))
            else:  # item is none
                if self.is_loop:
                    if None_supplied:
                        result = False
                        error = "Only one friction can be empty for a looped cable"
                    None_supplied = True

        if self.is_loop:
            if not None_supplied:
                error = "One friction must be un-defined (empty) for a looped cable"
                result = False

        if self.is_grommet_in_line_mode:
            # either the first or the last entry shall be None

            first_none = False
            if self.table.item(0, 0) is not None:
                if self.table.item(0, 0).text() != "":
                    first_none = True
            else:
                first_none = True

            last_none = False
            if self.table.item(N - 1, 0) is not None:
                if self.table.item(N - 1, 0).text() != "":
                    last_none = True
            else:
                last_none = True

            if (not first_none and not last_none) or (first_none and last_none):
                result = False
                error = "Either the first OR the last friction must be empty for a grommet in line mode"
                self.table.item(0, 0).setBackground(QColor.fromRgb(255, 100, 100, 255))
                self.table.item(N - 1, 0).setBackground(
                    QColor.fromRgb(255, 100, 100, 255)
                )

        # max winding angles

        for i_row in range(N):
            item = self.table.item(i_row, 1)
            if item is not None:
                if item.text() == "":
                    max_wind = 999
                else:
                    try:
                        max_wind = float(item.text())
                    except:
                        max_wind = -99  # wrong
                if max_wind < 180:
                    result = False
                    item.setBackground(QColor.fromRgb(255, 100, 100, 255))

        self.table.blockSignals(False)

        if result:
            self.generate_code()
            self.code_label.setText(self.code)
            self.code_label.setStyleSheet("")

        if error:
            self.code_label.setText(error)
            self.code_label.setStyleSheet("background-color: rgb(255,200,200);")

        return result

    def generate_code(self):
        # create code and set it to self.code
        N = self.table.rowCount()

        friction = []

        offset = 0 if self.endAFr else 1

        for i_row in range(len(self.cable.friction)):
            item = self.table.item(i_row + offset, 0)

            if item is None:
                value = None
            else:
                value = item.text()
                if value == "":
                    value = None
                else:
                    value = float(value)

            if not self.is_loop:
                if value is None:
                    value = 0

            friction.append(value)

        max_wind = []
        for i_row in range(N):
            item = self.table.item(i_row, 1)
            if item is not None:
                if item.text() == "":
                    max_wind.append(999)
                else:
                    max_wind.append(float(item.text()))
            else:
                max_wind.append(999)

        node = f"s['{self.cable.name}']"
        self.code = ""
        self.code += f"{node}.friction = {friction}\n"
        self.code += f"{node}.max_winding_angles = {max_wind}\n"

    def accept(self):
        # update the cable
        # self.cable.friction = self.friction
        # self.cable.max_wind = self.max_wind

        if self.check_data():
            super().accept()


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    s = Scene()
    f = s.new_rigidbody(
        "f", position=(0, 0, -10), fixed=(True, True, False, True, True, True), mass=32
    )

    hook1 = s.new_point("hook1", position=(0, 0, 0))
    hook2 = s.new_point("hook2", position=(1, 0, 0))
    s.new_point("p1", position=(0, 0, 0), parent=f)
    s.new_point("p2", position=(1, 0, 0), parent=f)

    # line
    line = s.new_cable(
        connections=["p1", "hook1", "hook2", "p2"],
        name="line",
        EA=122345,
        friction=[0.05, -0.05],
        length=7,
    )

    # loop
    loop = s.new_cable(
        connections=["p1", "hook1", "hook2", "p2", "p1"],
        name="loop",
        EA=122345,
        friction=[0.05, -0.05, 0, None],
        length=7,
    )

    app = QApplication(sys.argv)

    dialog = AdvancedCableSettings(cable=loop)
    dialog.exec()
    print(dialog.code)

    exec(dialog.code)
