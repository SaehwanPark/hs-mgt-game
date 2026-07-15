import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALIGNMENT = ROOT / "docs" / "visual-audio-phase0-alignment-v0.12.16.md"
ADR = ROOT / "docs" / "decision-records" / "0011-browser-native-presentation-client.md"
SPEC = ROOT / "SPEC.md"
ARCHITECTURE = ROOT / "ARCHITECTURE.md"


class VisualAudioPhase0Tests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.alignment = ALIGNMENT.read_text(encoding="utf-8")
    cls.adr = ADR.read_text(encoding="utf-8")
    cls.spec = SPEC.read_text(encoding="utf-8")
    cls.architecture = ARCHITECTURE.read_text(encoding="utf-8")

  def test_phase0_deliverables_are_present(self):
    for marker in (
      "## Approved interface boundary",
      "## First-month experience contract",
      "## Current presentation DTO inventory",
      "## Preliminary wireframe",
      "## Audio catalog and visible mapping",
      "## Asset and license policy",
      "### Hidden-state exclusions",
      "## Verification and promotion gate",
      "## Explicit non-goals",
    ):
      self.assertIn(marker, self.alignment)

  def test_actions_and_audio_are_bounded_by_visible_existing_surfaces(self):
    for marker in (
      "hold`, `recruit`, `invest`, `monitor`, `negotiate`, `commit`, and `project",
      "SessionEnvelope",
      "PlayerObservation",
      "TransitionSummary",
      "EndSessionEnvelope",
      "Every audio cue has a visible source",
      "classifier must",
      "No cue is assigned to private rival actions",
    ):
      self.assertIn(marker, self.alignment)

  def test_technology_decision_preserves_authority_boundary(self):
    for marker in (
      "browser-native HTML, CSS, and JavaScript ES",
      "native SVG",
      "host remains authoritative",
      "may not own true state",
      "no framework, bundler, remote asset service",
    ):
      self.assertIn(marker, self.alignment)
    for marker in (
      "# ADR-0011",
      "Browser-Native Presentation Client and Host Authority",
      "No framework, bundler, remote asset service",
    ):
      self.assertIn(marker, self.adr)

  def test_later_phases_remain_gated(self):
    self.assertIn("Phase 0 acceptance does not promote structured DTOs", self.spec)
    self.assertIn("Phase 1 static executive desktop", self.spec)
    self.assertIn("Phases 3–9 remain sequentially gated", self.spec)
    self.assertIn("remain planned implementations", self.architecture)

  def test_phase0_does_not_claim_runtime_or_human_validation(self):
    for marker in (
      "does not implement a GUI",
      "does not change simulation rules",
      "human usability",
      "lived human accessibility evidence",
    ):
      self.assertIn(marker, self.alignment)


if __name__ == "__main__":
  unittest.main()
