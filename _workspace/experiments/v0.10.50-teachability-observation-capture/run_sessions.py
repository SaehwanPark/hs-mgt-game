#!/usr/bin/env python3
"""Capture observation-driven competitive playtest traces for v0.10.50."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import McpClient  # noqa: E402


BATCH_ID = "v0.10.50-teachability-observation-capture"
CODE_VERSION = "0.10.50"
CAMPAIGN = "competitive-regional-v1"
DIFFICULTY = "hard"
SEEDS = [42, 43, 44]
EXPECTED_TRANSITIONS = 24

PROFILES = [
  {
    "id": "fiscal_steward",
    "name": "Fiscal Steward",
    "prompt": (
      "Protect cash runway, monitor rivals before committing, and use modest "
      "operational actions only when the visible report shows room."
    ),
  },
  {
    "id": "access_expansion_advocate",
    "name": "Access Expansion Advocate",
    "prompt": (
      "Prioritize access, staffed capacity, and public legitimacy while "
      "preserving enough cash to finish the Hard campaign."
    ),
  },
  {
    "id": "first_time_executive",
    "name": "First-Time Executive",
    "prompt": (
      "Read only the current actor-visible report and legal command hints; "
      "respond to visible workforce, access, payer, and market pressure."
    ),
  },
]


def observation_text(observation):
  return "\n".join(observation)


def cash_runway(observation):
  match = re.search(r"Cash runway:\s*([A-Za-z]+)", observation_text(observation))
  return match.group(1).lower() if match else "unknown"


def workforce_trust(observation):
  text = observation_text(observation)
  match = re.search(r"Workforce trust:\s*(-?\d+)", text)
  if match:
    return int(match.group(1))
  match = re.search(r"Workforce trust:\s*([A-Za-z-]+)", text)
  labels = {
    "critical": 35,
    "strained": 45,
    "moderate": 55,
    "stable": 65,
    "strong": 75,
  }
  return labels.get(match.group(1).lower()) if match else None


def reported_access(observation):
  match = re.search(r"Reported access index:\s*(-?\d+)", observation_text(observation))
  return int(match.group(1)) if match else 70


def has_visible_rival(observation):
  text = observation_text(observation).lower()
  return any(name in text for name in ("northlake", "summit", "valley"))


def legal_or_hold(command, legal_commands):
  legal_text = "\n".join(legal_commands).lower()
  for part in command.split(";"):
    verb = part.strip().split(maxsplit=1)[0].lower()
    if not re.search(rf"(?:^|\n){re.escape(verb)}(?:\s|$)", legal_text):
      return "hold"
  return command


def observation_policy(profile_id, observation, legal_commands, turn):
  """Return a command using visible observations, legal hints, and turn number."""
  runway = cash_runway(observation)
  trust = workforce_trust(observation) or 0
  access = reported_access(observation)
  rival_visible = has_visible_rival(observation)

  if profile_id == "fiscal_steward":
    if turn in (1, 6, 12, 18) and rival_visible:
      return legal_or_hold("monitor target=northlake depth=1; hold", legal_commands)
    if runway in ("strong", "stable") and turn in (2, 10):
      return legal_or_hold("recruit role=nurse headcount=2; hold", legal_commands)
    if runway in ("strong", "stable") and turn == 4:
      return legal_or_hold(
        "negotiate payer=carrier_a rate_posture=conservative; hold",
        legal_commands,
      )
    if turn == 16:
      return legal_or_hold("commit pledge_type=quality level=1; hold", legal_commands)
    return legal_or_hold("hold", legal_commands)

  if profile_id == "access_expansion_advocate":
    if turn == 1:
      return legal_or_hold(
        "monitor target=northlake depth=1; commit pledge_type=access level=1",
        legal_commands,
      )
    if turn == 2:
      return legal_or_hold(
        "recruit role=nurse headcount=2; negotiate payer=medicaid rate_posture=neutral",
        legal_commands,
      )
    if runway in ("strong", "stable") and access < 75 and turn in (3, 8):
      return legal_or_hold("invest domain=outpatient amount=2; hold", legal_commands)
    if turn in (5, 11, 17) and rival_visible:
      return legal_or_hold("monitor target=summit depth=1; hold", legal_commands)
    if trust < 55 and turn in (7, 13):
      return legal_or_hold("commit pledge_type=workforce level=1; hold", legal_commands)
    if turn == 15:
      return legal_or_hold(
        "negotiate payer=medicare rate_posture=neutral; hold",
        legal_commands,
      )
    return legal_or_hold("hold", legal_commands)

  if turn in (1, 7, 13, 19) and rival_visible:
    return legal_or_hold("monitor target=northlake depth=1; hold", legal_commands)
  if trust < 55 and turn in (2, 9):
    return legal_or_hold("recruit role=nurse headcount=2; hold", legal_commands)
  if trust < 60 and turn == 4:
    return legal_or_hold("commit pledge_type=workforce level=1; hold", legal_commands)
  if turn == 6:
    return legal_or_hold(
      "negotiate payer=carrier_a rate_posture=neutral; hold",
      legal_commands,
    )
  if runway in ("strong", "stable") and turn == 10:
    return legal_or_hold("invest domain=emergency amount=2; hold", legal_commands)
  if turn == 16:
    return legal_or_hold("commit pledge_type=quality level=1; hold", legal_commands)
  return legal_or_hold("hold", legal_commands)


def final_hash(history):
  return history[-1]["state_hash"] if history else None


def run_session(profile, seed):
  client = McpClient(timeout_seconds=60)
  client.start()
  try:
    response = client.call_tool(
      "start_session",
      {"campaign": CAMPAIGN, "seed": seed, "difficulty": DIFFICULTY},
    )
    if response["isError"]:
      raise RuntimeError(response["error"])

    session = response["data"]
    session_id = session["session_id"]
    history = []
    turn_trace = []
    validation_failures = []

    while not session["done"]:
      turn = session["turn"]
      observation = session["observation"]
      legal_commands = session["legal_commands"]
      command = observation_policy(profile["id"], observation, legal_commands, turn)
      trace = {
        "turn": turn,
        "observation": observation,
        "legal_commands": legal_commands,
        "submitted_command": command,
        "validation_failures": [],
        "retry_commands": [],
        "latest_transition": None,
        "done_after_submit": False,
      }

      response = client.call_tool(
        "submit_turn",
        {"session_id": session_id, "command_text": command},
      )
      if response["isError"]:
        failure = {"turn": turn, "command": command, "error": response["error"]}
        for field in ("code", "resource_limit", "hint"):
          if response.get(field) is not None:
            failure[field] = response[field]
        validation_failures.append(failure)
        trace["validation_failures"].append(failure)
        trace["retry_commands"].append("hold")
        response = client.call_tool(
          "submit_turn",
          {"session_id": session_id, "command_text": "hold"},
        )
        if response["isError"]:
          raise RuntimeError(
            f"{profile['id']} failed turn {turn} after safe retry: "
            f"{response['error']}"
          )

      session = response["data"]
      transition = session.get("latest_transition")
      if transition:
        history.append(transition)
        trace["latest_transition"] = transition
      trace["done_after_submit"] = session["done"]
      turn_trace.append(trace)

    response = client.call_tool("end_session", {"session_id": session_id})
    debrief = response["data"].get("debrief", []) if not response["isError"] else []
    return build_run_record(
      profile,
      seed,
      turn_trace,
      history,
      validation_failures,
      session["observation"],
      debrief,
    )
  finally:
    client.close()


def build_run_record(
  profile,
  seed,
  turn_trace,
  history,
  validation_failures,
  final_observation,
  debrief,
):
  return {
    "profile_id": profile["id"],
    "profile_name": f"{profile['name']} / {DIFFICULTY} / seed {seed}",
    "persona_prompt": profile["prompt"],
    "decision_source": (
      "deterministic observation-driven policy using actor-visible observations, "
      "legal command hints, and turn number"
    ),
    "seed": seed,
    "difficulty": DIFFICULTY,
    "completion_status": (
      "complete" if len(history) == EXPECTED_TRANSITIONS else "incomplete"
    ),
    "turn_trace": turn_trace,
    "commands": [entry["submitted_command"] for entry in turn_trace],
    "validation_failures": validation_failures,
    "retry_count": sum(len(entry["retry_commands"]) for entry in turn_trace),
    "transition_count": len(history),
    "state_hashes": [transition["state_hash"] for transition in history],
    "final_hash": final_hash(history),
    "final_observation": final_observation,
    "debrief": debrief,
  }


def build_artifact(runs):
  return {
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "difficulty": DIFFICULTY,
    "seed": ", ".join(str(seed) for seed in SEEDS),
    "seeds": SEEDS,
    "profiles": [profile["id"] for profile in PROFILES],
    "evidence_type": (
      "deterministic observation-driven competitive MCP capture for "
      "teachability, command comprehension, follow-through, and debrief use"
    ),
    "runs": runs,
  }


def main():
  os.chdir(ROOT)
  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"],
    cwd=ROOT,
    check=True,
  )
  runs = []
  for seed in SEEDS:
    for profile in PROFILES:
      print(f"Running {profile['name']} / {DIFFICULTY} / seed {seed}...", flush=True)
      runs.append(run_session(profile, seed))

  artifact_path = Path(__file__).with_name("results.json")
  artifact_path.write_text(
    json.dumps(build_artifact(runs), indent=2) + "\n",
    encoding="utf-8",
  )
  print(f"Wrote {artifact_path}")


if __name__ == "__main__":
  main()
