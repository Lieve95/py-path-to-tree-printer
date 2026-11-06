"""Public API for py-path-to-tree-printer.

Exports:
    render_tree(paths, *, root_label="/") -> str
    PathTreeError
"""

from .core import PathTreeError, render_tree

__all__ = ["render_tree", "PathTreeError"]
