"""Regression tests for excerpt drift and generated-link failures."""
import importlib.util
import tempfile
import unittest
from pathlib import Path


def load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


excerpts = load('check-excerpts')
links = load('check-output-links')


class ExcerptChecks(unittest.TestCase):
    def test_nested_fence_and_indent(self):
        text = '   ````md title="README.md"\n   ```bash\n   echo ok\n   ```\n   ````\n'
        self.assertEqual(list(excerpts.blocks(text))[0][3], ['```bash', 'echo ok', '```'])

    def test_hunk_checks_both_versions(self):
        hunk = ['--- a/x', '+++ b/x', '@@ -1,2 +1,2 @@', ' same', '-old', '+new']
        excerpts.check_diff(hunk, 'same\nold\n', 'same\nnew\n')
        with self.assertRaisesRegex(ValueError, 'new hunk'):
            excerpts.check_diff(hunk, 'same\nold\n', 'same\ndrift\n')
        with self.assertRaisesRegex(ValueError, 'old hunk'):
            excerpts.check_diff(hunk, 'same\ndrift\n', 'same\nnew\n')

    def test_truncated_hunk_fails(self):
        with self.assertRaisesRegex(ValueError, 'counts'):
            excerpts.check_diff(['@@ -1,2 +1,2 @@', ' one'], 'one\ntwo', 'one\ntwo')


class LinkChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def page(self, name, content):
        file = self.root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content)

    def test_relative_cross_deliverable_and_encoded_fragment(self):
        self.page('full/index.html', '<a href="../beginner/page.html?x=1#two%20words">Go</a><a href="https://example.com/missing">External</a>')
        self.page('beginner/page.html', '<h1 id="two words">Title</h1>')
        self.assertEqual(links.check(self.root), ([], 2))

    def test_missing_page_fragment_and_asset(self):
        self.page('index.html', '<a href="missing.html">X</a><a href="#missing">Y</a><img src="missing.png">')
        errors, _ = links.check(self.root)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any('missing fragment' in e for e in errors))

    def test_directory_links_and_named_anchors(self):
        self.page('index.html', '<a href="nested/#old">X</a>')
        self.page('nested/index.html', '<a name="old"></a>')
        self.assertEqual(links.check(self.root), ([], 2))

    def test_empty_base_duplicate_and_escape(self):
        self.assertEqual(len(links.check(self.root)[0]), 1)
        self.page('index.html', '<p id="x"></p><p id="x"></p><a href="../outside">X</a>')
        self.assertEqual(len(links.check(self.root)[0]), 2)
        self.page('index.html', '<base href="/prefix/">')
        self.assertIn('unsupported', links.check(self.root)[0][0])


if __name__ == '__main__':
    unittest.main()
