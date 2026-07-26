import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase11.1-campaign-coverage-ledger.json"
VISUAL_REGISTRY = ROOT / "assets" / "registry" / "visual-assets.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"
RESOLUTION = ROOT / "src" / "mcp" / "resolution.rs"
HISTORY_TEST = ROOT / "tests" / "test_phase11_live_history.py"


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
    cls.resolution = RESOLUTION.read_text(encoding="utf-8")
    cls.app = (ROOT / "gui" / "app.mjs").read_text(encoding="utf-8")
    cls.adapter = (ROOT / "gui" / "host-adapter.mjs").read_text(encoding="utf-8")
    cls.server = (ROOT / "src" / "gui_server.rs").read_text(encoding="utf-8")
    cls.session = (ROOT / "src" / "mcp" / "session.rs").read_text(encoding="utf-8")
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
      {"schema_version", "status", "campaign", "scope", "catalogs", "facility_asset_coverage", "event_cue_coverage", "music_state_coverage", "history_view_coverage", "continuity", "fallbacks", "open_limits"},
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
    self.assertEqual(continuity["status"], "bounded-first-month-evidence")
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
      "Overlay coverage complete.": " ",
      "Actor-family coverage complete.": "x",
      "Event cue coverage complete.": "x",
      "Music-state coverage complete.": "x",
      "History view updated.": "x",
      "Debrief view updated.": " ",
      "Save/load visual continuity tested.": " ",
      "Replay visual continuity tested.": " ",
      "Unknown content fallbacks tested.": "x",
      "Asset registry coverage is 100%.": " ",
      "Full campaign screenshot suite passes.": " ",
    }
    actual = {label: state for state, label in re.findall(r"^- \[([ x])\] (.+)$", self.phase11_1, re.MULTILINE)}
    self.assertEqual(actual, {label: state for label, state in expected.items()})


if __name__ == "__main__":
  unittest.main()
