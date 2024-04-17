# Annotation layers

Annotation layers place text over the 3D rendered image.

Annotation layers contain one or more `Annotations`.

Annotations are bound to a Node. The node provides the 3D anchor location and its properties can be used to compose the
text.
Once the 3D locations and text are known, the 2D positions of the text can be calculated in the viewport can derived.

Manual adjustments can be made to the 2D positions and visibility of the annotations.

With the 2D positions and text size known, as additional pass can be performed to avoid overlap of the annotations.

## Annotation Layer

An annotation layer is a collection of annotations and is associated with a viewport (Scene Renderer).
It takes care of rendering the annotations in the viewport.

It also supplies the formatting options for rendering the annotations.

- font : The font to use (PIL.ImageFont)
- background_rgba : The background color of the annotation, use None for transparent
- padding : The padding around the text (in pixels: top, right, bottom, left)
- border_width: The width of the border around the annotation
- border_rgba: The color of the border

Multi-line text is supported by using the newline character '\n' or `<br>` in the text.

Call:

- `render()` to render the annotations in the viewport.
- `update()` if the annotations have changed.

`Annotation` extends `HasNodeReference` and supports serialization to dict.

## Annotation

An annotation has a `text_producer` and an `anchor`.

The text producer takes care of the text while the anchor takes care of the position.

`Annotation` extends `HasNodeReference` and supports serialization to dict.

## Annotation Text

The text of an annotation is provided by an `TextProducer` object.
The TextProducer holds:

- a reference to a node
- a text
- a setting of how to handle the text
- optionally a format string

`TextProducer` extends `HasNodeReference` and supports serialization to dict.

Example:

```python
from DAVE import Scene
s = Scene()
p = s.new_point("p1", position = (0, 0, 1.23456))
t1 = TextProducer(p, "Just a text", how = ProduceTextAlgorithm.NOTHING)
print(t1.get_text())  # --> Just a text
```

| text                                                                    | how          | ff     | result                                       |                                                                                                       |
|-------------------------------------------------------------------------|--------------|--------|----------------------------------------------|-------------------------------------------------------------------------------------------------------|
| just a text                                                             | NOTHING      | n/a    | just a text                                  |                                                                                                       |
| name                                                                    | PROPERTY_RAW |        | p1                                           |                                                                                                       |
| name                                                                    | PROPERTY     |        | name = p1                                    |                                                                                                       |
| z                                                                       | PROPERTY_RAW |        | 1.235                                        | floats a by default rendered with 3 decimals                                                          |
| z                                                                       | PROPERTY     |        | z = 1.235 [m]                                |                                                                                                       |
| z                                                                       | PROPERTY     | {:.1f} | z = 1.2 [m]                                  | Formatting string used on property value                                                              |
| sdfsad                                                                  | PROPERTY_RAW |        |                                              | no error if property does not exist                                                                   |
| node.gz                                                                 | EVAL         | n/a    | 1.23456                                      | result of the evaluation where "node" can be used to refer to the node object                         |
| ```f'z = {node.z:.3f}m, fx = {node.fz / 9.81} tonnes'```                | EVAL         | n/a    | z = 1.235m, fx = 0.0 tonnes                  | text is evaluated using the eval function. In this case a f-string is used to get the desired result. |
| does not compute                                                        | EVAL         |        | ERROR:<br/>invalid syntax (<string>, line 1) | if the evaluation fails then the error is prepended with 'ERROR:'                                     |
| ```"f'{node.parent.force/9.81:.1f}t' if node.parent.force>0 else ''"``` | EVAL         | n/a    | xxx t or nothing                             | only produces a non-empty result if load>0                                                            | 

The properties of a `TextProducer` object can be altered after creation.

## Annotation Position

The position of an annotation is handled by it `Anchor`.

`Anchor` extends `HasNodeReference` and supports serialization to dict.

The `Anchor` object holds:

- position_1f, position_3d: These are user-supplied values that can be used to position the annotation in 3D
- screenspace_offset : This is a user-supplied value that can be used to offset the annotation in screen space
- node: The node to which the annotation is anchored

Anchor obtains the 3D position from a viewport (Scene Renderer) by invoking the `get_annotation_position` method of
the `visualActor` associated with the `node`. This method, in turn, calls the `get_annotation_position` method of the
node (if it exists). Otherwise, it used the logic implemented there.
The properties `position_1f` and `position_3d` are passed to that function and may have different meaning depending on
the type of node.
This logic is handled by the `get_annotation_position` method of the `visualActor`.

| Node type | position_1f                     | position_3d                      | 
|-----------|---------------------------------|----------------------------------|
| Cable     | Position along the cable [0..1] | not used                         |
| Beam      | Position along the beam [0..1]  | not used                         |
| Frame     | not used                        | 3D position in local axis system |

# Custom layers

Custom layers can be created by subclassing `CustomNodeLayer`.
The `CustomNodeLayer` class is a subclass of `AnnotationLayer` and provide annotations for nodes by implementing
the `provide_annotation_for_node` method.
It has a class-attribute `default_selector` that can be used to filter the nodes that the layer will provide annotations
for. A copy of this default selector
is used to filter the nodes that the layer will provide annotations for. This is stored in `.selector` and may be
modified after creation.

Example:

```python
from DAVE.annotations.layer import CustomNodeLayer, Annotation
from DAVE.settings import DAVE_ANNOTATION_LAYERS
from DAVE import NodeSelector, Cable

class CableTensionLayer(CustomNodeLayer):
    """Annotation layer that adds the tension in kN to all Cable nodes."""
    
    default_selector = NodeSelector(kind=(Cable,))

    def provide_annotation_for_node(self, node):
        return Annotation.create_node_property_annotation(node, 'tension')

DAVE_ANNOTATION_LAYERS["Cable tension"] = CableTensionLayer
```

A customNodeLayer

- Position
- Occlusion
- Formatting

