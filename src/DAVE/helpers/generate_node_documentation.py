import numpy as np
from typing import get_type_hints
import enum
import DAVE.nodes as dn
from DAVE.settings import DAVE_ADDITIONAL_RUNTIME_MODULES


def generate_python_code(cls, imports=True):
    skip_list = ["color"]

    code = []
    if imports:
        code.append("import numpy as np")
        code.append(
            "from DAVE.settings import NodePropertyInfo, DAVE_ADDITIONAL_RUNTIME_MODULES, DAVE_NODEPROP_INFO"
        )

    cls_name = cls.__name__

    code.append(
        f"# ===================== Auto-generated documentation registration for {cls_name}"
    )
    code.append(f'cls = DAVE_ADDITIONAL_RUNTIME_MODULES["{cls_name}"]')
    code.append(f"DAVE_NODEPROP_INFO[cls] = dict()")

    for name, what in cls.__dict__.items():
        if type(what) == property:
            # privates
            if name.startswith("_"):  # skip private props
                continue

            # skip-list
            if name in skip_list:
                continue

            # read-only
            read_only = what.fset is None
            if what.__doc__ is None:
                raise ValueError(f"Undocumented property for {cls_name} / {name}")

            # docstr
            doc = what.__doc__

            if "#NOGUI" in doc:
                continue  # skip documentation for these (no practical use for reporting or gui)

            # return type (is same as setter)
            value_type = get_type_hints(what.fget)

            if not value_type:
                raise ValueError(f"{cls_name}.{name} does not have type-hinting set")

            property_type = value_type["return"]

            print(f"{cls_name}.{name} --> {property_type}")

            # figure out if this is a float, int or Node
            if property_type in (int, float, bool):
                is_single = True
            elif property_type in (str, tuple) or "tuple" in str(property_type):
                is_single = False
            elif property_type == np.array:
                is_single = False
            else:
                print(property_type)

                if dn.Node in property_type.mro():
                    is_single = True
                elif isinstance(property_type, enum.EnumMeta):
                    is_single = True
                elif isinstance(property_type, type(dict)):
                    is_single = False
                else:
                    raise ValueError(
                        f"Could not determine what to do with this type: {property_type}"
                    )

            is_single_numeric = property_type in (int, float)
            is_single_settable = is_single and not read_only

            # extract data from docstring
            # short is first row.
            # On first row:
            # unit is part between []
            # remarks is part between ()

            lines = doc.split("\n")
            doc_short = lines[0]

            # scan for units
            if "[" not in doc_short or "]" not in doc_short:
                message = f"{cls_name}.{name} does not have units. First line of documentation should contain units between []. First line is {doc_short}"
                print(message)
                units = ""

                if property_type in (int, float):  # these need to be documented
                    raise ValueError(message)

            else:
                # extract units from doc
                i_start = doc_short.index("[")
                i_end = doc_short.index("]")
                units = doc_short[i_start : i_end + 1]

                doc_short = doc_short.replace(units, "")

            doc_long = doc

            # remarks are things between () IF it is the last thing in the short documentation after removal of the units

            if doc_short.strip().endswith(")"):
                # remarks = 'We have remarks'
                stripped = doc_short.strip()
                i_start = stripped.rindex("(")
                remarks = stripped[i_start:]
                doc_short = doc_short.replace(remarks, "")
                remarks = remarks[1:-1]  # remove the ()
            else:
                remarks = ""

            # propety type as string
            ptype = value_type["return"].__name__

            if ptype in DAVE_ADDITIONAL_RUNTIME_MODULES:
                ptype = f'DAVE_ADDITIONAL_RUNTIME_MODULES["{ptype}"]'
            elif ptype == "array":
                ptype = "np.array"

            # generate python code to generate this info
            code.append("")
            code.append(f"# Property: {name}")
            code.append(f"info = NodePropertyInfo(node_class=cls,")
            code.append(f'                        property_name="{name}",')
            code.append(f"                        property_type={ptype},")
            code.append(f'                        doc_short="""{doc_short}""",')
            code.append(f'                        doc_long = """{doc_long}""",')
            code.append(f'                        units = """{units.strip()}""",')
            code.append(f'                        remarks="""{remarks.strip()}""",')
            code.append(f"                        is_settable={not read_only},")
            code.append(
                f"                        is_single_settable = {is_single_settable},"
            )
            code.append(
                f"                        is_single_numeric = {is_single_numeric}"
            )
            code.append(f"                        )")
            code.append(f'DAVE_NODEPROP_INFO[cls]["{name}"] = info')
            code.append("")

    return code


# ======= Example use ======

if __name__ == "__main__":
    from DAVE import Point

    code = generate_python_code(Point)
    filename = r"C:\data\demo.py"

    with open(filename, "w") as f:
        f.write("\n".join(code))
