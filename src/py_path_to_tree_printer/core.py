"""Render a list of path strings as an indented ASCII tree.

Design decisions:

* Paths are split on ``/`` only. Backslashes are treated as ordinary
  characters, because mixing Windows and POSIX separators in one input list
  produces ambiguous trees and there is no portable way to guess which one
  the caller meant. Callers on Windows can normalise first.
* Empty segments are ignored. ``"a//b"`` is treated the same as ``"a/b"``,
  and a leading ``/`` does not create an extra empty root child.
* ``.`` segments are ignored; ``..`` segments are kept verbatim. Resolving
  ``..`` would require filesystem context the caller has not supplied.
* The output is deterministic: children are sorted lexicographically by
  segment. That makes the rendering stable across runs and platforms.
* A trailing newline is always included, so the result can be printed or
  written to a file without an extra concatenation step.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple


class PathTreeError(ValueError):
    """Raised when an input path cannot be represented in the tree."""


class _Node:
    """A single directory or file node in the tree.

    ``children`` is a plain dict keyed by segment. We deliberately do not
    use an ordered dict: ordering is applied at render time by sorting the
    keys, which keeps insertion order from leaking into the output.
    """

    __slots__ = ("children",)

    def __init__(self) -> None:
        self.children: Dict[str, "_Node"] = {}

    def insert(self, segments: Iterable[str]) -> None:
        node = self
        for segment in segments:
            node = node.children.setdefault(segment, _Node())


def _split(path: str) -> List[str]:
    """Split a path into meaningful segments.

    Empty segments and ``.`` are dropped. The function never returns an
    empty list for a non-empty input string, because a path that survives
    the filters is by definition at least one segment long.
    """
    if not isinstance(path, str):
        raise PathTreeError("paths must be strings, got {!r}".format(type(path).__name__))
    parts = path.split("/")
    return [part for part in parts if part not in ("", ".")]


def _render(node: _Node, prefix: str, lines: List[str]) -> None:
    """Depth-first render with box-drawing connectors.

    ``prefix`` carries the indentation for the current level. Children are
    sorted so the output is stable regardless of input order.
    """
    children = sorted(node.children.items())
    for index, (name, child) in enumerate(children):
        is_last = index == len(children) - 1
        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + name)
        extension = "    " if is_last else "│   "
        _render(child, prefix + extension, lines)


def render_tree(paths: Iterable[str], *, root_label: str = "/") -> str:
    """Render ``paths`` as an ASCII tree and return it as a string.

    Args:
        paths: An iterable of path strings. Each path is split on ``/``.
        root_label: The label printed for the synthetic root. Defaults to
            ``"/"``. Pass ``""`` to omit the root line entirely.

    Returns:
        A string ending in a newline. If ``paths`` is empty the result is
        just the root line (or an empty string when ``root_label`` is
        empty).

    Raises:
        PathTreeError: If any element of ``paths`` is not a string, or if
            ``root_label`` is not a string.
    """
    if not isinstance(root_label, str):
        raise PathTreeError(
            "root_label must be a string, got {!r}".format(type(root_label).__name__)
        )

    root = _Node()
    for path in paths:
        segments = _split(path)
        if segments:
            root.insert(segments)

    lines: List[str] = []
    if root_label:
        lines.append(root_label)
        _render(root, "", lines)
    else:
        _render(root, "", lines)

    if not lines:
        return ""
    return "\n".join(lines) + "\n"
