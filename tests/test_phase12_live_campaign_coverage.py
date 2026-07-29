import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase12-live-campaign-coverage.json"

EXPECTED_SOURCE_CONTRACT = {
  "gui_route": (
    "src/gui_server.rs",
    "/api/v1/sessions/{session_id}/campaign-coverage",
  ),
  "session_identity_route": ("src/gui_server.rs", "/api/v1/sessions/{session_id}"),
  "gui_store_call": ("src/gui_server.rs", "GetCampaignCoverageRequest"),
  "gui_launch_boundary": (
    "src/gui_server.rs",
    "GUI_CAMPAIGN_COVERAGE_CAMPAIGNS",
  ),
  "host_adapter": ("gui/host-adapter.mjs", "getCampaignCoverage"),
  "launcher_campaign_set": ("gui/app.mjs", "SESSION_LAUNCH_CAMPAIGNS"),
  "campaign_fallback": ("gui/app.mjs", "loadCampaignCoverage"),
  "campaign_renderer": ("gui/app.mjs", "renderCampaignCoverage"),
  "canonical_mutation": ("gui/app.mjs", "adapter.submitTurn(command)"),
}


class Phase12LiveCampaignCoverageTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_ledger_and_source_contract_are_exact(self):
    self.assertEqual(
      self.ledger["status"],
      "complete-current-technical-browser-handoff-only",
    )
    self.assertEqual(
      self.ledger["campaigns"],
      ["stabilization-v1", "regional-affiliation-v1"],
    )
    self.assertEqual(set(self.ledger["source_contract"]), set(EXPECTED_SOURCE_CONTRACT))
    for key, (source_path, marker) in EXPECTED_SOURCE_CONTRACT.items():
      self.assertEqual(
        self.ledger["source_contract"][key],
        f"{source_path}: {marker}",
      )
      source = (ROOT / source_path).read_text(encoding="utf-8")
      self.assertIn(marker, " ".join(source.split()), key)
    self.assertEqual(
      self.ledger["findings"],
      {
        "loopback_route_uses_existing_typed_projection": True,
        "both_campaign_coverage_campaigns_are_launchable": True,
        "competitive_difficulty_and_action_path_remain_separate": True,
        "campaign_decisions_use_host_submit_turn": True,
        "existing_session_campaign_is_resolved_from_host": True,
        "rejected_campaign_decisions_do_not_advance_history": True,
        "browser_true_state_or_new_authority_added": False,
        "campaign_specific_visual_audio_quality_review": False,
        "human_accessibility_educational_or_public_release_review": False,
      },
    )

  def test_gui_surfaces_keep_campaign_and_authority_boundaries_visible(self):
    html = (ROOT / "gui" / "index.html").read_text(encoding="utf-8")
    app = (ROOT / "gui" / "app.mjs").read_text(encoding="utf-8")
    adapter = (ROOT / "gui" / "host-adapter.mjs").read_text(encoding="utf-8")
    for marker in (
      'value="stabilization-v1"',
      'value="regional-affiliation-v1"',
      'id="campaign-coverage-panel"',
    ):
      self.assertIn(marker, html)
    for marker in (
      "campaign-coverage-v1",
      "SESSION_LAUNCH_CAMPAIGNS",
      "getCampaignCoverage",
      "loadCampaignCoverage",
      "adapter.submitTurn(command)",
      "competitive-regional-v1",
    ):
      self.assertIn(marker, app + adapter)
    for forbidden in (
      "WorldState",
      "ResolvedInputs",
      "resolved_inputs",
      "effect_queue",
      "fetch(\"https://",
    ):
      self.assertNotIn(forbidden, app)

  def test_launcher_accepts_campaign_coverage_campaign_without_difficulty(self):
    script = r'''
      import { createSessionLauncher } from "./gui/app.mjs";
      const listeners = new Map();
      const nodes = new Map();
      for (const selector of [
        "#session-launch-form", "#session-start", "#session-id", "#session-load",
        "#session-launch-status", "#session-campaign", "#session-seed", "#session-difficulty",
      ]) {
        nodes.set(selector, {
          value: selector === "#session-campaign" ? "stabilization-v1"
            : selector === "#session-seed" ? "42"
              : selector === "#session-difficulty" ? "not-used" : "",
          textContent: "",
          disabled: false,
          addEventListener(type, callback) { listeners.set(`${selector}:${type}`, callback); },
        });
      }
      const calls = [];
      const adapter = {
        async startSession(options) { calls.push(options); return { session_id: "session-new", campaign: options.campaign }; },
      };
      const root = { querySelector(selector) { return nodes.get(selector) ?? null; } };
      createSessionLauncher({ adapter, root, load: async () => ({ ok: true, envelope: {} }) });
      await listeners.get("#session-launch-form:submit")({ preventDefault() {} });
      if (JSON.stringify(calls) !== JSON.stringify([{ campaign: "stabilization-v1", seed: 42 }])) process.exit(1);
      if (!nodes.get("#session-start").textContent.includes("stabilization")) process.exit(2);
      if (!nodes.get("#session-difficulty").disabled) process.exit(3);
      console.log(JSON.stringify({ calls }));
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


if __name__ == "__main__":
  unittest.main()
