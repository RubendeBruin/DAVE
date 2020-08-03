Observed nodes
==============

Nodes can observe other nodes. If node A observes node B then node A gets notified when one of the settable properties of B is changed.

Every Node has a list of observers which are references to other Nodes. This list can be empty.

Whenever a property which is decorated with @node_setter_observable is set, the on_observed_node_changed(changed_node) is called on all observing nodes.


When observed nodes are deleted
--------------------------------

- no action is taken by the observation framework 
- if the observing node has the observed node in its "depends on" list, then the observing node will be deleted as well

