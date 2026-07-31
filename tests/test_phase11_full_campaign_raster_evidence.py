import hashlib
import json
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "evaluation" / "phase11.1-full-campaign-raster-evidence.json"
CAPTURE_METADATA = ROOT / "docs" / "evaluation" / "phase11.1-full-campaign-raster-capture-metadata.json"
LEDGER = ROOT / "docs" / "evaluation" / "phase11.1-campaign-coverage-ledger.json"
RELEASE_MANIFEST = ROOT / "assets" / "ASSET_RELEASE_MANIFEST.json"
HOST = ROOT / "src" / "gui_server.rs"
ADAPTER = ROOT / "gui" / "host-adapter.mjs"
APP = ROOT / "gui" / "app.mjs"
GUI = ROOT / "gui" / "index.html"


CAMPAIGNS = {
  "competitive-regional-v1": {"turns": {"active": "1/24", "terminal": "24/24"}, "native": (1004, 753)},
  "stabilization-v1": {"turns": {"active": "1/5", "terminal": "5/5"}, "native": (1009, 757)},
  "regional-affiliation-v1": {"turns": {"active": "1/6", "terminal": "6/6"}, "native": (1004, 753)},
}


def jpeg_dimensions(data):
  if not data.startswith(b"\xff\xd8"):
    raise AssertionError("artifact is not a JPEG")
  sof_markers = {
    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
  }
  offset = 2
  while offset < len(data):
    if data[offset] != 0xFF:
      offset += 1
      continue
    while offset < len(data) and data[offset] == 0xFF:
      offset += 1
    marker = data[offset]
    offset += 1
    if marker in (0xD8, 0xD9):
      continue
    if marker == 0xDA:
      break
    if offset + 2 > len(data):
      break
    segment_length = struct.unpack(">H", data[offset:offset + 2])[0]
    if marker in sof_markers:
      if offset + 7 > len(data):
        break
      height, width = struct.unpack(">HH", data[offset + 3:offset + 7])
      return width, height
    offset += segment_length
  raise AssertionError("JPEG dimensions were not found")


class FullCampaignRasterEvidenceTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    cls.capture_metadata = json.loads(CAPTURE_METADATA.read_text(encoding="utf-8"))
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

  def test_manifest_is_exact_six_state_matrix_and_not_release_eligible(self):
    self.assertEqual(
      self.evidence["schema_version"],
      "phase11.1-persisted-campaign-raster-evidence-v1",
    )
    self.assertEqual(self.evidence["status"], "complete-technical-persisted-raster-evidence")
    self.assertEqual(self.evidence["campaigns"], list(CAMPAIGNS))
    self.assertEqual(self.evidence["viewport"], {"width": 1024, "height": 768, "device_scale_factor": 1})
    self.assertEqual(self.evidence["artifact_directory"], "docs/evaluation/phase11.1-campaign-raster")
    self.assertFalse(self.evidence["release_eligible"])
    self.assertTrue(self.evidence["not_release_asset"])
    self.assertEqual(
      {(record["campaign"], record["state"]) for record in self.evidence["state_records"]},
      {(campaign, state) for campaign in CAMPAIGNS for state in ("active", "terminal")},
    )
    self.assertEqual(len(self.evidence["state_records"]), 6)

  def test_artifacts_exist_match_hashes_mime_and_exact_canvas(self):
    artifact_root = (ROOT / self.evidence["artifact_directory"]).resolve()
    expected_artifacts = {
      f"{self.evidence['artifact_directory']}/{campaign}-{state}-1024x768.jpg"
      for campaign in CAMPAIGNS
      for state in ("active", "terminal")
    }
    self.assertEqual({record["artifact"] for record in self.evidence["state_records"]}, expected_artifacts)
    self.assertEqual(
      {path.name for path in artifact_root.iterdir()},
      {Path(artifact).name for artifact in expected_artifacts},
    )
    self.assertTrue(all(path.is_file() for path in artifact_root.iterdir()))
    for record in self.evidence["state_records"]:
      artifact = (ROOT / record["artifact"]).resolve()
      self.assertTrue(artifact.is_file(), record["artifact"])
      self.assertTrue(artifact.is_relative_to(artifact_root), record["artifact"])
      self.assertNotIn("/assets/", f"/{record['artifact']}")
      self.assertNotIn("/release/", f"/{record['artifact']}")
      data = artifact.read_bytes()
      self.assertEqual(record["mime_type"], "image/jpeg")
      self.assertGreater(len(data), 0)
      self.assertEqual(data[:2], b"\xff\xd8")
      self.assertEqual(record["byte_size"], len(data))
      self.assertEqual(record["sha256"], hashlib.sha256(data).hexdigest())
      self.assertEqual((record["width"], record["height"]), (1024, 768))
      self.assertEqual(jpeg_dimensions(data), (1024, 768))

  def test_native_capture_and_host_state_metadata_are_fail_closed(self):
    self.assertEqual(
      self.evidence["native_capture_metadata"],
      "docs/evaluation/phase11.1-full-campaign-raster-capture-metadata.json",
    )
    self.assertEqual(self.capture_metadata["schema_version"], "phase11.1-native-capture-metadata-v1")
    self.assertEqual(self.capture_metadata["status"], "complete-raw-capture-provenance")
    self.assertEqual(
      {(record["campaign"], record["state"]) for record in self.capture_metadata["records"]},
      {(campaign, state) for campaign in CAMPAIGNS for state in ("active", "terminal")},
    )
    raw_records = {
      (record["campaign"], record["state"]): record
      for record in self.capture_metadata["records"]
    }
    for record in self.evidence["state_records"]:
      campaign = CAMPAIGNS[record["campaign"]]
      raw = raw_records[(record["campaign"], record["state"])]
      self.assertEqual(raw["normalized_artifact"], record["artifact"])
      self.assertEqual(raw["raw_mime_type"], "image/jpeg")
      self.assertGreater(raw["raw_byte_size"], 0)
      self.assertRegex(raw["raw_sha256"], r"^[0-9a-f]{64}$")
      self.assertEqual(
        (record["native_capture_size"]["width"], record["native_capture_size"]["height"]),
        campaign["native"],
      )
      self.assertEqual(
        (record["native_capture_size"]["width"], record["native_capture_size"]["height"]),
        (raw["native_width"], raw["native_height"]),
      )
      self.assertEqual(
        (self.evidence["viewport"]["width"] - raw["native_width"], self.evidence["viewport"]["height"] - raw["native_height"]),
        (20, 15) if raw["native_width"] == 1004 else (15, 11),
      )
      self.assertEqual(
        (record["native_capture_size"]["width"], record["native_capture_size"]["height"]),
        (
          self.evidence["canvas_rule"]["native_capture_sizes"][record["campaign"]]["width"],
          self.evidence["canvas_rule"]["native_capture_sizes"][record["campaign"]]["height"],
        ),
      )
      self.assertEqual(record["host_state"]["campaign"], record["campaign"])
      self.assertEqual(record["host_state"]["turn"], campaign["turns"][record["state"]])
      self.assertTrue(record["host_state"]["stage"])
      self.assertEqual(record["inspection_status"], "persisted-local-browser-raster")
      self.assertTrue(record["observed_content"])
      self.assertTrue(record["written_equivalent"])
      self.assertTrue(record["optional_audio"])
      self.assertEqual(record["terminal_debrief"], record["state"] == "terminal")
      if record["state"] == "terminal":
        self.assertTrue(any("debrief" in item.lower() for item in record["observed_content"]))

  def test_source_routes_and_registry_boundary_are_explicit(self):
    route = self.evidence["route"]
    self.assertEqual(route["schema"], "campaign-coverage-v1")
    self.assertEqual(route["source"], "src/gui_server.rs: existing loopback campaign-coverage route")
    self.assertEqual(route["adapter_source"], "gui/host-adapter.mjs: campaign coverage adapter")
    self.assertEqual(route["renderer_source"], "gui/app.mjs: shared campaign coverage renderer")
    self.assertEqual(route["surface_source"], "gui/index.html: desktop and campaign coverage regions")
    self.assertIn("campaign-coverage", HOST.read_text(encoding="utf-8"))
    self.assertIn("campaign", ADAPTER.read_text(encoding="utf-8").lower())
    self.assertIn("renderCampaignCoverage", APP.read_text(encoding="utf-8"))
    self.assertIn('id="desktop"', GUI.read_text(encoding="utf-8"))
    release_manifest = RELEASE_MANIFEST.read_text(encoding="utf-8")
    for record in self.evidence["state_records"]:
      self.assertNotIn(record["artifact"], release_manifest)
    self.assertEqual(
      self.ledger["full_campaign_raster_screenshot_evidence"]["capture_artifact"],
      "persisted-technical-evidence-not-release-asset",
    )

  def test_authority_boundary_and_limits_reject_overclaiming(self):
    boundary = " ".join(self.evidence["authority_boundary"]).lower()
    self.assertIn("does not simulate", boundary)
    self.assertIn("not included in commands", boundary)
    self.assertIn("actor-visible", boundary)
    for forbidden in ("worldstate", "resolvedinputs", "resolved_inputs", "true state", "private rival"):
      self.assertNotIn(forbidden, boundary)
    limits = " ".join(self.evidence["limits"]).lower()
    for marker in (
      "release assets",
      "pixel-level visual quality",
      "human visual",
      "cross-browser",
      "provenance/legal",
      "public-release",
    ):
      self.assertIn(marker, limits)


if __name__ == "__main__":
  unittest.main()
