import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.2-educational-usability-evidence-intake-packet.json"
PROTOCOL_PATH = ROOT / "docs" / "evaluation" / "phase10.2-evaluation-protocol.json"
FEEDBACK_PATH = ROOT / "docs" / "evaluation" / "phase13.2-pilot-feedback-instrument.json"
PILOT_PATH = ROOT / "docs" / "evaluation" / "phase13.2-pilot-evidence-intake-packet.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_educational_usability_evidence_intake.py"


def load_json(path):
  return json.loads(path.read_text(encoding="utf-8"))


class Phase132EducationalUsabilityEvidenceIntakeTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    sys.path.insert(0, str(ROOT / "scripts"))
    cls.packet = load_json(PACKET_PATH)
    cls.protocol = load_json(PROTOCOL_PATH)
    cls.feedback = load_json(FEEDBACK_PATH)
    cls.pilot = load_json(PILOT_PATH)
    spec = importlib.util.spec_from_file_location(
      "validate_educational_usability_evidence_intake",
      VALIDATOR_PATH,
    )
    cls.validator = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(cls.validator)

  def test_packet_is_empty_pending_and_source_bound(self):
    self.assertEqual(
      self.packet["schema_version"],
      "phase13.2-educational-usability-evidence-intake-v1",
    )
    self.assertEqual(
      self.packet["status"],
      "complete-technical-intake-pending-human-review",
    )
    self.assertEqual(self.packet["records"], [])
    self.assertEqual(self.packet["intake_boundary"]["record_count"], 0)
    self.assertFalse(self.packet["review_boundary"]["educational_usability_review_complete"])
    self.assertEqual(self.packet["decision"]["status"], "pending-authorized-human-review")
    self.assertIsNone(self.packet["decision"]["go_no_go"])
    for source in self.packet["source_contract"].values():
      source_path, marker = source.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source)

  def test_review_contract_reuses_protocol_and_feedback_vocabularies(self):
    contract = self.packet["review_contract"]
    self.assertEqual(
      contract["task_ids"],
      [task["id"] for task in self.protocol["tasks"]],
    )
    self.assertEqual(contract["reviewer_categories"], self.protocol["participant_groups"])
    self.assertEqual(contract["rating_dimensions"], self.protocol["rating_dimensions"])
    self.assertEqual(
      contract["accommodation_categories"],
      self.pilot["allowed_record_contract"]["accommodation_categories"],
    )
    self.assertEqual(contract["finding_categories"], self.feedback["finding_categories"])
    self.assertEqual(contract["forbidden_fields"], self.feedback["session_record"]["forbidden"])
    self.assertEqual(
      contract["record_fields"],
      [
        "review_id",
        "task_id",
        "reviewer_category",
        "review_status",
        "ratings",
        "accommodations",
        "finding_categories",
      ],
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
    task_id = contract["task_ids"][0]
    reviewer_category = "first-time-user"
    return {
      "review_id": f"educational-{task_id}-{reviewer_category}",
      "task_id": task_id,
      "reviewer_category": reviewer_category,
      "review_status": "reviewed",
      "ratings": {
        dimension: 4
        for dimension in contract["rating_dimensions"]
      },
      "accommodations": ["large-text", "written-equivalent"],
      "finding_categories": ["preference"],
    }

  def test_validator_accepts_bounded_record_shape(self):
    self.validator.validate_record(self._valid_record(), self.packet["review_contract"])

  def test_validator_rejects_identity_media_private_state_free_text_and_id_drift(self):
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

    record = self._valid_record()
    record["review_id"] = "free-form-review-id"
    with self.assertRaises(ValueError):
      self.validator.validate_record(record, contract)

  def test_validator_rejects_unknown_values_duplicate_lists_and_numeric_coercion(self):
    contract = self.packet["review_contract"]
    record = self._valid_record()
    record["ratings"]["institutional-recognition"] = 1.0
    with self.assertRaises(ValueError):
      self.validator.validate_record(record, contract)

    record = self._valid_record()
    record["ratings"]["unknown-dimension"] = 3
    with self.assertRaises(ValueError):
      self.validator.validate_record(record, contract)

    record = self._valid_record()
    record["accommodations"] = ["large-text", "large-text"]
    with self.assertRaises(ValueError):
      self.validator.validate_record(record, contract)

    record = self._valid_record()
    record["finding_categories"] = ["unbounded-finding"]
    with self.assertRaises(ValueError):
      self.validator.validate_record(record, contract)

  def test_packet_rejects_unknown_envelope_and_premature_decision(self):
    for section, field in (
      ("packet", "participant_results"),
      ("intake_boundary", "raw_transcript"),
      ("review_boundary", "learning_complete"),
      ("decision", "notes"),
    ):
      packet = copy.deepcopy(self.packet)
      target = packet if section == "packet" else packet[section]
      target[field] = True
      with self.subTest(section=section, field=field):
        with self.assertRaisesRegex(ValueError, "fields are not exactly bounded"):
          self.validator.validate_packet(packet)

    packet = copy.deepcopy(self.packet)
    packet["decision"]["status"] = "recorded"
    with self.assertRaisesRegex(ValueError, "decision status must remain pending"):
      self.validator.validate_packet(packet)

    packet = copy.deepcopy(self.packet)
    packet["records"] = [{"review_id": "not-empty"}]
    with self.assertRaisesRegex(ValueError, "zero records|no human records"):
      self.validator.validate_packet(packet)

  def test_packet_rejects_source_and_nested_pending_boundary_drift(self):
    packet = copy.deepcopy(self.packet)
    packet["source_contract"]["evaluation_protocol"] = "README.md: status"
    with self.assertRaisesRegex(ValueError, "source contract is not canonical"):
      self.validator.validate_packet(packet)

    packet = copy.deepcopy(self.packet)
    packet["review_contract"]["task_ids"].append("unrelated-task")
    with self.assertRaisesRegex(ValueError, "review contract is not source-bound"):
      self.validator.validate_packet(packet)

    original_load = self.validator._load_json
    first_session_path = (ROOT / "docs/evaluation/phase13.1-first-session-review-packet.json").resolve()

    def load_with_mutation(path):
      source = original_load(path)
      if path.resolve() == first_session_path:
        source["review_boundary"]["educational_usability_review_complete"] = True
      return source

    with patch.object(self.validator, "_load_json", side_effect=load_with_mutation):
      with self.assertRaisesRegex(ValueError, "first-session source boundary is not canonical"):
        self.validator.validate_packet(self.packet)

    def load_with_human_decision(path):
      source = original_load(path)
      if path.resolve() == first_session_path:
        source["human_review_record"]["decision"] = "approved"
      return source

    with patch.object(self.validator, "_load_json", side_effect=load_with_human_decision):
      with self.assertRaisesRegex(ValueError, "first-session human review record is not pending"):
        self.validator.validate_packet(self.packet)

    def load_with_numeric_boundary(path):
      source = original_load(path)
      if path.resolve() == first_session_path:
        source["review_boundary"]["technical_packet_complete"] = 1
      return source

    with patch.object(self.validator, "_load_json", side_effect=load_with_numeric_boundary):
      with self.assertRaisesRegex(ValueError, "first-session source boundary is not canonical"):
        self.validator.validate_packet(self.packet)

    def load_with_numeric_human_flag(path):
      source = original_load(path)
      if path.resolve() == first_session_path:
        source["human_review_record"]["participant_results_present"] = 0
      return source

    with patch.object(self.validator, "_load_json", side_effect=load_with_numeric_human_flag):
      with self.assertRaisesRegex(ValueError, "first-session human review record is not pending"):
        self.validator.validate_packet(self.packet)

  def test_packet_rejects_boolean_record_count(self):
    packet = copy.deepcopy(self.packet)
    packet["intake_boundary"]["record_count"] = False
    with self.assertRaisesRegex(ValueError, "zero records"):
      self.validator.validate_packet(packet)


if __name__ == "__main__":
  unittest.main()
