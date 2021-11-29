## Tags

Reporting

DAVE nodes are generic building block. This is nice because it allows you to build anything you want.

But then you need a report, or an analysis.

Reports are intended to be read by humans. So it makes sense to view the model from a certain perspective, for example a mooring analysis perspective or a lift-analysis perspective.
The perspective from which you look at the model determines what is important and what is not.

Problem is: DAVE has no idea what kind of thing you modelled. And it may even be a mix of things. Maybe you
have modelled a vessel that is performing a lift while moored. The cable nodes that are used for mooring lines should be reported in the "mooring" sections of the report while the cable nodes
that are used to model slings should instead be reported in the "rigging section". And when doing a mooring analysis you do not 
want to optimize the lengths of the rigging.

The reporting section of DAVE needs to know what is what, and the only way for DAVE to know it is if we tell it. So we need to
tell the reporing section which nodes should be included in the mooring report and which nodes should be included in the
rigging section.

Enter **TAGS**

Tags offer a way to "tag" nodes. 

Tags are `labels` that can be assigned to nodes. Every node can have an unlimited number of tags.
Tag can be used to define groups of nodes with a similar purpose.

In the example of a moored crane vessel the mooring lines (cables) would be given the tag `mooring` while the
cables used for rigging would be tagged `rigging`.

**TAG are not managed**, they are fully controlled by the Scene.

Each node can have tags. These are controlled by:

- `add_tag`
- `add_tags`
- `delete_tag`
- `has_tag` (accepts expressions)
- `tags` (read only property)

On scene level there are:

- `tags` (read only property) : all exiting tags
- `nodes_tagged` : returns all nodes that have some tag. Accepts expressions.
- `delete_tag` : removes given tag from all nodes

## Tags and tag-expressions

A tag is a string (text). For example "mooring".

When selecting nodes based on their tag a more flexible syntax is allowed to enable selection based on multiple tags or partial tags.

The syntax is similar to filename matching patterns: `?` replaces any character, `*` replaces any number of characters including none.

This means that
- `mo*` will match `mooring` are well as `more cargo`
- `tag?` will match `tag1` and `tag2` but not `tag10` 
- `*p*` match any tag containing a `p`, including `p` itself


Furthermore multiple matching patterns may be defined by separating them by a `,`

Examples:
- `tag2, tag1` will match both `tag1` and `tag2`
- `t*, mooring` will match any tag that starts with a `t` as well as any tag that equals `mooring`



### NOT IMPLEMENTED: Automatic tags

Some tags are added automatically. These start with `@`. For example `@Cable`. These can not be modified or deleted. 