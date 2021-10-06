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
from DAVE import *

s = Scene()


# code for LiftPoint
s.new_point(name='LiftPoint',
          position=(0.0,
                    0.0,
                    0.0))
# code for Piano
s.new_rigidbody(name='Piano',
                mass=100.0,
                cog=(0.0,
                     0.0,
                     -8.0),
                fixed =False )
# code for LP1
s.new_point(name='LP1',
          parent='Piano',
          position=(-10.0,
                    10.0,
                    0.0))
# code for LP2
s.new_point(name='LP2',
          parent='Piano',
          position=(10.0,
                    10.0,
                    0.0))
# code for LP3
s.new_point(name='LP3',
          parent='Piano',
          position=(-10.0,
                    -10.0,
                    0.0))
# code for LP4
s.new_point(name='LP4',
          parent='Piano',
          position=(10.0,
                    -10.0,
                    0.0))
# code for Visual
s.new_visual(name='Visual',
            parent='Piano',
            path=r'wirecube.obj',
            offset=(0.0, 0.0, -8.0),
            rotation=(0, 0, 0),
            scale=(10.0, 10.0, 8.0) )
# code for cable1
s.new_cable(name='cable1',
            endA='LiftPoint',
            endB='LP2',
            length=20.616,
            EA=1000.0)
# code for cable2
s.new_cable(name='cable2',
            endA='LP1',
            endB='LiftPoint',
            length=20.616,
            EA=1000.0)
# code for sheaved_cable
s.new_cable(name='sheaved_cable',
            endA='LP3',
            endB='LP4',
            length=41.231,
            EA=1000.0,
            sheaves = ['LiftPoint'])

# Limits 
s['Piano'].limits['x'] = (-2, 1.0)       # define a range
s['cable1'].limits['tension'] = 100      # define a maximum-absolute tension
s['sheaved_cable'].limits['tension'] = 500
s['LP4'].limits['fz'] = 300  # limit the vertical tension at this liftpoint
s['LP4'].limits['fx'] = -1   # counts as no limit 

```