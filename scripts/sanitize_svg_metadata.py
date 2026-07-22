#!/usr/bin/env python3
"""Create explicit SVG derivatives without metadata elements."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from xml.parsers import expat

try:
  import verify_asset_release as release
except ModuleNotFoundError:  # pragma: no cover - supports repository imports.
  from scripts import verify_asset_release as release


DERIVATIVE_PREFIX = Path("assets/generation/svg-derivatives")


def _local_name(name: str) -> str:
  return name.rsplit("}", 1)[-1].rsplit(":", 1)[-1].lower()


def _tag_end(data: bytes, start: int) -> int:
  quote: int | None = None
  for index in range(start, len(data)):
    byte = data[index]
    if quote is not None:
      if byte == quote:
        quote = None
      continue
    if byte in (ord('"'), ord("'")):
      quote = byte
    elif byte == ord(">"):
      return index
  raise ValueError("malformed SVG/XML: unterminated tag")


def _metadata_ranges(data: bytes) -> list[tuple[int, int]]:
  try:
    data.decode("utf-8")
    parser = expat.ParserCreate(namespace_separator="}")
    stack: list[tuple[str, int | None]] = []
    ranges: list[tuple[int, int]] = []
    root_name: str | None = None

    def start_element(name: str, _attributes: dict[str, str]) -> None:
      nonlocal root_name
      start = parser.CurrentByteIndex
      end = _tag_end(data, start)
      tag = data[start:end + 1]
      is_metadata = _local_name(name) == "metadata"
      if root_name is None:
        root_name = name
      marker: int | None = None
      if is_metadata:
        if re.search(rb"/\s*>$", tag):
          ranges.append((start, end + 1))
        else:
          marker = start
      stack.append((name, marker))

    def end_element(_name: str) -> None:
      if not stack:
        raise ValueError("malformed SVG/XML: unbalanced element stack")
      _name, marker = stack.pop()
      if marker is not None:
        start = marker
        end = _tag_end(data, parser.CurrentByteIndex)
        ranges.append((start, end + 1))

    parser.StartElementHandler = start_element
    parser.EndElementHandler = end_element
    parser.Parse(data, True)
  except (UnicodeDecodeError, expat.ExpatError, ValueError) as error:
    if isinstance(error, ValueError) and str(error).startswith("malformed SVG/XML:"):
      raise
    raise ValueError(f"malformed SVG/XML: {error}") from error

  if root_name is None or _local_name(root_name) != "svg":
    raise ValueError("input root element must be svg")
  if stack:
    raise ValueError("malformed SVG/XML: unbalanced element stack")
  return ranges


def sanitize_svg_bytes(data: bytes) -> bytes:
  """Validate SVG bytes and remove only parsed ``metadata`` elements."""
  ranges = _metadata_ranges(data)
  if not ranges:
    return data

  merged_ranges: list[tuple[int, int]] = []
  for start, end in sorted(ranges):
    if merged_ranges and start <= merged_ranges[-1][1]:
      merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], end))
    else:
      merged_ranges.append((start, end))
  output = data
  for start, end in reversed(merged_ranges):
    output = output[:start] + output[end:]
  _metadata_ranges(output)
  return output


def _contains_symlink(root: Path, path: Path) -> bool:
  normalized_root = root.absolute()
  path = (path if path.is_absolute() else Path.cwd() / path).absolute()
  try:
    relative = path.relative_to(normalized_root)
  except ValueError:
    return False
  current = normalized_root
  for part in relative.parts:
    current /= part
    if current.is_symlink():
      return True
  return False


def _safe_input(root: Path, path: Path) -> Path:
  resolved_root = root.resolve()
  if _contains_symlink(root, path):
    raise ValueError("input path cannot contain symlinks")
  resolved = (path if path.is_absolute() else Path.cwd() / path).resolve()
  if resolved_root not in resolved.parents:
    raise ValueError("input path must remain inside the repository root")
  if not resolved.is_file():
    raise ValueError("input path does not exist or is not a file")
  if resolved.suffix.lower() != ".svg":
    raise ValueError("input path must have an .svg extension")
  return resolved


def _safe_output(root: Path, path: Path) -> Path:
  derivative_root = (root / DERIVATIVE_PREFIX).resolve()
  if _contains_symlink(root, path):
    raise ValueError("output path cannot contain symlinks")
  resolved = (path if path.is_absolute() else Path.cwd() / path).resolve()
  if derivative_root not in resolved.parents:
    raise ValueError(f"output path must remain under {DERIVATIVE_PREFIX.as_posix()}")
  if resolved.suffix.lower() != ".svg":
    raise ValueError("output path must have an .svg extension")
  if not resolved.parent.is_dir():
    raise ValueError("output parent directory does not exist")
  if resolved.exists():
    raise ValueError("output path already exists")
  return resolved


def sanitize_file(root: Path, input_path: Path, output_path: Path) -> Path:
  """Write one new derivative after validating all input and output boundaries."""
  source = _safe_input(root, input_path)
  target = _safe_output(root, output_path)
  output = sanitize_svg_bytes(source.read_bytes())
  created = False
  try:
    with target.open("xb") as stream:
      created = True
      stream.write(output)
  except FileExistsError as error:
    raise ValueError("output path already exists") from error
  except OSError as error:
    if created and target.is_file() and not target.is_symlink():
      target.unlink()
    raise ValueError(f"cannot write output path: {error}") from error
  return target


def check_release(root: Path) -> list[str]:
  """Check approved release SVGs without modifying any repository file."""
  records, errors = release._release_records(root)
  if errors:
    return errors
  for record in records:
    path = record["path"]
    if Path(path).suffix.lower() != ".svg":
      continue
    try:
      release_file = release._release_path(root, path)
      data = release_file.read_bytes()
      sanitized = sanitize_svg_bytes(data)
    except (OSError, ValueError) as error:
      errors.append(f"{path}: SVG metadata check failed ({error})")
      continue
    if sanitized != data:
      errors.append(f"{path}: contains removable SVG metadata")
  return errors


def _parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("input", nargs="?", type=Path, help="local SVG input")
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument("--output", type=Path, help="new derivative path")
  group.add_argument("--check-release", action="store_true", help="check approved release SVGs")
  return parser


def main(argv: list[str] | None = None) -> int:
  args = _parser().parse_args(argv)
  root = Path(__file__).resolve().parents[1]
  if args.check_release:
    if args.input is not None:
      _parser().error("--check-release does not accept an input path")
    errors = check_release(root)
    if errors:
      for error in errors:
        print(f"error: {error}", file=sys.stderr)
      return 1
    svg_count = sum(1 for record in release._release_records(root)[0] if Path(record["path"]).suffix.lower() == ".svg")
    print(f"SVG metadata release check: passed ({svg_count} files)")
    return 0
  if args.input is None:
    _parser().error("an input path is required with --output")
  try:
    target = sanitize_file(root, args.input, args.output)
  except (OSError, ValueError) as error:
    print(f"error: {error}", file=sys.stderr)
    return 1
  print(f"SVG metadata derivative: wrote {target.relative_to(root)}")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
