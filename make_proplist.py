from abc import ABC

import DAVE.scene as ds
import inspect

import pandas as pd

clsmembers = inspect.getmembers(ds, inspect.isclass)

node_type = list()
prop_name = list()
prop_doc = list()
prop_unit = list()
prop_type = list()
prop_readonly = list()

md = []

for c in clsmembers:
    cls_name = c[0]
    cls = c[1]

    if not issubclass(cls, ds.Node):  # Only report nodes
        continue

    # Explicilty exclude some classes from the markdown documentation
    if (cls == ds.Node) or \
        (cls == ds.CoreConnectedNode) or \
        (cls == ds.Manager) or \
        (cls == ds.NodeWithCoreParent) or \
        (cls == ds._Area) or \
        (cls == ds.NodeWithParentAndFootprint):
        do_md = False
    else:
        do_md = True

    # Explicitly exclude _AREA
    if cls==ds._Area:
        continue

    if cls == ds.WindArea or cls == ds.CurrentArea:
            cls = ds._Area

    # markdown
    if do_md:

        md.append(f'#### {cls_name}')
        dc = cls.__doc__
        if dc:
            md.append(dc)
        md.append('|  Property | Read-Only  | Documentation ')
        md.append('|:---------------- |:------------------------------- |:---------------- |')

    for name, what in cls.__dict__.items():



        if type(what) == property:

            if name.startswith('_'):  # skip private props
                continue

            md_line = f'{name}'

            if what.fset is None:
                print(f'{name} (READ ONLY)')
                prop_readonly.append(True)

                md_line += ' | Read-only | '

            else:
                print(f'{name}')
                prop_readonly.append(False)

                md_line += ' |  | '

            print(what.__doc__)

            if what.__doc__:
                md_line += what.__doc__.replace('\n','<br>') + '|'
            else:
                md_line += '|'

            # store results
            node_type.append(cls_name)
            prop_name.append(name)
            prop_doc.append(what.__doc__)

            if do_md:
                md.append(md_line)

index = pd.MultiIndex.from_arrays([node_type, prop_name, prop_readonly],
                                  names = ('class','property','readonly'))

data = pd.DataFrame([prop_doc], columns = index)

print(data.transpose())

dt = data.transpose()
dt.columns = ['doc']

dt.to_csv(r'src\DAVE\resources\proplist.csv')

print('\n'.join(md))


with open('docs/nodes_reference.md','w') as f:
    f.write('\n'.join(md))
