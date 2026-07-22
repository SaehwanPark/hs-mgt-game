#!/usr/bin/env python3
"""Scan repository asset files for bounded security and integrity hazards."""

from __future__ import annotations

import math
import html
import json
import re
import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path
from struct import unpack


MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_DIMENSION = 8192
MAX_PIXELS = 16_777_216
ASSET_ROOTS = (
  Path("assets/source"),
  Path("assets/release"),
  Path("assets/generation/portrait-previews"),
)
REGISTRIES = (
  Path("assets/registry/visual-assets.json"),
  Path("assets/registry/audio-assets.json"),
)
REGISTERED_RUNTIME_SUFFIXES = {".mjs"}
RASTER_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png"}
AUDIO_SUFFIXES = {".flac", ".mp3", ".ogg", ".wav"}
SVG_SUFFIXES = {".svg"}
SUPPORTED_SUFFIXES = RASTER_SUFFIXES | AUDIO_SUFFIXES | SVG_SUFFIXES
RELEASE_PREFIX = "assets/release/"
PNG_METADATA_CHUNKS = {b"tEXt", b"zTXt", b"iTXt", b"eXIf", b"tIME"}
WAV_METADATA_CHUNKS = {b"LIST", b"bext", b"iXML", b"ID3 "}
NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
NUMBER_PATTERN = re.compile(rf"^{NUMBER}$")
LENGTH_PATTERN = re.compile(rf"^{NUMBER}(?:px|pt|pc|mm|cm|in)?$", re.IGNORECASE)
FORBIDDEN_SVG_PATTERNS = (
  (re.compile(r"<\s*script\b", re.IGNORECASE), "SVG script element"),
  (re.compile(r"\bon[a-z][a-z0-9_-]*\s*=", re.IGNORECASE), "SVG event handler"),
  (re.compile(r"<\s*(?:foreignObject|iframe|object|embed)\b", re.IGNORECASE), "SVG executable/container element"),
  (re.compile(r"<\s*(?:image|feImage)\b", re.IGNORECASE), "embedded SVG raster image"),
  (re.compile(r"<\s*metadata\b", re.IGNORECASE), "unstripped SVG metadata"),
  (re.compile(r"<!\s*(?:DOCTYPE|ENTITY)\b", re.IGNORECASE), "SVG entity declaration"),
  (re.compile(r"@(?:font-face|import)\b", re.IGNORECASE), "external SVG font/import rule"),
  (re.compile(r"(?:\b(?:href|xlink:href|src)\s*=\s*[\"']\s*(?:javascript:|data:|file:|https?:|//)|url\(\s*[\"']?\s*(?:javascript:|data:|file:|https?:|//))", re.IGNORECASE), "external SVG reference"),
)


def _relative(root: Path, path: Path) -> str:
  return path.resolve().relative_to(root.resolve()).as_posix()


def _safe_path(root: Path, path: Path) -> tuple[Path | None, list[str]]:
  errors: list[str] = []
  resolved_root = root.resolve()
  resolved = path.resolve()
  if resolved_root not in resolved.parents and resolved != resolved_root:
    errors.append(f"{path}: path escapes repository root")
    return None, errors
  if not path.is_file():
    errors.append(f"{path}: file does not exist")
    return None, errors
  return resolved, errors


def _contains_symlink(root: Path, path: Path) -> bool:
  try:
    relative = path.relative_to(root)
  except ValueError:
    return False
  current = root
  for part in relative.parts:
    current /= part
    if current.is_symlink():
      return True
  return False


def _number(value: str, allow_units: bool = True) -> float | None:
  pattern = LENGTH_PATTERN if allow_units else NUMBER_PATTERN
  normalized = value.strip()
  match = pattern.fullmatch(normalized)
  if match is None:
    return None
  number = float(re.match(NUMBER, normalized, re.IGNORECASE).group(0))
  return number if math.isfinite(number) else None


def _check_dimensions(relative: str, width: int, height: int) -> list[str]:
  if width <= 0 or height <= 0:
    return [f"{relative}: dimensions must be positive"]
  if width > MAX_DIMENSION or height > MAX_DIMENSION:
    return [f"{relative}: dimension exceeds {MAX_DIMENSION}px"]
  if width * height > MAX_PIXELS:
    return [f"{relative}: pixel area exceeds {MAX_PIXELS}"]
  return []


def _svg_dimensions(relative: str, document: str, root_element) -> list[str]:
  errors: list[str] = []
  for attribute in ("width", "height"):
    if attribute in root_element.attrib:
      value = _number(root_element.attrib[attribute])
      if value is None or value <= 0:
        errors.append(f"{relative}: SVG {attribute} is not a positive finite number")
      elif value > MAX_DIMENSION:
        errors.append(f"{relative}: SVG {attribute} exceeds {MAX_DIMENSION}px")
  view_box = root_element.attrib.get("viewBox") or root_element.attrib.get("viewbox")
  if view_box:
    values = view_box.replace(",", " ").split()
    if len(values) != 4:
      return errors + [f"{relative}: SVG viewBox must have four numbers"]
    numbers = [_number(value, allow_units=False) for value in values]
    if any(value is None for value in numbers):
      errors.append(f"{relative}: SVG viewBox contains a non-finite number")
    else:
      view_width, view_height = numbers[2], numbers[3]
      if view_width <= 0 or view_height <= 0:
        errors.append(f"{relative}: SVG viewBox dimensions must be positive")
      elif view_width > MAX_DIMENSION or view_height > MAX_DIMENSION:
        errors.append(f"{relative}: SVG viewBox exceeds {MAX_DIMENSION}px")
      elif view_width * view_height > MAX_PIXELS:
        errors.append(f"{relative}: SVG viewBox area exceeds {MAX_PIXELS}")
  elif "width" not in root_element.attrib or "height" not in root_element.attrib:
    errors.append(f"{relative}: SVG requires width/height or viewBox")
  return errors


def _validate_svg(relative: str, data: bytes) -> list[str]:
  errors: list[str] = []
  try:
    document = data.decode("utf-8")
    root_element = ElementTree.fromstring(document)
  except (UnicodeDecodeError, ElementTree.ParseError) as error:
    return [f"{relative}: malformed SVG/XML ({error})"]
  if root_element.tag.rsplit("}", 1)[-1].lower() != "svg":
    errors.append(f"{relative}: root element must be svg")
  for pattern, description in FORBIDDEN_SVG_PATTERNS:
    if pattern.search(document):
      errors.append(f"{relative}: rejected {description}")
  stylesheet_pattern = re.compile(r"<\?xml-stylesheet\b(.*?)\?>", re.IGNORECASE | re.DOTALL)
  for stylesheet in stylesheet_pattern.finditer(document):
    href_match = re.search(r"\bhref\s*=\s*([\"'])(.*?)\1", stylesheet.group(1), re.IGNORECASE | re.DOTALL)
    href = html.unescape(href_match.group(2)).strip() if href_match else ""
    if not href.startswith("#"):
      errors.append(f"{relative}: rejected external SVG stylesheet reference")
  for element in root_element.iter():
    for attribute, value in element.attrib.items():
      attribute_name = attribute.rsplit("}", 1)[-1].lower()
      decoded_value = html.unescape(str(value)).strip()
      if attribute_name in {"href", "src"} and decoded_value and not decoded_value.startswith("#"):
        errors.append(f"{relative}: rejected external SVG reference")
      if _has_external_svg_url(decoded_value):
        errors.append(f"{relative}: rejected external SVG reference")
      if attribute_name == "style":
        errors.extend(_svg_style_errors(relative, decoded_value))
    if element.tag.rsplit("}", 1)[-1].lower() == "style":
      errors.extend(_svg_style_errors(relative, element.text or ""))
  errors.extend(_svg_dimensions(relative, document, root_element))
  return errors


def _has_external_svg_url(value: str) -> bool:
  url_pattern = re.compile(r"url\(\s*(?:([\"'])(.*?)\1|([^)]*))\s*\)", re.IGNORECASE)
  for match in url_pattern.finditer(html.unescape(value)):
    target = (match.group(2) if match.group(1) else match.group(3) or "").strip()
    if target and not target.startswith("#"):
      return True
  return False


def _svg_style_errors(relative: str, value: str) -> list[str]:
  decoded_value = html.unescape(value).strip()
  errors: list[str] = []
  if _has_external_svg_url(decoded_value):
    errors.append(f"{relative}: rejected external SVG reference")
  if re.search(r"@(?:font-face|import)\b", decoded_value, re.IGNORECASE):
    errors.append(f"{relative}: rejected external SVG font/import rule")
  return errors


def _png_dimensions(relative: str, data: bytes) -> tuple[int, int] | None:
  if len(data) < 45 or data[:8] != b"\x89PNG\r\n\x1a\n":
    return None
  offset = 8
  dimensions: tuple[int, int] | None = None
  saw_idat = False
  while offset + 12 <= len(data):
    chunk_length = int.from_bytes(data[offset:offset + 4], "big")
    chunk_end = offset + 12 + chunk_length
    if chunk_end > len(data):
      return None
    chunk_type = data[offset + 4:offset + 8]
    if chunk_type == b"IHDR":
      if offset != 8 or chunk_length != 13:
        return None
      dimensions = unpack(">II", data[offset + 8:offset + 16])
    if chunk_type == b"IDAT" and chunk_length > 0:
      saw_idat = True
    if chunk_type == b"IEND":
      if chunk_length != 0 or dimensions is None or not saw_idat or chunk_end != len(data):
        return None
      return dimensions
    offset = chunk_end
  return None


def _gif_dimensions(relative: str, data: bytes) -> tuple[int, int] | None:
  if len(data) < 14 or data[:6] not in {b"GIF87a", b"GIF89a"} or not data.endswith(b"\x3b"):
    return None
  return unpack("<HH", data[6:10])


def _jpeg_dimensions(relative: str, data: bytes) -> tuple[int, int] | None:
  if len(data) < 4 or data[:2] != b"\xff\xd8":
    return None
  offset = 2
  dimensions: tuple[int, int] | None = None
  sof_markers = set(range(0xC0, 0xC4)) | set(range(0xC5, 0xC8)) | set(range(0xC9, 0xCC)) | set(range(0xCD, 0xD0))
  while offset + 3 < len(data):
    if data[offset] != 0xFF:
      offset += 1
      continue
    while offset < len(data) and data[offset] == 0xFF:
      offset += 1
    if offset >= len(data):
      break
    marker = data[offset]
    offset += 1
    if marker in {0xD8, 0xD9}:
      continue
    if offset + 2 > len(data):
      break
    segment_length = int.from_bytes(data[offset:offset + 2], "big")
    if segment_length < 2 or offset + segment_length > len(data):
      break
    if marker == 0xDA:
      if dimensions is not None and offset + segment_length < len(data) - 2:
        return dimensions
      return None
    if marker in sof_markers and segment_length >= 7:
      height = int.from_bytes(data[offset + 3:offset + 5], "big")
      width = int.from_bytes(data[offset + 5:offset + 7], "big")
      dimensions = width, height
    offset += segment_length
  return None


def _validate_raster(relative: str, suffix: str, data: bytes) -> list[str]:
  signatures = {
    ".png": data.startswith(b"\x89PNG\r\n\x1a\n"),
    ".gif": data[:6] in {b"GIF87a", b"GIF89a"},
    ".jpg": data.startswith(b"\xff\xd8") and data.endswith(b"\xff\xd9"),
    ".jpeg": data.startswith(b"\xff\xd8") and data.endswith(b"\xff\xd9"),
  }
  errors = [] if signatures[suffix] else [f"{relative}: invalid {suffix} signature"]
  dimensions = (
    _png_dimensions(relative, data) if suffix == ".png"
    else _gif_dimensions(relative, data) if suffix == ".gif"
    else _jpeg_dimensions(relative, data)
  )
  if dimensions is None:
    errors.append(f"{relative}: cannot determine {suffix} dimensions")
  else:
    errors.extend(_check_dimensions(relative, *dimensions))
  errors.extend(_release_metadata_errors(relative, suffix, data))
  return errors


def _validate_audio(relative: str, suffix: str, data: bytes) -> list[str]:
  if suffix == ".wav":
    valid = _valid_wav(data)
  elif suffix == ".ogg":
    valid = _valid_ogg(data)
  elif suffix == ".flac":
    valid = _valid_flac(data)
  else:
    valid = _valid_mp3(data)
  errors = [] if valid else [f"{relative}: invalid {suffix} audio signature"]
  errors.extend(_release_metadata_errors(relative, suffix, data))
  return errors


def _release_metadata_errors(relative: str, suffix: str, data: bytes) -> list[str]:
  if not relative.startswith(RELEASE_PREFIX):
    return []
  labels: list[str] = []
  if suffix == ".png":
    offset = 8
    while offset + 12 <= len(data):
      chunk_length = int.from_bytes(data[offset:offset + 4], "big")
      chunk_end = offset + 12 + chunk_length
      if chunk_end > len(data):
        break
      chunk_type = data[offset + 4:offset + 8]
      if chunk_type in PNG_METADATA_CHUNKS:
        labels.append(chunk_type.decode("ascii"))
      if chunk_type == b"IEND":
        break
      offset = chunk_end
  elif suffix in {".jpg", ".jpeg"}:
    offset = 2
    while offset + 3 < len(data):
      if data[offset] != 0xFF:
        offset += 1
        continue
      while offset < len(data) and data[offset] == 0xFF:
        offset += 1
      if offset >= len(data) or data[offset] in {0xD8, 0xD9}:
        offset += 1
        continue
      if offset + 2 > len(data):
        break
      marker = data[offset]
      segment_length = int.from_bytes(data[offset + 1:offset + 3], "big")
      if segment_length < 2 or offset + 1 + segment_length > len(data):
        break
      if marker == 0xFE or 0xE1 <= marker <= 0xEF:
        labels.append(f"JPEG marker 0x{marker:02x}")
      offset += 1 + segment_length
  elif suffix == ".gif":
    if b"\x21\xfe" in data:
      labels.append("GIF comment extension")
    if b"\x21\xff" in data:
      labels.append("GIF application extension")
  elif suffix == ".wav":
    offset = 12
    while offset + 8 <= len(data):
      chunk_size = int.from_bytes(data[offset + 4:offset + 8], "little")
      chunk_end = offset + 8 + chunk_size
      if chunk_end > len(data):
        break
      chunk_type = data[offset:offset + 4]
      if chunk_type in WAV_METADATA_CHUNKS:
        labels.append(chunk_type.decode("ascii", errors="replace"))
      offset = chunk_end + (chunk_size & 1)
  elif suffix == ".ogg":
    if b"\x03vorbis" in data:
      labels.append("Vorbis comment packet")
    if b"OpusTags" in data:
      labels.append("OpusTags packet")
  elif suffix == ".flac":
    offset = 4
    while offset + 4 <= len(data):
      block_header = data[offset:offset + 4]
      block_length = int.from_bytes(block_header[1:4], "big")
      block_end = offset + 4 + block_length
      if block_end > len(data):
        break
      if block_header[0] & 0x7F in {2, 4, 5, 6}:
        labels.append(f"FLAC metadata block {block_header[0] & 0x7F}")
      offset = block_end
      if block_header[0] & 0x80:
        break
  elif suffix == ".mp3":
    if data[:3] == b"ID3":
      labels.append("ID3 tag")
    if len(data) >= 128 and data[-128:-125] == b"TAG":
      labels.append("ID3v1 tag")
    if b"APETAGEX" in data[-160:]:
      labels.append("APE tag")
  return [f"{relative}: rejected release metadata ({label})" for label in labels]


def _valid_wav(data: bytes) -> bool:
  if len(data) < 44 or data[:4] != b"RIFF" or data[8:12] != b"WAVE":
    return False
  if int.from_bytes(data[4:8], "little") + 8 != len(data):
    return False
  offset = 12
  found_fmt = False
  found_data = False
  while offset + 8 <= len(data):
    chunk_size = int.from_bytes(data[offset + 4:offset + 8], "little")
    chunk_end = offset + 8 + chunk_size
    if chunk_end > len(data):
      return False
    chunk_id = data[offset:offset + 4]
    if chunk_id == b"fmt ":
      found_fmt = chunk_size >= 16
    elif chunk_id == b"data":
      found_data = True
    offset = chunk_end + (chunk_size & 1)
    if offset > len(data):
      return False
  return found_fmt and found_data and offset == len(data)


def _valid_ogg(data: bytes) -> bool:
  if len(data) < 28:
    return False
  offset = 0
  pages = 0
  has_payload = False
  while offset < len(data):
    if offset + 27 > len(data) or data[offset:offset + 4] != b"OggS" or data[offset + 4] != 0:
      return False
    segment_count = data[offset + 26]
    table_end = offset + 27 + segment_count
    if table_end > len(data):
      return False
    payload_end = table_end + sum(data[offset + 27:table_end])
    if payload_end > len(data):
      return False
    has_payload = has_payload or any(data[offset + 27:table_end])
    offset = payload_end
    pages += 1
  return pages > 0 and has_payload


def _valid_flac(data: bytes) -> bool:
  if len(data) < 44 or data[:4] != b"fLaC":
    return False
  offset = 4
  saw_streaminfo = False
  saw_last_block = False
  while offset + 4 <= len(data):
    block_header = data[offset:offset + 4]
    block_length = int.from_bytes(block_header[1:4], "big")
    block_end = offset + 4 + block_length
    if block_end > len(data):
      return False
    if offset == 4 and block_header[0] & 0x7F == 0 and block_length == 34:
      saw_streaminfo = True
    offset = block_end
    if block_header[0] & 0x80:
      saw_last_block = True
      break
  return (
    saw_streaminfo
    and saw_last_block
    and offset + 2 <= len(data)
    and data[offset] == 0xFF
    and data[offset + 1] & 0xFC == 0xF8
  )


def _valid_mp3(data: bytes) -> bool:
  if data[:3] == b"ID3":
    if len(data) < 10 or data[3] == 0xFF or any(byte & 0x80 for byte in data[6:10]):
      return False
    tag_size = sum(byte << shift for byte, shift in zip(data[6:10], (21, 14, 7, 0)))
    return tag_size <= len(data) - 10 and _valid_mp3_frame(data[10 + tag_size:])
  return _valid_mp3_frame(data)


def _valid_mp3_frame(data: bytes) -> bool:
  if len(data) < 4 or data[0] != 0xFF or data[1] & 0xE0 != 0xE0:
    return False
  version = (data[1] >> 3) & 0x03
  layer = (data[1] >> 1) & 0x03
  bitrate_index = (data[2] >> 4) & 0x0F
  sample_rate_index = (data[2] >> 2) & 0x03
  padding = (data[2] >> 1) & 0x01
  if version != 3 or layer != 1 or bitrate_index in {0, 15} or sample_rate_index == 3:
    return False
  bitrates = (32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320)
  sample_rates = (44100, 48000, 32000)
  frame_length = (144 * bitrates[bitrate_index - 1] * 1000) // sample_rates[sample_rate_index] + padding
  return len(data) >= frame_length


def validate_file(root: Path, relative_path: str) -> list[str]:
  path, errors = _safe_path(root, root / relative_path)
  if path is None:
    return errors
  relative = _relative(root, path)
  suffix = path.suffix.lower()
  if path.stat().st_size > MAX_FILE_BYTES:
    errors.append(f"{relative}: file exceeds {MAX_FILE_BYTES} bytes")
    if suffix not in SUPPORTED_SUFFIXES:
      errors.append(f"{relative}: unsupported asset extension {suffix or '<none>'}")
    return errors
  if suffix not in SUPPORTED_SUFFIXES:
    return errors + [f"{relative}: unsupported asset extension {suffix or '<none>'}"]
  try:
    data = path.read_bytes()
  except OSError as error:
    return errors + [f"{relative}: cannot read file ({error})"]
  if suffix in SVG_SUFFIXES:
    errors.extend(_validate_svg(relative, data))
  elif suffix in RASTER_SUFFIXES:
    errors.extend(_validate_raster(relative, suffix, data))
  else:
    errors.extend(_validate_audio(relative, suffix, data))
  return errors


def _registry_paths(root: Path) -> tuple[set[str], list[str]]:
  paths: set[str] = set()
  errors: list[str] = []
  for registry in REGISTRIES:
    registry_path = root / registry
    if not registry_path.exists():
      continue
    try:
      document = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
      errors.append(f"{registry.as_posix()}: registry cannot be read ({error})")
      continue
    if not isinstance(document, dict):
      errors.append(f"{registry.as_posix()}: registry document must be an object")
      continue
    entries = document.get("entries")
    if not isinstance(entries, list):
      errors.append(f"{registry.as_posix()}: registry entries must be a list")
      continue
    for entry in entries:
      if not isinstance(entry, dict):
        errors.append(f"{registry.as_posix()}: registry entry must be an object")
        continue
      for field in ("source_path", "release_path"):
        candidate = entry.get(field)
        if not isinstance(candidate, str) or not candidate:
          continue
        suffix = Path(candidate).suffix.lower()
        if suffix in REGISTERED_RUNTIME_SUFFIXES:
          continue
        if field == "release_path":
          if not candidate.startswith(RELEASE_PREFIX):
            errors.append(f"{registry.as_posix()}: release_path must be under {RELEASE_PREFIX}: {candidate}")
          else:
            candidate_path = root / candidate
            if _contains_symlink(root, candidate_path):
              errors.append(f"{registry.as_posix()}: release_path cannot contain symlinks: {candidate}")
            try:
              resolved = candidate_path.resolve()
              resolved_relative = resolved.relative_to(root.resolve()).as_posix()
              if not resolved_relative.startswith(RELEASE_PREFIX):
                errors.append(f"{registry.as_posix()}: resolved release_path must remain under {RELEASE_PREFIX}: {candidate}")
            except ValueError:
              errors.append(f"{registry.as_posix()}: release_path escapes repository root: {candidate}")
        paths.add(candidate)
  return paths, errors


def _asset_files(root: Path) -> list[str]:
  paths: set[str] = set()
  for relative_root in ASSET_ROOTS:
    directory = root / relative_root
    if not directory.is_dir():
      continue
    for path in directory.rglob("*"):
      if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
        paths.add(path.relative_to(root).as_posix())
  registry_paths, _ = _registry_paths(root)
  paths.update(registry_paths)
  return sorted(paths)


def validate(root: Path) -> list[str]:
  _, errors = _registry_paths(root)
  for relative_path in _asset_files(root):
    errors.extend(validate_file(root, relative_path))
  return errors


def main() -> int:
  root = Path(__file__).resolve().parents[1]
  errors = validate(root)
  if errors:
    for error in errors:
      print(f"error: {error}", file=sys.stderr)
    return 1
  print(f"asset security check: passed ({len(_asset_files(root))} files)")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
