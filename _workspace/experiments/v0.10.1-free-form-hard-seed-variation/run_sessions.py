#!/usr/bin/env python3
"""Operator capture for free-form Hard competitive MCP seed-variation sessions."""

import json
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts"))
from play_game import McpClient  # noqa: E402


def parse_resources(legal):
  for line in legal:
    m = re.search(
      r"Available resources: AP (\d+), cash (\d+), political capital (\d+)",
      line,
    )
    if m:
      return int(m.group(1)), int(m.group(2)), int(m.group(3))
  return None, None, None


def parse_access(obs):
  for line in obs:
    m = re.search(r"Reported access index:\s*(\d+)", line)
    if m:
      return int(m.group(1))
  return None


def parse_cash_runway(obs):
  for line in obs:
    m = re.search(r"Cash runway:\s*(\w+)", line)
    if m:
      return m.group(1).upper()
  return "UNKNOWN"


def parse_workforce_trust(obs):
  for line in obs:
    m = re.search(r"Workforce trust:\s*(\w+)", line, re.IGNORECASE)
    if m:
      word = m.group(1).lower()
      if word in ("moderate", "strained", "strong", "weak"):
        return word
    m = re.search(r"Workforce trust:\s*(\d+)", line)
    if m:
      return int(m.group(1))
  return None


def obs_text(obs):
  return "\n".join(obs).upper()


def nursing_pressure(obs):
  text = obs_text(obs)
  return "VACANCY" in text or "NURSING" in text


def access_scrutiny(obs):
  text = obs_text(obs)
  return "ACCESS" in text and ("SCRUTINY" in text or "MANDATE" in text)


def rival_intel_gap(obs):
  text = obs_text(obs)
  return "INTEL GAP" in text or "NORTHLAKE" in text


def strained(runway):
  return runway in ("STRAINED", "CRITICAL")


def watch_or_worse(runway):
  return runway in ("WATCH", "STRAINED", "CRITICAL")


def policy_fiscal_steward(obs, legal, turn):
  runway = parse_cash_runway(obs)
  access = parse_access(obs) or 70
  wf = parse_workforce_trust(obs)
  ap, cash, _pc = parse_resources(legal)

  if turn == 1:
    if rival_intel_gap(obs):
      return "monitor target=northlake depth=1; hold"
    return "hold"

  if strained(runway):
    if access_scrutiny(obs) and ap and ap >= 1:
      return "commit pledge_type=access level=1; hold"
    if turn % 4 == 0 and rival_intel_gap(obs):
      return "monitor target=northlake depth=1; hold"
    return "hold"

  if access_scrutiny(obs) and ap and ap >= 1 and turn % 3 == 0:
    return "commit pledge_type=access level=1; hold"

  if nursing_pressure(obs) and wf in ("strained", "weak") and cash and cash >= 20 and ap and ap >= 1:
    return "recruit role=nurse headcount=1; hold"

  if turn % 5 == 2 and ap and ap >= 1:
    return "negotiate payer=carrier_a rate_posture=conservative; hold"

  if turn % 6 == 0 and rival_intel_gap(obs):
    return "monitor target=summit depth=1; hold"

  if access < 70 and cash and cash >= 25 and ap and ap >= 2 and turn % 4 == 1:
    return "invest domain=outpatient amount=6; hold"

  return "hold"


def policy_access_advocate(obs, legal, turn):
  runway = parse_cash_runway(obs)
  access = parse_access(obs) or 70
  ap, cash, _pc = parse_resources(legal)

  if turn == 1:
    if nursing_pressure(obs) and ap and ap >= 2:
      return "invest domain=beds amount=12; recruit role=nurse headcount=2"
    return "invest domain=beds amount=10; hold"

  if strained(runway):
    if access_scrutiny(obs) and ap and ap >= 1:
      return "commit pledge_type=access level=2; hold"
    if ap and ap >= 1:
      return "negotiate payer=carrier_a rate_posture=neutral; hold"
    return "hold"

  if access_scrutiny(obs) and ap and ap >= 1:
    return "commit pledge_type=access level=2; hold"

  if access < 72 and cash and cash >= 20 and ap and ap >= 2:
    return "invest domain=beds amount=10; hold"

  if nursing_pressure(obs) and cash and cash >= 15 and ap and ap >= 1:
    return "recruit role=nurse headcount=2; hold"

  if turn % 4 == 0 and rival_intel_gap(obs):
    return "monitor target=northlake depth=1; hold"

  if turn % 5 == 3 and ap and ap >= 1:
    return "negotiate payer=carrier_a rate_posture=neutral; hold"

  if turn % 6 == 2 and cash and cash >= 18 and ap and ap >= 2:
    return "invest domain=outpatient amount=8; hold"

  return "hold"


def policy_first_time_executive(obs, legal, turn):
  runway = parse_cash_runway(obs)
  access = parse_access(obs) or 70
  wf = parse_workforce_trust(obs)
  ap, cash, _pc = parse_resources(legal)

  if turn == 1:
    if nursing_pressure(obs) and ap and ap >= 2:
      return "recruit role=nurse headcount=2; monitor target=northlake depth=1"
    return "monitor target=northlake depth=1; hold"

  if turn == 2 and cash and cash >= 30 and ap and ap >= 2:
    return "invest domain=beds amount=10; commit pledge_type=access level=1"

  if strained(runway):
    if access_scrutiny(obs) and ap and ap >= 1:
      return "commit pledge_type=access level=1; hold"
    if ap and ap >= 1 and turn % 3 == 0:
      return "negotiate payer=carrier_a rate_posture=neutral; hold"
    return "hold"

  if wf in ("strained", "weak") and cash and cash >= 15 and ap and ap >= 1:
    return "recruit role=nurse headcount=2; hold"

  if access < 73 and cash and cash >= 20 and ap and ap >= 2 and turn % 3 == 1:
    return "invest domain=outpatient amount=6; hold"

  if access_scrutiny(obs) and ap and ap >= 1:
    return "commit pledge_type=access level=1; hold"

  if turn % 4 == 0 and cash and cash >= 25 and ap and ap >= 2:
    return "project kind=clinic_network budget=12; hold"

  if turn % 5 == 0 and rival_intel_gap(obs):
    return "monitor target=northlake depth=2; hold"

  if turn % 7 == 0 and ap and ap >= 1:
    return "negotiate payer=medicaid rate_posture=neutral; hold"

  return "hold"


PROFILES = {
  "Free-Form Fiscal Steward": {
    "prompt": (
      "Protect cash runway, favor low-risk moves, monitor rivals before "
      "committing, and use modest access commitments when legitimacy is at stake."
    ),
    "policy": policy_fiscal_steward,
  },
  "Free-Form Access Expansion Advocate": {
    "prompt": (
      "Prioritize access, staffed capacity, and public legitimacy while "
      "preserving enough cash to finish the 24-month campaign at Hard difficulty."
    ),
    "policy": policy_access_advocate,
  },
  "Free-Form First-Time Executive": {
    "prompt": (
      "Play as a first-time executive who reads only the current observation, "
      "legal command hints, and player-facing docs. Preserve cash flexibility "
      "but act on visible access, workforce, policy, and market pressure."
    ),
    "policy": policy_first_time_executive,
  },
}


def play_free_form_session(profile_name, seed=42, difficulty="hard"):
  profile = PROFILES[profile_name]
  policy_fn = profile["policy"]
  client = McpClient(timeout_seconds=60)
  client.start()
  turns = []

  try:
    res = client.call_tool(
      "start_session",
      {
        "campaign": "competitive-regional-v1",
        "seed": seed,
        "difficulty": difficulty,
      },
    )
    if res["isError"]:
      raise RuntimeError(res["error"])

    session = res["data"]
    session_id = session["session_id"]
    validation_failures = []

    while not session["done"]:
      turn = session["turn"]
      obs = session["observation"]
      legal = session["legal_commands"]
      cmd = policy_fn(obs, legal, turn)

      turn_record = {
        "turn": turn,
        "observation_summary": obs[:8],
        "legal_hint": legal[0] if legal else "",
        "command": cmd,
      }

      res = client.call_tool(
        "submit_turn",
        {"session_id": session_id, "command_text": cmd},
      )
      if res["isError"]:
        validation_failures.append(
          {"turn": turn, "command": cmd, "error": res["error"]}
        )
        raise RuntimeError(
          f"{profile_name} failed turn {turn}: {res['error']}"
        )

      session = res["data"]
      if session.get("latest_transition"):
        turn_record["transition"] = session["latest_transition"]
      turns.append(turn_record)

    res = client.call_tool("end_session", {"session_id": session_id})
    debrief = res["data"].get("debrief", []) if not res["isError"] else []

    return {
      "profile": profile_name,
      "prompt": profile["prompt"],
      "campaign": "competitive-regional-v1",
      "seed": seed,
      "difficulty": difficulty,
      "turns": turns,
      "history": [t.get("transition") for t in turns if t.get("transition")],
      "debrief": debrief,
      "final_observation": session["observation"],
      "validation_failures": validation_failures,
    }
  finally:
    client.close()


def main():
  out_dir = os.path.dirname(os.path.abspath(__file__))
  seeds = [42, 43, 44]
  results = {
    "artifact_type": "free_form_hard_playtest",
    "code_version": "0.10.1",
    "campaign": "competitive-regional-v1",
    "seeds": seeds,
    "difficulty": "hard",
    "sessions": [],
  }

  for seed in seeds:
    for name in PROFILES:
      print(f"Running {name} seed {seed}...", flush=True)
      session = play_free_form_session(name, seed=seed, difficulty="hard")
      results["sessions"].append(session)
      print(f"  completed {len(session['turns'])} months", flush=True)

  out_path = os.path.join(out_dir, "results.json")
  with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
  print(f"Wrote {out_path}")


if __name__ == "__main__":
  main()
