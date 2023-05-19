# Dissolve

Dissolve is a function that removes information from the model without modifying the model itself.
Ususally this takes the form of removing empty Frames or removing management layers.

There are many situations where a Node can not be dissolved. For example a Point can only be dissolved when nothing is attached to it.
       

## Examples where dissolving is possible
- Removing an intermediate Frame without degrees of freedom.
- Breaking a shackle into up into a rigid-body, points and circles - while looing option to control the shackle type and associated information.
- Breaking a component into its nodes - while losing the reference to the file that it was loaded from.

# Technical

Nodes are partially dissolved by calling node.dissolve_some(). This function attempts to do some dissolving and returns True, message if any work was done. It returns False, message if no work was done.

Node.dissolve() calls self.dissolve_some until no work is done. It then checks if the node itself can be deleted without affecting the model and, if so, deletes itself.

If the node can not be deleted then it is marked as partially-dissolved and an error is raised.
This is checked by setting _is_partially_dissolved when the first dissolved_some() action succeeds.


Node.dissolve is a method that a class can override. By default node.dissolve simply raises an error that nothing can be dissolved.

Node.dissolve_some() is a methods that a class can implement. Because mixins are used the method shall call super().dissolve_some() when it can not do any work itself to ensure that all mixins are called.   

# Flatten

Flatten calls dissolve() on all nodes in the model repeatedly until all of them raise an exception (no work is done).

Again this can result in partially dissolved nodes in the scene.

# Dissolve-lock

Inter-twisted node trees and managers can make it impossible to wholly dissolve a node at once. Calling dissolve_some iteratively will solve this. 


