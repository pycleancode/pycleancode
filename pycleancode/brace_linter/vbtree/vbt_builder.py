"""
Module: vbt_builder

Builds a Virtual Brace Tree (VBT) from libcst CST nodes.
"""

import libcst as cst
from libcst.metadata import PositionProvider, MetadataWrapper, CodeRange
from pycleancode.brace_linter.vbtree.vbt_model import VBTNode
from typing import cast


class VBTBuilder(cst.CSTVisitor):
    """
    Converts libcst CST into Virtual Brace Tree structure.
    """

    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, wrapper: MetadataWrapper) -> None:
        """
        Initialize VBTBuilder.

        Args:
            wrapper (MetadataWrapper): LibCST MetadataWrapper instance.
        """
        self.root = VBTNode(node_type="ROOT", start_line=0, end_line=0)
        self.stack = [self.root]
        self.wrapper = wrapper
        self.wrapper.visit(self)

    def build(self) -> VBTNode:
        """
        Return the fully constructed Virtual Brace Tree.

        Returns:
            VBTNode: Root node of the tree.
        """
        return self.root

    # === Visitor Methods for all block-level nodes ===

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        self._enter_block("FunctionDef", node)

    def visit_If(self, node: cst.If) -> None:
        self._enter_block("If", node)

    def visit_For(self, node: cst.For) -> None:
        self._enter_block("For", node)

    def visit_While(self, node: cst.While) -> None:
        self._enter_block("While", node)

    def visit_With(self, node: cst.With) -> None:
        self._enter_block("With", node)

    def visit_Try(self, node: cst.Try) -> None:
        self._enter_block("Try", node)

    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        self._enter_block("ClassDef", node)

    # === Private helper ===

    def _enter_block(self, node_type: str, node: cst.CSTNode) -> None:
        position = cast(CodeRange, self.get_metadata(PositionProvider, node))
        current = VBTNode(
            node_type=node_type,
            start_line=position.start.line,
            end_line=position.end.line,
        )
        self.stack[-1].add_child(current)
        self.stack.append(current)

    def leave_default(self, node: cst.CSTNode) -> None:
        """
        Called after visiting any CST node.
        """
        if len(self.stack) > 1:
            self.stack.pop()
