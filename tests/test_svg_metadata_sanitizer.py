import hashlib
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
  "sanitize_svg_metadata",
  ROOT / "scripts" / "sanitize_svg_metadata.py",
)
SANITIZER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(SANITIZER)


class SvgMetadataSanitizerTests(unittest.TestCase):
  def test_removes_metadata_and_preserves_title_desc_and_other_bytes(self):
    data = (
      b'<?xml version="1.0" encoding="UTF-8"?>\n'
      b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
      b'<!-- <metadata>comment text remains</metadata> -->'
      b'<title>Riverside</title><desc>Community hospital</desc>'
      b'<metadata id="tool"><author>local-tool</author></metadata>'
      b'<rect x="1" y="2" width="3" height="4" />'
      b'</svg>'
    )
    metadata = b'<metadata id="tool"><author>local-tool</author></metadata>'
    expected = data.replace(metadata, b"")
    output = SANITIZER.sanitize_svg_bytes(data)
    self.assertEqual(output, expected)
    self.assertIn(b"<title>Riverside</title>", output)
    self.assertIn(b"<desc>Community hospital</desc>", output)
    self.assertIn(b"<metadata>comment text remains</metadata>", output)

  def test_removes_namespaced_and_self_closing_metadata(self):
    data = (
      b'<svg xmlns="http://www.w3.org/2000/svg" '
      b'xmlns:custom="urn:custom"><custom:metadata /><metadata />'
      b'<title>Title</title></svg>'
    )
    output = SANITIZER.sanitize_svg_bytes(data)
    self.assertNotIn(b"custom:metadata", output)
    self.assertNotIn(b"<metadata", output)
    self.assertIn(b"<title>Title</title>", output)

  def test_nested_metadata_ranges_are_removed_as_one_span(self):
    data = (
      b'<svg xmlns="http://www.w3.org/2000/svg"><metadata>'
      b'<metadata /><author>local-tool</author></metadata><title>x</title></svg>'
    )
    self.assertEqual(
      SANITIZER.sanitize_svg_bytes(data),
      b'<svg xmlns="http://www.w3.org/2000/svg"><title>x</title></svg>',
    )

  def test_malformed_and_unbalanced_input_fails_closed(self):
    for data in (
      b'<svg xmlns="http://www.w3.org/2000/svg"><metadata>',
      b'<svg xmlns="http://www.w3.org/2000/svg"><metadata></svg>',
      b'<svg xmlns="http://www.w3.org/2000/svg"><rect>',
      b'<svg xmlns="http://www.w3.org/2000/svg"><unknown:metadata /></svg>',
      b'<not-svg />',
    ):
      with self.subTest(data=data):
        with self.assertRaises(ValueError):
          SANITIZER.sanitize_svg_bytes(data)

  def test_explicit_derivative_output_is_bounded_and_collision_safe(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source = root / "assets" / "source" / "example.svg"
      derivative_root = root / "assets" / "generation" / "svg-derivatives"
      source.parent.mkdir(parents=True)
      derivative_root.mkdir(parents=True)
      source.write_bytes(
        b'<svg xmlns="http://www.w3.org/2000/svg"><metadata /><title>x</title></svg>'
      )
      target = derivative_root / "example.svg"

      written = SANITIZER.sanitize_file(root, source, target)
      self.assertEqual(written, target.resolve())
      self.assertNotIn(b"metadata", target.read_bytes())
      with self.assertRaisesRegex(ValueError, "already exists"):
        SANITIZER.sanitize_file(root, source, target)
      with self.assertRaisesRegex(ValueError, "under assets/generation/svg-derivatives"):
        SANITIZER.sanitize_file(root, source, root / "assets" / "release" / "copy.svg")

      missing = root / "assets" / "source" / "missing.svg"
      with self.assertRaisesRegex(ValueError, "does not exist"):
        SANITIZER.sanitize_file(root, missing, derivative_root / "missing.svg")
      malformed = root / "assets" / "source" / "malformed.svg"
      malformed.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"><metadata>')
      malformed_target = derivative_root / "malformed.svg"
      with self.assertRaises(ValueError):
        SANITIZER.sanitize_file(root, malformed, malformed_target)
      self.assertFalse(malformed_target.exists())
      symlink = root / "assets" / "source" / "linked.svg"
      try:
        symlink.symlink_to(source)
      except OSError as error:
        self.skipTest(f"symlinks unavailable: {error}")
      with self.assertRaisesRegex(ValueError, "input path cannot contain symlinks"):
        SANITIZER.sanitize_file(root, symlink, derivative_root / "linked.svg")
      output_symlink = derivative_root / "output-link.svg"
      try:
        output_symlink.symlink_to(target)
      except OSError as error:
        self.skipTest(f"symlinks unavailable: {error}")
      with self.assertRaisesRegex(ValueError, "output path cannot contain symlinks"):
        SANITIZER.sanitize_file(root, source, output_symlink)

  def test_current_approved_release_svgs_are_sanitized(self):
    self.assertEqual(SANITIZER.check_release(ROOT), [])

  def test_release_check_rejects_metadata_without_rewriting_release_bytes(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      registry = root / "assets" / "registry"
      release = root / "assets" / "release"
      registry.mkdir(parents=True)
      release.mkdir(parents=True)
      data = (
        b'<svg xmlns="http://www.w3.org/2000/svg"><metadata />'
        b'<title>x</title></svg>'
      )
      release_file = release / "metadata.svg"
      release_file.write_bytes(data)
      entry = {
        "release_path": "assets/release/metadata.svg",
        "release_hash": f"sha256:{hashlib.sha256(data).hexdigest()}",
        "approval_status": "approved",
      }
      (registry / "visual-assets.json").write_text(json.dumps({"entries": [entry]}), encoding="utf-8")
      (registry / "audio-assets.json").write_text(json.dumps({"entries": []}), encoding="utf-8")
      errors = SANITIZER.check_release(root)
      self.assertTrue(any("contains removable SVG metadata" in error for error in errors))
      self.assertEqual(release_file.read_bytes(), data)

  def test_relative_repository_root_keeps_symlink_boundary(self):
    with tempfile.TemporaryDirectory() as directory:
      original_cwd = Path.cwd()
      try:
        os.chdir(directory)
        root = Path("workspace")
        source = root / "assets" / "source" / "example.svg"
        derivative_root = root / "assets" / "generation" / "svg-derivatives"
        source.parent.mkdir(parents=True)
        derivative_root.mkdir(parents=True)
        source.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg" />')
        linked = root / "assets" / "source" / "linked.svg"
        linked.symlink_to(source)
        with self.assertRaisesRegex(ValueError, "input path cannot contain symlinks"):
          SANITIZER.sanitize_file(root, linked, derivative_root / "linked.svg")
      finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
  unittest.main()
