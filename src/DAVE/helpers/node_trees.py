

def give_parent_item(node, items):
    """Determines where to place the given node in the tree.

    Returns the item under which the node should be placed.
    If the item is to be placed as the root, then None is returned

    The possible parents are given in the items dictionary, which maps the name of the node to the
    node
    """
    parent = getattr(node, "parent", None)

    # if node does not have a parent, then use the manager (if any)
    if parent is None:
        parent = node.manager

    # no manager and no parent --> in root
    if parent is None:
        return None

    # there is a parent or manager to add to,
    # but the parent may not be in the tree.

    hidden_nodes_between = False

    while True:
        if parent.name in items:
            return items[parent.name]

        hidden_nodes_between = True

        parents_parent = getattr(parent, "parent", None)
        if parents_parent is None:
            parents_parent = parent.manager

        # no parent and no manager:
        if parents_parent is None:
            return None

        parent = parents_parent  # next iteration with parent
