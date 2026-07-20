import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OVERLAYS = ROOT / "gui" / "map-uncertainty.mjs"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class UncertaintyOverlayTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = OVERLAYS.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_uncertainty_set_is_deterministic_and_severity_free(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { UNCERTAINTY_SET, UNCERTAINTY_INFORMATION_BOUNDARY, uncertaintyFor } from './gui/map-uncertainty.mjs'; const first = JSON.stringify(UNCERTAINTY_SET); const second = JSON.stringify(UNCERTAINTY_SET); const fallback = uncertaintyFor('missing'); if (first !== second || UNCERTAINTY_SET.length !== 3 || !UNCERTAINTY_SET.every((overlay) => overlay.severity_encoding === 'none' && overlay.motion === 'none' && overlay.non_color_pattern && overlay.information_boundary === UNCERTAINTY_INFORMATION_BOUNDARY) || fallback.id !== 'uncertainty-generic' || fallback.severity_encoding !== 'none' || fallback.information_boundary !== UNCERTAINTY_INFORMATION_BOUNDARY) process.exit(1); console.log(first + UNCERTAINTY_INFORMATION_BOUNDARY);"],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("uncertainty-stale", result.stdout)
    self.assertIn("uncertainty-missing", result.stdout)
    self.assertIn("uncertainty-revised", result.stdout)
    self.assertIn("do not quantify hidden risk", result.stdout)

  def test_uncertainty_module_is_symbolic_and_side_effect_free(self):
    for marker in ("regional-uncertainty-overlay-v1", "uncertainty-stale", "uncertainty-missing", "uncertainty-revised", "Information status unavailable", "severity_encoding", "motion: \"none\"", "non_color_pattern", "UNCERTAINTY_INFORMATION_BOUNDARY"):
      self.assertIn(marker, self.source)
    for forbidden in ("fetch(", "WebSocket", "document.", "window.", "Math.random"):
      self.assertNotIn(forbidden, self.source)
    result = subprocess.run(["node", "--check", str(OVERLAYS)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_registry_hash_and_provenance(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.map.uncertainty-overlays"]
    self.assertEqual(entry["source_path"], "gui/map-uncertainty.mjs")
    self.assertIsNone(entry["release_path"])
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(OVERLAYS.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")


if __name__ == "__main__":
  unittest.main()
