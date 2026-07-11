#!/usr/bin/env python3
"""Capture adversarial resource-limit probes for v0.10.51."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import McpClient  # noqa: E402


BATCH_ID = "v0.10.51-adversarial-resource-probe"
CODE_VERSION = "0.10.51"
CAMPAIGN = "competitive-regional-v1"
DIFFICULTY = "hard"
SEEDS = [42, 43, 44]
EXPECTED_TRANSITIONS = 24
CONTROL_ARTIFACT = (
  "_workspace/experiments/v0.10.50-teachability-observation-capture/results.json"
)
CONTROL_PROFILE_PREFIX = "First-Time Executive / hard / seed "

PROBE_SCHEDULE = {
  1: {
    "probe_id": "initial_cash_overrun",
    "command": "invest domain=beds amount=40; recruit role=nurse headcount=5",
    "expected_code": "insufficient_cash",
  },
  2: {
    "probe_id": "action_budget_overrun",
    "command": (
      "invest domain=technology amount=10; recruit role=nurse headcount=1; "
      "negotiate payer=carrier_a rate_posture=aggressive; "
      "commit pledge_type=quality level=2"
    ),
    "expected_code": "ap_budget_exceeded",
  },
  3: {
    "probe_id": "accepted_beds_investment",
    "command": "invest domain=beds amount=15; hold",
    "expected_code": None,
  },
  4: {
    "probe_id": "accepted_clinic_project",
    "command": "project kind=clinic_network budget=18",
    "expected_code": None,
  },
  5: {
    "probe_id": "active_draw_cash_overrun",
    "command": "invest domain=beds amount=40; recruit role=nurse headcount=5",
    "expected_code": "insufficient_cash",
  },
  6: {
    "probe_id": "accepted_asc_project",
    "command": "project kind=asc_unit budget=6",
    "expected_code": None,
  },
  7: {
    "probe_id": "concurrent_project_overrun",
    "command": "project kind=neurology_unit budget=6",
    "expected_code": "too_many_concurrent_projects",
  },
  12: {
    "probe_id": "late_cash_overrun",
    "command": "invest domain=beds amount=40; recruit role=nurse headcount=5",
    "expected_code": "insufficient_cash",
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
  "latest_transition",
  "done_after_submit",
}


def code_version():
  text = (ROOT / "Cargo.toml").read_text(encoding="utf-8")
  match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
  return match.group(1) if match else "unknown"


def command_verbs(command):
  return [
    part.strip().split(maxsplit=1)[0].lower()
    for part in command.split(";")
    if part.strip()
  ]


def advertised_verbs(legal_commands):
  text = "\n".join(legal_commands).lower()
  verbs = {
    "hold",
    "invest",
    "recruit",
    "monitor",
    "negotiate",
    "commit",
    "project",
  }
  return {verb for verb in verbs if re.search(rf"(?:^|\n){verb}(?:\s|$)", text)}


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


def expected_probe_for_turn(turn):
  return PROBE_SCHEDULE.get(turn)


def failed_run(seed, error):
  return {
    "profile_id": "adversarial_resource_probe",
    "profile_name": f"Adversarial Resource Probe / {DIFFICULTY} / seed {seed}",
    "persona_prompt": (
      "Probe visible cash, action-point, and concurrent-project limits, then "
      "recover with hold and preserve the rejected command trace."
    ),
    "decision_source": "fixed commands using actor-visible MCP legal hints",
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
      observation = session["observation"]
      legal_commands = session["legal_commands"]
      probe = expected_probe_for_turn(turn)
      command = probe["command"] if probe else "hold"
      trace = {
        "turn": turn,
        "observation": observation,
        "legal_commands": legal_commands,
        "planned_command": command,
        "submitted_command": command,
        "validation_failures": [],
        "retry_commands": [],
        "turn_after_failure": None,
        "latest_transition": None,
        "done_after_submit": False,
      }

      missing_verbs = sorted(
        set(command_verbs(command)) - advertised_verbs(legal_commands)
      )
      if missing_verbs:
        trace["legal_hint_gap"] = missing_verbs
        unexpected_failures.append({
          "turn": turn,
          "command": command,
          "error": f"probe verbs absent from legal hints: {', '.join(missing_verbs)}",
          "code": "legal_hint_gap",
        })

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
          if trace["turn_after_failure"] != turn:
            unexpected_failures.append({
              "turn": turn,
              "command": command,
              "error": "rejected command advanced the session turn",
              "code": "rejected_command_advanced",
            })

        expected_code = probe["expected_code"] if probe else None
        if not probe or expected_code != failure.get("code"):
          unexpected_failures.append({
            **failure,
            "code": "unexpected_validation_failure",
            "observed_code": failure.get("code"),
            "expected_code": expected_code,
          })
        else:
          expected_probe_failures.append(failure)

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
      else:
        if probe and probe["expected_code"] is not None:
          unexpected_failures.append({
            "turn": turn,
            "command": command,
            "error": "resource probe was accepted unexpectedly",
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
        observed_code = (
          trace["validation_failures"][0].get("code")
          if trace["validation_failures"]
          else None
        )
        probe_results.append({
          "turn": turn,
          "probe_id": probe["probe_id"],
          "expected_code": probe["expected_code"],
          "observed_code": observed_code,
          "accepted": not trace["validation_failures"],
          "retry_commands": trace["retry_commands"],
          "turn_after_failure": trace["turn_after_failure"],
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

  completion_status = (
    "complete" if len(history) == EXPECTED_TRANSITIONS else "incomplete"
  )
  return {
    "profile_id": "adversarial_resource_probe",
    "profile_name": f"Adversarial Resource Probe / {DIFFICULTY} / seed {seed}",
    "persona_prompt": (
      "Probe visible cash, action-point, and concurrent-project limits, then "
      "recover with hold and preserve the rejected command trace."
    ),
    "decision_source": "fixed commands using actor-visible MCP legal hints",
    "seed": seed,
    "difficulty": DIFFICULTY,
    "completion_status": completion_status,
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


def control_summary():
  source = json.loads((ROOT / CONTROL_ARTIFACT).read_text(encoding="utf-8"))
  runs = [
    run
    for run in source["runs"]
    if run["profile_name"].startswith(CONTROL_PROFILE_PREFIX)
  ]
  if {run["seed"] for run in runs} != set(SEEDS):
    raise AssertionError("v0.10.50 control does not cover seeds 42, 43, and 44")
  if any(
    run["completion_status"] != "complete"
    or run["transition_count"] != EXPECTED_TRANSITIONS
    for run in runs
  ):
    raise AssertionError("v0.10.50 control contains an incomplete run")
  return [
    {
      "profile_name": run["profile_name"],
      "seed": run["seed"],
      "completion_status": run["completion_status"],
      "transition_count": run["transition_count"],
      "final_hash": run["final_hash"],
    }
    for run in sorted(runs, key=lambda item: item["seed"])
  ]


def build_artifact(runs, controls):
  return {
    "filename": "results.json",
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "difficulty": DIFFICULTY,
    "seeds": SEEDS,
    "profile": "Adversarial Resource Probe",
    "evidence_type": (
      "deterministic observation-driven resource-limit and retry capture"
    ),
    "control_artifact": CONTROL_ARTIFACT,
    "control_profile": "First-Time Executive",
    "control_runs": controls,
    "expected_probe_schedule": PROBE_SCHEDULE,
    "runs": runs,
  }


def validate_artifact(artifact):
  assert artifact["batch_id"] == BATCH_ID
  assert artifact["code_version"] == CODE_VERSION
  assert artifact["campaign"] == CAMPAIGN
  assert artifact["difficulty"] == DIFFICULTY
  assert artifact["seeds"] == SEEDS
  assert len(artifact["runs"]) == len(SEEDS)
  assert [run["seed"] for run in artifact["runs"]] == SEEDS
  assert len(artifact["control_runs"]) == len(SEEDS)

  expected_probe_count = sum(
    probe["expected_code"] is not None
    for probe in PROBE_SCHEDULE.values()
  )
  for run in artifact["runs"]:
    assert run["completion_status"] == "complete"
    assert run["transition_count"] == EXPECTED_TRANSITIONS
    assert len(run["turn_trace"]) == EXPECTED_TRANSITIONS
    assert len(run["expected_probe_failures"]) == expected_probe_count
    assert run["unexpected_failures"] == []
    assert run["retry_count"] == expected_probe_count
    assert len(run["probe_results"]) == len(PROBE_SCHEDULE)
    assert run["debrief"]
    for entry in run["turn_trace"]:
      assert REQUIRED_TRACE_FIELDS <= set(entry)
      if entry["validation_failures"]:
        assert entry["turn_after_failure"] == entry["turn"]
        assert entry["retry_commands"] == ["hold"]
      assert entry["latest_transition"]

    for result in run["probe_results"]:
      expected = PROBE_SCHEDULE[result["turn"]]
      assert result["probe_id"] == expected["probe_id"]
      assert result["expected_code"] == expected["expected_code"]
      if expected["expected_code"] is None:
        assert result["accepted"]
      else:
        assert result["observed_code"] == expected["expected_code"]
        assert result["accepted"] is False
        assert result["turn_after_failure"] == result["turn"]


def render_diagnostics(artifact):
  lines = [
    "# Adversarial Resource-Probe Diagnostics v0.10.51",
    "",
    f"- **Batch id:** {artifact['batch_id']}",
    f"- **Code version:** {artifact['code_version']}",
    f"- **Campaign:** `{artifact['campaign']}`",
    f"- **Difficulty:** `{artifact['difficulty']}`",
    f"- **Control:** `{artifact['control_artifact']}` / {artifact['control_profile']}",
    "- **Evidence type:** deterministic simulated-policy resource and retry probe",
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
    "| Seed | Month | Probe | Expected code | Observed code | Accepted | Retry turn |",
    "| ---: | ---: | --- | --- | --- | --- | ---: |",
  ])
  for run in artifact["runs"]:
    for result in run["probe_results"]:
      lines.append(
        f"| {run['seed']} | {result['turn']} | {result['probe_id']} | "
        f"{result['expected_code'] or 'accepted'} | "
        f"{result['observed_code'] or 'accepted'} | "
        f"{'yes' if result['accepted'] else 'no'} | "
        f"{result['turn_after_failure'] or '—'} |"
      )

  lines.extend([
    "",
    "## Interpretation",
    "",
    "- Expected validation failures are probes, not final replay failures.",
    "- A rejected command must leave the session turn unchanged; the safe `hold` retry must advance it once.",
    "- This artifact tests wrapper traceability and resource-guard compatibility, not human comprehension, exploit value, balance, winnability, or learning.",
    "- A concrete unexplained gap would require a separate runtime or interface plan.",
    "",
  ])
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
    print(f"Running adversarial resource probe / {DIFFICULTY} / seed {seed}...", flush=True)
    runs.append(run_session(seed))

  artifact = build_artifact(runs, control_summary())
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
