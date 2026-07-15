import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
VISUAL = ROOT / "gui" / "visual.mjs"
REGISTRY = ROOT / "gui" / "visual-catalog.json"
HTML = ROOT / "gui" / "index.html"
README = ROOT / "gui" / "README.md"
DOC = ROOT / "docs" / "visual-audio-phase12-visual-identity-v0.12.28.md"


class GuiVisualIdentityTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.app = APP.read_text(encoding="utf-8")
    cls.visual = VISUAL.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    cls.html = HTML.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8")

  def test_registry_covers_first_slice_visual_vocabulary(self):
    self.assertEqual(self.registry["schema_version"], "visual-catalog-v1")
    self.assertEqual(self.registry["third_party_assets"], [])
    self.assertEqual(
      {entry["id"] for entry in self.registry["identities"]},
      {"riverside", "northlake", "summit", "generic-institution"},
    )
    self.assertTrue(
      {
        "facility",
        "demand",
        "capacity",
        "project",
        "staffing",
        "payer-policy",
        "timeline",
        "generic",
      }.issubset({entry["id"] for entry in self.registry["markers"]})
    )
    self.assertTrue(
      {
        "stable",
        "watch",
        "constrained",
        "critical",
        "improving",
        "uncertain",
        "delayed",
        "revised",
        "reported",
      }.issubset({entry["id"] for entry in self.registry["statuses"]})
    )
    for entry in self.registry["identities"] + self.registry["markers"] + self.registry["statuses"]:
      self.assertEqual(entry["license"], "project-generated")
      self.assertEqual(entry["approval_status"], "approved")
      self.assertIn("source", entry)
      self.assertIn("equivalent", entry)

  def test_rendering_uses_semantic_tokens_at_existing_surfaces(self):
    for marker in (
      'from "./visual.mjs"',
      "createVisualToken",
      "visualIdentityFor(entity)",
      "visualMarkerFor(facility.kind)",
      "visualMarkerFor(overlay.marker ?? overlay.kind ?? overlay.label)",
      "visualMarkerFor(process.marker ?? process.label)",
      "visual-catalog-v1",
    ):
      self.assertIn(marker, self.app + self.visual)
    for marker in (
      "visual-token",
      "visual-token-label",
      "visual-token-symbol",
      "Identity and marker vocabulary",
    ):
      self.assertIn(marker, self.html + self.readme)

  def test_lookup_is_deterministic_and_has_explicit_unknown_fallback(self):
    script = r'''
      import { visualIdentityFor, visualMarkerFor } from "./gui/visual.mjs";
      const known = visualIdentityFor({ id: "riverside" });
      const alias = visualIdentityFor({ id: "unknown", name: "Summit Care" });
      const unknown = visualIdentityFor({ id: "future-system" });
      const misleading = visualIdentityFor({ id: "future-summit-network", name: "Future System" });
      const marker = visualMarkerFor("nursing staffing pressure");
      const empty = visualMarkerFor("");
      if (known.id !== "riverside" || known.label !== "Riverside") process.exit(1);
      if (alias.id !== "summit") process.exit(2);
      if (unknown.id !== "generic-institution" || misleading.id !== "generic-institution") process.exit(3);
      if (marker.id !== "staffing" || empty.id !== "generic") process.exit(4);
      if (JSON.stringify({ known, alias, unknown, marker, empty }).includes("private")) process.exit(5);
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_visual_boundary_has_no_host_or_external_asset_expansion(self):
    combined = self.app + self.visual + self.readme + self.doc
    for forbidden in (
      "CompetitiveWorldState",
      "resolved_inputs",
      "effect_queue",
      "transition_competitive",
      "fetch(",
      "WebSocket",
      "http://",
      "https://",
    ):
      self.assertNotIn(forbidden, combined)

  def test_javascript_parses(self):
    for path in (APP, VISUAL):
      result = subprocess.run(
        ["node", "--check", str(path)],
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
