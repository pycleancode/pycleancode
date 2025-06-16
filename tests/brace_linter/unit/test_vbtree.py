from pycleancode.brace_linter.vbtree.vbt_model import VBTNode


def test_vbt_node_initialization() -> None:
    node = VBTNode(node_type="FunctionDef", start_line=1, end_line=10)

    assert node.node_type == "FunctionDef"
    assert node.start_line == 1
    assert node.end_line == 10
    assert node.children == []
    assert node.parent is None


def test_add_child_sets_relationship() -> None:
    parent_node = VBTNode(node_type="FunctionDef", start_line=1, end_line=10)
    child_node = VBTNode(node_type="If", start_line=2, end_line=5)

    parent_node.add_child(child_node)

    # Parent should contain child
    assert child_node in parent_node.children
    # Child should reference parent
    assert child_node.parent is parent_node


def test_multiple_children_relationships() -> None:
    root = VBTNode(node_type="ROOT", start_line=0, end_line=0)
    func_node = VBTNode(node_type="FunctionDef", start_line=1, end_line=10)
    if_node = VBTNode(node_type="If", start_line=2, end_line=5)
    for_node = VBTNode(node_type="For", start_line=3, end_line=4)

    root.add_child(func_node)
    func_node.add_child(if_node)
    if_node.add_child(for_node)

    assert root.children == [func_node]
    assert func_node.parent == root
    assert if_node.parent == func_node
    assert for_node.parent == if_node
    assert for_node in if_node.children
