# py-path-to-tree-printer

Turn a flat list of path strings into an indented ASCII tree.

```python
from py_path_to_tree_printer import render_tree

print(render_tree(["src/app.py", "src/util.py", "tests/test_app.py"]))
```

That prints:

```
/
├── src
│   ├── app.py
│   └── util.py
└── tests
    └── test_app.py
```

## Why this exists

Logs, manifests, and archive listings often give you paths as a flat list.
Reconstructing the directory shape by hand is tedious and error-prone. This
library builds the tree in one pass and renders it with stable, sorted
output, so the same input always produces the same text.

The trade-off is deliberate: paths are split on `/` only, and empty or `.`
segments are dropped. Backslashes are treated as ordinary characters rather
than separators, because guessing a separator from the input would silently
change the meaning of filenames that legitimately contain a backslash.

## API

`render_tree(paths, *, root_label="/")` returns a string ending in a newline.
`paths` is any iterable of strings. `root_label` is printed on the first line;
pass `""` to omit it. `PathTreeError` is raised if a path or the root label
is not a string.

## The awkward edge

`..` is preserved as a literal segment. Resolving it would require knowing
the current working directory, which the caller has not provided, so the tree
shows what was actually in the input rather than guessing.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

