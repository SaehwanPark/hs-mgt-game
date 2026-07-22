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
    self.assertEqual(document["roles"][0]["id"], "rival-system-executive")
    self.assertIn("small_size_target", document["shared_style"])
    self.assertIn("grayscale_target", document["shared_style"])
    self.assertIn("public-figure or identifiable-real-person resemblance", document["prohibited_content"])

    malformed = copy.deepcopy(document)
    malformed["roles"][1]["id"] = malformed["roles"][0]["id"]
    errors = validate_portrait_documents(malformed, previews, manifest, set())
    self.assertTrue(any("exact seven unique" in error for error in errors))

    malformed_style = copy.deepcopy(document)
    malformed_style["shared_style"]["palette"] = []
    errors = validate_portrait_documents(malformed_style, previews, manifest, set())
    self.assertTrue(any("palette" in error for error in errors))

  def test_preview_is_hash_bound_and_release_blocked(self):
    document = json.loads(PREVIEWS.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entry = document["entries"][0]
    source = ROOT / entry["source_output_path"]
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    self.assertEqual(entry["source_hash"], f"sha256:{digest}")
    self.assertFalse(document["release_eligible"])
    self.assertEqual(entry["preview_status"], "unverified-preview")
    self.assertIsNone(entry["model_id"])
    self.assertIsNone(entry["seed"])
    self.assertEqual(entry["approval_status"], "pending")
    self.assertIsNone(entry["asset_registry_id"])
    self.assertEqual(manifest["entries"], [])

  def test_proof_exposes_identity_and_fallback_boundaries(self):
    content = PROOF.read_text(encoding="utf-8")
    role_document = json.loads(PORTRAIT_SET.read_text(encoding="utf-8"))
    for role in role_document["roles"]:
      self.assertIn(role["label"], content)
    for marker in (
      "Fixture-only Phase 8.2 proof",
      "rival-system-executive-preview.png",
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
    entry = json.loads(PREVIEWS.read_text(encoding="utf-8"))["entries"][0]
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

    previews = json.loads(PREVIEWS.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    portrait_set = json.loads(PORTRAIT_SET.read_text(encoding="utf-8"))
    previews["entries"][0]["asset_registry_id"] = "visual.runtime-identities"
    errors = validate_portrait_documents(portrait_set, previews, manifest, {"visual.runtime-identities"})
    self.assertTrue(any("release_path or asset_registry_id" in error for error in errors))


if __name__ == "__main__":
  unittest.main()
