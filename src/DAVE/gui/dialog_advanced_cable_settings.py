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



class AdvancedCableSettings(QDialog):
    """
    Dialog to edit the advanced settings of a cable

    Code to apply the settings is generated and stored in self.code (string)
    """

    def __init__(self, cable : Cable):

        super().__init__()
        self.code = ''
        self.cable = cable

        self.setWindowIcon(QIcon(":/icons/cable.png"))

        # create the ui
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        title = f"Editing '{cable.name}'"
        self.setWindowTitle(title)

        self.label = QLabel(f"- Friction, if defined, shall be between -1 and 1\n- Max winding angle, if defined, shall be between 180 and 360")
        self.layout.addWidget(self.label)

        self.loop_label = QLabel(f"This is a looped cable, exactly one friction must be empty or all friction must be empty or zero")
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
            offset = 0
            self.loop_label.setVisible(True)
        else:
            offset = 1
            self.loop_label.setVisible(False)

            # disable the first row
            self.table.setRowHidden(0, True)



        for i_row in range(N-1-offset):
            friction = cable.friction[i_row-offset]
            max_wind = cable.max_winding_angles[i_row-offset]

            if friction is not None:
                friction = str(friction)
            if max_wind is not None:
                max_wind = str(max_wind)

            self.table.setItem(i_row+offset, 0, QTableWidgetItem(friction))
            self.table.setItem(i_row+offset, 1, QTableWidgetItem(max_wind))

        # disable the last row
        self.table.setRowHidden(N-1, True)




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

        for i_row in range(N):
            for i_col in range(2):
                item = self.table.item(i_row, i_col)
                if item is not None:
                    item.setBackground(QColor.fromString('white'))

        None_supplied = False
        error = ""

        for i_row in range(N-1):

            # frictions
            item = self.table.item(i_row, 0)

            value = None
            if item is not None:
                value = item.text()
                if value == '':
                    value = None
                else:
                    try:
                        value = float(value)
                    except:
                        value = -99 # wrong


            if value is not None:
                if value < -1 or value > 1:
                    result = False
                    item.setBackground(QColor.fromRgb(255,100,100,255))
            else: # item is none
                if self.is_loop:
                    if None_supplied:
                        result = False
                        error = "Only one friction can be empty for a looped cable"
                    None_supplied = True

        if self.is_loop:
            if not None_supplied:
                error = "At one friction must be empty for a looped cable"
                result = False

            # max winding angles
        for i_row in range(N):
            item = self.table.item(i_row, 1)
            if item is not None:
                try:
                    max_wind = float(item.text())
                except:
                    max_wind = -99 # wrong
                if max_wind < 180:
                    result = False
                    item.setBackground(QColor.fromRgb(255,100,100,255))

        self.table.blockSignals(False)

        if result:
            self.generate_code()
            self.code_label.setText(self.code)
            self.code_label.setStyleSheet('')

        if error:
            self.code_label.setText(error)
            self.code_label.setStyleSheet("background-color: rgb(255,200,200);")

        return result

    def generate_code(self):
        # create code and set it to self.code
        N = self.table.rowCount()

        friction = []

        if self.is_loop:
            offset = 0
        else:
            offset = 1

        for i_row in range(N-1-offset):
            item = self.table.item(i_row+offset, 0)

            if item is None:
                value = None
            else:
                value = item.text()
                if value == '':
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
                max_wind.append(float(item.text()))
            else:
                max_wind.append(999)

        node = f"s['{self.cable.name}']"
        self.code = ''
        if any(friction):
            self.code += f"{node}.friction = {friction}\n"
        self.code += f"{node}.max_winding_angles = {max_wind}\n"



    def accept(self):
        # update the cable
        # self.cable.friction = self.friction
        # self.cable.max_wind = self.max_wind

        if self.check_data():
            super().accept()



if __name__ == '__main__':
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
    
    c = s.new_cable(
        connections=["p1", "hook1", "hook2", "p2", "p1"],
        name="cable",
        EA=122345,
        friction=[0.05, -0.05, 0, None],
        length=7,
    )


    app = QApplication(sys.argv)
    dialog = AdvancedCableSettings(cable = c)
    dialog.exec()
    print(dialog.code)
