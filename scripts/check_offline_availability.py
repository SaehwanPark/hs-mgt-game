#!/usr/bin/env python3
"""Check that the live GUI package is embedded and served locally."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path


POLICY_PATH = "assets/offline-policy.json"
LOADING_POLICY_PATH = "assets/loading-policy.json"
REPORT_SCHEMA_VERSION = "offline-policy-report-v1"
REQUIRED_FIELDS = (
  "schema_version",
  "server_source",
  "entrypoint_source",
  "entrypoint_urls",
  "local_origin",
  "embedded_resources",
)
RESOURCE_KINDS = {"entrypoint", "host-adapter", "module", "catalog"}
SOURCE_SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
CODE_SCHEME_PATTERN = re.compile(r"\b(?:data|javascript|blob|file|ftp|https?|ws|wss):", re.IGNORECASE)
HTML_EXTERNAL_SOURCE_PATTERN = re.compile(
  r"<(?:script|link|img|audio|video|source)\b[^>]*"
  r"(?:src|href|srcset)\s*=\s*[\"'](?:[A-Za-z][A-Za-z0-9+.-]*:|//)",
  re.IGNORECASE,
)


def _resolve(root: Path, relative: str) -> Path:
  candidate = Path(relative)
  if candidate.is_absolute():
    raise ValueError("path must be relative to repository root")
  resolved = (root / candidate).resolve()
  resolved_root = root.resolve()
  if resolved != resolved_root and resolved_root not in resolved.parents:
    raise ValueError("path escapes repository root")
  return resolved


def _symlink_components(root: Path, relative: str) -> list[Path]:
  current = root
  symlinks = []
  for part in Path(relative).parts:
    if part in ("", "."):
      continue
    current /= part
    if current.is_symlink():
      symlinks.append(current)
  return symlinks


def _valid_string_list(value: object) -> bool:
  return isinstance(value, list) and bool(value) and all(
    isinstance(item, str) and item.strip() for item in value
  )


def validate_definition(root: Path, document: object) -> list[str]:
  if not isinstance(document, dict):
    return ["offline policy document must be an object"]
  errors = []
  if document.get("schema_version") != "offline-policy-v1":
    errors.append("unsupported offline policy schema_version")
  for field in REQUIRED_FIELDS:
    if field not in document:
      errors.append(f"missing field {field!r}")

  for field in ("server_source", "entrypoint_source"):
    value = document.get(field)
    if not isinstance(value, str) or not value.strip():
      errors.append(f"{field} must be a non-empty relative path")
      continue
    try:
      resolved = _resolve(root, value)
    except ValueError as error:
      errors.append(f"{field} is invalid: {error}")
      continue
    if not resolved.is_file():
      errors.append(f"{field} does not exist: {value}")
    if _symlink_components(root, value):
      errors.append(f"{field} path cannot contain symlinks: {value}")

  entrypoint_urls = document.get("entrypoint_urls")
  if not _valid_string_list(entrypoint_urls) or any(
    not value.startswith("/") or "?" in value or "#" in value for value in entrypoint_urls
  ):
    errors.append("entrypoint_urls must be non-empty absolute URL paths without query or fragment")

  local_origin = document.get("local_origin")
  if not isinstance(local_origin, dict):
    errors.append("local_origin must be an object")
  else:
    if local_origin.get("binding") != "loopback-only":
      errors.append("local_origin.binding must be loopback-only")
    if local_origin.get("default_bind") != "127.0.0.1:7878":
      errors.append("local_origin.default_bind must be 127.0.0.1:7878")
    if local_origin.get("api_prefix") != "/api/v1/sessions":
      errors.append("local_origin.api_prefix must be /api/v1/sessions")

  resources = document.get("embedded_resources")
  if not isinstance(resources, list) or not resources:
    errors.append("embedded_resources must be a non-empty list")
    resources = []
  seen_urls = set()
  seen_sources = set()
  for index, resource in enumerate(resources):
    if not isinstance(resource, dict):
      errors.append(f"embedded resource {index} must be an object")
      continue
    urls = resource.get("urls")
    source = resource.get("source")
    kind = resource.get("kind")
    if not _valid_string_list(urls) or any(
      not url.startswith("/") or "?" in url or "#" in url for url in urls
    ):
      errors.append(f"embedded resource {index} urls are invalid")
    else:
      for url in urls:
        if url in seen_urls:
          errors.append(f"duplicate embedded route: {url}")
        seen_urls.add(url)
    if not isinstance(source, str) or not source.strip():
      errors.append(f"embedded resource {index} source must be a path")
    else:
      if SOURCE_SCHEME_PATTERN.match(source):
        errors.append(f"embedded resource {index} source must be repository-local: {source}")
      try:
        resolved = _resolve(root, source)
      except ValueError as error:
        errors.append(f"embedded resource {index} source is invalid: {error}")
      else:
        if not resolved.is_file():
          errors.append(f"embedded resource {index} source does not exist: {source}")
        if _symlink_components(root, source):
          errors.append(f"embedded resource {index} source cannot contain symlinks: {source}")
      if source in seen_sources:
        errors.append(f"duplicate embedded source: {source}")
      seen_sources.add(source)
    if kind not in RESOURCE_KINDS:
      errors.append(f"embedded resource {index} has unsupported kind: {kind}")

  if document.get("entrypoint_source") not in seen_sources:
    errors.append("entrypoint_source must be included in embedded_resources")
  if isinstance(entrypoint_urls, list) and not set(entrypoint_urls).issubset(seen_urls):
    errors.append("entrypoint_urls must be covered by embedded_resources")
  return errors


def _load_loading_checker():
  path = Path(__file__).with_name("check_loading_policy.py")
  spec = importlib.util.spec_from_file_location("check_loading_policy", path)
  if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load {path}")
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


def _loading_document(root: Path) -> object:
  return json.loads((root / LOADING_POLICY_PATH).read_text(encoding="utf-8"))


def route_errors(root: Path, document: dict) -> list[str]:
  server_source = document["server_source"]
  server_text = _resolve(root, server_source).read_text(encoding="utf-8")
  errors = []
  if 'DEFAULT_BIND: &str = "127.0.0.1:7878"' not in server_text:
    errors.append("server does not record the expected loopback default bind")
  if "ensure_loopback" not in server_text or "is_loopback()" not in server_text:
    errors.append("server does not enforce loopback binding")
  api_prefix = document["local_origin"]["api_prefix"]
  if api_prefix not in server_text:
    errors.append(f"server does not expose the declared API prefix: {api_prefix}")
  host_adapter_text = _resolve(root, "gui/host-adapter.mjs").read_text(encoding="utf-8")
  if f'const API_ROOT = "{api_prefix}";' not in host_adapter_text:
    errors.append("host adapter does not use the declared same-origin API prefix")

  for resource in document["embedded_resources"]:
    source = resource["source"]
    source_marker = f'include_str!("../{source}")'
    route_marker = " | ".join(f'"{url}"' for url in resource["urls"]) + " => ("
    route_start = server_text.find(route_marker)
    if route_start < 0:
      errors.append(f"server does not route declared URL set: {resource['urls']}")
      route_arm = ""
    else:
      route_end = server_text.find("\n    ),", route_start)
      route_arm = server_text[route_start:] if route_end < 0 else server_text[route_start:route_end]
    if source_marker not in route_arm:
      errors.append(f"server route does not embed its declared source: {resource['urls']} -> {source}")
    source_text = _resolve(root, source).read_text(encoding="utf-8")
    normalized_text = source_text.replace("http://www.w3.org/2000/svg", "")
    if CODE_SCHEME_PATTERN.search(normalized_text):
      errors.append(f"embedded source contains a non-local URL scheme: {source}")
    if resource["kind"] == "entrypoint" and HTML_EXTERNAL_SOURCE_PATTERN.search(source_text):
      errors.append(f"entrypoint contains an external HTML source: {source}")
  return errors


def build_report(root: Path, document: object) -> dict:
  errors = validate_definition(root, document)
  if not isinstance(document, dict) or errors:
    return {
      "schema_version": REPORT_SCHEMA_VERSION,
      "status": "fail",
      "errors": errors,
      "resource_count": 0,
      "route_count": 0,
    }

  loading_document = None
  try:
    loading_checker = _load_loading_checker()
    loading_document = _loading_document(root)
    loading_report = loading_checker.build_report(root, loading_document)
  except (OSError, json.JSONDecodeError, RuntimeError) as error:
    loading_report = {"status": "fail", "errors": [str(error)]}
  if loading_report["status"] != "pass":
    errors.extend(f"loading policy: {error}" for error in loading_report.get("errors", []))

  expected_sources = set(loading_document.get("live_files", [])) if isinstance(loading_document, dict) else set()
  expected_sources.update({"gui/host-adapter.mjs", "gui/audio-catalog.json", "gui/visual-catalog.json"})
  actual_sources = {resource["source"] for resource in document["embedded_resources"]}
  for source in sorted(expected_sources - actual_sources):
    errors.append(f"live source is not embedded in offline policy: {source}")
  for source in sorted(actual_sources - expected_sources):
    errors.append(f"offline policy embeds a non-live source: {source}")
  errors.extend(route_errors(root, document))
  route_count = sum(len(resource["urls"]) for resource in document["embedded_resources"])
  return {
    "schema_version": REPORT_SCHEMA_VERSION,
    "status": "pass" if not errors else "fail",
    "errors": errors,
    "resource_count": len(document["embedded_resources"]),
    "route_count": route_count,
    "entrypoint_source": document["entrypoint_source"],
    "local_origin": document["local_origin"],
    "loading_policy_status": loading_report["status"],
    "embedded_sources": sorted(actual_sources),
  }


def main() -> int:
  root = Path(__file__).resolve().parents[1]
  try:
    document = json.loads((root / POLICY_PATH).read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError) as error:
    report = {"schema_version": REPORT_SCHEMA_VERSION, "status": "fail", "errors": [str(error)]}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1
  report = build_report(root, document)
  print(json.dumps(report, indent=2, sort_keys=True))
  return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
  raise SystemExit(main())
