import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source" / "visual" / "identity" / "riverside-kit.svg"
RELEASE = ROOT / "assets" / "release" / "visual" / "svg" / "riverside.svg"
KIT = ROOT / "gui" / "identity-kits.mjs"
PROOF = ROOT / "gui" / "identity-proof.html"
README = ROOT / "gui" / "README.md"


def run_node(script):
  return subprocess.run(
    ["node", "--input-type=module", "-e", script],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
  )


class RiversideIdentityTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = SOURCE.read_text(encoding="utf-8")
    cls.release = RELEASE.read_text(encoding="utf-8")
    cls.kit = KIT.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")

  def test_source_and_release_variants_are_accessible_and_external_free(self):
    for document in (self.source, self.release):
      for marker in ("<title", "<desc", "system-ui", "Riverside"):
        self.assertIn(marker, document)
      self.assertNotIn('href="http://', document)
      self.assertNotIn('href="https://', document)
    for marker in ("logo-mark", "monochrome-mark", "compact-marker", "facility-sign", "report-header", "compact-badge", "RV"):
      self.assertIn(marker, self.source)

  def test_kit_surfaces_and_generic_fallback_are_deterministic(self):
    result = run_node(
      """
      import { identityKitFor, identitySurfaceSummary } from "./gui/identity-kits.mjs";
      const riverside = identityKitFor("riverside");
      const fallback = identityKitFor("future-system");
      const surfaces = identitySurfaceSummary("riverside");
      if (riverside.id !== "riverside" || riverside.monogram !== "RV" || surfaces.length !== 7) process.exit(1);
      if (fallback.id !== "generic-institution" || fallback.fallback?.label !== "Institution" || fallback.fallback?.equivalent !== "Institution identity unavailable") process.exit(2);
      if (JSON.stringify(riverside).includes("private") || JSON.stringify(fallback).includes("private")) process.exit(3);
      console.log(JSON.stringify({ riverside, fallback, surfaces }));
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    payload = json.loads(result.stdout)
    self.assertEqual(payload["riverside"]["monogram"], "RV")
    self.assertEqual(payload["fallback"]["id"], "generic-institution")

  def test_cross_screen_surface_and_audio_consistency_contract(self):
    for marker in ("logo_mark", "monochrome_mark", "compact_marker", "facility_signage", "report_header", "compact_badge", "audio_motif"):
      self.assertIn(marker, self.kit)
    for marker in ("Riverside identity kit", "Show generic fallback", "identitySurfaceSummary", "Visible equivalent", "identity-status"):
      self.assertIn(marker, self.proof)
    self.assertIn("Riverside identity proof", self.readme)
    for forbidden in ("CompetitiveWorldState", "resolved_inputs", "effect_queue", "private_rival", "transition_competitive", "fetch(", "WebSocket"):
      self.assertNotIn(forbidden, self.kit + self.proof)

  def test_javascript_syntax_is_valid(self):
    for path in (KIT, PROOF):
      if path.suffix == ".mjs":
        result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
