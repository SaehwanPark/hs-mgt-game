import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TILES = ROOT / "gui" / "map-tiles.mjs"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class RoadTileTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = TILES.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_road_tile_set_is_deterministic_and_has_required_tokens(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { ROAD_TILE_SET, SYMBOLIC_ROAD_BOUNDARY, roadTileFor } from './gui/map-tiles.mjs'; const first = JSON.stringify(ROAD_TILE_SET); const second = JSON.stringify(ROAD_TILE_SET); const fallback = roadTileFor('missing'); if (first !== second || ROAD_TILE_SET.length !== 3 || !ROAD_TILE_SET.every((tile) => tile.paths.length === 2 && tile.geography_boundary === SYMBOLIC_ROAD_BOUNDARY) || fallback.id !== 'road-generic' || fallback.geography_boundary !== SYMBOLIC_ROAD_BOUNDARY) process.exit(1); console.log(first + SYMBOLIC_ROAD_BOUNDARY);"],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("road-straight-horizontal", result.stdout)
    self.assertIn("road-curve-quarter", result.stdout)
    self.assertIn("do not establish real-world road geometry", result.stdout)

  def test_road_tile_module_is_symbolic_and_side_effect_free(self):
    for marker in ("regional-road-tile-v1", "road-straight-horizontal", "road-straight-vertical", "road-curve-quarter", "Road segment unavailable", "text_equivalent", "SYMBOLIC_ROAD_BOUNDARY"):
      self.assertIn(marker, self.source)
    for forbidden in ("fetch(", "WebSocket", "document.", "window.", "Math.random"):
      self.assertNotIn(forbidden, self.source)
    result = subprocess.run(["node", "--check", str(TILES)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_registry_hash_and_provenance(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.map.road-tile-set"]
    self.assertEqual(entry["source_path"], "gui/map-tiles.mjs")
    self.assertIsNone(entry["release_path"])
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(TILES.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")


if __name__ == "__main__":
  unittest.main()
