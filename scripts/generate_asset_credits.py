#!/usr/bin/env python3
"""Render or check deterministic asset credits from registry manifests."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REGISTRIES = (
  ("assets/registry/visual-assets.json", "Visual"),
  ("assets/registry/audio-assets.json", "Audio"),
)
NOTICE_TARGET = "assets/THIRD_PARTY_NOTICES.md"
RUNTIME_TARGET = "gui/asset-credits.mjs"


def project_version(root: Path) -> str:
  cargo = (root / "Cargo.toml").read_text(encoding="utf-8")
  match = re.search(r'^version\s*=\s*"([0-9]+\.[0-9]+\.[0-9]+)"$', cargo, re.MULTILINE)
  if match is None:
    raise ValueError("Cargo.toml package version is unavailable")
  return match.group(1)


def _registry_entries(root: Path) -> list[tuple[str, dict]]:
  entries: list[tuple[str, dict]] = []
  for relative_path, category in REGISTRIES:
    document = json.loads((root / relative_path).read_text(encoding="utf-8"))
    entries.extend((category, entry) for entry in document["entries"])
  return sorted(entries, key=lambda item: (item[0], item[1]["id"]))


def render(root: Path) -> str:
  entries = _registry_entries(root)
  version = project_version(root)
  has_third_party_release = any(
    entry["provenance"]["kind"] != "repository-authored"
    and entry["approval_status"] == "approved"
    and entry["release_path"]
    for _category, entry in entries
  )
  release_summary = (
    f"Third-party release assets in v{version} are detailed in the generated notice file."
    if has_third_party_release
    else f"No third-party release assets are included in v{version}."
  )
  lines = [
    "# Asset Credits", "",
    "This file is generated from `assets/registry/*.json`. Do not edit it",
    "directly; update a registry entry and run the credits check.", "",
    f"{release_summary} Runtime-generated",
    "visual tokens and Web Audio recipes remain optional presentation layers.", "",
    "| Type | ID | Source/generation | License | Attribution | Approval | Provenance | Source URL | Retrieved | License reference |",
    "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
  ]
  for category, entry in entries:
    source = entry["source_path"] or entry["creation_method"]
    provenance = entry["provenance"]
    lines.append(
      f"| {category} | `{entry['id']}` | `{source}` | {entry['license']} | "
      f"{entry['attribution_text']} | {entry['approval_status']} | {provenance['kind']} | "
      f"{provenance['source_url'] or '—'} | {provenance['retrieval_date'] or '—'} | "
      f"`{provenance['license_reference']}` |"
    )
  lines.extend([
    "", "Every entry also records its semantic role, visible source, accessible",
    "equivalent, modifications, and source/release hash fields in the registry.",
    f"Third-party release notices are generated separately in `{NOTICE_TARGET}`.", "",
    f"The static GUI credits disclosure is generated separately in `{RUNTIME_TARGET}`.", "",
  ])
  return "\n".join(lines)


def render_runtime(root: Path) -> str:
  entries = _registry_entries(root)
  records = []
  for category, entry in entries:
    records.append({
      "asset_type": category.lower(),
      "id": entry["id"],
      "source": entry["source_path"] or entry["creation_method"],
      "license": entry["license"],
      "attribution": entry["attribution_text"],
      "approval_status": entry["approval_status"],
      "provenance": entry["provenance"],
      "accessible_equivalent": entry["accessible_equivalent"],
      "release_status": "approved-release" if entry["release_path"] and entry["approval_status"] == "approved" else "not-released",
      "release_path": entry["release_path"],
    })
  third_party_release_count = sum(
    record["provenance"]["kind"] != "repository-authored"
    and record["release_status"] == "approved-release"
    for record in records
  )
  document = {
    "schema_version": "asset-credits-v1",
    "package_version": project_version(root),
    "registry_source": "assets/registry/*.json",
    "third_party_release_count": third_party_release_count,
    "entries": records,
  }
  payload = json.dumps(document, ensure_ascii=False, indent=2)
  return "\n".join([
    "// Generated from assets/registry/*.json; do not edit directly.",
    "// Regenerate with: python3 scripts/generate_asset_credits.py --runtime",
    f"export const ASSET_CREDITS = Object.freeze({payload});",
    "",
  ])


def render_notices(root: Path) -> str:
  entries = [entry for _category, entry in _registry_entries(root)]
  entries = [
    entry for entry in entries
    if entry["provenance"]["kind"] != "repository-authored"
    and entry["approval_status"] == "approved"
    and entry["release_path"]
  ]
  entries.sort(key=lambda entry: entry["id"])
  lines = [
    "# Third-party notices", "",
    "This file is generated from `assets/registry/*.json`. Do not edit it",
    "directly; update a registry entry and run the credits check.", "",
  ]
  if not entries:
    lines.extend([
      f"No third-party release assets are included in v{project_version(root)}.",
      "All current release-capable entries are repository-authored and use the",
      "project asset-licensing policy as their license reference.", "",
    ])
    return "\n".join(lines)
  lines.extend([f"The following third-party assets are distributed in v{project_version(root)}:", ""])
  for entry in entries:
    provenance = entry["provenance"]
    lines.extend([
      f"## `{entry['id']}`", "",
      f"- License: {entry['license']}",
      f"- Attribution: {entry['attribution_text']}",
      f"- Source URL: {provenance['source_url']}",
      f"- Retrieved: {provenance['retrieval_date']}",
      f"- License reference: `{provenance['license_reference']}`",
      f"- Release path: `{entry['release_path']}`", "",
    ])
  return "\n".join(lines)


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--check", action="store_true", help="check the generated file")
  parser.add_argument("--notices", action="store_true", help="render third-party notices")
  parser.add_argument("--runtime", action="store_true", help="render the GUI runtime projection")
  args = parser.parse_args()
  root = Path(__file__).resolve().parents[1]
  if args.runtime:
    print(render_runtime(root), end="")
    return 0
  if args.notices:
    print(render_notices(root), end="")
    return 0
  output = render(root)
  target = root / "assets" / "ASSET_CREDITS.md"
  if args.check:
    actual = target.read_text(encoding="utf-8")
    if actual != output:
      print(f"asset credits check: stale {target}")
      return 1
    notices = root / NOTICE_TARGET
    if notices.read_text(encoding="utf-8") != render_notices(root):
      print(f"asset credits check: stale {notices}")
      return 1
    runtime = root / RUNTIME_TARGET
    if runtime.read_text(encoding="utf-8") != render_runtime(root):
      print(f"asset credits check: stale {runtime}")
      return 1
    print("asset credits check: passed")
    return 0
  print(output, end="")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
