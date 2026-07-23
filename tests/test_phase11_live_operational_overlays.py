import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGIONAL = ROOT / "src" / "mcp" / "regional_world.rs"
BOARD = ROOT / "gui" / "regional-board.mjs"
APP = ROOT / "gui" / "app.mjs"


NODE_PROBE = r'''
import { regionalWorldToSceneData } from './gui/regional-board.mjs';
import { renderRegionalOverlays } from './gui/app.mjs';

const scene = regionalWorldToSceneData({
  schema_version: 'competitive-regional-world-v1',
  entities: [],
  overlays: [
    {
      id: 'unmet-demand',
      label: 'Unmet demand',
      value: '12',
      unit: 'demand units',
      source: 'PlayerObservation.monthly_unmet_demand',
      equivalent: 'Raw reported unmet-demand metric.',
      operational_overlay_id: 'operational-demand-pressure',
    },
    {
      id: 'demand',
      label: 'Reported demand',
      value: '120',
      unit: 'demand units',
      source: 'PlayerObservation.monthly_demand',
      equivalent: 'Raw demand metric.',
    },
    {
      id: 'unknown',
      label: 'Unknown category',
      value: 'reported',
      unit: 'status',
      source: 'Fixture source',
      equivalent: 'Fixture equivalent.',
      operational_overlay_id: 'not-registered',
    },
  ],
});
const [bound, raw, fallback] = scene.overlays;
if (bound.operational_overlay_id !== 'operational-demand-pressure') process.exit(1);
if (bound.label !== 'Demand pressure') process.exit(2);
if (bound.source !== 'PlayerObservation.monthly_unmet_demand') process.exit(3);
if (!bound.equivalent.includes('visible unmet-demand value')) process.exit(4);
if (raw.operational_overlay_id !== null || raw.label !== 'Reported demand') process.exit(5);
if (fallback.operational_overlay_id !== 'operational-overlay-generic') process.exit(6);
if (fallback.label !== 'Operational overlay unavailable') process.exit(7);
if (!fallback.equivalent.includes('visible category is unknown')) process.exit(8);
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
globalThis.document = { createElement: () => node() };
const list = node();
renderRegionalOverlays(scene.overlays, { querySelector: () => list });
if (list.children[0].dataset.operationalOverlayId !== 'operational-demand-pressure') process.exit(9);
if (!list.children[0]['aria-label'].includes('visible unmet-demand value')) process.exit(10);
if (!list.children[0].children.some((child) => String(child.textContent).includes('Catalog source:'))) process.exit(11);
console.log('pass');
'''


class Phase11LiveOperationalOverlayTests(unittest.TestCase):
  def test_live_overlay_catalog_binding_and_raw_metric_preservation(self):
    result = subprocess.run(
      ["node", "--input-type=module", "-e", NODE_PROBE],
      cwd=ROOT,
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_host_and_browser_contract_expose_only_visible_overlay_sources(self):
    regional = REGIONAL.read_text(encoding="utf-8")
    board = BOARD.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    for marker in (
      "operational_overlay_id",
      "PlayerObservation.monthly_unmet_demand",
      "PlayerObservation.in_flight_projects",
      "PlayerObservation.monthly_operating_margin",
      "PlayerObservation.community_trust_summary",
      "PlayerObservation.intel_gaps",
      "operationalOverlayFor",
    ):
      self.assertIn(marker, regional + board + app)
    for forbidden in (
      "CompetitiveWorldState",
      "HealthSystemState",
      "resolved_inputs",
      "effect_queue",
      "fetch(",
      "WebSocket",
      "Math.random",
    ):
      self.assertNotIn(forbidden, board + app)

  def test_changed_browser_modules_parse(self):
    for path in (BOARD, APP):
      result = subprocess.run(
        ["node", "--check", str(path)],
        capture_output=True,
        text=True,
        check=False,
      )
      self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
