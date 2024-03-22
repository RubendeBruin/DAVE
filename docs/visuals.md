3D visuals are included using VTK

Creating vtk actors:

visual_helpers/vtkActorMakers.py

All actors are PolyData based.
Not all of them have texture coordinates.



AbstractSceneRenderer

visual visualizes a scene using vtk and vedo helpers

Basic data structure:

Viewport
 - node_visuals (VisualActors)
    - [node] -> reference to corresponding node 
    - actors [dict]
        - [ActorType]
        
        <the appearance of these visuals is determined by painters which are activated by update_visibility>
        
 - temporary_visuals (VisualActors)
    These are visuals that are temporary added to the viewport. For example a moment-line or boundary edges of a mesh
    these are automatically deleted when the viewport is updated (position_visuals) 
        
 - private visuals (wave-plane, etc)
 
       <the appearance of these visuals is determined by Viewport>
       <set by update_global_visibility which is called bt update_visibility>




Viewport
============

Viewport is the main class which handles the viewport (ie: Plotter).
It supports embedded plotting (in a qt application) as well as stand-alone or via Jupyter or Renders (offscreen renderer)

A viewport contains VisualActors.


Visual-Actors
------------------

this class contains a reference to a Node (optional) and a dict of actors

Dict of actors: On of them is always called "main". This is used, among others, to determine the position of the label (if any) 
    

a visual actor can be hidden by setting visible to False

each of the individual vtk-plotter actors has a "actor_type" property which is a enum ActorType.

ActorType is used for general control of these actors. At the moment this is only Scaling which is implemented in "position visuals"


VISUALS FOR NODES
==================



     each actor:
       - may have an ActorType property. This is yet another way to tell what kind of feature the visual represents
    - has a property "node"
   


- A visual representing a Node has its node property set to a node (not None).
  appearance of these nodes is controlled by Painters.
- The visibility of these nodes may be overridden by the .visible setting of the node.
  
  
   
    Updates the visibility settings for all of the actors
    A visual can be hidden completely by setting visible to false
    An actor can be hidden depending on the actor-type using ????  <-- obsolete
        
        


Creating and updating actors
-----------------------------

Creating and updating of actors is done by Viewport:

When a new viewport has been created:
- create_world_actors : Creates the global scenery

When new nodes are added to the screen:
- create_visuals      : Creates actors for nodes in the scene that do not yet have one

When the nodes in the scene have moved:
- position_visuals    : Updates the positions of existing visuals
                        Removes visuals for which the node is no longer present in the scene
                        Applies scaling for non-physical actors
                        Updates the geometry for visuals where needed (meshes)
                        Updates the "paint_state" property for tanks and contact nodes (see paint)
                        
When the nodes in the screen have changed:                    
- add_new_actors_to_screen:
                        Checks all visuals for actors that are not yet added to the screen. Adds them
                        Checks for Visual and Mesh nodes that need to be reloaded by checking _new_mesh
                            if so then only reloads the main component; the other components are handled by (position_visuals)                                                    
  
Painting

-  update_painting : paints all actors of a visual according to the node-type
                     and paint-definition in VieportSettings (called internally when needed)
-  update_visibility : updates the paint for all non-selected nodes
                       updates the outlines
-  update_outlines : Updates the outlines of all actors
                     Hides outlines for invisible actors, except if they are xray

Painting definition

Paint is stored in a nested dictionary.

painters['node-class']['actor_key']

- Some actors may change paint based on their state. This state gets post-fixed to the node-class
    - Tanks will change color based on their fill
        empty
        partial
        full
        freeflooding
    - Contact-balls will change color based on contact or not 
        free
        contact
  
  for these nodes the entry becomes:
    painters['node-class:paint_state']['actor_key']
  
Temporary actors
-----------------
Actors (anything derived from vtkActor) can be added to the viewport by calling
add_temporary_actor. Temporary actors are automatically removed when the viewport
is updated or can be removed manually be calling remove_temporary_actors


Outlines
=========
Outlines are individual actors. They attach to an actor and do not have a reference to the node or the other actors
of the node.
They copy the data of the actor that they outline when they are created. They update based on the global-transform of
the referenced actor.

If the geometry of the referenced actor (ie the vertices) have changed then the outline needs to be re-created.
In that case the ._vertices_changed = True flag of the outlined actor should be set. 

