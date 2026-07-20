import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "check_documentation_links.py"
SPEC = importlib.util.spec_from_file_location("check_documentation_links", MODULE_PATH)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class DocumentationLinkTests(unittest.TestCase):
  def test_repository_documentation_links_resolve(self):
    self.assertEqual([], CHECKER.check_repository(ROOT))

  def test_checker_reports_broken_and_machine_local_links(self):
    with tempfile.TemporaryDirectory() as temporary_directory:
      root = Path(temporary_directory)
      document = root / "document.md"
      document.write_text(
        "[missing](missing.md)\n[local](file:///home/example/private.md)\n",
        encoding="utf-8",
      )

      issues = CHECKER.check_markdown_file(document, root)

    self.assertTrue(any("missing local link missing.md" in issue for issue in issues))
    self.assertTrue(any("machine-local path" in issue for issue in issues))


if __name__ == "__main__":
  unittest.main()
