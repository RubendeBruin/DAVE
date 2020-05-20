Managed Nodes
==============

Nodes or groups of nodes can be "managed" by another node. This makes it possible to standardize common groups of nodes. For example the nodes that make up a shackle or sling.

A node is managed when its "_manager" property is not None.

A managed node:

- should not be edited directly
- shall not export python code (give_python_code returns an empty string)

Managers shall:

- Derive from Manager
- take care of the creation of their managed nodes when producing python code
- implement "depends_on". This is used for sorting the nodes before creating python code
- implement "managed_nodes"
- implement "delete". This function deletes the manager and MAY delete managed nodes if needed.

Mangers may:
- change the nodes that they manage


