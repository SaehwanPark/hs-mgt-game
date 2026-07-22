import hashlib
import json
import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_generation_metadata import validate_portrait_documents


PORTRAIT_SET = ROOT / "assets" / "generation" / "portrait-set.json"
PREVIEWS = ROOT / "assets" / "generation" / "portrait-previews.json"
MANIFEST = ROOT / "assets" / "generation" / "generation-manifest.json"
PROOF = ROOT / "gui" / "portrait-workflow-proof.html"


class PortraitWorkflowTests(unittest.TestCase):
  def test_role_set_and_shared_style_are_complete(self):
    document = json.loads(PORTRAIT_SET.read_text(encoding="utf-8"))
    previews = json.loads(PREVIEWS.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    self.assertEqual(validate_portrait_documents(document, previews, manifest, set()), [])
    self.assertEqual(document["schema_version"], "fictional-portrait-set-v1")
    self.assertEqual({role["id"] for role in document["roles"]}, {
      "rival-system-executive",
      "payer-negotiator",
      "regulator",
      "labor-representative",
      "community-leader",
      "board-chair",
      "affiliation-partner-executive",
    })
    self.assertEqual(len(document["roles"]), 7)
    self.assertEqual(sum(role["target_in_first_slice"] for role in document["roles"]), 1)
    self.assertEqual(
      {role["id"] for role in document["roles"] if role["target_in_current_slice"]},
      {
        "payer-negotiator",
        "regulator",
        "labor-representative",
        "community-leader",
        "board-chair",
        "affiliation-partner-executive",
      },
    )
    self.assertEqual(document["roles"][0]["id"], "rival-system-executive")
    self.assertIn("small_size_target", document["shared_style"])
    self.assertIn("grayscale_target", document["shared_style"])
    self.assertIn("public-figure or identifiable-real-person resemblance", document["prohibited_content"])

    malformed = copy.deepcopy(document)
    malformed["roles"][1]["id"] = malformed["roles"][0]["id"]
    errors = validate_portrait_documents(malformed, previews, manifest, set())
    self.assertTrue(any("exact seven unique" in error for error in errors))

    malformed_current_slice = copy.deepcopy(document)
    malformed_current_slice["roles"][0]["target_in_current_slice"] = True
    malformed_current_slice["roles"][1]["target_in_current_slice"] = False
    errors = validate_portrait_documents(malformed_current_slice, previews, manifest, set())
    self.assertTrue(any("current slice" in error for error in errors))

    malformed_provenance = copy.deepcopy(previews)
    del malformed_provenance["entries"][0]["settings"]
    del malformed_provenance["entries"][0]["source_image_references"]
    malformed_provenance["entries"][0]["generation_date"] = "not-a-date"
    errors = validate_portrait_documents(document, malformed_provenance, manifest, set())
    self.assertTrue(any("settings" in error for error in errors))
    self.assertTrue(any("source_image_references" in error for error in errors))
    self.assertTrue(any("generation_date" in error for error in errors))

    malformed_style = copy.deepcopy(document)
    malformed_style["shared_style"]["palette"] = []
    errors = validate_portrait_documents(malformed_style, previews, manifest, set())
    self.assertTrue(any("palette" in error for error in errors))

  def test_preview_is_hash_bound_and_release_blocked(self):
    document = json.loads(PREVIEWS.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    self.assertEqual({entry["role_id"] for entry in document["entries"]}, {
      "rival-system-executive",
      "payer-negotiator",
      "regulator",
      "labor-representative",
      "community-leader",
      "board-chair",
      "affiliation-partner-executive",
    })
    for entry in document["entries"]:
      source = ROOT / entry["source_output_path"]
      digest = hashlib.sha256(source.read_bytes()).hexdigest()
      self.assertEqual(entry["source_hash"], f"sha256:{digest}")
      self.assertEqual(entry["preview_status"], "unverified-preview")
      self.assertIsNone(entry["model_id"])
      self.assertIsNone(entry["model_revision"])
      self.assertIsNone(entry["seed"])
      self.assertEqual(entry["approval_status"], "pending")
      self.assertIsNone(entry["asset_registry_id"])
    self.assertFalse(document["release_eligible"])
    self.assertEqual(manifest["entries"], [])

  def test_proof_exposes_identity_and_fallback_boundaries(self):
    content = PROOF.read_text(encoding="utf-8")
    role_document = json.loads(PORTRAIT_SET.read_text(encoding="utf-8"))
    for role in role_document["roles"]:
      self.assertIn(role["label"], content)
      self.assertIn(role["family"], content)
      self.assertIn(role["fallback"], content)
    for entry in json.loads(PREVIEWS.read_text(encoding="utf-8"))["entries"]:
      self.assertIn(entry["source_output_path"].split("/")[-1], content)
      self.assertIn(entry["accessible_equivalent"], content)
    for marker in (
      "Fixture-only Phase 8.2 proof",
      "rival-system-executive-preview.png",
      "payer-negotiator-preview.png",
      "regulator-preview.png",
      "labor-representative-preview.png",
      "community-leader-preview.png",
      "board-chair-preview.png",
      "affiliation-partner-executive-preview.png",
      "unverified preview",
      "generic fallback",
      "small-size",
      "grayscale",
      "Identity consistency",
      "Release blocked",
      "approved local model revision",
    ):
      self.assertIn(marker, content)
    self.assertNotIn("fetch(", content)
    self.assertNotIn("WebSocket", content)

  def test_portrait_review_fields_are_present_and_pending(self):
    previews = json.loads(PREVIEWS.read_text(encoding="utf-8"))
    for entry in previews["entries"]:
      self.assertEqual(set(entry["portrait_review"]), {
        "identity_only_reviewed",
        "role_consistency_reviewed",
        "generic_fallback_reviewed",
        "small_size_reviewed",
        "grayscale_reviewed",
      })
      self.assertFalse(any(entry["portrait_review"].values()))
      self.assertIn("captured_at", entry)
      self.assertIn("contributor", entry)
      self.assertIn("provenance_note", entry)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    portrait_set = json.loads(PORTRAIT_SET.read_text(encoding="utf-8"))
    previews["entries"][1]["asset_registry_id"] = "visual.runtime-identities"
    errors = validate_portrait_documents(portrait_set, previews, manifest, {"visual.runtime-identities"})
    self.assertTrue(any("release_path or asset_registry_id" in error for error in errors))

    swapped = json.loads(PREVIEWS.read_text(encoding="utf-8"))
    swapped["entries"][1]["source_output_path"] = swapped["entries"][0]["source_output_path"]
    errors = validate_portrait_documents(portrait_set, swapped, manifest, set())
    self.assertTrue(any("must match role_id" in error for error in errors))
    self.assertTrue(any("must be unique" in error for error in errors))

    absolute = json.loads(PREVIEWS.read_text(encoding="utf-8"))
    absolute["entries"][0]["source_output_path"] = str(ROOT / absolute["entries"][0]["source_output_path"])
    errors = validate_portrait_documents(portrait_set, absolute, manifest, set())
    self.assertTrue(any("repository-relative" in error for error in errors))


if __name__ == "__main__":
  unittest.main()
