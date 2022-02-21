import csv
from abc import ABC

import DAVE.scene as ds
import DAVE.nodes as dn
import DAVE.settings as settings
import inspect
from typing import get_type_hints
import enum

clsmembers = inspect.getmembers(ds, inspect.isclass)

node_type = list()
prop_name = list()
prop_doc = list()
prop_unit = list()
prop_readonly = list()

md = []

node_property_infos = []

for cls_name, cls in clsmembers:

    if not issubclass(cls, ds.Node):  # Only report nodes
        continue

    for name, what in cls.__dict__.items():

        if type(what) == property:

            # privates
            if name.startswith('_'):  # skip private props
                continue

            # read-only
            read_only = what.fset is None
            if what.__doc__ is None:
                raise ValueError(f'Undocumented property for {cls_name} / {name}')

            # docstr
            doc = what.__doc__

            if '#NOGUI' in doc:
                continue # skip documentation for these (no practical use for reporting or gui)


            # return type (is same as setter)
            value_type = get_type_hints(what.fget)

            if not value_type:
                raise ValueError(f'{cls_name}.{name} does not have type-hinting set')

            property_type = value_type["return"]

            # figure out if this is a float, int or Node
            if property_type in (int, float, bool):
                is_single = True
            elif property_type in (str, tuple) or 'tuple' in str(property_type):
                is_single = False
            else:
                if dn.Node in property_type.mro():
                    is_single = True
                else:
                    if isinstance(property_type,enum.EnumMeta):
                        is_single = True
                    else:
                        raise ValueError(f'Could not determine what to do with this type: {property_type}')

            is_single_numeric = property_type in (int, float)
            is_single_settable= is_single and not read_only

            # extract data from docstring
            # short is first row.
            # On first row:
            # unit is part between []
            # remarks is part between ()

            lines = doc.split('\n')
            doc_short = lines[0]



            # scan for units
            if '[' not in doc_short or ']' not in doc_short:
                message = f'{cls_name}.{name} does not have units. First line of documentation should contain units between []. First line is {doc_short}'
                print(message)
                units = ''

                if property_type in (int,float): # these need to be documented
                    raise ValueError(message)

            else:

                # extract units from doc
                i_start = doc_short.index('[')
                i_end = doc_short.index(']')
                units = doc_short[i_start:i_end+1]

                doc_short = doc_short.replace(units, '')

            doc_long = doc

            # remarks are things between () IF it is the last thing in the short documentation after removal of the units

            if doc_short.strip().endswith(')'):
                # remarks = 'We have remarks'
                stripped = doc_short.strip()
                i_start = stripped.rindex('(')
                remarks = stripped[i_start:]
                doc_short = doc_short.replace(remarks,'')
                remarks = remarks[1:-1] # remove the ()
            else:
                remarks = ''

            info = settings.NodePropertyInfo(node_class=cls,
                                             property_name=name,
                                             property_type=value_type["return"],
                                             doc_short=doc_short,
                                             doc_long = doc_long,
                                             units = units,
                                             remarks=remarks,
                                             is_settable=not read_only,
                                             is_single_settable = is_single_settable,
                                             is_single_numeric = is_single_numeric
                                             )

            node_property_infos.append(info)

filename = settings.RESOURCE_PATH[0] / 'node_prop_info.csv'

with open(filename,'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(node_property_infos[0].header_as_tuple())
    for d in node_property_infos:
        writer.writerow(d.as_tuple())

print(f'>> Created or overwritten {filename}')
