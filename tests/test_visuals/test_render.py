from DAVE import DG, Visual


def test_render_basic_nodes(model_basic_nodes):

    s = model_basic_nodes
    s['Visual'].parent = None

    for node in s._nodes:
        if not isinstance(node, Visual):
            s.delete(node)

    DG(model_basic_nodes)