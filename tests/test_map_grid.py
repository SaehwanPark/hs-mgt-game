import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP_GRID = ROOT / "gui" / "map-environment.mjs"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class MapGridTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = MAP_GRID.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_grid_contract_is_deterministic_and_symbolic(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { MAP_GRID, mapGridCell } from './gui/map-environment.mjs'; const first = JSON.stringify({ grid: MAP_GRID, cell: mapGridCell(3, 4) }); const second = JSON.stringify({ grid: MAP_GRID, cell: mapGridCell(3, 4) }); let rejected = 0; for (const [column, row] of [[-1, 0], [40, 0], [0, -1], [0, 25]]) { try { mapGridCell(column, row); } catch (error) { if (error instanceof RangeError) rejected += 1; } } if (first !== second || rejected !== 4 || MAP_GRID.columns * MAP_GRID.unit !== MAP_GRID.width || MAP_GRID.rows * MAP_GRID.unit !== MAP_GRID.height || mapGridCell(3, 4).x !== 72 || mapGridCell(3, 4).y !== 96) process.exit(1); console.log(first);"],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("does not assert real-world distance, geography, travel time, or jurisdiction", result.stdout)

  def test_grid_module_has_no_runtime_side_effects(self):
    for marker in ("regional-map-grid-v1", "width: 960", "height: 600", "unit: 24", "columns: 40", "rows: 25", "mapGridCell", "RangeError"):
      self.assertIn(marker, self.source)
    for forbidden in ("fetch(", "WebSocket", "document.", "window.", "Math.random"):
      self.assertNotIn(forbidden, self.source)
    result = subprocess.run(["node", "--check", str(MAP_GRID)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_registry_hash_and_provenance(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.map.regional-grid"]
    self.assertEqual(entry["source_path"], "gui/map-environment.mjs")
    self.assertIsNone(entry["release_path"])
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(MAP_GRID.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")


if __name__ == "__main__":
  unittest.main()
