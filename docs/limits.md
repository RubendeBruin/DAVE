# Limits

Some nodes may have structural limits: 
- maximum tension in a cable,
- sideload on a padeye,
  

Geometrical limits:
- minimum distance between two points
- maximum heel angle
- displacement (angular or linear)

**Purpose: define the limits of nodes such that it is possible to see if a situation is allowable**

Limits:
- applicable to any single-values property
- maximum-absolute value
- minimum value
- maximum value


Uses:
- mooring analysis
- cog envelope


## Storing



Node | Property | range(min,max) | abs(max) | active |
-----|----------|----------|----------|----------|
Sling | Tension |   | 1000 | X |
Barge | x | 100 , 110 | |  X
Barge | heel |  | 1 | 
Point | fx |  | 50 |
Point | fy |  | 50 |
Point | force |  | 80 | X
Barge | Heading | 350 , 10 | | THIS DOES NOT WORK*


`*` Work-around for heading: place a Frame in the target-heading. Create a 6D spring between the
two. Limit the rz of that 6D spring

> Either MAX-ABS (single number) or a (min, max) [tuple or list] 


`s['node'].limits['tension'] = 100  # define as max-abs`

`s['node'].limits['x'] = (50,100)  # define as range`


> or a string that need to be evaluated to return the UC - is this needed? eg: `(1-cos(value)) / 0.1`


## Saving / Loading

Dictionary in node `Limits['property']`.

The dict is part of `Node`, so all nodes have one.

Saving is done by the *Scene* AFTER exporting all nodes. So the limits are applied AFTER loading the model.
This gives the opportunity to override default limits set in imported models or managed nodes.


## Calculating the UC:

Calculating the UC is implemented in `Node`.

the governing of:

- range: distance from midpoint
- based on max-abs: |actual| / max-abs

actual = 60, min = 50 , max = 100
UCrange = |(60-75)| / (0.5 * |max-min|) = 15 / 25 = 0.6
UCmax = 60/100 = 0.6

## Example

```python
s = Scene()

# TODO

```