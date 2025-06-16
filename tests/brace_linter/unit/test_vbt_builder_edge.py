from pycleancode.brace_linter.vbtree.vbt_model import VBTNode


def test_vbt_leave_default_behavior():
    root = VBTNode(node_type="ROOT", start_line=0, end_line=0)
    child = VBTNode(node_type="If", start_line=1, end_line=2)
    root.add_child(child)

    assert child.parent == root
    assert child in root.children
