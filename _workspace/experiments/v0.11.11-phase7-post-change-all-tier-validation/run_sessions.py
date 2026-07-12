#!/usr/bin/env python3
"""Capture the current post-difficulty all-tier validation matrix."""

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
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
  "operating_loop_ai_validation_runner",
  SOURCE_RUNNER_PATH,
)
SOURCE_RUNNER = importlib.util.module_from_spec(SOURCE_SPEC)
SOURCE_SPEC.loader.exec_module(SOURCE_RUNNER)


BATCH_ID = "v0.11.11-phase7-post-change-all-tier-validation"
ARTIFACT_TYPE = "post_change_all_tier_difficulty_validation"
CAMPAIGN = "competitive-regional-v1"
RULESET = "competitive-ruleset-0.2.0"
STATE_HASH_SCHEMA = "competitive-state-hash-v9"
EXPECTED_CODE_VERSION = "0.11.11"
SEEDS = [42, 43, 44]
DIFFICULTIES = ["easy", "normal", "hard", "expert"]
PROFILES = list(SOURCE_RUNNER.PROFILES)
EXPECTED_TRANSITIONS = 24
GOLDEN_CONTROL_HASH = "61357596d8800592"
REQUIRED_TRACE_FIELDS = {
  "turn",
  "observation",
  "legal_commands",
  "submitted_command",
  "validation_failures",
  "latest_transition",
  "done_after_submit",
}


def code_version():
  cargo = (ROOT / "Cargo.toml").read_text(encoding="utf-8")
  match = re.search(r'^version\s*=\s*"([^"]+)"', cargo, re.MULTILINE)
  return match.group(1) if match else "unknown"


def expected_matrix():
  return [
    (profile, seed, difficulty)
    for profile in PROFILES
    for seed in SEEDS
    for difficulty in DIFFICULTIES
  ]


def final_hash(result):
  return result["history"][-1]["state_hash"] if result["history"] else None


def failed_run(profile, seed, difficulty, error):
  return {
    "profile": profile,
    "seed": seed,
    "difficulty": difficulty,
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


def run_profile(profile, seed, difficulty):
  try:
    result = play_session(
      CAMPAIGN,
      seed=seed,
      difficulty=difficulty,
      policy_fn=SOURCE_RUNNER.policy_for(profile),
      capture_trace=True,
    )
  except Exception as error:
    return failed_run(profile, seed, difficulty, str(error))

  if result is None:
    return failed_run(profile, seed, difficulty, "play_session returned no result")

  history = result["history"]
  status = "complete" if len(history) == EXPECTED_TRANSITIONS else "incomplete"
  run = {
    "profile": profile,
    "seed": seed,
    "difficulty": difficulty,
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


def validate_artifact(artifact):
  assert artifact["artifact_type"] == ARTIFACT_TYPE
  assert artifact["batch_id"] == BATCH_ID
  assert artifact["code_version"] == EXPECTED_CODE_VERSION
  assert artifact["campaign"] == CAMPAIGN
  assert artifact["ruleset"] == RULESET
  assert artifact["state_hash_schema"] == STATE_HASH_SCHEMA
  assert artifact["seeds"] == SEEDS
  assert artifact["difficulties"] == DIFFICULTIES
  assert artifact["profiles"] == PROFILES
  assert artifact["runtime_promotion"] == "deferred"

  runs = artifact["runs"]
  coordinates = [
    (run.get("profile"), run.get("seed"), run.get("difficulty"))
    for run in runs
  ]
  assert len(runs) == len(expected_matrix())
  assert len(set(coordinates)) == len(coordinates)
  assert set(coordinates) == set(expected_matrix())

  for run in runs:
    assert run["campaign"] == CAMPAIGN
    assert run["completion_status"] in {"complete", "incomplete", "failed"}
    assert run["transition_count"] == len(run["state_hashes"])
    assert isinstance(run.get("history"), list)
    assert isinstance(run.get("turn_trace"), list)
    assert run.get("final_observation") is not None
    assert run.get("debrief") is not None

    history_hashes = [
      transition.get("state_hash") for transition in run["history"]
    ]
    assert run["state_hashes"] == history_hashes
    assert run["final_hash"] == (history_hashes[-1] if history_hashes else None)

    for index, trace_entry in enumerate(run["turn_trace"]):
      assert REQUIRED_TRACE_FIELDS <= set(trace_entry)
      latest_transition = trace_entry["latest_transition"]
      if latest_transition is not None:
        assert index < len(history_hashes)
        assert latest_transition.get("state_hash") == history_hashes[index]

    if run["completion_status"] == "complete":
      assert run["transition_count"] == EXPECTED_TRANSITIONS
      assert not run["validation_failures"]
      assert len(run["turn_trace"]) == EXPECTED_TRANSITIONS
    else:
      assert run.get("run_error")


def capture(output_path):
  os.chdir(ROOT)
  version = code_version()
  if version != EXPECTED_CODE_VERSION:
    raise RuntimeError(
      f"expected package version {EXPECTED_CODE_VERSION}, found {version}"
    )

  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"],
    check=True,
  )

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
    print(f"Running {profile} / seed {seed} / {difficulty}")
    runs.append(run_profile(profile, seed, difficulty))

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
    default=str(Path(__file__).with_name("results.json")),
  )
  args = parser.parse_args()
  capture(Path(args.output))


if __name__ == "__main__":
  main()
