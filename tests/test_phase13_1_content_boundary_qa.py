import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase13.1-content-boundary-qa.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"
REVIEWED_SURFACES = (
  ROOT / "README.md",
  ROOT / "docs" / "guides" / "gui-how-to-play.md",
  ROOT / "gui" / "index.html",
  ROOT / "gui" / "metric-visualization-proof.html",
  *sorted((ROOT / "gui").glob("*.mjs")),
)

EXPECTED_SOURCE_CONTRACT = {
  "player_limitations": (
    "docs/guides/gui-how-to-play.md",
    "This is a fictional educational simulation and research prototype.",
  ),
  "decision_boundary": (
    "docs/guides/gui-how-to-play.md",
    "operational, clinical, financial, regulatory,",
  ),
  "metric_boundary": (
    "gui/metric-visualization-proof.html",
    "Numeric visuals never add precision beyond supplied fields and do not establish a probability, forecast, or hidden state.",
  ),
  "semantic_source_boundary": (
    "gui/semantic-containers.mjs",
    "Preserve visible source and status language; never add hidden severity.",
  ),
  "hidden_state_scan": (
    "tests/test_phase13_1_hidden_state_boundary.py",
    'BROWSER_MODULES = tuple(sorted((ROOT / "gui").glob("*.mjs")))',
  ),
}

FORBIDDEN_CLAIM_PATTERNS = (
  r"\bdiagnos(?:e|es|ed|ing|tic|tics)\b",
  r"\b(?:prescrib\w*|prescription|dosage)\b",
  r"\bmedical advice\b",
  r"\bmedication\w*\b",
  r"\b(?:treatment|care)\s+(?:plan|recommendation|decision|advice)\b",
  r"\bpatient[- ]specific\b",
  r"\bclinical\s+(?:recommendation|decision|advice|treatment)\w*\b",
)


class Phase131ContentBoundaryQATests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")
    cls.surface_text = "\n".join(
      path.read_text(encoding="utf-8") for path in REVIEWED_SURFACES
    )

  def test_source_contract_markers_exist(self):
    self.assertEqual(
      self.ledger["schema_version"], "phase13.1-content-boundary-qa-v1"
    )
    self.assertEqual(
      self.ledger["status"], "pass-bounded-technical-content-qa-only"
    )
    self.assertEqual(set(self.ledger["source_contract"]), set(EXPECTED_SOURCE_CONTRACT))
    for key, (source_path, marker) in EXPECTED_SOURCE_CONTRACT.items():
      self.assertEqual(
        self.ledger["source_contract"][key], f"{source_path}: {marker}"
      )
      path = ROOT / source_path
      self.assertTrue(path.is_file(), key)
      self.assertIn(marker, path.read_text(encoding="utf-8"), key)

  def test_reviewed_surfaces_do_not_make_clinical_advice_claims(self):
    normalized = self.surface_text.lower()
    self.assertEqual(
      tuple(self.ledger["forbidden_claim_fragments"]),
      (
        "clinical recommendation",
        "medical advice",
        "diagnosis or diagnostic wording",
        "prescribing, prescription, or dosage wording",
        "medication wording",
        "treatment or care plan wording",
        "patient-specific wording",
        "clinical decision wording",
      ),
    )
    for pattern in FORBIDDEN_CLAIM_PATTERNS:
      self.assertIsNone(
        re.search(pattern, normalized),
        pattern,
      )

  def test_fictional_precision_and_source_boundaries_remain_visible(self):
    guide = " ".join(
      (ROOT / "docs" / "guides" / "gui-how-to-play.md")
      .read_text(encoding="utf-8")
      .split()
    )
    metric_proof = (ROOT / "gui" / "metric-visualization-proof.html").read_text(
      encoding="utf-8"
    )
    semantic_catalog = (ROOT / "gui" / "semantic-containers.mjs").read_text(
      encoding="utf-8"
    )
    for marker in (
      "fictional educational simulation",
      "not a calibrated policy forecast",
      "operational, clinical, financial, regulatory",
      "real institution, policy, payer, workforce, or community",
      "Do not use the game to make real-world decisions",
    ):
      self.assertIn(marker, guide)
    self.assertIn("Numeric visuals never add precision", metric_proof)
    self.assertIn("do not establish a probability, forecast, or hidden state", metric_proof)
    self.assertIn("Preserve visible source and status language", semantic_catalog)

  def test_roadmap_marks_only_bounded_content_qa(self):
    normalized_roadmap = " ".join(self.roadmap.split())
    self.assertIn("[ ] No unsupported clinical implication introduced.", normalized_roadmap)
    self.assertIn("[x] Current GUI source/content wording scan completed.", normalized_roadmap)
    self.assertIn("bounded repository-owned source/content wording check", normalized_roadmap)
    for marker in (
      "clinical or policy expert approval",
      "human comprehension",
      "educational effectiveness",
      "public-release review",
    ):
      self.assertIn(marker, " ".join(self.ledger["limits"]).lower())


if __name__ == "__main__":
  unittest.main()
