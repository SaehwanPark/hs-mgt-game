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
    }


if __name__ == "__main__":
  unittest.main()
