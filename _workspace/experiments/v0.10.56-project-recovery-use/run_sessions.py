#!/usr/bin/env python3
"""Capture response-conditioned project-limit recovery evidence for v0.10.56."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import McpClient  # noqa: E402


BATCH_ID = "v0.10.56-project-recovery-use"
CODE_VERSION = "0.10.56"
CAMPAIGN = "competitive-regional-v1"
DIFFICULTY = "hard"
SEEDS = [42, 43, 44]
EXPECTED_TRANSITIONS = 24
SOURCE_ARTIFACT = (
  "_workspace/experiments/v0.10.55-asc-project-observation/results.json"
)
SOURCE_BATCH_ID = "v0.10.55-asc-project-observation"
SOURCE_CODE_VERSION = "0.10.55"
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
  "recovery_decision",
  "latest_transition",
  "done_after_submit",
}
LIMITATIONS = [
  "The project ceiling is a game abstraction, not an empirical health-system constraint.",
  "Response-conditioned simulated-policy behavior is traceability evidence, not human comprehension or learning evidence.",
  "The three-seed Hard matrix does not establish balance, winnability, strategy quality, calibration, or policy validity.",
  "Project validation hints and broader project guidance remain deferred unless a separate artifact identifies unexplained recovery failure.",
]


def code_version():
  text = (ROOT / "Cargo.toml").read_text(encoding="utf-8")
  match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
  return match.group(1) if match else "unknown"


def source_summary():
  source = json.loads((ROOT / SOURCE_ARTIFACT).read_text(encoding="utf-8"))
  assert source["batch_id"] == SOURCE_BATCH_ID
  assert source["code_version"] == SOURCE_CODE_VERSION
  assert source["campaign"] == CAMPAIGN
  assert source["difficulty"] == DIFFICULTY
  assert source["seeds"] == SEEDS
  return {
    "path": SOURCE_ARTIFACT,
    "batch_id": source["batch_id"],
    "code_version": source["code_version"],
    "campaign": source["campaign"],
    "difficulty": source["difficulty"],
    "seeds": source["seeds"],
  }


def source_hashes_by_seed():
  source = json.loads((ROOT / SOURCE_ARTIFACT).read_text(encoding="utf-8"))
  return {run["seed"]: run["state_hashes"] for run in source["runs"]}


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


def response_conditioned_recovery(error, observation):
  """Select a safe retry from only the plain error and visible observation."""
  error_text = error.lower()
  observation_text = "\n".join(observation)
  if (
    "concurrent projects" in error_text
    and "limit" in error_text
    and "ClinicNetwork" in observation_text
    and "AscUnit" in observation_text
  ):
    return {
      "basis": "plain_error_and_unchanged_observation",
      "command": "hold",
      "recognized_limit": True,
      "used_structured_fields": False,
    }
  raise RuntimeError("plain project-limit recovery surface was not actionable")


def failed_run(seed, error):
  return {
    "profile_id": "project_recovery_use",
    "profile_name": f"Project-Recovery Use / {DIFFICULTY} / seed {seed}",
    "persona_prompt": (
      "Use only actor-visible observations and the plain validation error to "
      "recover from the concurrent-project rejection."
    ),
    "decision_source": (
      "response-conditioned policy using actor-visible observation and error text"
    ),
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
        "recovery_decision": None,
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
              "error": "rejected command changed actor-visible observation",
              "code": "rejected_command_changed_observation",
            })
          else:
            try:
              trace["recovery_decision"] = response_conditioned_recovery(
                failure["error"], trace["observation_after_failure"]
              )
            except RuntimeError as error:
              unexpected_failures.append({
                "turn": turn,
                "command": command,
                "error": str(error),
                "code": "recovery_surface_not_actionable",
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

        retry_command = (
          trace["recovery_decision"]["command"]
          if trace["recovery_decision"]
          else "hold"
        )
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
          "accepted": not bool(failure),
          "retry_commands": trace["retry_commands"],
          "turn_after_failure": trace["turn_after_failure"],
          "response_conditioned": bool(trace["recovery_decision"]),
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
    "profile_id": "project_recovery_use",
    "profile_name": f"Project-Recovery Use / {DIFFICULTY} / seed {seed}",
    "persona_prompt": (
      "Use only actor-visible observations and the plain validation error to "
      "recover from the concurrent-project rejection."
    ),
    "decision_source": (
      "response-conditioned policy using actor-visible observation and error text"
    ),
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
  decisions = [
    entry["recovery_decision"]
    for run in runs
    for entry in run["turn_trace"]
    if entry["recovery_decision"]
  ]
  return {
    "run_count": len(runs),
    "expected_failure_count": len(failures),
    "stable_code_count": sum(
      failure.get("code") == "too_many_concurrent_projects"
      for failure in failures
    ),
    "response_conditioned_recovery_count": sum(
      decision["basis"] == "plain_error_and_unchanged_observation"
      for decision in decisions
    ),
    "structured_field_use_count": sum(
      decision["used_structured_fields"] for decision in decisions
    ),
    "same_turn_recovery_count": sum(
      result["turn_after_failure"] == result["turn"]
      for run in runs
      for result in run["turn_trace"]
      if result["validation_failures"]
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
    "profile": "Project-Recovery Use",
    "evidence_type": (
      "deterministic response-conditioned project-limit recovery capture"
    ),
    "source": source_summary(),
    "expected_probe_schedule": PROBE_SCHEDULE,
    "policy_surface": {
      "allowed": ["actor-visible observation", "legal command hints", "plain error text"],
      "excluded": ["hidden state", "history", "code", "hint", "resource_limit"],
    },
    "recovery_surface": recovery_surface_summary(runs),
    "promotion_basis": (
      "Test whether the existing plain project-limit response supports a "
      "response-conditioned simulated recovery. A runtime or interface change "
      "requires separate evidence of unexplained recovery failure."
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
  assert artifact["source"] == source_summary()
  assert artifact["policy_surface"]["excluded"] == [
    "hidden state",
    "history",
    "code",
    "hint",
    "resource_limit",
  ]
  assert [run["seed"] for run in artifact["runs"]] == SEEDS
  assert len(artifact["runs"]) == len(SEEDS)

  source_hashes = source_hashes_by_seed()
  for run in artifact["runs"]:
    assert run["completion_status"] == "complete"
    assert run["transition_count"] == EXPECTED_TRANSITIONS
    assert len(run["turn_trace"]) == EXPECTED_TRANSITIONS
    assert len(run["probe_results"]) == len(PROBE_SCHEDULE)
    assert len(run["expected_probe_failures"]) == 1
    assert run["unexpected_failures"] == []
    assert run["retry_count"] == 1
    assert run["debrief"]
    assert run["state_hashes"] == source_hashes[run["seed"]]

    for result in run["probe_results"]:
      assert result["turn"] in PROBE_SCHEDULE
      expected = PROBE_SCHEDULE[result["turn"]]
      assert result["probe_id"] == expected["probe_id"]
      assert result["expected_code"] == expected["expected_code"]
      if expected["expected_code"] is None:
        assert result["accepted"]
        assert result["observed_code"] is None
      else:
        assert not result["accepted"]
        assert result["observed_code"] == expected["expected_code"]
        assert result["turn_after_failure"] == result["turn"]
        assert result["retry_commands"] == ["hold"]
        assert result["response_conditioned"]

    for entry in run["turn_trace"]:
      assert REQUIRED_TRACE_FIELDS <= set(entry)
      assert entry["latest_transition"]
      if entry["validation_failures"]:
        assert entry["turn_after_failure"] == entry["turn"]
        assert entry["observation_after_failure"] == entry["observation"]
        assert entry["retry_commands"] == ["hold"]
        assert entry["recovery_decision"] == {
          "basis": "plain_error_and_unchanged_observation",
          "command": "hold",
          "recognized_limit": True,
          "used_structured_fields": False,
        }
        failure = entry["validation_failures"][0]
        assert failure["code"] == "too_many_concurrent_projects"
        assert "hint" not in failure
        assert "resource_limit" not in failure
      else:
        assert entry["recovery_decision"] is None

  surface = artifact["recovery_surface"]
  assert surface["run_count"] == len(SEEDS)
  assert surface["expected_failure_count"] == len(SEEDS)
  assert surface["stable_code_count"] == len(SEEDS)
  assert surface["response_conditioned_recovery_count"] == len(SEEDS)
  assert surface["structured_field_use_count"] == 0
  assert surface["same_turn_recovery_count"] == len(SEEDS)
  assert surface["safe_retry_count"] == len(SEEDS)
  assert surface["debrief_limit_explanation_count"] == len(SEEDS)


def render_diagnostics(artifact):
  surface = artifact["recovery_surface"]
  lines = [
    "# Project-Recovery Use Diagnostics v0.10.56",
    "",
    f"- **Batch id:** {artifact['batch_id']}",
    f"- **Code version:** {artifact['code_version']}",
    f"- **Campaign:** `{artifact['campaign']}`",
    f"- **Difficulty:** `{artifact['difficulty']}`",
    f"- **Source:** `{artifact['source']['path']}` / {artifact['source']['batch_id']}",
    "- **Evidence type:** deterministic response-conditioned project-limit recovery capture",
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
    "## Recovery Surface",
    "",
    f"- Stable `too_many_concurrent_projects` codes: {surface['stable_code_count']}/{surface['expected_failure_count']}.",
    f"- Response-conditioned recoveries: {surface['response_conditioned_recovery_count']}/{surface['expected_failure_count']}.",
    f"- Structured validation fields consumed: {surface['structured_field_use_count']}/{surface['expected_failure_count']}.",
    f"- Same-turn recovery observations: {surface['same_turn_recovery_count']}/{surface['expected_failure_count']}.",
    f"- Safe `hold` retries: {surface['safe_retry_count']}/{surface['run_count']}.",
    f"- Debriefs explaining the two-project ceiling: {surface['debrief_limit_explanation_count']}/{surface['run_count']}.",
    "",
    "## Interpretation",
    "",
    "- The simulated policy selected `hold` from the plain project-limit error and unchanged actor-visible observation.",
    "- No structured validation hint or resource-limit payload was consumed.",
    "- These records support response-surface traceability only; they do not establish human comprehension, learning, or advice quality.",
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
      f"Running project-recovery use / {DIFFICULTY} / seed {seed}...",
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
