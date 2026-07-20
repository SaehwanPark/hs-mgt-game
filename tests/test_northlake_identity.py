import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source" / "visual" / "identity" / "northlake-kit.svg"
RELEASE = ROOT / "assets" / "release" / "visual" / "svg" / "northlake.svg"
KIT = ROOT / "gui" / "identity-kits.mjs"
PROOF = ROOT / "gui" / "identity-proof.html"


class NorthlakeIdentityTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = SOURCE.read_text(encoding="utf-8")
    cls.release = RELEASE.read_text(encoding="utf-8")
    cls.kit = KIT.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")

  def test_source_release_and_kit_are_northlake_specific(self):
    for document in (self.source, self.release):
      for marker in ("Northlake", "<title", "<desc", "system-ui"):
        self.assertIn(marker, document)
      self.assertNotIn('href="http://', document)
      self.assertNotIn('href="https://', document)
    for marker in ("northlake-mark", "northlake-mark-mono", "northlake-compact", "Northlake Clinic", "PUBLIC SIGNAL", "NL"):
      self.assertIn(marker, self.source)
    for marker in ("id: \"northlake\"", "monogram: \"NL\"", "northlake-kit.svg", "northlake.svg", "audio.direction-northlake-motif"):
      self.assertIn(marker, self.kit)

  def test_shared_proof_selects_northlake_and_keeps_fallback(self):
    for marker in ("Show Northlake", "render(\"northlake\")", "render(\"unknown\")", "kit.asset.release_path"):
      self.assertIn(marker, self.proof)
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { identityKitFor } from './gui/identity-kits.mjs'; const kit = identityKitFor('northlake'); const fallback = identityKitFor('missing'); if (kit.label !== 'Northlake' || kit.monogram !== 'NL' || fallback.id !== 'generic-institution') process.exit(1);"],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_javascript_syntax_is_valid(self):
    result = subprocess.run(["node", "--check", str(KIT)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
