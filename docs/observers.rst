Observed nodes
==============

Nodes can observe other nodes. If node A observes node B then node A gets notified when one of the settable properties of B is changed.
An observing node DEPENDS on the observed node

Every Node has a list of observers which are references to other Nodes. This list can be empty.

Whenever a property which is decorated with @node_setter_observable is set, the on_observed_node_changed(changed_node) is called on all observing nodes.


When observed nodes are deleted
--------------------------------

- any node observing the deleted node is deleted as well
