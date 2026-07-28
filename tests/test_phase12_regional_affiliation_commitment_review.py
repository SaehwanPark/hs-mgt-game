import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-regional-affiliation-commitment-review.json"


class Phase12RegionalAffiliationCommitmentReviewTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_commitment_and_review_sources_match(self):
    ledger = self.ledger
    self.assertEqual(ledger["schema_version"], "regional-affiliation-commitment-review-v1")
    self.assertEqual(ledger["status"], "complete-current-commitment-review-boundary")
    self.assertEqual(ledger["campaign"], "regional-affiliation-v1")
    for source_ref in ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)
    commitment = ledger["commitment_state"]
    self.assertEqual(
      commitment["metric_labels"],
      ["Community commitment", "Workforce commitment", "Continuity commitment"],
    )
    self.assertEqual(commitment["metric_unit"], "commitment units")
    self.assertEqual(
      commitment["reported_partner_statuses"],
      ["Pursuing", "PartnerAccepted", "PartnerConditioned", "PartnerRejected"],
    )
    review = ledger["review_state"]
    self.assertEqual(review["process_id"], "institutional-review")
    self.assertEqual(review["process_status"], "pending")
    self.assertEqual([decision["id"] for decision in review["decisions"]], ["submit-review", "await-review"])
    self.assertEqual(
      review["reported_status_values"],
      ["Approved", "ConditionallyApproved", "ReviewDelayed", "ReviewRejected", "ReviewPending"],
    )

  def test_presentation_and_information_boundaries_remain_bounded(self):
    surface = self.ledger["presentation_surface"]
    self.assertIn("host-supplied", surface["shared_process_renderer"])
    self.assertIn("canonical host command", surface["shared_decision_renderer"])
    self.assertIn("competitive-regional-v1 only", surface["live_gui_boundary"])
    self.assertIn("optional", surface["audio_state"])
    self.assertIn("none-required", surface["new_asset_need"])
    self.assertTrue(self.ledger["open_work"])
    limits = " ".join(self.ledger["limits"])
    for marker in (
      "private review deliberation",
      "hidden threshold",
      "stylized host-resolved observations",
      "Optional audio",
      "No new map",
      "public-release",
    ):
      self.assertIn(marker, limits)
    self.assertEqual(self.ledger["test_source"], "tests/test_phase12_regional_affiliation_commitment_review.py")


if __name__ == "__main__":
  unittest.main()
