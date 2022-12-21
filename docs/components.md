# Components (sub-scenes)

A component is a scene within a scene. A component is a single Node (Frame) managing all
the nodes from the imported scene.

The node-names in the imported scene are pre-fixed with the name of the component.

The contents of a component are read from a file.

So component node-data is:
- name
- resource


## Updating a component

Other nodes may depend on nodes in the component. This makes updating tricky. 

The easiest way it to simply re-create the whole scene from python. But performance-wise
this is not the best.

An other option is to reload the component into a temporary scene and sync. But there is no
mechanism for syncing nodes.

Updating a component may also BREAK the model. For example if a point in the component that
a line is connected to does no longer exist in the new component.

## Editing a component

This is just opening that file in the editor.
- store current model
- open component file
- save component file
- open current model




## Would it make sense to store components in the same file as the rest of the model?

Scene.components { dict }

Can be done.
Same limitations apply on updates
Components can be edited by doing `Gui(s.components['name'])`

But what would be the benefit?

- Model is self-contained. Will not be broken in the future

But it breaks the whole idea. So NO.

If you want to embed, then just evaporate.

## Exposed settings

Quite often you want to allow some of the properties of the nodes inside the component to be editable by the user.

This can be done by `exposing` these properties.

To expose a property we need to:
1. define the node (name of the node)
2. define the property (name of the property)
3. define its type? (we can pull that from the settings?) --> scene.give_documentation --> type
4. For the user: a description



This is done as follows:

-  In the .dave file of the component, create a variable `exposed`

```python
exposed = []
exposed.append(('description[str] for use user','node_name','property_name'))
exposed.append(('description2 [str] for use user','node_name2','property_name2'))
s.exposed = exposed
...
```




