import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source" / "visual" / "facilities" / "general-hospital-base.svg"
RELEASE = ROOT / "assets" / "release" / "visual" / "svg" / "general-hospital-base.svg"
COMPONENTS = ROOT / "gui" / "facility-components.mjs"
PROOF = ROOT / "gui" / "facility-proof.html"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class GeneralHospitalBaseTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = SOURCE.read_text(encoding="utf-8")
    cls.release = RELEASE.read_text(encoding="utf-8")
    cls.components = COMPONENTS.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_source_release_and_layer_contract(self):
    for document in (self.source, self.release):
      for marker in ("<title", "<desc", "system-ui", "viewBox"):
        self.assertIn(marker, document)
      self.assertNotIn('href="http://', document)
      self.assertNotIn('href="https://', document)
    for marker in ("hospital-base", "identity-layer", "capacity-layer", "project-layer", "pressure-layer", "selection-layer", "uncertainty-layer"):
      self.assertIn(marker, self.source)
    for marker in ("--facility-primary", "--facility-secondary", "--facility-ink", "--facility-paper", "--facility-muted"):
      self.assertIn(marker, self.source)

  def test_component_catalog_and_generic_fallback(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { facilityComponentFor, facilityLayerSummary } from './gui/facility-components.mjs'; const component = facilityComponentFor('general-hospital-base'); const fallback = facilityComponentFor('future-facility'); if (component.layers.length !== 7 || component.grid !== '8px' || component.view_box !== '0 0 760 500') process.exit(1); if (facilityLayerSummary().length !== 7 || fallback.id !== 'generic-facility' || fallback.fallback?.label !== 'Facility' || fallback.fallback?.equivalent !== 'Facility label and generic marker') process.exit(2); if (JSON.stringify(component).includes('resolved_inputs') || JSON.stringify(component).includes('private')) process.exit(3); console.log(JSON.stringify({ component, fallback }));"],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_proof_preserves_text_and_layer_patterns(self):
    for marker in ("Facility Component Proof", "release/visual/svg/general-hospital-base.svg", "Composable layers", "Written equivalent", "data-kind", "generic facility fallback"):
      self.assertIn(marker, self.proof)
    for forbidden in ("CompetitiveWorldState", "resolved_inputs", "effect_queue", "private_rival", "fetch(", "WebSocket"):
      self.assertNotIn(forbidden, self.components + self.proof)

  def test_registry_entry_hashes_and_provenance(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.facility.general-hospital-base"]
    self.assertEqual(entry["source_path"], "assets/source/visual/facilities/general-hospital-base.svg")
    self.assertEqual(entry["release_path"], "assets/release/visual/svg/general-hospital-base.svg")
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(SOURCE.read_bytes()).hexdigest()}")
    self.assertEqual(entry["release_hash"], f"sha256:{hashlib.sha256(RELEASE.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")

  def test_javascript_syntax_is_valid(self):
    result = subprocess.run(["node", "--check", str(COMPONENTS)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
