#!/usr/bin/env python3
"""Capture project-limit rejection and recovery evidence for v0.10.54."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import McpClient  # noqa: E402


BATCH_ID = "v0.10.54-project-limit-recovery"
CODE_VERSION = "0.10.54"
CAMPAIGN = "competitive-regional-v1"
DIFFICULTY = "hard"
SEEDS = [42, 43, 44]
EXPECTED_TRANSITIONS = 24
SOURCE_ARTIFACT = (
  "_workspace/experiments/v0.10.51-adversarial-resource-probe/results.json"
)
PROBE_SCHEDULE = {
  4: {
    "probe_id": "accepted_clinic_project",
    "command": "project kind=clinic_network budget=18",
    "expected_code": None,
  },
  6: {
    "probe_id": "accepted_asc_project",
    "command": "project kind=asc_unit budget=6",
    "expected_code": None,
  },
  7: {
    "probe_id": "concurrent_project_limit",
    "command": "project kind=neurology_unit budget=6",
    "expected_code": "too_many_concurrent_projects",
  },
}
REQUIRED_TRACE_FIELDS = {
  "turn",
  "observation",
  "legal_commands",
  "planned_command",
  "submitted_command",
  "validation_failures",
  "retry_commands",
  "turn_after_failure",
  "observation_after_failure",
  "latest_transition",
  "done_after_submit",
}
LIMITATIONS = [
  "The project ceiling is a game abstraction, not an empirical health-system constraint.",
  "A stable error code and safe retry show traceability, not human comprehension or learning.",
  "The three-seed Hard matrix does not establish balance, winnability, strategy quality, calibration, or policy validity.",
  "This evidence gate does not promote a validation-hint or runtime change.",
]


def code_version():
  text = (ROOT / "Cargo.toml").read_text(encoding="utf-8")
  match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
  return match.group(1) if match else "unknown"


def failure_record(turn, command, response):
  failure = {
    "turn": turn,
    "command": command,
    "error": response.get("error", "unknown MCP validation error"),
  }
  for field in ("code", "resource_limit", "hint"):
    if response.get(field) is not None:
      failure[field] = response[field]
  return failure


def failed_run(seed, error):
  return {
    "profile_id": "project_limit_recovery",
    "profile_name": f"Project-Limit Recovery / {DIFFICULTY} / seed {seed}",
    "persona_prompt": (
      "Start two valid capital projects, probe the existing two-project limit, "
      "then recover with hold while preserving actor-visible evidence."
    ),
    "decision_source": "fixed probe schedule using actor-visible MCP surfaces",
    "seed": seed,
    "difficulty": DIFFICULTY,
    "completion_status": "failed",
    "run_error": error,
    "turn_trace": [],
    "probe_results": [],
    "validation_failures": [],
    "expected_probe_failures": [],
    "unexpected_failures": [],
    "retry_count": 0,
    "transition_count": 0,
    "state_hashes": [],
    "final_hash": None,
    "final_observation": [],
    "debrief": [],
  }


def run_session(seed):
  client = McpClient(timeout_seconds=60)
  session = None
  turn_trace = []
  history = []
  validation_failures = []
  expected_probe_failures = []
  unexpected_failures = []
  probe_results = []

  try:
    client.start()
    start_response = client.call_tool(
      "start_session",
      {"campaign": CAMPAIGN, "seed": seed, "difficulty": DIFFICULTY},
    )
    if start_response["isError"]:
      return failed_run(seed, start_response["error"])

    session = start_response["data"]
    session_id = session["session_id"]

    while not session["done"]:
      turn = session["turn"]
      probe = PROBE_SCHEDULE.get(turn)
      command = probe["command"] if probe else "hold"
      trace = {
        "turn": turn,
        "observation": session["observation"],
        "legal_commands": session["legal_commands"],
        "planned_command": command,
        "submitted_command": command,
        "validation_failures": [],
        "retry_commands": [],
        "turn_after_failure": None,
        "observation_after_failure": None,
        "latest_transition": None,
        "done_after_submit": False,
      }

      response = client.call_tool(
        "submit_turn",
        {"session_id": session_id, "command_text": command},
      )

      if response["isError"]:
        failure = failure_record(turn, command, response)
        validation_failures.append(failure)
        trace["validation_failures"].append(failure)

        after_failure = client.call_tool(
          "get_observation",
          {"session_id": session_id},
        )
        if after_failure["isError"]:
          unexpected_failures.append({
            "turn": turn,
            "command": command,
            "error": after_failure["error"],
            "code": "retry_observation_error",
          })
        else:
          trace["turn_after_failure"] = after_failure["data"]["turn"]
          trace["observation_after_failure"] = after_failure["data"]["observation"]
          if trace["turn_after_failure"] != turn:
            unexpected_failures.append({
              "turn": turn,
              "command": command,
              "error": "rejected command advanced the session turn",
              "code": "rejected_command_advanced",
            })
          if trace["observation_after_failure"] != trace["observation"]:
            unexpected_failures.append({
              "turn": turn,
              "command": command,
              "error": "rejected command changed the actor-visible observation",
              "code": "rejected_command_changed_observation",
            })

        expected_code = probe["expected_code"] if probe else None
        if expected_code == failure.get("code"):
          expected_probe_failures.append(failure)
        else:
          unexpected_failures.append({
            **failure,
            "code": "unexpected_validation_failure",
            "observed_code": failure.get("code"),
            "expected_code": expected_code,
          })

        retry_command = "hold"
        trace["retry_commands"].append(retry_command)
        response = client.call_tool(
          "submit_turn",
          {"session_id": session_id, "command_text": retry_command},
        )
        if response["isError"]:
          unexpected_failures.append(
            failure_record(turn, retry_command, response)
            | {"code": "safe_retry_failed"}
          )
          trace["retry_error"] = response.get("error")
          turn_trace.append(trace)
          break
      elif probe and probe["expected_code"] is not None:
        unexpected_failures.append({
          "turn": turn,
          "command": command,
          "error": "project-limit probe was accepted unexpectedly",
          "code": "probe_accepted",
          "expected_code": probe["expected_code"],
        })

      if response["isError"]:
        break

      session = response["data"]
      transition = session.get("latest_transition")
      if transition:
        history.append(transition)
        trace["latest_transition"] = transition
      trace["done_after_submit"] = session["done"]
      turn_trace.append(trace)

      if probe:
        failure = trace["validation_failures"][0] if trace["validation_failures"] else {}
        probe_results.append({
          "turn": turn,
          "probe_id": probe["probe_id"],
          "expected_code": probe["expected_code"],
          "observed_code": failure.get("code"),
          "accepted": not trace["validation_failures"],
          "retry_commands": trace["retry_commands"],
          "turn_after_failure": trace["turn_after_failure"],
          "hint_present": bool(failure.get("hint")),
          "resource_limit_present": bool(failure.get("resource_limit")),
        })
  except Exception as error:
    return failed_run(seed, str(error))
  finally:
    if session is not None:
      end_response = client.call_tool(
        "end_session",
        {"session_id": session["session_id"]},
      )
      debrief = (
        end_response["data"].get("debrief", [])
        if not end_response["isError"]
        else []
      )
    else:
      debrief = []
    client.close()

  return {
    "profile_id": "project_limit_recovery",
    "profile_name": f"Project-Limit Recovery / {DIFFICULTY} / seed {seed}",
    "persona_prompt": (
      "Start two valid capital projects, probe the existing two-project limit, "
      "then recover with hold while preserving actor-visible evidence."
    ),
    "decision_source": "fixed probe schedule using actor-visible MCP surfaces",
    "seed": seed,
    "difficulty": DIFFICULTY,
    "completion_status": (
      "complete" if len(history) == EXPECTED_TRANSITIONS else "incomplete"
    ),
    "turn_trace": turn_trace,
    "probe_results": probe_results,
    "validation_failures": validation_failures,
    "expected_probe_failures": expected_probe_failures,
    "unexpected_failures": unexpected_failures,
    "retry_count": sum(len(entry["retry_commands"]) for entry in turn_trace),
    "transition_count": len(history),
    "state_hashes": [transition["state_hash"] for transition in history],
    "final_hash": history[-1]["state_hash"] if history else None,
    "final_observation": session.get("observation", []) if session else [],
    "debrief": debrief,
  }


def recovery_surface_summary(runs):
  failures = [
    failure
    for run in runs
    for failure in run["expected_probe_failures"]
  ]
  return {
    "run_count": len(runs),
    "expected_failure_count": len(failures),
    "stable_code_count": sum(
      failure.get("code") == "too_many_concurrent_projects"
      for failure in failures
    ),
    "structured_hint_count": sum("hint" in failure for failure in failures),
    "resource_limit_count": sum("resource_limit" in failure for failure in failures),
    "same_turn_recovery_count": sum(
      result["turn_after_failure"] == result["turn"]
      for run in runs
      for result in run["probe_results"]
      if result["expected_code"]
    ),
    "safe_retry_count": sum(run["retry_count"] == 1 for run in runs),
    "debrief_limit_explanation_count": sum(
      any("maximum of 2 concurrent projects" in line for line in run["debrief"])
      for run in runs
    ),
  }


def build_artifact(runs):
  return {
    "filename": "results.json",
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "difficulty": DIFFICULTY,
    "seeds": SEEDS,
    "profile": "Project-Limit Recovery",
    "evidence_type": (
      "deterministic actor-visible concurrent-project rejection and recovery capture"
    ),
    "source_artifact": SOURCE_ARTIFACT,
    "expected_probe_schedule": PROBE_SCHEDULE,
    "recovery_surface": recovery_surface_summary(runs),
    "promotion_basis": (
      "Record the current project-limit response and recovery surface. A runtime "
      "or interface change requires separate evidence of unexplained decision friction."
    ),
    "limitations": LIMITATIONS,
    "runs": runs,
  }


def validate_artifact(artifact):
  assert artifact["batch_id"] == BATCH_ID
  assert artifact["code_version"] == CODE_VERSION
  assert artifact["campaign"] == CAMPAIGN
  assert artifact["difficulty"] == DIFFICULTY
  assert artifact["seeds"] == SEEDS
  assert [run["seed"] for run in artifact["runs"]] == SEEDS
  assert len(artifact["runs"]) == len(SEEDS)

  for run in artifact["runs"]:
    assert run["completion_status"] == "complete"
    assert run["transition_count"] == EXPECTED_TRANSITIONS
    assert len(run["turn_trace"]) == EXPECTED_TRANSITIONS
    assert len(run["probe_results"]) == len(PROBE_SCHEDULE)
    assert len(run["expected_probe_failures"]) == 1
    assert run["unexpected_failures"] == []
    assert run["retry_count"] == 1
    assert run["debrief"]

    for entry in run["turn_trace"]:
      assert REQUIRED_TRACE_FIELDS <= set(entry)
      assert entry["latest_transition"]
      if entry["validation_failures"]:
        assert entry["turn_after_failure"] == entry["turn"]
        assert entry["observation_after_failure"] == entry["observation"]
        assert entry["retry_commands"] == ["hold"]

    for result in run["probe_results"]:
      expected = PROBE_SCHEDULE[result["turn"]]
      assert result["probe_id"] == expected["probe_id"]
      assert result["expected_code"] == expected["expected_code"]
      if expected["expected_code"] is None:
        assert result["accepted"]
      else:
        assert result["accepted"] is False
        assert result["observed_code"] == expected["expected_code"]
        assert result["turn_after_failure"] == result["turn"]
        assert result["retry_commands"] == ["hold"]

  surface = artifact["recovery_surface"]
  assert surface["run_count"] == len(SEEDS)
  assert surface["expected_failure_count"] == len(SEEDS)
  assert surface["stable_code_count"] == len(SEEDS)
  assert surface["structured_hint_count"] == 0
  assert surface["resource_limit_count"] == 0
  assert surface["same_turn_recovery_count"] == len(SEEDS)
  assert surface["safe_retry_count"] == len(SEEDS)
  assert surface["debrief_limit_explanation_count"] == len(SEEDS)


def render_diagnostics(artifact):
  surface = artifact["recovery_surface"]
  lines = [
    "# Project-Limit Recovery Diagnostics v0.10.54",
    "",
    f"- **Batch id:** {artifact['batch_id']}",
    f"- **Code version:** {artifact['code_version']}",
    f"- **Campaign:** `{artifact['campaign']}`",
    f"- **Difficulty:** `{artifact['difficulty']}`",
    f"- **Source:** `{artifact['source_artifact']}`",
    "- **Evidence type:** deterministic actor-visible project-limit recovery capture",
    "",
    "## Run Summary",
    "",
    "| Profile | Seed | Status | Transitions | Expected failures | Retries | Final hash |",
    "| --- | ---: | --- | ---: | ---: | ---: | --- |",
  ]
  for run in artifact["runs"]:
    lines.append(
      f"| {run['profile_name']} | {run['seed']} | {run['completion_status']} | "
      f"{run['transition_count']} | {len(run['expected_probe_failures'])} | "
      f"{run['retry_count']} | {run['final_hash'] or '—'} |"
    )

  lines.extend([
    "",
    "## Probe Results",
    "",
    "| Seed | Month | Probe | Expected code | Observed code | Accepted | Retry turn | Structured hint | Resource limit |",
    "| ---: | ---: | --- | --- | --- | --- | ---: | --- | --- |",
  ])
  for run in artifact["runs"]:
    for result in run["probe_results"]:
      lines.append(
        f"| {run['seed']} | {result['turn']} | {result['probe_id']} | "
        f"{result['expected_code'] or 'accepted'} | "
        f"{result['observed_code'] or 'accepted'} | "
        f"{'yes' if result['accepted'] else 'no'} | "
        f"{result['turn_after_failure'] or '—'} | "
        f"{'yes' if result['hint_present'] else 'no'} | "
        f"{'yes' if result['resource_limit_present'] else 'no'} |"
      )

  lines.extend([
    "",
    "## Recovery Surface",
    "",
    f"- Stable `too_many_concurrent_projects` codes: {surface['stable_code_count']}/{surface['expected_failure_count']}.",
    f"- Structured hint fields: {surface['structured_hint_count']}/{surface['expected_failure_count']}.",
    f"- Resource-limit fields: {surface['resource_limit_count']}/{surface['expected_failure_count']}.",
    f"- Same-turn recoveries: {surface['same_turn_recovery_count']}/{surface['expected_failure_count']}.",
    f"- Safe `hold` retries: {surface['safe_retry_count']}/{surface['run_count']}.",
    f"- Debriefs explaining the two-project ceiling: {surface['debrief_limit_explanation_count']}/{surface['run_count']}.",
    "",
    "## Interpretation",
    "",
    "- The current response exposes a stable code and plain-language limit, while structured hint and resource-limit fields are absent.",
    "- Rejected commands preserve the actor-visible turn and observation; one safe `hold` retry advances each run exactly once.",
    "- The debrief retains the two-project ceiling for retrospective review.",
    "- These facts support recovery traceability. They do not establish human comprehension or justify a validation-hint change by themselves.",
    "",
    "## Evidence Limits",
    "",
  ])
  lines.extend(f"- {limitation}" for limitation in artifact["limitations"])
  lines.append("")
  return "\n".join(lines)


def main():
  os.chdir(ROOT)
  if code_version() != CODE_VERSION:
    raise RuntimeError(f"expected Cargo.toml version {CODE_VERSION}")
  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"],
    cwd=ROOT,
    check=True,
  )
  runs = []
  for seed in SEEDS:
    print(
      f"Running project-limit recovery / {DIFFICULTY} / seed {seed}...",
      flush=True,
    )
    runs.append(run_session(seed))

  artifact = build_artifact(runs)
  validate_artifact(artifact)
  output_dir = Path(__file__).parent
  (output_dir / "results.json").write_text(
    json.dumps(artifact, indent=2) + "\n",
    encoding="utf-8",
  )
  (output_dir / "diagnostics.md").write_text(
    render_diagnostics(artifact),
    encoding="utf-8",
  )
  print(f"Wrote {output_dir / 'results.json'}")
  print(f"Wrote {output_dir / 'diagnostics.md'}")


if __name__ == "__main__":
  main()
