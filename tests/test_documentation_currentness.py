import unittest
from pathlib import Path

from scripts.check_documentation_currentness import (
  ROOT,
  check_repository,
  classify_markdown,
)


class DocumentationCurrentnessTests(unittest.TestCase):
  def test_roles_cover_representative_document_classes(self):
    self.assertEqual(classify_markdown(ROOT / "README.md"), "maintained")
    self.assertEqual(classify_markdown(ROOT / "docs/history/playtests/v0.10/playtest-findings-v0.10.14.md"), "historical")
    self.assertEqual(classify_markdown(ROOT / "docs/decision-records/0012-loopback-gui-host.md"), "ADR")
    self.assertEqual(classify_markdown(ROOT / "_workspace/00_input/request-summary.md"), "workspace")
    self.assertEqual(classify_markdown(ROOT / "assets/ASSET_CREDITS.md"), "generated")

  def test_current_repository_contract_passes(self):
    issues, counts = check_repository()
    self.assertEqual(issues, [])
    for role in ("maintained", "generated", "historical", "ADR", "workspace"):
      self.assertGreater(counts[role], 0, role)


if __name__ == "__main__":
  unittest.main()
