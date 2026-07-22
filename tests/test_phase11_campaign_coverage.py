import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase11.1-campaign-coverage-ledger.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"


NODE_PROBE = r'''
globalThis.fetch = () => { throw new Error("network blocked"); };
globalThis.WebSocket = class { constructor() { throw new Error("network blocked"); } };
const [facilities, overlays, actors, markers, cues, music, availability] = await Promise.all([
  import("./gui/facility-components.mjs"),
  import("./gui/operational-overlays.mjs"),
  import("./gui/actor-families.mjs"),
  import("./gui/map-event-markers.mjs"),
  import("./gui/audio-cue-contract.mjs"),
  import("./gui/music-stem-contract.mjs"),
  import("./gui/asset-availability.mjs"),
]);
const unknownAsset = availability.assetPresentationFor({
  id: "unknown-asset",
  label: "Unknown asset",
  fallback: { id: "generic-asset", label: "Asset", equivalent: "Asset unavailable" },
}, "unknown");
const unknownFacility = facilities.facilityPresentationFor("general-hospital-base", "unknown");
const unknownFacilityComponent = facilities.facilityComponentFor("unknown");
console.log(JSON.stringify({
  facilities: Object.keys(facilities.FACILITY_COMPONENTS),
  operational_overlays: overlays.OPERATIONAL_OVERLAY_SET.map((entry) => entry.id),
  actor_families: actors.ACTOR_FAMILIES.map((entry) => entry.id),
  event_markers: markers.EVENT_MARKER_SET.map((entry) => entry.id),
  event_cues: cues.AUDIO_CUE_CONTRACT.entries.map((entry) => entry.id),
  music_states: music.MUSIC_STEM_CONTRACT.entries.map((entry) => entry.id),
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
      {"schema_version", "status", "campaign", "scope", "catalogs", "continuity", "fallbacks", "open_limits"},
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
      "Facility asset coverage complete.": " ",
      "Overlay coverage complete.": " ",
      "Actor-family coverage complete.": "x",
      "Event cue coverage complete.": " ",
      "Music-state coverage complete.": " ",
      "History view updated.": " ",
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
