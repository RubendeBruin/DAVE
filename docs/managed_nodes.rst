Managed Nodes
==============

Nodes or groups of nodes can be "managed" by another node. This makes it possible to standardize common groups of nodes. For example the nodes that make up a shackle or sling.

A node is managed when its "manager" property is not None.

A managed node:

- shall not be edited directly.
- shall not export python code (give_python_code returns an empty string)

Managers shall:

- Derive from Manager
- take care of the creation of their managed nodes when producing python code
- implement "depends_on". This is used for sorting the nodes before creating python code. These are the nodes that need to exist before the manager is created.
- implement "managed_nodes" which return a list of all nodes that this manager manages.
- implement "delete". This function deletes the manager and MAY delete managed nodes if needed. Typically a manager would delete the nodes it created.
- for nodes that are not deleted: manager shall release management.

**Editing**

Editing a managed node is only allowed when scene.current_manager is the same manager as the manager of the node.
This is enforced.

So typically the manager implements something like:

.. code-block:: python

    backup = self._scene.current_manager # store
    self._scene.current_manager = self
    # perform changes to nodes
    self._scene.current_manager = backup # restore

**Deleting**

deleting a manger:
- calls delete of that manager, then deletes the manger

deleting a managed node:
- calls delete of that manager

**Example**

.. code-block:: python

    s = Scene()
    a1 = s.new_axis('a1')
    p1 = s.new_poi('p1',parent = a1)
    s1 = s.new_sheave('s1',parent=p1, axis=(0,1,0), radius=1.0)

    a2 = s.new_axis('a2')
    p2 = s.new_poi('p2', parent=a2)
    s2 = s.new_sheave('s2', parent=p2, axis=(0, 1, 0), radius=1.0)

    s.new_geometriccontact('connection',s1,s2)

- The manager creates a few axis system to connect a1 and a2
- The manager sets .manager on s1 and s2, this is because changing one of these would make the connection outdated.

If manager is deleted:
- the created axis systems are deleted,
- management on s1 and s2 is released (set to None)

if a1 is deleted:

- this causes p1 to be deleted
- this causes s1 to be deleted, but, because s1 is managed, the delete method on the manager is called instead. So s1 is not yet deleted
- the delete method of the manager:
- releases the managment on s1 and s2
- **de-connects a1 from the created axis systems** This breaks the connection between a1 and a2
- deletes the created axis
- then the manager itself is deleted
- there are no further remaining nodes depending on a1, so done.

So, even though a2 is slaved to a1, deleting a1 does not result in the deletion of a2 because deleting the managed connection resets the parent of a2 setting is free from a1.

