"""Property editor widget / dialog

This is a simple Qt GUI (widget) that creates a qui of editable properties for a single object.
It features a callback to signal change of any of the properties.

See the example in __main__

Supported property types:
- string
- float
- int
- tuple

Input:
- setting names
- setting types
- getter callback
- setter callback
- into (optional)
- parent (optional)

An inherited class `PropertyEditorWidget` exists for convenience with objects. For this class
property types and the getter function can be replaced with a reference to an object. This works
if all settings are properties of the object.



"""
from dataclasses import dataclass
from collections.abc import Callable

from PySide2.QtWidgets import *

class PropertyEditorDialog(QDialog):

    def __init__(self, prop_names : tuple or list, prop_types : tuple or list, getter_callback : Callable[str, any], setter_callback : Callable[str, any], info = None, parent=None):

        # checks

        assert len(prop_types) == len(prop_names)


        #
        super().__init__(parent=parent)

        self.setWindowTitle("Edit")

        self.setter_callback = setter_callback
        self.getter_callback = getter_callback
        self.prop_types = prop_types

        # build Gui

        layout = QGridLayout()
        self.setLayout(layout)

        self.editors = []


        row = 0
        for prop, kind in zip(prop_names, self.prop_types):

            # label
            label = QLabel(prop)
            layout.addWidget(label, row, 0)

            if kind==bool:
                edit = QCheckBox()
                edit.toggled.connect(lambda *args, a=row: self.user_changed(a))
            else:
                edit = QLineEdit()
                edit.textChanged.connect(lambda *args, a=row: self.user_changed(a))

            self.editors.append(edit)

            layout.addWidget(edit, row, 1)

            # info
            if info:
                if len(info)>row:
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
        for editor, kind, prop_name in zip(self.editors, self.prop_types, self.prop_names):

            if editor.hasFocus():  # do not fill if control has focus
                continue

            editor.blockSignals(True)

            value = self.getter_callback(prop_name)

            if kind == bool:
                editor.setChecked(value)
            elif kind == str:
                editor.setText(value)
            elif kind == float:
                editor.setText(str(float(value)))
            elif kind == int:
                editor.setText(str(int(value)))
            elif kind == tuple:
                editor.setText('(' + ', '.join([str(v) for v in value]) + ')')
            else:
                raise ValueError(f'Can not represent value for  {prop_name} - unknown type. Value is {str(value)}')

            editor.setStyleSheet('background: white')

            editor.blockSignals(False)


    def user_changed(self, i_row):
        editor = self.editors[i_row]
        kind = self.prop_types[i_row]
        prop_name = self.prop_names[i_row]

        if kind == bool:
            value = editor.isChecked()
        else:
            value = editor.text()

            if kind == float:
                try:
                    value=float(value)
                except ValueError:
                    editor.setStyleSheet('background:  rgb(255, 170, 127);')
                    return
            elif kind == int:
                try:
                    value=int(value)
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

        if self.setter_callback(prop_name, value):
            self.load_data()



class PropertyEditorWidget(PropertyEditorDialog):

    def __init__(self, dataobject, prop_names : tuple or list, callback_func, info = None, parent=None):

        self.callback_func = callback_func
        self.data_object = dataobject

        prop_types = []
        for prop in prop_names:
            test = getattr(dataobject, prop)
            if isinstance(test, str):
                prop_types.append(str)
            elif isinstance(test, bool):  # isinstance(0, bool) --> false
                prop_types.append(bool)
            elif isinstance(test, (float, int)): # can not differentiate between int and float
                prop_types.append(float)
            elif isinstance(test, (tuple, list)):
                prop_types.append(tuple)
            else:
                raise ValueError(f'Unsupported type for property name {prop} with value {test}')

        PropertyEditorDialog.__init__(self, prop_names=prop_names,
                                      prop_types=prop_types,
                                      setter_callback=self.set_data,
                                      getter_callback=self.get_data,
                                      info=info,
                                      parent=parent)

    def get_data(self, name):
        value = getattr(self.data_object, name)
        return value

    def set_data(self, name, value):
        self.callback_func(name, value)



if __name__ == '__main__':
    app = QApplication()

    use_dataobject = False

    #
    if not use_dataobject:

        names = ('een','twee','string','float','tuple','yes or no')
        types = (str, int, str, float,tuple, bool)

        database = dict()
        database['een'] = 'een'
        database['twee'] = 41
        database['string'] = 'een'
        database['float'] = 1.2345
        database['tuple'] = (1,2,'vijftien')
        database['yes or no'] = False

        info = ('','','','<-- hint for float')

        def getvalue(name):
            return database[name]

        def setvalue(name, value):
            database[name] = value
            print(f'database = {database}')


        widget = PropertyEditorDialog(prop_names=names, prop_types=types, getter_callback=getvalue, setter_callback=setvalue, info=info)

    else:

        from DAVE import *
        s = Scene()

        node = s.new_frame('DEMO')


        def callback(prop_name, prop_value):
            print(f'{prop_name} = {prop_value}')
            setattr(node,prop_name,prop_value)

            print(f'position of {node.name} is now {node.position}')

            return True


        prop_names = ('name', 'x', 'y','fixed_x')
        info =       ('','','[m]','-')

        widget = PropertyEditorWidget(dataobject=node, prop_names=prop_names, info=info, callback_func = callback)

    # -------- Example without dataobject


    widget.show()
    app.exec_()




