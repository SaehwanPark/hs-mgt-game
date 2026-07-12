#!/usr/bin/env python3
"""Capture current-code observation-driven teachability traces."""

import argparse
import importlib.util
import json
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
  / "v0.10.50-teachability-observation-capture"
  / "run_sessions.py"
)
SOURCE_SPEC = importlib.util.spec_from_file_location(
  "historical_teachability_policy",
  SOURCE_RUNNER_PATH,
)
SOURCE_RUNNER = importlib.util.module_from_spec(SOURCE_SPEC)
SOURCE_SPEC.loader.exec_module(SOURCE_RUNNER)


BATCH_ID = "v0.11.12-phase7-current-code-teachability-capture"
ARTIFACT_TYPE = "current_code_teachability_capture"
CAMPAIGN = "competitive-regional-v1"
DIFFICULTY = "hard"
RULESET = "competitive-ruleset-0.2.0"
STATE_HASH_SCHEMA = "competitive-state-hash-v9"
EXPECTED_CODE_VERSION = "0.11.12"
SEEDS = [42, 43, 44]
PROFILES = [profile["id"] for profile in SOURCE_RUNNER.PROFILES]
EXPECTED_TRANSITIONS = 24
GOLDEN_CONTROL_HASH = "61357596d8800592"


def code_version():
  cargo = (ROOT / "Cargo.toml").read_text(encoding="utf-8")
  match = re.search(r'^version\s*=\s*"([^"]+)"', cargo, re.MULTILINE)
  return match.group(1) if match else "unknown"


def expected_matrix():
  return [
    (profile_id, seed)
    for profile_id in PROFILES
    for seed in SEEDS
  ]


def failed_run(profile_id, seed, error):
  return {
    "profile_id": profile_id,
    "profile_name": f"{profile_id} / {DIFFICULTY} / seed {seed}",
    "persona_prompt": "Use only actor-visible observations and legal hints.",
    "decision_source": "deterministic observation-driven policy",
    "seed": seed,
    "difficulty": DIFFICULTY,
    "campaign": CAMPAIGN,
    "completion_status": "failed",
    "run_error": str(error),
    "transition_count": 0,
    "history": [],
    "state_hashes": [],
    "final_hash": None,
    "turn_trace": [],
    "commands": [],
    "validation_failures": [],
    "retry_count": 0,
    "final_observation": [],
    "debrief": [],
  }


def run_profile(profile, seed):
  profile_id = profile["id"]
  try:
    run = SOURCE_RUNNER.run_session(profile, seed)
  except Exception as error:  # Preserve failed coordinates for the audit.
    return failed_run(profile_id, seed, error)

  run["campaign"] = CAMPAIGN
  run["difficulty"] = DIFFICULTY
  run["profile_id"] = profile_id
  run["history"] = [
    entry["latest_transition"]
    for entry in run.get("turn_trace", [])
    if isinstance(entry, dict)
    and isinstance(entry.get("latest_transition"), dict)
  ]
  return run


def capture(output_path):
  if code_version() != EXPECTED_CODE_VERSION:
    raise RuntimeError(
      f"expected package version {EXPECTED_CODE_VERSION}, found {code_version()}"
    )

  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"],
    cwd=ROOT,
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

  profiles_by_id = {profile["id"]: profile for profile in SOURCE_RUNNER.PROFILES}
  runs = []
  for profile_id, seed in expected_matrix():
    print(f"Running {profile_id} / {DIFFICULTY} / seed {seed}", flush=True)
    runs.append(run_profile(profiles_by_id[profile_id], seed))

  artifact = {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": EXPECTED_CODE_VERSION,
    "campaign": CAMPAIGN,
    "ruleset": RULESET,
    "state_hash_schema": STATE_HASH_SCHEMA,
    "difficulty": DIFFICULTY,
    "seeds": SEEDS,
    "profiles": PROFILES,
    "policy_source": str(SOURCE_RUNNER_PATH.relative_to(ROOT)),
    "runtime_promotion": "deferred",
    "control": {
      "campaign": CAMPAIGN,
      "seed": 42,
      "difficulty": "normal",
      "policy": "hold",
      "first_transition_hash": GOLDEN_CONTROL_HASH,
    },
    "runs": runs,
  }

  from run_audit import validate_artifact

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
