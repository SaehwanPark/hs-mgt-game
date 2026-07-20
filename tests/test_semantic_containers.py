import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "gui" / "semantic-containers.mjs"
PROOF = ROOT / "gui" / "semantic-container-proof.html"
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


class SemanticContainerTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.catalog = CATALOG.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")

  def test_all_target_containers_have_the_complete_contract(self):
    result = run_node(
      """
      import { SEMANTIC_CONTAINER_CATALOG, orderedSemanticContainers, semanticContainerFor } from './gui/semantic-containers.mjs';
      const required = ['board-packet', 'operations-ledger', 'intelligence-report', 'regulatory-letter', 'project-sheet', 'news-wire', 'executive-action-queue', 'after-action-report'];
      if (SEMANTIC_CONTAINER_CATALOG.containers.length !== required.length) process.exit(1);
      for (const id of required) {
        const entry = semanticContainerFor(id);
        for (const field of ['semantic_purpose', 'header_treatment', 'icon', 'marker_pattern', 'compact_variant', 'expanded_variant', 'aria_label', 'large_text_behavior', 'narrow_width_behavior', 'print_behavior', 'source_status_rule']) {
          if (!entry[field]) process.exit(2);
        }
      }
      const ordered = orderedSemanticContainers().map((entry) => entry.id).join(',');
      if (ordered !== [...required].sort().join(',')) process.exit(3);
      if (semanticContainerFor('unknown').id !== 'generic-container') process.exit(4);
      console.log('pass');
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_proof_and_live_gui_preserve_accessible_container_variants(self):
    for marker in ('orderedSemanticContainers', 'compact variants', 'expanded variants', 'aria-label', 'Print/export proof', 'prefers-reduced-motion', '@media print'):
      self.assertIn(marker, self.proof)
    for marker in ('semantic-container--board-packet', 'semantic-container--intelligence-report', 'semantic-container--executive-action-queue', 'data-semantic-container="project-sheet"'):
      self.assertIn(marker, self.html)
    for forbidden in ('CompetitiveWorldState', 'resolved_inputs', 'effect_queue', 'fetch(', 'WebSocket', 'Math.random'):
      self.assertNotIn(forbidden, self.catalog + self.proof)

  def test_live_gui_keeps_source_and_status_surface(self):
    for marker in ('panel-heading span', 'source', 'createStatus', 'visual-legend', 'semantic-container'):
      self.assertIn(marker, self.html if marker != 'createStatus' else self.app)
    for path in (CATALOG, APP):
      result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, check=False)
      self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
