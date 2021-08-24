# Groups

Nodes can be combined to create more complex nodes. For example:

- Combine multiple beams and axis into a segmented beam
- Combine cables, sheaves and bodies into a sling
- Combine axis into a geometric contact

A few mechanisms are introduced to enable the control of these groups as if it were a single node.
These mechanisms are:

- Managers: A managed node is controlled completely by another node
- Observers: An observed node will notify its observer of any changes

These mechanisms are implemented at Node level and are thus available and should be implemented for every node type.

And then there is the issue of Node modification

- Node modification: A node may change other nodes when it is created. Most notably the geometric-contact node changes the parent of the child node. Not managing this correctly may result in circular references when trying to sort the nodes by dependancy. 


## Node modification example

 
- axis 1
    - point 1
        - circle 1
            - geometric contact
                - ... some more axis ...
                  -  axis 2
                    - point 2
                        - circle 2
                        
Geometric contact depends on circle2. (can only be created when circle 2 exists)
Circle 2 depends on point 2 and axis 2
Axis 2 depends on the manager.

This is a circular reference, so something needs to take care of this. 



## Observed nodes

Nodes can observe other nodes. If node A observes node B then node A gets notified when one of the settable properties of B is changed.
An observing node DEPENDS on the observed node

Every Node has a list of observers which are references to other Nodes. This list can be empty.

Whenever a property which is decorated with @node_setter_observable is set, the on_observed_node_changed(changed_node) is called on all observing nodes.

### Deleting

- When a node is deleted, any node observing the deleted node is deleted as well


## Managed Nodes

Nodes or groups of nodes can be "managed" by another node. This makes it possible to standardize common groups of nodes. For example the nodes that make up a shackle or sling.

A node is managed when its "manager" property is not None.

A managed node:

- shall not be edited directly.


Managers shall:

- Derive from Manager
- implement "depends_on". This is used for sorting the nodes before creating python code. These are the nodes that need to exist before the manager is created.
- implement "managed_nodes" which return a list of all nodes that this manager manages.
- implement "delete". This function deletes the manager and MAY delete managed nodes if needed. Typically a manager would delete the nodes it created.
- implement "creates(node)". This function returns True if the manager creates node "node". This means no python code needs to be exported for node "node"
- take care of the creation of the managed nodes for which creates(node) returns True.

Managers may:

- change the parent of a managed node and
- change the _parent_for_code_export property of that node (see circular references)


### Editing

Editing a managed node is only allowed when scene.current_manager is the same manager as the manager of the node.
This is enforced by adding the @node_setter_manageable decorator to any setter of any node.

So typically the manager implements something like:

```python
with ClaimManagement(scene, manager):
    # perform changes to nodes
    managed_node.position = 23
```

### Deleting

deleting a manger:
- calls delete method of that manager, then deletes the manger

deleting a managed node:
- calls delete of the manager

- for nodes that are not deleted: manager shall release management.

A short-cut for releasing management of a managed node is `n._manager = None`

When a manager is deleted it will delete all the nodes it created. This may trigger the deletion of
depending nodes.

#### Example

```python
 s = Scene()
a1 = s.new_frame('a1')
p1 = s.new_poi('p1', parent=a1)
s1 = s.new_sheave('s1', parent=p1, axis=(0, 1, 0), radius=1.0)

a2 = s.new_frame('a2')
p2 = s.new_poi('p2', parent=a2)
s2 = s.new_sheave('s2', parent=p2, axis=(0, 1, 0), radius=1.0)

s.new_geometriccontact('connection', s1, s2)
```

- The manager creates a few axis systems between a1 and a2
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

So, even though a2 is slaved to a1, deleting a1 does not result in the deletion of a2 because deleting the managed connection resets the parent of a2 setting it free from a1.

### Issues with managers

Managers can only manage WHOLE nodes, even though only a few properties need to be managed

## The circular reference thing

The solution is to create axis2 without a parent.

To do so:

- sort_nodes_by_dependency needs to know that the parent of axis2 will be changed by geometric contact
- the export code of axis 2 (Axis) needs to export parent as None

This is implemented as follows. 

---> NodeWithParent._parent_for_export ==
- True : use parent
- None : use None
- Node : use that Node