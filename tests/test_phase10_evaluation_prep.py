import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs" / "evaluation" / "phase10.2-evaluation-protocol.json"
GUIDE = ROOT / "docs" / "guides" / "phase10.2-structured-evaluation.md"
LOG = ROOT / "docs" / "evaluation" / "phase10.2-revision-log.md"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"

EXPECTED_TASKS = {
  "first-session-start-to-resolution": "first-session",
  "recognize-three-systems": "recognition",
  "recognize-facility-pressure-source": "recognition",
  "trace-visible-consequence": "consequence-tracing",
  "reconstruct-first-month": "consequence-tracing",
  "keyboard-large-text-reduced-motion": "accessibility",
  "audio-preference-and-equivalent": "audio",
}
EXPECTED_RATINGS = {
  "institutional-recognition", "facility-recognition", "map-legibility",
  "consequence-comprehension", "information-density", "cognitive-load",
  "animation-usefulness", "audio-usefulness", "audio-fatigue",
  "perceived-game-identity", "accessibility", "trust-in-information-boundaries",
}
EXPECTED_PRIVACY_FORBIDDEN = [
  "names", "contact details", "health information", "private game state",
  "identifying recordings",
]


class Phase10EvaluationPreparationTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    cls.guide = GUIDE.read_text(encoding="utf-8")
    cls.log = LOG.read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    cls.phase10_2 = roadmap.split("## Milestone 10.2:", 1)[1].split("# Phase 11:", 1)[0]

  def test_protocol_covers_preparation_tasks_and_dimensions(self):
    self.assertEqual(
      set(self.protocol),
      {
        "schema_version", "status", "campaign", "seed_policy",
        "participant_groups", "tasks", "rating_dimensions", "rating_scale",
        "finding_categories", "privacy", "decision", "evidence_limits",
      },
    )
    self.assertEqual(self.protocol["schema_version"], "visual-audio-phase10-2-evaluation-v1")
    self.assertEqual(self.protocol["status"], "ready-for-human-evaluation")
    tasks = self.protocol["tasks"]
    self.assertEqual(len(tasks), len(EXPECTED_TASKS))
    self.assertEqual(len({task["id"] for task in tasks}), len(tasks))
    self.assertEqual({task["id"]: task["category"] for task in tasks}, EXPECTED_TASKS)
    for task in tasks:
      self.assertEqual(set(task), {"id", "category", "prompt", "success_observation"})
      for field in ("id", "category", "prompt", "success_observation"):
        self.assertIsInstance(task[field], str)
        self.assertTrue(task[field].strip())
    self.assertEqual(len(self.protocol["rating_dimensions"]), len(EXPECTED_RATINGS))
    self.assertEqual(set(self.protocol["rating_dimensions"]), EXPECTED_RATINGS)
    self.assertEqual(
      self.protocol["rating_scale"],
      "1=very poor or confusing; 5=very clear or useful; not-observed is allowed.",
    )
    self.assertEqual(
      self.protocol["participant_groups"],
      [
        "project-owner-or-contributor", "strategy-game-player",
        "health-policy-or-management-expert", "accessibility-oriented-reviewer",
        "first-time-user",
      ],
    )
    self.assertEqual(self.protocol["finding_categories"], ["defect", "preference", "scope-expansion"])

  def test_privacy_and_decision_boundaries_remain_blank(self):
    privacy = self.protocol["privacy"]
    self.assertEqual(set(privacy), {"repository_may_contain", "repository_must_not_contain"})
    self.assertEqual(
      privacy["repository_may_contain"],
      ["anonymized role/category", "task outcome", "bounded feedback", "revision classification"],
    )
    self.assertEqual(privacy["repository_must_not_contain"], EXPECTED_PRIVACY_FORBIDDEN)
    decision = self.protocol["decision"]
    self.assertEqual(
      set(decision), {"status", "go_no_go", "authorized_reviewer", "recorded_at", "rationale"},
    )
    self.assertEqual(decision["status"], "pending-human-evidence")
    for field in ("go_no_go", "authorized_reviewer", "recorded_at", "rationale"):
      self.assertIsNone(decision[field])
    self.assertIn("No participant results", " ".join(self.protocol["evidence_limits"]))
    self.assertIn("Status: prepared; no participant findings have been collected or entered.", self.log)
    self.assertEqual(
      [line for line in self.log.splitlines() if line.startswith("|")],
      [
        "| Finding ID | Participant group | Task ID | Category (`defect` / `preference` / `scope-expansion`) | Observation | Evidence reference | Proposed revision | Owner | Status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        "| — | — | — | — | No findings recorded. | — | — | — | pending human evaluation |",
      ],
    )
    decision_lines = self.log.split("## Decision record", 1)[1].split("Automated checks", 1)[0]
    self.assertEqual(
      [line.strip() for line in decision_lines.splitlines() if line.strip()],
      [
        "- Go/no-go: pending human evidence.",
        "- Authorized reviewer: —",
        "- Decision date: —",
        "- Rationale: —",
      ],
    )

  def test_roadmap_marks_only_preparation_items_complete(self):
    expected_checklist = [
      ("x", "Test protocol written."),
      ("x", "First-session tasks defined."),
      ("x", "Recognition tasks defined."),
      ("x", "Consequence-tracing tasks defined."),
      ("x", "Accessibility tasks defined."),
      (" ", "Audio preference feedback collected."),
      (" ", "Quantitative ratings collected."),
      (" ", "Qualitative interviews completed."),
      (" ", "Findings classified as defect, preference, or scope expansion."),
      ("x", "Revision log created."),
      (" ", "Go/no-go decision recorded."),
    ]
    actual_checklist = re.findall(r"^- \[([ x])\] (.+)$", self.phase10_2, re.MULTILINE)
    self.assertEqual(actual_checklist, expected_checklist)

  def test_facilitator_guide_and_log_state_evidence_limits(self):
    for marker in (
      "Purpose and boundaries",
      "Participants and session shape",
      "First-session tasks",
      "Recognition tasks",
      "Consequence-tracing tasks",
      "Accessibility and audio tasks",
      "Measurement and coding",
      "Evidence limits",
      "does not establish",
      "No participant results",
    ):
      self.assertIn(marker, self.guide)
    self.assertIn("No findings recorded", self.log)
    self.assertNotIn("go/no-go: go", self.log.lower())


if __name__ == "__main__":
  unittest.main()
