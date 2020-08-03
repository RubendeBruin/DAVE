Observed nodes
==============

Nodes can observe other nodes. If node A observes node B then node A gets notified when one of the settable properties of B is changed.

Every Node has a list of observers. This list can be empty.

- observers are function references?
- observers are objects?

on_observed_node_changed(changed_node)