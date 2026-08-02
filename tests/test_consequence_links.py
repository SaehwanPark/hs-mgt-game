import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINKS = ROOT / "gui" / "consequence-links.mjs"
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"


def run_node(script):
  return subprocess.run(
    ["node", "--input-type=module", "-e", script],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
  )


class ConsequenceLinkTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.links = LINKS.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")

  def test_regional_links_preserve_public_observation_boundary(self):
    result = run_node(
      """
      import { regionalWorldConsequenceLinks } from './gui/consequence-links.mjs';
      const links = regionalWorldConsequenceLinks({
        schema_version: 'competitive-regional-world-v1',
        session: { turn: 2 },
        entities: [
          { id: 'northlake', name: 'Northlake', layout_slot: 1, signals: [{ text: 'Outpatient expansion reported', observed_month: 1, source: 'PublicActionEntry' }], processes: [] },
          { id: 'riverside', name: 'Riverside', layout_slot: 0, signals: [], processes: [{ label: 'Recruitment process', detail: 'Pending host-reported process', source: 'PlayerObservation.in_flight_projects' }] },
        ],
      });
      if (links[0].target_id !== 'northlake' || links[0].observed_month !== 1) process.exit(1);
      if (!links[0].information_boundary.includes('private rival detail')) process.exit(2);
      if (links[1].target_id !== 'riverside' || links[1].kind !== 'visible-process') process.exit(3);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_resolution_effects_are_stable_and_do_not_infer_targets(self):
    result = run_node(
      """
      import { resolutionConsequenceLinks } from './gui/consequence-links.mjs';
      const links = resolutionConsequenceLinks({
        schema_version: 'competitive-resolution-v1',
        turn: 3,
        effects: [
          { metric: 'margin', delta: -2, text: 'Margin changed', source: 'ResolutionEffect.margin' },
          { metric: 'cash', delta: 4, text: 'Cash changed', source: 'ResolutionEffect.cash' },
        ],
        replay: { selected_turn: 3, state_hash: 'hash-3' },
      });
      if (links[0].label !== 'cash' || links[1].label !== 'margin') process.exit(1);
      if (links.some((link) => link.target_id)) process.exit(2);
      if (!links.every((link) => link.state_hash === 'hash-3' && link.information_boundary.includes('future outcome'))) process.exit(3);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_response_links_preserve_order_and_public_boundary(self):
    result = run_node(
      """
      import { resolutionResponseLinks } from './gui/consequence-links.mjs';
      const links = resolutionResponseLinks({
        schema_version: 'competitive-resolution-v1',
        turn: 3,
        steps: [{ id: 'responses', source: 'TransitionSummary.events', items: ['Payer response reported', 'Workforce response reported'] }],
        replay: { state_hash: 'hash-3' },
      });
      if (links.length !== 2 || links[0].detail !== 'Payer response reported' || links[1].detail !== 'Workforce response reported') process.exit(1);
      if (links.some((link) => link.target_id || link.delta !== undefined)) process.exit(2);
      if (!links.every((link) => link.turn === 3 && link.state_hash === 'hash-3' && link.information_boundary.includes('actor intent'))) process.exit(3);
      const fallback = resolutionResponseLinks({ schema_version: 'competitive-resolution-v1', turn: 4, steps: [{ id: 'responses', items: [true, {}, '   '] }], replay: {} });
      if (fallback.length !== 3 || !fallback.every((link) => link.detail === 'No visible institutional responses.') || fallback.some((link) => link.source !== 'Host response source unavailable.')) process.exit(4);
      const mixed = resolutionResponseLinks({ schema_version: 'competitive-resolution-v1', steps: [{ id: 'responses', items: ['Public response', true, {}, '   '] }] });
      if (mixed.length !== 4 || mixed[0].detail !== 'Public response' || !mixed.slice(1).every((link) => link.detail === 'No visible institutional responses.')) process.exit(5);
      if (resolutionResponseLinks({ schema_version: 'competitive-resolution-v1', steps: [{ id: 'operations', items: ['not a response'] }] }).length !== 0) process.exit(6);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_context_formatter_preserves_timing_and_explicit_replay_fallbacks(self):
    result = run_node(
      """
      import { consequenceLinkContext } from './gui/consequence-links.mjs';
      if (consequenceLinkContext({ observed_month: 2, turn: 4, state_hash: 'hash-4' }) !== 'Observed month 2 · Replay state hash hash-4') process.exit(1);
      if (consequenceLinkContext({ turn: 4 }) !== 'Turn 4 · Replay context unavailable') process.exit(2);
      if (consequenceLinkContext({ turn: 'invalid', state_hash: '   ' }) !== 'Timing unavailable · Replay context unavailable') process.exit(3);
      if (consequenceLinkContext({ observed_month: true, turn: [], state_hash: 123 }) !== 'Timing unavailable · Replay context unavailable') process.exit(4);
      if (consequenceLinkContext({ observed_month: [2], turn: 4, state_hash: {} }) !== 'Turn 4 · Replay context unavailable') process.exit(5);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_delta_formatter_is_signed_and_fail_closed(self):
    result = run_node(
      """
      import { consequenceLinkDelta } from './gui/consequence-links.mjs';
      if (consequenceLinkDelta({ kind: 'committed-effect', delta: 4 }) !== 'Delta +4') process.exit(1);
      if (consequenceLinkDelta({ kind: 'committed-effect', delta: -2 }) !== 'Delta -2') process.exit(2);
      if (consequenceLinkDelta({ kind: 'committed-effect', delta: 0 }) !== 'Delta 0') process.exit(3);
      if (consequenceLinkDelta({ kind: 'committed-effect' }) !== 'Delta unavailable') process.exit(4);
      if (consequenceLinkDelta({ kind: 'committed-effect', delta: true }) !== 'Delta unavailable') process.exit(5);
      if (consequenceLinkDelta({ kind: 'committed-effect', delta: [] }) !== 'Delta unavailable') process.exit(6);
      if (consequenceLinkDelta({ kind: 'visible-process', delta: 9 }) !== '') process.exit(7);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_replay_sequence_keeps_historical_turns_and_hashes(self):
    result = run_node(
      """
      import { replayConsequenceSequence } from './gui/consequence-links.mjs';
      const sequence = replayConsequenceSequence([
        { schema_version: 'competitive-resolution-v1', turn: 2, replay: { selected_turn: 2, state_hash: 'hash-2' }, effects: [] },
        { schema_version: 'competitive-resolution-v1', turn: 1, replay: { selected_turn: 1, state_hash: 'hash-1' }, effects: [] },
      ]);
      if (sequence.length !== 2 || sequence[0].turn !== 1 || sequence[1].state_hash !== 'hash-2') process.exit(1);
      if (sequence[0].links === sequence[1].links) process.exit(2);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_gui_exposes_bidirectional_links_and_static_boundary(self):
    for marker in (
      "regionalWorldConsequenceLinks",
      "resolutionConsequenceLinks",
      "consequenceLinkContext",
      "consequenceLinkDelta",
      "resolutionResponseLinks",
      "renderConsequenceLinks",
      "consequence-delta",
      "link.kind === \"visible-response\"",
      "visualStatusFor(\"reported\")",
      "createVisualToken(reported, \"status\", root)",
      "function prependOrInsertBefore(parent, node)",
      "parent.insertBefore(node, parent.firstChild)",
      "currentResolutionSessionId",
      "presentationSessionId",
      "regionalSessionId",
      "Show related reports and consequences",
      "Focus board",
      "selectedEntityId = link.target_id",
      "renderSelectedEntity(currentMapEntities, root)",
      "briefingFocusEntityId = entity.id",
      "renderConsequenceLinks([...currentRegionalLinks, ...currentResolutionLinks], root)",
      "behavior: \"auto\"",
    ):
      self.assertIn(marker, self.app)
    for marker in ('id="consequence-link-list"', "Linked visible consequences"):
      self.assertIn(marker, self.html)
    for forbidden in ("CompetitiveWorldState", "resolved_inputs", "effect_queue", "fetch(", "WebSocket", "Math.random"):
      self.assertNotIn(forbidden, self.links + self.app)
    result = subprocess.run(["node", "--check", str(LINKS)], capture_output=True, text=True, check=False)
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
