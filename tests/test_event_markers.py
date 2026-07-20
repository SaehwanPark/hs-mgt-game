import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKERS = ROOT / "gui" / "map-event-markers.mjs"
ENVIRONMENT = ROOT / "gui" / "map-environment.mjs"
PROOF = ROOT / "gui" / "map-environment-proof.html"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class EventMarkerTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.marker_source = MARKERS.read_text(encoding="utf-8")
    cls.environment_source = ENVIRONMENT.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_event_marker_set_is_deterministic_and_severity_free(self):
    result = subprocess.run(
      [
        "node", "--input-type=module", "-e",
        "import { EVENT_MARKER_SET, EVENT_MARKER_INFORMATION_BOUNDARY, eventMarkerFor } from './gui/map-event-markers.mjs'; const first = JSON.stringify(EVENT_MARKER_SET); const second = JSON.stringify(EVENT_MARKER_SET); const fallback = eventMarkerFor('missing'); if (first !== second || EVENT_MARKER_SET.length !== 4 || !EVENT_MARKER_SET.every((marker) => marker.priority_encoding === 'none' && marker.severity_encoding === 'none' && marker.motion === 'none' && marker.non_color_pattern && marker.text_equivalent && marker.information_boundary === EVENT_MARKER_INFORMATION_BOUNDARY) || fallback.id !== 'event-marker-generic' || fallback.severity_encoding !== 'none' || fallback.information_boundary !== EVENT_MARKER_INFORMATION_BOUNDARY) process.exit(1); console.log(first + EVENT_MARKER_INFORMATION_BOUNDARY);",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    for marker_id in ("event-marker-policy", "event-marker-workforce", "event-marker-community", "event-marker-project"):
      self.assertIn(marker_id, result.stdout)
    self.assertIn("do not encode severity", result.stdout)

  def test_event_marker_and_map_contracts_are_symbolic_and_side_effect_free(self):
    for marker in (
      "regional-event-marker-v1",
      "event-marker-policy",
      "event-marker-workforce",
      "event-marker-community",
      "event-marker-project",
      "Event marker unavailable",
      "priority_encoding",
      "severity_encoding",
      "motion: \"none\"",
      "non_color_pattern",
      "EVENT_MARKER_INFORMATION_BOUNDARY",
    ):
      self.assertIn(marker, self.marker_source)
    for marker in (
      "MAP_TARGET_VIEWPORTS",
      "MAP_KEYBOARD_NAVIGATION_ORDER",
      "MAP_ZOOM_STEPS",
      "MAP_PAN_BOUNDS",
      "normalizeMapZoom",
      "clampMapPan",
      "geography_boundary",
    ):
      self.assertIn(marker, self.environment_source)
    for document in (self.marker_source, self.environment_source, self.proof):
      for forbidden in ("fetch(", "WebSocket", "Math.random", "resolved_inputs", "private_rival"):
        self.assertNotIn(forbidden, document)
    for marker in (
      "Symbolic regional board",
      "event-marker-list",
      "map-legend",
      "zoom-controls",
      "pan-controls",
      "prefers-reduced-motion",
      "MAP_TARGET_VIEWPORTS",
      "text_scale",
      "Symbolic geography disclaimer",
      "ArrowUp",
      "ArrowRight",
    ):
      self.assertIn(marker, self.proof)
    self.assertEqual(subprocess.run(["node", "--check", str(MARKERS)], capture_output=True, text=True, check=False).returncode, 0)
    self.assertEqual(subprocess.run(["node", "--check", str(ENVIRONMENT)], capture_output=True, text=True, check=False).returncode, 0)

  def test_map_interaction_contract_is_bounded_and_deterministic(self):
    result = subprocess.run(
      [
        "node", "--input-type=module", "-e",
        "import { MAP_TARGET_VIEWPORTS, MAP_KEYBOARD_NAVIGATION_ORDER, MAP_ZOOM_STEPS, MAP_PAN_BOUNDS, normalizeMapZoom, clampMapPan } from './gui/map-environment.mjs'; if (MAP_TARGET_VIEWPORTS.length !== 3 || MAP_TARGET_VIEWPORTS[0].width !== 320 || MAP_TARGET_VIEWPORTS[2].width !== 1280) process.exit(1); if (MAP_KEYBOARD_NAVIGATION_ORDER.join(',') !== 'board-heading,map-viewport,zoom-controls,pan-controls,event-marker-list,map-legend') process.exit(2); if (JSON.stringify(MAP_ZOOM_STEPS) !== '[0.75,1,1.25,1.5]' || normalizeMapZoom(99) !== 1.5 || normalizeMapZoom(-99) !== 0.75) process.exit(3); const pan = clampMapPan({ x: 999, y: -999 }); if (pan.x !== MAP_PAN_BOUNDS.x.max || pan.y !== MAP_PAN_BOUNDS.y.min) process.exit(4); console.log(JSON.stringify({ MAP_TARGET_VIEWPORTS, MAP_KEYBOARD_NAVIGATION_ORDER, MAP_ZOOM_STEPS, MAP_PAN_BOUNDS, pan }));",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("Compact", result.stdout)
    self.assertIn("pan", result.stdout)

  def test_registry_hash_and_provenance(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.map.event-marker-set"]
    self.assertEqual(entry["source_path"], "gui/map-event-markers.mjs")
    self.assertIsNone(entry["release_path"])
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(MARKERS.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")


if __name__ == "__main__":
  unittest.main()
