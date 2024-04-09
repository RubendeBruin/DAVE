from DAVE.annotations.layer import NodeLabelLayer


def test_labels(model):
    s= model
    a = NodeLabelLayer(s)
    assert len(a.annotations) == len(s._nodes)


def test_labels_positions_and_labels(model):
    s= model
    L = NodeLabelLayer(s)

    node_labels = [node.label for node in s.nodes()]

    for a in L.annotations:
        # get the node from the annotation
        text = a.get_text()
        assert text in node_labels


def test_labels_remove(model):
    s = model
    L = NodeLabelLayer(s)

    s.clear()
    L.update()

    assert len(L.annotations) == 0


def test_labels_add(model):
    s = model
    L = NodeLabelLayer(s)

    s.new_point("new_point", position=(0, 0, 0))

    L.update()

    assert len(L.annotations) == len(s._nodes)

    s.clear()
    L.update()

    assert len(L.annotations) == 0

