#!/usr/bin/env python3
"""Capture Expert difficulty validation after difficulty resource scaling."""

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

import importlib.util  # noqa: E402

SOURCE_SPEC = importlib.util.spec_from_file_location(
  "operating_loop_ai_validation_runner",
  SOURCE_RUNNER_PATH,
)
SOURCE_RUNNER = importlib.util.module_from_spec(SOURCE_SPEC)
SOURCE_SPEC.loader.exec_module(SOURCE_RUNNER)


BATCH_ID = "v0.11.9-expert-difficulty-validation"
CAMPAIGN = "competitive-regional-v1"
DIFFICULTY = "expert"
SEEDS = [42, 43, 44]
EXPECTED_TRANSITIONS = 24
EXPECTED_CODE_VERSION = "0.11.9"
GOLDEN_CONTROL_HASH = "61357596d8800592"
PROFILES = list(SOURCE_RUNNER.PROFILES)
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
  return [(profile, seed) for profile in PROFILES for seed in SEEDS]


def final_hash(result):
  return result["history"][-1]["state_hash"] if result["history"] else None


def failed_run(profile, seed, error):
  return {
    "profile_id": profile.lower().replace("/", "_").replace(" ", "_"),
    "profile_name": profile,
    "persona_prompt": (
      "Deterministic existing scripted policy used as a simulated-agent profile "
      "for bounded Expert difficulty validation after risk-posture and resource "
      "scaling changes."
    ),
    "decision_source": "actor-visible MCP observation and legal resource hints",
    "seed": seed,
    "difficulty": DIFFICULTY,
    "completion_status": "failed",
    "run_error": error,
    "turn_trace": [],
    "validation_failures": [],
    "transition_count": 0,
    "state_hashes": [],
    "final_hash": None,
    "final_observation": [],
    "debrief": [],
  }


def run_profile(profile, seed):
  try:
    result = play_session(
      CAMPAIGN,
      seed=seed,
      difficulty=DIFFICULTY,
      policy_fn=SOURCE_RUNNER.policy_for(profile),
      capture_trace=True,
    )
  except Exception as error:
    return failed_run(profile, seed, str(error))

  if result is None:
    return failed_run(profile, seed, "play_session returned no result")

  status = "complete" if len(result["history"]) == EXPECTED_TRANSITIONS else "incomplete"
  run = {
    "profile_id": profile.lower().replace("/", "_").replace(" ", "_"),
    "profile_name": profile,
    "persona_prompt": (
      "Deterministic existing scripted policy used as a simulated-agent profile "
      "for bounded Expert difficulty validation after risk-posture and resource "
      "scaling changes."
    ),
    "decision_source": "actor-visible MCP observation and legal command hints",
    "seed": seed,
    "difficulty": DIFFICULTY,
    "completion_status": status,
    "turn_trace": result.get("turn_trace", []),
    "validation_failures": result["validation_failures"],
    "transition_count": len(result["history"]),
    "history": result["history"],
    "state_hashes": [transition["state_hash"] for transition in result["history"]],
    "final_hash": final_hash(result),
    "final_observation": result["final_observation"],
    "debrief": result["debrief"],
  }
  if status != "complete":
    run["run_error"] = (
      f"expected {EXPECTED_TRANSITIONS} transitions, got {run['transition_count']}"
    )
  return run


def validate_artifact(artifact):
  assert artifact["batch_id"] == BATCH_ID
  assert artifact["campaign"] == CAMPAIGN
  assert artifact["difficulty"] == DIFFICULTY
  assert artifact["seeds"] == SEEDS
  assert artifact["profiles"] == PROFILES

  runs = artifact["runs"]
  assert len(runs) == len(expected_matrix())
  observed_matrix = [(run["profile_name"], run["seed"]) for run in runs]
  assert len(set(observed_matrix)) == len(observed_matrix)
  assert set(observed_matrix) == set(expected_matrix())

  for run in runs:
    assert run["difficulty"] == DIFFICULTY
    assert run["completion_status"] in {"complete", "incomplete", "failed"}
    assert isinstance(run.get("turn_trace"), list)
    assert run["transition_count"] == len(run["state_hashes"])
    assert run["final_observation"] is not None
    assert run["debrief"] is not None

    for trace_entry in run["turn_trace"]:
      assert REQUIRED_TRACE_FIELDS <= set(trace_entry)

    if run["completion_status"] == "complete":
      assert run["transition_count"] == EXPECTED_TRANSITIONS
      assert not run["validation_failures"]
      assert len(run["turn_trace"]) == EXPECTED_TRANSITIONS
    else:
      assert run.get("run_error")


def render_diagnostics(artifact):
  lines = [
    "# Expert Difficulty Validation Diagnostics",
    "",
    f"- **Batch id:** {artifact['batch_id']}",
    f"- **Code version:** {artifact['code_version']}",
    f"- **Campaign:** `{artifact['campaign']}`",
    f"- **Difficulty:** `{artifact['difficulty']}`",
    "- **Evidence type:** deterministic simulated-agent completion matrix",
    "",
    "## Run Summary",
    "",
    "| Profile | Seed | Status | Transitions | Validation failures | Final hash |",
    "| --- | ---: | --- | ---: | ---: | --- |",
  ]
  for run in artifact["runs"]:
    lines.append(
      f"| {run['profile_name']} | {run['seed']} | {run['completion_status']} | "
      f"{run['transition_count']} | {len(run['validation_failures'])} | "
      f"{run['final_hash'] or '-'} |"
    )

  complete_count = sum(
    run["completion_status"] == "complete" for run in artifact["runs"]
  )
  lines.extend([
    "",
    "## Interpretation",
    "",
    f"- Completed runs: {complete_count}/{len(artifact['runs'])}.",
    "- Completion is a bounded clearability proxy for these policies, seeds, and difficulty.",
    "- This artifact does not establish general Expert winnability, balance, causal value, human learning, or policy validity.",
    "",
  ])
  return "\n".join(lines)


def main():
  os.chdir(ROOT)
  version = code_version()
  if version != EXPECTED_CODE_VERSION:
    raise RuntimeError(f"expected package version {EXPECTED_CODE_VERSION}, found {version}")

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

  runs = [run_profile(profile, seed) for profile, seed in expected_matrix()]
  artifact = {
    "filename": "results.json",
    "batch_id": BATCH_ID,
    "code_version": version,
    "campaign": CAMPAIGN,
    "seeds": SEEDS,
    "difficulty": DIFFICULTY,
    "profiles": PROFILES,
    "evidence_type": "deterministic Expert difficulty validation matrix",
    "runtime_promotion": "deferred",
    "runs": runs,
  }
  validate_artifact(artifact)

  output_dir = Path(__file__).parent
  (output_dir / "results.json").write_text(
    json.dumps(artifact, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (output_dir / "diagnostics.md").write_text(
    render_diagnostics(artifact),
    encoding="utf-8",
  )
  print(f"wrote {output_dir / 'results.json'}")
  print(f"wrote {output_dir / 'diagnostics.md'}")


if __name__ == "__main__":
  main()
