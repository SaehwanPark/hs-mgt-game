import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase13.2-pilot-preparation-boundary.json"
GUIDE = ROOT / "docs" / "guides" / "phase10.2-structured-evaluation.md"
FEEDBACK = ROOT / "docs" / "evaluation" / "phase13.2-pilot-feedback-instrument.json"


class Phase132PilotPreparationTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.guide = GUIDE.read_text(encoding="utf-8")
    cls.feedback = json.loads(FEEDBACK.read_text(encoding="utf-8"))

  def test_source_contract_markers_exist(self):
    self.assertEqual(
      self.ledger["schema_version"],
      "phase13.2-pilot-preparation-boundary-v1",
    )
    self.assertEqual(self.ledger["status"], "complete-preparation-only")
    for source_ref in self.ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)

  def test_guide_contains_actual_pilot_boundaries(self):
    for marker in (
      "### Facilitator preflight",
      "### Classroom hardware assumptions",
      "### Audio and accessibility guidance",
      "### Screenshot, recording, and feedback handling",
      "explicit consent",
      "low-distraction recipe",
      "Reduced motion",
      "Large",
      "cues-only",
      "1024×768",
      "same computer",
      "does not establish measured",
    ):
      self.assertIn(marker, self.guide)

  def test_feedback_instrument_is_structured_and_pending(self):
    self.assertEqual(self.feedback["schema_version"], "phase13.2-pilot-feedback-instrument-v1")
    self.assertEqual(self.feedback["status"], "ready-for-authorized-human-pilot")
    self.assertGreaterEqual(len(self.feedback["tasks"]), 4)
    self.assertIn("not-observed", self.feedback["rating_scale"])
    self.assertEqual(self.feedback["decision"]["status"], "pending-human-evidence")
    self.assertIsNone(self.feedback["decision"]["go_no_go"])
    consent = self.feedback["consent_record"]
    for field in ("feedback", "screenshot", "recording"):
      self.assertIn("granted", consent[field])
      self.assertIn("declined", consent[field])
    self.assertIn("Record consent status only", consent["storage_rule"])
    forbidden = " ".join(self.feedback["session_record"]["forbidden"])
    for marker in ("names", "health information", "private game state", "browser URLs"):
      self.assertIn(marker, forbidden)

  def test_preparation_limits_keep_human_gates_open(self):
    limits = " ".join(self.ledger["limits"] + self.feedback["evidence_limits"])
    for marker in (
      "participant results",
      "go/no-go",
      "human accessibility",
      "educational effectiveness",
      "audio usefulness",
      "low-distraction mode",
    ):
      self.assertIn(marker, limits)


if __name__ == "__main__":
  unittest.main()
