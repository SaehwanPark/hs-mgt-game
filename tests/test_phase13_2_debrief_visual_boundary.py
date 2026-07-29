import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase13.2-debrief-visual-boundary.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"

EXPECTED_SOURCE_CONTRACT = {
  "host_debrief": (
    "src/mcp/session.rs",
    "debrief: educational_debrief(&session.history)",
  ),
  "terminal_test": (
    "tests/test_phase11_live_debrief.py",
    "def test_host_terminal_contract_is_explicit_and_presentation_only(self):",
  ),
  "terminal_renderer": (
    "gui/app.mjs",
    "export function renderEndSessionEnvelope(envelope, root = document) {",
  ),
  "terminal_validator": (
    "gui/app.mjs",
    "export function validateEndSessionEnvelope(envelope) {",
  ),
  "direct_effect_renderer": (
    "gui/app.mjs",
    "function appendResolutionItems(list, items, emptyMessage) {",
  ),
  "consequence_links": (
    "gui/consequence-links.mjs",
    "export function resolutionConsequenceLinks(envelope = {})",
  ),
  "text_first_boundary": (
    "gui/README.md",
    "text-first history/debrief view",
  ),
  "audio_fallback": (
    "gui/README.md",
    "Optional debrief music is atmospheric only",
  ),
}

NODE_PROBE = r'''
import { renderEndSessionEnvelope, renderResolution, validateEndSessionEnvelope } from "./gui/app.mjs";
import { resolutionConsequenceLinks } from "./gui/consequence-links.mjs";
import { planResolutionSequence } from "./gui/resolution-sequence.mjs";
import { createAudioClient } from "./gui/audio.mjs";

function node() {
  return {
    children: [],
    dataset: {},
    disabled: false,
    hidden: false,
    textContent: "",
    replaceChildren(...children) { this.children = children; },
    append(...children) { this.children.push(...children); },
    setAttribute(name, value) { this[name] = value; },
  };
}
const nodes = new Map([
  ["#history-list", node()],
  ["#debrief-list", node()],
  ["#session-meta", node()],
  ["#session-end", node()],
  ["#command-form", node()],
  ["#legal-command-list", node()],
  ["#action-builder", node()],
  ["#draft-action-list", node()],
  ["#validate-actions", node()],
  ["#submit-month", node()],
  ["#resolution-panel", node()],
  ["#resolution-state", node()],
  ["#resolution-step-list", node()],
  ["#resolution-before-list", node()],
  ["#resolution-after-list", node()],
  ["#resolution-effect-list", node()],
  ["#resolution-progress", node()],
  ["#consequence-link-list", node()],
]);
globalThis.document = { createElement: node };
const root = { querySelector(selector) { return nodes.get(selector) ?? null; } };
const envelope = {
  schema_version: "competitive-end-session-v1",
  session_id: "session-1",
  campaign: "competitive-regional-v1",
  turn: 24,
  max_turns: 24,
  done: true,
  history: [{ turn: 24, state_hash: "hash-24" }],
  replay: { transition_count: 1, latest_state_hash: "hash-24" },
  debrief: ["Committed tradeoff remains available."],
};
const resolution = {
  schema_version: "competitive-resolution-v1",
  session_id: "session-1",
  turn: 24,
  steps: [{ id: "submitted", source: "HostResolution", items: ["Batch committed"] }],
  before: { resources: { cash: 40 }, observation: { operations: { margin: 3 } } },
  after: { resources: { cash: 38 }, observation: { operations: { margin: 1 } } },
  effects: [{ metric: "margin", delta: -2, text: "Margin changed", source: "ResolutionEffect.margin" }],
  replay: { state_hash: "hash-24" },
};
const audioRoot = { hidden: false, querySelector() { return null; }, addEventListener() {}, removeEventListener() {} };
const audio = createAudioClient({ root: audioRoot, AudioContextCtor: null });
audio.setMuted(true);
if (!audio.state().muted) process.exit(6);
const rendered = renderEndSessionEnvelope(envelope, root);
const invalid = validateEndSessionEnvelope({ ...envelope, replay: { ...envelope.replay, latest_state_hash: "wrong" } });
if (!rendered.ok || nodes.get("#history-list").children.length !== 1) process.exit(1);
if (nodes.get("#debrief-list").children.length !== 1) process.exit(2);
if (!nodes.get("#session-meta").textContent.includes("final turn 24/24")) process.exit(3);
if (!nodes.get("#session-end").disabled) process.exit(4);
if (!nodes.get("#command-form").hidden || nodes.get("#legal-command-list").children.length !== 1) process.exit(5);
if (!["#action-builder", "#draft-action-list", "#validate-actions", "#submit-month"].every((selector) => nodes.get(selector).hidden)) process.exit(7);
if (invalid.ok || invalid.code !== "misaligned_end_session") process.exit(8);
const renderedResolution = renderResolution(resolution, root);
if (!renderedResolution.ok || nodes.get("#resolution-effect-list").children.length !== 1) process.exit(9);
if (!nodes.get("#resolution-effect-list").children[0].textContent.includes("Margin changed · Source: ResolutionEffect.margin")) process.exit(10);
if (!nodes.get("#resolution-before-list").children[0].textContent.includes("Cash: 40")) process.exit(11);
if (nodes.get("#consequence-link-list").children.length !== 1) process.exit(12);
const links = resolutionConsequenceLinks(resolution);
if (links[0].source !== "ResolutionEffect.margin" || !links[0].information_boundary.includes("no future outcome")) process.exit(13);
const reduced = planResolutionSequence(resolution, { reduced_motion: true });
if (!reduced.every((step) => step.reduced_motion && step.items.length > 0)) process.exit(14);
audio.destroy();
console.log(JSON.stringify({ rendered: rendered.ok, invalid: invalid.code, effect: nodes.get("#resolution-effect-list").children[0].textContent, reducedStages: reduced.length }));
'''


class Phase132DebriefVisualBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")

  def test_source_contract_is_independently_anchored(self):
    self.assertEqual(
      self.ledger["schema_version"], "phase13.2-debrief-visual-boundary-v1"
    )
    self.assertEqual(
      self.ledger["status"],
      "complete-current-technical-debrief-visual-boundary-only",
    )
    self.assertEqual(set(self.ledger["source_contract"]), set(EXPECTED_SOURCE_CONTRACT))
    for key, (source_path, marker) in EXPECTED_SOURCE_CONTRACT.items():
      self.assertEqual(
        self.ledger["source_contract"][key], f"{source_path}: {marker}"
      )
      path = ROOT / source_path
      self.assertTrue(path.is_file(), key)
      source_text = " ".join(path.read_text(encoding="utf-8").split())
      self.assertIn(" ".join(marker.split()), source_text, key)

  def test_terminal_renderer_executes_alignment_and_read_only_contract(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", NODE_PROBE],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
    self.assertEqual(
      json.loads(result.stdout),
      {
        "rendered": True,
        "invalid": "misaligned_end_session",
        "effect": "Margin changed · Source: ResolutionEffect.margin",
        "reducedStages": 8,
      },
    )

  def test_path_surface_and_authority_contract_are_exactly_bounded(self):
    self.assertEqual(
      self.ledger["technical_path"],
      [
        "receive a host-supplied terminal session envelope",
        "validate terminal history, debrief, replay transition count, and latest state hash alignment",
        "render committed history, written debrief lines, terminal metadata, and read-only controls",
        "render host-supplied before/after snapshots, direct effects, and consequence links descriptively",
        "retain written history, hashes, debrief, and effect text when audio or motion is unavailable",
      ],
    )
    self.assertEqual(
      self.ledger["surface_contract"],
      {
        "terminal_sections": [
          "committed history",
          "replay transition count",
          "latest state hash",
          "written debrief",
          "before/after snapshots",
          "direct committed effects",
          "consequence links",
        ],
        "read_only_terminal_behavior": [
          "disable further action controls",
          "disable end-session control",
          "preserve host-supplied history and debrief",
        ],
        "optional_audio_boundary": "Debrief music is atmospheric only; written history, hashes, and debrief text remain complete when muted or unavailable.",
        "human_review_boundary": "Technical rendering evidence does not replace human visual, accessibility, educational, or classroom review.",
      },
    )
    self.assertEqual(
      self.ledger["findings"],
      {
        "terminal_envelope_alignment_is_source_bound": True,
        "history_hash_debrief_text_are_rendered": True,
        "direct_effects_remain_descriptive": True,
        "terminal_controls_become_read_only": True,
        "written_audio_and_motion_fallback_is_present": True,
        "human_debrief_visual_review": False,
        "educational_and_classroom_review": False,
      },
    )
    self.assertEqual(
      self.ledger["authority_boundary"],
      "The host/core owns terminal history, replay metadata, debrief lines, snapshots, direct effects, and hashes; the browser validates and renders supplied fields and does not author outcomes, infer causal graphs, or retain terminal mutation authority.",
    )

  def test_roadmap_keeps_technical_and_human_debrief_gates_distinct(self):
    normalized = " ".join(self.roadmap.split())
    self.assertIn("[ ] Debrief visuals reviewed.", normalized)
    self.assertIn(
      "[x] Current technical debrief visual presentation contract documented.",
      normalized,
    )
    for marker in (
      "visual quality",
      "human comprehension",
      "educational effectiveness",
      "structured human visual/educational review",
    ):
      self.assertIn(marker, " ".join(self.ledger["limits"]).lower())


if __name__ == "__main__":
  unittest.main()
