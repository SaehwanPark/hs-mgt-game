#!/usr/bin/env python3
"""Audit the bounded visual/audio first-month contract without running the game."""

import argparse
import json
from pathlib import Path


CONTRACT_SCHEMA = "visual-audio-first-month-contract-v1"
PHASE_DOCUMENTS = tuple(
  [
    "docs/history/initiatives/visual-audio/visual-audio-phase0-alignment-v0.12.16.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase1-static-desktop-v0.12.17.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase2-live-read-only-v0.12.18.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase3-contextual-actions-v0.12.19.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase4-resolution-causal-v0.12.20.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase5-foundational-audio-v0.12.21.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase6-regional-world-v0.12.22.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase7-campaign-coverage-v0.12.23.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase8-ai-agent-testplay-v0.12.24.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase9-ai-agent-evaluation-v0.12.25.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase10-accessibility-v0.12.26.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase11-session-launch-v0.12.27.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase12-visual-identity-v0.12.28.md",
    "docs/history/initiatives/visual-audio/visual-audio-phase13-first-month-continuity-v0.12.29.md",
  ]
)
PROVENANCE_FILES = (
  "gui/audio-catalog.json",
  "gui/visual-catalog.json",
  "gui/ASSET_CREDITS.md",
)
BOUNDARY_FILES = (
  "gui/app.mjs",
  "gui/audio.mjs",
  "gui/first-month.mjs",
  "gui/playtest.mjs",
  "gui/visual.mjs",
)
FORBIDDEN_BOUNDARY_MARKERS = (
  "transition_competitive",
  "resolved_inputs",
  "effect_queue",
  "fetch(",
  "WebSocket",
)


CONTRACT_REQUIREMENTS = (
  {
    "id": "launch_load",
    "label": "Start or load a host session",
    "sources": {
      "gui/app.mjs": ("createSessionLauncher", "startSession", "loadExisting"),
    },
    "tests": {
      "tests/test_gui_session_launch.py": ("startSession", "session_id"),
    },
  },
  {
    "id": "market_inspection",
    "label": "Inspect the actor-visible regional market",
    "sources": {
      "gui/app.mjs": ("renderRegionalWorld", "competitive-regional-world-v1"),
    },
    "tests": {
      "tests/test_gui_regional_world.py": ("renderRegionalWorld", "effect_queue"),
    },
  },
  {
    "id": "owned_facilities",
    "label": "Inspect Riverside and its facilities",
    "sources": {
      "gui/app.mjs": ("renderSelectedEntity", "facilities", "Riverside"),
    },
    "tests": {
      "tests/test_gui_static_desktop.py": ("facilities", "Public rival"),
    },
  },
  {
    "id": "visible_pressure_intelligence",
    "label": "Identify visible workforce/capacity pressure and payer/rival context",
    "sources": {
      "gui/app.mjs": ("renderBriefing", "workforce", "capacity", "Public rival"),
      "gui/visual-catalog.json": ("staffing", "capacity", "payer-policy"),
    },
    "tests": {
      "tests/test_gui_static_desktop.py": ("Workforce trust", "Access", "Public rival"),
      "tests/test_gui_regional_world.py": ("Private rival operations", "PUBLIC_RIVAL_LAG_MONTHS"),
    },
  },
  {
    "id": "contextual_actions",
    "label": "Draft at least two contextual actions with canonical metadata",
    "sources": {
      "gui/app.mjs": ("renderActionCatalog", "command_template", "drafts"),
    },
    "tests": {
      "tests/test_gui_contextual_actions.py": ("validateTurn", "actionCommand"),
      "tests/test_gui_first_month.py": ("drafts.length", "continue"),
    },
  },
  {
    "id": "canonical_submission",
    "label": "Validate and submit only through the host boundary",
    "sources": {
      "gui/app.mjs": ("validateTurn", "submitTurn", "unchanged"),
    },
    "tests": {
      "tests/test_gui_contextual_actions.py": ("submitTurn", "validation_required"),
      "tests/test_gui_first_month.py": ("validated", "submit"),
    },
  },
  {
    "id": "resolution_metrics",
    "label": "Review committed resolution and updated operating/resource metrics",
    "sources": {
      "gui/app.mjs": ("createResolutionClient", "snapshotItems", "Revenue", "Margin"),
    },
    "tests": {
      "tests/test_gui_resolution.py": ("competitive-resolution-v1", "resolution-effect-list"),
    },
  },
  {
    "id": "causal_feedback",
    "label": "Inspect direct committed causal effects and pending processes",
    "sources": {
      "gui/app.mjs": ("renderResolution", "effects", "pending"),
    },
    "tests": {
      "tests/test_gui_resolution.py": ("effects", "resolution-effect-list"),
    },
  },
  {
    "id": "optional_audio",
    "label": "Receive optional visible-only audio with complete text equivalents",
    "sources": {
      "gui/audio.mjs": ("AUDIO_CATALOG", "visibleEventCues", "reducedNotifications"),
      "gui/index.html": ("audio-mute", "audio-reduced-notifications"),
    },
    "tests": {
      "tests/test_gui_audio.py": ("AUDIO_CATALOG", "mute", "reducedNotifications"),
      "tests/test_gui_accessibility.py": ("text-equivalents", "text_equivalents"),
    },
  },
  {
    "id": "continuation",
    "label": "Continue to the next actor-visible observation",
    "sources": {
      "gui/first-month.mjs": (
        "competitive-first-month-v1",
        '"resolution"',
        '"continue"',
      ),
      "gui/app.mjs": ("resolutionVisible", "refreshed"),
    },
    "tests": {
      "tests/test_gui_first_month.py": ("competitive-first-month-v1", "continue", "refreshed"),
    },
  },
)


def _read(root, relative_path):
  path = root / relative_path
  if not path.is_file():
    return None
  return path.read_text(encoding="utf-8")


def _check_files_and_markers(root, entries):
  missing_files = []
  missing_markers = []
  evidence = []
  for relative_path in sorted(entries):
    content = _read(root, relative_path)
    if content is None:
      missing_files.append(relative_path)
      continue
    evidence.append(relative_path)
    for marker in entries[relative_path]:
      if marker not in content:
        missing_markers.append(f"{relative_path}:{marker}")
  return {
    "files": evidence,
    "missing_files": missing_files,
    "missing_markers": missing_markers,
    "status": "pass" if not missing_files and not missing_markers else "fail",
  }


def audit(root):
  requirements = []
  for requirement in CONTRACT_REQUIREMENTS:
    source_check = _check_files_and_markers(root, requirement["sources"])
    test_check = _check_files_and_markers(root, requirement["tests"])
    requirements.append(
      {
        "id": requirement["id"],
        "label": requirement["label"],
        "status": "pass" if source_check["status"] == test_check["status"] == "pass" else "fail",
        "claim_class": "technical/interface-task evidence",
        "source_evidence": source_check,
        "test_evidence": test_check,
      }
    )

  phase_documents = [
    {"path": path, "present": _read(root, path) is not None}
    for path in PHASE_DOCUMENTS
  ]
  provenance = [
    {"path": path, "present": _read(root, path) is not None}
    for path in PROVENANCE_FILES
  ]
  boundary_violations = []
  for relative_path in BOUNDARY_FILES:
    content = _read(root, relative_path)
    if content is None:
      boundary_violations.append(f"missing:{relative_path}")
      continue
    for marker in FORBIDDEN_BOUNDARY_MARKERS:
      if marker in content:
        boundary_violations.append(f"{relative_path}:{marker}")

  phase_status = "pass" if all(item["present"] for item in phase_documents) else "fail"
  provenance_status = "pass" if all(item["present"] for item in provenance) else "fail"
  boundary_status = "pass" if not boundary_violations else "fail"
  requirements_status = "pass" if all(item["status"] == "pass" for item in requirements) else "fail"
  overall_status = "complete" if all(
    status == "pass"
    for status in (phase_status, provenance_status, boundary_status, requirements_status)
  ) else "incomplete"
  return {
    "schema_version": CONTRACT_SCHEMA,
    "status": overall_status,
    "scope": "bounded technical first-month visual/audio contract",
    "requirements": requirements,
    "phase_documents": {"status": phase_status, "items": phase_documents},
    "provenance": {"status": provenance_status, "items": provenance},
    "presentation_boundary": {
      "status": boundary_status,
      "files": list(BOUNDARY_FILES),
      "forbidden_markers": list(FORBIDDEN_BOUNDARY_MARKERS),
      "violations": boundary_violations,
    },
    "evidence_limits": [
      "No browser transport, viewport rendering, contrast, screen-reader, or hardware-audio claim.",
      "No human usability, lived accessibility, learning, engagement, calibration, balance, policy-validity, or domain-expert claim.",
      "No claim that technical coverage is a production release or a calibrated policy forecast.",
    ],
  }


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--pretty", action="store_true", help="indent JSON output")
  args = parser.parse_args()
  result = audit(Path(__file__).resolve().parents[1])
  print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
  return 0 if result["status"] == "complete" else 1


if __name__ == "__main__":
  raise SystemExit(main())
