import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
  "verify_asset_release",
  ROOT / "scripts" / "verify_asset_release.py",
)
RELEASE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RELEASE)


def sha256(data: bytes) -> str:
  return f"sha256:{hashlib.sha256(data).hexdigest()}"


class AssetReleaseTests(unittest.TestCase):
  def test_repository_manifest_is_current_and_deterministic(self):
    output, errors = RELEASE.render_manifest(ROOT)
    self.assertEqual(errors, [])
    self.assertEqual(ROOT.joinpath("assets/ASSET_RELEASE_MANIFEST.json").read_text(encoding="utf-8"), output)
    self.assertEqual(output, RELEASE.render_manifest(ROOT)[0])
    self.assertEqual(RELEASE.check_manifest(ROOT), [])

  def test_manifest_orders_paths_and_detects_stale_output(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      registry = root / "assets" / "registry"
      release = root / "assets" / "release"
      registry.mkdir(parents=True)
      release.mkdir(parents=True)
      files = {"z.svg": b"z", "a.svg": b"a"}
      entries = []
      for name, content in files.items():
        path = release / name
        path.write_bytes(content)
        entries.append({
          "id": name,
          "release_path": f"assets/release/{name}",
          "release_hash": sha256(content),
          "approval_status": "approved",
        })
      (registry / "visual-assets.json").write_text(json.dumps({"entries": list(reversed(entries))}), encoding="utf-8")
      (registry / "audio-assets.json").write_text(json.dumps({"entries": []}), encoding="utf-8")
      output, errors = RELEASE.render_manifest(root)
      self.assertEqual(errors, [])
      document = json.loads(output)
      self.assertEqual([entry["path"] for entry in document["files"]], [
        "assets/release/a.svg", "assets/release/z.svg",
      ])
      manifest = root / "assets" / "ASSET_RELEASE_MANIFEST.json"
      manifest.write_text(output, encoding="utf-8")
      self.assertEqual(RELEASE.check_manifest(root), [])
      manifest.write_text(output + "\n", encoding="utf-8")
      self.assertTrue(any("generated manifest is stale" in error for error in RELEASE.check_manifest(root)))

  def test_missing_and_hash_mismatched_release_files_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      registry = root / "assets" / "registry"
      release = root / "assets" / "release"
      registry.mkdir(parents=True)
      release.mkdir(parents=True)
      (release / "present.svg").write_bytes(b"actual")
      entries = {
        "entries": [
          {
            "release_path": "assets/release/present.svg",
            "release_hash": sha256(b"expected"),
            "approval_status": "approved",
          },
          {
            "release_path": "assets/release/missing.svg",
            "release_hash": sha256(b"missing"),
            "approval_status": "approved",
          },
        ],
      }
      (registry / "visual-assets.json").write_text(json.dumps(entries), encoding="utf-8")
      (registry / "audio-assets.json").write_text(json.dumps({"entries": []}), encoding="utf-8")
      _, errors = RELEASE.render_manifest(root)
      self.assertTrue(any("release_hash does not match" in error for error in errors))
      self.assertTrue(any("release_path does not exist" in error for error in errors))

  def test_release_path_must_use_canonical_release_root(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      registry = root / "assets" / "registry"
      registry.mkdir(parents=True)
      (root / "assets" / "source.svg").write_bytes(b"source")
      (registry / "visual-assets.json").write_text(json.dumps({
        "entries": [{
          "release_path": "assets/source.svg",
          "release_hash": sha256(b"source"),
          "approval_status": "approved",
        }],
      }), encoding="utf-8")
      (registry / "audio-assets.json").write_text(json.dumps({"entries": []}), encoding="utf-8")
      _, errors = RELEASE.render_manifest(root)
      self.assertTrue(any("release_path must be under assets/release/" in error for error in errors))

  def test_release_path_traversal_and_symlinks_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      registry = root / "assets" / "registry"
      release = root / "assets" / "release"
      source = root / "assets" / "source.svg"
      registry.mkdir(parents=True)
      release.mkdir(parents=True)
      source.write_bytes(b"source")
      entries = [{
        "release_path": "assets/release/../source.svg",
        "release_hash": sha256(b"source"),
        "approval_status": "approved",
      }]
      (registry / "visual-assets.json").write_text(json.dumps({"entries": entries}), encoding="utf-8")
      (registry / "audio-assets.json").write_text(json.dumps({"entries": []}), encoding="utf-8")
      _, errors = RELEASE.render_manifest(root)
      self.assertTrue(any("resolved release_path must remain under assets/release/" in error for error in errors))

      symlink = release / "linked.svg"
      try:
        symlink.symlink_to(source)
      except OSError as error:
        self.skipTest(f"symlinks unavailable: {error}")
      entries[0]["release_path"] = "assets/release/linked.svg"
      (registry / "visual-assets.json").write_text(json.dumps({"entries": entries}), encoding="utf-8")
      _, errors = RELEASE.render_manifest(root)
      self.assertTrue(any("release_path cannot contain symlinks" in error for error in errors))


if __name__ == "__main__":
  unittest.main()
