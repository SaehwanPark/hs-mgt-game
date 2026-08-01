import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase11.1-campaign-coverage-ledger.json"
VISUAL_REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"
AUDIO_REGISTRY = ROOT / "assets" / "registry" / "audio-assets.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"
HTML = ROOT / "gui" / "index.html"
RESOLUTION = ROOT / "src" / "mcp" / "resolution.rs"
CAMPAIGN_COVERAGE = ROOT / "src" / "mcp" / "campaign_coverage.rs"
HISTORY_TEST = ROOT / "tests" / "test_phase11_live_history.py"
DEBRIEF_TEST = ROOT / "tests" / "test_phase11_live_debrief.py"
CHECKPOINT_TEST = ROOT / "tests" / "test_phase11_live_checkpoint.py"
REPLAY_TEST = ROOT / "tests" / "test_phase11_live_replay.py"
ASSET_REGISTRY_TEST = ROOT / "tests" / "test_asset_registry.py"
ASSET_VALIDATOR = ROOT / "scripts" / "validate_assets.py"
ASSET_RELEASE = ROOT / "scripts" / "verify_asset_release.py"
ASSET_SECURITY = ROOT / "scripts" / "validate_asset_security.py"
ASSET_CREDITS = ROOT / "scripts" / "generate_asset_credits.py"
MCP_SERVER = ROOT / "src" / "mcp" / "server.rs"


NODE_PROBE = r'''
globalThis.fetch = () => { throw new Error("network blocked"); };
globalThis.WebSocket = class { constructor() { throw new Error("network blocked"); } };
const [facilities, overlays, actors, markers, cues, music, availability, audio] = await Promise.all([
  import("./gui/facility-components.mjs"),
  import("./gui/operational-overlays.mjs"),
  import("./gui/actor-families.mjs"),
  import("./gui/map-event-markers.mjs"),
  import("./gui/audio-cue-contract.mjs"),
  import("./gui/music-stem-contract.mjs"),
  import("./gui/asset-availability.mjs"),
  import("./gui/audio.mjs"),
]);
const unknownAsset = availability.assetPresentationFor({
  id: "unknown-asset",
  label: "Unknown asset",
  fallback: { id: "generic-asset", label: "Asset", equivalent: "Asset unavailable" },
}, "unknown");
const unknownFacility = facilities.facilityPresentationFor("general-hospital-base", "unknown");
const unknownFacilityComponent = facilities.facilityComponentFor("unknown");
const legacyEventCueFixtures = [
  { steps: ["Project complete was reported"] },
  { observation: { workforce_trust: "Staffing constraint reported" } },
  { before: { observation: { operations: { margin: 0 } } }, after: { observation: { operations: { margin: -1 } } } },
  { before: { observation: { operations: { margin: -1 } } }, after: { observation: { operations: { margin: 0 } } } },
  { steps: ["Payer decision was reported"] },
  { steps: ["Regulatory policy decision was reported"] },
  { steps: ["Public rival expansion was observed"] },
  { steps: ["Affiliation milestone was committed"] },
];
const musicClassifierFixtures = [
  { stage: "menu" },
  { done: true },
  { observation: { policy_bullets: ["Regulatory review letter reported"] } },
  { observation: { market_bullets: ["Affiliation partner negotiation reported"] } },
  { observation: { market_bullets: ["Public rival expansion reported"] } },
  { observation: { operations: { margin: -1, unmet_demand: 0 } } },
  { observation: { operations: { margin: 10, unmet_demand: 0 }, cash_runway_signal: "adequate", workforce_trust: "stable", in_flight_projects: "none" } },
];
console.log(JSON.stringify({
  facilities: Object.keys(facilities.FACILITY_COMPONENTS),
  facility_assets: Object.entries(facilities.FACILITY_COMPONENTS).map(([key, entry]) => ({
    key,
    id: entry.id,
    source_path: entry.source_path ?? null,
    release_path: entry.release_path ?? null,
  })),
  operational_overlays: overlays.OPERATIONAL_OVERLAY_SET.map((entry) => entry.id),
  actor_families: actors.ACTOR_FAMILIES.map((entry) => entry.id),
  event_markers: markers.EVENT_MARKER_SET.map((entry) => entry.id),
  event_cues: cues.AUDIO_CUE_CONTRACT.entries.map((entry) => entry.id),
  event_channel_cues: cues.AUDIO_CUE_CONTRACT.entries
    .filter((entry) => entry.channel === "event")
    .map((entry) => entry.id),
  event_cue_contract: cues.AUDIO_CUE_CONTRACT.entries
    .filter((entry) => entry.channel === "event")
    .map((entry) => [entry.id, entry.visible_trigger_source, entry.text_equivalent, entry.cues_only]),
  legacy_event_cues: [...new Set(legacyEventCueFixtures.map((fixture) => audio.visibleEventCues(fixture)).flat())],
  music_states: music.MUSIC_STEM_CONTRACT.entries.map((entry) => entry.id),
  music_state_contract: music.MUSIC_STEM_CONTRACT.entries.map((entry) => [
    entry.id,
    entry.visible_trigger_source,
    entry.text_equivalent,
    entry.fallback,
    entry.stem_order,
  ]),
  music_classifier_states: musicClassifierFixtures.map((fixture) => music.classifyVisibleMusicState(fixture)),
  semantics: {
    facilities: Object.values(facilities.FACILITY_COMPONENTS).map((entry) => [entry.id, entry.source, entry.equivalent]),
    operational_overlays: overlays.OPERATIONAL_OVERLAY_SET.map((entry) => [entry.id, entry.visible_source, entry.text_equivalent]),
    actor_families: actors.ACTOR_FAMILIES.map((entry) => [entry.id, entry.source, entry.equivalent]),
    event_markers: markers.EVENT_MARKER_SET.map((entry) => [entry.id, entry.visible_source, entry.text_equivalent]),
    event_cues: cues.AUDIO_CUE_CONTRACT.entries.map((entry) => [entry.id, entry.visible_trigger_source, entry.text_equivalent]),
    music_states: music.MUSIC_STEM_CONTRACT.entries.map((entry) => [entry.id, entry.visible_trigger_source, entry.text_equivalent, entry.fallback]),
  },
  fallbacks: {
    facility_unknown: facilities.facilityComponentFor("unknown").id,
    actor_family_unknown: actors.actorFamilyFor("unknown").id,
    operational_overlay_unknown: overlays.operationalOverlayFor("unknown").id,
    event_marker_unknown: markers.eventMarkerFor("unknown").id,
    asset_unknown_display_mode: unknownAsset.display_mode,
    audio_cue_unknown: cues.audioCueContractFor("unknown"),
    music_state_unknown: music.musicStateFor("unknown"),
  },
  catalog_fallbacks: {
    facilities: facilities.facilityComponentFor("unknown").id,
    operational_overlays: overlays.operationalOverlayFor("unknown").id,
    actor_families: actors.actorFamilyFor("unknown").id,
    event_markers: markers.eventMarkerFor("unknown").id,
    event_cues: cues.audioCueContractFor("unknown"),
    music_states: music.musicStateFor("unknown"),
  },
  fallback_descriptors: {
    generic_facility_component: {
      id: unknownFacilityComponent.id,
      label: unknownFacilityComponent.label,
      source: unknownFacilityComponent.source,
      equivalent: unknownFacilityComponent.equivalent,
    },
    facility: {
      rendered_id: unknownFacility.rendered_id,
      rendered_label: unknownFacility.rendered_label,
      source: unknownFacility.source,
      equivalent: unknownFacility.equivalent,
      release_path: unknownFacility.release_path,
      fallback_reason: unknownFacility.fallback_reason,
    },
    actor_family: {
      id: actors.actorFamilyFor("unknown").id,
      label: actors.actorFamilyFor("unknown").label,
      source: actors.actorFamilyFor("unknown").source,
      equivalent: actors.actorFamilyFor("unknown").equivalent,
    },
    operational_overlay: {
      id: overlays.operationalOverlayFor("unknown").id,
      label: overlays.operationalOverlayFor("unknown").label,
      visible_source: overlays.operationalOverlayFor("unknown").visible_source,
      text_equivalent: overlays.operationalOverlayFor("unknown").text_equivalent,
    },
    event_marker: {
      id: markers.eventMarkerFor("unknown").id,
      label: markers.eventMarkerFor("unknown").label,
      visible_source: markers.eventMarkerFor("unknown").visible_source,
      text_equivalent: markers.eventMarkerFor("unknown").text_equivalent,
    },
    asset: {
      rendered_id: unknownAsset.rendered_id,
      rendered_label: unknownAsset.rendered_label,
      source: unknownAsset.source,
      equivalent: unknownAsset.equivalent,
      release_path: unknownAsset.release_path,
      fallback_reason: unknownAsset.fallback_reason,
    },
  },
}, null, 0));
'''

CATALOG_MODULES = {
  "gui/facility-components.mjs", "gui/operational-overlays.mjs", "gui/actor-families.mjs",
  "gui/map-event-markers.mjs", "gui/audio-cue-contract.mjs", "gui/music-stem-contract.mjs",
}
IMPORT_PATTERN = re.compile(r'''(?:from\s+|import\(\s*)["'](\.?\.?/[^"']+\.mjs)["']''')
FORBIDDEN_AUTHORITY_MARKERS = (
  "fetch(", "WebSocket", "CompetitiveWorldState", "HealthSystemState",
  "resolved_inputs", "effect_queue", "transition_competitive",
)


class Phase11CampaignCoverageTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.registry = json.loads(VISUAL_REGISTRY.read_text(encoding="utf-8"))
    cls.audio_registry = json.loads(AUDIO_REGISTRY.read_text(encoding="utf-8"))
    cls.resolution = RESOLUTION.read_text(encoding="utf-8")
    cls.campaign_coverage = CAMPAIGN_COVERAGE.read_text(encoding="utf-8")
    cls.html = HTML.read_text(encoding="utf-8")
    cls.app = (ROOT / "gui" / "app.mjs").read_text(encoding="utf-8")
    cls.adapter = (ROOT / "gui" / "host-adapter.mjs").read_text(encoding="utf-8")
    cls.server = (ROOT / "src" / "gui_server.rs").read_text(encoding="utf-8")
    cls.mcp_server = MCP_SERVER.read_text(encoding="utf-8")
    cls.session = (ROOT / "src" / "mcp" / "session.rs").read_text(encoding="utf-8")
    cls.persistence = (ROOT / "src" / "mcp" / "persistence.rs").read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    cls.phase11_1 = roadmap.split("## Milestone 11.1:", 1)[1].split("## Milestone 11.2:", 1)[0]
    result = subprocess.run(
      ["node", "--input-type=module", "-e", NODE_PROBE],
      cwd=ROOT,
      check=True,
      capture_output=True,
      text=True,
    )
    cls.live = json.loads(result.stdout)
    source_targets = []
    for catalog_name, catalog in cls.ledger["catalogs"].items():
      source_path, export_path = catalog["source"].split(": ", 1)
      source_targets.append({
        "catalog": catalog_name,
        "module": f"./{source_path}",
        "property_path": export_path.split("."),
      })
    source_probe = f'''
globalThis.fetch = () => {{ throw new Error("network blocked"); }};
globalThis.WebSocket = class {{ constructor() {{ throw new Error("network blocked"); }} }};
const targets = {json.dumps(source_targets)};
const resolved = {{}};
for (const target of targets) {{
  const module = await import(target.module);
  let value = module;
  for (const property of target.property_path) value = value?.[property];
  if (Array.isArray(value)) resolved[target.catalog] = value.map((entry) => typeof entry === "string" ? entry : entry?.id);
  else if (value && typeof value === "object") resolved[target.catalog] = Object.keys(value);
  else resolved[target.catalog] = value;
}}
console.log(JSON.stringify(resolved));
'''
    source_result = subprocess.run(
      ["node", "--input-type=module", "-e", source_probe],
      cwd=ROOT,
      check=True,
      capture_output=True,
      text=True,
    )
    cls.source_exports = json.loads(source_result.stdout)

  def test_ledger_shape_and_catalog_ids_match_live_modules(self):
    self.assertEqual(
      set(self.ledger),
      {"schema_version", "status", "campaign", "scope", "catalogs", "facility_asset_coverage", "facility_placement_use_coverage", "asset_registry_coverage", "screenshot_coverage", "full_campaign_screenshot_inspection", "full_campaign_raster_screenshot_evidence", "event_cue_coverage", "debrief_view_coverage", "debrief_visual_review_packet", "checkpoint_view_coverage", "durable_checkpoint_coverage", "full_campaign_checkpoint_continuity", "full_stabilization_checkpoint_continuity", "full_affiliation_checkpoint_continuity", "cross_campaign_checkpoint_identity", "checkpoint_discovery", "checkpoint_reference_transfer", "checkpoint_artifact_download", "full_campaign_audio_state_coverage", "full_campaign_replay_continuity", "full_campaign_browser_coverage_rendering", "full_campaign_coverage_transport_continuity", "durable_stabilization_checkpoint_coverage", "durable_affiliation_checkpoint_coverage", "autosave_coverage", "campaign_coverage_read_coverage", "replay_view_coverage", "music_state_coverage", "history_view_coverage", "browser_refresh_coverage", "continuity", "fallbacks", "open_limits"},
    )
    self.assertEqual(self.ledger["schema_version"], "competitive-campaign-coverage-ledger-v1")
    self.assertEqual(self.ledger["status"], "bounded-technical-ledger")
    self.assertEqual(self.ledger["campaign"], "competitive-regional-v1")
    self.assertEqual(
      set(self.ledger["catalogs"]),
      {"facilities", "operational_overlays", "actor_families", "event_markers", "event_cues", "music_states"},
    )
    for catalog_name, catalog in self.ledger["catalogs"].items():
      self.assertEqual(catalog["ids"], self.live[catalog_name])
      self.assertEqual(len(catalog["ids"]), len(set(catalog["ids"])))
      self.assertIsInstance(catalog["source"], str)
      self.assertTrue(catalog["source"])
      source_path, export_name = catalog["source"].split(": ", 1)
      self.assertTrue((ROOT / source_path).is_file())
      self.assertEqual(self.source_exports[catalog_name], catalog["ids"], catalog["source"])

  def test_asset_registry_coverage_matches_current_validated_registries(self):
    coverage = self.ledger["asset_registry_coverage"]
    visual_entries = self.registry["entries"]
    audio_entries = self.audio_registry["entries"]
    all_entries = visual_entries + audio_entries
    self.assertEqual(coverage["status"], "complete-current-registries")
    self.assertEqual(coverage["schema"], "asset-registry-v1")
    self.assertEqual(
      coverage["entry_counts"],
      {"visual": len(visual_entries), "audio": len(audio_entries), "total": len(all_entries)},
    )
    self.assertEqual(
      coverage["entry_counts"],
      {"visual": 38, "audio": 7, "total": 45},
    )
    for registry in (self.registry, self.audio_registry):
      self.assertEqual(registry["schema_version"], "asset-registry-v1")
      ids = [entry["id"] for entry in registry["entries"]]
      self.assertEqual(len(ids), len(set(ids)))
      self.assertTrue(all(entry["approval_status"] == "approved" for entry in registry["entries"]))
    release_count = sum(bool(entry.get("release_path")) for entry in all_entries)
    self.assertEqual(release_count, coverage["release_boundary"]["file_backed_release_entries"])
    self.assertEqual(
      len(all_entries) - release_count,
      coverage["release_boundary"]["runtime_or_catalog_entries_with_null_release_paths"],
    )
    source = "".join(
      path.read_text(encoding="utf-8")
      for path in (
        ASSET_REGISTRY_TEST,
        ASSET_VALIDATOR,
        ASSET_RELEASE,
        ASSET_SECURITY,
        ASSET_CREDITS,
      )
    )
    for marker in (
      "test_repository_registries_and_credits_are_current",
      "validate(ROOT)",
      "check_manifest",
      "render_notices",
    ):
      self.assertIn(marker, source)
    self.assertIn("null release paths", coverage["release_boundary"]["rule"])

  def test_screenshot_coverage_matches_current_supported_surface(self):
    coverage = self.ledger["screenshot_coverage"]
    self.assertEqual(coverage["status"], "complete-current-supported-surface")
    self.assertEqual(coverage["schema"], "current-gui-screenshot-surface-v1")
    self.assertGreaterEqual(len(coverage["surface_sources"]), 5)
    source_text = {
      "gui/index.html": self.html,
      "gui/app.mjs": self.app,
      "gui/regional-board.mjs": (ROOT / "gui" / "regional-board.mjs").read_text(encoding="utf-8"),
    }
    for surface in coverage["surface_sources"]:
      source_path, marker = surface["source"].split(": ", 1)
      path = ROOT / source_path
      self.assertTrue(path.is_file(), surface["source"])
      content = source_text.get(source_path, path.read_text(encoding="utf-8"))
      self.assertIn(marker, content, surface["source"])
      self.assertTrue(surface["visible_regions"])
    snapshot_path, snapshot_marker = coverage["deterministic_evidence"]["svg_snapshot"].split(": ", 1)
    self.assertTrue((ROOT / snapshot_path).is_file())
    self.assertIn(snapshot_marker, (ROOT / snapshot_path).read_text(encoding="utf-8"))
    for test_path in (
      coverage["deterministic_evidence"]["structural_gui"]
      + coverage["deterministic_evidence"]["live_handoff"]
    ):
      self.assertTrue((ROOT / test_path).is_file(), test_path)
    playtest_path, playtest_marker = coverage["deterministic_evidence"]["playtest_surface"].split(": ", 1)
    self.assertTrue((ROOT / playtest_path).is_file())
    self.assertIn(playtest_marker, (ROOT / playtest_path).read_text(encoding="utf-8"))
    browser = coverage["browser_smoke"]
    self.assertEqual(browser["status"], "inspected-local-only")
    self.assertEqual(browser["route"], "http://127.0.0.1:7878/")
    self.assertEqual(browser["action"], "Start competitive session")
    self.assertIn("not persisted", browser["capture_policy"])
    self.assertIn("pixel-level visual quality", " ".join(coverage["limits"]))

  def test_current_operational_overlay_bindings_cover_the_registered_catalog(self):
    coverage = self.ledger["catalogs"]["operational_overlays"]
    self.assertEqual(coverage["status"], "complete")
    self.assertEqual(
      coverage["host_projection_source"],
      "src/mcp/regional_world.rs: operational_overlays",
    )
    self.assertEqual(set(coverage["binding_conditions"]), set(coverage["ids"]))
    self.assertTrue(all(value for value in coverage["binding_conditions"].values()))
    self.assertTrue(coverage["evidence"])

  def test_file_backed_facility_assets_cover_the_live_catalog_and_registry(self):
    coverage = self.ledger["facility_asset_coverage"]
    self.assertEqual(coverage["status"], "complete")
    self.assertEqual(coverage["registry_id_prefix"], "visual.facility.")
    self.assertEqual(coverage["fallback_id"], "generic-facility")
    for component in self.live["facility_assets"]:
      self.assertEqual(component["key"], component["id"])

    file_backed = [entry for entry in self.live["facility_assets"] if entry["id"] != coverage["fallback_id"]]
    self.assertEqual(
      [entry["id"] for entry in file_backed],
      coverage["file_backed_ids"],
    )
    self.assertEqual(len(file_backed), len(set(coverage["file_backed_ids"])))
    registry_facility_ids = sorted(
      entry["id"].removeprefix(coverage["registry_id_prefix"])
      for entry in self.registry["entries"]
      if entry["id"].startswith(coverage["registry_id_prefix"])
    )
    self.assertEqual(registry_facility_ids, sorted(coverage["file_backed_ids"]))

    for component in file_backed:
      self.assertIsInstance(component["source_path"], str)
      self.assertIsInstance(component["release_path"], str)
      self.assertEqual(
        component["source_path"],
        f"assets/source/visual/facilities/{component['id']}.svg",
      )
      self.assertEqual(
        component["release_path"],
        f"assets/release/visual/svg/{component['id']}.svg",
      )
      source_path = ROOT / component["source_path"]
      release_path = ROOT / component["release_path"]
      self.assertTrue(source_path.is_file(), component["id"])
      self.assertTrue(release_path.is_file(), component["id"])
      registry_id = f"{coverage['registry_id_prefix']}{component['id']}"
      matches = [entry for entry in self.registry["entries"] if entry["id"] == registry_id]
      self.assertEqual(len(matches), 1, registry_id)
      entry = matches[0]
      self.assertEqual(entry["semantic_role"], "facility")
      self.assertEqual(entry["source_path"], component["source_path"])
      self.assertEqual(entry["release_path"], component["release_path"])
      self.assertEqual(entry["approval_status"], "approved")
      self.assertEqual(entry["original_hash"], f"sha256:{hashlib.sha256(source_path.read_bytes()).hexdigest()}")
      self.assertEqual(entry["release_hash"], f"sha256:{hashlib.sha256(release_path.read_bytes()).hexdigest()}")

    fallback = next(entry for entry in self.live["facility_assets"] if entry["id"] == coverage["fallback_id"])
    self.assertIsNone(fallback["source_path"])
    self.assertIsNone(fallback["release_path"])

  def test_facility_placement_use_coverage_is_host_bound_for_the_full_competitive_loop(self):
    coverage = self.ledger["facility_placement_use_coverage"]
    self.assertEqual(coverage["status"], "complete-competitive-24-month-host-read")
    self.assertEqual(coverage["schema"], "competitive-regional-world-v1")
    self.assertEqual(coverage["host_source"], "src/mcp/regional_world.rs: player_facilities")
    self.assertEqual(
      coverage["test_source"],
      "src/mcp/session.rs: fn regional_world_facility_projection_covers_all_competitive_months",
    )
    self.assertEqual(
      coverage["facility_component_ids"],
      [
        "general-hospital-base",
        "ambulatory-center",
        "emergency-department",
        "specialty-center",
      ],
    )
    self.assertEqual(
      coverage["capacity_metric_labels"],
      [
        "Staffed beds",
        "Outpatient capacity",
        "Emergency",
        "ICU",
        "Obstetrics",
        "Psychiatric",
        "Cardiology",
        "Oncology",
        "Infusion",
        "Neurology",
        "ASC",
      ],
    )
    self.assertTrue(coverage["evidence"])
    self.assertTrue(any("24" in item for item in coverage["evidence"]))
    self.assertTrue(any("private" in item.lower() for item in coverage["evidence"]))

  def test_event_cue_catalog_matches_visible_projection_and_fallback(self):
    coverage = self.ledger["event_cue_coverage"]
    expected = coverage["ids"]
    self.assertEqual(coverage["status"], "complete")
    self.assertEqual(coverage["host_projection_source"], "src/mcp/resolution.rs: visible_event_cue_ids")
    self.assertEqual(coverage["browser_fallback_source"], "gui/audio.mjs: visibleEventCues")
    self.assertEqual(self.live["event_channel_cues"], expected)
    event_contract_ids = [entry[0] for entry in self.live["event_cue_contract"]]
    self.assertEqual(event_contract_ids, expected)
    self.assertEqual(self.live["legacy_event_cues"], expected)
    self.assertEqual(len(expected), len(set(expected)))
    for cue_id, source, equivalent, cues_only in self.live["event_cue_contract"]:
      self.assertIn(cue_id, self.live["event_cues"])
      self.assertTrue(source)
      self.assertTrue(equivalent)
      self.assertTrue(cues_only)
      self.assertIn(f'"{cue_id}"', self.resolution)
    self.assertIn("audio_cue_ids", self.resolution)
    self.assertIn("visible_event_cue_ids", self.resolution)

  def test_music_state_catalog_matches_host_and_browser_projections(self):
    coverage = self.ledger["music_state_coverage"]
    self.assertEqual(coverage["status"], "complete")
    self.assertEqual(coverage["host_projection_source"], "src/mcp/resolution.rs: visible_music_state_id")
    self.assertEqual(coverage["browser_classifier_source"], "gui/music-stem-contract.mjs: classifyVisibleMusicState")
    self.assertEqual(self.live["music_states"], coverage["ids"])
    self.assertEqual(
      [entry[0] for entry in self.live["music_state_contract"]],
      coverage["ids"],
    )
    self.assertEqual(
      self.live["music_classifier_states"],
      ["menu", "debrief", "regulatory_scrutiny", "affiliation_negotiation", "competitive_escalation", "pressure", "stable_operations"],
    )
    self.assertEqual(set(coverage["host_ids"]) | set(coverage["browser_only_ids"]), set(coverage["ids"]))
    self.assertEqual(coverage["browser_only_ids"], ["menu"])
    for state_id, source, equivalent, fallback, stem_order in self.live["music_state_contract"]:
      self.assertTrue(source)
      self.assertTrue(equivalent)
      self.assertTrue(fallback)
      self.assertEqual(stem_order, ["base_pulse", "institutional_motif", "pressure_layer", "policy_layer", "transition_cadence"])
      if state_id in coverage["host_ids"]:
        self.assertIn(f'"{state_id}"', self.resolution)
    self.assertIn("visible_music_state_id", self.resolution)

  def test_history_view_coverage_matches_the_live_read_only_handoff(self):
    coverage = self.ledger["history_view_coverage"]
    history_test = HISTORY_TEST.read_text(encoding="utf-8")
    self.assertEqual(coverage["status"], "complete")
    self.assertEqual(coverage["host_schema"], "competitive-history-v1")
    self.assertEqual(coverage["row_contract"], ["turn", "state_hash"])
    for marker in (
      "competitive-history-v1",
      "GetHistoryRequest",
      "get_history",
      "get_competitive_history",
      "unsupported_gui_campaign_history",
      "createHistoryClient",
      "validateHistoryEnvelope",
      "renderHistoryEnvelope",
      "history_adapter_missing",
      "history_adapter_error",
      "state hash: hash-1",
    ):
      self.assertIn(marker, history_test + self.app + self.adapter + self.server + self.session)
    self.assertIn("get_history(GetHistoryRequest {", self.session)
    self.assertIn("session_id: request.session_id", self.session)
    self.assertNotIn("submit_turn", history_test.split("def test_live_history_read", 1)[0])
    for forbidden in ("transition_competitive", "resolved_inputs", "effect_queue", "CompetitiveWorldState", "WebSocket"):
      self.assertNotIn(forbidden, self.app + self.adapter + self.server)

  def test_debrief_view_coverage_matches_the_live_terminal_handoff(self):
    coverage = self.ledger["debrief_view_coverage"]
    debrief_test = DEBRIEF_TEST.read_text(encoding="utf-8")
    self.assertEqual(coverage["status"], "complete")
    self.assertEqual(coverage["schema"], "competitive-end-session-v1")
    self.assertEqual(coverage["history_row_contract"], ["turn", "command", "state_hash"])
    self.assertEqual(
      coverage["replay_contract"],
      ["seed", "transition_count", "latest_state_hash"],
    )
    for marker in (
      "competitive-end-session-v1",
      "renderEndSessionEnvelope",
      "validateEndSessionEnvelope",
      "endHostSession",
      "final history and debrief",
      'id="session-end"',
      "/api/v1/sessions/{session_id}/end",
      "EndSessionEnvelope",
      "latest_state_hash",
    ):
      self.assertIn(marker, debrief_test + self.app + self.adapter + self.server)
    for forbidden in (
      "CompetitiveWorldState",
      "HealthSystemState",
      "resolved_inputs",
      "effect_queue",
      "transition_competitive",
      "Math.random",
    ):
      self.assertNotIn(forbidden, self.app + self.adapter)

  def test_checkpoint_view_coverage_matches_the_live_in_memory_handoff(self):
    coverage = self.ledger["checkpoint_view_coverage"]
    checkpoint_test = CHECKPOINT_TEST.read_text(encoding="utf-8")
    mcp_server = MCP_SERVER.read_text(encoding="utf-8")
    self.assertEqual(coverage["status"], "complete-in-memory-host")
    self.assertEqual(coverage["schema"], "competitive-save-v1")
    self.assertEqual(
      coverage["metadata_contract"],
      ["operation", "session_id", "campaign", "seed", "transition_count", "latest_state_hash"],
    )
    for marker in (
      "competitive-save-v1",
      "SaveEnvelope",
      "save_session",
      "load_session",
      "createCheckpointClient",
      "validateSaveEnvelope",
      "checkpoint_refresh_error",
      "checkpoint_missing",
      'id="session-save"',
      'id="session-restore"',
    ):
      self.assertIn(marker, checkpoint_test + self.app + self.adapter + self.server + mcp_server + self.session)
    for boundary in (
      "in-memory host checkpoint",
      "without client-side state restoration",
      "test_checkpoint_boundary_does_not_add_browser_or_route_simulation_authority",
    ):
      self.assertIn(boundary, checkpoint_test + mcp_server + self.session)

  def test_replay_view_coverage_matches_the_live_host_projection(self):
    coverage = self.ledger["replay_view_coverage"]
    replay_test = REPLAY_TEST.read_text(encoding="utf-8")
    mcp_server = MCP_SERVER.read_text(encoding="utf-8")
    self.assertEqual(coverage["status"], "complete-live-host-projection-local-playback-and-host-regeneration")
    self.assertEqual(coverage["schema"], "competitive-replay-v1")
    self.assertEqual(
      coverage["metadata_contract"],
      ["session_id", "campaign", "seed", "transition_count", "latest_state_hash"],
    )
    self.assertEqual(coverage["row_contract"], ["turn", "state_hash"])
    for marker in (
      "competitive-replay-v1",
      "ReplayEnvelope",
      "get_replay",
      '"/api/v1/sessions/{session_id}/replay"',
      "getReplay",
      "createReplayClient",
      "validateReplayEnvelope",
      "renderReplayEnvelope",
      "regenerate_competitive_history",
      "replay-previous",
      "replay-play",
      "replay-pause",
      "replay-next",
      "replay-playback-status",
      "replay_adapter_missing",
      "replay_adapter_error",
      "replay_verification_failed",
    ):
      self.assertIn(marker, replay_test + self.app + self.adapter + self.server + mcp_server + self.session)
    for boundary in (
      "test_live_replay_read_does_not_expose_simulation_authority",
      "self.get_history(GetHistoryRequest",
      'self.assertNotIn("submit_turn", replay_handler)',
    ):
      self.assertIn(boundary, replay_test + mcp_server + self.session)

  def test_autosave_coverage_matches_the_existing_checkpoint_path(self):
    coverage = self.ledger["autosave_coverage"]
    checkpoint_test = CHECKPOINT_TEST.read_text(encoding="utf-8")
    self.assertEqual(coverage["status"], "complete-host-autosave-after-accepted-decision")
    self.assertEqual(coverage["schema"], "competitive-save-v1 plus existing campaign save wrappers")
    for marker in (
      "save_session",
      '"/api/v1/sessions/{session_id}/save"',
      "createCheckpointClient",
      "autosave",
      "checkpoint_autosave_error",
      "ui.save-complete",
      "current session remains active",
    ):
      self.assertIn(marker, checkpoint_test + self.app + self.adapter + self.server)
    for boundary in (
      "without client-side state restoration",
      "The browser stores no save artifact or simulation state",
      "test_checkpoint_boundary_does_not_add_browser_or_route_simulation_authority",
    ):
      self.assertIn(boundary, checkpoint_test + self.app + self.server + self.mcp_server + self.session + json.dumps(coverage))

  def test_checkpoint_reference_transfer_is_metadata_only(self):
    coverage = self.ledger["checkpoint_reference_transfer"]
    self.assertEqual(coverage["status"], "complete-browser-safe-metadata-reference-transfer")
    self.assertEqual(coverage["schema"], "gui-checkpoint-reference-v1")
    self.assertEqual(
      coverage["fields"],
      ["schema_version", "session_id", "campaign", "seed", "transition_count", "storage"],
    )
    for marker in (
      "serializeCheckpointReference",
      "parseCheckpointReference",
      "importCheckpointReference",
      "downloadCheckpointReference",
      "gui-checkpoint-reference-v1",
    ):
      self.assertIn(marker, self.app + self.html + json.dumps(coverage))
    for forbidden in ("CompetitiveWorldState", "resolved_inputs", "effect_queue", "transition_competitive"):
      self.assertNotIn(forbidden, self.app.split("export function serializeCheckpointReference", 1)[-1].split("export function parseCheckpointReference", 1)[0])

  def test_checkpoint_artifact_download_is_host_validated_and_opaque(self):
    coverage = self.ledger["checkpoint_artifact_download"]
    self.assertEqual(coverage["status"], "complete-host-validated-opaque-artifact-download")
    self.assertEqual(coverage["schema"], "host-save-artifact-download-v1")
    self.assertEqual(coverage["storage_sources"], ["archive", "legacy"])
    for marker in (
      "save-artifact",
      "downloadCheckpointArtifact",
      "downloadHostCheckpointArtifact",
      "read_checkpoint_artifact",
      "read_gui_session_checkpoint_artifact",
      "Download host save",
    ):
      self.assertIn(marker, self.server + self.session + self.persistence + self.adapter + self.app + self.html + json.dumps(coverage))
    for boundary in (
      "exact existing bytes",
      "never deserializes, loads, stores",
      "browser is only a manual opaque download surface",
    ):
      self.assertIn(boundary, json.dumps(coverage))

  def test_campaign_coverage_read_covers_all_launchable_campaigns(self):
    coverage = self.ledger["campaign_coverage_read_coverage"]
    self.assertEqual(coverage["status"], "complete-host-typed-coverage-read-for-all-launchable-campaigns")
    self.assertEqual(coverage["schema"], "campaign-coverage-v1")
    self.assertEqual(
      coverage["supported_campaigns"],
      ["competitive-regional-v1", "stabilization-v1", "regional-affiliation-v1"],
    )
    for marker in (
      "from_stabilization",
      "from_competitive",
      "from_affiliation",
      "get_campaign_coverage",
      "getCampaignCoverage",
      "renderCampaignCoverage",
      "campaign-coverage-v1",
    ):
      self.assertIn(marker, self.session + self.server + self.adapter + self.app + json.dumps(coverage))
    for forbidden in FORBIDDEN_AUTHORITY_MARKERS:
      self.assertNotIn(forbidden, self.app)
    self.assertIn("competitive coverage", self.session)

  def test_full_campaign_audio_state_coverage_is_host_bound(self):
    coverage = self.ledger["full_campaign_audio_state_coverage"]
    self.assertEqual(coverage["status"], "complete-full-campaign-host-audio-state-continuity")
    self.assertEqual(coverage["schema"], "campaign-coverage-v1")
    self.assertEqual(
      coverage["campaigns"],
      ["competitive-regional-v1", "stabilization-v1", "regional-affiliation-v1"],
    )
    self.assertEqual(coverage["terminal_music_state"], "debrief")
    self.assertEqual(
      coverage["allowlists"]["music_states"],
      ["menu", "stable_operations", "pressure", "regulatory_scrutiny", "competitive_escalation", "affiliation_negotiation", "debrief"],
    )
    self.assertEqual(
      coverage["allowlists"]["event_cues"],
      ["event.project-complete", "event.staffing-constraint", "event.operating-loss", "event.operating-recovery", "event.payer-decision", "event.regulatory-decision", "event.rival-expansion", "event.affiliation-milestone"],
    )
    for marker in (
      "campaign_coverage_audio_state_covers_all_full_campaign_reads",
      "get_campaign_coverage(GetCampaignCoverageRequest",
      "CampaignCoverageAudio",
      "campaign_audio",
      "debrief",
      "competitive-regional-v1",
      "stabilization-v1",
      "regional-affiliation-v1",
    ):
      self.assertIn(marker, self.session + self.campaign_coverage + json.dumps(coverage))
    self.assertIn("event.project-complete", self.session)
    self.assertIn("event.affiliation-milestone", self.session)
    self.assertIn("Every active and terminal campaign-coverage-v1 read", json.dumps(coverage))
    for boundary in ("No new route/schema", "written equivalents", "does not submit commands"):
      self.assertIn(boundary, json.dumps(coverage))

  def test_full_campaign_replay_continuity_target_is_host_bound(self):
    coverage = self.ledger["full_campaign_replay_continuity"]
    self.assertEqual(coverage["status"], "complete-full-campaign-host-history-replay-continuity")
    self.assertEqual(
      coverage["schemas"],
      ["competitive-history-v1", "competitive-replay-v1"],
    )
    self.assertEqual(
      coverage["campaigns"],
      ["competitive-regional-v1", "stabilization-v1", "regional-affiliation-v1"],
    )
    self.assertEqual(
      coverage["test_source"],
      "src/mcp/session.rs: fn full_campaign_history_and_replay_reads_remain_hash_aligned",
    )
    for marker in (
      "get_history(GetHistoryRequest",
      "get_replay(GetReplayRequest",
      "HistoryEnvelope",
      "ReplayEnvelope",
      "competitive-history-v1",
      "competitive-replay-v1",
    ):
      self.assertIn(marker, self.session + json.dumps(coverage))
    for boundary in ("No new route/schema", "browser serialization", "cannot submit commands"):
      self.assertIn(boundary, json.dumps(coverage))

  def test_full_campaign_coverage_renderer_preserves_host_envelope(self):
    coverage = self.ledger["full_campaign_browser_coverage_rendering"]
    self.assertEqual(coverage["status"], "complete-full-campaign-browser-coverage-renderer-continuity")
    self.assertEqual(coverage["schema"], "campaign-coverage-v1")
    self.assertEqual(
      coverage["campaigns"],
      ["competitive-regional-v1", "stabilization-v1", "regional-affiliation-v1"],
    )
    self.assertEqual(len(coverage["fixtures"]), 6)
    for marker in (
      "renderCampaignCoverage",
      "campaign-coverage-v1",
      "campaignMusicStateId",
      "campaignAudioCueIds",
      "Use the competitive action rail",
    ):
      self.assertIn(marker, self.app + json.dumps(coverage))
    for boundary in ("does not submit commands", "classify hidden state", "No new route/schema"):
      self.assertIn(boundary, json.dumps(coverage))
    script = r'''
      function makeNode(tagName = "div") {
        return {
          tagName: tagName.toUpperCase(),
          children: [],
          dataset: {},
          classList: { add() {}, toggle() {} },
          hidden: true,
          disabled: false,
          textContent: "",
          append(...children) { this.children.push(...children); },
          replaceChildren(...children) { this.children = children; },
          setAttribute(name, value) { this[name] = value; },
          removeAttribute(name) { delete this[name]; },
          addEventListener() {},
        };
      }
      globalThis.document = undefined;
      const { renderCampaignCoverage } = await import("./gui/app.mjs");
      globalThis.document = { createElement: (tagName) => makeNode(tagName) };

      const cases = [
        ["competitive-regional-v1", "Competitive", "Month 1", 1, 24, false, "competitive_escalation"],
        ["competitive-regional-v1", "Competitive", "Complete", 24, 24, true, "debrief"],
        ["stabilization-v1", "Stabilization", "Turn 1", 1, 5, false, "stable_operations"],
        ["stabilization-v1", "Stabilization", "Complete", 5, 5, true, "debrief"],
        ["regional-affiliation-v1", "Affiliation", "Assess partner", 1, 6, false, "affiliation_negotiation"],
        ["regional-affiliation-v1", "Affiliation", "Complete", 6, 6, true, "debrief"],
      ];
      for (const [campaign, role, label, turn, maxTurns, done, music] of cases) {
        const envelope = {
          schema_version: "campaign-coverage-v1",
          campaign_role: role,
          session: { session_id: `${campaign}-${turn}`, campaign, turn, max_turns: maxTurns, done },
          stage: { label, detail: "Host-visible stage detail" },
          briefing: [], metrics: [], actors: [], processes: [],
          decisions: done ? [] : [{ label: "Hold", command_template: "hold", parameters: [], uncertainty: "Visible uncertainty" }],
          history: [{ turn: Math.max(1, turn - 1), command: "hold", state_hash: `${campaign}-hash` }],
          debrief: done ? [`${role} debrief remains written`] : [],
          audio: { music_state_id: music, audio_cue_ids: ["event.project-complete"] },
        };
        const nodes = new Map();
        const root = {
          querySelector(selector) {
            if (!nodes.has(selector)) nodes.set(selector, makeNode());
            return nodes.get(selector);
          },
        };
        const result = renderCampaignCoverage(envelope, root);
        if (!result.ok || result.envelope !== envelope) process.exit(1);
        if (nodes.get("#campaign-coverage-panel").hidden) process.exit(2);
        if (!nodes.get("#campaign-coverage-meta").textContent.includes(campaign)) process.exit(3);
        if (!nodes.get("#campaign-role").textContent.includes(role)) process.exit(4);
        if (nodes.get("#campaign-history-list").children.length !== 1) process.exit(5);
        if (done && nodes.get("#campaign-debrief-list").children.length !== 1) process.exit(6);
        if (!done) {
          const form = nodes.get("#campaign-decision-list").children[0].children.find((child) => child.tagName === "FORM");
          if (!form || !form.children[0].disabled) process.exit(7);
        }
      }
      console.log(JSON.stringify({ cases: cases.length, host_envelope_preserved: true, decisions_read_only: true }));
    '''
    result = subprocess.run(
      ["node", "--input-type=module", "-e", script],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

  def test_full_campaign_coverage_transport_target_is_host_bound(self):
    coverage = self.ledger["full_campaign_coverage_transport_continuity"]
    self.assertEqual(coverage["status"], "complete-full-campaign-loopback-coverage-transport-continuity")
    self.assertEqual(coverage["schema"], "campaign-coverage-v1")
    self.assertEqual(
      coverage["campaigns"],
      ["competitive-regional-v1", "stabilization-v1", "regional-affiliation-v1"],
    )
    self.assertEqual(len(coverage["active_reads"]), 3)
    for marker in (
      "live_transport_covers_full_campaign_coverage_reads",
      "campaign-coverage-v1",
      "GUI_CAMPAIGN_COVERAGE_CAMPAIGNS",
      "/api/v1/sessions/{session_id}/campaign-coverage",
      "get_campaign_coverage",
    ):
      self.assertIn(marker, self.session + self.server + json.dumps(coverage))
    for boundary in ("No new route/schema", "coverage remains observational", "Rust remains authoritative"):
      self.assertIn(boundary, json.dumps(coverage))

  def test_ledger_fallback_references_match_live_adapters(self):
    for catalog_name, catalog in self.ledger["catalogs"].items():
      self.assertEqual(catalog["fallback_id"], self.live["catalog_fallbacks"][catalog_name])

  def test_catalog_entries_preserve_visible_semantics(self):
    for entries in self.live["semantics"].values():
      for entry in entries:
        self.assertGreaterEqual(len(entry), 3)
        self.assertTrue(all(isinstance(value, str) and value.strip() for value in entry[1:]))

  def test_unknown_and_fallback_boundaries_are_explicit(self):
    self.assertEqual(
      self.live["fallbacks"],
      self.ledger["fallbacks"],
    )
    self.assertIsNone(self.live["fallbacks"]["audio_cue_unknown"])
    self.assertIsNone(self.live["fallbacks"]["music_state_unknown"])
    self.assertEqual(
      self.live["fallback_descriptors"],
      {
        "generic_facility_component": {
          "id": "generic-facility",
          "label": "Facility",
          "source": "Missing or unknown visible facility kind",
          "equivalent": "Facility label and generic marker",
        },
        "facility": {
          "rendered_id": "generic-facility",
          "rendered_label": "Facility",
          "source": "Visible fallback because the release asset is malformed",
          "equivalent": "Facility label and generic marker",
          "release_path": None,
          "fallback_reason": "malformed",
        },
        "actor_family": {
          "id": "generic-actor",
          "label": "Actor",
          "source": "Missing or unknown actor-family ID",
          "equivalent": "Actor label, generic marker, neutral frame, and written notification",
        },
        "operational_overlay": {
          "id": "operational-overlay-generic",
          "label": "Operational overlay unavailable",
          "visible_source": "Fixture-only actor-visible operational overlay vocabulary",
          "text_equivalent": "Operational overlay unavailable; visible category is unknown",
        },
        "event_marker": {
          "id": "event-marker-generic",
          "label": "Event marker unavailable",
          "visible_source": "Fixture-only symbolic event-marker vocabulary",
          "text_equivalent": "Event marker unavailable; visible category is unknown",
        },
        "asset": {
          "rendered_id": "generic-asset",
          "rendered_label": "Asset",
          "source": "Visible fallback because the release asset is malformed",
          "equivalent": "Asset unavailable",
          "release_path": None,
          "fallback_reason": "malformed",
        },
      },
    )
    self.assertIn("not established", " ".join(self.ledger["open_limits"]))
    self.assertIn("human quality", " ".join(self.ledger["open_limits"]))

  def test_bounded_continuity_surfaces_are_present(self):
    continuity = self.ledger["continuity"]
    self.assertEqual(continuity["status"], "bounded-competitive-stabilization-and-affiliation-durable-checkpoint-evidence")
    for relative_path in continuity["surfaces"]:
      self.assertTrue((ROOT / relative_path).is_file(), relative_path)
    self.assertIn("host/core-owned", continuity["boundary"])
    self.assertIn("presentation references only", continuity["boundary"])

  def test_catalog_import_closure_has_no_network_or_authority_dependencies(self):
    pending = [ROOT / relative_path for relative_path in CATALOG_MODULES]
    visited = set()
    while pending:
      path = pending.pop()
      if path in visited:
        continue
      visited.add(path)
      source = path.read_text(encoding="utf-8")
      for marker in FORBIDDEN_AUTHORITY_MARKERS:
        self.assertNotIn(marker, source, f"{marker} in {path}")
      for import_path in IMPORT_PATTERN.findall(source):
        imported = (path.parent / import_path).resolve()
        if imported.is_file() and imported not in visited:
          pending.append(imported)
    self.assertGreaterEqual(len(visited), len(CATALOG_MODULES))

  def test_roadmap_closes_only_catalog_and_fallback_items(self):
    expected = {
      "Facility asset coverage complete.": "x",
      "Current supported operational-overlay coverage complete. Evidence:": "x",
      "Current 24-month competitive facility placement/use read continuity": "x",
      "Actor-family coverage complete.": "x",
      "Event cue coverage complete.": "x",
      "Music-state coverage complete.": "x",
      "History view updated.": "x",
      "Current competitive terminal debrief view covered. Evidence:": "x",
      "Current in-memory host checkpoint visual continuity covered. Evidence:": "x",
      "Current explicit durable competitive host checkpoint recovery covered.": "x",
      "Current competitive full-campaign host checkpoint continuation covered.": "x",
      "Current full stabilization host checkpoint continuation covered.": "x",
      "Current full regional-affiliation host checkpoint continuation covered.": "x",
      "Current cross-campaign latest-checkpoint identity covered. Evidence:": "x",
      "Current full-campaign host audio-state coverage covered. Evidence:": "x",
      "Current full-campaign host history/replay continuity covered. Evidence:": "x",
      "Current full-campaign coverage renderer continuity covered. Evidence:": "x",
      "Current full-campaign coverage transport continuity covered. Evidence:": "x",
      "Current explicit durable stabilization host checkpoint recovery covered.": "x",
      "Current explicit durable regional-affiliation host checkpoint recovery covered.": "x",
      "Current live replay visual continuity covered. Evidence:": "x",
      "Current local replay playback over visible host rows covered. Evidence:": "x",
      "Unknown content fallbacks tested.": "x",
      "Current tracked visual/audio asset-registry coverage is 100%. Evidence:": "x",
      "Current supported screenshot-surface contract passes. Evidence:": "x",
      "Current full-campaign local-browser screenshot inspection recorded.": "x",
      "Current persisted 1024x768 full-campaign raster evidence recorded.": "x",
      "Current persisted terminal raster state correction recorded. Evidence:": "x",
    }
    actual = {label: state for state, label in re.findall(r"^- \[([ x])\] (.+)$", self.phase11_1, re.MULTILINE)}
    self.assertEqual(actual, {label: state for label, state in expected.items()})


if __name__ == "__main__":
  unittest.main()
