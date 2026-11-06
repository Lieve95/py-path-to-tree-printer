import unittest

from py_path_to_tree_printer import PathTreeError, render_tree


class RenderTreeTests(unittest.TestCase):
    def test_single_file(self):
        self.assertEqual(render_tree(["a.txt"]), "/\n└── a.txt\n")

    def test_nested_directories(self):
        result = render_tree(["a/b/c.txt"])
        self.assertEqual(
            result,
            "/\n"
            "└── a\n"
            "    └── b\n"
            "        └── c.txt\n",
        )

    def test_siblings_are_sorted(self):
        result = render_tree(["b.txt", "a.txt", "c.txt"])
        self.assertEqual(
            result,
            "/\n"
            "├── a.txt\n"
            "├── b.txt\n"
            "└── c.txt\n",
        )

    def test_shared_prefix_merged(self):
        result = render_tree(["src/a.py", "src/b.py"])
        self.assertEqual(
            result,
            "/\n"
            "└── src\n"
            "    ├── a.py\n"
            "    └── b.py\n",
        )

    def test_empty_segments_ignored(self):
        result = render_tree(["a//b", "/a/b", "a/b/"])
        self.assertEqual(
            result,
            "/\n"
            "└── a\n"
            "    └── b\n",
        )

    def test_dot_segments_ignored(self):
        result = render_tree(["./a/./b"])
        self.assertEqual(
            result,
            "/\n"
            "└── a\n"
            "    └── b\n",
        )

    def test_dotdot_segments_preserved(self):
        result = render_tree(["a/../b"])
        self.assertEqual(
            result,
            "/\n"
            "└── a\n"
            "    └── ..\n"
            "        └── b\n",
        )

    def test_empty_input(self):
        self.assertEqual(render_tree([]), "/\n")

    def test_empty_string_input(self):
        self.assertEqual(render_tree([""]), "/\n")

    def test_custom_root_label(self):
        result = render_tree(["a"], root_label="root")
        self.assertEqual(result, "root\n└── a\n")

    def test_empty_root_label_omits_root_line(self):
        result = render_tree(["a", "b"], root_label="")
        self.assertEqual(
            result,
            "├── a\n"
            "└── b\n",
        )

    def test_non_string_path_raises(self):
        with self.assertRaises(PathTreeError):
            render_tree(["ok", 42])

    def test_non_string_root_label_raises(self):
        with self.assertRaises(PathTreeError):
            render_tree(["a"], root_label=None)

    def test_duplicate_paths_collapse(self):
        result = render_tree(["a/b", "a/b"])
        self.assertEqual(
            result,
            "/\n"
            "└── a\n"
            "    └── b\n",
        )

    def test_unicode_segments(self):
        result = render_tree(["café/naïve.txt"])
        self.assertEqual(
            result,
            "/\n"
            "└── café\n"
            "    └── naïve.txt\n",
        )


if __name__ == "__main__":
    unittest.main()
