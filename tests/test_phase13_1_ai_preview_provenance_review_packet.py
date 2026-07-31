import hashlib
import json
import struct
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "evaluation" / "phase13.1-ai-preview-provenance-review-packet.json"
AI_BOUNDARY = ROOT / "docs" / "evaluation" / "phase13.1-ai-generation-metadata-boundary.json"
ATTRIBUTION = ROOT / "docs" / "evaluation" / "phase13.1-attribution-boundary.json"
PORTRAITS = ROOT / "assets" / "generation" / "portrait-previews.json"
QUEUE = ROOT / "assets" / "generation" / "portrait-review-queue.json"
PORTRAIT_SET = ROOT / "assets" / "generation" / "portrait-set.json"
WORKFLOW = ROOT / "assets" / "generation" / "generation-workflow.json"
APPROVED_MODELS = ROOT / "assets" / "generation" / "approved-models.json"
GENERATION_MANIFEST = ROOT / "assets" / "generation" / "generation-manifest.json"
VISUAL_REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"
AUDIO_REGISTRY = ROOT / "assets" / "registry" / "audio-assets.json"
RELEASE_MANIFEST = ROOT / "assets" / "ASSET_RELEASE_MANIFEST.json"
ASSET_CREDITS = ROOT / "assets" / "ASSET_CREDITS.md"
THIRD_PARTY_NOTICES = ROOT / "assets" / "THIRD_PARTY_NOTICES.md"
RUNTIME_CREDITS = ROOT / "gui" / "asset-credits.mjs"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"


EXPECTED_SHARED_SOURCES = {
  "ai_metadata_boundary": "docs/evaluation/phase13.1-ai-generation-metadata-boundary.json",
  "attribution_boundary": "docs/evaluation/phase13.1-attribution-boundary.json",
  "generation_workflow": "assets/generation/generation-workflow.json",
  "approved_model_registry": "assets/generation/approved-models.json",
  "portrait_set": "assets/generation/portrait-set.json",
  "portrait_previews": "assets/generation/portrait-previews.json",
  "portrait_review_queue": "assets/generation/portrait-review-queue.json",
  "generation_manifest": "assets/generation/generation-manifest.json",
  "visual_registry": "assets/registry/visual-assets.json",
  "audio_registry": "assets/registry/audio-assets.json",
  "release_manifest": "assets/ASSET_RELEASE_MANIFEST.json",
  "credits": "assets/ASSET_CREDITS.md",
  "runtime_credits": "gui/asset-credits.mjs",
  "generation_validator": "scripts/validate_generation_metadata.py",
  "asset_validator": "scripts/validate_assets.py",
  "release_validator": "scripts/verify_asset_release.py",
  "generation_boundary_test": "tests/test_phase13_1_ai_generation_metadata_boundary.py",
  "attribution_boundary_test": "tests/test_phase13_1_attribution_boundary.py",
  "portrait_workflow_test": "tests/test_portrait_workflow.py",
}


EXPECTED_SOURCE_CONTRACT = {
  "ai_metadata_schema": (
    "docs/evaluation/phase13.1-ai-generation-metadata-boundary.json",
    "phase13.1-ai-generation-metadata-boundary-v1",
  ),
  "ai_metadata_limits": (
    "docs/evaluation/phase13.1-ai-generation-metadata-boundary.json",
    "human-review, and public-release readiness gates remain open",
  ),
  "attribution_schema": (
    "docs/evaluation/phase13.1-attribution-boundary.json",
    "phase13.1-attribution-boundary-v1",
  ),
  "approved_models_schema": (
    "assets/generation/approved-models.json",
    "approved-generation-models-v1",
  ),
  "workflow_schema": (
    "assets/generation/generation-workflow.json",
    "generation-workflow-v1",
  ),
  "required_model_revision": (
    "assets/generation/generation-workflow.json",
    '"model_revision"',
  ),
  "required_seed": ("assets/generation/generation-workflow.json", '"seed"'),
  "required_human_review": (
    "assets/generation/generation-workflow.json",
    '"human_review"',
  ),
  "fictional_portrait_set_schema": (
    "assets/generation/portrait-set.json",
    "fictional-portrait-set-v1",
  ),
  "portrait_prohibited_content": (
    "assets/generation/portrait-set.json",
    "public-figure or identifiable-real-person resemblance",
  ),
  "portrait_preview_schema": (
    "assets/generation/portrait-previews.json",
    "fictional-portrait-preview-v1",
  ),
  "preview_unverified_status": (
    "assets/generation/portrait-previews.json",
    "unverified-preview",
  ),
  "preview_missing_model": (
    "assets/generation/portrait-previews.json",
    "not-exposed-by-preview-tool",
  ),
  "preview_release_block": (
    "assets/generation/portrait-previews.json",
    "Preview tool does not expose the approved local model revision or actual seed",
  ),
  "review_queue_schema": (
    "assets/generation/portrait-review-queue.json",
    "fictional-portrait-review-queue-v1",
  ),
  "review_queue_pending": (
    "assets/generation/portrait-review-queue.json",
    "pending-human-review",
  ),
  "review_queue_required_gate": (
    "assets/generation/portrait-review-queue.json",
    "model_and_seed_provenance",
  ),
  "generation_manifest_schema": (
    "assets/generation/generation-manifest.json",
    "generation-manifest-v1",
  ),
  "visual_registry_schema": (
    "assets/registry/visual-assets.json",
    "asset-registry-v1",
  ),
  "release_manifest_schema": (
    "assets/ASSET_RELEASE_MANIFEST.json",
    "asset-release-manifest-v1",
  ),
  "asset_credits_boundary": (
    "assets/ASSET_CREDITS.md",
    "No third-party release assets are included",
  ),
  "runtime_credits_boundary": (
    "gui/asset-credits.mjs",
    '"third_party_release_count": 0',
  ),
  "generation_validator": (
    "scripts/validate_generation_metadata.py",
    "generation workflow check: passed",
  ),
  "asset_validator": (
    "scripts/validate_assets.py",
    "asset registry check: passed",
  ),
  "release_validator": (
    "scripts/verify_asset_release.py",
    "asset release manifest check: passed",
  ),
  "generation_test": (
    "tests/test_phase13_1_ai_generation_metadata_boundary.py",
    "test_promotion_shaped_mutation_fails_closed",
  ),
  "attribution_test": (
    "tests/test_phase13_1_attribution_boundary.py",
    "test_unverified_portraits_cannot_enter_attribution_or_release_surfaces",
  ),
  "portrait_test": (
    "tests/test_portrait_workflow.py",
    "test_preview_is_hash_bound_and_release_blocked",
  ),
}


EXPECTED_GATES = [
  "identity_only",
  "role_consistency",
  "real_person_resemblance",
  "protected_marks_and_text",
  "artifact_quality",
  "accessible_equivalent",
  "small_size",
  "grayscale",
  "model_and_seed_provenance",
  "release_derivative",
  "registry_bridge",
]


def png_dimensions(path):
  data = path.read_bytes()
  if data[:8] != b"\x89PNG\r\n\x1a\n":
    raise AssertionError(f"not a PNG: {path}")
  return struct.unpack(">II", data[16:24])


class AiPreviewProvenanceReviewPacketTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = json.loads(PACKET.read_text(encoding="utf-8"))
    cls.ai_boundary = json.loads(AI_BOUNDARY.read_text(encoding="utf-8"))
    cls.attribution = json.loads(ATTRIBUTION.read_text(encoding="utf-8"))
    cls.previews = json.loads(PORTRAITS.read_text(encoding="utf-8"))
    cls.queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    cls.portrait_set = json.loads(PORTRAIT_SET.read_text(encoding="utf-8"))
    cls.workflow = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    cls.approved_models = json.loads(APPROVED_MODELS.read_text(encoding="utf-8"))
    cls.generation_manifest = json.loads(GENERATION_MANIFEST.read_text(encoding="utf-8"))
    cls.visual_registry = json.loads(VISUAL_REGISTRY.read_text(encoding="utf-8"))
    cls.audio_registry = json.loads(AUDIO_REGISTRY.read_text(encoding="utf-8"))
    cls.release_manifest = json.loads(RELEASE_MANIFEST.read_text(encoding="utf-8"))
    cls.asset_credits = ASSET_CREDITS.read_text(encoding="utf-8")
    cls.third_party_notices = THIRD_PARTY_NOTICES.read_text(encoding="utf-8")
    cls.runtime_credits = RUNTIME_CREDITS.read_text(encoding="utf-8")
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")

  def test_packet_is_technical_only_and_not_a_release_asset(self):
    self.assertEqual(
      self.packet["schema_version"],
      "phase13.1-ai-preview-provenance-review-packet-v1",
    )
    self.assertEqual(
      self.packet["status"],
      "complete-technical-packet-pending-human-review",
    )
    self.assertTrue(self.packet["review_boundary"]["technical_packet_complete"])
    self.assertTrue(self.packet["review_boundary"]["preview_source_inventory_complete"])
    for key, value in self.packet["review_boundary"].items():
      if key not in ("technical_packet_complete", "preview_source_inventory_complete"):
        self.assertFalse(value, key)
    self.assertFalse(self.packet["technical_contract"]["release_eligible"])
    self.assertTrue(self.packet["release_boundary"]["technical_packet_does_not_authorize_promotion"])
    self.assertEqual(self.packet["release_boundary"]["release_asset_paths"], [])
    release_text = RELEASE_MANIFEST.read_text(encoding="utf-8")
    for record in self.packet["preview_records"]:
      self.assertNotIn(record["source_output_path"], release_text)

  def test_shared_sources_and_source_contract_are_exactly_anchored(self):
    self.assertEqual(self.packet["shared_sources"], EXPECTED_SHARED_SOURCES)
    for source_path in self.packet["shared_sources"].values():
      self.assertTrue((ROOT / source_path).is_file(), source_path)
    self.assertEqual(set(self.packet["source_contract"]), set(EXPECTED_SOURCE_CONTRACT))
    for key, (source_path, marker) in EXPECTED_SOURCE_CONTRACT.items():
      self.assertEqual(self.packet["source_contract"][key], f"{source_path}: {marker}")
      path = ROOT / source_path
      self.assertTrue(path.is_file(), key)
      source_text = " ".join(path.read_text(encoding="utf-8").split())
      self.assertIn(" ".join(marker.split()), source_text, key)

  def test_preview_records_match_source_files_hashes_dimensions_and_roles(self):
    self.assertEqual(len(self.packet["preview_records"]), 7)
    self.assertEqual(
      [record["asset_id"] for record in self.packet["preview_records"]],
      [f"visual.portrait.{entry['role_id']}" for entry in self.previews["entries"]],
    )
    roles = {role["id"]: role for role in self.portrait_set["roles"]}
    role_projection = [
      {
        key: role[key]
        for key in (
          "id",
          "label",
          "family",
          "alt_text_guidance",
          "fallback",
          "target_in_first_slice",
          "target_in_current_slice",
        )
      }
      for role in self.portrait_set["roles"]
    ]
    packet_projection = [
      {
        "id": record["role_id"],
        "label": record["label"],
        "family": record["family"],
        "alt_text_guidance": record["alt_text_guidance"],
        "fallback": record["fallback"],
        "target_in_first_slice": record["target_in_first_slice"],
        "target_in_current_slice": record["target_in_current_slice"],
      }
      for record in self.packet["preview_records"]
    ]
    self.assertEqual(packet_projection, role_projection)
    for record, preview in zip(self.packet["preview_records"], self.previews["entries"]):
      self.assertEqual(record["asset_id"], preview["asset_id"])
      self.assertEqual(record["role_id"], preview["role_id"])
      self.assertEqual(record["family"], roles[preview["role_id"]]["family"])
      role = roles[preview["role_id"]]
      for key in ("label", "alt_text_guidance", "fallback", "target_in_first_slice", "target_in_current_slice"):
        self.assertEqual(record[key], role[key], (preview["asset_id"], key))
      self.assertEqual(preview["accessible_equivalent"], record["accessible_equivalent"])
      self.assertEqual(preview["generic_fallback"], record["generic_fallback"])
      self.assertEqual(record["source_output_path"], preview["source_output_path"])
      self.assertEqual(record["source_hash"], preview["source_hash"])
      self.assertEqual(record["dimensions"], preview["dimensions"])
      self.assertEqual(record["accessible_equivalent"], preview["accessible_equivalent"])
      self.assertEqual(record["generic_fallback"], preview["generic_fallback"])
      source = ROOT / preview["source_output_path"]
      self.assertTrue(source.is_file(), preview["asset_id"])
      self.assertEqual(
        preview["source_hash"],
        f"sha256:{hashlib.sha256(source.read_bytes()).hexdigest()}",
      )
      self.assertEqual(png_dimensions(source), (1254, 1254))
      self.assertEqual(preview["dimensions"], {"width": 1254, "height": 1254})

  def test_preview_and_queue_gates_remain_pending_and_missing_metadata_is_not_guessed(self):
    self.assertEqual(
      self.packet["technical_contract"]["workflow_required_metadata_fields"],
      self.workflow["required_metadata_fields"],
    )
    self.assertEqual(
      self.packet["technical_contract"]["approved_model_scope"],
      [
        {
          "id": model["id"],
          "model_revision": model["model_revision"],
          "model_license": model["model_license"],
          "approval_status": model["approval_status"],
        }
        for model in self.approved_models["entries"]
      ],
    )
    self.assertEqual(
      self.packet["technical_contract"]["required_queue_gates"],
      EXPECTED_GATES,
    )
    self.assertEqual(self.queue["required_gates"], EXPECTED_GATES)
    self.assertEqual(self.queue["review_status"], "pending-human-review")
    self.assertEqual(len(self.queue["entries"]), len(self.previews["entries"]))
    self.assertEqual(
      [entry["asset_id"] for entry in self.queue["entries"]],
      [entry["asset_id"] for entry in self.previews["entries"]],
    )
    self.assertEqual(
      {record["asset_id"] for record in self.packet["preview_records"]},
      {entry["asset_id"] for entry in self.queue["entries"]},
    )
    for preview, queue_entry in zip(self.previews["entries"], self.queue["entries"]):
      self.assertEqual(preview["asset_id"], queue_entry["asset_id"])
      self.assertEqual(preview["role_id"], queue_entry["role_id"])
      self.assertEqual(preview["source_output_path"], queue_entry["source_output_path"])
      self.assertEqual(preview["source_hash"], queue_entry["source_hash"])
      self.assertEqual(preview["accessible_equivalent"], queue_entry["accessible_equivalent"])
      self.assertEqual(preview["generic_fallback"], queue_entry["generic_fallback"])
      self.assertEqual(preview["preview_status"], "unverified-preview")
      self.assertEqual(preview["approval_status"], "pending")
      for field in self.packet["technical_contract"]["required_missing_fields"]:
        self.assertIsNone(preview.get(field), (preview["asset_id"], field))
      self.assertEqual(preview["model_identity_status"], "not-exposed-by-preview-tool")
      self.assertEqual(preview["seed_status"], "not-exposed-by-preview-tool")
      self.assertEqual(preview["sampler_status"], "not-exposed-by-preview-tool")
      self.assertEqual(queue_entry["decision"], "pending")
      self.assertEqual(queue_entry["approval_status"], "pending")
      self.assertEqual(
        queue_entry["reviewer"],
        {"name": None, "type": "human-review-required", "reviewed_at": None, "notes": None},
      )
      self.assertEqual(set(queue_entry["gates"]), set(EXPECTED_GATES))
      self.assertFalse(any(queue_entry["gates"].values()))
      self.assertIsNone(queue_entry["release_path"])
      self.assertIsNone(queue_entry["release_hash"])
      self.assertIsNone(queue_entry["asset_registry_id"])

  def test_generation_registry_runtime_and_release_surfaces_exclude_previews(self):
    self.assertEqual(self.generation_manifest["entries"], [])
    visual_ids = {entry["id"] for entry in self.visual_registry["entries"]}
    audio_ids = {entry["id"] for entry in self.audio_registry["entries"]}
    preview_ids = {entry["asset_id"] for entry in self.previews["entries"]}
    self.assertTrue(preview_ids.isdisjoint(visual_ids))
    self.assertTrue(preview_ids.isdisjoint(audio_ids))
    self.assertEqual(self.packet["release_boundary"]["generation_manifest_entries"], 0)
    self.assertEqual(self.packet["release_boundary"]["visual_registry_preview_entries"], 0)
    self.assertEqual(self.packet["release_boundary"]["release_manifest_preview_entries"], 0)
    self.assertEqual(self.packet["release_boundary"]["runtime_credits_preview_entries"], 0)
    for preview_id in preview_ids:
      self.assertNotIn(preview_id, self.runtime_credits)
    self.assertEqual(self.release_manifest["schema_version"], "asset-release-manifest-v1")
    manifest_paths = {record["path"] for record in self.release_manifest["files"]}
    for preview in self.previews["entries"]:
      self.assertNotIn(preview["source_output_path"], manifest_paths)
      preview_stem = Path(preview["source_output_path"]).stem
      for surface in (
        self.asset_credits,
        self.third_party_notices,
        self.runtime_credits,
        RELEASE_MANIFEST.read_text(encoding="utf-8"),
      ):
        self.assertNotIn(preview["asset_id"], surface)
        self.assertNotIn(preview_stem, surface)
      self.assertTrue(all(preview_stem not in path for path in manifest_paths))
      self.assertIsNone(preview["release_path"])
      self.assertIsNone(preview["release_hash"])
      self.assertIsNone(preview["asset_registry_id"])

  def test_tasks_questions_limits_and_roadmap_gate_are_complete(self):
    self.assertEqual(
      [task["id"] for task in self.packet["human_review_tasks"]],
      [
        "identity-and-role",
        "resemblance-and-marks",
        "artifact-and-accessibility",
        "generation-provenance",
        "release-and-registry",
      ],
    )
    self.assertEqual(len(self.packet["review_questions"]), 7)
    self.assertTrue(all(question.endswith("?") for question in self.packet["review_questions"]))
    boundary = self.packet["authority_privacy_provenance_boundary"]
    self.assertIn("Null or not-exposed-by-preview-tool metadata remain null", boundary["no_guessing_rule"])
    for forbidden in (
      "actual model identity, immutable revision, sampler, or seed",
      "training-data provenance or ownership",
      "real-person or protected-mark clearance",
      "portrait quality or universal accessibility",
      "educational usefulness",
      "legal clearance",
      "release eligibility or public-release approval",
    ):
      self.assertIn(forbidden, boundary["forbidden_claims"])
    normalized = " ".join(self.roadmap.split())
    self.assertIn("[ ] AI-generation metadata complete.", normalized)
    self.assertIn("phase13.1-ai-preview-provenance-review-packet.json", normalized)
    self.assertIn("technical AI-preview provenance/human-review packet prepared", normalized)

  def test_authoritative_generation_attribution_and_portrait_tests_pass(self):
    commands = [
      [
        sys.executable,
        "-m",
        "unittest",
        "tests/test_phase13_1_ai_generation_metadata_boundary.py",
        "tests/test_phase13_1_attribution_boundary.py",
        "tests/test_portrait_workflow.py",
      ],
      [sys.executable, "scripts/validate_generation_metadata.py"],
      [sys.executable, "scripts/validate_assets.py"],
      [sys.executable, "scripts/validate_asset_security.py"],
      [sys.executable, "scripts/verify_asset_release.py", "--check"],
    ]
    for command in commands:
      result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, f"{command}\n{result.stdout}\n{result.stderr}")


if __name__ == "__main__":
  unittest.main()
