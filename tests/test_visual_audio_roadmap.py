import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"


class VisualAudioRoadmapTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    roadmap = ROADMAP.read_text(encoding="utf-8")
    cls.roadmap = roadmap
    cls.phase9 = roadmap.split("# Phase 9:", 1)[1].split("# Phase 10:", 1)[0]

  def test_phase9_technical_checklists_have_no_unrecorded_gates(self):
    self.assertNotIn("- [ ]", self.phase9)
    for version in ("0.12.78", "0.12.79", "0.12.80", "0.12.81", "0.12.82", "0.12.83", "0.12.84"):
      self.assertRegex(self.roadmap, rf"Status: Complete in v{re.escape(version)}\b")
    for label in (
      "License allowlist encoded in validation.",
      "License denylist encoded in validation.",
      "Attribution text generated.",
      "Source URLs archived where practical.",
      "Retrieval dates present.",
      "Original licenses saved or referenced.",
      "Modification descriptions present.",
      "Approval status required.",
      "Third-party notices generated.",
      "Release package includes credits.",
      "In-game credits accessible.",
      "Automated license policy audit completed before release;",
      "SVG scripts and external references rejected.",
      "Embedded raster images reviewed.",
      "External fonts rejected.",
      "Unexpected metadata stripped.",
      "Audio codec validation implemented.",
      "File-size limits enforced.",
      "Dimension limits enforced.",
      "Hashes verified in CI.",
      "Release build reproducibility checked.",
      "Asset loading failures degrade gracefully.",
    ):
      self.assertRegex(self.phase9, rf"- \[x\] {re.escape(label)}")
    for marker in (
      "scripts/validate_assets.py",
      "scripts/validate_asset_security.py",
      "scripts/verify_asset_release.py",
      "scripts/sanitize_svg_metadata.py",
      "assets/ASSET_RELEASE_MANIFEST.json",
      "assets/THIRD_PARTY_NOTICES.md",
    ):
      self.assertIn(marker, self.roadmap)

  def test_phase9_technical_closure_preserves_external_review_boundaries(self):
    lowered = self.phase9.lower()
    self.assertIn("human legal", lowered)
    self.assertIn("human review", lowered)
    self.assertIn("technical policy conformance only", lowered)
    self.assertIn("legal clearance", lowered)
    for forbidden in ("automatically approved", "legal clearance established", "human review complete"):
      self.assertNotIn(forbidden, lowered)

  def test_phase9_evidence_files_are_present(self):
    for relative_path in (
      "scripts/validate_assets.py",
      "scripts/validate_asset_security.py",
      "scripts/verify_asset_release.py",
      "scripts/sanitize_svg_metadata.py",
      "assets/ASSET_RELEASE_MANIFEST.json",
      "assets/ASSET_CREDITS.md",
      "assets/THIRD_PARTY_NOTICES.md",
      "gui/asset-credits.mjs",
    ):
      self.assertTrue((ROOT / relative_path).is_file(), relative_path)


if __name__ == "__main__":
  unittest.main()
