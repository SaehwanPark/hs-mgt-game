import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source" / "visual" / "facilities" / "undeveloped-parcel.svg"
RELEASE = ROOT / "assets" / "release" / "visual" / "svg" / "undeveloped-parcel.svg"
COMPONENTS = ROOT / "gui" / "facility-components.mjs"
PROOF = ROOT / "gui" / "facility-proof.html"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


class UndevelopedParcelTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.source = SOURCE.read_text(encoding="utf-8")
    cls.release = RELEASE.read_text(encoding="utf-8")
    cls.components = COMPONENTS.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_source_release_and_parcel_layers_are_distinct(self):
    for document in (self.source, self.release):
      for marker in ("<title", "<desc", "system-ui", "viewBox", "Undeveloped parcel"):
        self.assertIn(marker, document)
      self.assertNotIn('href="http://', document)
      self.assertNotIn('href="https://', document)
    self.assertIn("not a development potential, ownership, or future use claim", self.release)
    for marker in ("undeveloped-parcel", "identity-layer", "capacity-layer", "project-layer", "pressure-layer", "selection-layer", "uncertainty-layer"):
      self.assertIn(marker, self.source)

  def test_catalog_and_shared_proof_select_undeveloped_parcel(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", "import { FACILITY_COMPONENTS, facilityComponentFor, facilityLayerSummary } from './gui/facility-components.mjs'; const parcel = facilityComponentFor('undeveloped-parcel'); const fallback = facilityComponentFor('missing'); if (FACILITY_COMPONENTS['undeveloped-parcel'].label !== 'Undeveloped parcel' || parcel.layers.length !== 7 || facilityLayerSummary('undeveloped-parcel').length !== 7) process.exit(1); if (fallback.id !== 'generic-facility') process.exit(2); console.log(JSON.stringify({ parcel, fallback }));"],
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
    entry = entries["visual.facility.undeveloped-parcel"]
    self.assertEqual(entry["source_path"], "assets/source/visual/facilities/undeveloped-parcel.svg")
    self.assertEqual(entry["release_path"], "assets/release/visual/svg/undeveloped-parcel.svg")
    self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(SOURCE.read_bytes()).hexdigest()}")
    self.assertEqual(entry["release_hash"], f"sha256:{hashlib.sha256(RELEASE.read_bytes()).hexdigest()}")
    self.assertEqual(entry["approval_status"], "approved")

  def test_javascript_syntax_is_valid(self):
    result = subprocess.run(["node", "--check", str(COMPONENTS)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
