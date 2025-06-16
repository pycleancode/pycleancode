"""
Module: vbt_model

Defines the Virtual Brace Tree (VBT) node data structure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class VBTNode:
    """
    Represents a node in the Virtual Brace Tree structure.

    Attributes:
        node_type (str): Type of the AST block (e.g. FunctionDef, If, For).
        start_line (int): Starting line number of the node.
        end_line (int): Ending line number of the node.
        children (List[VBTNode]): List of child nodes.
        parent (Optional[VBTNode]): Parent node reference.
    """

    node_type: str
    start_line: int
    end_line: int
    children: List[VBTNode] = field(default_factory=list)
    parent: Optional[VBTNode] = None

    def add_child(self, child: VBTNode) -> None:
        """
        Add a child node and automatically set parent reference.

        Args:
            child (VBTNode): The child node to add.
        """
        self.children.append(child)
        child.parent = self
