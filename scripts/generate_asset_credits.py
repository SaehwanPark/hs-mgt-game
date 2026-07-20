#!/usr/bin/env python3
"""Render or check deterministic asset credits from registry manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REGISTRIES = (
  ("assets/registry/visual-assets.json", "Visual"),
  ("assets/registry/audio-assets.json", "Audio"),
)


def render(root: Path) -> str:
  entries: list[tuple[str, dict]] = []
  for relative_path, category in REGISTRIES:
    document = json.loads((root / relative_path).read_text(encoding="utf-8"))
    entries.extend((category, entry) for entry in document["entries"])
  entries.sort(key=lambda item: (item[0], item[1]["id"]))
  lines = [
    "# Asset Credits", "",
    "This file is generated from `assets/registry/*.json`. Do not edit it",
    "directly; update a registry entry and run the credits check.", "",
    "No third-party release assets are included in v0.12.53. Runtime-generated",
    "visual tokens and Web Audio recipes remain optional presentation layers.", "",
    "| Type | ID | Source/generation | License | Attribution | Approval |",
    "| --- | --- | --- | --- | --- | --- |",
  ]
  for category, entry in entries:
    source = entry["source_path"] or entry["creation_method"]
    lines.append(
      f"| {category} | `{entry['id']}` | `{source}` | {entry['license']} | "
      f"{entry['attribution_text']} | {entry['approval_status']} |"
    )
  lines.extend([
    "", "Every entry also records its semantic role, visible source, accessible",
    "equivalent, modifications, and source/release hash fields in the registry.", "",
  ])
  return "\n".join(lines)


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--check", action="store_true", help="check the generated file")
  args = parser.parse_args()
  root = Path(__file__).resolve().parents[1]
  output = render(root)
  target = root / "assets" / "ASSET_CREDITS.md"
  if args.check:
    actual = target.read_text(encoding="utf-8")
    if actual != output:
      print(f"asset credits check: stale {target}")
      return 1
    print("asset credits check: passed")
    return 0
  print(output, end="")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
