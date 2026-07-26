import unittest

from scripts.lib.frontmatter import FrontmatterError, parse_frontmatter


class FrontmatterTests(unittest.TestCase):
    def test_parse_simple(self):
        meta, body = parse_frontmatter(
            "---\nname: demo\ndescription: Use when testing.\n---\n\n# demo\n"
        )
        self.assertEqual(meta["name"], "demo")
        self.assertEqual(meta["description"], "Use when testing.")
        self.assertIn("# demo", body)

    def test_requires_fence(self):
        with self.assertRaises(FrontmatterError):
            parse_frontmatter("# no frontmatter\n")


if __name__ == "__main__":
    unittest.main()
