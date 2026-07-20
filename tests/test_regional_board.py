import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "gui" / "regional-board.mjs"
SCENE = ROOT / "gui" / "scene.mjs"
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
PROOF = ROOT / "gui" / "regional-board-proof.html"
SNAPSHOT = ROOT / "tests" / "fixtures" / "regional_board_snapshot.sha256"


def run_node(script):
  return subprocess.run(
    ["node", "--input-type=module", "-e", script],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
  )


class RegionalBoardTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.adapter = ADAPTER.read_text(encoding="utf-8")
    cls.scene = SCENE.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")

  def test_host_dto_mapping_is_deterministic_and_explicit(self):
    result = run_node(
      """
      import { regionalWorldToSceneData } from './gui/regional-board.mjs';
      const scene = regionalWorldToSceneData({
        schema_version: 'competitive-regional-world-v1',
        entities: [
          { id: 'rival z', name: 'Zeta', role: 'Public rival', visibility: 'public', layout_slot: 'rival-2', status: 'uncertain', source: 'visible-source', facilities: [] },
          { id: 'unknown-system', name: 'Unlisted', role: 'Institution unavailable', visibility: 'unknown', layout_slot: 'rival-1', status: 'not-provided', source: 'visible-source', facilities: [{ name: 'Unlisted facility', kind: 'unknown kind' }] },
        ],
        missing: [{ id: 'unknown-system-private-detail', label: 'Private detail', source: 'missing-source' }],
        overlays: [{ id: 'demand', label: 'Demand pressure', value: '12', unit: 'units', source: 'overlay-source', equivalent: 'Written equivalent.' }],
      });
      if (scene.entities[0].id !== 'unknown-system' || scene.entities[1].id !== 'rival-z' || scene.entities[1].source_id !== 'rival z') process.exit(1);
      if (!scene.entities[0].summary.includes('Private detail')) process.exit(2);
      if (scene.entities[0].facilities[0].id !== 'unknown-system-unlisted-facility') process.exit(3);
      if (scene.overlays[0].source !== 'overlay-source') process.exit(4);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_static_board_svg_snapshot_is_stable(self):
    expected = SNAPSHOT.read_text(encoding="utf-8").strip()
    result = run_node(
      """
      import { createHash } from 'node:crypto';
      import { regionalWorldToSceneData } from './gui/regional-board.mjs';
      import { renderRegionalSvg } from './gui/scene.mjs';
      const scene = regionalWorldToSceneData({
        schema_version: 'competitive-regional-world-v1',
        entities: [
          { id: 'riverside', name: 'Riverside', role: 'Player system', visibility: 'owned', layout_slot: 'player', status: 'constrained', source: 'PlayerObservation', facilities: [{ name: 'General hospital', kind: 'general hospital' }] },
          { id: 'northlake', name: 'Northlake', role: 'Public rival', visibility: 'public', layout_slot: 'rival-1', status: 'uncertain', source: 'PublicActionEntry', facilities: [] },
          { id: 'unknown-system', name: 'Unlisted institution', role: 'Institution unavailable', visibility: 'unknown', layout_slot: 'rival-2', status: 'not-provided', source: 'RegionalWorldEntity', facilities: [{ name: 'Unlisted facility', kind: 'unknown kind' }] },
        ],
        missing: [{ id: 'northlake-private-detail', label: 'Private rival operations', source: 'RegionalWorldMissing' }],
        overlays: [{ id: 'demand', label: 'Demand pressure', value: '12', unit: 'units', source: 'PlayerObservation.monthly_unmet_demand', equivalent: 'Written demand pressure.' }],
      });
      const svg = renderRegionalSvg(scene, { selectedId: 'riverside' });
      if (!svg.includes('Demand pressure') || !svg.includes('Private rival operations')) process.exit(1);
      if (!svg.includes('PlayerObservation') || !svg.includes('Uncertain') || !svg.includes('Institution')) process.exit(2);
      console.log(createHash('sha256').update(svg).digest('hex'));
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), expected)

  def test_existing_gui_mounts_board_and_keeps_selection_local(self):
    for marker in (
      'import { presentationFixtureToSceneData, regionalWorldToSceneData }',
      'renderRegionalBoard',
      'View on regional board',
      'data-entity-container-id',
      'currentMapEntities',
    ):
      self.assertIn(marker, self.app)
    for marker in ('id="regional-board"', 'Graphical regional operating board'):
      self.assertIn(marker, self.html)
    order = [self.html.index(marker) for marker in ('id="regional-board"', 'id="map-list"', 'id="regional-overlay-list"', 'id="entity-detail"')]
    self.assertEqual(order, sorted(order))
    for forbidden in ('CompetitiveWorldState', 'resolved_inputs', 'effect_queue', 'fetch(', 'WebSocket'):
      self.assertNotIn(forbidden, self.adapter + self.proof)

  def test_proof_is_static_keyboard_and_source_aware(self):
    for marker in ('regionalWorldToSceneData', 'renderRegionalSvg', 'Fixture-only host-shaped DTO', 'data-select', 'keydown', 'Private rival operations'):
      self.assertIn(marker, self.proof)
    for path in (ADAPTER, SCENE, APP):
      result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, check=False)
      self.assertEqual(result.returncode, 0, result.stderr)

if __name__ == "__main__":
  unittest.main()
