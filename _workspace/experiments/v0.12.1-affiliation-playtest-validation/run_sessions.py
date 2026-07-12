"""Capture and audit a bounded regional-affiliation MCP playtest matrix.

The artifact is intentionally read-only with respect to simulation semantics.
It records the observation and legal-command surface before each submitted
command, then validates the returned transition summary and debrief linkage.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PLAY_GAME_PATH = ROOT / "scripts" / "play_game.py"
PLAY_GAME_SPEC = importlib.util.spec_from_file_location("play_game", PLAY_GAME_PATH)
PLAY_GAME = importlib.util.module_from_spec(PLAY_GAME_SPEC)
assert PLAY_GAME_SPEC.loader is not None
PLAY_GAME_SPEC.loader.exec_module(PLAY_GAME)


ARTIFACT_TYPE = "regional-affiliation-phase7-playtest"
BATCH_ID = "v0.12.1-affiliation-playtest-validation"
CODE_VERSION = "0.12.1"
CAMPAIGN = "regional-affiliation-v1"
SEEDS = (42, 43, 44)
PROFILES = (
  {
    "id": "independent",
    "name": "Independent posture",
    "posture": "independent",
    "description": "Assess the partner, remain independent, and preserve cash and optionality.",
  },
  {
    "id": "deferred",
    "name": "Deferred posture",
    "posture": "defer",
    "description": "Assess the partner, defer pursuit, and gather no further commitment exposure.",
  },
  {
    "id": "pursuit",
    "name": "Affiliation pursuit",
    "posture": "pursue",
    "description": "Assess the partner, submit the maximum legal commitment package, and integrate when approved.",
  },
)
PROFILE_BY_ID = {profile["id"]: profile for profile in PROFILES}
TYPED_CONTEXT_FIELDS = ("alternatives", "assumptions", "commitments")
RESPONSE_FIELDS = ("partner", "review", "labor", "payer", "community")


def _legal_command_contains(legal_commands: list[str], token: str) -> bool:
  return any(token in command for command in legal_commands)


def policy_for(profile_id: str):
  """Return an observation/legal-hint-only policy for one profile."""

  profile = PROFILE_BY_ID[profile_id]

  def choose(_observation: list[str], legal_commands: list[str], turn: int) -> str:
    if turn == 1:
      return "assess"
    if turn == 2:
      return f"posture choice={profile['posture']}"
    if turn == 3:
      if profile["posture"] == "pursue":
        return "commit community=6 workforce=6 continuity=6"
      return "hold"
    if turn == 4:
      return "submit_review" if _legal_command_contains(legal_commands, "submit_review") else "hold"
    if turn == 5:
      return "await_review" if _legal_command_contains(legal_commands, "await_review") else "hold"
    if turn == 6:
      return "integrate decision=begin" if _legal_command_contains(legal_commands, "integrate") else "hold"
    raise AssertionError(f"unexpected affiliation turn {turn}")

  return choose


def _final_status(debrief: list[str]) -> str | None:
  for line in debrief:
    if line.startswith("Final status: "):
      return line.removeprefix("Final status: ")
  return None


def _stage_lines(debrief: list[str]) -> list[str]:
  return [line for line in debrief if line.startswith("Stage ")]


def _response_values(stage_lines: list[str]) -> dict[str, list[str]]:
  values = {field: set() for field in RESPONSE_FIELDS}
  for line in stage_lines:
    for field in RESPONSE_FIELDS:
      match = re.search(rf"\b{field} ([A-Za-z]+)", line)
      if match:
        values[field].add(match.group(1))
  return {field: sorted(field_values) for field, field_values in values.items()}


def _observation_field_present(run: dict, field: str) -> bool:
  labels = {
    "alternatives": r"\balternatives?\s*:",
    "assumptions": r"\bassumptions?\s*:",
    "commitments": r"\bcommitments?\s*:",
  }
  return any(
    re.search(labels[field], line.lower()) is not None
    for trace in run["turn_trace"]
    for line in trace["observation"]
  )


def _capture_run(profile_id: str, seed: int) -> dict:
  result = PLAY_GAME.play_session(
    CAMPAIGN,
    seed=seed,
    policy_fn=policy_for(profile_id),
    capture_trace=True,
  )
  assert result is not None
  history = result["history"]
  debrief = result["debrief"]
  return {
    "profile_id": profile_id,
    "profile_name": PROFILE_BY_ID[profile_id]["name"],
    "posture": PROFILE_BY_ID[profile_id]["posture"],
    "policy_description": PROFILE_BY_ID[profile_id]["description"],
    "decision_source": "deterministic policy using only actor-visible observations and legal command hints",
    "campaign": result["campaign"],
    "seed": result["seed"],
    "difficulty": result["difficulty"],
    "completion_status": "complete" if len(history) == 6 else "incomplete",
    "transition_count": len(history),
    "history": history,
    "state_hashes": [transition["state_hash"] for transition in history],
    "final_hash": history[-1]["state_hash"] if history else None,
    "turn_trace": result["turn_trace"],
    "validation_failures": result["validation_failures"],
    "final_observation": result["final_observation"],
    "debrief": debrief,
    "final_status": _final_status(debrief),
  }


def build_artifact() -> dict:
  runs = [
    _capture_run(profile["id"], seed)
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

  expected_coordinates = {
    (profile["id"], seed) for profile in PROFILES for seed in SEEDS
  }
  actual_coordinates = {(run["profile_id"], run["seed"]) for run in artifact["runs"]}
  assert actual_coordinates == expected_coordinates
  assert len(artifact["runs"]) == len(expected_coordinates)

  for run in artifact["runs"]:
    assert run["campaign"] == CAMPAIGN
    assert run["difficulty"] is None
    assert run["completion_status"] == "complete"
    assert run["transition_count"] == 6
    assert len(run["history"]) == 6
    assert len(run["state_hashes"]) == 6
    assert run["state_hashes"] == [
      transition["state_hash"] for transition in run["history"]
    ]
    assert run["final_hash"] == run["state_hashes"][-1]
    assert run["final_status"] is not None
    assert run["validation_failures"] == []
    assert len(run["turn_trace"]) == 6
    assert len(_stage_lines(run["debrief"])) == 6
    assert "Decision quality:" in "\n".join(run["debrief"])
    assert "Actor utility and social welfare are separate:" in "\n".join(run["debrief"])

    for expected_turn, (transition, trace) in enumerate(
      zip(run["history"], run["turn_trace"], strict=True),
      start=1,
    ):
      assert transition["turn"] == expected_turn
      assert trace["turn"] == expected_turn
      assert trace["latest_transition"] == transition
      assert trace["done_after_submit"] is (expected_turn == 6)
      assert isinstance(trace["observation"], list)
      assert isinstance(trace["legal_commands"], list)
      assert trace["validation_failures"] == []


def build_audit(artifact: dict) -> dict:
  validate_artifact(artifact)
  reports = []
  final_statuses = {}
  response_coverage = {field: set() for field in RESPONSE_FIELDS}
  missing_fields = set()
  total_observations = 0
  total_stage_lines = 0

  for run in artifact["runs"]:
    stage_lines = _stage_lines(run["debrief"])
    responses = _response_values(stage_lines)
    for field, values in responses.items():
      response_coverage[field].update(values)
    for field in TYPED_CONTEXT_FIELDS:
      if not _observation_field_present(run, field):
        missing_fields.add(field)
    total_observations += len(run["turn_trace"])
    total_stage_lines += len(stage_lines)
    final_statuses[run["final_status"]] = final_statuses.get(run["final_status"], 0) + 1
    reports.append(
      {
        "profile_id": run["profile_id"],
        "seed": run["seed"],
        "final_status": run["final_status"],
        "final_hash": run["final_hash"],
        "transition_count": run["transition_count"],
        "observation_count": len(run["turn_trace"]),
        "stage_line_count": len(stage_lines),
        "response_coverage": responses,
        "missing_typed_context_fields": sorted(
          field
          for field in TYPED_CONTEXT_FIELDS
          if not _observation_field_present(run, field)
        ),
      }
    )

  unexplained_gaps = []
  if missing_fields:
    unexplained_gaps.append(
      {
        "type": "decision-time context",
        "fields": sorted(missing_fields),
        "description": (
          "The typed AffiliationObservation exposes alternatives, assumptions, "
          "and commitments, but the MCP-rendered observation omits them across "
          "all nine captured runs. The debrief later asks the player to compare "
          "alternatives, so this is a bounded observation-context gap rather than "
          "evidence for balance or transition tuning."
        ),
      }
    )

  return {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "status": "supported_with_gap" if unexplained_gaps else "supported",
    "run_count": len(artifact["runs"]),
    "complete_run_count": sum(
      run["completion_status"] == "complete" for run in artifact["runs"]
    ),
    "transition_count": sum(run["transition_count"] for run in artifact["runs"]),
    "observation_count": total_observations,
    "debrief_stage_line_count": total_stage_lines,
    "validation_failure_count": sum(
      len(run["validation_failures"]) for run in artifact["runs"]
    ),
    "matrix": {
      "profiles": list(artifact["profiles"]),
      "seeds": list(artifact["seeds"]),
      "coordinates": len(artifact["runs"]),
    },
    "final_status_counts": dict(sorted(final_statuses.items())),
    "response_coverage": {
      field: sorted(values) for field, values in response_coverage.items()
    },
    "missing_typed_context_fields": sorted(missing_fields),
    "unexplained_gaps": unexplained_gaps,
    "unexplained_gap_count": len(unexplained_gaps),
    "runtime_promotion": "deferred",
    "next_bounded_candidate": "Expose typed affiliation observation context in the MCP surface, then rerun this audit.",
    "reports": reports,
    "evidence_limits": [
      "This is deterministic simulated-policy evidence, not human-learning or classroom-effectiveness evidence.",
      "The nine-run matrix does not establish general winnability, balance, calibration, legal validity, or policy forecasting.",
      "The observation-context gap supports an interface follow-up only; it does not justify runtime transition or ruleset tuning.",
    ],
  }


def validate_audit(audit: dict) -> None:
  assert audit["artifact_type"] == ARTIFACT_TYPE
  assert audit["batch_id"] == BATCH_ID
  assert audit["run_count"] == 9
  assert audit["complete_run_count"] == 9
  assert audit["transition_count"] == 54
  assert audit["observation_count"] == 54
  assert audit["debrief_stage_line_count"] == 54
  assert audit["validation_failure_count"] == 0
  assert audit["matrix"]["coordinates"] == 9
  assert audit["unexplained_gap_count"] == 1
  assert audit["missing_typed_context_fields"] == list(TYPED_CONTEXT_FIELDS)
  assert audit["runtime_promotion"] == "deferred"
  assert len(audit["reports"]) == 9


def render_markdown(audit: dict) -> str:
  validate_audit(audit)
  lines = [
    f"# Regional Affiliation Playtest Validation — `{audit['batch_id']}`",
    "",
    "- Code version: `0.12.1`",
    "- Campaign: `regional-affiliation-v1`",
    "- Matrix: independent, deferred, and pursuit × seeds `42`, `43`, `44`",
    "- Evidence type: deterministic simulated-policy MCP trace and debrief audit",
    f"- Status: `{audit['status']}`",
    f"- Runtime promotion: `{audit['runtime_promotion']}`",
    "",
    "## Coverage",
    "",
    "| Measure | Count |",
    "| --- | ---: |",
    f"| Complete runs | {audit['complete_run_count']} / {audit['run_count']} |",
    f"| Committed stages | {audit['transition_count']} |",
    f"| Pre-command observations | {audit['observation_count']} |",
    f"| Debrief stage lines | {audit['debrief_stage_line_count']} |",
    f"| Unexpected validation failures | {audit['validation_failure_count']} |",
    "",
    "## Final statuses",
    "",
  ]
  for status, count in audit["final_status_counts"].items():
    lines.append(f"- `{status}`: {count}")
  lines.extend(["", "## Actor-response coverage", ""])
  for field in RESPONSE_FIELDS:
    values = audit["response_coverage"][field]
    lines.append(f"- `{field}`: {', '.join(f'`{value}`' for value in values)}")
  lines.extend(["", "## Concrete gap", ""])
  for gap in audit["unexplained_gaps"]:
    lines.append(
      f"- **{gap['type']}** (`{', '.join(gap['fields'])}`): {gap['description']}"
    )
  lines.extend(["", "Next bounded candidate: " + audit["next_bounded_candidate"], ""])
  lines.extend(["## Evidence limits", ""])
  lines.extend(f"- {limit}" for limit in audit["evidence_limits"])
  lines.append("")
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
