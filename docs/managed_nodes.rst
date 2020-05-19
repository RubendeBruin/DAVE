Managed Nodes
==============

Nodes or groups of nodes can be "managed" by another node. This makes it possible to standardize common groups of nodes. For example the nodes that make up a shackle or sling.

A node is managed when its "_manager" property is not None.

A managed node:

- should not be edited directly
- shall not export python code (give_python_code returns an empty string)
- depends on its manager

Managers shall:
- take care of the creation of their managed nodes when producing python code
- implement "depends_on"

The export python code routine

- of the manager is called as soon a one of the managed nodes is encountered in the sorted node list, but only if
  all its depends_on properties are satisfied.






Mangers may:
- change the nodes that they manage


