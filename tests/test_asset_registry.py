import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
  spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
  module = importlib.util.module_from_spec(spec)
  assert spec.loader is not None
  spec.loader.exec_module(module)
  return module


CHECK = load_module("validate_assets", "scripts/validate_assets.py")
CREDITS = load_module("generate_asset_credits", "scripts/generate_asset_credits.py")


class AssetRegistryTests(unittest.TestCase):
  def test_repository_registries_and_credits_are_current(self):
    self.assertEqual(CHECK.validate(ROOT), [])
    self.assertEqual(
      CREDITS.render(ROOT),
      (ROOT / "assets" / "ASSET_CREDITS.md").read_text(encoding="utf-8"),
    )
    self.assertEqual(
      CREDITS.render_notices(ROOT),
      (ROOT / "assets" / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8"),
    )

  def test_duplicate_ids_and_unknown_roles_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "source.txt"
      source.write_text("source", encoding="utf-8")
      entry = self._entry(root, "same-id", "identity")
      document = {"schema_version": "asset-registry-v1", "asset_type": "visual", "entries": [entry, dict(entry)]}
      path = root / "registry.json"
      path.write_text(json.dumps(document), encoding="utf-8")
      errors, _ = CHECK.validate_registry(root, "registry.json", "visual")
      self.assertTrue(any("duplicate asset ID" in error for error in errors))
      entry["semantic_role"] = "not-a-role"
      path.write_text(json.dumps(document), encoding="utf-8")
      errors, _ = CHECK.validate_registry(root, "registry.json", "visual")
      self.assertTrue(any("unknown semantic role" in error for error in errors))

  def test_stale_hash_and_missing_generation_metadata_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "source.txt"
      source.write_text("source", encoding="utf-8")
      entry = self._entry(root, "asset", "marker")
      entry["original_hash"] = "sha256:stale"
      entry["creation_method"] = ""
      errors = CHECK._validate_entry(root, entry, "visual", "fixture")
      self.assertTrue(any("original_hash does not match" in error for error in errors))
      self.assertTrue(any("creation_method is required" in error for error in errors))

  def test_invalid_id_and_modification_metadata_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "source.txt"
      source.write_text("source", encoding="utf-8")
      entry = self._entry(root, "", "marker")
      entry["modifications"] = ""
      errors = CHECK._validate_entry(root, entry, "visual", "fixture")
      self.assertTrue(any("id must be a non-empty token" in error for error in errors))
      self.assertTrue(any("modifications is required" in error for error in errors))

  def test_external_provenance_requires_retrieval_and_license_basis(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "source.txt"
      source.write_text("source", encoding="utf-8")
      (root / "license.txt").write_text("CC0 license reference", encoding="utf-8")
      entry = self._entry(root, "external", "marker")
      entry["license"] = "CC0-1.0"
      entry["provenance"] = {
        "kind": "external",
        "source_url": "https://example.test/source",
        "retrieval_date": "2026-07-21",
        "license_reference": "license.txt",
      }
      self.assertEqual(CHECK._validate_entry(root, entry, "visual", "fixture"), [])
      entry["license"] = "project-generated"
      errors = CHECK._validate_entry(root, entry, "visual", "fixture")
      self.assertTrue(any("cannot use project-generated license" in error for error in errors))
      entry["license"] = "CC0-1.0"
      entry["provenance"]["retrieval_date"] = None
      errors = CHECK._validate_entry(root, entry, "visual", "fixture")
      self.assertTrue(any("require provenance retrieval_date" in error for error in errors))

  def test_provenance_date_and_denylisted_text_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "source.txt"
      source.write_text("source", encoding="utf-8")
      entry = self._entry(root, "asset", "marker")
      entry["provenance"]["retrieval_date"] = "2026-99-99"
      entry["visible_source"] = "Pinterest aggregator screenshot"
      errors = CHECK._validate_entry(root, entry, "visual", "fixture")
      self.assertTrue(any("retrieval_date must be null or YYYY-MM-DD" in error for error in errors))
      self.assertTrue(any("denylisted provenance marker 'pinterest'" in error for error in errors))

  def test_malformed_https_provenance_url_fails_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "source.txt"
      source.write_text("source", encoding="utf-8")
      (root / "license.txt").write_text("CC0 license reference", encoding="utf-8")
      entry = self._entry(root, "external", "marker")
      entry["license"] = "CC0-1.0"
      entry["provenance"] = {
        "kind": "external",
        "source_url": "https://example.com:bad",
        "retrieval_date": "2026-07-21",
        "license_reference": "license.txt",
      }
      errors = CHECK._validate_entry(root, entry, "visual", "fixture")
      self.assertTrue(any("source_url must be null or a valid HTTPS URL" in error for error in errors))

  def test_external_release_appears_in_credits_and_notices(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      (root / "assets" / "registry").mkdir(parents=True)
      (root / "assets" / "release").mkdir(parents=True)
      (root / "Cargo.toml").write_text('[package]\nversion = "1.0.0"\n', encoding="utf-8")
      source = root / "source.txt"
      source.write_text("source", encoding="utf-8")
      (root / "license.txt").write_text("CC0 license reference", encoding="utf-8")
      release = root / "assets" / "release" / "external.svg"
      release.write_text("release", encoding="utf-8")
      entry = self._entry(root, "external", "marker")
      entry.update({
        "license": "CC0-1.0",
        "release_path": "assets/release/external.svg",
        "release_hash": CHECK._sha256(release),
        "provenance": {
          "kind": "external",
          "source_url": "https://example.test/source",
          "retrieval_date": "2026-07-21",
          "license_reference": "license.txt",
        },
      })
      (root / "assets" / "registry" / "visual-assets.json").write_text(
        json.dumps({"schema_version": "asset-registry-v1", "asset_type": "visual", "entries": [entry]}),
        encoding="utf-8",
      )
      (root / "assets" / "registry" / "audio-assets.json").write_text(
        json.dumps({"schema_version": "asset-registry-v1", "asset_type": "audio", "entries": []}),
        encoding="utf-8",
      )
      self.assertIn("Third-party release assets in v1.0.0", CREDITS.render(root))
      self.assertIn("`external`", CREDITS.render_notices(root))
      entry["approval_status"] = "pending"
      (root / "assets" / "registry" / "visual-assets.json").write_text(
        json.dumps({"schema_version": "asset-registry-v1", "asset_type": "visual", "entries": [entry]}),
        encoding="utf-8",
      )
      self.assertNotIn("`external`", CREDITS.render_notices(root))

  def test_unregistered_release_file_fails_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      (root / "assets" / "release").mkdir(parents=True)
      (root / "assets" / "registry").mkdir(parents=True)
      (root / "assets" / "release" / "unlisted.svg").write_text("svg", encoding="utf-8")
      for relative_path, asset_type in CHECK.REGISTRIES:
        path = root / relative_path
        path.write_text(
          json.dumps({"schema_version": "asset-registry-v1", "asset_type": asset_type, "entries": []}),
          encoding="utf-8",
        )
      errors = CHECK.validate(root)
      self.assertIn("unregistered release asset: assets/release/unlisted.svg", errors)

  @staticmethod
  def _entry(root, asset_id, role):
    source = root / "source.txt"
    (root / "policy.md").write_text("policy", encoding="utf-8")
    return {
      "id": asset_id,
      "asset_type": "visual",
      "semantic_role": role,
      "source_path": "source.txt",
      "release_path": None,
      "creator": "test",
      "creation_method": "hand-authored",
      "license": "project-generated",
      "modifications": "none",
      "original_hash": CHECK._sha256(source),
      "release_hash": None,
      "attribution_text": "test",
      "accessible_equivalent": "text",
      "visible_source": "visible fixture",
      "approval_status": "approved",
      "provenance": {
        "kind": "repository-authored",
        "source_url": None,
        "retrieval_date": None,
        "license_reference": "policy.md",
      },
    }


if __name__ == "__main__":
  unittest.main()
