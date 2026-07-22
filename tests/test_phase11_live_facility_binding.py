import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = (
  ROOT / "gui" / "regional-board.mjs",
  ROOT / "gui" / "scene.mjs",
  ROOT / "gui" / "app.mjs",
)


NODE_PROBE = r'''
import { regionalWorldToSceneData } from './gui/regional-board.mjs';
import { renderRegionalSvg } from './gui/scene.mjs';
import { regionalEntitiesToFixture } from './gui/app.mjs';

const scene = regionalWorldToSceneData({
  schema_version: 'competitive-regional-world-v1',
  entities: [{
    id: 'system-1',
    name: 'Riverside',
    role: 'Player system',
    visibility: 'owned',
    layout_slot: 1,
    status: 'reported',
    source: 'Host-projected player identity + PlayerObservation',
    facilities: [
      { name: 'Inpatient beds', kind: 'Owned capacity', component_id: 'general-hospital-base', source: 'PlayerObservation capacity fields' },
      { name: 'Unknown facility', kind: 'Owned capacity', component_id: 'not-registered', source: 'Fixture source' },
    ],
  }],
  missing: [],
  overlays: [],
});
const [known, fallback] = scene.entities[0].facilities;
if (known.component_id !== 'general-hospital-base') process.exit(1);
if (known.component_label !== 'General hospital base') process.exit(2);
if (known.component_release_path !== 'assets/release/visual/svg/general-hospital-base.svg') process.exit(3);
if (fallback.component_id !== 'generic-facility') process.exit(4);
if (fallback.component_source !== 'Missing or unknown visible facility kind') process.exit(5);
if (fallback.component_equivalent !== 'Facility label and generic marker') process.exit(6);
const detailEntities = regionalEntitiesToFixture({
  entities: [{
    id: 'system-1',
    name: 'Riverside',
    role: 'Player system',
    visibility: 'owned',
    status: 'reported',
    status_label: 'Reported',
    source: 'PlayerObservation',
    facilities: [
      { name: 'Known', kind: 'Owned capacity', component_id: 'general-hospital-base', metrics: [], source: 'PlayerObservation' },
      { name: 'Unknown', kind: 'Owned capacity', component_id: '__proto__', metrics: [], source: 'PlayerObservation' },
    ],
  }],
  missing: [],
});
const [detailKnown, detailFallback] = detailEntities[0].facilities;
if (detailKnown.component_label !== 'General hospital base' || detailKnown.component_source !== 'Visible facility kind and actor-visible status context') process.exit(8);
if (detailFallback.component_id !== 'generic-facility' || detailFallback.component_label !== 'Facility') process.exit(9);
const svg = renderRegionalSvg(scene, { selectedId: known.id });
for (const marker of [
  'data-component-id="general-hospital-base"',
  'Component: General hospital base',
  'General hospital label, base silhouette, identity badge, and written layer labels',
  'data-component-id="generic-facility"',
]) {
  if (!svg.includes(marker)) process.exit(10);
}
console.log('pass');
'''


class Phase11LiveFacilityBindingTests(unittest.TestCase):
  def test_actor_visible_facilities_bind_to_catalog_components_with_fallback(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", NODE_PROBE],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_presentation_path_has_no_hidden_authority_or_network_imports(self):
    source = "".join(path.read_text(encoding="utf-8") for path in MODULES)
    for forbidden in (
      "CompetitiveWorldState",
      "HealthSystemState",
      "resolved_inputs",
      "effect_queue",
      "fetch(",
      "WebSocket",
      "Math.random",
    ):
      self.assertNotIn(forbidden, source)
    for path in MODULES:
      result = subprocess.run(
        ["node", "--check", str(path)],
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr)

  def test_detail_view_exposes_component_semantics(self):
    app = (ROOT / "gui" / "app.mjs").read_text(encoding="utf-8")
    for marker in (
      "Visual component:",
      "component_equivalent",
      "component_source",
      "component_release_path",
    ):
      self.assertIn(marker, app)


if __name__ == "__main__":
  unittest.main()
