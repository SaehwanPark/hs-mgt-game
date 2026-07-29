import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase13.2-low-distraction-mode.json"
HTML = ROOT / "gui" / "index.html"
APP = ROOT / "gui" / "app.mjs"
GUIDE = ROOT / "docs" / "guides" / "gui-how-to-play.md"


class Phase132LowDistractionModeTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.html = HTML.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")
    cls.guide = GUIDE.read_text(encoding="utf-8")

  def test_source_contract_markers_exist(self):
    self.assertEqual(self.ledger["schema_version"], "phase13.2-low-distraction-mode-v1")
    self.assertEqual(self.ledger["status"], "complete-local-presentation-mode-only")
    for source_ref in self.ledger["source_contract"].values():
      source_path, marker = source_ref.split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), source_ref)
      self.assertIn(marker, path.read_text(encoding="utf-8"), source_ref)

  def test_mode_contract_and_limits_are_explicit(self):
    for marker in (
      'id="settings-low-distraction"',
      'data-low-distraction="true"',
      "low_distraction",
      "applyLowDistractionAudio",
      "audio.setMuted?.(true)",
      "audio.setReducedNotifications?.(true)",
      "**Low-distraction mode**",
    ):
      self.assertIn(marker, self.html + self.app + self.guide)
    limits = " ".join(self.ledger["limits"])
    for marker in ("universal accessibility", "educational usability", "not a new host game mode"):
      self.assertIn(marker, limits)

  def test_mode_forces_and_restores_local_preferences(self):
    script = r'''
      import { createPresentationSettings } from "./gui/app.mjs";
      const listeners = new Map();
      const nodes = new Map();
      for (const selector of [
        "#settings-low-distraction",
        "#settings-reduced-motion",
        "#settings-text-equivalents",
        "#settings-text-scale",
        "#settings-state",
      ]) {
        nodes.set(selector, {
          checked: false,
          value: "standard",
          textContent: "",
          disabled: false,
          addEventListener(type, callback) { listeners.set(`${selector}:${type}`, callback); },
        });
      }
      const audioState = { muted: false, reducedNotifications: false };
      const audio = {
        state() { return { ...audioState }; },
        setMuted(value) { audioState.muted = value; },
        setReducedNotifications(value) { audioState.reducedNotifications = value; },
      };
      const root = {
        documentElement: { dataset: {} },
        querySelector(selector) { return nodes.get(selector) ?? null; },
        querySelectorAll() { return []; },
      };
      let saved = "";
      const storage = {
        getItem() { return JSON.stringify({ reduced_motion: false, text_equivalents: false, text_scale: "standard" }); },
        setItem(_key, value) { saved = value; },
      };
      const settings = createPresentationSettings({ root, storage, audio });
      listeners.get("#settings-low-distraction:change")({ target: { checked: true } });
      if (!settings.state.low_distraction || root.documentElement.dataset.lowDistraction !== "true") process.exit(1);
      if (root.documentElement.dataset.textScale !== "large" || root.documentElement.dataset.textEquivalents !== "true") process.exit(2);
      if (!audioState.muted || !audioState.reducedNotifications) process.exit(3);
      if (!JSON.parse(saved).low_distraction) process.exit(4);
      listeners.get("#settings-low-distraction:change")({ target: { checked: false } });
      if (settings.state.low_distraction || root.documentElement.dataset.lowDistraction !== "false") process.exit(5);
      if (root.documentElement.dataset.textScale !== "standard" || root.documentElement.dataset.textEquivalents !== "false") process.exit(6);
      if (audioState.muted || audioState.reducedNotifications) process.exit(7);
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
