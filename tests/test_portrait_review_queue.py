import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_generation_metadata import validate_portrait_review_queue


PORTRAIT_SET = ROOT / "assets" / "generation" / "portrait-set.json"
PREVIEWS = ROOT / "assets" / "generation" / "portrait-previews.json"
QUEUE = ROOT / "assets" / "generation" / "portrait-review-queue.json"
PROOF = ROOT / "gui" / "portrait-review-proof.html"
MANIFEST = ROOT / "assets" / "generation" / "generation-manifest.json"

ROLE_IDS = {
  "rival-system-executive",
  "payer-negotiator",
  "regulator",
  "labor-representative",
  "community-leader",
  "board-chair",
  "affiliation-partner-executive",
}


class PortraitReviewQueueTests(unittest.TestCase):
  def documents(self):
    portrait_set = json.loads(PORTRAIT_SET.read_text(encoding="utf-8"))
    previews = json.loads(PREVIEWS.read_text(encoding="utf-8"))
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return portrait_set, previews, queue, manifest

  def test_queue_is_complete_and_pending(self):
    portrait_set, previews, queue, manifest = self.documents()
    self.assertEqual(validate_portrait_review_queue(portrait_set, previews, queue, set()), [])
    self.assertEqual({entry["role_id"] for entry in queue["entries"]}, ROLE_IDS)
    self.assertFalse(queue["release_eligible"])
    self.assertEqual(queue["review_status"], "pending-human-review")
    self.assertEqual(manifest["entries"], [])
    for entry in queue["entries"]:
      self.assertEqual(entry["decision"], "pending")
      self.assertEqual(entry["approval_status"], "pending")
      self.assertTrue(all(value is False for value in entry["gates"].values()))
      self.assertIsNone(entry["reviewer"]["name"])
      self.assertIsNone(entry["reviewer"]["reviewed_at"])
      self.assertIsNone(entry["reviewer"]["notes"])
      self.assertIsNone(entry["release_path"])
      self.assertIsNone(entry["release_hash"])
      self.assertIsNone(entry["asset_registry_id"])

  def test_queue_binds_to_preview_identity_and_hash(self):
    portrait_set, previews, queue, manifest = self.documents()
    malformed = copy.deepcopy(queue)
    malformed["entries"][1]["source_hash"] = malformed["entries"][0]["source_hash"]
    errors = validate_portrait_review_queue(portrait_set, previews, malformed, set())
    self.assertTrue(any("source_hash" in error for error in errors))

    malformed = copy.deepcopy(queue)
    malformed["entries"][2]["accessible_equivalent"] = "Wrong accessible equivalent."
    errors = validate_portrait_review_queue(portrait_set, previews, malformed, set())
    self.assertTrue(any("accessible_equivalent" in error for error in errors))

    malformed = copy.deepcopy(queue)
    malformed["entries"][3]["source_output_path"] = malformed["entries"][0]["source_output_path"]
    errors = validate_portrait_review_queue(portrait_set, previews, malformed, set())
    self.assertTrue(any("must match role_id" in error for error in errors))
    self.assertTrue(any("must be unique" in error for error in errors))

    malformed = copy.deepcopy(queue)
    del malformed["entries"][0]["release_path"]
    errors = validate_portrait_review_queue(portrait_set, previews, malformed, set())
    self.assertTrue(any("missing release_path" in error for error in errors))

    malformed_previews = copy.deepcopy(previews)
    malformed_previews["entries"] = None
    errors = validate_portrait_review_queue(portrait_set, malformed_previews, queue, set())
    self.assertTrue(any("previews.entries must be a list" in error for error in errors))

  def test_queue_rejects_unreviewed_promotion(self):
    portrait_set, previews, queue, manifest = self.documents()
    malformed = copy.deepcopy(queue)
    malformed["entries"][0]["approval_status"] = "approved"
    malformed["entries"][0]["decision"] = "approved"
    malformed["entries"][0]["asset_registry_id"] = "visual.runtime-identities"
    errors = validate_portrait_review_queue(portrait_set, previews, malformed, {"visual.runtime-identities"})
    self.assertTrue(any("must remain pending" in error for error in errors))
    self.assertTrue(any("must remain null" in error for error in errors))

    malformed = copy.deepcopy(queue)
    malformed["entries"][0]["gates"]["identity_only"] = True
    errors = validate_portrait_review_queue(portrait_set, previews, malformed, set())
    self.assertTrue(any("named human reviewer" in error for error in errors))

    promoted_previews = copy.deepcopy(previews)
    promoted_previews["entries"][0]["preview_status"] = "approved"
    errors = validate_portrait_review_queue(portrait_set, promoted_previews, queue, set())
    self.assertTrue(any("must remain unverified and pending" in error for error in errors))

  def test_review_proof_exposes_all_roles_and_boundaries(self):
    content = PROOF.read_text(encoding="utf-8")
    portrait_set, previews, queue, manifest = self.documents()
    previews_by_role = {entry["role_id"]: entry for entry in previews["entries"]}
    for role in portrait_set["roles"]:
      self.assertIn(role["label"], content)
      self.assertIn(role["fallback"], content)
      preview = previews_by_role[role["id"]]
      expected_packet = json.dumps([
        role["id"],
        role["label"],
        preview["accessible_equivalent"],
        role["fallback"],
        Path(preview["source_output_path"]).name,
        preview["source_hash"],
      ])
      self.assertIn(expected_packet, content)
    for entry in previews["entries"]:
      self.assertIn(entry["source_output_path"].split("/")[-1], content)
      self.assertIn(entry["accessible_equivalent"], content)
    for gate in queue["required_gates"]:
      self.assertIn(gate.replace("_", " ").split()[0].capitalize(), content)
    for marker in ("Review-only Phase 8.2 proof", "Pending human review", "Release blocked", "generic actor marker"):
      self.assertIn(marker, content)
    self.assertNotIn("fetch(", content)
    self.assertNotIn("WebSocket", content)


if __name__ == "__main__":
  unittest.main()
