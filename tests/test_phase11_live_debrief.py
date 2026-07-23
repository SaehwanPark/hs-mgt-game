import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "gui" / "app.mjs"
ADAPTER = ROOT / "gui" / "host-adapter.mjs"
SERVER = ROOT / "src" / "gui_server.rs"
SESSION = ROOT / "src" / "mcp" / "session.rs"
HTML = ROOT / "gui" / "index.html"


NODE_PROBE = r'''
import { renderEndSessionEnvelope, validateEndSessionEnvelope } from './gui/app.mjs';

function node() {
  return {
    children: [],
    dataset: {},
    classList: { add() {} },
    append(...children) { this.children.push(...children); },
    replaceChildren(...children) { this.children = children; },
    setAttribute(name, value) { this[name] = value; },
  };
}
const nodes = new Map([
  ['#history-list', node()],
  ['#debrief-list', node()],
  ['#session-meta', node()],
  ['#command-form', node()],
  ['#legal-command-list', node()],
  ['#action-builder', node()],
  ['#draft-action-list', node()],
  ['#validate-actions', node()],
  ['#submit-month', node()],
  ['#session-end', node()],
  ['#session-status', node()],
  ['#presentation-state', node()],
]);
globalThis.document = {
  createElement: () => node(),
};
const root = { querySelector: (selector) => nodes.get(selector) ?? null };
const envelope = {
  schema_version: 'competitive-end-session-v1',
  session_id: 'session-1',
  campaign: 'competitive-regional-v1',
  seed: 42,
  turn: 2,
  max_turns: 24,
  done: true,
  history: [
    { turn: 1, command: 'hold', state_hash: 'hash-1' },
    { turn: 2, command: 'hold', state_hash: 'hash-2' },
  ],
  replay: { seed: 42, transition_count: 2, latest_state_hash: 'hash-2' },
  debrief: ['Host lesson: committed responses remain inspectable.'],
};
if (!validateEndSessionEnvelope(envelope).ok) process.exit(1);
const result = renderEndSessionEnvelope(envelope, root);
if (!result.ok) process.exit(2);
if (nodes.get('#history-list').children.length !== 2) process.exit(3);
if (nodes.get('#debrief-list').children.length !== 1) process.exit(4);
if (!nodes.get('#session-meta').textContent.includes('hash-2')) process.exit(5);
if (nodes.get('#session-end').disabled !== true) process.exit(6);
if (!nodes.get('#presentation-state').textContent.includes('final history and debrief')) process.exit(7);
if (validateEndSessionEnvelope({ ...envelope, schema_version: 'unknown' }).ok) process.exit(8);
if (validateEndSessionEnvelope({ ...envelope, replay: { transition_count: -1 } }).ok) process.exit(9);
if (validateEndSessionEnvelope({ ...envelope, replay: { transition_count: 1, latest_state_hash: 'hash-1' } }).ok) process.exit(10);
console.log('pass');
'''


class Phase11LiveDebriefTests(unittest.TestCase):
  def test_terminal_envelope_renders_aligned_history_replay_and_debrief(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", NODE_PROBE],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_host_terminal_contract_is_explicit_and_presentation_only(self):
    app = APP.read_text(encoding="utf-8")
    adapter = ADAPTER.read_text(encoding="utf-8")
    server = SERVER.read_text(encoding="utf-8")
    session = SESSION.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    for marker in (
      "competitive-end-session-v1",
      "renderEndSessionEnvelope",
      "validateEndSessionEnvelope",
      "endHostSession",
      "endSession",
      "final history and debrief",
      'id="session-end"',
      "/api/v1/sessions/{session_id}/end",
      "EndSessionEnvelope",
      "EndSessionReplayMetadata",
      "latest_state_hash",
    ):
      self.assertIn(marker, app + adapter + server + session + html)
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
      self.assertNotIn(forbidden, app)

  def test_changed_javascript_parses(self):
    for path in (APP, ADAPTER):
      result = subprocess.run(
        ["node", "--check", str(path)],
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
