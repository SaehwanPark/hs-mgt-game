import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "gui" / "actor-families.mjs"
PROOF = ROOT / "gui" / "actor-family-proof.html"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class ActorFamilyLanguageTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.catalog = CATALOG.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_all_families_have_shared_language_and_visible_equivalents(self):
    result = subprocess.run(
      [
        "node",
        "--input-type=module",
        "-e",
        "import { ACTOR_FAMILIES, actorFamilyFor, actorFamilySummary } from './gui/actor-families.mjs'; const expected = ['payer', 'regulator', 'labor', 'employer', 'community', 'board', 'policy-coalition', 'independent-provider']; if (ACTOR_FAMILIES.length !== expected.length || ACTOR_FAMILIES.map((family) => family.id).join('|') !== expected.join('|')) process.exit(1); for (const family of ACTOR_FAMILIES) { for (const key of ['glyph', 'icon_shape', 'report_frame', 'notification_style', 'source', 'equivalent']) if (!family[key]) process.exit(2); } const fallback = actorFamilyFor('missing'); if (fallback.id !== 'generic-actor' || actorFamilySummary('missing').sonic_tag !== null) process.exit(3); console.log(JSON.stringify({ families: ACTOR_FAMILIES, fallback }));",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    payload = json.loads(result.stdout)
    self.assertEqual(len(payload["families"]), 8)
    self.assertEqual(payload["fallback"]["id"], "generic-actor")

  def test_proof_has_non_color_cues_and_safe_fallback(self):
    for marker in (
      "Actor-family Language Proof",
      "Show generic fallback",
      "data-frame",
      "data-shape",
      "Written notification",
      "written equivalent retained",
      "actorFamilySummary",
    ):
      self.assertIn(marker, self.proof)
    for forbidden in ("CompetitiveWorldState", "resolved_inputs", "private_rival", "fetch(", "WebSocket"):
      self.assertNotIn(forbidden, self.catalog + self.proof)

  def test_actor_family_catalog_is_registry_backed(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.actor-family-language"]
    self.assertEqual(entry["source_path"], "gui/actor-families.mjs")
    self.assertEqual(entry["release_path"], None)
    self.assertEqual(entry["approval_status"], "approved")
    self.assertIn("actor-family ID", entry["visible_source"])
    self.assertIn("written", entry["accessible_equivalent"])

  def test_javascript_syntax_is_valid(self):
    result = subprocess.run(["node", "--check", str(CATALOG)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
