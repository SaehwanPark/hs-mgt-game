import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source" / "visual" / "identity" / "summit-kit.svg"
RELEASE = ROOT / "assets" / "release" / "visual" / "svg" / "summit.svg"
KIT = ROOT / "gui" / "identity-kits.mjs"
PROOF = ROOT / "gui" / "identity-proof.html"


class SummitIdentityTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = SOURCE.read_text(encoding="utf-8")
    cls.release = RELEASE.read_text(encoding="utf-8")
    cls.kit = KIT.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")

  def test_source_release_and_kit_are_summit_specific(self):
    for document in (self.source, self.release):
      for marker in ("Summit", "<title", "<desc", "system-ui"):
        self.assertIn(marker, document)
      self.assertNotIn('href="http://', document)
      self.assertNotIn('href="https://', document)
    for marker in ("summit-mark", "summit-mark-mono", "summit-compact", "Summit Center", "MARKET SIGNAL", "SM"):
      self.assertIn(marker, self.source)
    for marker in ("id: \"summit\"", "monogram: \"SM\"", "summit-kit.svg", "summit.svg", "audio.direction-summit-motif"):
      self.assertIn(marker, self.kit)

  def test_shared_proof_selects_summit_and_fallback(self):
    for marker in ("Show Summit", "render(\"summit\")", "render(\"unknown\")", "document.title"):
      self.assertIn(marker, self.proof)
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { identityKitFor } from './gui/identity-kits.mjs'; const kit = identityKitFor('summit'); const fallback = identityKitFor('missing'); if (kit.label !== 'Summit' || kit.monogram !== 'SM' || fallback.id !== 'generic-institution') process.exit(1);"],
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
