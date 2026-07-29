import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "evaluation" / "phase13.1-attribution-boundary.json"
ROADMAP = ROOT / "docs" / "visual_audio_enhancement_roadmap.md"
REGISTRIES = (
  ROOT / "assets" / "registry" / "visual-assets.json",
  ROOT / "assets" / "registry" / "audio-assets.json",
)
MANIFEST = ROOT / "assets" / "ASSET_RELEASE_MANIFEST.json"
PORTRAITS = ROOT / "assets" / "generation" / "portrait-previews.json"
PORTRAIT_QUEUE = ROOT / "assets" / "generation" / "portrait-review-queue.json"
PORTRAIT_PREVIEW_ROOT = ROOT / "assets" / "generation" / "portrait-previews"


def load_module(name, relative_path):
  spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
  module = importlib.util.module_from_spec(spec)
  assert spec.loader is not None
  spec.loader.exec_module(module)
  return module


CREDITS = load_module("generate_asset_credits", "scripts/generate_asset_credits.py")
RELEASE = load_module("verify_asset_release", "scripts/verify_asset_release.py")

EXPECTED_SOURCE_CONTRACT = {
  "visual_registry": (
    "assets/registry/visual-assets.json",
    "asset-registry-v1",
  ),
  "audio_registry": (
    "assets/registry/audio-assets.json",
    "asset-registry-v1",
  ),
  "asset_credits": (
    "assets/ASSET_CREDITS.md",
    "No third-party release assets are included",
  ),
  "third_party_notices": (
    "assets/THIRD_PARTY_NOTICES.md",
    "All current release-capable entries are repository-authored",
  ),
  "runtime_credits": (
    "gui/asset-credits.mjs",
    '"third_party_release_count": 0',
  ),
  "release_manifest": (
    "assets/ASSET_RELEASE_MANIFEST.json",
    "asset-release-manifest-v1",
  ),
  "portrait_boundary": (
    "assets/generation/portrait-review-queue.json",
    "Human review, approved model/seed provenance, release derivative, and registry bridge are incomplete",
  ),
}


class Phase131AttributionBoundaryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    cls.roadmap = ROADMAP.read_text(encoding="utf-8")
    cls.registry_documents = [
      json.loads(path.read_text(encoding="utf-8")) for path in REGISTRIES
    ]
    cls.entries = [
      entry
      for document in cls.registry_documents
      for entry in document["entries"]
    ]
    cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cls.portraits = json.loads(PORTRAITS.read_text(encoding="utf-8"))
    cls.portrait_queue = json.loads(PORTRAIT_QUEUE.read_text(encoding="utf-8"))
    cls.preview_files = tuple(
      sorted(path for path in PORTRAIT_PREVIEW_ROOT.iterdir() if path.is_file())
    )

  def test_source_contract_markers_are_independently_anchored(self):
    self.assertEqual(
      self.ledger["schema_version"], "phase13.1-attribution-boundary-v1"
    )
    self.assertEqual(
      self.ledger["status"], "complete-current-technical-attribution-boundary-only"
    )
    self.assertEqual(set(self.ledger["source_contract"]), set(EXPECTED_SOURCE_CONTRACT))
    for key, (source_path, marker) in EXPECTED_SOURCE_CONTRACT.items():
      self.assertEqual(
        self.ledger["source_contract"][key], f"{source_path}: {marker}"
      )
      path = ROOT / source_path
      self.assertTrue(path.is_file(), key)
      self.assertIn(marker, path.read_text(encoding="utf-8"), key)

  def test_current_registry_entries_have_attribution_and_hashes(self):
    self.assertGreater(len(self.entries), 0)
    for entry in self.entries:
      for field in (
        "id",
        "source_path",
        "creator",
        "creation_method",
        "license",
        "modifications",
        "original_hash",
        "attribution_text",
        "accessible_equivalent",
        "approval_status",
      ):
        self.assertTrue(str(entry.get(field, "")).strip(), (entry["id"], field))
      provenance = entry.get("provenance", {})
      self.assertTrue(provenance.get("license_reference"), entry["id"])
      if entry.get("release_path"):
        self.assertTrue(entry.get("release_hash"), entry["id"])

    release_paths = {
      entry["release_path"] for entry in self.entries if entry.get("release_path")
    }
    self.assertEqual(
      release_paths,
      {record["path"] for record in self.manifest["files"]},
    )
    self.assertEqual(self.manifest["schema_version"], "asset-release-manifest-v1")
    self.assertEqual(RELEASE.check_manifest(ROOT), [])

  def test_generated_credits_and_runtime_projection_are_current(self):
    self.assertEqual(
      CREDITS.render(ROOT),
      (ROOT / "assets" / "ASSET_CREDITS.md").read_text(encoding="utf-8"),
    )
    self.assertEqual(
      CREDITS.render_notices(ROOT),
      (ROOT / "assets" / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8"),
    )
    runtime = (ROOT / "gui" / "asset-credits.mjs").read_text(encoding="utf-8")
    self.assertEqual(CREDITS.render_runtime(ROOT), runtime)
    self.assertIn('"third_party_release_count": 0', runtime)
    self.assertIn('"release_status": "approved-release"', runtime)

  def test_unverified_portraits_cannot_enter_attribution_or_release_surfaces(self):
    self.assertFalse(self.portraits["release_eligible"])
    self.assertFalse(self.portrait_queue["release_eligible"])
    registry_ids = {entry["id"] for entry in self.entries}
    manifest_paths = {record["path"] for record in self.manifest["files"]}
    preview_by_id = {entry["asset_id"]: entry for entry in self.portraits["entries"]}
    queue_by_id = {entry["asset_id"]: entry for entry in self.portrait_queue["entries"]}
    self.assertEqual(set(preview_by_id), set(queue_by_id))
    metadata_paths = set()
    for entry in self.portraits["entries"]:
      self.assertNotIn(entry["asset_id"], registry_ids)
      self.assertIsNone(entry["release_path"])
      self.assertIsNone(entry["asset_registry_id"])
      self.assertEqual(entry["approval_status"], "pending")
      self.assertNotIn(entry["source_output_path"], manifest_paths)
      metadata_paths.add(entry["source_output_path"])
      queue_entry = queue_by_id[entry["asset_id"]]
      self.assertEqual(queue_entry["source_output_path"], entry["source_output_path"])
      self.assertEqual(queue_entry["source_hash"], entry["source_hash"])
      self.assertEqual(queue_entry["decision"], "pending")
      self.assertEqual(queue_entry["approval_status"], "pending")
      self.assertIsNone(queue_entry["release_path"])
      self.assertIsNone(queue_entry["asset_registry_id"])
      self.assertNotIn(entry["asset_id"], CREDITS.render_runtime(ROOT))

    actual_paths = {
      path.relative_to(ROOT).as_posix() for path in self.preview_files
    }
    self.assertEqual(actual_paths, metadata_paths)
    self.assertEqual(
      actual_paths,
      {entry["source_output_path"] for entry in self.portrait_queue["entries"]},
    )

  def test_roadmap_and_limits_keep_technical_and_human_gates_distinct(self):
    normalized = " ".join(self.roadmap.split())
    self.assertIn("[x] Attribution complete. Evidence:", normalized)
    self.assertIn("current repository-owned attribution", normalized)
    limits = " ".join(self.ledger["limits"]).lower()
    for marker in (
      "human legal clearance",
      "ownership",
      "training-data provenance",
      "resemblance review",
      "public-release approval",
      "ai-generation metadata remains open",
    ):
      self.assertIn(marker, limits)


if __name__ == "__main__":
  unittest.main()
