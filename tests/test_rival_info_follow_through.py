import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "_workspace" / "experiments" / "v0.10.43-rival-info-follow-through"
RUNNER_PATH = EXPERIMENT / "run_sessions.py"
RUNNER_SPEC = importlib.util.spec_from_file_location(
  "rival_info_follow_through_runner",
  RUNNER_PATH,
)
RUNNER = importlib.util.module_from_spec(RUNNER_SPEC)
RUNNER_SPEC.loader.exec_module(RUNNER)

classify_monitor_signal = RUNNER.classify_monitor_signal
extract_monitor_signals = RUNNER.extract_monitor_signals
response_command_for_signal = RUNNER.response_command_for_signal


class RivalInformationFollowThroughTests(unittest.TestCase):
  def test_extract_monitor_signal_preserves_source_month_and_visible_text(self):
    signals = extract_monitor_signals(
      [
        "Market: Rival Summit Care (monitor intel, month 3): "
        "Summit Care: private payer talks with CarrierA (Aggressive)"
      ],
      observation_turn=4,
    )

    self.assertEqual(
      signals,
      [
        {
          "observation_turn": 4,
          "source_month": 3,
          "signal_kind": "payer",
          "signal_text": (
            "Market: Rival Summit Care (monitor intel, month 3): "
            "Summit Care: private payer talks with CarrierA (Aggressive)"
          ),
        }
      ],
    )

  def test_signal_classification_uses_visible_content(self):
    self.assertEqual(
      classify_monitor_signal(
        "Rival Northlake: investing 25 in Beds"
      ),
      "capacity",
    )
    self.assertEqual(
      classify_monitor_signal(
        "Rival Valley: public Access pledge level 2"
      ),
      "access",
    )
    self.assertEqual(
      classify_monitor_signal("Rival action: unfamiliar private event"),
      "other",
    )

  def test_response_command_matches_visible_payer_signal(self):
    command, reason = response_command_for_signal(
      {
        "signal_kind": "payer",
        "signal_text": "Rival Summit: private payer talks with CarrierA",
      },
      ["Available resources: AP 3, cash 60, political capital 8"],
      ["In-flight projects: none"],
    )

    self.assertEqual(
      command,
      "negotiate payer=carrier_a rate_posture=neutral; hold",
    )
    self.assertIsNone(reason)

  def test_response_falls_back_to_hold_when_visible_resources_are_insufficient(self):
    command, reason = response_command_for_signal(
      {
        "signal_kind": "payer",
        "signal_text": "Rival Summit: private payer talks with CarrierA",
      },
      ["Available resources: AP 3, cash 60, political capital 1"],
      ["In-flight projects: none"],
    )

    self.assertEqual(command, "hold")
    self.assertIn("political capital", reason.lower())


if __name__ == "__main__":
  unittest.main()
