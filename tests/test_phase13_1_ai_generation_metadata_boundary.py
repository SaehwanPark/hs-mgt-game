import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
LEDGER = ROOT / "docs" / "evaluation" / "phase13.1-ai-generation-metadata-boundary.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"
WORKFLOW = ROOT / "assets" / "generation" / "generation-workflow.json"
MODELS = ROOT / "assets" / "generation" / "approved-models.json"
MANIFEST = ROOT / "assets" / "generation" / "generation-manifest.json"
PORTRAIT_SET = ROOT / "assets" / "generation" / "portrait-set.json"
PORTRAITS = ROOT / "assets" / "generation" / "portrait-previews.json"
PORTRAIT_QUEUE = ROOT / "assets" / "generation" / "portrait-review-queue.json"
REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"


def load_module(name, relative_path):
  spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
  module = importlib.util.module_from_spec(spec)
  assert spec.loader is not None
  spec.loader.exec_module(module)
  return module


VALIDATOR = load_module(
  "validate_generation_metadata_phase13_1", "scripts/validate_generation_metadata.py"
)

EXPECTED_SOURCE_CONTRACT = {
  "approved_model_registry": (
    "assets/generation/approved-models.json",
    "approved-generation-models-v1",
  ),
  "generation_workflow": (
    "assets/generation/generation-workflow.json",
    "generation-workflow-v1",
  ),
  "capture_validator": (
    "scripts/capture_generation_metadata.py",
    "generation-record-v1",
  ),
  "workflow_validator": (
    "scripts/validate_generation_metadata.py",
    "generation workflow check: passed",
  ),
  "portrait_previews": (
    "assets/generation/portrait-previews.json",
    "fictional-portrait-preview-v1",
  ),
  "portrait_review_queue": (
    "assets/generation/portrait-review-queue.json",
    "fictional-portrait-review-queue-v1",
  ),
  "generation_manifest": (
    "assets/generation/generation-manifest.json",
    "generation-manifest-v1",
  ),
  "visual_registry": (
    "assets/registry/visual-assets.json",
    "asset-registry-v1",
  ),
}

EXPECTED_FINDINGS = {
  "approved_model_registry_complete": True,
  "required_metadata_contract_complete": True,
  "current_preview_source_hashes_complete": True,
  "current_preview_model_and_seed_metadata": False,
  "current_preview_human_review": False,
  "current_preview_release_eligible": False,
  "promotion_validation_fail_closed": True,
  "generation_manifest_empty": True,
  "visual_registry_excludes_previews": True,
}


class Phase131AiGenerationMetadataBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")
    cls.workflow = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    cls.models = json.loads(MODELS.read_text(encoding="utf-8"))
    cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cls.portrait_set = json.loads(PORTRAIT_SET.read_text(encoding="utf-8"))
    cls.portraits = json.loads(PORTRAITS.read_text(encoding="utf-8"))
    cls.portrait_queue = json.loads(PORTRAIT_QUEUE.read_text(encoding="utf-8"))
    cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

  def test_source_contract_markers_are_anchored(self):
    self.assertEqual(
      self.ledger["schema_version"],
      "phase13.1-ai-generation-metadata-boundary-v1",
    )
    self.assertEqual(
      self.ledger["status"], "complete-current-technical-metadata-boundary-only"
    )
    self.assertEqual(self.ledger["findings"], EXPECTED_FINDINGS)
    self.assertEqual(
      set(self.ledger["source_contract"]), set(EXPECTED_SOURCE_CONTRACT)
    )
    for key, (source_path, marker) in EXPECTED_SOURCE_CONTRACT.items():
      self.assertEqual(
        self.ledger["source_contract"][key], f"{source_path}: {marker}"
      )
      path = ROOT / source_path
      self.assertTrue(path.is_file(), key)
      self.assertIn(marker, path.read_text(encoding="utf-8"), key)

  def test_existing_workflow_and_model_registry_pass_technical_validation(self):
    self.assertEqual(VALIDATOR.validate(), [])
    self.assertEqual(self.workflow["schema_version"], "generation-workflow-v1")
    self.assertIn("model_revision", self.workflow["required_metadata_fields"])
    self.assertIn("seed", self.workflow["required_metadata_fields"])
    self.assertIn("human_review", self.workflow["required_metadata_fields"])
    self.assertEqual(self.models["schema_version"], "approved-generation-models-v1")
    self.assertGreaterEqual(len(self.models["entries"]), 1)
    for model in self.models["entries"]:
      self.assertEqual(model["approval_status"], "approved-for-local-prototype")
      self.assertTrue(model["model_revision"])
      self.assertTrue(model["model_license"])

  def test_current_previews_remain_missing_provenance_and_unreleased(self):
    entries = self.portraits["entries"]
    self.assertEqual(len(entries), 7)
    self.assertFalse(self.portraits["release_eligible"])
    self.assertEqual(self.manifest["entries"], [])
    registry_ids = {entry["id"] for entry in self.registry["entries"]}
    queue_by_asset = {
      entry["asset_id"]: entry for entry in self.portrait_queue["entries"]
    }
    for entry in entries:
      self.assertEqual(entry["preview_status"], "unverified-preview")
      self.assertEqual(entry["approval_status"], "pending")
      self.assertIsNone(entry["model_id"])
      self.assertIsNone(entry["model_revision"])
      self.assertIsNone(entry["model_license"])
      self.assertIsNone(entry["model_card_url"])
      self.assertIsNone(entry["sampler"])
      self.assertIsNone(entry["seed"])
      self.assertIsNone(entry["release_path"])
      self.assertIsNone(entry["release_hash"])
      self.assertIsNone(entry["asset_registry_id"])
      self.assertNotIn(entry["asset_id"], registry_ids)
      self.assertTrue(entry["human_review"]["accessibility_equivalent_written"])
      self.assertTrue(entry["human_review"]["source_output_preserved"])
      for field in (
        "real_person_resemblance_reviewed",
        "logo_trademark_reviewed",
        "clinical_plausibility_reviewed",
        "artifact_quality_reviewed",
        "release_derivative_reviewed",
      ):
        self.assertFalse(entry["human_review"][field])
      queue_entry = queue_by_asset[entry["asset_id"]]
      self.assertEqual(queue_entry["decision"], "pending")
      self.assertEqual(queue_entry["approval_status"], "pending")
      self.assertFalse(any(queue_entry["gates"].values()))

  def test_promotion_shaped_mutation_fails_closed(self):
    promoted = copy.deepcopy(self.portraits)
    promoted_entry = promoted["entries"][0]
    promoted_entry["preview_status"] = "approved"
    promoted_entry["approval_status"] = "approved"
    errors = VALIDATOR.validate_portrait_documents(
      self.portrait_set,
      promoted,
      self.manifest,
      {entry["id"] for entry in self.registry["entries"]},
    )
    self.assertTrue(
      any("requires approved model_id" in error for error in errors), errors
    )
    self.assertTrue(
      any("requires model_revision" in error for error in errors), errors
    )

    guessed_seed = copy.deepcopy(self.portraits)
    guessed_seed["entries"][0]["seed"] = 42
    errors = VALIDATOR.validate_portrait_documents(
      self.portrait_set,
      guessed_seed,
      self.manifest,
      {entry["id"] for entry in self.registry["entries"]},
    )
    self.assertTrue(any("must keep" in error and "seed" in error for error in errors), errors)

  def test_roadmap_keeps_technical_readiness_separate_from_open_gate(self):
    normalized = " ".join(self.roadmap.split())
    self.assertIn(
      "[ ] AI-generation metadata complete.",
      normalized,
    )
    for marker in (
      "phase13.1-ai-generation-metadata-boundary.json",
      "actual model identity, immutable revision, sampler, and seed",
      "remain `unverified-preview`/`pending`",
      "human-review gates remain open",
    ):
      self.assertIn(marker, normalized.lower())
    limits = " ".join(self.ledger["limits"]).lower()
    for marker in (
      "actual model identity",
      "seed",
      "human-review",
      "public-release readiness",
    ):
      self.assertIn(marker, limits)


if __name__ == "__main__":
  unittest.main()
