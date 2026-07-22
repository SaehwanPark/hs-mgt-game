import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
VISUAL_CATALOG = ROOT / "gui" / "visual-catalog.json"
IMPORT_PATTERN = re.compile(r"(?:from|import) [\"'](\.[^\"']+\.mjs)[\"']")


def run_node(script):
  return subprocess.run(
    ["node", "--input-type=module", "-e", script],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
  )


def production_module_closure(entry):
  pending = [entry]
  visited = set()
  while pending:
    path = pending.pop()
    if path in visited:
      continue
    visited.add(path)
    source = path.read_text(encoding="utf-8")
    for relative in IMPORT_PATTERN.findall(source):
      dependency = (path.parent / relative).resolve()
      if dependency.is_file():
        pending.append(dependency)
  return visited


class Phase10FirstMonthTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    roadmap = ROADMAP.read_text(encoding="utf-8")
    cls.phase10 = roadmap.split("## Milestone 10.1:", 1)[1].split("## Milestone 10.2:", 1)[0]
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.visual_catalog = json.loads(VISUAL_CATALOG.read_text(encoding="utf-8"))

  def test_every_phase10_technical_checklist_item_is_evidenced(self):
    expected_labels = (
      "Three systems visible.",
      "Facilities visually distinct.",
      "Institutional identity consistent.",
      "Facility selection works.",
      "Uncertainty rendering works.",
      "Project overlay works.",
      "Pressure overlay works.",
      "Rival observation timing respected.",
      "Briefing uses semantic container.",
      "Action queue uses semantic container.",
      "Reports use actor-family identities.",
      "Metrics use appropriate visualizations.",
      "Source and status labels remain visible.",
      "Month sequence implemented.",
      "Critical event prioritization works.",
      "Map and reports update coherently.",
      "Skip behavior works.",
      "Reduced-motion behavior works.",
      "Replay is deterministic.",
      "UI cues refined.",
      "Environmental ambience available.",
      "Adaptive music transition works.",
      "Priority and cooldown manager works.",
      "Full mute works.",
      "Cues-only mode works.",
      "Text equivalents remain available.",
      "Every asset registered.",
      "Every asset hashed.",
      "Every license policy check passes; human legal review remains external.",
      "Credits generated.",
      "AI metadata complete where applicable.",
    )
    actual = re.findall(r"^- \[([ x])\] (.+)$", self.phase10, re.MULTILINE)
    self.assertEqual([label for _state, label in actual], list(expected_labels))
    self.assertTrue(all(state == "x" for state, _label in actual))

  def test_live_sources_bind_the_feature_matrix_without_authority_expansion(self):
    identities = {entry["id"] for entry in self.visual_catalog["identities"]}
    self.assertTrue({"riverside", "northlake", "summit"}.issubset(identities))
    for marker in (
      'id="regional-board"',
      'id="map-list"',
      'id="entity-detail"',
      'id="first-month-flow"',
      'id="action-region"',
      'id="resolution-panel"',
      'id="audio-panel"',
      'id="history-heading"',
      'id="debrief-region"',
      "renderRegionalWorld",
      "createFirstMonthFlow",
      "createResolutionClient",
      "createAudioClient",
      "setMusicState",
      "setAmbienceFromVisible",
      "prefers-reduced-motion",
      "resolution-skip",
      "replay",
      "state_hash",
    ):
      self.assertIn(marker, self.app + self.html)
    for path in production_module_closure(APP):
      source = path.read_text(encoding="utf-8")
      for forbidden in (
        "CompetitiveWorldState",
        "HealthSystemState",
        "resolved_inputs",
        "effect_queue",
        "transition_competitive",
        "fetch(",
        "WebSocket",
        "Math.random",
      ):
        self.assertNotIn(forbidden, source, path.relative_to(ROOT).as_posix())

  def test_first_month_and_music_probes_are_deterministic(self):
    result = run_node(
      """
      globalThis.fetch = () => { throw new Error('network access forbidden'); };
      globalThis.WebSocket = class { constructor() { throw new Error('socket access forbidden'); } };
      const { FIRST_MONTH_FLOW_SCHEMA, firstMonthStageFor } = await import('./gui/first-month.mjs');
      const { musicReplaySequence } = await import('./gui/music-stem-contract.mjs');
      const { sequenceForSkip } = await import('./gui/resolution-sequence.mjs');
      const stages = [
        firstMonthStageFor({}),
        firstMonthStageFor({ sessionLoaded: true }),
        firstMonthStageFor({ sessionLoaded: true, actionCatalogLoaded: true }),
        firstMonthStageFor({ sessionLoaded: true, actionCatalogLoaded: true, draftCount: 2 }),
        firstMonthStageFor({ sessionLoaded: true, actionCatalogLoaded: true, draftCount: 2, validated: true }),
        firstMonthStageFor({ sessionLoaded: true, actionCatalogLoaded: true, draftCount: 2, validated: true, submitted: true }),
        firstMonthStageFor({ sessionLoaded: true, actionCatalogLoaded: true, submitted: true, resolutionVisible: true, refreshed: true }),
      ];
      const expected = ['start', 'inspect', 'draft', 'validate', 'submit', 'resolution', 'continue'];
      if (FIRST_MONTH_FLOW_SCHEMA !== 'competitive-first-month-v1' || JSON.stringify(stages) !== JSON.stringify(expected)) process.exit(1);
      const music = musicReplaySequence([
        { stage: 'menu' },
        { observation: { policy_bullets: ['Regulatory review is visible'] } },
        { observation: { operations: { margin: -1, unmet_demand: 2 } } },
        { done: true },
      ]);
      if (JSON.stringify(music) !== JSON.stringify(['menu', 'regulatory_scrutiny', 'pressure', 'debrief'])) process.exit(2);
      const skipped = sequenceForSkip({ steps: [{ id: 'a' }, { id: 'b' }], turn: 1 });
      if (!skipped.skipped || skipped.active_index !== 9 || skipped.written_stage_count !== 10 || !skipped.report_text_retained) process.exit(3);
      console.log(JSON.stringify({ schema: FIRST_MONTH_FLOW_SCHEMA, stages, music, skipped: skipped.skipped }));
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    payload = json.loads(result.stdout)
    self.assertEqual(payload["stages"][-1], "continue")
    self.assertTrue(payload["skipped"])

  def test_javascript_syntax_is_valid(self):
    result = subprocess.run(["node", "--check", str(APP)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
