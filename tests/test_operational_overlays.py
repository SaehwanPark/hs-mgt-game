import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OVERLAYS = ROOT / "gui" / "operational-overlays.mjs"
PROOF = ROOT / "gui" / "operational-overlay-proof.html"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class OperationalOverlayTests(unittest.TestCase):
  REQUIRED_IDS = (
    "operational-staffing-constraint",
    "operational-capacity-constraint",
    "operational-demand-pressure",
    "operational-active-capital-project",
    "operational-delayed-project",
    "operational-project-completion",
    "operational-payer-network-change",
    "operational-regulatory-review",
    "operational-community-trust-concern",
    "operational-financial-distress",
    "operational-recovery",
    "operational-uncertain-stale-intelligence",
  )

  @classmethod
  def setUpClass(cls):
    cls.source = OVERLAYS.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_all_required_overlays_have_the_shared_contract(self):
    result = subprocess.run(
      [
        "node", "--input-type=module", "-e",
        "import { OPERATIONAL_OVERLAY_SET, OPERATIONAL_OVERLAY_FALLBACK, OPERATIONAL_OVERLAY_INFORMATION_BOUNDARY, operationalOverlayFor } from './gui/operational-overlays.mjs'; const required = ['operational-staffing-constraint','operational-capacity-constraint','operational-demand-pressure','operational-active-capital-project','operational-delayed-project','operational-project-completion','operational-payer-network-change','operational-regulatory-review','operational-community-trust-concern','operational-financial-distress','operational-recovery','operational-uncertain-stale-intelligence']; const fields = ['semantic_role','triggering_visible_field','non_color_pattern','reduced_motion','text_equivalent','collision_behavior','priority_rule','visible_source','information_boundary']; if (OPERATIONAL_OVERLAY_SET.length !== 12 || JSON.stringify(OPERATIONAL_OVERLAY_SET.map((entry) => entry.id)) !== JSON.stringify(required) || !OPERATIONAL_OVERLAY_SET.every((entry) => fields.every((field) => entry[field]) && entry.severity_encoding === 'none' && entry.motion === 'none' && entry.information_boundary === OPERATIONAL_OVERLAY_INFORMATION_BOUNDARY) || OPERATIONAL_OVERLAY_FALLBACK.id !== 'operational-overlay-generic' || operationalOverlayFor('missing').text_equivalent !== OPERATIONAL_OVERLAY_FALLBACK.text_equivalent) process.exit(1); console.log(JSON.stringify({ ids: required, fallback: OPERATIONAL_OVERLAY_FALLBACK, boundary: OPERATIONAL_OVERLAY_INFORMATION_BOUNDARY }));",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    for overlay_id in self.REQUIRED_IDS:
      self.assertIn(overlay_id, result.stdout)
    self.assertIn("do not infer hidden severity", result.stdout)

  def test_priority_collision_and_simultaneous_layout_are_deterministic(self):
    result = subprocess.run(
      [
        "node", "--input-type=module", "-e",
        "import { OPERATIONAL_OVERLAY_SET, orderedOperationalOverlays, layoutOperationalOverlays } from './gui/operational-overlays.mjs'; const input = [...OPERATIONAL_OVERLAY_SET].reverse().map((entry) => entry.id); const first = orderedOperationalOverlays(input); const second = orderedOperationalOverlays(input); const layout = layoutOperationalOverlays(input, 5); const fallbackLayout = layoutOperationalOverlays(input, 0); if (JSON.stringify(first) !== JSON.stringify(second) || first[0].id !== 'operational-staffing-constraint' || first[11].id !== 'operational-uncertain-stale-intelligence' || layout.visible.length !== 5 || layout.overflow_count !== 7 || layout.visible[0].collision_state !== 'stack-root' || !layout.visible.slice(1).every((entry) => entry.collision_state === 'stacked-visible') || fallbackLayout.visible.length !== 4 || !layout.overflow_text.includes('7 additional')) process.exit(1); console.log(JSON.stringify({ ordered: first.map((entry) => entry.id), layout }));",
      ],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("stack-root", result.stdout)
    self.assertIn("7 additional", result.stdout)

  def test_proof_has_text_fallback_and_reduced_motion_boundaries(self):
    for marker in (
      "Operational overlay library proof",
      "All required overlay categories",
      "Simultaneous overlay layout",
      "layoutOperationalOverlays",
      "collision-stack",
      "reduced-motion",
      "Display priority is ordering only",
      "Overflow remains visible as a count",
      "aria-label",
      "tabIndex = 0",
    ):
      self.assertIn(marker, self.proof)
    for document in (self.source, self.proof):
      for forbidden in ("fetch(", "WebSocket", "Math.random", "resolved_inputs", "private_rival", "effect_queue"):
        self.assertNotIn(forbidden, document)
    self.assertEqual(subprocess.run(["node", "--check", str(OVERLAYS)], capture_output=True, text=True, check=False).returncode, 0)

  def test_registry_hash_and_provenance(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.runtime-operational-overlays"]
    self.assertEqual(entry["source_path"], "gui/operational-overlays.mjs")
    self.assertIsNone(entry["release_path"])
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(OVERLAYS.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")


if __name__ == "__main__":
  unittest.main()
