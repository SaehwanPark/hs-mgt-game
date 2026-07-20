import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OVERLAYS = ROOT / "gui" / "map-service-areas.mjs"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class ServiceAreaOverlayTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = OVERLAYS.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_service_area_set_is_deterministic_and_symbolic(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { SERVICE_AREA_SET, SERVICE_AREA_INFORMATION_BOUNDARY, serviceAreaFor } from './gui/map-service-areas.mjs'; const first = JSON.stringify(SERVICE_AREA_SET); const second = JSON.stringify(SERVICE_AREA_SET); const fallback = serviceAreaFor('missing'); if (first !== second || SERVICE_AREA_SET.length !== 3 || !SERVICE_AREA_SET.every((overlay) => overlay.geometry_claim === 'symbolic contour only' && overlay.metric_encoding === 'none' && overlay.directionality === 'not encoded' && overlay.non_color_pattern && overlay.information_boundary === SERVICE_AREA_INFORMATION_BOUNDARY) || fallback.id !== 'service-area-generic' || fallback.metric_encoding !== 'none' || fallback.information_boundary !== SERVICE_AREA_INFORMATION_BOUNDARY) process.exit(1); console.log(first + SERVICE_AREA_INFORMATION_BOUNDARY);"],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("service-area-primary", result.stdout)
    self.assertIn("service-area-shared", result.stdout)
    self.assertIn("service-area-coordinated", result.stdout)
    self.assertIn("do not establish real-world catchment", result.stdout)

  def test_service_area_module_is_symbolic_and_side_effect_free(self):
    for marker in ("regional-service-area-overlay-v1", "service-area-primary", "service-area-shared", "service-area-coordinated", "Service area unavailable", "geometry_claim", "metric_encoding", "non_color_pattern", "SERVICE_AREA_INFORMATION_BOUNDARY"):
      self.assertIn(marker, self.source)
    for forbidden in ("fetch(", "WebSocket", "document.", "window.", "Math.random"):
      self.assertNotIn(forbidden, self.source)
    result = subprocess.run(["node", "--check", str(OVERLAYS)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_registry_hash_and_provenance(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.map.service-area-overlays"]
    self.assertEqual(entry["source_path"], "gui/map-service-areas.mjs")
    self.assertIsNone(entry["release_path"])
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(OVERLAYS.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")


if __name__ == "__main__":
  unittest.main()
