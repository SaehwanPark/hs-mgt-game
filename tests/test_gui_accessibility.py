import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "gui" / "index.html"
APP = ROOT / "gui" / "app.mjs"
README = ROOT / "gui" / "README.md"
DOC = ROOT / "docs" / "visual-audio-phase10-accessibility-v0.12.26.md"


class GuiAccessibilityTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.html = HTML.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.readme = README.read_text(encoding="utf-8")
    cls.doc = DOC.read_text(encoding="utf-8") if DOC.exists() else ""

  def test_keyboard_landmarks_and_stable_targets_exist(self):
    for marker in (
      'class="skip-link"',
      'href="#briefing-region"',
      'id="briefing-region" tabindex="-1"',
      'id="presentation-navigation"',
      'aria-label="Presentation sections"',
      'href="#action-region"',
      'href="#resolution-panel"',
      'href="#debrief-region"',
      'id="briefing-region"',
      'id="action-region"',
      'id="resolution-panel"',
      'id="debrief-region"',
    ):
      self.assertIn(marker, self.html)

  def test_status_language_is_text_and_non_color(self):
    for marker in (
      'id="status-language-legend"',
      "Stable",
      "Watch",
      "Constrained",
      "Critical",
      "Improving",
      "Uncertain",
      "Delayed",
      "Revised",
      "Reported",
      "status-pattern",
    ):
      self.assertIn(marker, self.html + self.app)
    self.assertIn("dataset.status", self.app)
    self.assertIn("aria-label", self.app)
    self.assertIn("target.focus", self.app)

  def test_text_scale_and_cue_equivalent_settings_are_functional(self):
    for marker in (
      'id="settings-text-scale"',
      'data-text-scale="large"',
      "text_scale",
      "dataset.textScale",
      "text_equivalents",
      "audio-equivalent",
      "dataset.textEquivalents",
      "localStorage",
    ):
      self.assertIn(marker, self.html + self.app)
    self.assertIn("settings_changed", self.app)

  def test_focus_and_live_region_contract_is_targeted(self):
    for marker in (
      ":focus-visible",
      "outline-offset",
      'role="status"',
      'aria-live="polite"',
    ):
      self.assertIn(marker, self.html)
    self.assertNotIn('<main class="desktop-grid" id="desktop" aria-live=', self.html)

  def test_documentation_and_no_boundary_expansion(self):
    for marker in (
      "Phase 10",
      "keyboard",
      "text scale",
      "non-color",
      "technical interface proxies",
      "human accessibility",
    ):
      self.assertIn(marker.lower(), (self.doc + self.readme).lower())
    for forbidden in (
      "fetch(",
      "WebSocket",
      "transition_competitive",
      "CompetitiveWorldState",
      "resolved_inputs",
    ):
      self.assertNotIn(forbidden, self.app)

  def test_javascript_parses(self):
    result = subprocess.run(
      ["node", "--check", str(APP)],
      capture_output=True,
      text=True,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)

  def test_settings_apply_and_persist_through_local_boundary(self):
    script = r'''
      import { createPresentationSettings } from "./gui/app.mjs";
      const listeners = new Map();
      const nodes = new Map();
      for (const selector of ["#settings-reduced-motion", "#settings-text-equivalents", "#settings-text-scale", "#settings-state"]) {
        nodes.set(selector, {
          checked: false,
          value: "standard",
          textContent: "",
          addEventListener(type, callback) { listeners.set(`${selector}:${type}`, callback); },
        });
      }
      const root = {
        documentElement: { dataset: {} },
        querySelector(selector) { return nodes.get(selector) ?? null; },
      };
      let saved = "";
      const storage = {
        getItem() { return JSON.stringify({ text_scale: "large", text_equivalents: false }); },
        setItem(_key, value) { saved = value; },
      };
      const settings = createPresentationSettings({ root, storage });
      if (settings.state.text_scale !== "large" || root.documentElement.dataset.textScale !== "large") process.exit(1);
      listeners.get("#settings-text-scale:change")({ target: { value: "standard" } });
      if (JSON.parse(saved).text_scale !== "standard") process.exit(2);
      listeners.get("#settings-text-equivalents:change")({ target: { checked: true } });
      if (root.documentElement.dataset.textEquivalents !== "true") process.exit(3);
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
  unittest.main()
