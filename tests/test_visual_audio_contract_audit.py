import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
  "audit_visual_audio_contract",
  ROOT / "scripts" / "audit_visual_audio_contract.py",
)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AUDIT)


class VisualAudioContractAuditTests(unittest.TestCase):
  def test_current_repository_completes_the_bounded_contract(self):
    result = AUDIT.audit(ROOT)
    self.assertEqual(result["schema_version"], "visual-audio-first-month-contract-v1")
    self.assertEqual(result["status"], "complete")
    self.assertTrue(all(item["status"] == "pass" for item in result["requirements"]))
    self.assertEqual(result["presentation_boundary"]["violations"], [])

  def test_committed_compact_artifact_matches_the_audit_contract(self):
    artifact = ROOT / "_workspace" / "experiments" / "v0.12.30-first-month-contract-audit" / "audit.json"
    result = json.loads(artifact.read_text(encoding="utf-8"))
    current = AUDIT.audit(ROOT)
    self.assertEqual(result["schema_version"], current["schema_version"])
    self.assertEqual(result["status"], current["status"])
    self.assertEqual(
      [item["id"] for item in result["requirements"]],
      [item["id"] for item in AUDIT.CONTRACT_REQUIREMENTS],
    )
    self.assertEqual(
      [(item["id"], item["status"]) for item in result["requirements"]],
      [(item["id"], item["status"]) for item in current["requirements"]],
    )
    for artifact_item, current_item in zip(result["requirements"], current["requirements"]):
      self.assertEqual(artifact_item["source_evidence"], current_item["source_evidence"]["files"])
      self.assertEqual(artifact_item["test_evidence"], current_item["test_evidence"]["files"])
    self.assertEqual(result["phase_documents"]["status"], current["phase_documents"]["status"])
    self.assertEqual(result["phase_documents"]["count"], len(current["phase_documents"]["items"]))
    self.assertEqual(result["provenance"]["status"], current["provenance"]["status"])
    self.assertEqual(result["provenance"]["files"], [item["path"] for item in current["provenance"]["items"]])
    self.assertEqual(result["presentation_boundary"]["violations"], [])
    self.assertEqual(
      result["presentation_boundary"]["violations"],
      current["presentation_boundary"]["violations"],
    )

  def test_missing_marker_fails_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "source.txt"
      source.write_text("present", encoding="utf-8")
      check = AUDIT._check_files_and_markers(root, {"source.txt": ("missing",)})
      self.assertEqual(check["status"], "fail")
      self.assertEqual(check["missing_markers"], ["source.txt:missing"])

  def test_missing_file_fails_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      check = AUDIT._check_files_and_markers(
        Path(directory),
        {"missing.txt": ("marker",)},
      )
      self.assertEqual(check["status"], "fail")
      self.assertEqual(check["missing_files"], ["missing.txt"])

  def test_forbidden_presentation_marker_is_reported(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      for relative_path in AUDIT.BOUNDARY_FILES:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("resolved_inputs", encoding="utf-8")
      for relative_path in AUDIT.PHASE_DOCUMENTS + AUDIT.PROVENANCE_FILES:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("present", encoding="utf-8")
      result = AUDIT.audit(root)
      self.assertEqual(result["status"], "incomplete")
      self.assertEqual(result["presentation_boundary"]["status"], "fail")
      self.assertIn("gui/first-month.mjs:resolved_inputs", result["presentation_boundary"]["violations"])


if __name__ == "__main__":
  unittest.main()
