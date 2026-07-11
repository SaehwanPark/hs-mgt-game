import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "_workspace" / "experiments" / "v0.10.41-consultant-advice-usage"
sys.path.append(str(EXPERIMENT))

from run_sessions import (  # noqa: E402
  build_option_command,
  parse_rendered_options,
  select_option,
  visible_command_budget,
)


class ConsultantAdviceUsageTests(unittest.TestCase):
  def test_parse_rendered_options_preserves_labels_titles_and_tradeoffs(self):
    observation = [
      "STRATEGY CONSULTANT NOTES — Advisory, not binding",
      "Option A — Defensive capacity: invest in staffed beds",
      "  Tradeoff: consumes cash before delayed capacity arrives",
      "Option B — Workforce resilience: recruit nurses",
      "  Tradeoff: spends cash before staffing relief arrives",
      "Option C — Information-first: monitor an identified rival gap",
      "  Tradeoff: costs AP and delays direct action",
      "Option D — Public access pledge: commit to an access target",
      "  Tradeoff: creates a visible follow-through obligation",
    ]

    self.assertEqual(
      parse_rendered_options(observation),
      [
        {
          "label": "A",
          "title": "Defensive capacity: invest in staffed beds",
          "tradeoff_bullets": ["consumes cash before delayed capacity arrives"],
        },
        {
          "label": "B",
          "title": "Workforce resilience: recruit nurses",
          "tradeoff_bullets": ["spends cash before staffing relief arrives"],
        },
        {
          "label": "C",
          "title": "Information-first: monitor an identified rival gap",
          "tradeoff_bullets": ["costs AP and delays direct action"],
        },
        {
          "label": "D",
          "title": "Public access pledge: commit to an access target",
          "tradeoff_bullets": ["creates a visible follow-through obligation"],
        },
      ],
    )

  def test_select_option_uses_visible_profile_priority(self):
    observation = [
      "Reported access index: 66",
      "Workforce trust: strained; vacancy rate elevated in nursing",
      "Policy: access scrutiny is increasing",
      "Intel gap: rival actions remain partially observed",
    ]
    options = [
      {"label": label, "title": label, "tradeoff_bullets": []}
      for label in "ABCD"
    ]

    decision = select_option(observation, options, "Fiscal Caution")

    self.assertEqual(decision["label"], "C")
    self.assertIn("rival", decision["reason"].lower())

  def test_select_option_can_decline_when_no_visible_cue_exists(self):
    decision = select_option(
      ["Reported access index: 75", "Cash runway: STRAINED"],
      [{"label": label, "title": label, "tradeoff_bullets": []} for label in "ABCD"],
      "Naive First-Time",
    )

    self.assertIsNone(decision["label"])
    self.assertEqual(decision["mode"], "declined")

  def test_build_option_command_applies_visible_resource_guards(self):
    legal = ["Available resources: AP 3, cash 60, political capital 8"]
    observation = ["In-flight projects: none"]

    command, reason = build_option_command("B", legal, observation)
    self.assertEqual(command, "recruit role=nurse headcount=1; hold")
    self.assertIsNone(reason)

    command, reason = build_option_command(
      "D",
      ["Available resources: AP 1, cash 60, political capital 0"],
      observation,
    )
    self.assertIsNone(command)
    self.assertIn("political capital", reason.lower())

  def test_visible_command_budget_turns_unaffordable_inherited_action_into_failure(self):
    affordable, reason = visible_command_budget(
      "recruit role=admin headcount=1; hold",
      ["Available resources: AP 3, cash 0, political capital 8"],
      ["In-flight projects: none"],
    )

    self.assertFalse(affordable)
    self.assertIn("cash", reason.lower())


if __name__ == "__main__":
  unittest.main()
