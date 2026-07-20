import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARCELS = ROOT / "gui" / "map-parcels.mjs"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class ParcelTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = PARCELS.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_parcel_set_is_deterministic_and_has_required_tokens(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { PARCEL_SET, SYMBOLIC_PARCEL_BOUNDARY, parcelFor } from './gui/map-parcels.mjs'; const first = JSON.stringify(PARCEL_SET); const second = JSON.stringify(PARCEL_SET); const fallback = parcelFor('missing'); if (first !== second || PARCEL_SET.length !== 2 || !PARCEL_SET.every((parcel) => parcel.paths.length === 3 && parcel.view_box === '0 0 144 120' && parcel.grid === '24px' && parcel.footprint === '6x5 cells' && parcel.geography_boundary === SYMBOLIC_PARCEL_BOUNDARY && parcel.non_color_pattern) || fallback.id !== 'parcel-generic' || fallback.geography_boundary !== SYMBOLIC_PARCEL_BOUNDARY) process.exit(1); console.log(first + SYMBOLIC_PARCEL_BOUNDARY);"],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("parcel-facility", result.stdout)
    self.assertIn("parcel-undeveloped", result.stdout)
    self.assertIn("do not establish real-world ownership", result.stdout)

  def test_parcel_module_is_symbolic_and_side_effect_free(self):
    for marker in ("regional-parcel-v1", "parcel-facility", "parcel-undeveloped", "Parcel unavailable", "text_equivalent", "non_color_pattern", "SYMBOLIC_PARCEL_BOUNDARY"):
      self.assertIn(marker, self.source)
    for forbidden in ("fetch(", "WebSocket", "document.", "window.", "Math.random"):
      self.assertNotIn(forbidden, self.source)
    result = subprocess.run(["node", "--check", str(PARCELS)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_registry_hash_and_provenance(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.map.parcel-system"]
    self.assertEqual(entry["source_path"], "gui/map-parcels.mjs")
    self.assertIsNone(entry["release_path"])
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(PARCELS.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")


if __name__ == "__main__":
  unittest.main()
