import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "gui" / "metric-visualizations.mjs"
PROOF = ROOT / "gui" / "metric-visualization-proof.html"
APP = ROOT / "gui" / "app.mjs"
HTML = ROOT / "gui" / "index.html"
SNAPSHOT = ROOT / "tests" / "fixtures" / "metric_visualization_snapshot.sha256"


def run_node(script):
  return subprocess.run(
    ["node", "--input-type=module", "-e", script],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
  )


class MetricVisualizationTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.module = MODULE.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")

  def test_catalog_covers_the_bounded_visualization_slice(self):
    result = run_node(
      """
      import { METRIC_VISUALIZATION_SCHEMA, metricVisualizationFor, orderedMetricVisualizations } from './gui/metric-visualizations.mjs';
      const required = ['capacity-bar', 'delta', 'payer-mix', 'project-progress', 'sparkline', 'staffing-composition', 'trust-trend', 'uncertainty-interval'];
      const fields = ['semantic_purpose', 'precision_rule', 'uncertainty_rule', 'missingness_rule', 'exact_text_rule', 'color_independent_rule', 'large_text_rule', 'snapshot_fixture'];
      if (METRIC_VISUALIZATION_SCHEMA !== 'metric-visualization-v1') process.exit(1);
      if (JSON.stringify(orderedMetricVisualizations().map((entry) => entry.id)) !== JSON.stringify(required)) process.exit(2);
      for (const id of required) if (!fields.every((field) => metricVisualizationFor(id)[field])) process.exit(3);
      if (metricVisualizationFor('unknown').id !== 'generic-metric') process.exit(4);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_models_preserve_exact_values_missingness_and_uncertainty(self):
    result = run_node(
      """
      import { METRIC_VISUALIZATION_PROOF_FIXTURES, metricVisualizationModel } from './gui/metric-visualizations.mjs';
      const spark = metricVisualizationModel(METRIC_VISUALIZATION_PROOF_FIXTURES[0], 'sparkline');
      const interval = metricVisualizationModel(METRIC_VISUALIZATION_PROOF_FIXTURES.at(-1), 'uncertainty-interval');
      if (!spark.exact_text.includes('unavailable') || !spark.missingness.includes('missing')) process.exit(1);
      if (interval.lower !== 62 || interval.estimate !== 68 || interval.upper !== 74 || !interval.uncertainty.includes('probability')) process.exit(2);
      if (!spark.accessible_text.includes('Source: PlayerObservation.monthly_margin')) process.exit(3);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_deterministic_svg_snapshot_is_stable(self):
    expected = SNAPSHOT.read_text(encoding="utf-8").strip()
    result = run_node(
      """
      import { createHash } from 'node:crypto';
      import { METRIC_VISUALIZATION_PROOF_FIXTURES, metricVisualizationModel, orderedMetricVisualizations, renderMetricVisualizationSvg } from './gui/metric-visualizations.mjs';
      const payload = orderedMetricVisualizations().map((entry) => {
        const fixture = METRIC_VISUALIZATION_PROOF_FIXTURES.find((candidate) => candidate.visualization_kind === entry.id);
        return { id: entry.id, svg: renderMetricVisualizationSvg(fixture, entry.id), model: metricVisualizationModel(fixture, entry.id) };
      });
      console.log(createHash('sha256').update(JSON.stringify(payload)).digest('hex'));
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), expected)

  def test_proof_and_live_gui_keep_text_fallback_and_authority_boundary(self):
    for marker in ('METRIC_VISUALIZATION_PROOF_FIXTURES', 'renderMetricVisualizationSvg', 'Use large text', 'Print/export proof', 'prefers-reduced-motion', '@media print', 'Exact values', 'without color'):
      self.assertIn(marker, self.proof)
    for marker in ('renderMetricVisualizationSvg', 'metric-visualization', 'source', 'status'):
      self.assertIn(marker, self.app if marker == 'renderMetricVisualizationSvg' else self.html + self.app)
    for forbidden in ('CompetitiveWorldState', 'resolved_inputs', 'effect_queue', 'fetch(', 'WebSocket', 'Math.random'):
      self.assertNotIn(forbidden, self.module + self.proof)
    for path in (MODULE, APP):
      result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, check=False)
      self.assertEqual(result.returncode, 0, result.stderr)

  def test_missing_and_categorical_visuals_do_not_reallocate_or_score(self):
    result = run_node(
      """
      import { METRIC_VISUALIZATION_PROOF_FIXTURES, renderMetricVisualizationSvg } from './gui/metric-visualizations.mjs';
      const spark = renderMetricVisualizationSvg(METRIC_VISUALIZATION_PROOF_FIXTURES[0], 'sparkline');
      const staffing = renderMetricVisualizationSvg(METRIC_VISUALIZATION_PROOF_FIXTURES[3], 'staffing-composition');
      const trust = renderMetricVisualizationSvg(METRIC_VISUALIZATION_PROOF_FIXTURES[6], 'trust-trend');
      if ((spark.match(/class="trend-line"/g) ?? []).length !== 1 || !spark.includes('class="trend-point"')) process.exit(1);
      if (!staffing.includes('category unavailable; not redistributed') || !staffing.includes('class="missing-pattern"')) process.exit(2);
      if (!trust.includes('categorical-point point-') || trust.includes('class="trend-line"') || !trust.includes('Moderate') || !trust.includes('High')) process.exit(3);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")


if __name__ == "__main__":
  unittest.main()
