import importlib.util
import struct
import tempfile
import unittest
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
  "validate_asset_security",
  ROOT / "scripts" / "validate_asset_security.py",
)
SECURITY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(SECURITY)


class AssetSecurityTests(unittest.TestCase):
  def test_repository_asset_roots_pass_security_scan(self):
    self.assertEqual(SECURITY.validate(ROOT), [])
    self.assertGreaterEqual(len(SECURITY._asset_files(ROOT)), 40)

  def test_svg_executable_external_and_metadata_content_fails_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      unsafe = root / "unsafe.svg"
      unsafe.write_text(
        '<?xml-stylesheet href="other.css"?>'
        '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
        '<script>alert(1)</script><rect onclick="go()" />'
        '<image href="https://example.test/image.png" />'
        '<use href="other.svg#icon" /><use href="j&#x61;vascript:alert(1)" />'
        '<foreignObject /><metadata /><style>@font-face { src: url(https://example.test/font.woff); }'
        '.icon { fill: url(other.svg#paint); }</style>'
        '</svg>',
        encoding="utf-8",
      )
      errors = SECURITY.validate_file(root, "unsafe.svg")
      for marker in (
        "SVG script element",
        "SVG event handler",
        "embedded SVG raster image",
        "SVG executable/container element",
        "unstripped SVG metadata",
        "external SVG font/import rule",
        "external SVG reference",
        "external SVG stylesheet reference",
      ):
        self.assertTrue(any(marker in error for error in errors), marker)

      malformed_dimensions = root / "malformed-dimensions.svg"
      malformed_dimensions.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="10pxgarbage" height="10" />',
        encoding="utf-8",
      )
      errors = SECURITY.validate_file(root, "malformed-dimensions.svg")
      self.assertTrue(any("SVG width is not a positive finite number" in error for error in errors))

  def test_malformed_size_and_dimension_limits_fail_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      (root / "broken.svg").write_text('<svg width="10">', encoding="utf-8")
      self.assertTrue(any("malformed SVG/XML" in error for error in SECURITY.validate_file(root, "broken.svg")))

      large = root / "large.bin"
      large.write_bytes(b"x" * (SECURITY.MAX_FILE_BYTES + 1))
      errors = SECURITY.validate_file(root, "large.bin")
      self.assertTrue(any("file exceeds" in error for error in errors))
      self.assertTrue(any("unsupported asset extension" in error for error in errors))

      png = root / "large.png"
      png.write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        + struct.pack(">II", SECURITY.MAX_DIMENSION + 1, 1)
        + b"\x08\x06\x00\x00\x00\x00\x00\x00\x00"
        + b"\x00\x00\x00\x01IDAT\x78\x00\x00\x00\x00"
        + b"\x00\x00\x00\x00IEND\x00\x00\x00\x00"
      )
      errors = SECURITY.validate_file(root, "large.png")
      self.assertTrue(any("dimension exceeds" in error for error in errors))

  def test_supported_raster_dimensions_and_audio_signatures_pass(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      (root / "one.gif").write_bytes(b"GIF89a" + struct.pack("<HH", 1, 1) + b"\x00\x00\x00\x3b")
      (root / "one.png").write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        + struct.pack(">II", 1, 1)
        + b"\x08\x06\x00\x00\x00\x00\x00\x00\x00"
        + b"\x00\x00\x00\x0bIDAT" + zlib.compress(b"\x00\x00\x00\x00\x00") + b"\x00\x00\x00\x00"
        + b"\x00\x00\x00\x00IEND\x00\x00\x00\x00"
      )
      (root / "one.jpg").write_bytes(
        b"\xff\xd8\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00"
        + b"\xff\xda\x00\x08\x01\x01\x00\x00\x3f\x00\x00\xff\xd9"
      )
      (root / "one.wav").write_bytes(
        b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00"
        + b"\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00"
        + b"data\x00\x00\x00\x00"
      )
      (root / "one.ogg").write_bytes(b"OggS" + b"\x00" * 22 + b"\x01\x01\x00")
      (root / "one.flac").write_bytes(b"fLaC\x80\x00\x00\x22" + b"\x00" * 34 + b"\xff\xf8")
      (root / "one.mp3").write_bytes(
        b"ID3\x04\x00\x00\x00\x00\x00\x00\xff\xfb\x90\x64" + b"\x00" * 413
      )
      for name in ("one.gif", "one.png", "one.jpg", "one.wav", "one.ogg", "one.flac", "one.mp3"):
        self.assertEqual(SECURITY.validate_file(root, name), [], name)

  def test_truncated_media_signatures_fail_closed(self):
    fixtures = {
      "short.gif": b"GIF89a" + b"\x01\x00\x01\x00",
      "short.png": b"\x89PNG\r\n\x1a\n",
      "short.jpg": b"\xff\xd8\xff\xc0",
      "short.wav": b"RIFF\x00\x00\x00\x00WAVE",
      "short.ogg": b"OggS",
      "short.flac": b"fLaC",
      "short.mp3": b"ID3",
    }
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      for name, data in fixtures.items():
        (root / name).write_bytes(data)
        self.assertTrue(SECURITY.validate_file(root, name), name)

  def test_registry_paths_are_included_in_security_scope(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      registry_directory = root / "assets" / "registry"
      registry_directory.mkdir(parents=True)
      custom_asset = root / "custom" / "registered.svg"
      custom_asset.parent.mkdir()
      custom_asset.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" />',
        encoding="utf-8",
      )
      (registry_directory / "visual-assets.json").write_text(
        '{"entries":[{"source_path":"custom/registered.svg"}]}',
        encoding="utf-8",
      )
      (registry_directory / "audio-assets.json").write_text('{"entries":[]}', encoding="utf-8")
      self.assertIn("custom/registered.svg", SECURITY._asset_files(root))
      self.assertEqual(SECURITY.validate(root), [])

      custom_asset.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
        '<script>alert(1)</script></svg>',
        encoding="utf-8",
      )
      self.assertTrue(SECURITY.validate(root))

      unsupported = root / "custom" / "payload.bin"
      unsupported.write_bytes(b"payload")
      (registry_directory / "visual-assets.json").write_text(
        '{"entries":[{"source_path":"custom/registered.svg"},{"source_path":"custom/payload.bin"}]}',
        encoding="utf-8",
      )
      errors = SECURITY.validate(root)
      self.assertTrue(any("unsupported asset extension .bin" in error for error in errors))

      (registry_directory / "audio-assets.json").write_text("{", encoding="utf-8")
      errors = SECURITY.validate(root)
      self.assertTrue(any("audio-assets.json: registry cannot be read" in error for error in errors))

      (registry_directory / "visual-assets.json").write_text("[]", encoding="utf-8")
      errors = SECURITY.validate(root)
      self.assertTrue(any("visual-assets.json: registry document must be an object" in error for error in errors))

  def test_release_metadata_fails_but_source_preview_metadata_is_allowed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      release = root / "assets" / "release"
      release.mkdir(parents=True)
      release_png = release / "metadata.png"
      png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        + struct.pack(">II", 1, 1)
        + b"\x08\x06\x00\x00\x00\x00\x00\x00\x00"
        + b"\x00\x00\x00\x09tEXtkey\x00value\x00\x00\x00\x00"
        + b"\x00\x00\x00\x0bIDAT" + zlib.compress(b"\x00\x00\x00\x00\x00") + b"\x00\x00\x00\x00"
        + b"\x00\x00\x00\x00IEND\x00\x00\x00\x00"
      )
      release_png.write_bytes(png)
      errors = SECURITY.validate_file(root, "assets/release/metadata.png")
      self.assertTrue(any("rejected release metadata (tEXt)" in error for error in errors))

      preview = root / "assets" / "generation" / "portrait-previews"
      preview.mkdir(parents=True)
      (preview / "metadata.png").write_bytes(png)
      errors = SECURITY.validate_file(root, "assets/generation/portrait-previews/metadata.png")
      self.assertFalse(any("rejected release metadata" in error for error in errors))

  def test_release_metadata_classes_fail_closed_for_image_and_audio_formats(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      release = root / "assets" / "release"
      release.mkdir(parents=True)
      files = {
        "metadata.jpg": (
          b"\xff\xd8\xff\xe1\x00\x06Exif"
          b"\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00"
          b"\xff\xda\x00\x08\x01\x01\x00\x00\x3f\x00\x00\xff\xd9"
        ),
        "metadata.gif": b"GIF89a" + struct.pack("<HH", 1, 1) + b"\x00\x00\x00\x21\xfe\x01x\x00\x3b",
        "metadata.wav": (
          b"RIFF\x30\x00\x00\x00WAVEfmt \x10\x00\x00\x00"
          + b"\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00"
          + b"LIST\x04\x00\x00\x00INFOdata\x00\x00\x00\x00"
        ),
        "metadata.ogg": b"OggS" + b"\x00" * 22 + b"\x01\x07\x03vorbis",
        "metadata.flac": b"fLaC\x00\x00\x00\x22" + b"\x00" * 34 + b"\x84\x00\x00\x01x\xff\xf8",
        "metadata.mp3": b"ID3\x04\x00\x00\x00\x00\x00\x00\xff\xfb\x90\x64" + b"\x00" * 413,
        "metadata-flac-application.flac": b"fLaC\x00\x00\x00\x22" + b"\x00" * 34 + b"\x82\x00\x00\x01x\x84\x00\x00\x01x\xff\xf8",
        "metadata-mp3-id3v1.mp3": b"\xff\xfb\x90\x64" + b"\x00" * 413 + b"TAG" + b"\x00" * 125,
        "metadata-mp3-ape.mp3": b"\xff\xfb\x90\x64" + b"\x00" * 413 + b"\x00" * 24 + b"APETAGEX" + b"\x00" * 24,
      }
      for name, data in files.items():
        (release / name).write_bytes(data)
        errors = SECURITY.validate_file(root, f"assets/release/{name}")
        self.assertTrue(any("rejected release metadata" in error for error in errors), name)

  def test_mismatched_audio_signature_fails_closed(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      (root / "fake.wav").write_bytes(b"not-wave")
      errors = SECURITY.validate_file(root, "fake.wav")
      self.assertTrue(any("invalid .wav audio signature" in error for error in errors))


if __name__ == "__main__":
  unittest.main()
