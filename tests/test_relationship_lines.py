import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLES = ROOT / "gui" / "map-relationships.mjs"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class RelationshipLineTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = STYLES.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_relationship_styles_are_deterministic_and_non_directional(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { RELATIONSHIP_LINE_SET, RELATIONSHIP_INFORMATION_BOUNDARY, relationshipLineStyleFor } from './gui/map-relationships.mjs'; const first = JSON.stringify(RELATIONSHIP_LINE_SET); const second = JSON.stringify(RELATIONSHIP_LINE_SET); const fallback = relationshipLineStyleFor('missing'); if (first !== second || RELATIONSHIP_LINE_SET.length !== 4 || !RELATIONSHIP_LINE_SET.every((style) => style.arrowhead === 'none' && style.directionality === 'not encoded' && style.non_color_pattern && style.information_boundary === RELATIONSHIP_INFORMATION_BOUNDARY) || fallback.id !== 'relationship-generic' || fallback.arrowhead !== 'none' || fallback.information_boundary !== RELATIONSHIP_INFORMATION_BOUNDARY) process.exit(1); console.log(first + RELATIONSHIP_INFORMATION_BOUNDARY);"],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("relationship-peer", result.stdout)
    self.assertIn("relationship-service", result.stdout)
    self.assertIn("relationship-policy", result.stdout)
    self.assertIn("relationship-uncertain", result.stdout)
    self.assertIn("do not infer hidden intent", result.stdout)

  def test_relationship_module_is_symbolic_and_side_effect_free(self):
    for marker in ("regional-relationship-line-v1", "relationship-peer", "relationship-service", "relationship-policy", "relationship-uncertain", "Relationship unavailable", "text_equivalent", "non_color_pattern", "RELATIONSHIP_INFORMATION_BOUNDARY", "arrowhead: \"none\""):
      self.assertIn(marker, self.source)
    for forbidden in ("fetch(", "WebSocket", "document.", "window.", "Math.random"):
      self.assertNotIn(forbidden, self.source)
    result = subprocess.run(["node", "--check", str(STYLES)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_registry_hash_and_provenance(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.map.relationship-line-styles"]
    self.assertEqual(entry["source_path"], "gui/map-relationships.mjs")
    self.assertIsNone(entry["release_path"])
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(STYLES.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")


if __name__ == "__main__":
  unittest.main()
