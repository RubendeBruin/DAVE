from DAVE import *

def test_name_like():
    s = Scene()
    s.new_point('A')
    s.new_point('A1')
    s.new_point('A2')
    s.new_point('A3')

    name = s.available_name_like('A')
    assert s.name_available(name)

    assert name == 'A4'

def test_name_like2():
    s = Scene()
    s.new_point('B')

    name = s.available_name_like('B')
    assert s.name_available(name)

    assert name == 'B2'



def give_model():
    s = Scene()
    f1 = s.new_frame('f1')
    f3 = s.new_frame('f3')
    f2 = s.new_frame('f2', parent = f1)
    p1 = s.new_point('p1',parent=f1)
    p2 = s.new_point('p2',parent=f2, position=(1,2,3))
    c1= s.new_cable('c1',endA=p1, endB=p2, EA = 12345)

    s.new_visual(name="Visual", parent="f2", path="res: cube_with_bevel.obj")
    s.new_circle(name="Circle", parent="p1", axis=(0, 1, 0), radius=1)

    return s

def test_copy():

    s = give_model()

    nodes = s.nodes_with_parent(s['f1'], recursive=True)
    assert len(nodes) == 5

    nodes.append(s['f1'])

    more_nodes = s.nodes_with_dependancies_in_and_satifsfied_by(nodes)
    assert len(more_nodes) == 6

    # all nodes except f3
    branch = list(set([*nodes, *more_nodes]))

    assert len(branch) == len(s._nodes)-1  # check number of nodes

    cpy = s.copy(branch)

    cpy.print_node_tree()

def test_branch_of_f2():
    s = give_model()
    s.print_node_tree()

    nodes = s.nodes_with_parent(s['f2'], recursive=True)
    nodes.append(s['f2'])

    more_nodes = s.nodes_with_dependancies_in_and_satifsfied_by(nodes)

    assert s['p1'] not in more_nodes

    print(more_nodes)


def test_duplicate_node():
    s = give_model()
    f_new = s.duplicate_node('f1')

    assert f_new.name == 'f4'

def test_duplicate_branch():
    s = give_model()
    s.duplicate_branch(s['f1'])

    s.print_node_tree()
    """
   f1 [Frame]
     |-> f2 [Frame]
     |    |-> p2 [Point]
     |    |-> Visual [Visual]
     |-> p1 [Point]
     |    |-> Circle [Circle]
    f3 [Frame]
    c1 [Cable]
    f5 [Frame]
     |-> p3 [Point]
     |    |-> Circle2 [Circle]
     |-> f4 [Frame]
     |    |-> Visual2 [Visual]
     |    |-> p4 [Point]
    c2 [Cable]
    """

    def assert_parent(a,b):
        assert s[a].parent == s[b]

    assert_parent('f2','f1')
    assert_parent('p2','f2')
    assert_parent('Visual','f2')
    assert_parent('p1','f1')
    assert_parent('Circle','p1')

    assert_parent('f4','f5')
    assert_parent('p4','f5')
    assert_parent('Visual2','f4')
    assert_parent('p3','f4')
    assert_parent('Circle2','p4')

def test_duplicate_sub_branch_f2():
    s = give_model()
    assert s["f2"].parent == s["f1"]
    s.duplicate_branch(s['f2'])

    s.print_node_tree()

    assert s['f2'].parent == s['f1']
    assert s["f4"].parent == s["f1"]


def test_duplicate_branch_node_with_parent():
    s = give_model()
    s.duplicate_branch(s['f2'])

    s.print_node_tree()

def test_2():
    s = give_model()
    s.duplicate_node('f1')
    s.duplicate_branch('f1')

#
#
# def test_gui():
#     s = give_model()
#     from DAVE.gui import Gui
#     Gui(s)

