import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.2-debrief-visual-evidence-intake-packet.json"
REVIEW_PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.2-debrief-visual-review-packet.json"
FEEDBACK_PATH = ROOT / "docs" / "evaluation" / "phase13.2-pilot-feedback-instrument.json"
PROTOCOL_PATH = ROOT / "docs" / "evaluation" / "phase10.2-evaluation-protocol.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_debrief_visual_evidence_intake.py"


def load_json(path):
  return json.loads(path.read_text(encoding="utf-8"))


class Phase132DebriefVisualEvidenceIntakeTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = load_json(PACKET_PATH)
    cls.review_packet = load_json(REVIEW_PACKET_PATH)
    cls.feedback = load_json(FEEDBACK_PATH)
    cls.protocol = load_json(PROTOCOL_PATH)
    spec = importlib.util.spec_from_file_location("validate_debrief_visual_evidence_intake", VALIDATOR_PATH)
    cls.validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.validator)

  def test_packet_is_empty_pending_and_source_bound(self):
    self.assertEqual(
      self.packet["schema_version"],
      "phase13.2-debrief-visual-evidence-intake-v1",
    )
    self.assertEqual(
      self.packet["status"],
      "complete-technical-intake-pending-human-review",
    )
    self.assertEqual(self.packet["records"], [])
    self.assertEqual(self.packet["review_questions"], self.review_packet["review_questions"])
    self.assertFalse(self.packet["intake_boundary"]["reviewer_identity_collected"])
    self.assertEqual(self.packet["decision"]["status"], "pending-authorized-human-review")
    self.assertIsNone(self.packet["decision"]["go_no_go"])
    for source in self.packet["source_contract"].values():
      source_path, marker = source.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source)

  def test_review_contract_matches_existing_sources(self):
    contract = self.packet["review_contract"]
    self.assertEqual(
      contract["case_ids"],
      [case["id"] for case in self.review_packet["cases"]],
    )
    self.assertEqual(contract["reviewer_categories"], self.protocol["participant_groups"])
    self.assertEqual(contract["finding_categories"], self.feedback["finding_categories"])
    self.assertEqual(
      contract["forbidden_fields"],
      self.feedback["session_record"]["forbidden"],
    )
    self.assertEqual(
      set(contract["record_fields"]),
      {
        "case_id",
        "reviewer_category",
        "review_status",
        "ratings",
        "accommodations",
        "finding_categories",
      },
    )

  def test_validator_accepts_empty_packet_and_cli(self):
    self.validator.validate_packet(self.packet)
    result = subprocess.run(
      [sys.executable, str(VALIDATOR_PATH)],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
    self.assertIn('"status": "pass"', result.stdout)

  def _valid_record(self):
    contract = self.packet["review_contract"]
    return {
      "case_id": "competitive-terminal-debrief",
      "reviewer_category": "accessibility-oriented-reviewer",
      "review_status": "reviewed",
      "ratings": {
        dimension: 4
        for dimension in contract["review_dimensions"]
      },
      "accommodations": ["written-equivalent", "keyboard-navigation"],
      "finding_categories": ["preference"],
    }

  def test_validator_accepts_bounded_record_shape(self):
    self.validator.validate_record(
      self._valid_record(),
      self.packet["review_contract"],
    )

  def test_validator_rejects_identity_media_private_state_and_free_text(self):
    contract = self.packet["review_contract"]
    for field, value in (
      ("name", "Alice"),
      ("session_id", "session-1"),
      ("browser_url", "http://127.0.0.1:7878/"),
      ("private_game_state", {"cash": 1}),
      ("raw_notes", "free text"),
    ):
      record = self._valid_record()
      record[field] = value
      with self.assertRaises(ValueError, msg=field):
        self.validator.validate_record(record, contract)

  def test_validator_rejects_unknown_envelope_source_and_values(self):
    for section, field, value in (
      ("packet", "human_findings", []),
      ("intake_boundary", "participant_result", True),
      ("decision", "human_finding", "complete"),
    ):
      packet = copy.deepcopy(self.packet)
      target = packet if section == "packet" else packet[section]
      target[field] = value
      with self.assertRaises(ValueError, msg=f"{section}.{field}"):
        self.validator.validate_packet(packet)

    packet = copy.deepcopy(self.packet)
    packet["source_contract"]["review_packet"] = "README.md: Health Policy Strategy Game"
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

    packet = copy.deepcopy(self.packet)
    packet["review_contract"]["case_ids"] = ["unrelated-case"]
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

    record = self._valid_record()
    record["ratings"]["history-debrief-distinction"] = 1.0
    with self.assertRaises(ValueError):
      self.validator.validate_record(record, self.packet["review_contract"])

    packet = copy.deepcopy(self.packet)
    packet["intake_boundary"]["record_count"] = False
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)


if __name__ == "__main__":
  unittest.main()
