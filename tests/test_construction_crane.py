import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source" / "visual" / "facilities" / "construction-crane.svg"
RELEASE = ROOT / "assets" / "release" / "visual" / "svg" / "construction-crane.svg"
COMPONENTS = ROOT / "gui" / "facility-components.mjs"
PROOF = ROOT / "gui" / "facility-proof.html"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class ConstructionCraneTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = SOURCE.read_text(encoding="utf-8")
    cls.release = RELEASE.read_text(encoding="utf-8")
    cls.components = COMPONENTS.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_source_release_and_crane_layers_are_distinct(self):
    for document in (self.source, self.release):
      for marker in ("<title", "<desc", "system-ui", "viewBox", "Construction crane"):
        self.assertIn(marker, document)
      self.assertNotIn('href="http://', document)
      self.assertNotIn('href="https://', document)
    self.assertIn("not a project status or completion claim", self.release)
    for marker in ("construction-crane", "identity-layer", "capacity-layer", "project-layer", "pressure-layer", "selection-layer", "uncertainty-layer"):
      self.assertIn(marker, self.source)

  def test_catalog_and_shared_proof_select_construction_crane(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { FACILITY_COMPONENTS, facilityComponentFor, facilityLayerSummary } from './gui/facility-components.mjs'; const crane = facilityComponentFor('construction-crane'); const fallback = facilityComponentFor('missing'); if (FACILITY_COMPONENTS['construction-crane'].label !== 'Construction crane' || crane.layers.length !== 7 || facilityLayerSummary('construction-crane').length !== 7) process.exit(1); if (fallback.id !== 'generic-facility') process.exit(2); console.log(JSON.stringify({ crane, fallback }));"],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    for marker in ("FACILITY_COMPONENTS", "facilityComponentFor", "facilityLayerSummary", "general-hospital-base"):
      self.assertIn(marker, self.proof)

  def test_registry_hashes_and_provenance(self):
    entries = {entry["id"]: entry for entry in self.registry["entries"]}
    entry = entries["visual.facility.construction-crane"]
    self.assertEqual(entry["source_path"], "assets/source/visual/facilities/construction-crane.svg")
    self.assertEqual(entry["release_path"], "assets/release/visual/svg/construction-crane.svg")
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(SOURCE.read_bytes()).hexdigest()}")
    self.assertEqual(entry["release_hash"], f"sha256:{hashlib.sha256(RELEASE.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")

  def test_javascript_syntax_is_valid(self):
    result = subprocess.run(["node", "--check", str(COMPONENTS)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
