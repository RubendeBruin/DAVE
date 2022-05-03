"""Property editor

This is a simple Qt GUI (widget) that creates a qui of editable properties for a single object.
It features a callback to signal change of any of the properties.

See the example in __main__

Supported property types:
- string
- float (int is treated as float)


Input:
- target object
- property names


"""
from dataclasses import dataclass

from PySide2.QtWidgets import *

class PropertyEditorWidget(QDialog):

    def __init__(self, dataobject, prop_names : tuple or list, callback_func, info = None, parent=None):
        super().__init__(parent=parent)

        if isinstance(prop_names, str):
            prop_names = (prop_names,)

        self.setWindowTitle("Edit")

        self.callback_func = callback_func
        self.data_object = dataobject

        # get data-types
        self.prop_types = []
        for prop in prop_names:
            test = getattr(dataobject, prop)
            if isinstance(test, str):
                self.prop_types.append(str)
            elif isinstance(test, (int,float)):
                self.prop_types.append(float)
            elif isinstance(test, (tuple, list)):
                self.prop_types.append(tuple)
            else:
                raise ValueError(f'Unsupported type for property name {prop} with value {test}')

        # build Gui

        layout = QGridLayout()
        self.setLayout(layout)

        self.editors = []


        row = 0
        for prop, kind in zip(prop_names, self.prop_types):

            # label
            label = QLabel(prop)
            layout.addWidget(label, row, 0)

            # editor
            value = getattr(dataobject, prop)
            edit = QLineEdit()

            #   callback
            edit.textChanged.connect(lambda *args, a=row: self.user_changed(a))
            self.editors.append(edit)

            layout.addWidget(edit, row, 1)

            # info
            if info is not None:
                info_label = QLabel(info[row])
                layout.addWidget(info_label, row, 2)

            row += 1

        # _ = layout.columnCount()

        button = QPushButton('Ok')     # Add some space and then a button
        layout.setRowMinimumHeight(row, 20)
        layout.addWidget(button, row+1, 1)
        button.pressed.connect(self.close)

        self.prop_names = tuple(prop_names)
        self.load_data()

    def load_data(self):
        """Fills the editors with the current values in the dataobject"""
        for editor, kind, name in zip(self.editors, self.prop_types, self.prop_names):

            if editor.hasFocus():  # do not fill if control has focus
                continue

            editor.blockSignals(True)


            value = getattr(self.data_object, name)

            if kind == str:
                editor.setText(value)
            elif kind == float:
                editor.setText(str(float(value)))
            elif kind == tuple:
                editor.setText('(' + ', '.join([str(v) for v in value]) + ')')
            else:
                raise ValueError(f'Can not set value for  {name} - unknown type')

            editor.setStyleSheet('background: white')

            editor.blockSignals(False)


    def user_changed(self, i_row):
        print(f'changed {i_row}')

        editor = self.editors[i_row]
        kind = self.prop_types[i_row]
        prop_name = self.prop_names[i_row]

        value = editor.text()

        if kind == float:
            try:
                value=float(value)
            except ValueError:
                editor.setStyleSheet('background:  rgb(255, 170, 127);')
                return
        elif kind == tuple:
            try:
                if not value.strip().startswith('('):
                    value = '(' + value
                if not value.strip().endswith(')'):
                    value = value + ')'
                value = eval(value)
            except:
                editor.setStyleSheet('background:  rgb(255, 170, 127);')
                return


        editor.setStyleSheet('background: white')

        if self.callback_func(prop_name, value):
            self.load_data()


if __name__ == '__main__':
    app = QApplication()

    from DAVE import *
    s = Scene()

    node = s.new_frame('DEMO')


    def callback(prop_name, prop_value):
        print(f'{prop_name} = {prop_value}')
        setattr(node,prop_name,prop_value)

        print(f'position of {node.name} is now {node.position}')

        return True


    prop_names = ('name', 'x', 'y')
    info =       ('','','[m]')

    widget = PropertyEditorWidget(dataobject=node, prop_names=prop_names, info=info, callback_func = callback)

    widget.show()
    app.exec_()





