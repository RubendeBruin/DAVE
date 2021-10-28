# Documentation generation

Documentation for node-properties is automatically generated from the docstrings.
This is done by running the function `make_proplist.py` in the root.

This function reads the docstrings of nodes and exports two files

1. nodes_reference.md
2. proplist.csv

The first is to be copied to the online documentation.
The second is read by DAVE itself.

## Docstring structure

Docstrings are parsed as follows:

- properties for which no setter is defined are marked READ-ONLY
- properties starting with a _ are ignored

The first line of the docstring is the "short" documentation. The "long" documentation is the full docstring.
Do *not* include a . at the end of the docstring (that's just ugly in the limits report)

There are some MAGIC texts in the docstring

- `#NOGUI` signals that the property should not be included in the gui lists such as for limits. Typically because it is not a numerical value.
- `[]` on first line lists units, for example [kN] or [m,m,m]
- `()` on first line gives remarks, for example (global) or (local)

## Getting the documentation

`Scene.give_documentation(Node, propname)` returns the documentation of a node (Node) /property (str) combination
