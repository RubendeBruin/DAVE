from DAVE import *

def test_give_node_properties():
    s = Scene()
    p = s.new_point('point')

    for prop in s.give_properties_for_node(p):
        print('----')
        print(prop)
        docs = s.give_documentation (p, prop)
        print(docs.doc_long)

