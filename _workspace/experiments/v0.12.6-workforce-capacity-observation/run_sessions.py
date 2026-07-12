#!/usr/bin/env python3
"""Capture and compare the v0.12.6 workforce-observation matrix."""

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

from play_game import play_session  # noqa: E402


SOURCE_RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.1-operating-loop-ai-validation"
  / "run_sessions.py"
)
SOURCE_SPEC = importlib.util.spec_from_file_location(
  "workforce_capacity_source_runner",
  SOURCE_RUNNER_PATH,
)
SOURCE_RUNNER = importlib.util.module_from_spec(SOURCE_SPEC)
assert SOURCE_SPEC.loader is not None
SOURCE_SPEC.loader.exec_module(SOURCE_RUNNER)


ARTIFACT_TYPE = "workforce_capacity_observation_validation"
BATCH_ID = "v0.12.6-workforce-capacity-observation"
CODE_VERSION = "0.12.6"
CAMPAIGN = "competitive-regional-v1"
RULESET = "competitive-ruleset-0.2.0"
STATE_HASH_SCHEMA = "competitive-state-hash-v9"
SEEDS = [42, 43, 44]
DIFFICULTIES = ["easy", "normal", "hard", "expert"]
PROFILES = list(SOURCE_RUNNER.PROFILES)
EXPECTED_TRANSITIONS = 24
GOLDEN_CONTROL_HASH = "61357596d8800592"
HIDDEN_MARKERS = (
  "role_targets",
  "effective_capacity",
  "allocation_queues",
  "pending_hire_outcomes",
  "rival_private_workforce_state",
  "future_actor_responses",
)
SOURCE_CONTRACTS = {
  "all_tiers": {
    "path": "_workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/results.json",
    "code_version": "0.11.11",
    "run_count": 60,
  },
  "expert": {
    "path": "_workspace/experiments/v0.11.9-expert-difficulty-validation/results.json",
    "code_version": "0.11.9",
    "run_count": 15,
  },
}
REQUIRED_TRACE_FIELDS = {
  "turn",
  "observation",
  "legal_commands",
  "submitted_command",
  "validation_failures",
  "latest_transition",
  "done_after_submit",
}


def expected_matrix():
  return [
    (profile, seed, difficulty)
    for profile in PROFILES
    for seed in SEEDS
    for difficulty in DIFFICULTIES
  ]


def expert_matrix():
  return [(profile, seed, "expert") for profile in PROFILES for seed in SEEDS]


def code_version():
  cargo = (ROOT / "Cargo.toml").read_text(encoding="utf-8")
  match = re.search(r'^version\s*=\s*"([^"]+)"', cargo, re.MULTILINE)
  return match.group(1) if match else "unknown"


def final_hash(result):
  return result["history"][-1]["state_hash"] if result["history"] else None


def failed_run(profile, seed, difficulty, source_id, error):
  return {
    "profile": profile,
    "seed": seed,
    "difficulty": difficulty,
    "source_id": source_id,
    "campaign": CAMPAIGN,
    "completion_status": "failed",
    "run_error": error,
    "transition_count": 0,
    "history": [],
    "state_hashes": [],
    "turn_trace": [],
    "validation_failures": [],
    "final_hash": None,
    "final_observation": [],
    "debrief": [],
  }


def run_profile(profile, seed, difficulty, source_id):
  try:
    result = play_session(
      CAMPAIGN,
      seed=seed,
      difficulty=difficulty,
      policy_fn=SOURCE_RUNNER.policy_for(profile),
      capture_trace=True,
    )
  except Exception as error:
    return failed_run(profile, seed, difficulty, source_id, str(error))

  if result is None:
    return failed_run(
      profile,
      seed,
      difficulty,
      source_id,
      "play_session returned no result",
    )

  history = result["history"]
  status = "complete" if len(history) == EXPECTED_TRANSITIONS else "incomplete"
  run = {
    "profile": profile,
    "seed": seed,
    "difficulty": difficulty,
    "source_id": source_id,
    "campaign": CAMPAIGN,
    "completion_status": status,
    "transition_count": len(history),
    "history": history,
    "state_hashes": [transition["state_hash"] for transition in history],
    "turn_trace": result.get("turn_trace", []),
    "validation_failures": result["validation_failures"],
    "final_hash": final_hash(result),
    "final_observation": result["final_observation"],
    "debrief": result["debrief"],
  }
  if status != "complete":
    run["run_error"] = (
      f"expected {EXPECTED_TRANSITIONS} transitions, got {len(history)}"
    )
  return run


def _history(run):
  return run.get("history", []) if isinstance(run, dict) else []


def _coordinate(run):
  return (run.get("profile"), run.get("seed"), run.get("difficulty"))


def _source_coordinate(run):
  return (
    run.get("profile", run.get("profile_name")),
    run.get("seed"),
    run.get("difficulty"),
  )


def _load_source_runs(source_id):
  contract = SOURCE_CONTRACTS[source_id]
  artifact = json.loads((ROOT / contract["path"]).read_text(encoding="utf-8"))
  assert artifact["code_version"] == contract["code_version"]
  assert len(artifact["runs"]) == contract["run_count"]
  return artifact, {
    _source_coordinate(run): run for run in artifact.get("runs", [])
  }


def _compare_source(current_runs, source_id):
  _, source_runs = _load_source_runs(source_id)
  comparisons = []
  for run in current_runs:
    coordinate = _coordinate(run)
    source = source_runs.get(coordinate)
    current_history = _history(run)
    source_history = _history(source) if source else []
    current_hashes = [item.get("state_hash") for item in current_history]
    source_hashes = [item.get("state_hash") for item in source_history]
    comparisons.append({
      "profile": coordinate[0],
      "seed": coordinate[1],
      "difficulty": coordinate[2],
      "source_id": source_id,
      "source_present": source is not None,
      "history_match": source is not None and current_history == source_history,
      "state_hashes_match": source is not None and current_hashes == source_hashes,
      "transition_count": len(current_history),
      "source_transition_count": len(source_history),
      "final_hash": current_hashes[-1] if current_hashes else None,
      "source_final_hash": source_hashes[-1] if source_hashes else None,
    })
  return comparisons


def validate_artifact(artifact):
  assert artifact["artifact_type"] == ARTIFACT_TYPE
  assert artifact["batch_id"] == BATCH_ID
  assert artifact["code_version"] == CODE_VERSION
  assert artifact["campaign"] == CAMPAIGN
  assert artifact["ruleset"] == RULESET
  assert artifact["state_hash_schema"] == STATE_HASH_SCHEMA
  assert artifact["seeds"] == SEEDS
  assert artifact["difficulties"] == DIFFICULTIES
  assert artifact["profiles"] == PROFILES
  assert artifact["runtime_promotion"] == "deferred"
  assert artifact["difficulty_change_authorized"] is False

  runs = artifact["runs"]
  assert len(runs) == 75
  assert sum(run.get("source_id") == "all_tiers" for run in runs) == 60
  assert sum(run.get("source_id") == "expert" for run in runs) == 15

  expected_coordinates = set(expected_matrix())
  for source_id, expected_count in (("all_tiers", 60), ("expert", 15)):
    source_runs = [run for run in runs if run.get("source_id") == source_id]
    coordinates = [_coordinate(run) for run in source_runs]
    expected = expected_coordinates if source_id == "all_tiers" else set(expert_matrix())
    assert len(source_runs) == expected_count
    assert set(coordinates) == expected

  projection = artifact["observation_projection"]
  assert projection["trace_entry_count"] == 75 * EXPECTED_TRANSITIONS
  assert projection["staffing_line_count"] == projection["trace_entry_count"]
  assert projection["physical_capacity_line_count"] == projection["trace_entry_count"]
  assert projection["hidden_marker_count"] == 0

  for run in runs:
    assert run["campaign"] == CAMPAIGN
    assert run["completion_status"] == "complete"
    assert run["transition_count"] == EXPECTED_TRANSITIONS
    assert not run["validation_failures"]
    assert len(run["turn_trace"]) == EXPECTED_TRANSITIONS
    history_hashes = [item.get("state_hash") for item in run["history"]]
    assert run["state_hashes"] == history_hashes
    assert run["final_hash"] == history_hashes[-1]
    for index, trace_entry in enumerate(run["turn_trace"]):
      assert REQUIRED_TRACE_FIELDS <= set(trace_entry)
      assert any(
        line.startswith("Staffing:") for line in trace_entry["observation"]
      )
      assert any(
        line.startswith("Physical capacity:")
        for line in trace_entry["observation"]
      )
      assert trace_entry["latest_transition"]["state_hash"] == history_hashes[index]

  comparisons = artifact["source_comparisons"]
  assert len(comparisons) == 75
  assert all(item["source_present"] for item in comparisons)
  assert all(item["history_match"] for item in comparisons)
  assert all(item["state_hashes_match"] for item in comparisons)


def capture(output_path):
  os.chdir(ROOT)
  version = code_version()
  if version != CODE_VERSION:
    raise RuntimeError(f"expected package version {CODE_VERSION}, found {version}")

  subprocess.run(["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"], check=True)

  control = play_session(
    CAMPAIGN,
    seed=42,
    difficulty="normal",
    policy_fn=lambda obs, legal, turn: "hold",
  )
  if control["history"][0]["state_hash"] != GOLDEN_CONTROL_HASH:
    raise RuntimeError(
      "seed-42 Normal hold-control hash changed: "
      f"{control['history'][0]['state_hash']}"
    )

  runs = []
  for profile, seed, difficulty in expected_matrix():
    print(f"Running all-tiers {profile} / seed {seed} / {difficulty}")
    runs.append(run_profile(profile, seed, difficulty, "all_tiers"))
  for profile, seed, difficulty in expert_matrix():
    print(f"Running expert-overlap {profile} / seed {seed} / {difficulty}")
    runs.append(run_profile(profile, seed, difficulty, "expert"))

  trace_entries = [
    entry
    for run in runs
    for entry in run["turn_trace"]
  ]
  observations = [
    line
    for entry in trace_entries
    for line in entry["observation"]
    if isinstance(line, str)
  ]
  comparisons = []
  comparisons.extend(
    _compare_source(
      [run for run in runs if run["source_id"] == "all_tiers"],
      "all_tiers",
    )
  )
  comparisons.extend(
    _compare_source(
      [run for run in runs if run["source_id"] == "expert"],
      "expert",
    )
  )
  artifact = {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": version,
    "campaign": CAMPAIGN,
    "ruleset": RULESET,
    "state_hash_schema": STATE_HASH_SCHEMA,
    "seeds": SEEDS,
    "difficulties": DIFFICULTIES,
    "profiles": PROFILES,
    "runtime_promotion": "deferred",
    "difficulty_change_authorized": False,
    "source_artifacts": [
      {"source_id": source_id, **contract}
      for source_id, contract in SOURCE_CONTRACTS.items()
    ],
    "observation_projection": {
      "safe_lines": [
        "Staffing: nurses <n>, physicians <n>, admins <n>",
        "Physical capacity: staffed beds <n>, outpatient <n>, emergency <n>, ICU <n>, obstetrics <n>, psychiatric <n>, cardiology <n>, oncology <n>, infusion <n>, neurology <n>, ASC <n>",
      ],
      "trace_entry_count": len(trace_entries),
      "staffing_line_count": sum(line.startswith("Staffing:") for line in observations),
      "physical_capacity_line_count": sum(
        line.startswith("Physical capacity:") for line in observations
      ),
      "hidden_marker_count": sum(
        marker in line.casefold()
        for line in observations
        for marker in HIDDEN_MARKERS
      ),
    },
    "source_comparisons": comparisons,
    "evidence_limits": [
      "This is deterministic simulated-policy evidence, not human or classroom evidence.",
      "Exact history and state-hash equality supports an observation-only change claim; it does not establish causal difficulty, balance, winnability, or comprehension.",
      "The source artifacts were produced at earlier code versions and are used only as immutable transition controls.",
      "Integer staffing and capacity quantities are gameplay abstractions, not calibrated clinical, financial, or workforce estimates.",
    ],
    "runs": runs,
  }
  validate_artifact(artifact)
  output_path.parent.mkdir(parents=True, exist_ok=True)
  output_path.write_text(
    json.dumps(artifact, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  print(f"Wrote {len(runs)} runs to {output_path}")


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output",
    default=str(OUTPUT_DIR / "results.json"),
  )
  args = parser.parse_args()
  capture(Path(args.output))


if __name__ == "__main__":
  main()
