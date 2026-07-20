import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TILES = ROOT / "gui" / "map-districts.mjs"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class DistrictTileTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = TILES.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_district_tile_set_is_deterministic_and_has_required_tokens(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { DISTRICT_TILE_SET, SYMBOLIC_DISTRICT_BOUNDARY, districtTileFor } from './gui/map-districts.mjs'; const first = JSON.stringify(DISTRICT_TILE_SET); const second = JSON.stringify(DISTRICT_TILE_SET); const fallback = districtTileFor('missing'); if (first !== second || DISTRICT_TILE_SET.length !== 4 || !DISTRICT_TILE_SET.every((tile) => tile.paths.length === 3 && tile.view_box === '0 0 192 144' && tile.grid === '24px' && tile.footprint === '8x6 cells' && tile.geography_boundary === SYMBOLIC_DISTRICT_BOUNDARY && tile.non_color_pattern) || fallback.id !== 'district-generic' || fallback.geography_boundary !== SYMBOLIC_DISTRICT_BOUNDARY) process.exit(1); console.log(first + SYMBOLIC_DISTRICT_BOUNDARY);"],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("district-commercial", result.stdout)
    self.assertIn("district-residential", result.stdout)
    self.assertIn("district-employer-center", result.stdout)
    self.assertIn("district-government", result.stdout)
    self.assertIn("do not establish real-world land use", result.stdout)

  def test_district_tile_module_is_symbolic_and_side_effect_free(self):
    for marker in ("regional-district-tile-v1", "district-commercial", "district-residential", "district-employer-center", "district-government", "District unavailable", "text_equivalent", "non_color_pattern", "SYMBOLIC_DISTRICT_BOUNDARY"):
      self.assertIn(marker, self.source)
    for forbidden in ("fetch(", "WebSocket", "document.", "window.", "Math.random"):
      self.assertNotIn(forbidden, self.source)
    result = subprocess.run(["node", "--check", str(TILES)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_registry_hash_and_provenance(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.map.district-tile-set"]
    self.assertEqual(entry["source_path"], "gui/map-districts.mjs")
    self.assertIsNone(entry["release_path"])
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(TILES.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")


if __name__ == "__main__":
  unittest.main()
