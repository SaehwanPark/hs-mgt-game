import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "evaluation" / "phase11.1-full-campaign-screenshot-evidence.json"
GUI = ROOT / "gui" / "index.html"
HOST = ROOT / "src" / "gui_server.rs"
ADAPTER = ROOT / "gui" / "host-adapter.mjs"
APP = ROOT / "gui" / "app.mjs"


class FullCampaignScreenshotEvidenceTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    cls.gui = GUI.read_text(encoding="utf-8")
    cls.host = HOST.read_text(encoding="utf-8")
    cls.adapter = ADAPTER.read_text(encoding="utf-8")
    cls.app = APP.read_text(encoding="utf-8")

  def test_manifest_covers_exact_active_and_terminal_campaign_matrix(self):
    self.assertEqual(self.evidence["schema_version"], "full-campaign-screenshot-evidence-v1")
    self.assertEqual(self.evidence["status"], "complete-technical-local-browser-inspection")
    self.assertEqual(self.evidence["viewport"], {"width": 1024, "height": 768})
    self.assertEqual(
      {(record["campaign"], record["state"]) for record in self.evidence["records"]},
      {
        ("competitive-regional-v1", "active"),
        ("competitive-regional-v1", "terminal"),
        ("stabilization-v1", "active"),
        ("stabilization-v1", "terminal"),
        ("regional-affiliation-v1", "active"),
        ("regional-affiliation-v1", "terminal"),
      },
    )
    self.assertEqual(len(self.evidence["records"]), 6)

  def test_every_record_is_source_bound_and_has_safe_fallbacks(self):
    route = self.evidence["route"]
    self.assertEqual(route["schema"], "campaign-coverage-v1")
    self.assertEqual(route["source"], "src/gui_server.rs: existing loopback campaign-coverage route")
    self.assertEqual(route["adapter_source"], "gui/host-adapter.mjs: campaign coverage adapter")
    self.assertEqual(route["renderer_source"], "gui/app.mjs: shared campaign coverage renderer")
    self.assertEqual(route["surface_source"], "gui/index.html: desktop and campaign coverage regions")
    self.assertTrue((ROOT / "src" / "gui_server.rs").is_file())
    self.assertTrue((ROOT / "gui" / "host-adapter.mjs").is_file())
    self.assertTrue((ROOT / "gui" / "app.mjs").is_file())
    self.assertIn("campaign-coverage", self.host)
    self.assertIn("campaign", self.adapter.lower())
    self.assertIn("renderCampaignCoverage", self.app)
    self.assertIn('id="desktop"', self.gui)
    for record in self.evidence["records"]:
      self.assertEqual(record["inspection_status"], "inspected-local-browser")
      self.assertTrue(record["written_equivalent"])
      self.assertTrue(record["optional_audio"])
      self.assertTrue(record["host_state"])
      self.assertTrue(record["observed_content"])
      if record["state"] == "terminal":
        self.assertTrue(record["terminal_debrief"])
        self.assertTrue(any("debrief" in item.lower() for item in record["observed_content"]))
      else:
        self.assertFalse(record["terminal_debrief"])

  def test_capture_is_explicitly_ephemeral_and_not_release_or_human_approval(self):
    artifact = self.evidence["capture_artifact"]
    self.assertEqual(artifact["status"], "ephemeral-not-persisted")
    self.assertIsNone(artifact["path"])
    self.assertIsNone(artifact["hash"])
    self.assertFalse(artifact["release_eligible"])
    limits = " ".join(self.evidence["limits"]).lower()
    self.assertIn("not persisted", limits)
    self.assertIn("raster golden", limits)
    self.assertIn("human visual", limits)

  def test_authority_boundary_rejects_hidden_or_browser_owned_claims(self):
    boundary = " ".join(self.evidence["authority_boundary"]).lower()
    self.assertIn("does not simulate", boundary)
    self.assertIn("not included in commands", boundary)
    for forbidden in ("true state", "resolved input", "private rival"):
      self.assertIn(forbidden, boundary)
    self.assertNotIn("worldstate", boundary)
    self.assertNotIn("resolvedinputs", boundary)


if __name__ == "__main__":
  unittest.main()
