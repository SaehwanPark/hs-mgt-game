import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "gui" / "motion-catalog.mjs"
PROOF = ROOT / "gui" / "motion-proof.html"
APP = ROOT / "gui" / "app.mjs"


def run_node(script):
  return subprocess.run(
    ["node", "--input-type=module", "-e", script],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
  )


class MotionCatalogTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.module = MODULE.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")

  def test_catalog_covers_all_motion_categories_and_requirements(self):
    result = run_node(
      """
      import { MOTION_CATALOG, MOTION_CATALOG_SCHEMA, MOTION_POLICY, motionFor, orderedMotionCatalog } from './gui/motion-catalog.mjs';
      const required = ['focus-transition', 'report-arrival', 'month-transition', 'project-progress', 'project-completion', 'new-visible-rival-action', 'status-change', 'metric-delta-reveal', 'relationship-line-change'];
      const fields = ['semantic_purpose', 'duration_ms', 'easing', 'reduced_motion_replacement', 'interruption_behavior', 'replay_behavior', 'deterministic_order', 'input_behavior', 'performance_budget_ms'];
      if (MOTION_CATALOG_SCHEMA !== 'motion-catalog-v1' || MOTION_CATALOG.entries.length !== 9) process.exit(1);
      if (JSON.stringify(orderedMotionCatalog().map((entry) => entry.id)) !== JSON.stringify(required)) process.exit(2);
      if (MOTION_POLICY.max_simultaneous_animations !== 3 || MOTION_POLICY.baseline_frame_budget_ms !== 16) process.exit(3);
      for (const id of required) if (!fields.every((field) => motionFor(id)[field])) process.exit(4);
      if (motionFor('unknown') !== null) process.exit(5);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_replay_reduced_motion_interruption_and_load_are_deterministic(self):
    result = run_node(
      """
      import { interruptMotion, motionLoadReport, replayMotionSequence } from './gui/motion-catalog.mjs';
      const events = [
        { motion_id: 'status-change', sequence: 2, batch: 0, target_id: 'b' },
        { motion_id: 'report-arrival', sequence: 1, batch: 0, target_id: 'a' },
        { motion_id: 'metric-delta-reveal', sequence: 1, batch: 1, target_id: 'metric' },
      ];
      const replay = replayMotionSequence(events);
      const reduced = replayMotionSequence(events, { reduced_motion: true });
      if (replay[0].motion_id !== 'report-arrival' || replay[1].motion_id !== 'status-change' || replay[2].duration_ms !== 260) process.exit(1);
      if (reduced.some((entry) => entry.duration_ms !== 0 || entry.easing !== 'step-end' || !entry.replacement)) process.exit(2);
      const interruption = interruptMotion('report-arrival', 'status-change');
      if (interruption.host_state_changed || !interruption.written_information_retained || interruption.replacement !== 'status-change') process.exit(3);
      const load = motionLoadReport(events);
      if (load.maximum_simultaneous !== 2 || !load.within_simultaneous_budget) process.exit(4);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_local_motion_catalog_smoke_stays_within_declared_budget(self):
    result = run_node(
      """
      import { motionLoadReport, replayMotionSequence } from './gui/motion-catalog.mjs';
      const events = Array.from({ length: 27 }, (_, index) => ({ motion_id: 'status-change', sequence: index, batch: Math.floor(index / 3), target_id: `target-${index}` }));
      const started = performance.now();
      for (let index = 0; index < 1000; index += 1) replayMotionSequence(events);
      const elapsed = performance.now() - started;
      if (!motionLoadReport(events).within_simultaneous_budget || elapsed > 1000) process.exit(1);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_proof_is_static_reduced_motion_and_authority_safe(self):
    for marker in ('MOTION_CATALOG', 'replayMotionSequence', 'Show reduced-motion replacements', 'Show interruption result', 'Print/export proof', 'prefers-reduced-motion', '@media print', 'maximum 3 simultaneous', 'host state changed'):
      self.assertIn(marker, self.proof)
    for forbidden in ('CompetitiveWorldState', 'resolved_inputs', 'effect_queue', 'fetch(', 'WebSocket', 'Math.random', 'requestAnimationFrame', 'setTimeout'):
      self.assertNotIn(forbidden, self.module + self.proof)
    self.assertIn('prefers-reduced-motion', self.app)
    for path in (MODULE, APP):
      result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, check=False)
      self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
