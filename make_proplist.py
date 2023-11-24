from pathlib import Path
import inspect

filename = Path(__file__).parent / 'src' / 'DAVE' / 'nds' / 'auto_generated_node_documentation.py'

# first clear the existing file
with open(filename,'w') as f:
    f.write('')


import DAVE.scene as ds

from DAVE.helpers.generate_node_documentation import generate_python_code



clsmembers = inspect.getmembers(ds, inspect.isclass)

code = []
first = True

for cls_name, cls in clsmembers:

    if not issubclass(cls, ds.DAVENodeBase):  # Only report nodes and mixins
        continue


    code.extend(generate_python_code(cls, imports=first))
    first = False


with open(filename,'w') as f:
    f.write('\n'.join(code))
