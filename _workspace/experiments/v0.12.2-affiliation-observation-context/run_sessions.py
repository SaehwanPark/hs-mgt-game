"""Capture and audit the v0.12.2 post-fix affiliation MCP matrix."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BASE_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.12.1-affiliation-playtest-validation"
  / "run_sessions.py"
)
HISTORICAL_ARTIFACT_PATH = BASE_PATH.with_name("results.json")
BASE_SPEC = importlib.util.spec_from_file_location("affiliation_playtest_base", BASE_PATH)
BASE = importlib.util.module_from_spec(BASE_SPEC)
assert BASE_SPEC.loader is not None
BASE_SPEC.loader.exec_module(BASE)


ARTIFACT_TYPE = "regional-affiliation-observation-context"
BATCH_ID = "v0.12.2-affiliation-observation-context"
CODE_VERSION = "0.12.2"
CAMPAIGN = BASE.CAMPAIGN
SEEDS = BASE.SEEDS
PROFILES = BASE.PROFILES
REQUIRED_LABELS = ("Commitments:", "Alternative:", "Assumption:")


def _base_artifact_view(artifact: dict) -> dict:
  """Adapt the post-fix artifact to the historical structural validator."""

  view = dict(artifact)
  view.update(
    {
      "artifact_type": BASE.ARTIFACT_TYPE,
      "batch_id": BASE.BATCH_ID,
      "code_version": BASE.CODE_VERSION,
      "runtime_promotion": "deferred",
    }
  )
  return view


def _context_lines(observation: list[str], label: str) -> list[str]:
  return [line for line in observation if line.startswith(label)]


def _assert_history_unchanged(artifact: dict) -> None:
  historical = json.loads(HISTORICAL_ARTIFACT_PATH.read_text())
  historical_runs = {
    (run["profile_id"], run["seed"]): run for run in historical["runs"]
  }
  current_runs = {
    (run["profile_id"], run["seed"]): run for run in artifact["runs"]
  }
  assert current_runs.keys() == historical_runs.keys()
  for coordinate, run in current_runs.items():
    historical_run = historical_runs[coordinate]
    assert run["state_hashes"] == historical_run["state_hashes"]
    assert run["history"] == historical_run["history"]


def build_artifact() -> dict:
  runs = [
    BASE._capture_run(profile["id"], seed)
    for profile in PROFILES
    for seed in SEEDS
  ]
  artifact = {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "seeds": list(SEEDS),
    "profiles": [profile["id"] for profile in PROFILES],
    "runtime_promotion": "deferred",
    "runs": runs,
  }
  validate_artifact(artifact)
  return artifact


def validate_artifact(artifact: dict) -> None:
  assert artifact["artifact_type"] == ARTIFACT_TYPE
  assert artifact["batch_id"] == BATCH_ID
  assert artifact["code_version"] == CODE_VERSION
  assert artifact["campaign"] == CAMPAIGN
  assert artifact["seeds"] == list(SEEDS)
  assert artifact["profiles"] == [profile["id"] for profile in PROFILES]
  assert artifact["runtime_promotion"] == "deferred"
  BASE.validate_artifact(_base_artifact_view(artifact))
  _assert_history_unchanged(artifact)

  for run in artifact["runs"]:
    for trace in run["turn_trace"]:
      observation = trace["observation"]
      for label in REQUIRED_LABELS:
        assert _context_lines(observation, label)
      assert len(_context_lines(observation, "Commitments:")) == 1
      assert len(_context_lines(observation, "Alternative:")) >= 2
      assert len(_context_lines(observation, "Assumption:")) == 2


def build_audit(artifact: dict) -> dict:
  validate_artifact(artifact)
  audit = BASE.build_audit(_base_artifact_view(artifact))
  audit.update(
    {
      "artifact_type": ARTIFACT_TYPE,
      "batch_id": BATCH_ID,
      "code_version": CODE_VERSION,
      "status": "supported",
      "missing_typed_context_fields": [],
      "unexplained_gaps": [],
      "unexplained_gap_count": 0,
      "runtime_promotion": "deferred",
      "history_unchanged": True,
      "next_bounded_candidate": "Continue evidence-only validation; no balance or transition change is promoted by this capture.",
    }
  )
  return audit


def validate_audit(audit: dict) -> None:
  assert audit["artifact_type"] == ARTIFACT_TYPE
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == CODE_VERSION
  assert audit["status"] == "supported"
  assert audit["run_count"] == 9
  assert audit["complete_run_count"] == 9
  assert audit["transition_count"] == 54
  assert audit["observation_count"] == 54
  assert audit["debrief_stage_line_count"] == 54
  assert audit["validation_failure_count"] == 0
  assert audit["missing_typed_context_fields"] == []
  assert audit["unexplained_gap_count"] == 0
  assert audit["runtime_promotion"] == "deferred"
  assert audit["history_unchanged"] is True
  assert len(audit["reports"]) == 9


def render_markdown(audit: dict) -> str:
  validate_audit(audit)
  lines = [
    f"# Regional Affiliation Observation Context — `{audit['batch_id']}`",
    "",
    "- Code version: `0.12.2`",
    "- Campaign: `regional-affiliation-v1`",
    "- Matrix: independent, deferred, and pursuit × seeds `42`, `43`, `44`",
    "- Evidence type: deterministic simulated-policy MCP post-fix audit",
    "- Status: `supported`",
    "- Runtime promotion for balance/transition changes: `deferred`",
    "",
    "## Coverage",
    "",
    "| Measure | Count |",
    "| --- | ---: |",
    f"| Complete runs | {audit['complete_run_count']} / {audit['run_count']} |",
    f"| Committed stages | {audit['transition_count']} |",
    f"| Observations with commitments/alternatives/assumptions | {audit['observation_count']} |",
    f"| Debrief stage lines | {audit['debrief_stage_line_count']} |",
    f"| Unexpected validation failures | {audit['validation_failure_count']} |",
    "| Missing typed context fields | 0 |",
    "",
    "## Result",
    "",
    "- The v0.12.1 decision-time context gap is closed at the MCP rendering boundary.",
    "- The post-fix capture preserves the same transition/state-hash/debrief matrix.",
    "- The post-fix transition summaries and state hashes exactly match v0.12.1.",
    "- No balance, transition, legal, winnability, or human-learning claim is made.",
    "",
    "## Evidence limits",
    "",
    "- This is deterministic simulated-policy evidence, not human-learning or classroom-effectiveness evidence.",
    "- The capture does not establish general winnability, balance, calibration, legal validity, or policy forecasting.",
    "- Further gameplay or educational gaps require separate evidence before runtime promotion.",
    "",
  ]
  return "\n".join(lines)


def write_json(path: Path, value: dict) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument(
    "--output",
    type=Path,
    default=Path(__file__).with_name("results.json"),
  )
  parser.add_argument(
    "--diagnostics",
    type=Path,
    default=Path(__file__).with_name("diagnostics.md"),
  )
  args = parser.parse_args()

  artifact = build_artifact()
  audit = build_audit(artifact)
  validate_audit(audit)
  write_json(args.output, artifact)
  args.diagnostics.parent.mkdir(parents=True, exist_ok=True)
  args.diagnostics.write_text(render_markdown(audit))
  print(f"Captured {audit['run_count']} runs and {audit['transition_count']} stages.")
  print(f"Diagnostics written to {args.diagnostics}")


if __name__ == "__main__":
  main()
