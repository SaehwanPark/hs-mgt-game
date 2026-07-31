import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "docs" / "evaluation" / "phase13.2-pilot-evidence-intake-packet.json"
FEEDBACK_PATH = ROOT / "docs" / "evaluation" / "phase13.2-pilot-feedback-instrument.json"
PROTOCOL_PATH = ROOT / "docs" / "evaluation" / "phase10.2-evaluation-protocol.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_pilot_evidence_intake.py"


def load_json(path):
  return json.loads(path.read_text(encoding="utf-8"))


class Phase132PilotEvidenceIntakeTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.packet = load_json(PACKET_PATH)
    cls.feedback = load_json(FEEDBACK_PATH)
    cls.protocol = load_json(PROTOCOL_PATH)
    spec = importlib.util.spec_from_file_location("validate_pilot_evidence_intake", VALIDATOR_PATH)
    cls.validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cls.validator)

  def test_packet_is_empty_pending_and_source_bound(self):
    self.assertEqual(self.packet["schema_version"], "phase13.2-pilot-evidence-intake-v1")
    self.assertEqual(self.packet["status"], "complete-technical-intake-pending-human-evidence")
    self.assertEqual(self.packet["records"], [])
    self.assertFalse(self.packet["intake_boundary"]["participant_results_present"])
    self.assertEqual(self.packet["decision"]["status"], "pending-human-evidence")
    self.assertIsNone(self.packet["decision"]["go_no_go"])
    for source in self.packet["source_contract"].values():
      source_path, marker = source.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source)

  def test_record_contract_matches_authorized_pilot_sources(self):
    contract = self.packet["allowed_record_contract"]
    self.assertEqual(
      contract["task_ids"],
      [task["id"] for task in self.feedback["tasks"]],
    )
    self.assertEqual(contract["rating_dimensions"], self.feedback["rating_dimensions"])
    self.assertEqual(contract["finding_categories"], self.feedback["finding_categories"])
    self.assertEqual(
      contract["participant_categories"],
      self.protocol["participant_groups"],
    )
    self.assertEqual(
      set(contract["record_fields"]),
      {
        "participant_category",
        "campaign",
        "seed",
        "difficulty",
        "consent",
        "tasks",
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
    contract = self.packet["allowed_record_contract"]
    return {
      "participant_category": "first-time-user",
      "campaign": "competitive-regional-v1",
      "seed": 42,
      "difficulty": "normal",
      "consent": {
        "feedback": "granted",
        "screenshot": "not-applicable",
        "recording": "not-applicable",
      },
      "tasks": [
        {"id": task_id, "response": "completed"}
        for task_id in contract["task_ids"]
      ],
      "ratings": {
        dimension: 4
        for dimension in contract["rating_dimensions"]
      },
      "accommodations": ["written-equivalent", "keyboard-navigation"],
      "finding_categories": ["preference"],
    }

  def test_validator_accepts_bounded_record_shape(self):
    self.validator.validate_record(
      self._valid_record(),
      self.packet["allowed_record_contract"],
    )

  def test_validator_rejects_identity_media_hidden_state_and_free_text(self):
    contract = self.packet["allowed_record_contract"]
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

  def test_validator_rejects_unbounded_values(self):
    contract = self.packet["allowed_record_contract"]
    record = self._valid_record()
    record["ratings"]["audio-usefulness"] = 6
    with self.assertRaises(ValueError):
      self.validator.validate_record(record, contract)

    record = self._valid_record()
    record["tasks"][0]["response"] = "maybe"
    with self.assertRaises(ValueError):
      self.validator.validate_record(record, contract)

    record = self._valid_record()
    record["tasks"].append(copy.deepcopy(record["tasks"][0]))
    with self.assertRaises(ValueError):
      self.validator.validate_record(record, contract)

  def test_validator_rejects_unknown_envelope_fields(self):
    for section, field, value in (
      ("packet", "participant_results", []),
      ("intake_boundary", "raw_notes_collected", True),
      ("decision", "participant_result", "complete"),
    ):
      packet = copy.deepcopy(self.packet)
      target = packet if section == "packet" else packet[section]
      target[field] = value
      with self.assertRaises(ValueError, msg=f"{section}.{field}"):
        self.validator.validate_packet(packet)

  def test_validator_rejects_source_and_vocabulary_redirects(self):
    packet = copy.deepcopy(self.packet)
    packet["source_contract"]["feedback_instrument"] = "README.md: Health Policy Strategy Game"
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

    packet = copy.deepcopy(self.packet)
    packet["allowed_record_contract"]["campaigns"] = ["example-campaign"]
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)

  def test_validator_rejects_privacy_text_and_boolean_coercion(self):
    for field, value in (
      ("purpose", "participant Alice completed the study"),
      ("evidence_limits", ["participant result: pass"]),
      ("test_source", "docs/participant-results.json"),
    ):
      packet = copy.deepcopy(self.packet)
      packet[field] = value
      with self.assertRaises(ValueError, msg=field):
        self.validator.validate_packet(packet)

    record = self._valid_record()
    record["ratings"]["audio-usefulness"] = True
    with self.assertRaises(ValueError):
      self.validator.validate_record(record, self.packet["allowed_record_contract"])

    record = self._valid_record()
    record["ratings"]["audio-usefulness"] = 1.0
    with self.assertRaises(ValueError):
      self.validator.validate_record(record, self.packet["allowed_record_contract"])

    packet = copy.deepcopy(self.packet)
    packet["intake_boundary"]["record_count"] = False
    with self.assertRaises(ValueError):
      self.validator.validate_packet(packet)


if __name__ == "__main__":
  unittest.main()
