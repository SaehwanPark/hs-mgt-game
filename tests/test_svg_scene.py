import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "gui" / "scene.mjs"
PROOF = ROOT / "gui" / "svg-proof.html"
README = ROOT / "gui" / "README.md"
SNAPSHOT_HASH = "d1732b58703acebdeee60fcea7a8503eacae229a353785da2ca860877e56e3b5"


def run_node(script):
  return subprocess.run(
    ["node", "--input-type=module", "-e", script],
    cwd=ROOT,
    capture_output=True,
    text=True,
    check=False,
  )


class SvgSceneTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.scene = SCENE.read_text(encoding="utf-8")
    cls.proof = PROOF.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")

  def test_fixture_output_is_deterministic_and_snapshot_stable(self):
    result = run_node(
      """
      import { createHash } from "node:crypto";
      import { renderRegionalSvg, SVG_SCENE_FIXTURE } from "./gui/scene.mjs";
      const first = renderRegionalSvg(SVG_SCENE_FIXTURE);
      const second = renderRegionalSvg(SVG_SCENE_FIXTURE);
      if (first !== second) process.exit(1);
      console.log(createHash("sha256").update(first).digest("hex"));
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), SNAPSHOT_HASH)

  def test_svg_has_keyboard_text_uncertainty_and_unknown_fallbacks(self):
    result = run_node(
      """
      import { renderRegionalSvg, SVG_SCENE_FIXTURE } from "./gui/scene.mjs";
      const standard = renderRegionalSvg(SVG_SCENE_FIXTURE);
      const reduced = renderRegionalSvg(SVG_SCENE_FIXTURE, { reducedMotion: true });
      for (const marker of [
        'role="button"', 'tabindex="0"', 'data-entity-id="riverside"',
        'data-facility-id="riverside-general"', 'Unlisted institution',
        'Institution', 'Uncertain', 'stroke-dasharray="7 5"',
        'data-motion="standard"',
      ]) if (!standard.includes(marker)) process.exit(2);
      if (!reduced.includes('data-motion="reduced"') || reduced.includes('<animate')) process.exit(3);
      console.log("pass");
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_interactive_entity_and_facility_controls_are_not_nested(self):
    result = run_node(
      """
      import { renderRegionalSvg, SVG_SCENE_FIXTURE } from "./gui/scene.mjs";
      const svg = renderRegionalSvg(SVG_SCENE_FIXTURE);
      let depth = 0;
      for (const match of svg.matchAll(/<\\/?a\\b[^>]*>/g)) {
        if (match[0].startsWith("</")) depth -= 1;
        else if (depth !== 0) process.exit(1);
        else depth += 1;
      }
      if (depth !== 0) process.exit(2);
      console.log("pass");
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout.strip(), "pass")

  def test_render_time_meets_fixture_target(self):
    result = run_node(
      """
      import { performance } from "node:perf_hooks";
      import { renderRegionalSvg, SVG_SCENE_FIXTURE } from "./gui/scene.mjs";
      const start = performance.now();
      for (let index = 0; index < 500; index += 1) renderRegionalSvg(SVG_SCENE_FIXTURE);
      console.log(performance.now() - start);
      """
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertLess(float(result.stdout.strip()), 1000.0)

  def test_scene_and_proof_are_presentation_only(self):
    for marker in ("normalizeScene", "renderRegionalSvg", "SVG_SCENE_FIXTURE", "data-motion", "status-uncertain"):
      self.assertIn(marker, self.scene)
    for marker in ("data-select", "keydown", "aria-label", "reduced-motion", "scene.mjs"):
      self.assertIn(marker, self.proof)
    for forbidden in ("CompetitiveWorldState", "resolved_inputs", "effect_queue", "private_rival", "transition_competitive", "fetch(", "WebSocket"):
      self.assertNotIn(forbidden, self.scene + self.proof)
    self.assertIn("fixture-only", self.readme)


if __name__ == "__main__":
  unittest.main()
