# Watches

Purpose:

make interesting properties of nodes available for the user for quick access and reporting.



**Isn't a watch a limit without limit?** No, watches are less formal.



|         | Watch                                                        | Limit                                                        |
| ------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| stored  | in node                                                      | in node                                                      |
| as      | collection of objects. No enforced relation to a specific property | dictionary with property as key. This means only a single limit can be defined for each property |
|         | can be anything                                              | defines UC, needs to be a single number                      |
| used in | reporting, for information                                   | optimization, reporting, colors                              |
|         | can have a condition to show                                 | has a numerical limit                                        |
|         | has a sign                                                   | is always positive                                           |
|         | can the limits via the UC                                    |                                                              |



Watch [description]

- evaluate
- 



Differences between watches and limits

- Multiple watches can be defined on a single property

- Watches do not have a limit

- Watches do not contribute to the UC

  

Examples:

- tilt_x and tilt_y of a lifted object
- sideload on a liftpoint
- UC of an item (although this is already a "limit")



What:

- any property of any node

- add a description as well to override the standard text? (force can be more clear than connection_force_z)

- evaluated python code with `self` as node and `s` as scene such that for example a force can be reported in tonnes using `self.force / s.g`

  
  
  

Use where:

- in the GUI in a dedicated widget
- as a report over timeline, for example using a graph over timeline steps
- as a report for a scene
- in the 3d view using the labels



Store what:

- node

- property / code to be evaluated

- optional: description <-- mandatory : key

- condition of when to become visible (evaluated to be True) with `value` as actual value

Store how:

- Watches are a `dictionary` of of watch objects. The key is the description of the watch.

  

Store where:

- Watches are stored in the Node they watch
- But saved together with the scene (just like limits)
- Consequences:
  - Watches defined in components get loaded with the component
  - But can be overridden in scene.
  - So we need to keep track on what was loaded with the component somehow. 
    - Store a list of dict keys when loading??
    - Store a copy of the dict after loading and only save the values that differ.