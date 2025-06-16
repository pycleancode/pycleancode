import libcst as cst
from libcst.metadata import MetadataWrapper

from pycleancode.brace_linter.vbtree.vbt_builder import VBTBuilder
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode


def test_vbt_builder_simple_function() -> None:
    source_code = """
def my_function():
    if True:
        for i in range(5):
            while i < 5:
                pass
"""
    # Parse CST
    tree = cst.parse_module(source_code)
    wrapper = MetadataWrapper(tree)

    # Build VBT
    builder = VBTBuilder(wrapper)
    vbt_root: VBTNode = builder.build()

    # Assert root exists
    assert vbt_root.node_type == "ROOT"
    assert len(vbt_root.children) == 1

    # First level: FunctionDef
    func_node = vbt_root.children[0]
    assert func_node.node_type == "FunctionDef"

    # Second level: If inside function
    if_node = func_node.children[0]
    assert if_node.node_type == "If"

    # Third level: For inside If
    for_node = if_node.children[0]
    assert for_node.node_type == "For"

    # Fourth level: While inside For
    while_node = for_node.children[0]
    assert while_node.node_type == "While"

    # Leaf node (pass statement does not generate node)
    assert len(while_node.children) == 0


def test_vbt_builder_multiple_toplevel_blocks() -> None:
    source_code = """
class MyClass:
    def method(self):
        if True:
            pass
"""
    tree = cst.parse_module(source_code)
    wrapper = MetadataWrapper(tree)

    builder = VBTBuilder(wrapper)
    vbt_root: VBTNode = builder.build()

    assert vbt_root.node_type == "ROOT"
    assert len(vbt_root.children) == 1

    class_node = vbt_root.children[0]
    assert class_node.node_type == "ClassDef"

    method_node = class_node.children[0]
    assert method_node.node_type == "FunctionDef"

    if_node = method_node.children[0]
    assert if_node.node_type == "If"
